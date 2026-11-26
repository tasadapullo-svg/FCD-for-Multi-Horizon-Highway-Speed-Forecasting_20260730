"""Descriptive fixed-versus-validated E06 comparisons on identical manifests."""
from g2_common import *
selected=load(ROOT/'04_EXPERIMENTS/E06_MODEL_FAIRNESS/E06_Selected_Configurations.json');out=ROOT/'04_EXPERIMENTS/G2_E04_E07_ACCEPTANCE';runs=[]
for p in ART.glob('*/run.json'):
 try:m=load(p)
 except Exception:continue
 if m.get('status')=='COMPLETED' and m.get('condition')=='base':runs.append(m)
def one(model,H,fold,seed,key,value):
 v=[m for m in runs if m['model']==model and m['horizon']==H and m['fold']==fold and m['seed']==seed and m['configuration'].get(key)==value]
 assert len(v)==1,(model,H,fold,seed,key,value,len(v));return v[0]
rows=[]
for model,key,fixed in [('Ridge','alpha',1.0),('XGBoost','max_depth',8),('GRU','hidden_size',64)]:
 for H in HS:
  tuned=selected[f'{model}_H{H}']['value']
  for fold in range(1,7):
   a=one(model,H,fold,42,key,fixed);b=one(model,H,fold,42,key,tuned)
   assert a['manifest_sha256']==b['manifest_sha256']
   rows.append({'model':model,'fold':fold,'horizon':H,'comparison':'FIXED_VS_VALIDATION_SELECTED_SINGLE_SEED','fixed_value':fixed,'selected_value':tuned,'common_test_n':a['support']['test']['n'],'fixed_test_MAE':a['test_metrics']['MAE'],'selected_test_MAE':b['test_metrics']['MAE'],'delta_selected_minus_fixed':b['test_metrics']['MAE']-a['test_metrics']['MAE'],'fixed_run_id':a['run_id'],'selected_run_id':b['run_id'],'same_manifest':True,'selection_source':'Fold1 validation only'})
ensemble=pd.read_csv(out/'G2_E06_Method_A_B_Actual.csv');
for H in HS:
 for fold in range(1,7):
  x=ensemble[(ensemble.horizon==H)&(ensemble.fold==fold)];a=x[x.model=='GRU'];b=x[x.model=='GRU_WITH_STATIC'];assert len(a)==len(b)==1 and int(a.iloc[0]['n'])==int(b.iloc[0]['n'])
  rows.append({'model':'GRU_WITH_STATIC','fold':fold,'horizon':H,'comparison':'SELECTED_DYNAMIC_VS_SELECTED_STATIC_METHOD_A','fixed_value':selected[f'GRU_H{H}']['value'],'selected_value':selected[f'GRU_H{H}']['value'],'common_test_n':int(a.iloc[0]['n']),'fixed_test_MAE':float(a.iloc[0]['method_A_MAE']),'selected_test_MAE':float(b.iloc[0]['method_A_MAE']),'delta_selected_minus_fixed':float(b.iloc[0]['method_A_MAE']-a.iloc[0]['method_A_MAE']),'fixed_run_id':a.iloc[0]['seed_run_ids'],'selected_run_id':b.iloc[0]['seed_run_ids'],'same_manifest':True,'selection_source':'Same validated hidden size; static input only differs'})
save(pd.DataFrame(rows),out/'G2_E06_Configuration_Contrasts.csv');print('E06_CONTRASTS',len(rows))
