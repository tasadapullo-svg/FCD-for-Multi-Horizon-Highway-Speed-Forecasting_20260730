from g2_common import *
import torch,copy,joblib
from torch import nn
from sklearn.linear_model import Ridge
from xgboost import XGBRegressor
torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
IMPLEMENTATION='REVISION_INDEPENDENT_IMPLEMENTATION_v1'
class GRUNet(nn.Module):
 def __init__(self,hidden=64,input_size=13,static=False):
  super().__init__();self.gru=nn.GRU(input_size,hidden,batch_first=True);self.head=nn.Sequential(nn.LayerNorm(hidden+(3 if static else 0)),nn.Linear(hidden+(3 if static else 0),1));self.static=static
 def forward(self,x,s=None):
  _,h=self.gru(x);z=h[-1]
  if self.static:z=torch.cat([z,s],dim=-1)
  return self.head(z).squeeze(-1)
def config_for(model,value=None):
 if model=='Ridge':return {'alpha':1. if value is None else float(value),'solver':'cholesky','fit_intercept':True}
 if model=='XGBoost':return {'n_estimators':500,'max_depth':8 if value is None else int(value),'learning_rate':.05,'subsample':.8,'colsample_bytree':.8,'objective':'reg:squarederror','tree_method':'hist','n_jobs':10}
 if model.startswith('GRU') or model=='NEIGHBOR_AWARE_GRU':return {'hidden_size':64 if value is None else int(value),'num_layers':1,'batch_size':256,'maximum_epochs':30,'patience':5,'learning_rate':.001,'weight_decay':.0001,'loss':'MSE_standardized_y','optimizer':'AdamW','gradient_clip_norm':1.,'static':model!='GRU'}
 if model=='SeasonalHA':return {'rule':load(GATE/'baseline_rules.json').get('SeasonalHA','node_hour_weekday'),'fallback':'node_target_mean_then_corridor_target_mean'}
 if model=='HA':return {'rule':load(GATE/'baseline_rules.json').get('HA','global_target_mean')}
 return {'rule':'last_causally_filled_speed'}
def baseline_predict(model,train,frame,data,config):
 globalmean=float(train.y_true.mean());nodemean=train.groupby('node_id').y_true.mean()
 if model=='HA':return np.full(len(frame),globalmean) if config['rule']=='global_target_mean' else frame.node_id.map(nodemean).fillna(globalmean).to_numpy()
 if model=='Persistence':return data.filled[frame.index]
 a=train.copy();b=frame.copy();rule=config.get('rule','node_hour_weekday');H=int(a.horizon.iloc[0]);offset=H if rule=='node_target_hour_weekday' else 0
 for x in [a,b]:x['hod']=(x.forecast_origin+pd.Timedelta(hours=offset)).dt.hour;x['dow']=(x.forecast_origin+pd.Timedelta(hours=offset)).dt.dayofweek
 keys=['node_id','hod']+(['dow'] if rule!='node_hour' else []);stat=a.groupby(keys).y_true.mean();values=stat.reindex(pd.MultiIndex.from_frame(b[keys])).to_numpy();fallback=b.node_id.map(nodemean).fillna(globalmean).to_numpy();return np.where(np.isfinite(values),values,fallback)
def run_one(data,model,seed=42,config=None,experiment='BASELINE',test=True):
 cfg=config or config_for(model);ident={'implementation':IMPLEMENTATION,'condition':data.meta['condition'],'model':model,'fold':data.meta['fold'],'horizon':data.meta['horizon'],'seed':seed,'configuration':cfg,'split_hashes':data.meta['split_hashes'],'schema_hash':data.meta['schema_sha256'],'target':'future_observed_window_mean','preprocessing':'revision_data_v2'};runid=digest(ident)[:24];folder=ART/runid;folder.mkdir(exist_ok=True);meta_path=folder/'run.json'
 if meta_path.exists():
  meta=load(meta_path)
  if meta.get('status') in ['COMPLETED','COMPLETED_VALIDATION_ONLY']:
   with (LOG/'reuse_events.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps({'at':now(),'run_id':runid,'experiment':experiment,'status':'REUSED_RUN'})+'\n')
   if test and not (folder/'predictions_test.parquet').exists():materialize_test(data,folder)
   return load(meta_path)
 tr=data.split('train');va=data.split('validation');te=data.split('test');meta={**ident,'run_id':runid,'experiment_first_use':experiment,'status':'RUNNING','started_at':now(),'artifact_folder':str(folder),'support':data.meta['support'],'preprocess_seconds':data.meta['preprocess_seconds'],'config_id':digest(cfg),'manifest_path':str(data.folder/'manifest.parquet'),'manifest_sha256':data.meta['manifest_sha256'],'model_fit':model not in ['HA','SeasonalHA','Persistence'],'deterministic_execution':model in ['HA','SeasonalHA','Persistence'],'validation_only':not test};dump(meta_path,meta)
 if min(len(tr),len(va),len(te))==0:
  meta.update(status='NOT_ESTIMABLE_EMPTY_SPLIT',ended_at=now());dump(meta_path,meta);return meta
 log(f'FIT {experiment} {model} F{data.meta["fold"]} H{data.meta["horizon"]} S{seed} {cfg.get("max_depth",cfg.get("hidden_size",cfg.get("alpha","")))} n={len(tr)}/{len(va)}/{len(te)}')
 try:
  start=time.perf_counter();np.random.seed(seed);torch.manual_seed(seed);y=data.manifest.y_true.to_numpy(dtype=np.float32);modeltype='baseline';state={}
  if model in ['HA','SeasonalHA','Persistence']:
   train=data.manifest.iloc[tr];predva=baseline_predict(model,train,data.manifest.iloc[va],data,cfg);state={'train_reference':str(data.folder/'manifest.parquet'),'configuration':cfg};dump(folder/'baseline.json',state)
  elif model=='Ridge':
   x=data.tabular();learner=Ridge(**cfg);learner.fit(x[tr],y[tr]);predva=learner.predict(x[va]);joblib.dump(learner,folder/'model.joblib');modeltype='sklearn'
  elif model=='XGBoost':
   x=data.tabular();learner=XGBRegressor(**cfg,random_state=seed);learner.fit(x[tr],y[tr],verbose=False);predva=learner.predict(x[va]);learner.save_model(folder/'model.ubj');modeltype='xgboost'
  else:
   x=np.asarray(data.X,dtype=np.float32);s=np.asarray(data.static_scaled,dtype=np.float32);net=GRUNet(cfg['hidden_size'],x.shape[-1],cfg['static']);optimizer=torch.optim.AdamW(net.parameters(),lr=cfg['learning_rate'],weight_decay=cfg['weight_decay']);ym=float(y[tr].mean());ys=float(y[tr].std(ddof=0));ys=ys if ys>0 else 1.;yt=(y-ym)/ys;lossfn=nn.MSELoss();trainx=torch.from_numpy(x[tr].copy());trainy=torch.from_numpy(yt[tr].copy());trains=torch.from_numpy(s[tr].copy());best=np.inf;beststate=None;stale=0;curves=[];valtime=0.
   for epoch in range(1,cfg['maximum_epochs']+1):
    net.train();order=torch.randperm(len(tr));loss_sum=0.;epstart=time.perf_counter()
    for ix in order.split(cfg['batch_size']):
     optimizer.zero_grad(set_to_none=True);out=net(trainx[ix],trains[ix] if cfg['static'] else None);loss=lossfn(out,trainy[ix]);loss.backward();nn.utils.clip_grad_norm_(net.parameters(),cfg['gradient_clip_norm']);optimizer.step();loss_sum+=float(loss.detach())*len(ix)
    vs=time.perf_counter();predva=predict_net(net,x[va],s[va],ym,ys);vmae=metrics(y[va],predva)['MAE'];valtime+=time.perf_counter()-vs;curves.append({'epoch':epoch,'train_MSE_standardized':loss_sum/len(tr),'validation_MAE_kmh':vmae,'seconds':time.perf_counter()-epstart})
    if vmae<best:best=vmae;beststate=copy.deepcopy(net.state_dict());best_epoch=epoch;stale=0
    else:stale+=1
    if epoch==1 or epoch%5==0:log(f'EPOCH {runid[:8]} {epoch} valMAE={vmae:.6f} sec={curves[-1]["seconds"]:.2f}')
    save(pd.DataFrame(curves),folder/'training_curve.csv')
    if stale>=cfg['patience']:break
   assert beststate is not None;net.load_state_dict(beststate);torch.save({'state_dict':beststate,'y_mean':ym,'y_std':ys,'configuration':cfg,'input_size':x.shape[-1],'best_epoch':best_epoch},folder/'weights.pt');meta.update(best_epoch=best_epoch,epochs_ran=epoch,budget_still_improving=best_epoch==epoch and epoch==cfg['maximum_epochs'],validation_seconds=valtime);predva=predict_net(net,x[va],s[va],ym,ys);modeltype='torch'
  fit_seconds=time.perf_counter()-start;assert np.isfinite(predva).all();meta.update(training_seconds=fit_seconds,validation_metrics=metrics(y[va],predva),model_type=modeltype);save_predictions(data,va,predva,model,seed,cfg,runid,folder/'predictions_validation.parquet');meta['status']='COMPLETED_VALIDATION_ONLY';meta['ended_at']=now();meta['model_size_bytes']=sum(p.stat().st_size for p in folder.iterdir() if p.suffix in ['.pt','.ubj','.joblib','.json'] and p.name!='run.json');dump(meta_path,meta)
  if test:materialize_test(data,folder)
  log(f'DONE {runid[:8]} {model} fit={fit_seconds:.2f}s valMAE={meta["validation_metrics"]["MAE"]:.6f}');return load(meta_path)
 except Exception as e:
  import traceback
  meta.update(status='FAILED',error=str(e),traceback=traceback.format_exc(),ended_at=now());dump(meta_path,meta);log('FAILED '+runid+' '+str(e));raise
def predict_net(net,x,s,ym,ys):
 net.eval();pred=[]
 with torch.inference_mode():
  for begin in range(0,len(x),1024):pred.append(net(torch.from_numpy(np.ascontiguousarray(x[begin:begin+1024])),torch.from_numpy(np.ascontiguousarray(s[begin:begin+1024])) if net.static else None).numpy()*ys+ym)
 return np.concatenate(pred)
def save_predictions(data,ix,pred,model,seed,cfg,runid,path):
 df=data.manifest.iloc[ix][['sample_id','node_id','forecast_origin','forecast_decision_time','target_interval_start','target_interval_end','fold','horizon','y_true','split','history_coverage_ratio','max_gap_24h','volatility_24h']].copy();df['y_pred']=pred;df['model']=model;df['seed']=seed;df['run_id']=runid;df['implementation']=IMPLEMENTATION;df['condition']=data.meta['condition'];df['manifest_sha256']=data.meta['manifest_sha256'];df['config_id']=digest(cfg);df['target_definition']='future_observed_window_mean';save(df,path)
def materialize_test(data,folder):
 meta=load(folder/'run.json');model=meta['model'];cfg=meta['configuration'];tr=data.split('train');te=data.split('test');begin=time.perf_counter()
 if meta['model_type']=='baseline':p=baseline_predict(model,data.manifest.iloc[tr],data.manifest.iloc[te],data,cfg)
 elif meta['model_type']=='sklearn':learner=joblib.load(folder/'model.joblib');p=learner.predict(data.tabular()[te])
 elif meta['model_type']=='xgboost':learner=XGBRegressor();learner.load_model(folder/'model.ubj');p=learner.predict(data.tabular()[te])
 else:
  z=torch.load(folder/'weights.pt',map_location='cpu',weights_only=True);net=GRUNet(cfg['hidden_size'],z['input_size'],cfg['static']);net.load_state_dict(z['state_dict']);p=predict_net(net,data.X[te],data.static_scaled[te],z['y_mean'],z['y_std'])
 assert len(p)==len(te) and np.isfinite(p).all();save_predictions(data,te,p,model,meta['seed'],cfg,meta['run_id'],folder/'predictions_test.parquet');meta.update(status='COMPLETED',inference_seconds=time.perf_counter()-begin,test_metrics=metrics(data.manifest.y_true.to_numpy()[te],p),prediction_path=str(folder/'predictions_test.parquet'),prediction_sha256=sha(folder/'predictions_test.parquet'));dump(folder/'run.json',meta)

