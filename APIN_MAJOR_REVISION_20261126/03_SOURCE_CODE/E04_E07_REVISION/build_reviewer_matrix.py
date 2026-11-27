"""Carry 31 G1 reviewer issues forward with evidence-backed G2 stage states."""
from g2_common import *
source=ROOT/'04_EXPERIMENTS/G1_E01_E03_ACCEPTANCE/G1_03_Reviewer_Response_Progress.csv';out=ROOT/'04_EXPERIMENTS/G2_E04_E07_ACCEPTANCE/G2_04_Reviewer_Evidence_Matrix.csv'
g1=pd.read_csv(source).fillna('');e04=ROOT/'04_EXPERIMENTS/E04_SENSITIVITY';e05=ROOT/'04_EXPERIMENTS/E05_ABLATION';e06=ROOT/'04_EXPERIMENTS/E06_MODEL_FAIRNESS';e07=ROOT/'04_EXPERIMENTS/E07_SPATIAL_OPERATIONAL'
checks={
 'E04_T1':(e04/'E04_threshold1_completion.json','E04 1/4 rule'),
 'E04_T3_H1':(e04/'E04_threshold3_h1_completion.json','E04 3/4 H1'),
 'E04_T4':(e04/'E04_Threshold4_Decision_CN.md','E04 4/4 conditional support decision'),
 'E04_H6_STRICT':(e04/'E04_strict6_completion.json','E04 strict H6'),
 'E04_IMPUTE':(e04/'E04_seasonal_impute_completion.json','E04 alternate imputation'),
 'E04_HISTORY':(e04/'E04_history_completion.json','E04 history window'),
 'E05_GRID_CAUSAL':(e05/'E05_returned_only_completion.json','E05 returned-only grid'),
 'E05_MANIFEST':(e05/'E05_returned_only_completion.json','E05 manifest comparison'),
 'E06_TUNE':(e06/'E06_Core_Completion.json','E06 tuning'),
 'E06_GRU_STATIC':(e06/'E06_Core_Completion.json','E06 static GRU'),
 'E07_GIS_CALENDAR_COST':(e07/'E07_New_PC_Inference_Benchmark.csv','E07 GIS/calendar/cost'),
 'E07_FREEFLOW':(ROOT/'04_EXPERIMENTS/G1_E01_E03_ACCEPTANCE/G1_06_Acceptance_Report_CN.md','G1 freeflow reused')}
rows=[]
for g in g1.to_dict('records'):
 req=str(g['remaining_experiment']);codes=[x.strip() for x in req.split(';') if x.strip() in checks or x.strip() in ['E06_SPATIAL','E08_EXTERNAL']];states=[];refs=[]
 for code in codes:
  if code in ['E06_SPATIAL','E08_EXTERNAL']:
   states.append(code+':DEFERRED_CONDITIONAL' if code=='E06_SPATIAL' else code+':NOT_IN_G2_SCOPE');continue
  path,label=checks[code];exists=path.exists();state='DEFERRED_CONDITIONAL_WITH_SUPPORT_EVIDENCE' if code=='E04_T4' and exists else 'EVIDENCE_FILE_PRESENT' if exists else 'PENDING';states.append(code+':'+state);refs.append(str(path.relative_to(ROOT)) if exists else '')
 if 'E05_GRID_CAUSAL' in codes and not (e05/'E05_leaky_scaling_completion.json').exists():states.append('E05_LEAKAGE_DIAGNOSTIC:PENDING')
 if 'E07_GIS_CALENDAR_COST' in codes and not (e07/'E07_GIS_Calendar_Evidence_CN.md').exists():states.append('E07_SOURCE:PENDING')
 if any('PENDING' in x for x in states):status='G2_EVIDENCE_PENDING'
 elif any('DEFERRED' in x or 'NOT_IN_G2_SCOPE' in x for x in states):status='PARTIAL_WITH_EXPLICIT_DEFERRED_ITEM'
 else:status='G2_STAGE_EVIDENCE_AVAILABLE_MANUSCRIPT_PENDING'
 if not codes:status='G1_EVIDENCE_REUSED_EDITORIAL_WORK_PENDING'
 if 'LITERATURE_RELEVANCE_PENDING' in str(g['response_readiness']):readiness='LITERATURE_PENDING'
 elif 'E08_EXTERNAL' in codes or 'EXTERNAL_VALIDATION' in str(g['response_readiness']):readiness='CONDITIONAL_EXTERNAL_VALIDATION'
 elif 'E06_SPATIAL' in codes or 'E04_T4' in codes:readiness='EXPLANATION_WITH_LIMITATIONS'
 elif any('PENDING' in x for x in states):readiness='PARTIALLY_SUPPORTED'
 elif not codes:readiness='EDITORIAL_REVISION_PENDING'
 else:readiness='FULLY_SUPPORTED_FOR_RESPONSE'
 stage_evidence={stage:' | '.join(x for x in states if x.startswith(stage)) for stage in ['E04','E05','E06','E07']}
 rows.append({'comment_id':g['comment_id'],'reviewer_id':g['reviewer_id'],'original_comment':g['original_comment'],'scientific_issue':g['original_comment'],'G1_status':g['response_readiness'],'G1_evidence':' | '.join(str(g[k]) for k in ['E01_evidence','E02_evidence','E03_evidence'] if g[k]),'G1_key_result':g['key_result'],'G2_requested_evidence':req,'E04_evidence':stage_evidence['E04'],'E05_evidence':stage_evidence['E05'],'E06_evidence':stage_evidence['E06'],'E07_evidence':stage_evidence['E07'],'G2_evidence_states':' | '.join(states),'G2_evidence_paths':' | '.join(x for x in refs if x),'G2_issue_status':status,'evidence_readiness':readiness,'remaining_work':g['remaining_data'],'manuscript_section':g['planned_manuscript_section'],'response_strategy':'Cite completed stage evidence and state remaining limitations in the later manuscript response','limitation':'G2 stage evidence is not reviewer acceptance; manuscript and formal response not authored in this phase'})
assert len(rows)==31 and len({x['comment_id'] for x in rows})==31
save(pd.DataFrame(rows),out);print(pd.Series([x['G2_issue_status'] for x in rows]).value_counts().to_dict())
