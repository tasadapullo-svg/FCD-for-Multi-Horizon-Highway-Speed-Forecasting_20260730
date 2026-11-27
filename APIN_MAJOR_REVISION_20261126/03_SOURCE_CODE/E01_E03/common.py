from pathlib import Path
import sys,os,json,csv,hashlib,datetime,time,re
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];CTL=ROOT/'00_PROJECT_CONTROL';CODE=Path(__file__).resolve().parent
sys.path.insert(0,str(CTL/'deps'))
import numpy as np,pandas as pd,pyarrow.parquet as pq
DER=ROOT/'02_DATA/03_DERIVED_DATA/E01_E03';LOG=ROOT/'04_EXPERIMENTS/G1_E01_E03_ACCEPTANCE/logs'
E01=ROOT/'04_EXPERIMENTS/E01_DATA_COMPLETENESS';E02=ROOT/'04_EXPERIMENTS/E02_TRAFFIC_RELIABILITY';E03=ROOT/'04_EXPERIMENTS/E03_STATISTICAL_INFERENCE';G1=ROOT/'04_EXPERIMENTS/G1_E01_E03_ACCEPTANCE'
for d in [DER,LOG,E01,E02,E03,G1]:d.mkdir(parents=True,exist_ok=True)
V=json.loads((CTL/'verification_evidence.json').read_text(encoding='utf-8'));REPO=Path('\\\\?\\'+V['repo']);BASE=REPO/'04_PHASE2A_DATA_RESULTS'
PROTOCOL=CTL/'G1_Analysis_Protocol.yaml';P=json.loads(PROTOCOL.read_text(encoding='utf-8'));PROTOCOL_SHA=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()
assert PROTOCOL_SHA==json.loads((CTL/'G1_Protocol_Freeze_Receipt.json').read_text(encoding='utf-8'))['sha256']
MODELS=['HA','SeasonalHA','Persistence','Ridge','XGBoost','GRU'];SEEDS=[42,2026,3407];HS=[1,3,6]
PAIRS=[('XGBoost','GRU'),('XGBoost','Ridge'),('XGBoost','SeasonalHA'),('Persistence','HA'),('GRU','Ridge')]
GRID_START=pd.Timestamp(P['time']['grid_start']);GRID_END=pd.Timestamp(P['time']['hour_grid_end']);HOURS=pd.date_range(GRID_START,GRID_END,freq='h');NODES=[f'N{i:03}' for i in range(1,52)]
FOLDS={}
config=(BASE/'00_DEFINITION_FREEZE/phase2a1_frozen.yaml').read_text(encoding='utf-8')
for part in re.split(r'  - fold: ',config)[1:]:
 f=int(part.splitlines()[0]);FOLDS[f]={}
 for split in ['train','validation','test']:
  match=re.search(r"    "+split+r": \['([^']+)', '([^']+)'\]",part)
  FOLDS[f][split]=tuple(pd.Timestamp(s) for s in match.groups())
def norm(p):return str(p).removeprefix('\\\\?\\')
def save(df,path):
 path=Path(path)
 if path.suffix=='.parquet':df.to_parquet(path,index=False)
 else:df.to_csv(path,index=False,encoding='utf-8-sig',float_format='%.12g')
def read(name):return pd.read_parquet(DER/(name+'.parquet'))
def jwrite(p,obj):Path(p).write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
def now():return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
def log(msg):
 text=f'{now()} {msg}';print(text,flush=True)
 with (LOG/'pipeline.log').open('a',encoding='utf-8') as f:f.write(text+'\n')
def metrics(x):
 err=np.asarray(x.y_pred-x.y_true,dtype=float);ae=np.abs(err);return {'n':len(err),'MAE':ae.mean(),'RMSE':np.sqrt(np.mean(err**2)),'Bias':err.mean(),'Median_AE':np.median(ae),'P90_AE':np.quantile(ae,.9),'P95_AE':np.quantile(ae,.95)}
def perf(df,groups):
 rows=[]
 for k,x in df.groupby(groups,observed=True,dropna=False,sort=True):
  k=k if isinstance(k,tuple) else (k,);r=dict(zip(groups,k));r.update(metrics(x));r['nodes']=x.node_id.nunique();r['dates']=x.forecast_origin.dt.normalize().nunique();r['support']='LOW_SUPPORT' if r['n']<30 or r['nodes']<3 or r['dates']<3 else 'SUPPORTED';rows.append(r)
 return pd.DataFrame(rows)
def describe(series):
 x=np.asarray(pd.to_numeric(series,errors='coerce'),dtype=float);n=len(x);x=x[np.isfinite(x)]
 if not len(x):return dict(n=0,missing_or_invalid=n,mean=np.nan,median=np.nan,sd=np.nan,min=np.nan,max=np.nan,p05=np.nan,p25=np.nan,p75=np.nan,p95=np.nan)
 return dict(n=len(x),missing_or_invalid=n-len(x),mean=x.mean(),median=np.median(x),sd=x.std(ddof=0),min=x.min(),max=x.max(),p05=np.quantile(x,.05),p25=np.quantile(x,.25),p75=np.quantile(x,.75),p95=np.quantile(x,.95))
def confbin(x):return np.select([x.isna()|~np.isfinite(x),(x<0)|(x>1),x<.8,x<.9,x<1,x==1],['INVALID_OR_MISSING','OUT_OF_RANGE','c<0.80','0.80<=c<0.90','0.90<=c<1.00','c=1.00'],default='INVALID_OR_MISSING')
def regime(r,t=.7):return np.select([~np.isfinite(r)|(r<0),r<t,r<.9],['UNCLASSIFIED','congested_proxy','intermediate'],default='near_free_flow_proxy')
def covbin(x):return np.select([x<.5,x<.75,x<1,x==1],['[0,.50)','[.50,.75)','[.75,1)','1'],default='INVALID')
def gapbin(x):return np.select([x==0,x<=2,x<=6,x<=12,x<=24],['0','1-2','3-6','7-12','13-24'],default='INVALID')
def agebin(x):return np.select([x==0,x<=2,x<=6,x<=12,x<=24,x<168,x==168],['0','1-2','3-6','7-12','13-24','25-167','168_CAP'],default='INVALID')
def stamp(stage,inputs,outputs,extra=None):
 jwrite(LOG/(stage+'_receipt.json'),{'stage':stage,'completed_at':now(),'protocol_sha256':PROTOCOL_SHA,'code_sha256':hashlib.sha256((CODE/(stage+'.py')).read_bytes()).hexdigest(),'inputs':[norm(p) for p in inputs],'outputs':[str(p) for p in outputs],'extra':extra or {}})
