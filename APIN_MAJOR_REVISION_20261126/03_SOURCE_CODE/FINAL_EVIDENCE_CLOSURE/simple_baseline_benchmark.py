"""Targeted CPU inference timing of the three accepted deterministic baselines."""
import sys,time,json,warnings
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'E04_E07_REVISION'))
from data_engine import prepare
from g2_common import ROOT,pd,np,sha

def baseline_predict(model,train,frame,data,config):
 globalmean=float(train.y_true.mean());nodemean=train.groupby('node_id').y_true.mean()
 if model=='HA':return np.full(len(frame),globalmean) if config['rule']=='global_target_mean' else frame.node_id.map(nodemean).fillna(globalmean).to_numpy()
 if model=='Persistence':return data.filled[frame.index]
 a=train.copy();b=frame.copy();rule=config['rule'];H=int(a.horizon.iloc[0]);offset=H if rule=='node_target_hour_weekday' else 0
 for x in (a,b):x['hod']=(x.forecast_origin+pd.Timedelta(hours=offset)).dt.hour;x['dow']=(x.forecast_origin+pd.Timedelta(hours=offset)).dt.dayofweek
 keys=['node_id','hod']+(['dow'] if rule!='node_hour' else []);stat=a.groupby(keys).y_true.mean();values=stat.reindex(pd.MultiIndex.from_frame(b[keys])).to_numpy();fallback=b.node_id.map(nodemean).fillna(globalmean).to_numpy();return np.where(np.isfinite(values),values,fallback)

def config_for(model):
 if model=='HA':return {'rule':json.loads((ROOT/'04_EXPERIMENTS/SOURCE_GATE/baseline_rules.json').read_text(encoding='utf-8'))['HA']}
 if model=='SeasonalHA':return {'rule':json.loads((ROOT/'04_EXPERIMENTS/SOURCE_GATE/baseline_rules.json').read_text(encoding='utf-8'))['SeasonalHA']}
 return {'rule':'last_causally_filled_speed'}

out=ROOT/'04_EXPERIMENTS/FINAL_TARGETED_CHECKS';out.mkdir(parents=True,exist_ok=True)
warnings.filterwarnings('ignore',category=DeprecationWarning)
rows=[]
source_sha256=sha(ROOT/'03_CODE/E04_E07_REVISION/models.py')
for H in (1,6):
 data=prepare('base',1,H);frame=data.manifest.iloc[data.split('test')[:1024]];train=data.manifest.iloc[data.split('train')]
 assert len(frame)==1024
 for model in ('HA','SeasonalHA','Persistence'):
  cfg=config_for(model)
  def infer():return baseline_predict(model,train,frame,data,cfg)
  ref=infer();assert len(ref)==1024 and np.isfinite(ref).all()
  for _ in range(20):infer()
  times=[]
  for _ in range(100):
   t=time.perf_counter();p=infer();times.append(time.perf_counter()-t)
  assert np.array_equal(ref,p)
  rows.append(dict(model=model,fold=1,horizon=H,execution='single_deterministic',device='CPU',batch_samples=1024,warmup_batches=20,measured_batches=100,mean_batch_seconds=float(np.mean(times)),median_batch_seconds=float(np.median(times)),p95_batch_seconds=float(np.percentile(times,95)),mean_seconds_per_sample=float(np.mean(times)/1024),train_reference_rows=len(train),train_reference_bytes=int(train.memory_usage(deep=True).sum()),timing_boundary='baseline_predict full in-memory training-reference groupby + lookup; manifest and filled array already loaded; no disk I/O or feature preparation',manifest_sha256=sha(data.folder/'manifest.parquet'),model_source_sha256=source_sha256))
 pd.DataFrame(rows).to_csv(out/'Simple_Baseline_Inference_Benchmark.csv',index=False)
 print(model,H,rows[-1]['mean_batch_seconds'],flush=True)
old=pd.read_csv(ROOT/'04_EXPERIMENTS/E07_SPATIAL_OPERATIONAL/E07_New_PC_Inference_Benchmark.csv')
old['p95_batch_seconds']=np.nan;old['train_reference_rows']=np.nan;old['train_reference_bytes']=np.nan
old['timing_boundary']='pretrained model.predict on in-memory preprocessed features; no feature preparation or disk I/O'
combined=pd.concat([pd.DataFrame(rows),old],ignore_index=True,sort=False)
combined.to_csv(out/'Final_Computational_Efficiency_Table.csv',index=False)
(out/'Efficiency_Comparison_Notes.md').write_text('# 简单基准计算效率补测\n\nFold 1、H1/H6、CPU、共同前1024测试样本、20次预热及100次计时。简单基准使用原 `baseline_predict` 逐批调用，HA/SeasonalHA 包含训练参考表的内存 groupby 与查表；Persistence 读取已装载数组。学习模型沿用 G2 已验收的预处理特征 `predict` 计时。两类计时边界不同，不能直接作为严格模型速度排名，也未包括原始数据读取或特征准备。表中 P95 只对本次简单基准有实测值。计时不是经济收益或线上延迟。\n',encoding='utf-8')
