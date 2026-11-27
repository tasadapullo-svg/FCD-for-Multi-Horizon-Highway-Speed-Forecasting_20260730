from pathlib import Path
import sys,json,csv,zipfile
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];CTL=ROOT/'00_PROJECT_CONTROL'
v=json.loads((CTL/'verification_evidence.json').read_text(encoding='utf-8'));repo=Path('\\\\?\\'+v['repo'])
mode=sys.argv[1] if len(sys.argv)>1 else 'protocol_inputs'
if mode=='tex':
 with zipfile.ZipFile(ROOT/'Applied_Intelligence_20260905.zip') as z:lines=z.read('main.tex').decode('utf-8').splitlines()
 start=int(sys.argv[2]);end=int(sys.argv[3])
 for i in range(start,end):print(i+1,lines[i])
elif mode=='prompt':
 t=Path(r'C:\Users\17279\.codex\attachments\a307f19d-74ea-4b1f-9ea1-4e248807ee1e\已粘贴的文本.txt').read_text(encoding='utf-8');lines=t.splitlines()
 start=int(sys.argv[2]) if len(sys.argv)>2 else 380
 end=int(sys.argv[3]) if len(sys.argv)>3 else 810
 for i in range(start,min(end,len(lines))):print(f'{i+1}: {lines[i]}')
elif mode=='definitions':
 p=repo/'04_PHASE2A_DATA_RESULTS/01_DATA_PIPELINE/folds/fold1/fold_train_parameters.json';print(p.read_text(encoding='utf-8'))
 with zipfile.ZipFile(ROOT/'Applied_Intelligence_20260905.zip') as z:tex=z.read('main.tex').decode('utf-8').splitlines()
 for i,line in enumerate(tex):
  if any(s in line.lower() for s in ['volatil','\\label{eq','ensemble','seeds','eligible origin','at least','scaler','median']):print(i+1,'\n'.join(tex[max(0,i-2):i+4]))
elif mode=='protocol_inputs':
 print('PROJECT_RULES', (CTL/'PROJECT_RULES.md').read_text(encoding='utf-8'))
 print('FROZEN CONFIG', (repo/'04_PHASE2A_DATA_RESULTS/00_DEFINITION_FREEZE/phase2a1_frozen.yaml').read_text(encoding='utf-8'))
 for p in [repo/'04_PHASE2A_DATA_RESULTS/01_DATA_PIPELINE/folds/fold1/fold_train_parameters.json',repo/'04_PHASE2A_DATA_RESULTS/01_DATA_PIPELINE/folds/fold1/H6/sample_build_summary.json']:
  print(p,p.read_text(encoding='utf-8'))
 with zipfile.ZipFile(ROOT/'Applied_Intelligence_20260905.zip') as z:tex=z.read('main.tex').decode('utf-8')
 for i,line in enumerate(tex.splitlines()):
  if any(s in line.lower() for s in ['volatil','eligible','imput','history','threshold','baseline','ensemble','seed','equation','eq:','label{eq']):print('TEX',i+1,line)
 print('G0 CORE')
 for p in (ROOT/'04_EXPERIMENTS/G0_DATA_READINESS').iterdir():
  if p.suffix=='.csv':
   with p.open(encoding='utf-8-sig',newline='') as f:r=list(csv.DictReader(f));print(p.name,len(r),'rows')
  elif p.suffix=='.md': print(p.name,p.read_text(encoding='utf-8')[:19000])
  elif p.suffix=='.json': print(p.name,json.loads(p.read_text(encoding='utf-8'))['overall_status'])
  elif p.suffix=='.xlsx':
   import openpyxl
   w=openpyxl.load_workbook(p,read_only=True,data_only=True)
   for sh in w:print('G0 WORKSHEET',sh.title,len(list(sh.iter_rows(values_only=True))))
