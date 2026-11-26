"""Map logged sklearn LinAlgWarning instances to immutable G2 Ridge Run IDs."""
from pathlib import Path
import re
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'04_EXPERIMENTS/FINAL_TARGETED_CHECKS'
reg=pd.read_csv(ROOT/'04_EXPERIMENTS/G2_E04_E07_ACCEPTANCE/G2_02_Experiment_Run_Registry.csv')
ridge=reg[reg.model=='Ridge'].copy()
by_prefix={str(r.run_id)[:8]:r for r in ridge.itertuples(index=False)}
events=[];unmapped=[]
for path in (ROOT/'04_EXPERIMENTS').glob('**/*.log'):
    pending=[];fit=''
    for lineno,line in enumerate(path.read_text(encoding='utf-8',errors='replace').splitlines(),1):
        if 'FIT ' in line and ' Ridge ' in line:fit=line
        if 'LinAlgWarning: An ill-conditioned matrix' in line:
            match=re.search(r'rcond\s*=\s*([0-9.eE+-]+)',line)
            pending.append((lineno,float(match.group(1).rstrip('.')) if match else None,fit))
        done=re.search(r'\bDONE\s+([0-9a-f]{8})\s+Ridge\b',line)
        if done and pending:
            prefix=done.group(1)
            for warning_line,rcond,fit_line in pending:
                if prefix in by_prefix:
                    run=by_prefix[prefix]
                    events.append({'run_id':run.run_id,'warning_log':str(path.relative_to(ROOT)).replace('\\','/'),'warning_line':warning_line,'rcond':rcond,'fit_log_line':fit_line})
                else:unmapped.append({'prefix':prefix,'log':str(path),'line':warning_line})
            pending=[]
    for warning_line,rcond,fit_line in pending:unmapped.append({'prefix':'NO_DONE_AFTER_WARNING','log':str(path),'line':warning_line,'fit_log_line':fit_line,'rcond':rcond})

event_df=pd.DataFrame(events)
if not event_df.empty:
    agg=event_df.groupby('run_id').agg(warning_events=('run_id','size'),min_rcond=('rcond','min'),warning_logs=('warning_log',lambda s:'|'.join(sorted(set(s))))).reset_index()
else:agg=pd.DataFrame(columns=['run_id','warning_events','min_rcond','warning_logs'])
allridge=ridge.merge(agg,on='run_id',how='left')
allridge['warning_logged']=allridge.warning_events.notna()
allridge['warning_events']=allridge.warning_events.fillna(0).astype(int)
cols=['run_id','status','condition','experiment_first_use','fold','horizon','seed','configuration_json','manifest_sha256','train_n','validation_n','test_n','validation_MAE','test_MAE','warning_logged','warning_events','min_rcond','warning_logs','local_artifact_relpath']
allridge[cols].to_csv(OUT/'Ridge_Affected_Run_Registry.csv',index=False,encoding='utf-8-sig')
pd.DataFrame(events).to_csv(OUT/'Ridge_Warning_Log_Events.csv',index=False,encoding='utf-8-sig')
pd.DataFrame(unmapped).to_csv(OUT/'Ridge_Unmapped_Warnings.csv',index=False,encoding='utf-8-sig')
print({'ridge_runs':len(allridge),'warning_run_ids':int(allridge.warning_logged.sum()),'warning_events':len(events),'unmapped_events':len(unmapped),'min_rcond':float(event_df.rcond.min()) if len(events) else None})
