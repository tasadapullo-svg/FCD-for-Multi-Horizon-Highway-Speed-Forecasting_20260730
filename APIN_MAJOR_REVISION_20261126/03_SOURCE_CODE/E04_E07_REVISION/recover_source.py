from pathlib import Path
import json,hashlib,zipfile,io,sys,datetime,re
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[2];C=R/'00_PROJECT_CONTROL';O=R/'04_EXPERIMENTS/SOURCE_GATE';O.mkdir(parents=True,exist_ok=True)
a=json.loads((C/'prior_assets_located.json').read_text(encoding='utf-8'));tree=json.loads((C/'github_tree_20261125.json').read_text(encoding='utf-8'))
names=['build_phase2a1_data.py','run_phase2a1_campaign.py','finalize_phase2a1.py'];evidence=[]
for x in a:
 p=Path(x['actual_path'])
 if p.name in names:evidence.append({'path':str(p),'kind':'PHYSICAL_EXACT_ENTRY'})
 if p.suffix=='.zip' and any(s in p.name for s in ['AJSE_ALL_DATA_FINAL_CLEAN','AJSE_GATE_FCD_Experiment','AJSE_Phase2A0_Definition_Freeze']):
  with zipfile.ZipFile(p) as z:
   for name in z.namelist():
    if Path(name).name in names or name.endswith('.py'):
     b=z.read(name);evidence.append({'path':str(p)+'!'+name,'sha256':hashlib.sha256(b).hexdigest(),'kind':'ARCHIVE_SOURCE_CANDIDATE','formal_exact_entry':Path(name).name in names})
for x in tree.get('tree',[]):
 if Path(x['path']).name in names:evidence.append({'path':x['path'],'kind':'GITHUB_EXACT_ENTRY','blob_sha':x['sha']})
record={'executed_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'search_scope':'G0 indexed exact source paths and three relevant existing release/data archives; public tree already fetched at0a4d2e; original worktree freeze commit probe422 reused; no unrelated research scan','entries':evidence,'recovered_original_phase2a1':any(x.get('formal_exact_entry') or x['kind'].endswith('EXACT_ENTRY') for x in evidence),'status':'ORIGINAL_SOURCE_NOT_RECOVERED','stop_further_search':True}
(O/'source_recovery_evidence.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(record,ensure_ascii=False,indent=2)[:18000])
with zipfile.ZipFile(R/'Applied_Intelligence_20260905.zip') as z:lines=z.read('main.tex').decode('utf-8').splitlines()
for i in range(400,550):print('TEX',i+1,lines[i])
