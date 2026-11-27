"""Frozen E04 single-factor experiments; idempotent run identifiers and local artifacts."""
from g2_common import *
from data_engine import prepare
from models import run_one
import sys,time
assert load(GATE/'status.json')['status']=='PASS_NEW_IMPLEMENTATION'
assert (CTL/'G2_Training_Protocol.yaml').exists()
OUT=ROOT/'04_EXPERIMENTS/E04_SENSITIVITY';OUT.mkdir(exist_ok=True);start=time.perf_counter()
stages={
 'matched_baselines': [('base',MODELS,HS,range(1,7))],
 'threshold1': [('threshold1',MODELS,HS,range(1,7))],
 'threshold3_h1': [('threshold3',MODELS,[1],range(1,7))],
 'strict6': [('strict6',MODELS,[6],range(1,7))],
 'seasonal_impute': [('seasonal_impute',['XGBoost','GRU','Persistence'],HS,range(1,7))],
 'history': [(c,['XGBoost','GRU'],[1,6],range(1,7)) for c in ['history12','history24_matched','history48']]
}
requested=sys.argv[1:] or list(stages)
for stage in requested:
 if stage not in stages:raise ValueError(stage)
 for condition,models,hs,folds in stages[stage]:
  for H in hs:
   for fold in folds:
    data=prepare(condition,fold,H);support=data.meta['support']
    if min(support[s]['n'] for s in ['train','validation','test'])==0:
     log(f'E04 NOT_ESTIMABLE {condition} F{fold} H{H} empty split');continue
    for model in models:
     run_one(data,model,seed=42,experiment='E04_'+stage.upper(),test=True)
    log(f'E04 CONDITION_DONE {condition} F{fold} H{H}')
 dump(OUT/f'E04_{stage}_completion.json',{'status':'COMPLETED','at':now(),'elapsed_seconds_since_command_start':time.perf_counter()-start})

