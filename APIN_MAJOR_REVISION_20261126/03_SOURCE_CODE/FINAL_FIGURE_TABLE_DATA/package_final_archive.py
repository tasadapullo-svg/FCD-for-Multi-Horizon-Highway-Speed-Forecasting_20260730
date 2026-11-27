from pathlib import Path
import hashlib,json,zipfile,os
import pandas as pd
from openpyxl import Workbook
O=Path(r'E:\20261125_论文修改_Applied Intelligence');A=O/'APIN_FINAL_RESEARCH_ARCHIVE';C=A/'00_PROJECT_CONTROL';T=A/'15_GITHUB_RELEASE';K=T/'APIN_GITHUB_RELEASE_CANDIDATE'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def files(d):return sorted(p for p in d.rglob('*') if p.is_file() and '.git' not in p.parts and not p.name.endswith('.inspect.ndjson'))
ps=[p for p in files(A) if p.name not in {'APIN_FINAL_ARCHIVE_MANIFEST.json','APIN_FINAL_ARCHIVE_SHA256SUMS.txt','APIN_FINAL_ARCHIVE_REPORT_CN.md','PROJECT_MASTER_FILE_REGISTRY.csv','PROJECT_MASTER_FILE_REGISTRY.xlsx'}]
rows=[]
for i,p in enumerate(ps,1):
 rel=str(p.relative_to(A)).replace('\\','/');private=any(x in rel for x in ['01_ORIGINAL_MANUSCRIPT','02_PEER_REVIEW','09_GIS_QGIS','16_GPT_REVIEW_PACKAGE','18_MANUSCRIPT_REVISION'])
 rows.append({'file_id':f'AR{i:05d}','filename':p.name,'archive_relative_path':rel,'file_size':p.stat().st_size,'sha256':sha(p),'source_phase':rel.split('/')[0],'experiment_id':next((x for x in rel.split('/') if x.startswith('E0')),''),'figure_id':next((x[:5] for x in rel.split('/') if x.startswith('Fig')),''),'table_id':p.stem if p.stem.startswith('Table') else '', 'version':'2026-11-26 archive','canonical_status':'CURRENT_CANONICAL_RESULT' if '05_EXPERIMENT_RESULTS' in rel or '12_SCIENTIFIC_REPORTS' in rel else 'REQUIRED_REFERENCE','confidentiality':'LOCAL_CONTROLLED' if private else 'AUTHOR_REVIEW','license_status':'AUTHOR_CONFIRMATION_REQUIRED','github_eligibility':'NOT_STAGED','gpt_review_eligibility':'SEE_EXISTING_GPT_PACKAGE'})
index=pd.DataFrame(rows);index.to_csv(C/'PROJECT_MASTER_FILE_REGISTRY.csv',index=False,encoding='utf-8-sig')
w=Workbook();s=w.active;s.title='00_Overview';s.append(['Archive files','Folders','Canonical results','Duplicates','GitHub staged']);s.append([len(rows),len([x for x in A.rglob('*') if x.is_dir()]),int((index.canonical_status=='CURRENT_CANONICAL_RESULT').sum()),len(pd.read_csv(A/'17_HISTORICAL_VERSIONS/Duplicate_File_Registry.csv')),0]);s=w.create_sheet('01_File_Registry');s.append(list(index.columns))
for row in index.itertuples(index=False,name=None):s.append(list(row))
for name,p in [('02_Duplicates',A/'17_HISTORICAL_VERSIONS/Duplicate_File_Registry.csv'),('03_Canonical',C/'Canonical_Result_Registry.csv'),('04_GitHub_Eligibility',T/'GitHub_Publication_Eligibility_Matrix.csv')]:
 x=pd.read_csv(p).fillna('');s=w.create_sheet(name);s.append(list(x.columns))
 for row in x.itertuples(index=False,name=None):s.append(list(row))
w.save(C/'PROJECT_MASTER_FILE_REGISTRY.xlsx')
rows2=[]
for d in sorted(p for p in A.iterdir() if p.is_dir()):
 fs=files(d);rows2.append({'folder':d.name,'files':len(fs),'bytes':sum(p.stat().st_size for p in fs)})
dup=pd.read_csv(A/'17_HISTORICAL_VERSIONS/Duplicate_File_Registry.csv');report='# Applied Intelligence 最终科研归档报告\n\n归档：`'+str(A)+'`。本轮仅整理文件，新增模型拟合0次、交通数据0套。\n\n'+pd.DataFrame(rows2).to_markdown(index=False) if False else ''
report='# Applied Intelligence 最终科研归档报告\n\n归档：`'+str(A)+'`。本轮新增模型拟合0次、交通数据0套。\n\n|目录|文件数|字节|\n|---|---:|---:|\n'+'\n'.join(f"|{r['folder']}|{r['files']}|{r['bytes']}|" for r in rows2)+f"\n\n完全重复引用：{len(dup)}，避免重复复制 {int(dup.bytes_avoided.sum())} 字节。正式结果见 `PROJECT_MASTER_FILE_REGISTRY.csv`。图表8张、正文表9张、补充8组、审稿意见31条。GIS原始节点51、道路1598、路径50；15节点待人工复核，历史约130 km未验证，QGIS工程未运行验证。远程仓库为公开AJSE Phase 2A，尚未确认APIN能否写入。候选文档7份，实际Git暂存/提交/推送均为0。\n"
(A/'APIN_FINAL_ARCHIVE_REPORT_CN.md').write_text(report,encoding='utf-8')
def package(path,members,root,prefix):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in members:z.write(p,prefix+str(p.relative_to(root)).replace('\\','/'))
 with zipfile.ZipFile(path) as z:assert z.testzip() is None;return len(z.namelist())
z1=O/'APIN_COMPLETE_RESEARCH_ARCHIVE_LOCAL_20261126.zip';z2=O/'APIN_GITHUB_UPDATE_CANDIDATE_20261126.zip';z3=O/'APIN_GPT_FINAL_REVIEW_AND_PLOTTING_20261126.zip';z4=O/'APIN_QGIS_FINAL_ARCHIVE_LOCAL_20261126.zip'
gpt=O/'APIN_GPT_REVIEW_AND_SCI_PLOTTING_20261126.zip';qgis=O/'APIN_QGIS_DRAWING_AND_VALIDATION_LOCAL_20261126.zip'
counts={};counts[z2.name]=package(z2,[p for p in files(T) if 'REMOTE_READONLY_CHECKOUT' not in str(p)],T,'GITHUB_CANDIDATE/')
for source,target in [(gpt,z3),(qgis,z4)]:
 if source.exists() and sha(source)==sha(target) if target.exists() else False:pass
 else:target.write_bytes(source.read_bytes())
 counts[target.name]=len(zipfile.ZipFile(target).namelist())
counts[z1.name]=package(z1,[p for p in files(A) if p.name not in {'APIN_FINAL_ARCHIVE_MANIFEST.json','APIN_FINAL_ARCHIVE_SHA256SUMS.txt'}],A,'APIN_FINAL_RESEARCH_ARCHIVE/')
manifest={'archive_root':str(A),'archive_files':len(files(A)),'archive_folders':len([x for x in A.rglob('*') if x.is_dir()]),'archive_bytes':sum(p.stat().st_size for p in files(A)),'duplicate_references':len(dup),'avoided_bytes':int(dup.bytes_avoided.sum()),'canonical_result_count':int((index.canonical_status=='CURRENT_CANONICAL_RESULT').sum()),'github_status':'RELEASE_CANDIDATE_BLOCKED_BY_REPO_SCOPE_AND_LICENSE','git_staged':0,'git_committed':0,'remote_push':'NOT_EXECUTED','packages':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p),'entries':counts[p.name],'crc':'PASS'} for p in [z1,z2,z3,z4]]}
(A/'APIN_FINAL_ARCHIVE_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(A/'APIN_FINAL_ARCHIVE_SHA256SUMS.txt').write_text('\n'.join(f"{sha(p)}  {p.name}" for p in [z1,z2,z3,z4])+'\n',encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False))
