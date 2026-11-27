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

zi=pd.read_csv(O/'00_MANIFESTS/G0_zip_crc_inventory.csv').fillna('');r=zi[zi.entry.str.endswith('/tomtom_cleaned_records.csv.gz')].iloc[0]
with zipfile.ZipFile(r.archive) as z: raw=pd.read_csv(io.BytesIO(z.read(r.entry)),compression='gzip')
t=pd.to_datetime(raw.event_time);ok=raw.confidence.between(.8,1)&raw.current_speed.between(0,130,inclusive='right')&(raw.current_travel_time>0)
for k in ['valid_record','valid_coordinates','valid_speed','valid_travel_time','valid_confidence','valid_time']:ok &=raw[k].astype(str).str.lower().isin(['true','1','1.0'])
ok &=raw.road_closure.astype(str).str.lower().isin(['false','0','0.0']);q=raw[ok].copy();q['quarter_hour']=t[ok].dt.floor('15min');dd=q.groupby(['node_id','quarter_hour']).current_speed.mean().reset_index();dd=dd[dd.quarter_hour>=pd.Timestamp('2025-12-08 14:00')];panel=pd.read_parquet(P/'01_DATA_PIPELINE/panels/deduplicated_15min_observations.parquet');j=dd.merge(panel,on=['node_id','quarter_hour'],validate='one_to_one');delta=(j.current_speed-j.speed_15min).abs();save('01_DATA_LINEAGE/G0_raw_to_panel_value_comparison.csv',[dict(raw_grid_dedup_rows=len(dd),saved_panel_rows=len(panel),joined_rows=len(j),max_abs_speed_delta=delta.max(),mismatches_over_1e_12=int((delta>1e-12).sum()),status='PASS_RECALCULATED' if len(dd)==len(panel)==len(j) and (delta<=1e-12).all() else 'MISMATCH',precision_policy='float mean numerical error 1e-12; exact delta retained')])
counts=pd.read_csv(P/'01_DATA_PIPELINE/sample_count_registry.csv');m=pd.read_csv(O/'01_DATA_LINEAGE/G0_split_manifest_audit.csv');rows=[]
for r in counts.itertuples():
 for split in ['train','validation','test']:
  actual=int(m[(m.fold==r.fold)&(m.horizon==r.horizon)&(m.split==split)].rows.iloc[0]);expected=getattr(r,split+'_count');rows.append(dict(fold=r.fold,horizon=r.horizon,split=split,expected=expected,recalculated=actual,status='PASS_RECALCULATED' if actual==expected else 'MISMATCH'))
save('01_DATA_LINEAGE/G0_sample_count_registry_verification.csv',rows)
# Add observed visual discrepancy without inferring a replacement statistic.
p=O/'04_REVIEW_AND_GAPS/G0_discrepancy_register.csv';df=pd.read_csv(p).fillna('');row=dict(issue_id='V1',severity='MAJOR',claim_or_file='Fig2(a)与底部summary',expected='同一图中最大日可用率定义与数值一致',actual='底部max=99.03%，面板(a)多处100%标注',unit='percent',exact_evidence=str(R/'Applied_Intelligence_20260905/Fig2.png'),root_cause_confirmed_or_hypothesis='内部标注冲突已视觉观察；底层来源及正确数值未知',minimal_fix='先恢复原图数据与分母定义并复核，不在G0修图',owner_action='只读追溯',blocks_G1=True,status='MISMATCH');df=pd.concat([df,pd.DataFrame([row])],ignore_index=True);save('04_REVIEW_AND_GAPS/G0_discrepancy_register.csv',df.to_dict('records'))
fig=pd.read_csv(O/'02_PAPER_ALIGNMENT/G0_figure_alignment.csv').fillna('');fig['visual_inspected']=True;fig.loc[fig.figure=='Fig2','status']='MISMATCH';fig.loc[fig.figure=='Fig2','reason']='面板a有100%点标注，底部max=99.03%；源数据对应尚未完成';save('02_PAPER_ALIGNMENT/G0_figure_alignment.csv',fig.to_dict('records'))
for n in ['G0_FULL_AUDIT_REPORT.md','G0_EXECUTIVE_VERDICT.md']:
 p=O/'05_REPORTS'/n
 with p.open('a',encoding='utf8') as f:f.write('\n补充核验：六幅投稿PNG已视觉检查（未完成所有图内数值逐项核对）；Fig2(a)多个100%点标签与底部max=99.03%冲突，已登记V1，正确值仍未知。原始CSV→冻结15min面板逐键速度值比较及54项split计数检查见新增专表；这些检查的实际状态以CSV为准。\n')
# Input preservation metadata check; full SHA values already frozen, no original file writes.
inv=pd.read_csv(O/'00_MANIFESTS/G0_file_inventory.csv');changes=[]
for r in inv.itertuples():
 p=Path(r.relative_path);st=p.stat();changes.append(dict(path=str(p),size_unchanged=st.st_size==r.size_bytes,status='PASS_DOCUMENT_MATCH' if st.st_size==r.size_bytes else 'MISMATCH',reason='本轮只读；此处为大小复核，非再次全量哈希'))
save('00_MANIFESTS/G0_original_preservation_check.csv',changes)
print('SUPPLEMENT DONE',flush=True)
