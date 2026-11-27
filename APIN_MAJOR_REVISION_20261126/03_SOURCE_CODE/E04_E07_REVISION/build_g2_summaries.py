"""Read-only aggregation of completed local G2 runs; no training or artifact duplication."""
from g2_common import *
from pathlib import Path
import collections
ACC=ROOT/'04_EXPERIMENTS/G2_E04_E07_ACCEPTANCE';ACC.mkdir(exist_ok=True)
records=[]
for p in sorted(ART.glob('*/run.json')):
 try:m=load(p)
 except Exception:continue
 records.append(m)
reuse=collections.Counter()
reuse_file=LOG/'reuse_events.jsonl'
if reuse_file.exists():
 for line in reuse_file.read_text(encoding='utf-8').splitlines():
  try:reuse[json.loads(line)['run_id']]+=1
  except Exception:pass
rows=[]
for m in records:
 support=m.get('support',{});test=m.get('test_metrics',{});val=m.get('validation_metrics',{})
 rows.append({'run_id':m.get('run_id'),'status':m.get('status'),'experiment_first_use':m.get('experiment_first_use'),'condition':m.get('condition'),'implementation':m.get('implementation'),'model':m.get('model'),'fold':m.get('fold'),'horizon':m.get('horizon'),'seed':m.get('seed'),'config_id':m.get('config_id'),'configuration_json':json.dumps(m.get('configuration',{}),ensure_ascii=False,sort_keys=True),'manifest_sha256':m.get('manifest_sha256'),'train_n':support.get('train',{}).get('n'),'validation_n':support.get('validation',{}).get('n'),'test_n':support.get('test',{}).get('n'),'validation_MAE':val.get('MAE'),'test_MAE':test.get('MAE'),'test_RMSE':test.get('RMSE'),'test_Bias':test.get('Bias'),'test_sMAPE':test.get('sMAPE'),'training_seconds':m.get('training_seconds'),'inference_seconds':m.get('inference_seconds'),'preprocess_seconds':m.get('preprocess_seconds'),'epochs_ran':m.get('epochs_ran'),'best_epoch':m.get('best_epoch'),'model_size_bytes':m.get('model_size_bytes'),'reuse_events':reuse[m.get('run_id')],'local_artifact_relpath':str(Path(m['artifact_folder']).relative_to(ROOT)) if m.get('artifact_folder') and Path(m['artifact_folder']).is_relative_to(ROOT) else ''})
registry=pd.DataFrame(rows);save(registry,ACC/'G2_02_Experiment_Run_Registry.csv')
completed=[m for m in records if m.get('status')=='COMPLETED' and m.get('prediction_path') and Path(m['prediction_path']).is_file()]
bykey={(m['condition'],m['model'],m['fold'],m['horizon'],m['seed'],m['config_id']):m for m in completed}
def pred(m):return pd.read_parquet(m['prediction_path'])[['sample_id','forecast_origin','y_true','y_pred']]
def calc(y,p):return metrics(np.asarray(y,dtype=float),np.asarray(p,dtype=float))
# E06 three-seed ensemble (Method A) and mean seed metrics (Method B).
selected_path=ROOT/'04_EXPERIMENTS/E06_MODEL_FAIRNESS/E06_Selected_Configurations.json';ensemble=[]
if selected_path.exists():
 selected=load(selected_path)
 for model in ['Ridge','XGBoost','GRU','GRU_WITH_STATIC']:
  for H in HS:
   for fold in range(1,7):
    entries=[m for m in completed if m['condition']=='base' and m['model']==model and m['horizon']==H and m['fold']==fold and m['seed'] in SEEDS]
    if model=='Ridge':continue # protocol has one Ridge seed, not a three-seed ensemble
    if model=='GRU_WITH_STATIC':entries=[m for m in entries if m.get('configuration',{}).get('hidden_size')==selected.get(f'GRU_H{H}',{}).get('value')]
    elif model in ['GRU','XGBoost']:
     key='hidden_size' if model=='GRU' else 'max_depth';entries=[m for m in entries if m.get('configuration',{}).get(key)==selected.get(f'{model}_H{H}',{}).get('value')]
    if set(m['seed'] for m in entries)!={42,2026,3407}:continue
    frames=[]
    for m in sorted(entries,key=lambda z:z['seed']):
     q=pred(m).set_index('sample_id');q=q.rename(columns={'y_pred':f'pred_{m["seed"]}'});frames.append(q)
    merged=frames[0]
    for q in frames[1:]:
     assert merged.index.equals(q.index) and np.allclose(merged.y_true,q.y_true,atol=0,rtol=0)
     merged=merged.join(q[[f'pred_{q.columns[-1].split("_")[-1]}']])
    yp=merged[[f'pred_{s}' for s in SEEDS]].mean(axis=1);A=calc(merged.y_true,yp)
    B={k:float(np.mean([m['test_metrics'][k] for m in entries])) for k in ['MAE','RMSE','Bias','sMAPE']}
    ensemble.append({'model':model,'fold':fold,'horizon':H,'n':len(merged),'method_A_MAE':A['MAE'],'method_A_RMSE':A['RMSE'],'method_A_Bias':A['Bias'],'method_A_sMAPE':A['sMAPE'],'method_B_MAE':B['MAE'],'method_B_RMSE':B['RMSE'],'method_B_Bias':B['Bias'],'method_B_sMAPE':B['sMAPE'],'seed_run_ids':'|'.join(m['run_id'] for m in entries)})
if ensemble:save(pd.DataFrame(ensemble),ACC/'G2_E06_Method_A_B_Actual.csv')
# Explicit common-origin comparison: alternate predictions on base-reference target.
comparisons=[]
for alt in completed:
 cond=alt['condition']
 if cond in ['base','history24_matched']:continue
 ref_cond='history24_matched' if cond in ['history12','history48'] else 'base'
 ref=bykey.get((ref_cond,alt['model'],alt['fold'],alt['horizon'],alt['seed'],alt['config_id']))
 if ref is None:continue
 a=pred(alt).rename(columns={'y_true':'alt_y','y_pred':'alt_pred'});b=pred(ref).rename(columns={'y_true':'ref_y','y_pred':'ref_pred'});merged=b.merge(a[['sample_id','alt_y','alt_pred']],on='sample_id',validate='one_to_one')
 if merged.empty:continue
 r=calc(merged.ref_y,merged.ref_pred);t=calc(merged.ref_y,merged.alt_pred)
 comparisons.append({'condition':cond,'reference_condition':ref_cond,'model':alt['model'],'fold':alt['fold'],'horizon':alt['horizon'],'seed':alt['seed'],'common_n':len(merged),'reference_MAE_on_common_origin':r['MAE'],'alternative_MAE_on_reference_target':t['MAE'],'paired_MAE_delta_alt_minus_ref':t['MAE']-r['MAE'],'alternative_own_target_MAE':alt['test_metrics']['MAE'],'target_values_equal_on_common_origin':bool(np.allclose(merged.ref_y,merged.alt_y,atol=1e-8,rtol=0)),'interpretation':'LEAKAGE_DIAGNOSTIC_ONLY' if cond=='leaky_scaling' else 'COMMON_ORIGIN_REFERENCE_TARGET','reference_run_id':ref['run_id'],'alternative_run_id':alt['run_id']})
if comparisons:save(pd.DataFrame(comparisons),ACC/'G2_Actual_Common_Origin_Contrasts.csv')
summary={'generated_at':now(),'run_json_count':len(records),'completed_count':len(completed),'failed_count':sum(m.get('status')=='FAILED' for m in records),'reuse_event_count':sum(reuse.values()),'conditions':dict(collections.Counter(m.get('condition') for m in completed)),'method_A_B_rows':len(ensemble),'common_origin_contrast_rows':len(comparisons)};dump(ACC/'G2_Summary_Build_Receipt.json',summary);print(json.dumps(summary,ensure_ascii=False))
