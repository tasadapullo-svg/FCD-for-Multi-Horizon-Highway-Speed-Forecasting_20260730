import sys,json,os,hashlib,zipfile,io,csv,re,datetime
from pathlib import Path
C=json.loads(Path(__file__).with_name('config.json').read_text()); O=Path(C['out']); R=Path(C['root']); H=Path(C['hist']); repo=H/'20260730_AJSE_FINAL_GitHub'; P=repo/'04_PHASE2A_DATA_RESULTS'
sys.path.insert(0,str(O/'06_AUDIT_SCRIPTS/deps'))
def save(name,rows,fields=None):
 rows=list(rows); fields=fields or list(dict.fromkeys(k for r in rows for k in r)) or ['status','reason']
 with (O/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def role(s):
 s=s.lower()
 for pat,r in [('legacy|phase13','LEGACY'),('prediction','PREDICTION'),('checkpoint|.pt$|.pth$','WEIGHT'),('manifest','FOLD_MANIFEST'),('frozen|.yaml$','MODEL_CONFIG'),('.py$|.ipynb$','MODEL_CODE'),('metric','METRIC'),('statistic','STATISTIC'),('fig','FIGURE_SOURCE'),('tomtom|raw','API_RAW'),('.parquet$|.npy$','PROCESSED_DATA'),('main.tex','OVERLEAF_SOURCE'),('.pdf$','PAPER')]:
  if re.search(pat,s):return r
 return 'UNKNOWN'
files=sorted(set([p for b in [R,H,Path('D:/Desktop/2026112_论文修改')] for p in b.rglob('*') if p.is_file() and O not in p.parents])); inventory=[]; zi=[]; errors=[]
def zipaudit(z,container,depth=0):
 for x in z.infolist():
  if x.is_dir():continue
  try:
   h=hashlib.sha256()
   with z.open(x) as f:
    for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
   zi.append(dict(archive=container,entry=x.filename,size_bytes=x.file_size,crc=x.CRC,crc_status='PASS',sha256=h.hexdigest(),role=role(x.filename)))
   if x.filename.lower().endswith('.zip') and depth<5:
    with zipfile.ZipFile(io.BytesIO(z.read(x))) as zz:zipaudit(zz,container+'!'+x.filename,depth+1)
  except Exception as e:zi.append(dict(archive=container,entry=x.filename,crc_status='ERROR',error=str(e)));errors.append(str(e))
for i,p in enumerate(files):
 try:
  st=p.stat(); h=sha(p);inventory.append(dict(file_id='F'+str(i+1),role=role(str(p)),relative_path=str(p),container_or_zip_entry='',size_bytes=st.st_size,mtime_utc=datetime.datetime.fromtimestamp(st.st_mtime,datetime.timezone.utc).isoformat(),sha256=h,source_type='PHYSICAL_FILE',readability='HASH_READ',version_group=p.name,license_risk='LOCAL_ONLY',status='PASS_HASH_ONLY',note=''))
  if p.suffix.lower()=='.zip':
   with zipfile.ZipFile(p) as z:zipaudit(z,str(p))
 except Exception as e:errors.append(str(p)+':'+str(e))
 if i%200==0:print('inventory',i,len(files),flush=True)
save('00_MANIFESTS/G0_file_inventory.csv',inventory);save('00_MANIFESTS/G0_sha256_manifest.csv',inventory,['relative_path','size_bytes','sha256']);save('00_MANIFESTS/G0_zip_crc_inventory.csv',zi)
(O/'07_LOGS/G0_errors.log').write_text('\n'.join(errors),encoding='utf8');(O/'00_MANIFESTS/inventory_summary.json').write_text(json.dumps(dict(files=len(files),dirs=len(set(str(p.parent) for p in files)),bytes=sum(x['size_bytes'] for x in inventory),zip_entries=len(zi),errors=len(errors))))
print('INVENTORY DONE',len(inventory),len(zi),flush=True)
