"""Predeclared G2 daily paired tests; reads local predictions, outputs aggregates only."""
from g2_common import *
from pathlib import Path
import math
OUT=ROOT/'04_EXPERIMENTS/G2_E04_E07_ACCEPTANCE';protocol=load(CTL/'G2_Key_Comparisons_Freeze.json');assert len(protocol['comparisons'])==4
records=[]
for f in ART.glob('*/run.json'):
 try:m=load(f)
 except Exception:continue
 if m.get('status')=='COMPLETED' and m.get('prediction_path') and Path(m['prediction_path']).is_file():records.append(m)
selected=load(ROOT/'04_EXPERIMENTS/E06_MODEL_FAIRNESS/E06_Selected_Configurations.json')
def find(condition,model,fold,H,seed,field,value):
 matches=[m for m in records if m.get('condition')==condition and m.get('model')==model and m.get('fold')==fold and m.get('horizon')==H and m.get('seed')==seed and m.get('configuration',{}).get(field)==value]
 if len(matches)!=1:raise RuntimeError(f'Expected one {condition} {model} F{fold} H{H} seed{seed}, found {len(matches)}')
 return pd.read_parquet(matches[0]['prediction_path'])[['sample_id','forecast_origin','y_true','y_pred']]
def ensemble(condition,model,fold,H,field,value):
 frames=[]
 for seed in SEEDS:
  d=find(condition,model,fold,H,seed,field,value).set_index('sample_id');frames.append(d)
 x=frames[0][['forecast_origin','y_true']].copy()
 for i,d in enumerate(frames):
  assert x.index.equals(d.index) and np.allclose(x.y_true,d.y_true,atol=0,rtol=0)
  x[f'p{i}']=d.y_pred
 x['y_pred']=x[['p0','p1','p2']].mean(axis=1);return x.reset_index()[['sample_id','forecast_origin','y_true','y_pred']]
def boot(day_values,block,B,seed):
 v=np.asarray(day_values,dtype=float);n=len(v);assert n>=block;starts=np.arange(n-block+1);rng=np.random.default_rng(seed);observed=v.mean();sims=np.empty(B,dtype=float);null=v-observed
 for i in range(B):
  chosen=[]
  while len(chosen)<n:
   j=int(rng.choice(starts));chosen.extend(range(j,j+block))
  ix=np.asarray(chosen[:n]);sims[i]=v[ix].mean()
 lower,upper=np.quantile(sims,[.025,.975]);null_stats=np.empty(B,dtype=float);rng=np.random.default_rng(seed+block)
 for i in range(B):
  chosen=[]
  while len(chosen)<n:
   j=int(rng.choice(starts));chosen.extend(range(j,j+block))
  null_stats[i]=null[np.asarray(chosen[:n])].mean()
 p=(1+np.count_nonzero(np.abs(null_stats)>=abs(observed)))/(B+1)
 return float(lower),float(upper),float(p)
results=[]
for spec in protocol['comparisons']:
 name=spec['id'];days=[];sample_deltas=[];total=0
 for fold in range(1,7):
  if name=='K1_T1_XGB_H1':ref=find('base','XGBoost',fold,1,42,'max_depth',8);alt=find('threshold1','XGBoost',fold,1,42,'max_depth',8)
  elif name=='K2_STRICT6_XGB_H6':ref=find('base','XGBoost',fold,6,42,'max_depth',8);alt=find('strict6','XGBoost',fold,6,42,'max_depth',8)
  elif name=='K3_IMPUTE_XGB_H1':ref=find('base','XGBoost',fold,1,42,'max_depth',8);alt=find('seasonal_impute','XGBoost',fold,1,42,'max_depth',8)
  else:
   hidden=selected['GRU_H1']['value'];ref=ensemble('base','GRU',fold,1,'hidden_size',hidden);alt=ensemble('base','GRU_WITH_STATIC',fold,1,'hidden_size',hidden)
  merged=ref.rename(columns={'y_true':'ref_y','y_pred':'ref_p'}).merge(alt[['sample_id','y_true','y_pred']].rename(columns={'y_true':'alt_y','y_pred':'alt_p'}),on='sample_id',validate='one_to_one')
  if merged.empty:raise RuntimeError('No common sample '+name)
  if name!='K1_T1_XGB_H1':assert np.allclose(merged.ref_y,merged.alt_y,atol=1e-8,rtol=0)
  merged['loss_delta']=np.abs(merged.alt_p-merged.ref_y)-np.abs(merged.ref_p-merged.ref_y)
  sample_deltas.extend(merged.loss_delta.to_list());merged['day']=pd.to_datetime(merged.forecast_origin).dt.normalize()
  days.extend(merged.groupby('day').loss_delta.mean().items());total+=len(merged)
 daydf=pd.DataFrame(days,columns=['day','daily_mean_delta']).groupby('day',as_index=False).daily_mean_delta.mean().sort_values('day');v=daydf.daily_mean_delta.to_numpy();lo3,hi3,p3=boot(v,3,10000,20261125);lo7,hi7,p7=boot(v,7,10000,20261125)
 results.append({'comparison_id':name,'paired_samples':total,'test_days':len(v),'sample_weighted_MAE_delta_alt_minus_ref':float(np.mean(sample_deltas)),'day_mean_MAE_delta_alt_minus_ref':float(v.mean()),'block3_CI_low':lo3,'block3_CI_high':hi3,'block3_p_two_sided':p3,'block7_CI_low':lo7,'block7_CI_high':hi7,'block7_p_descriptive':p7,'seed':20261125,'resamples':10000,'target_definition':spec['target'],'interpretation':'predeclared paired comparison; no causal event effect'})
# Holm correction across the four primary 3-day p-values.
order=np.argsort([r['block3_p_two_sided'] for r in results]);adjusted=np.empty(len(results));running=0
for rank,i in enumerate(order):running=max(running,(len(results)-rank)*results[i]['block3_p_two_sided']);adjusted[i]=min(1.,running)
for i,r in enumerate(results):r['holm_adjusted_p']=float(adjusted[i])
save(pd.DataFrame(results),OUT/'G2_Key_Comparisons_Actual.csv');print(pd.DataFrame(results)[['comparison_id','paired_samples','test_days','day_mean_MAE_delta_alt_minus_ref','block3_p_two_sided','holm_adjusted_p']].to_string(index=False))
