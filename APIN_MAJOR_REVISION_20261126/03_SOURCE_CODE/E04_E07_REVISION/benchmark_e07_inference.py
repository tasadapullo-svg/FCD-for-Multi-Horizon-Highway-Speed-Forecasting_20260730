"""Fixed Fold1 H1/H6 CPU inference benchmark; 20 warm-up and 100 measured batches."""
from g2_common import *
from data_engine import prepare
from models import GRUNet
import torch,joblib,time
from xgboost import XGBRegressor
OUT=ROOT/'04_EXPERIMENTS/E07_SPATIAL_OPERATIONAL';OUT.mkdir(exist_ok=True)
selected=load(ROOT/'04_EXPERIMENTS/E06_MODEL_FAIRNESS/E06_Selected_Configurations.json')
rows=[]
for H in [1,6]:
 data=prepare('base',1,H);te=data.split('test');n=min(1024,len(te));assert n>0
 for model in ['Ridge','XGBoost','GRU']:
  field={'Ridge':'alpha','XGBoost':'max_depth','GRU':'hidden_size'}[model];value=selected[f'{model}_H{H}']['value'];metas=[];engines=[]
  for seed in ([42] if model=='Ridge' else [42,2026,3407]):
   matching=[]
   for f in ART.glob('*/run.json'):
    m=load(f)
    if m.get('status')=='COMPLETED' and m.get('condition')=='base' and m.get('fold')==1 and m.get('horizon')==H and m.get('model')==model and m.get('seed')==seed and m.get('configuration',{}).get(field)==value:matching.append(m)
   if len(matching)!=1:raise RuntimeError(f'Expected one completed selected {model} F1 H{H} seed{seed}, found {len(matching)}')
   meta=matching[0];folder=ART/meta['run_id'];metas.append(meta)
   if model=='Ridge':engine=joblib.load(folder/'model.joblib')
   elif model=='XGBoost':engine=XGBRegressor();engine.load_model(folder/'model.ubj')
   else:
    z=torch.load(folder/'weights.pt',map_location='cpu',weights_only=True);engine=GRUNet(z['configuration']['hidden_size'],z['input_size'],False);engine.load_state_dict(z['state_dict']);engine.eval();engine=(engine,z['y_mean'],z['y_std'])
   engines.append(engine)
  if model=='GRU':x=torch.from_numpy(np.ascontiguousarray(data.X[te[:n]]))
  else:x=data.tabular()[te[:n]]
  def infer(engine):
   if model=='GRU':
    net,ym,ys=engine
    with torch.inference_mode():return net(x).numpy()*ys+ym
   return engine.predict(x)
  def bench(which):
   for _ in range(20):
    for engine in which:infer(engine)
   times=[]
   for _ in range(100):
    t=time.perf_counter();preds=[infer(engine) for engine in which]
    if len(preds)>1:np.mean(preds,axis=0)
    times.append(time.perf_counter()-t)
   return float(np.median(times)),float(np.mean(times))
  for label,which in [('single_seed',[engines[0]])]+([('three_seed_ensemble',engines)] if len(engines)==3 else []):
   selected_metas=metas[:1] if label=='single_seed' else metas
   median,mean=bench(which);rows.append({'model':model,'fold':1,'horizon':H,'execution':label,'device':'CPU','batch_samples':n,'warmup_batches':20,'measured_batches':100,'median_batch_seconds':median,'mean_batch_seconds':mean,'mean_seconds_per_sample':mean/n,'run_ids':'|'.join(m['run_id'] for m in selected_metas),'total_model_bytes':sum(m.get('model_size_bytes',0) for m in selected_metas),'source':'actual new-PC inference, pretrained current-revision models'})
   save(pd.DataFrame(rows),OUT/'E07_New_PC_Inference_Benchmark.csv');log(f'E07 BENCH {model} H{H} {label} {mean:.6f}s/batch')
