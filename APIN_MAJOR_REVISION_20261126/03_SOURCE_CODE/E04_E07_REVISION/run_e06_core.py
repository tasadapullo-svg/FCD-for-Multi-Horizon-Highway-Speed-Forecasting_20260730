"""Frozen E06 finite tuning and static-feature comparison; restartable via run_one."""
from g2_common import *
from data_engine import prepare
from models import run_one,config_for,materialize_test
import time
assert load(GATE/'status.json')['status']=='PASS_NEW_IMPLEMENTATION'
assert (CTL/'G2_Training_Protocol.yaml').exists()
start=time.perf_counter();result_dir=ROOT/'04_EXPERIMENTS/E06_MODEL_FAIRNESS';result_dir.mkdir(exist_ok=True)
candidates={'Ridge':[.1,1.,10.],'XGBoost':[4,8,12],'GRU':[32,64,128]}
selected={};selection=[]
for H in HS:
 data=prepare('base',1,H)
 for model,values in candidates.items():
  found=[]
  for value in values:
   meta=run_one(data,model,seed=42,config=config_for(model,value),experiment='E06_TUNE_F1',test=False)
   if not meta['status'].startswith('COMPLETED'):raise RuntimeError(f'Invalid candidate {model} H{H} {value}: {meta["status"]}')
   found.append((float(meta['validation_metrics']['MAE']),value,meta))
   selection.append({'model':model,'horizon':H,'candidate':value,'validation_MAE':found[-1][0],'run_id':meta['run_id'],'fit_seconds':meta['training_seconds'],'status':meta['status']})
  best=min(found,key=lambda x:(x[0],x[1]))
  selected[f'{model}_H{H}']={'value':best[1],'validation_MAE':best[0],'run_id':best[2]['run_id']}
  save(pd.DataFrame(selection),result_dir/'E06_Fold1_Validation_Candidates.csv');dump(result_dir/'E06_Selected_Configurations.json',selected)
  if not (ART/best[2]['run_id']/'predictions_test.parquet').exists():
   materialize_test(data,ART/best[2]['run_id'])
  log(f'E06 SELECT {model} H{H} {best[1]} validationMAE={best[0]:.6f}')
for H in HS:
 for fold in range(1,7):
  data=prepare('base',fold,H)
  for model in candidates:
   cfg=config_for(model,selected[f'{model}_H{H}']['value'])
   run_one(data,model,seed=42,config=cfg,experiment='E06_SELECTED',test=True)
  for model in ['XGBoost','GRU']:
   cfg=config_for(model,selected[f'{model}_H{H}']['value'])
   for seed in [2026,3407]:run_one(data,model,seed=seed,config=cfg,experiment='E06_SEED_STABILITY',test=True)
  static_cfg=config_for('GRU_WITH_STATIC',selected[f'GRU_H{H}']['value'])
  for seed in SEEDS:run_one(data,'GRU_WITH_STATIC',seed=seed,config=static_cfg,experiment='E06_STATIC_INFORMATION',test=True)
  log(f'E06 FOLD_DONE F{fold} H{H}')
dump(result_dir/'E06_Core_Completion.json',{'status':'COMPLETED','at':now(),'selected':selected,'elapsed_seconds':time.perf_counter()-start,'candidates':len(selection)})
