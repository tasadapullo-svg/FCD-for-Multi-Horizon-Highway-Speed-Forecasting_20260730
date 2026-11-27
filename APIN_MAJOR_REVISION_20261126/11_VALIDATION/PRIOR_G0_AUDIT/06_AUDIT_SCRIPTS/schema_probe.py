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

p=P/'01_DATA_PIPELINE/panels/hourly_panel_all_thresholds.parquet';d=pd.read_parquet(p);print('hourly',d.shape,d.columns.tolist());print('statsfiles',[x.name for x in (P/'05_STATISTICS').iterdir()]);print('ckpt',len(list((P/'03_FORMAL_PREDICTIONS/checkpoints').glob('*.pt'))))
for p in (P/'05_STATISTICS').glob('*.csv'):
 if 'pairwise' in p.name or 'bootstrap' in p.name:print(p.name,pd.read_csv(p).columns.tolist())
