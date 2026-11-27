"""Read-only unified Fold1 H1/H6 inference benchmark. No model fitting."""
from pathlib import Path
import sys,time,json,warnings
warnings.filterwarnings('ignore',category=DeprecationWarning)
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'E04_E07_REVISION'))
from g2_common import *
from data_engine import prepare
from models import GRUNet,baseline_predict,config_for
import torch
from xgboost import XGBRegressor

OUT=ROOT/'04_EXPERIMENTS/FINAL_NONTRAINING_CLOSURE';OUT.mkdir(parents=True,exist_ok=True)
selected=load(ROOT/'04_EXPERIMENTS/E06_MODEL_FAIRNESS/E06_Selected_Configurations.json')
rows=[]
for H in [1,6]:
 data=prepare('base',1,H);ix=data.split('test')[:1024];assert len(ix)==1024
 frame=data.manifest.iloc[ix];train=data.manifest.iloc[data.split('train')]
 for model in ['HA','SeasonalHA','Persistence','Ridge','XGBoost','GRU']:
  if model=='Ridge':
   rows.append({'model':model,'horizon':H,'status':'NOT_TIMED_SVD_WEIGHT_NOT_SAVED','reason':'Final SVD diagnostic fit has metrics but no saved SVD model; no refit authorized','fold':1,'batch_samples':1024})
   continue
  prep_start=time.perf_counter();load_seconds=0;load_times=[];engines=[];metas=[];storage=0
  if model in ['HA','SeasonalHA','Persistence']:
   cfg=config_for(model);globalmean=float(train.y_true.mean());node=train.groupby('node_id').y_true.mean()
   if model=='HA':
    if cfg['rule']=='global_target_mean':constant=globalmean;infer=lambda:np.full(len(frame),constant)
    else:
     lookup=frame.node_id.map(node).fillna(globalmean).to_numpy();infer=lambda:lookup.copy()
    storage=8 if cfg['rule']=='global_target_mean' else int(node.memory_usage(deep=True))
   elif model=='Persistence':
    infer=lambda:data.filled[ix];storage=0
   else:
    a=train.copy();b=frame.copy();rule=cfg['rule'];offset=H if rule=='node_target_hour_weekday' else 0
    for x in [a,b]:x['hod']=(x.forecast_origin+pd.Timedelta(hours=offset)).dt.hour;x['dow']=(x.forecast_origin+pd.Timedelta(hours=offset)).dt.dayofweek
    keys=['node_id','hod']+(['dow'] if rule!='node_hour' else [])
    stat=a.groupby(keys).y_true.mean();key=pd.MultiIndex.from_frame(b[keys]);fallback=b.node_id.map(node).fillna(globalmean).to_numpy()
    def infer():
     values=stat.reindex(key).to_numpy()
     return np.where(np.isfinite(values),values,fallback)
    storage=int(stat.memory_usage(deep=True)+node.memory_usage(deep=True)+8)
   reference=baseline_predict(model,train,frame,data,cfg)
   assert np.allclose(infer(),reference,rtol=0,atol=1e-10)
   labels=[('single_deterministic',infer,[])]
  else:
   field={'XGBoost':'max_depth','GRU':'hidden_size'}[model];val=selected[f'{model}_H{H}']['value']
   for seed in [42,2026,3407]:
    match=[]
    for f in ART.glob('*/run.json'):
     m=load(f)
     if m.get('status')=='COMPLETED' and m.get('condition')=='base' and m.get('fold')==1 and m.get('horizon')==H and m.get('model')==model and m.get('seed')==seed and m.get('configuration',{}).get(field)==val:match.append(m)
    assert len(match)==1,(model,H,seed,len(match))
    meta=match[0];folder=ART/meta['run_id'];metas.append(meta)
    t=time.perf_counter()
    if model=='XGBoost':
     engine=XGBRegressor();engine.load_model(folder/'model.ubj');size=(folder/'model.ubj').stat().st_size
    else:
     z=torch.load(folder/'weights.pt',map_location='cpu',weights_only=True);engine=GRUNet(z['configuration']['hidden_size'],z['input_size'],False);engine.load_state_dict(z['state_dict']);engine.eval();engine=(engine,z['y_mean'],z['y_std']);size=(folder/'weights.pt').stat().st_size
    elapsed_load=time.perf_counter()-t;load_seconds+=elapsed_load;load_times.append(elapsed_load);storage+=size;engines.append(engine)
   if model=='GRU':x=torch.from_numpy(np.ascontiguousarray(data.X[ix]))
   else:x=data.tabular()[ix]
   def one(engine):
    if model=='GRU':
     net,ym,ys=engine
     with torch.inference_mode():return net(x).numpy()*ys+ym
    return engine.predict(x)
   labels=[('single_seed',lambda:one(engines[0]),metas[:1]),('three_seed_ensemble',lambda:np.mean([one(e) for e in engines],axis=0),metas)]
  prep_seconds=time.perf_counter()-prep_start-load_seconds
  for label,infer,used in labels:
   ref=infer();assert len(ref)==1024 and np.isfinite(ref).all()
   for _ in range(20):infer()
   elapsed=[]
   for _ in range(100):
    t=time.perf_counter();v=infer();elapsed.append(time.perf_counter()-t)
   assert np.allclose(v,ref,rtol=1e-6,atol=1e-5)
   rows.append({'model':model,'horizon':H,'status':'MEASURED','execution':label,'device':'CPU','torch_threads':torch.get_num_threads(),'fold':1,'batch_samples':1024,'warmup_batches':20,'measured_batches':100,'reference_or_input_preparation_seconds':prep_seconds,'model_loading_seconds':(load_times[0] if label=='single_seed' else load_seconds),'mean_batch_seconds':float(np.mean(elapsed)),'median_batch_seconds':float(np.median(elapsed)),'p95_batch_seconds':float(np.percentile(elapsed,95)),'mean_seconds_per_sample':float(np.mean(elapsed)/1024),'storage_bytes':storage if label!='single_seed' else (used[0].get('model_size_bytes',0) if used else storage),'run_ids':'|'.join(m['run_id'] for m in used),'timing_boundary':'in-memory prepared 1024 inputs; model/reference loaded; batch predict only; no disk I/O or feature preparation'})
   pd.DataFrame(rows).to_csv(OUT/'Final_Unified_Inference_Benchmark.csv',index=False)
   print(model,H,label,rows[-1]['mean_batch_seconds'],flush=True)
(OUT/'Computational_Efficiency_Boundary_Notes.md').write_text('所有可直接加载模型在同机 CPU、Fold1 H1/H6、相同 1024 测试样本、20 预热/100 测量重新计时；模型加载、参考统计、输入准备在计时外。SeasonalHA 使用训练期预建统计表并在计时内查表/回退，规则与原实现预测逐值对照。学习模型只计载入特征后的 predict。准备时间包含运行元数据查找和预测一致性检查，属于本次测量工作开销，不等于模型训练时间；单seed加载时间只计对应权重，三seed计全部权重。Ridge 最终 SVD 权重未保存，因此不为计时重新拟合；旧 Cholesky 计时不作为最终 Ridge 数字。准备、加载和纯推理分别列示；不代表线上 API 延迟或经济收益。\n',encoding='utf-8')
