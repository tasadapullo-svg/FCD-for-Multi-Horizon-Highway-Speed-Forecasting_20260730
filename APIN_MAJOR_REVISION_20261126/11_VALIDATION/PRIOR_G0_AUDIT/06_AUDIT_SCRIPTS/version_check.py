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

x=pd.read_csv(O/'00_MANIFESTS/G0_github_freeze_comparison.csv').fillna('')
for ix,r in x[x.status=='MISMATCH'].iterrows():
 b=(repo/r.path).read_bytes();lf=b.replace(b'\r\n',b'\n');git=hashlib.sha1(b'blob '+str(len(lf)).encode()+b'\0'+lf).hexdigest()
 if git==r.git_blob_expected:x.at[ix,'reason']='CRLF→LF normalization matches Git object; bytes differ';x.at[ix,'status']='PASS_DOCUMENT_MATCH'
 else:x.at[ix,'reason']='确实Git blob不同；版本差异未定位'
save('00_MANIFESTS/G0_github_freeze_comparison.csv',x.to_dict('records'))
(O/'07_LOGS/github_comparison_summary.json').write_text(json.dumps(x.status.value_counts().to_dict()))
print(x.status.value_counts().to_dict(),flush=True)
