from pathlib import Path
import sys,json,zipfile,importlib.util,os,subprocess
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[2];C=R/'00_PROJECT_CONTROL';mode=sys.argv[1] if len(sys.argv)>1 else 'inputs'
if mode=='prompt':
 p=Path(r'C:\Users\17279\.codex\attachments\26693caa-a759-4883-9b49-435a3cfcaf47\已粘贴的文本.txt');t=p.read_text(encoding='utf-8');lines=t.splitlines();start=int(sys.argv[2]) if len(sys.argv)>2 else 0;end=int(sys.argv[3]) if len(sys.argv)>3 else len(lines)
 for i in range(start,min(end,len(lines))):print(i+1,lines[i])
elif mode=='skill':
 p=Path('C:/Users/17279/.codex/plugins/cache/openai-primary-runtime/spreadsheets/26.1123.11515/skills/spreadsheets/SKILL.md');print(p.read_text(encoding='utf-8'))
elif mode=='inputs':
 print('PACKAGES',{n:bool(importlib.util.find_spec(n)) for n in ['torch','sklearn','xgboost','numpy','pandas','geopandas','shapely','pyproj','networkx','requests']})
 print('PYTHON candidates')
 for cmd in [['where','python'],['where','conda'],['where','nvidia-smi']]:
  p=subprocess.run(cmd,capture_output=True,text=True,errors='replace');print(cmd,p.stdout)
 for folder in [R/'04_EXPERIMENTS/G0_DATA_READINESS',R/'04_EXPERIMENTS/G1_E01_E03_ACCEPTANCE']:
  for p in sorted(folder.iterdir()):
   if p.suffix=='.csv':
    import csv
    with p.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f));print(p.name,len(rows),list(rows[0]) if rows else [])
   elif p.suffix=='.md':print(p.name,p.read_text(encoding='utf-8')[:20000])
   elif p.suffix=='.json':d=json.loads(p.read_text(encoding='utf-8'));print(p.name,'keys',list(d))
   elif p.suffix=='.xlsx':
    import openpyxl
    w=openpyxl.load_workbook(p,read_only=True,data_only=True)
    for s in w:print('SHEET',s.title,len(list(s.iter_rows(values_only=True))))
 v=json.loads((C/'verification_evidence.json').read_text(encoding='utf-8'));repo=Path('\\\\?\\'+v['repo'])
 print('CONFIG',(repo/'04_PHASE2A_DATA_RESULTS/00_DEFINITION_FREEZE/phase2a1_frozen.yaml').read_text(encoding='utf-8'))
 assets=json.loads((C/'prior_assets_located.json').read_text(encoding='utf-8'))
 for x in assets:
  p=Path(x['actual_path'])
  if p.suffix in ['.py','.zip'] and any(s in p.name.lower() for s in ['phase2a','source','final','experiment','pipeline']):print('SOURCE CANDIDATE',p)
