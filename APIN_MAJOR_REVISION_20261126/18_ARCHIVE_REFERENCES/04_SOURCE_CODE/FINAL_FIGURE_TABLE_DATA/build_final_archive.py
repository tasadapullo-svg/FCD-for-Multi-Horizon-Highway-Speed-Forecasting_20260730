from pathlib import Path
import hashlib,json,shutil,zipfile,os
import pandas as pd

O=Path(r'E:\20261125_论文修改_Applied Intelligence');R=O/'大修_Applied Intelligence_2026112_论文修改';A=O/'APIN_FINAL_RESEARCH_ARCHIVE';B=R/'07_FIGURES_TABLES/FINAL_FIGURE_TABLE_DATA';E=R/'04_EXPERIMENTS';C=R/'03_CODE';G=B/'01_FIGURE_DATA/Fig01_Study_Area_GIS';T=A/'15_GITHUB_RELEASE';A.mkdir(exist_ok=True)
sections=['00_PROJECT_CONTROL','01_ORIGINAL_MANUSCRIPT','02_PEER_REVIEW','03_DATA_AND_PROVENANCE','04_SOURCE_CODE','05_EXPERIMENT_RESULTS','06_STATISTICAL_ANALYSIS','07_FIGURE_DATA','08_TABLE_DATA','09_GIS_QGIS','10_SUPPLEMENTARY_MATERIALS','11_REFERENCES','12_SCIENTIFIC_REPORTS','13_AUDIT_AND_VALIDATION','14_REPRODUCIBILITY','15_GITHUB_RELEASE','16_GPT_REVIEW_PACKAGE','17_HISTORICAL_VERSIONS','18_MANUSCRIPT_REVISION']
for s in sections:(A/s).mkdir(exist_ok=True)
seen={};logs=[];dups=[]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def add(p,d,role='CURRENT_CANONICAL_RESULT',license='AUTHOR_LOCAL'):
 if not p.exists() or not p.is_file():return
 h=sha(p);dest=A/d;dest.parent.mkdir(parents=True,exist_ok=True)
 if h in seen:
  dups.append({'source':str(p),'intended_archive':str(d).replace('\\','/'),'canonical_archive':seen[h],'sha256':h,'classification':'EXACT_DUPLICATE','bytes_avoided':p.stat().st_size});return
 if dest.exists() and sha(dest)!=h:raise RuntimeError(f'Archive collision: {dest}')
 if not dest.exists():shutil.copy2(p,dest)
 seen[h]=str(d).replace('\\','/');logs.append({'original_path':str(p),'archive_relative_path':seen[h],'file_size':dest.stat().st_size,'sha256':h,'role':role,'license':license})
def add_tree(src,dest,extensions=None,exclude=()):
 for p in sorted(src.rglob('*')):
  if not p.is_file() or any(t in str(p) for t in exclude):continue
  if extensions and p.suffix.lower() not in extensions:continue
  add(p,Path(dest)/p.relative_to(src))

# Submission source remains a separate local read-only lineage.
for n in ['Applied_Intelligence_20260905.zip','APIN-D-26-12623.pdf']:add(R/n,Path('01_ORIGINAL_MANUSCRIPT')/n,'REQUIRED_REFERENCE','EXCLUDED_CONFIDENTIAL')
add(R/'APIN_D_26_12623_Reviewer_Comments20261122.docx',Path('02_PEER_REVIEW/01_ORIGINAL_COMMENTS')/'APIN_D_26_12623_Reviewer_Comments20261122.docx','REQUIRED_REFERENCE','EXCLUDED_CONFIDENTIAL')
original=next(O.glob('大修_20261124-*/20260905Applied Intelligence 投稿/Applied_Intelligence_20260905'),None)
if original:
 for p in original.iterdir():
  if p.is_file() and (p.name in ['main.tex','references.bib','preview.pdf'] or (p.name.startswith('Fig') and p.suffix.lower() in ['.png','.jpg','.pdf'])):add(p,Path('01_ORIGINAL_MANUSCRIPT/SUBMISSION_SOURCE')/p.name,'REQUIRED_REFERENCE','EXCLUDED_CONFIDENTIAL')
for p in sorted(E.rglob('*.csv')):
 if 'logs' in p.parts or 'G2_ARTIFACTS' in p.parts:continue
 stage=p.parent.name
 if stage.startswith('E01'):dest='05_EXPERIMENT_RESULTS/E01_DATA_AVAILABILITY'
 elif stage.startswith('E02'):dest='05_EXPERIMENT_RESULTS/E02_TRAFFIC_REGIME_RELIABILITY'
 elif stage.startswith('E03'):dest='05_EXPERIMENT_RESULTS/E03_MODEL_EVALUATION'
 elif stage.startswith('E04'):dest='05_EXPERIMENT_RESULTS/E04_SENSITIVITY'
 elif stage.startswith('E05'):dest='05_EXPERIMENT_RESULTS/E05_GATE_FCD_ABLATION'
 elif stage.startswith('E06'):dest='05_EXPERIMENT_RESULTS/E06_MODEL_FAIRNESS'
 elif stage.startswith('E07'):dest='05_EXPERIMENT_RESULTS/E07_SPATIAL_OPERATIONAL'
 elif p.name.startswith(('JB','E08')):dest='05_EXPERIMENT_RESULTS/E08_EXTERNAL_VALIDATION_DECISION'
 elif p.name.startswith(('Ridge_','Final_Ridge')):dest='05_EXPERIMENT_RESULTS/E06_MODEL_FAIRNESS/RIDGE_SVD_NUMERICAL_CORRECTION'
 elif p.name.startswith(('E03_06','E03_07','E03_08','Final_Statistical')):dest='06_STATISTICAL_ANALYSIS'
 else:dest='13_AUDIT_AND_VALIDATION'
 add(p,Path(dest)/p.name,'CURRENT_CANONICAL_RESULT' if 'FINAL' in stage or stage.startswith('E0') else 'REQUIRED_REFERENCE')
for p in sorted(E.rglob('*.md')):
 if 'logs' in p.parts:continue
 if p.stat().st_size<500000:add(p,Path('12_SCIENTIFIC_REPORTS/HISTORICAL_REPORTS')/p.name,'REQUIRED_REFERENCE')
add_tree(C,'04_SOURCE_CODE',extensions={'.py','.yaml','.yml','.json','.md','.txt'},exclude=('__pycache__','.pyc'))
for d,target in [('01_FIGURE_DATA','07_FIGURE_DATA'),('02_TABLE_DATA','08_TABLE_DATA'),('03_SUPPLEMENTARY_DATA','10_SUPPLEMENTARY_MATERIALS')]:add_tree(B/d,target,exclude=('.inspect.ndjson',))
for p in sorted(G.iterdir()):
 if p.is_file() and p.suffix.lower() in ['.gpkg','.shp','.shx','.dbf','.prj','.cpg','.geojson','.csv','.md','.json','.xlsx']:add(p,Path('09_GIS_QGIS')/p.name,'CURRENT_CANONICAL_RESULT','RESTRICTED_LOCAL_ONLY')
add_tree(B/'09_QGIS_VALIDATION','09_GIS_QGIS/09_VALIDATION_REPORTS',exclude=('.inspect.ndjson',))
for n in ['APIN_00_All_Research_Results_Master.xlsx','APIN_01_Complete_Research_Results_Summary_CN.md','APIN_01_Complete_Research_Results_Summary_EN.md','Master_Aggregate_Provenance.csv']:add(B/'08_MASTER_RESEARCH_RESULTS'/n,Path('12_SCIENTIFIC_REPORTS')/n)
for p in (B/'07_FINAL_DELIVERY').glob('*'):
 if p.is_file():add(p,Path('13_AUDIT_AND_VALIDATION')/p.name,'REQUIRED_REFERENCE')
for p in (B/'08_MASTER_RESEARCH_RESULTS').glob('R*/*.csv'):
 add(p,Path('05_EXPERIMENT_RESULTS/MASTER_CATEGORY_SUMMARIES')/p.parent.name/p.name)
for n in ['APIN_GPT_REVIEW_AND_SCI_PLOTTING_20261126.zip','APIN_QGIS_DRAWING_AND_VALIDATION_LOCAL_20261126.zip']:
 add(O/n,Path('16_GPT_REVIEW_PACKAGE' if 'GPT' in n else '09_GIS_QGIS')/n,'REQUIRED_REFERENCE','AUTHOR_CONFIRMATION_REQUIRED' if 'GPT' in n else 'RESTRICTED_LOCAL_ONLY')
for n in ['APIN_G0_Data_Readiness_20261125.zip','APIN_G1_E01_E03_Results_20261125.zip','APIN_G2_E04_E07_Results_20261126.zip','APIN_FINAL_EVIDENCE_FREEZE_20261126.zip','APIN_E08_JB_FEASIBILITY_AND_FINAL_CLOSURE_20261126.zip']:
 p=O/n
 if p.exists():add(p,Path('17_HISTORICAL_VERSIONS')/n,'REQUIRED_REFERENCE')

# Original source copied to an explicitly unfinished working area, without editing.
if original and (original/'main.tex').exists():add(original/'main.tex',Path('18_MANUSCRIPT_REVISION/03_MANUSCRIPT_WORKING_COPY')/'main.tex','WORKING_COPY_NOT_REVISED','EXCLUDED_CONFIDENTIAL')
for n in ['01_FIGURE_FINAL','02_TABLE_FINAL','03_MANUSCRIPT_WORKING_COPY','04_CLEAN_MANUSCRIPT','05_MARKED_MANUSCRIPT','06_RESPONSE_TO_REVIEWERS','07_SUPPLEMENTARY_FINAL','08_SUBMISSION_PACKAGE']:(A/'18_MANUSCRIPT_REVISION'/n).mkdir(parents=True,exist_ok=True)
for s in sections:
 d=A/s;count=len([p for p in d.rglob('*') if p.is_file()]);(d/'README_CN.md').write_text(f'# {s}\n\n用途：{s}。来源：当前已冻结工程及原投稿受控文件。当前版本：2026-11-26归档候选；实际内容 {count} 个文件（不含本说明）。数据许可：默认作者本地受控，公开须按15_GITHUB_RELEASE权限矩阵逐项确认。后续从00_PROJECT_CONTROL总索引定位文件。\n',encoding='utf-8')

pd.DataFrame(logs).to_csv(A/'00_PROJECT_CONTROL/File_Merge_and_Copy_Log.csv',index=False,encoding='utf-8-sig');pd.DataFrame(dups).to_csv(A/'17_HISTORICAL_VERSIONS/Duplicate_File_Registry.csv',index=False,encoding='utf-8-sig')
pd.DataFrame([x for x in logs if x['role']=='CURRENT_CANONICAL_RESULT']).to_csv(A/'00_PROJECT_CONTROL/Canonical_Result_Registry.csv',index=False,encoding='utf-8-sig')
pd.DataFrame([{'result':'G1 Method A','canonical':'E03_03_Original_vs_Recomputed_Table7.csv','superseded':'Original manuscript Method B display','reason':'Seed aggregation definition'},{'result':'G2 Ridge native metric','canonical':'Ridge_Corrected_Aggregates.csv','superseded':'Cholesky Ridge native metric','reason':'SVD numerical stability correction'}]).to_csv(A/'17_HISTORICAL_VERSIONS/Superseded_Result_Registry.csv',index=False,encoding='utf-8-sig')
pd.DataFrame([{'version':'2026-11-26','source':'Prompt06 frozen final aggregates','status':'CURRENT_CANONICAL_RESULT'},{'version':'original submission','source':'Applied_Intelligence_20260905.zip','status':'REQUIRED_REFERENCE'}]).to_csv(A/'17_HISTORICAL_VERSIONS/Historical_Version_Map.csv',index=False,encoding='utf-8-sig')
print(json.dumps({'copied':len(logs),'exact_duplicates':len(dups),'bytes_avoided':sum(x['bytes_avoided'] for x in dups),'archive_root':str(A)},ensure_ascii=False))
