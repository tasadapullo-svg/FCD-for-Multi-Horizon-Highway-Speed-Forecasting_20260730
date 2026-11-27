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
inv=pd.read_csv(O/'00_MANIFESTS/G0_file_inventory.csv').fillna(''); zi=pd.read_csv(O/'00_MANIFESTS/G0_zip_crc_inventory.csv').fillna(''); paths=[Path(x) for x in inv.relative_path]; hashes=dict(zip(inv.relative_path,inv.sha256));tree=json.loads((O/'00_MANIFESTS/github_tree.json').read_text());comp=[]
for x in tree['tree']:
 if x['type']!='blob':continue
 p=repo/x['path'];exists=p.exists(); actual=''
 if exists:
  b=p.read_bytes();actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 comp.append(dict(path=x['path'],git_blob_expected=x['sha'],git_blob_actual=actual,status=('PASS_HASH_ONLY' if actual==x['sha'] else 'MISMATCH') if exists else 'MISSING_LOCAL_DATA'))
save('00_MANIFESTS/G0_github_freeze_comparison.csv',comp)
dups=[]
for name,g in inv.groupby(inv.relative_path.map(lambda s:Path(s).name)):
 if len(g)>1:
  for _,r in g.iterrows():dups.append(dict(name=name,path=r.relative_path,sha256=r.sha256,group_distinct_sha=g.sha256.nunique(),status='PASS_HASH_ONLY' if g.sha256.nunique()==1 else 'NOT_VERIFIED',reason='同名异哈希代表版本差异，不自动认定权威冲突'))
save('00_MANIFESTS/G0_duplicate_and_version_registry.csv',dups)
code=[]
for p in paths:
 if p.suffix.lower() in ['.py','.ipynb','.yaml','.yml','.bat','.ps1'] or re.search('requirements|environment',p.name,re.I):
  code.append(dict(path=str(p),sha256=hashes[str(p)],role='LEGACY_EXCLUDED' if re.search('phase13|LEGACY|历史投稿文章',str(p),re.I) else 'NOT_VERIFIED',formal_training_proven=False))
for n in ['build_phase2a1_data.py','run_phase2a1_campaign.py','finalize_phase2a1.py']:
 found=[str(p) for p in paths if p.name==n];zfound=zi[zi.entry.str.endswith(n)]
 code.append(dict(path='src/'+n,status='NOT_VERIFIED' if found or len(zfound) else 'MISSING_CODE',search_scope='投稿根目录、历史投稿全树、全部嵌套ZIP、公开仓库tree',evidence=str(found)+str(zfound[['archive','entry']].to_dict('records'))))
save('03_CODE_AND_RESULTS/G0_code_inventory.csv',code)
# Paper numeric locator: all numeric tokens in prose/equations/tables, excluding bibliography and TeX layout/preamble/comments.
texp=R/'Applied_Intelligence_20260905/main.tex';text=texp.read_text(encoding='utf8');lines=text.splitlines();claims=[];table='';section='';intable=False;tables=[];equations=[];active=False
for ln,line in enumerate(lines,1):
 if r'\begin{document}' in line:active=True
 if not active or line.lstrip().startswith('%'):continue
 if r'\bibliography' in line:break
 if r'\section' in line or r'\subsection' in line:section=line
 if r'\begin{table' in line:intable=True;table='table@'+str(ln)
 if r'\label{tab:' in line:table=re.search(r'\\label\{([^}]+)',line).group(1)
 if intable:tables.append(dict(tex_line=ln,table_or_figure=table,source_line=line,status='NOT_VERIFIED',reason='需逐单元格语义关联，不能按相同数字自动匹配'))
 if r'\begin{equation' in line or r'\begin{align' in line:equations.append(dict(tex_line=ln,status='NOT_VERIFIED',evidence_path=str(texp),reason='公式与实现逐式对应未完成'))
 if not re.match(r'\s*\\(setlength|vspace|hspace|includegraphics|label|begin|end|toprule|midrule|bottomrule)',line):
  for m in re.finditer(r'(?<![A-Za-z])[-−]?\d[\d,]*(?:\.\d+)?(?:[eE][-+]?\d+)?',line):
   claims.append(dict(claim_id='N'+str(len(claims)+1),section=section,page='',tex_file=str(texp),tex_line=ln,table_or_figure=table if intable else '',metric='',horizon='',model='',fold='',seed='',unit='',denominator='',manuscript_value=m.group(),archive_value='',recalculated_value='',rounding_tolerance='',delta='',status='NOT_VERIFIED',evidence_path=str(texp),reason='自动定位候选；编号/引文待人工筛除，尚不构成事实数字全量覆盖分母',source_line=line))
 if r'\end{table' in line:intable=False;table=''
save('02_PAPER_ALIGNMENT/G0_paper_numeric_alignment.csv',claims);save('02_PAPER_ALIGNMENT/G0_paper_table_alignment.csv',tables);save('02_PAPER_ALIGNMENT/G0_equation_and_definition_audit.csv',equations)
# PDF/source versions and page text identity (not byte identity)
pdfs=[]
for p in [Path(C['pdf']),R/'Applied_Intelligence_20260905.pdf',R/'Applied_Intelligence_20260905/preview.pdf']+[x for x in paths if x.name=='Manuscript_Applied_Intelligence.pdf']:
 rr=PdfReader(p);texts=[q.extract_text() or '' for q in rr.pages];pdfs.append(dict(path=str(p),pages=len(texts),sha256=sha(p)));(O/'02_PAPER_ALIGNMENT'/('pdf_text_'+str(len(pdfs))+'.txt')).write_text('\n'.join('PAGE '+str(i+1)+'\n'+s for i,s in enumerate(texts)),encoding='utf8')
save('02_PAPER_ALIGNMENT/G0_pdf_versions.csv',pdfs)
# Existing CSV/JSON evidence only, not recalculated data.
for folder,pattern,target in [('05_STATISTICS','*.csv','03_CODE_AND_RESULTS/G0_statistics_existing_results_alignment.csv')]:
 rows=[]
 for p in (P/folder).glob(pattern):
  df=pd.read_csv(p);rows.append(dict(path=str(p),rows=len(df),columns='|'.join(df.columns),status='PASS_DOCUMENT_MATCH',reason='读取已存统计结果，不执行新统计推断'))
 save(target,rows)
reg=pd.read_csv(P/'03_FORMAL_PREDICTIONS/formal_run_registry.csv');metrics=pd.read_csv(P/'04_METRICS/per_run_test_metrics.csv');print('registry',reg.shape,'metric cols',metrics.columns.tolist(),flush=True)
(O/'07_LOGS/registry_schema.txt').write_text(str(reg.columns.tolist())+'\n'+str(metrics.columns.tolist()),encoding='utf8')
# Environment snapshot, recorded version is evidence only.
save('03_CODE_AND_RESULTS/G0_environment_and_reproducibility.csv',[dict(path=str(p),status='PASS_DOCUMENT_MATCH',reason='既存版本记录；不是依赖锁完整性证明') for p in paths if re.search('requirements|environment|pipeline_status|GIT_RESULT_FREEZE',p.name,re.I)])
# candidate figure sources, exact image hashes tracked separately.
fig=[]
for i in range(1,7):
 p=R/f'Applied_Intelligence_20260905/Fig{i}.png';candidates=[str(q) for q in paths if re.search('fig0?'+str(i)+'|figure0?'+str(i),str(q),re.I) and q.suffix.lower() in ['.csv','.py','.xlsx','.geojson','.shp','.qgs','.gpkg']];zc=zi[zi.entry.str.contains('fig0?'+str(i)+'|figure0?'+str(i),case=False,regex=True)]
 fig.append(dict(figure='Fig'+str(i),image_path=str(p),sha256=sha(p),candidate_source_paths='|'.join(candidates),zip_candidate_entries=len(zc),status='NOT_VERIFIED',reason='候选源存在不等于已证明生成投稿PNG；图内标注尚需视觉逐项核验'))
save('02_PAPER_ALIGNMENT/G0_figure_alignment.csv',fig)
print('CORE METADATA DONE',flush=True)
