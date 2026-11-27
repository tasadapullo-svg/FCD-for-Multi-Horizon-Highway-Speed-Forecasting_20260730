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

zi=pd.read_csv(O/'00_MANIFESTS/G0_zip_crc_inventory.csv').fillna('')
def readentry(r):
 parts=r['archive'].split('!');z=zipfile.ZipFile(parts[0])
 for s in parts[1:]:z=zipfile.ZipFile(io.BytesIO(z.read(s)))
 return z.read(r['entry'])
r=zi[zi.entry.str.endswith('/tomtom_cleaned_records.csv.gz')].iloc[0];raw=pd.read_csv(io.BytesIO(readentry(r)),compression='gzip');print('RAW',raw.shape,raw.columns.tolist(),flush=True)
node=zi[zi.entry.str.endswith('/nodes.csv')].iloc[0];nodes=pd.read_csv(io.BytesIO(readentry(node)));print('NODES',nodes.shape,nodes.columns.tolist(),flush=True)
counts=[]
def count(stage,n,evidence,status='PASS_RECALCULATED',expected=''):
 counts.append(dict(stage_id=stage,rows_out=n,expected=expected,status=status,evidence=evidence))
count('cleaned_input',len(raw),r['archive']+'!'+r['entry'],expected=244477);count('nodes',len(nodes),node['archive']+'!'+node['entry'],expected=51)
t=pd.to_datetime(raw.event_time,errors='coerce');ok=t.notna() & np.isfinite(raw.current_speed)&(raw.current_speed>0)&(raw.current_speed<=130)&np.isfinite(raw.current_travel_time)&(raw.current_travel_time>0)&np.isfinite(raw.confidence)&raw.confidence.between(.8,1)
for k in ['valid_record','valid_coordinates','valid_speed','valid_travel_time','valid_confidence','valid_time']:
 ok &= raw[k].astype(str).str.lower().isin(['true','1','1.0'])
ok &= raw.road_closure.astype(str).str.lower().isin(['false','0','0.0'])
q=raw.loc[ok].copy();q['quarter_hour']=t[ok].dt.floor('15min');ded=q.groupby(['node_id','quarter_hour']).current_speed.mean().reset_index();count('quality_pass',len(q),r['entry'],expected=243307);count('confidence_fail',int((raw.confidence<.8).sum()),r['entry'],expected=1170);count('deduplicated',len(ded),r['entry'],expected=241601);count('duplicates_removed',len(q)-len(ded),r['entry']);count('duplicate_groups',int((q.groupby(['node_id','quarter_hour']).size()>1).sum()),r['entry'])
count('min_time',str(t.min()),r['entry']);count('max_time',str(t.max()),r['entry']);planned=len(pd.date_range(t.min(),t.max(),freq='15min'))*len(nodes);count('planned_slots',planned,'date_range inclusive × nodes',expected=403512);count('15min_return_percent',100*len(ded)/planned,'deduplicated/planned')
# Hour bins using complete study hours only, timestamps floor hour.
ded['hour']=ded.quarter_hour.dt.floor('h');hour=ded.groupby(['node_id','hour']).current_speed.agg(['count','mean']).reset_index();hour=hour[(hour.hour>=pd.Timestamp('2025-12-08 14:00'))&(hour.hour<=pd.Timestamp('2026-02-28 23:00'))]
for k in [1,2,3,4]:count(str(k)+'_of_4_hours',int((hour['count']>=k).sum()),'原始CSV质量过滤后15min去重，再floor hour分组')
save('01_DATA_LINEAGE/G0_pipeline_stage_counts.csv',counts)
save('01_DATA_LINEAGE/G0_schema_and_key_audit.csv',[dict(path=r['archive']+'!'+r['entry'],rows=len(raw),columns='|'.join(raw.columns),status='PASS_RECALCULATED'),dict(path=node['archive']+'!'+node['entry'],rows=len(nodes),columns='|'.join(nodes.columns),status='PASS_HASH_ONLY')])
(O/'07_LOGS/raw_recalculation_summary.json').write_text(json.dumps(counts,ensure_ascii=False,default=str),encoding='utf8')
print('RAW DONE',flush=True)
# Parquet audits use only existing files, never run model or unpickle weights.
try: import pyarrow
except ImportError:
 print('BINARY_READ_BLOCKED pyarrow',flush=True);sys.exit(2)
reg=pd.read_csv(P/'03_FORMAL_PREDICTIONS/formal_run_registry.csv');ms={};splitrows=[]
for p in (P/'01_DATA_PIPELINE/folds').rglob('sample_manifest*.parquet'):
 df=pd.read_parquet(p);fold=int(re.search(r'fold(\d)',str(p)).group(1));h=int(re.search(r'H(\d)',str(p)).group(1));ms[fold,h]=(df,p);splitrows.append(dict(fold=fold,horizon=h,path=str(p),rows=len(df),columns='|'.join(df.columns),sha256=sha(p),status='NOT_VERIFIED',reason='已读取；边界及target逐行检查待补'))
save('01_DATA_LINEAGE/G0_split_manifest_audit.csv',splitrows)
print('MANIFEST_SCHEMA',next(iter(ms.values()))[0].columns.tolist(),flush=True)
runs=[];recalc=[];maps=[]
for _,r in reg.iterrows():
 p=P/'03_FORMAL_PREDICTIONS/predictions'/Path(r.prediction_file.replace('\\','/')).name;df=pd.read_parquet(p);mf,mp=ms[int(r.fold),int(r.horizon)];actual=sha(p);cp=P/'03_FORMAL_PREDICTIONS/checkpoints'/(r.run_name+'.pt');finite=True
 yc=next((k for k in ['y_true','target','y','actual'] if k in df),None);pc=next((k for k in ['y_pred','prediction','pred'] if k in df),None)
 if yc and pc:
  finite=bool(np.isfinite(df[[yc,pc]].to_numpy()).all());err=df[pc]-df[yc];recalc.append(dict(run_id=r.run_name,model=r.model,fold=r.fold,horizon=r.horizon,seed=r.seed,MAE=float(err.abs().mean()),RMSE=float(np.sqrt((err**2).mean())),status='PASS_RECALCULATED' if finite else 'MISMATCH',evidence_path=str(p),reason='由现有预测独立计算；与已存指标比较见后续汇总'))
 samplekey=next((k for k in ['sample_id','sample_idx','sample_index'] if k in df and k in mf),None);match='NOT_VERIFIED'
 if samplekey:
  test=mf[mf.split=='test'] if 'split' in mf else mf;match=str(set(df[samplekey])==set(test[samplekey]))
 runs.append(dict(run_id=r.run_name,model=r.model,fold=r.fold,horizon=r.horizon,seed=r.seed,registry_status=r.status,rows=len(df),expected_rows=r.test_samples,prediction_sha_match=actual==r.prediction_sha256,manifest_sha_match=sha(mp)==r.sample_manifest_sha256,sample_ids_match=match,finite=finite,columns='|'.join(df.columns),checkpoint_exists=cp.exists() if r.model=='GRU' else '',status='PASS_HASH_ONLY' if actual==r.prediction_sha256 and len(df)==r.test_samples else 'MISMATCH',reason='标签与manifest逐值核验未完成，不能宣称180_RUNS_INTEGRITY_PASS'))
 maps.append(dict(run_id=r.run_name,fold=r.fold,horizon=r.horizon,model=r.model,seed=r.seed,config_sha=sha(P/'00_DEFINITION_FREEZE/phase2a1_frozen.yaml'),code_entrypoint='src/run_phase2a1_campaign.py',code_sha='',input_manifest_sha=sha(mp),prediction_path=str(p),prediction_sha=actual,checkpoint_path=str(cp) if cp.exists() else '',reproducibility_status='MISSING_CODE',blocker='正式训练源码未定位'))
save('03_CODE_AND_RESULTS/G0_formal_180_run_integrity.csv',runs);save('03_CODE_AND_RESULTS/G0_source_to_run_map.csv',maps);save('03_CODE_AND_RESULTS/G0_saved_metrics_recalculation.csv',recalc)
print('PREDICTIONS DONE',len(runs),len(recalc),flush=True)
