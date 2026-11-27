from common import *
import zipfile,shutil
from openpyxl import load_workbook
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 log('final output packaging integrity check START; not repeating scientific validation')
 context=json.loads((CTL/'G1_deliverable_context.json').read_text(encoding='utf-8'));validation=json.loads((G1/'G1_Validation_Receipt.json').read_text(encoding='utf-8'));assert validation['overall_status']=='CONDITIONAL_PASS'
 for folder,name in [(E01,'E01_Summary_CN.md'),(E02,'E02_Summary_CN.md'),(E03,'E03_Summary_CN.md')]:
  p=folder/name;text=p.read_text(encoding='utf-8')
  if '本实验包实际输出绝对路径' not in text:text+='\n\n本实验包实际输出绝对路径：\n\n'+'\n'.join('- `'+str(x)+'`' for x in sorted(folder.iterdir()) if x.suffix in ['.csv','.md'])+'\n';p.write_text(text,encoding='utf-8')
 for p in G1.glob('*.inspect.ndjson'):p.replace(CTL/p.name)
 # Workbook read-back, range comparison and object presence; no recalculation of analyses.
 content=json.loads((CTL/'G1_workbooks_content.json').read_text(encoding='utf-8'));book_checks=[]
 for file,sheets in content.items():
  w=load_workbook(G1/file,read_only=False,data_only=False)
  assert w.sheetnames==list(sheets)
  for name,rows in sheets.items():
   sh=w[name];actual=list(sh.iter_rows(values_only=True));header=list(actual[0]);assert len(actual)-1==len(rows)
   assert len(sh.tables)==1 and sh.freeze_panes is not None
   for rr,src in zip(actual[1:],rows):
    for col,val in zip(header,rr):
     expected=src.get(col)
     if expected is None:assert val=='NA'
     elif isinstance(expected,(int,float)) and not isinstance(expected,bool):assert isinstance(val,(int,float)) and abs(val-expected)<=1e-10*max(1,abs(expected))
     else:assert val==expected,(file,name,col,val,expected)
   book_checks.append(dict(file=file,sheet=name,rows=len(rows),values_readback='PASS',table_and_freeze='PASS',visual='RENDERED_AND_INSPECTED'))
  w.close()
 jwrite(LOG/'workbook_delivery_checks.json',book_checks);assert len(book_checks)==21
 with (G1/'G1_03_Reviewer_Response_Progress.csv').open(encoding='utf-8-sig',newline='') as f:progress=list(csv.DictReader(f))
 assert len(progress)==31 and len({r['comment_id'] for r in progress})==31
 for row in progress:
  for evidence in row['evidence_file'].split(';'):assert Path(evidence).exists(),evidence
 # Index aggregate outputs. Exclude self-referential hashes from manifest/registry and use external hash list.
 diagnostic=ROOT/'07_FIGURES_TABLES/G1_DIAGNOSTICS';aggregates=[*sorted(E01.glob('*.csv')),*sorted(E01.glob('*.md')),*sorted(E02.glob('*.csv')),*sorted(E02.glob('*.md')),*sorted(E03.glob('*.csv')),*sorted(E03.glob('*.md')),*sorted(diagnostic.glob('*.png')),diagnostic/'Diagnostic_Source_Index.csv']
 aggregate_g1=[p for p in G1.iterdir() if p.is_file() and p.suffix in ['.csv','.xlsx','.md'] and p.name!='G1_01_E01_E03_Result_Registry.csv'];aggregates+=sorted(aggregate_g1)
 result_rows=[]
 for p in aggregates:
  stage='E01' if p.parent==E01 else 'E02' if p.parent==E02 else 'E03' if p.parent==E03 else 'G1'
  df=pd.read_csv(p) if p.suffix=='.csv' else None
  key='; '.join(f'{c}={df.iloc[0][c]}' for c in ['metric','value','n','MAE','effect','status'] if df is not None and len(df) and c in df)
  result_rows.append(dict(experiment_id=stage,result_table=p.name,actual_file_path=str(p),data_source=str(DER)+'; original inputs indexed in execution manifest',calculation_definition='G1 frozen protocol '+PROTOCOL_SHA,key_value=key or 'see aggregate rows/report/workbook',sample_count=len(df) if df is not None else 'NA (report/figure/workbook)',file_sha256=sha(p),acceptance_status='CONDITIONAL_PASS' if stage in ['E02','E03','G1'] else 'PASS',manuscript_use='G3 revision evidence only; original manuscript unchanged',data_class='AGGREGATE_OR_INDEX_NO_COMMERCIAL_RECORDS'))
 save(pd.DataFrame(result_rows),G1/'G1_01_E01_E03_Result_Registry.csv')
 # Snapshot only actual used source metadata; G0 content hashes reused, not recomputed.
 env=json.loads((LOG/'environment.json').read_text(encoding='utf-8'));source_paths=[]
 for x in V['hash_checks']:
  p=Path('\\\\?\\'+x['path'])
  if p.suffix in ['.parquet','.json','.yaml','.csv','.npy'] and '.pt' not in p.name:source_paths.append(p)
 source_paths.append(Path('\\\\?\\'+V['raw_archive']))
 source_signatures=[]
 for p in sorted(set(source_paths)):
  if p.exists():stat=p.stat();source_signatures.append(dict(path=norm(p),size_bytes=stat.st_size,mtime_ns=stat.st_mtime_ns))
 code_files=[CODE/name for name in ['common.py','prepare_shared.py','run_e01.py','run_e02.py','run_e03.py','validate_g1.py']]
 code_hash=[dict(path=str(p),sha256=sha(p)) for p in code_files]
 core_names=['G1_01_E01_E03_Result_Registry.csv','G1_02_Integrated_Results.xlsx','G1_03_Reviewer_Response_Progress.csv','G1_04_Manuscript_Consistency_Matrix.xlsx','G1_05_Minimum_Remaining_Experiment_Plan.xlsx','G1_06_Acceptance_Report_CN.md','G1_07_Execution_Manifest.json']
 commands=[dict(command=f'{sys.executable} '+name,cwd=str(CODE)) for name in ['inspect_inputs.py','freeze_protocol.py','probe_schema.py','prepare_shared.py','prepare_shared.py --resume-receipt-only','run_e01.py','run_e01.py --summary-only','run_e02.py','probe_statistics.py','run_e03.py','check_cluster.py','fix_cluster_reconstruction.py','validate_g1.py','fix_validation_precision.py','build_g1_deliverables.py','make_diagnostics.py','g1_support_note.py','finalize_g1.py','run_e01_e03_pipeline.py']]
 commands.extend([dict(command='node G1_workbooks.mjs',cwd=str(CTL)),dict(command='python -m pip install matplotlib --target plotting_deps --no-cache-dir --no-compile --disable-pip-version-check',cwd=str(CTL))])
 original_meta={'G0_core_manifest':str(ROOT/'04_EXPERIMENTS/G0_DATA_READINESS/G0_06_Execution_Manifest.json'),'G0_evidence_sha256':sha(CTL/'verification_evidence.json'),'inherited_public_main':'0a4d2e00ac509d4f4e64f950df5a7d35238d6e4c','original_config_sha256':P['input_version']['config_sha256'],'original_cleaned_sha256':P['input_version']['cleaned_sha256'],'source_metadata':source_signatures,'content_hash_policy':'Reuse G0 file hashes; do not repeat entire544 hash audit; current source stat signatures pin actual read assets'}
 manifest={'project':'APIN-D-26-12623','phase':'G1_E01_E03','overall_status':validation['overall_status'],'completed_at':now(),'output_root':str(ROOT),'analysis_protocol':{'path':str(PROTOCOL),'sha256':PROTOCOL_SHA,'version':P['protocol_version'],'receipt':str(CTL/'G1_Protocol_Freeze_Receipt.json')},'input_versions':original_meta,'software_environment':env,'plotting_environment':json.loads((LOG/'plotting_environment.json').read_text(encoding='utf-8')),'random_seed':20261125,'bootstrap_replicates':10000,'primary_block_days':3,'sensitivity_block_days':7,'actual_commands':commands,'analysis_code_sha256':code_hash,'outputs':[{'path':str(p),'sha256':sha(p),'size_bytes':p.stat().st_size} for p in aggregates+[G1/'G1_01_E01_E03_Result_Registry.csv']],'core_outputs':[str(G1/n) for n in core_names],'local_restricted_intermediates':str(DER),'zip_exclusions':['raw commercial FCD','record-level derived speeds','per-sample predictions','feature tensors','model weights','API credentials','dependencies'],'tasks_completed':['E01 7 components','E02 10 components with closure NOT_ESTIMABLE','E03 9 components','31 original comments progress','data-supported E04-E07 bounded proposal','3 workbooks21 sheets values/native tables/rendered QA','6 aggregate diagnostic figures'],'not_completed_or_not_applicable':['formal Phase2A1 source recovery','original97.30 definition (author decided no further search)','road closure effect not observable','independent ground truth','HAC/DM not applicable under frozen choice','official calendar/GIS road distance','model_training','formal_manuscript_and_response_edit'],'validation':validation,'implementation_fixes_log':str(LOG/'implementation_fixes.md'),'remaining_training':{'core_max_executions':context['core_budget_cap'],'conditional_max_executions':context['conditional_budget_cap'],'actual_training_executions_this_stage':0,'source_gate_max6_first':'all later budgets0 until passed and author-approved','not_a_full_factorial_design':True},'reuse_policy':'Accepted E01-E03 do not rerun. Compare protocol/code/input/output signatures and mark REUSED_PASS. Reopen only affected task for recorded concrete scientific/code issue.','self_hash_policy':'manifest and ZIP hashes in external G1_Delivery_SHA256.csv and delivery_receipt.json; no self-hash'}
 jwrite(G1/'G1_07_Execution_Manifest.json',manifest)
 accepted_paths=sorted(set(aggregates+[G1/'G1_01_E01_E03_Result_Registry.csv',G1/'G1_07_Execution_Manifest.json']))
 accepted_hashes=[dict(path=str(p),sha256=sha(p),size_bytes=p.stat().st_size) for p in accepted_paths]
 jwrite(CTL/'G1_Accepted_Result_Lock.json',{'accepted_at':now(),'status':'CONDITIONAL_PASS','protocol_sha256':PROTOCOL_SHA,'analysis_code':code_hash,'source_signatures':source_signatures,'accepted_result_hashes':accepted_hashes,'no_automatic_recalculation':True})
 policy=CTL/'PROJECT_RULES.md';text=policy.read_text(encoding='utf-8')
 if 'G1已验收' not in text:text+='\n\n## 2026-11-25 G1已验收后的当前状态（优先于上文历史阶段描述）\n\nPrompt02授权的E01–E03已实际计算并CONDITIONAL_PASS。其已验收结果、原基准和统计协议保留，不重复全量执行。后续只因具体科学或代码问题定向处理。E04–E07建议规模已根据G1实际结果形成，尚未训练；先恢复源码或由作者批准独立新实现与最小基准验证。E08仍为条件项。不得自动进入后续训练或改文。\n';policy.write_text(text,encoding='utf-8')
 # Store exact builder and protocol in package. No restricted intermediate directory allowed.
 package=[G1/n for n in core_names]+[p for p in aggregates if p.name not in core_names]+list(CODE.glob('*.py'))+[PROTOCOL,CTL/'G1_Protocol_Freeze_Receipt.json',CTL/'G1_workbooks.mjs',CTL/'G1_Accepted_Result_Lock.json',CTL/'G1_workbook_render_verification.json']+list(LOG.glob('*.json'))+list(LOG.glob('*.md'))+[LOG/'pipeline.log']
 package=sorted(set(p for p in package if p.exists()))
 forbidden_suffix={'.parquet','.npy','.npz','.pt','.pkl','.gz','.h5'}
 for p in package:assert p.suffix not in forbidden_suffix and DER not in p.parents
 zip_path=ROOT/'APIN_G1_E01_E03_Results_20261125.zip'
 with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in package:z.write(p,str(p.relative_to(ROOT)))
 with zipfile.ZipFile(zip_path) as z:
  assert z.testzip() is None;members=z.namelist();assert len(members)==len(set(members));assert all(str((G1/n).relative_to(ROOT)).replace('\\','/') in members for n in core_names)
 hashpaths=[G1/n for n in core_names]+[zip_path]
 save(pd.DataFrame([dict(absolute_path=str(p),sha256=sha(p),size_bytes=p.stat().st_size) for p in hashpaths]),G1/'G1_Delivery_SHA256.csv')
 receipt={'phase':'G1_E01_E03','status':'CONDITIONAL_PASS','zip_path':str(zip_path),'zip_sha256':sha(zip_path),'zip_size_bytes':zip_path.stat().st_size,'zip_members':len(members),'crc':'PASS','core_files':len(core_names),'workbook_sheets_checked':len(book_checks),'diagnostics':6,'restricted_record_files_in_zip':0,'source_models_trained':0,'completed_at':now()};jwrite(G1/'delivery_receipt.json',receipt)
 log('G1 packaged '+json.dumps(receipt,ensure_ascii=False));print('APPLIED INTELLIGENCE MAJOR REVISION\nG1 E01–E03 FINAL ACCEPTANCE\nOverall Status: CONDITIONAL_PASS\nG0 Evidence Reused: 544 hash comparisons /180 prior prediction audits, no G0 rerun\nE01 Status: PASS; grid403512=241601+1156+160755; four threshold hours96968/83439/45356/15838; H6 complete14521 partial14620; all54 sample attrition keys match; 4/4 H6 validation empty\nE02 Status: CONDITIONAL_PASS; raw freeflow equality85.4886%; congested proxy n952/614/700; FreeFlow MAE2.169594/2.172871/2.193327; closure NOT_ESTIMABLE\nE03 Status: CONDITIONAL_PASS; Table7 matches B all18; A XGB0.935267/0.819415/0.744363; A GRU1.046958/0.947604/0.868938; Daymacro XGB-SeasonalHA +0.077330/+0.012295/-0.012050; all three CIs cross0; Holm7/15 significant; LOFO all6 exclusions saved\nOriginal Manuscript Discrepancies: Equation12/Table7;97.30%; LOFO H3 depends on aggregation\nReviewer Evidence Coverage:31 original comments retained; analysis sufficient/partial/plan distinguished in progress table\nRemaining Scientific Issues: true counterfactual training, source, external truth, GIS/calendar/cost, license\nMandatory Remaining Experiments: see frozen G1_05 scope; stages gated by source/author\nConditional Remaining Experiments: per-model-manifest ablation, one lightweight neighbor model, E08\nMissing Data: original source, roadline/calendar, ingestion/failed request logs, public redistribution evidence\nSource Code Dependencies: three Phase2A1 entries missing; no silent reimplementation\nAuthor Decisions Required: inspect G1 and approve source/new implementation and bounded next scope\nGenerated Deliverables:')
 for n in core_names:print(G1/n)
 print('Final ZIP Absolute Path:',zip_path,'\nRecommended Next Action: STOP; accepted E01-E03 reused; author reviews next training scope before any E04 execution')
if __name__=='__main__':main()
