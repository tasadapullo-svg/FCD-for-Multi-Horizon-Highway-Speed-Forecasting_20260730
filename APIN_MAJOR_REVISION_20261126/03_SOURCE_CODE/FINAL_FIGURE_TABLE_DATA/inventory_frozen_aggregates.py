from pathlib import Path
import csv, hashlib
import pandas as pd

root=Path(r'E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改')
out=root/'07_FIGURES_TABLES/FINAL_FIGURE_TABLE_DATA/08_MASTER_RESEARCH_RESULTS'
out.mkdir(parents=True,exist_ok=True)
rows=[]
for p in sorted((root/'04_EXPERIMENTS').rglob('*.csv')):
 try:
  df=pd.read_csv(p,nrows=2,encoding='utf-8-sig')
  with p.open('rb') as f:
   n=sum(b.count(b'\n') for b in iter(lambda:f.read(1024*1024),b''))-1
  h=hashlib.sha256(p.read_bytes()).hexdigest()
  rows.append({'relative_path':str(p.relative_to(root)).replace('\\','/'),'stage':p.parent.name,'filename':p.name,'rows_approx':n,'columns':len(df.columns),'column_names':' | '.join(df.columns),'size_bytes':p.stat().st_size,'sha256':h,'status':'READABLE'})
 except Exception as e:rows.append({'relative_path':str(p.relative_to(root)).replace('\\','/'),'stage':p.parent.name,'filename':p.name,'status':'UNREADABLE:'+str(e)})
pd.DataFrame(rows).to_csv(out/'Frozen_Aggregate_Source_Inventory.csv',index=False,encoding='utf-8-sig')
print('FROZEN_CSV',len(rows),'READABLE',sum(x['status']=='READABLE' for x in rows))
