"""Frozen E05 grid protocol and deliberately leaky scaler diagnostic."""
from g2_common import *
from data_engine import prepare
from models import run_one
import time,sys
assert load(GATE/'status.json')['status']=='PASS_NEW_IMPLEMENTATION'
OUT=ROOT/'04_EXPERIMENTS/E05_ABLATION';OUT.mkdir(exist_ok=True);start=time.perf_counter()
stages=sys.argv[1:] or ['returned_only','leaky_scaling']
for stage in stages:
 if stage not in ['returned_only','leaky_scaling']:raise ValueError(stage)
 for H in [1,6]:
  for fold in range(1,7):
   base=prepare('base',fold,H);other=prepare(stage,fold,H)
   if stage=='leaky_scaling':
    a=base.manifest[['sample_id','y_true','split']];b=other.manifest[['sample_id','y_true','split']]
    assert a.equals(b),f'Leaky scaler changed sample/target F{fold} H{H}'
   else:
    a=base.manifest.set_index('sample_id').y_true;b=other.manifest.set_index('sample_id').y_true
    common=a.index.intersection(b.index);assert len(common)>0 and np.allclose(a.loc[common],b.loc[common],atol=0,rtol=0)
    dump(OUT/f'E05_Returned_Only_Support_F{fold}_H{H}.json',{'common_origin_count':len(common),'base_count':len(a),'returned_count':len(b),'median_returned_history_span_hours':float(other.manifest.history_span_hours.median()),'same_wallclock_targets_on_common_samples':True,'interpretation':'returned-event history is not a 24-hour history'})
   for model in ['Ridge','XGBoost']:
    run_one(base,model,seed=42,experiment='E05_MATCHED_FULL_GRID',test=True)
    run_one(other,model,seed=42,experiment='E05_'+stage.upper(),test=True)
   log(f'E05 CONDITION_DONE {stage} F{fold} H{H}')
 dump(OUT/f'E05_{stage}_completion.json',{'status':'COMPLETED','at':now(),'elapsed_seconds_since_command_start':time.perf_counter()-start,'leakage_control':stage=='leaky_scaling','legitimate_performance_rank':stage!='leaky_scaling'})
