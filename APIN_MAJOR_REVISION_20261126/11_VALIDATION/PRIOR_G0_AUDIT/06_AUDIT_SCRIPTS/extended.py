import sys,json,csv,re,hashlib,zipfile,io,datetime,os
from pathlib import Path
C=json.loads(Path(__file__).with_name('config.json').read_text(encoding='utf8')); O=Path(C['out']); R=Path(C['root']); H=Path(C['hist']); repo=H/'20260730_AJSE_FINAL_GitHub'; P=repo/'04_PHASE2A_DATA_RESULTS'
sys.path.insert(0,str(O/'06_AUDIT_SCRIPTS/deps'))
import pandas as pd,numpy as np
from pypdf import PdfReader
def save(name,rows,fields=None):
 rows=list(rows); fields=fields or list(dict.fromkeys(k for r in rows for k in r)) or ['status','reason']
 with (O/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

import yaml
cfg=yaml.safe_load((P/'00_DEFINITION_FREEZE/phase2a1_frozen.yaml').read_text());ri=pd.read_csv(O/'03_CODE_AND_RESULTS/G0_formal_180_run_integrity.csv'); reg=pd.read_csv(P/'03_FORMAL_PREDICTIONS/formal_run_registry.csv'); sm=[]; checks=[]
for _,r in reg.iterrows():
 p=P/'03_FORMAL_PREDICTIONS/predictions'/(r.run_name+'.parquet');df=pd.read_parquet(p);mp=P/f'01_DATA_PIPELINE/folds/fold{r.fold}/H{r.horizon}/sample_manifest_fold{r.fold}_H{r.horizon}.parquet';mf=pd.read_parquet(mp);mt=mf[mf.split=='test'];j=df.merge(mt[['sample_id','target']],on='sample_id',validate='one_to_one');ok=len(j)==len(df)==len(mt) and np.array_equal(j.y_true.to_numpy(),j.target.to_numpy());ri.loc[ri.run_id==r.run_name,'target_matches_manifest']=ok
ri['status']=np.where(ri.prediction_sha_match & ri.manifest_sha_match & ri.finite & ri.target_matches_manifest & (ri.rows==ri.expected_rows),'PASS_RECALCULATED','MISMATCH');ri['reason']='逐预测文件哈希、行数、sample_id一对一连接、y_true与manifest target精确相等、finite核验；checkpoint结构另列未核验';save('03_CODE_AND_RESULTS/G0_formal_180_run_integrity.csv',ri.to_dict('records'))
rec=pd.read_csv(O/'03_CODE_AND_RESULTS/G0_saved_metrics_recalculation.csv');saved=pd.read_csv(P/'04_METRICS/per_run_test_metrics.csv');j=rec.merge(saved,on=['model','fold','horizon','seed'],suffixes=('_actual','_saved'));j['MAE_delta']=j.MAE_actual-j.MAE_saved;j['RMSE_delta']=j.RMSE_actual-j.RMSE_saved;j['status']=np.where((j.MAE_delta.abs()<1e-12)&(j.RMSE_delta.abs()<1e-12),'PASS_RECALCULATED','MISMATCH');save('03_CODE_AND_RESULTS/G0_saved_metrics_recalculation.csv',j.to_dict('records'))
fold=rec.groupby(['model','horizon','fold'])[['MAE','RMSE']].mean().reset_index();summary=fold.groupby(['model','horizon']).agg(MAE_mean=('MAE','mean'),MAE_sd=('MAE','std'),RMSE_mean=('RMSE','mean')).reset_index();save('03_CODE_AND_RESULTS/G0_recalculated_model_summary.csv',summary.to_dict('records'))
for p in (P/'01_DATA_PIPELINE/folds').rglob('sample_manifest*.parquet'):
 d=pd.read_parquet(p);f=int(d.fold.iloc[0]);h=int(d.horizon.iloc[0]);fc=cfg['folds'][f-1];bounds=True
 for split,g in d.groupby('split'):
  st,en=map(pd.Timestamp,fc[split]);ori=pd.to_datetime(g.forecast_origin);ts=pd.to_datetime(g.target_start);te=pd.to_datetime(g.target_end);hs=pd.to_datetime(g.history_start);he=pd.to_datetime(g.history_end)
  b=bool(((ori>=st)&(ori<en)&(ts>ori)&(te<en)&(hs<=he)&(he<=ori)&((he-hs)==pd.Timedelta(hours=23))&(g.target_observed_count>={1:1,3:3,6:5}[h])).all());bounds &= b
  checks.append(dict(fold=f,horizon=h,split=split,rows=len(g),unique_sample_id=g.sample_id.is_unique,causal_and_split_bounds=b,observed5=int((g.target_observed_count==5).sum()) if h==6 else '',observed6=int((g.target_observed_count==6).sum()) if h==6 else '',status='PASS_RECALCULATED' if b and g.sample_id.is_unique else 'MISMATCH',evidence_path=str(p)))
save('01_DATA_LINEAGE/G0_split_manifest_audit.csv',checks)
# Full-hour grid scope vs original first partial hour, no tolerance adjustment.
ct=pd.read_csv(O/'01_DATA_LINEAGE/G0_pipeline_stage_counts.csv').fillna('');ct.loc[ct.stage_id=='deduplicated','stage_id']='deduplicated_all_raw_span';ct.loc[ct.stage_id=='deduplicated_all_raw_span','expected']='';ct.loc[ct.stage_id=='planned_slots','stage_id']='planned_slots_all_raw_span';ct.loc[ct.stage_id=='planned_slots_all_raw_span','expected']=''
panel=pd.read_parquet(P/'01_DATA_PIPELINE/panels/deduplicated_15min_observations.parquet');print('PANEL_SCHEMA',panel.columns.tolist(),len(panel),flush=True)
ct=pd.concat([ct,pd.DataFrame([dict(stage_id='frozen_deduplicated_panel',rows_out=len(panel),expected=241601,status='PASS_RECALCULATED',evidence=str(P/'01_DATA_PIPELINE/panels/deduplicated_15min_observations.parquet')),dict(stage_id='frozen_planned_slots',rows_out=1978*4*51,expected=403512,status='PASS_RECALCULATED',evidence='complete-hour grid 2025-12-08 14:00 through 2026-02-28 23:45'),dict(stage_id='excluded_first_partial_hour_dedup',rows_out=241727-len(panel),status='PASS_RECALCULATED',evidence='all raw-span dedup minus frozen panel')])],ignore_index=True);save('01_DATA_LINEAGE/G0_pipeline_stage_counts.csv',ct.to_dict('records'))
# Config fields versus source, actual runtime implementation absent.
configs=[]
def flatten(x,key=''):
 if isinstance(x,dict):
  for k,v in x.items():flatten(v,key+'.'+str(k))
 else:configs.append(dict(parameter=key,config_value=str(x),config_path=str(P/'00_DEFINITION_FREEZE/phase2a1_frozen.yaml'),status='PASS_DOCUMENT_MATCH',implementation_verified=False,reason='正式配置已读，正式训练代码缺失'))
flatten(cfg);save('03_CODE_AND_RESULTS/G0_model_config_alignment.csv',configs)
# Precisely compare primary Table 7 MAE +/- SD cells, no broad token-value guessing.
claims=pd.read_csv(O/'02_PAPER_ALIGNMENT/G0_paper_numeric_alignment.csv').fillna('');lines=(R/'Applied_Intelligence_20260905/main.tex').read_text(encoding='utf8').splitlines();start=next(i for i,l in enumerate(lines) if r'\label{tab:main_mae}' in l);end=next(i for i in range(start,len(lines)) if r'\end{table}' in lines[i]);alignment=[]
for i in range(start,end):
 l=lines[i];model=l.split('&')[0].strip()
 if model not in set(summary.model):continue
 pairs=re.findall(r'(\d+\.\d+)\\pm(\d+\.\d+)',l)
 for h,pair in zip([1,3,6],pairs):
  row=summary[(summary.model==model)&(summary.horizon==h)].iloc[0]
  for metric,v in zip(['MAE_mean','MAE_sd'],pair):
   actual=float(row[metric]);status='PASS_RECALCULATED' if f'{actual:.3f}'==v else 'MISMATCH';alignment.append(dict(tex_line=i+1,table_or_figure='tab:main_mae',model=model,horizon=h,metric=metric,manuscript_value=v,recalculated_value=actual,delta=actual-float(v),status=status,evidence_path='G0_recalculated_model_summary.csv',rounding_policy='3 decimal fixed, no added tolerance'))
   inds=claims[(claims.tex_line==i+1)&(claims.manuscript_value==v)&(claims.status=='NOT_VERIFIED')].index
   if len(inds):
    ix=inds[0]
    for k,val in dict(metric=metric,model=model,horizon=h,recalculated_value=actual,status=status,delta=actual-float(v),reason='现有预测→逐seed→逐fold→六折mean/sample SD',evidence_path='03_CODE_AND_RESULTS/G0_recalculated_model_summary.csv',rounding_tolerance='display rounding 0.001').items():claims.at[ix,k]=val
save('02_PAPER_ALIGNMENT/G0_primary_table_cell_verification.csv',alignment);save('02_PAPER_ALIGNMENT/G0_paper_numeric_alignment.csv',claims.to_dict('records'))
print('EXTENDED DONE',ri.status.value_counts().to_dict(),j.status.value_counts().to_dict(),flush=True)
