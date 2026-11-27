from common import *
for p in (BASE/'05_STATISTICS').iterdir():
 print(p.name,p.stat().st_size)
 if p.suffix=='.csv':
  x=pd.read_csv(p);print(x.columns.tolist());print(x.head(2).to_string(index=False))
