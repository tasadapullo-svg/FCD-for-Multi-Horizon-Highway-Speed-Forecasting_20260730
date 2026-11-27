"""Build Prompt04 evidence tables and workbook payload from accepted G1/G2 and targeted checks."""
from pathlib import Path
import pandas as pd,json,csv,hashlib,datetime
from openpyxl import load_workbook

R=Path(__file__).resolve().parents[2];T=R/'04_EXPERIMENTS/FINAL_TARGETED_CHECKS';F=R/'05_FINAL_RESULTS/FINAL_EVIDENCE_CLOSURE';L=R/'05_FINAL_RESULTS/FINAL_EVIDENCE_LIBRARY'
for p in (T,F,L):p.mkdir(parents=True,exist_ok=True)
G2=R/'04_EXPERIMENTS/G2_E04_E07_ACCEPTANCE';G1=R/'04_EXPERIMENTS/G1_E01_E03_ACCEPTANCE'
def read(p):return pd.read_csv(p).fillna('')
def save(name,rows):
 p=T/name;pd.DataFrame(rows).to_csv(p,index=False,encoding='utf-8-sig');return p
def tab(name,source,df):return {'name':name,'title':name,'source':source,'headers':list(df.columns),'rows':df.fillna('').astype(object).where(pd.notna(df),'').values.tolist()}
stats=read(T/'Final_Statistical_Inference.csv');sens=read(T/'Final_Statistical_Sensitivity_3d_7d.csv');claims=read(T/'Final_Scientific_Claims_Registry.csv')
bench=read(T/'Simple_Baseline_Inference_Benchmark.csv')
ridge=json.loads((T/'Ridge_Impact_Summary.json').read_text(encoding='utf-8'));gis=json.loads((T/'GIS_Final_Summary.json').read_text(encoding='utf-8'))

# S06: existing independent assets absent. One public fallback has unverified data redistribution terms.
e08=pd.DataFrame([
 {'priority':1,'candidate':'Pan Borneo same corridor, later independent FCD','local_asset':'NOT_FOUND','source':'local RAW_SOURCE and 02_EXTERNAL_DATA file inventory','independent_question':'future time, same corridor','fields_frequency':'not established','period':'no later archive','license':'AUTHOR_CONFIRMATION_REQUIRED','download':'none','size':'unknown','decision':'NOT_CURRENTLY_EXECUTABLE'},
 {'priority':2,'candidate':'Other corridor, same supplier FCD','local_asset':'NOT_FOUND','source':'local RAW_SOURCE and 02_EXTERNAL_DATA file inventory','independent_question':'cross corridor, same source','fields_frequency':'not established','period':'none','license':'AUTHOR_CONFIRMATION_REQUIRED','download':'none','size':'unknown','decision':'NOT_CURRENTLY_EXECUTABLE'},
 {'priority':3,'candidate':'METR-LA fixed loop detector speed benchmark','local_asset':'NOT_DOWNLOADED','source':'https://github.com/liyaguang/DCRNN ; project README links canonical Google Drive HDF5','independent_question':'cross data source protocol stress test only','fields_frequency':'timestamp x 207 sensors; 5-minute speed; unit and zero/missing semantics require file-level confirmation','period':'March–June 2012 (exact endpoints require source file check)','license':'Repository MIT is code license; raw METR-LA data license NOT VERIFIED','download':'author decision required; canonical README Google Drive link','size':'not verified before download','decision':'CANDIDATE_ONLY_NOT_ELIGIBLE_WITH_CURRENT_EVIDENCE'}
])
save('E08_Data_Feasibility_and_Decision.csv',e08)
(T/'E08_Minimum_External_Validation_Plan.md').write_text('# E08 决策：NOT_FEASIBLE_WITH_CURRENT_DATA\n\n工程内仅见原 Pan Borneo 商业 FCD 包，无同走廊后续独立时期或其他走廊的合格归档。R1-08 的测试集历史暴露和 R2-04 的独立评价时期因此不能宣称解决；R2-01 跨道路泛化、R3-12 同址真实速度也未验证。\n\n唯一公开候选 METR-LA 为美国固定环路检测器速度序列，项目原始 DCRNN README 给出 HDF5 下载入口；仓库 MIT 仅能证明代码许可，不能据此认定数据可再分发。原文件的精确日期、速度单位、零值/缺失定义、大小尚需下载后核验。人工模拟缺失只能测试算法压力，不能验证商业 FCD 的真实返回机制，也不能验证 Pan Borneo 同址真实速度。\n\n若作者随后确认合法获取并批准 E08：只取一个 METR-LA 数据集；按原时间顺序划分独立测试段；由5分钟序列构造真实观测小时与 H1/H3/H6 未来窗口平均目标，共同样本比较 SeasonalHA、Persistence、XGBoost、GRU；冻结原模型选择规则，只允许数据维度适配，不复制 E04–E06 全部实验；记录传感器数、有效小时、真实缺失、训练/测试边界、机器耗时。预计需数十次模型拟合，预算须在文件级数据核验后确定。不得将该结果表述为商业 FCD 或当地真实速度的外部验证。本阶段未下载或训练，作者须先确认数据许可及获取方式。\n\n官方项目：https://github.com/liyaguang/DCRNN\n',encoding='utf-8')

# S07: rights are independent questions; no contract was located.
rights=[]
for item,known in [
 ('商业API获取及作者本机受控研究','已有历史采集与研究成果；适用合同未见'),
 ('商业原始FCD公开分发','无授予证据'),
 ('派生矩阵与逐样本预测公开分发','无授予证据'),
 ('聚合统计与匿名图表公开发表','无明确合同条款；期刊发表实践不能代替许可'),
 ('分析和新训练代码公开','作者新实现可评估公开；仍需排除密钥和受限数据'),
 ('训练权重公开','可能泄露商业训练数据特征；无授予证据')]:
 rights.append({'material_or_action':item,'observed_evidence':known,'permission_status':'AUTHOR_CONFIRMATION_REQUIRED','public_package':'NO until rights confirmed' if '代码' not in item else 'Code only after author review','local_restricted':'YES','required_document':'historical subscription/contract/API terms and author decision'})
save('Data_Licensing_and_Distribution_Matrix.csv',rights)
(T/'Reproducibility_Evidence_Statement.md').write_text('# 可复现性边界\n\n原正式训练源码未恢复，原历史预测与 G0 证据冻结；G2 是独立新实现，SOURCE_GATE 为 PASS_NEW_IMPLEMENTATION，同实现匹配基准用于 E04–E07。可供复现的候选材料为新实现训练/评价代码、冻结协议、字段与样本构造说明、聚合统计及不含真实商业数据的使用示例。原始商业 FCD、派生矩阵、逐样本预测和模型权重均限本机，公开权限需作者依据实际合同确认。只凭现时通用网站条款不能倒推历史授权。GitHub 本轮只读，未推送。\n',encoding='utf-8')
(T/'Author_Permission_Decisions.md').write_text('# 作者需核定的实际许可决定\n\n1. 提供原始订阅/合同/API条款，确认当时的研究、论文聚合发表及数据派生权。\n2. 分别确认原始 FCD、逐样本预测、派生矩阵、模型权重和代码能否公开。\n3. 确认 METR-LA 官方数据获取及使用条款后，决定是否启动 E08。\n\n在明确书面依据前，本轮交付 ZIP 仅含聚合结果、代码与证据摘要，不含上述受限数据。\n',encoding='utf-8')

# S08: publisher/official-source metadata checks. Full text not claimed unless open official PDF.
lit=[
('R1-06','Separating the predictable part of returns with CNN-GRU-attention from inputs to predict stock returns','Jiahao Yang et al.',2024,'Applied Soft Computing','10.1016/j.asoc.2024.112116','https://www.sciencedirect.com/science/article/pii/S1568494624008901','publisher abstract; full text not verified','stock forecasting temporal decomposition; indirect','method context only','Related work','OPTIONAL','Different target and data mechanism'),
('R1-06','Enhancing stock ranking forecasting by modeling returns with heteroscedastic Gaussian Distribution','Jiahao Yang et al.',2025,'Physica A','10.1016/j.physa.2025.130442','https://www.sciencedirect.com/science/article/pii/S0378437125000949','publisher abstract; full text not verified','uncertainty modeling; indirect','conceptual context only','Limitations','OPTIONAL','No FCD uncertainty estimate validated'),
('R1-06','A hierarchical deep model integrating economic facts for stock movement prediction','Jiahao Yang et al.',2024,'Engineering Applications of Artificial Intelligence','10.1016/j.engappai.2024.108320','https://www.sciencedirect.com/science/article/pii/S0952197624004780','publisher abstract; full text not verified','economic facts not used in current traffic experiment','none direct','none','EXCLUDE','Cross domain and does not support performed model'),
('R2-03','Feature selection in image analysis: a survey','Verónica Bolón-Canedo; Beatriz Remeseiro',2020,'Artificial Intelligence Review','10.1007/s10462-019-09750-3','https://link.springer.com/article/10.1007/s10462-019-09750-3','publisher abstract; full text not verified','DOI supplied as Kolmogorov complexity evidence but article is image feature selection','does not support claimed rapid gain','Response explanation','EXCLUDE','DOI-title-topic mismatch'),
('R2-03','Machine learning enabled orthogonal camera goniometry for accurate and robust contact angle measurements','authors not confirmed from publisher',2023,'Scientific Reports','10.1038/s41598-023-28763-1','https://www.nature.com/articles/s41598-023-28763-1','institutional metadata only; publisher page inaccessible','DOI supplied as Kolmogorov complexity evidence but article is contact-angle measurement','does not support claimed rapid gain','Response explanation','EXCLUDE','DOI-topic mismatch; verify publisher metadata if citation reconsidered'),
('R3-05','Driving Economic Value: Assessing the Financial Impact of Dynamic Message Signs on Freeways','Mousa Ahmad Abushattal et al.',2025,'Civil Engineering Journal','10.28991/CEJ-2025-011-07-023','https://civilejournal.org/index.php/cej/article/download/5774/1892/16242','official open PDF metadata/abstract','operational DMS economics; no benefit-cost model here','context only; no quantitative extrapolation','Discussion','OPTIONAL','Cannot infer forecast economic value'),
('R3-09','Real-Time Vehicle Type Detection and Counting for Emission Pollution Monitoring and Traffic Violation Identification','Mizanur Rahman et al.',2025,'Emerging Science Journal','10.28991/ESJ-2025-09-02-023','https://research.bond.edu.au/en/publications/real-time-vehicle-type-detection-and-counting-for-emission-pollut/','institutional open full text available; abstract checked','video vehicle detection rather than FCD forecasting','none direct','Response explanation','EXCLUDE','Different sensing and outcome'),
('R3-09','Smart Roundabout Coordination Systems for Sustainable Urban Mobility','Ahmed T. M. Halawani',2025,'Civil Engineering Journal','10.28991/CEJ-2025-011-02-013','https://civilejournal.org/index.php/cej/article/view/5498','official abstract; open PDF available','intersection control rather than highway speed forecasting','none direct','Response explanation','EXCLUDE','Different intervention and outcome')
]
cols=['reviewer_comment','article_title','authors','year','journal','doi','publisher_url','full_text_availability','relevance_to_manuscript','evidence_supported','proposed_citation_location','decision','decision_rationale']
litdf=pd.DataFrame(lit,columns=cols);save('Final_Reviewer_Recommended_Literature.csv',litdf)
methods=[
 {'topic':'Holm familywise correction','reference':'Holm S. A simple sequentially rejective multiple test procedure. Scandinavian Journal of Statistics 6:65–70 (1979).','doi':'none confirmed','official_or_original_url':'https://www.ime.usp.br/~abe/lista/pdf4R8xPVzCnX.pdf','decision':'INCLUDE','use':'G1 five comparisons per horizon and 7-day sensitivity'},
 {'topic':'Dependent-observation block bootstrap','reference':'Künsch HR. The Jackknife and the Bootstrap for General Stationary Observations. Annals of Statistics 17 (1989).','doi':'10.1214/aos/1176347265','official_or_original_url':'https://doi.org/10.1214/aos/1176347265','decision':'INCLUDE','use':'background for temporal block dependence; exact implemented resampling defined by G1 protocol'},
 {'topic':'XGBoost','reference':'Chen T; Guestrin C. XGBoost: A Scalable Tree Boosting System. KDD (2016).','doi':'10.1145/2939672.2939785','official_or_original_url':'https://doi.org/10.1145/2939672.2939785','decision':'INCLUDE','use':'model method'},
 {'topic':'Spatial temporal benchmark','reference':'Li Y; Yu R; Shahabi C; Liu Y. Diffusion Convolutional Recurrent Neural Network: Data-Driven Traffic Forecasting. ICLR (2018).','doi':'none confirmed','official_or_original_url':'https://openreview.net/forum?id=SJiHXGWAZ','decision':'INCLUDE_AS_CONTEXT','use':'explain spatial graph models and why current topology limits experiment'}
]
save('Final_Required_Method_References.csv',methods)
save('Literature_Missing_FullText_List.csv',litdf[litdf.full_text_availability.str.contains('not verified|inaccessible')][['reviewer_comment','article_title','doi','publisher_url','full_text_availability']])

# S09: retain all verbatim comments, inherited evidence and explicit final decisions.
m=read(G2/'G2_04_Reviewer_Evidence_Matrix.csv')
external={'R1-08','R2-01','R2-04','R3-12'}
editorial={'R1-10','R3-07'}
explanation={'R1-04','R1-06','R3-05','R3-09','R6-01'}
notestim={'R6-04'}
def status(i):
 if i in external:return 'EXTERNAL_VALIDATION_PENDING'
 if i in editorial:return 'EDITORIAL_REVISION_PENDING'
 if i in explanation:return 'EXPLANATION_ONLY'
 if i in notestim:return 'NOT_ESTIMABLE'
 return 'PARTIALLY_ADDRESSED'
m['final_adoption_status']=m.comment_id.map(status)
m['actual_final_evidence']=m['G1_key_result'].astype(str)+' | G2: '+m['G2_evidence_states'].astype(str)
m['statistical_basis']=m.comment_id.map(lambda i:'G1 day-macro 3-day primary/7-day sensitivity, Holm within five per horizon' if i in {'R1-01','R2-04','R3-08','R6-02'} else 'Descriptive or not tested; see evidence paths')
m['significance_status']=m.comment_id.map(lambda i:'G1 7 significant primary; XGB–SeasonalHA non-significant; G2 four key contrasts non-significant' if i in {'R1-01','R2-04','R3-08','R6-02'} else 'No new significance claim')
m['final_evidence_paths']=m.G2_evidence_paths.astype(str)+' | 04_EXPERIMENTS/FINAL_TARGETED_CHECKS'
m['specific_manuscript_change']=m.remaining_work.astype(str)
m['final_limitation']=m.limitation.astype(str)
for i,s in {
 'R2-02':'4/4 H6 validation empty in all 6 folds; H3 validation only 8 pooled; H1 512 pooled, min fold 21. Conditional training not estimable.',
 'R1-06':'Spatial neighbor model 0 fits; historical directed topology and causal neighbor feature not verified.',
 'R6-04':'Spatial neighbor model 0 fits; GRU with static node attributes is not spatial neighbor model.',
 'R1-08':'Original terminal test previously exposed; no new truly independent period in local assets.',
 'R2-01':'Single corridor only; no cross corridor validation.',
 'R2-04':'Day-block inference completed, but no independent evaluation period; model superiority remains qualified.',
 'R1-04':'Target is supplier speed, not independent physical ground truth.',
 'R3-12':'No independent colocated speed sensor measurement.',
 'R1-03':'Original 97.30% unavailable denominator; remove and use verified coverage definitions.',
 'R1-10':'Table 7 vs Eq12 denominator/aggregation consistency must be corrected from registered G1 evidence.'
}.items():m.loc[m.comment_id==i,'final_limitation']=s
assert len(m)==31 and m.comment_id.is_unique
save('FINAL_04_Reviewer_Evidence_Matrix.csv',m)

# S10: concrete revision mapping and source index, no manuscript edits.
cons=read(G1/'G1_Manuscript_Consistency.csv')
cons['final_status']='REVISE_WITH_ACCEPTED_EVIDENCE'
cons['final_source_relative']=cons.evidence_file.astype(str).str.replace(r'^.*?(?=04_EXPERIMENTS\\|04_EXPERIMENTS/|02_DATA\\|02_DATA/)', '',regex=True).str.replace('\\','/',regex=False)
cons['evidence_file']=cons['final_source_relative']
extra=[
 {'manuscript_section':'Abstract/Results','equation':'','figure_table':'main comparison','original_claim':'XGBoost wins all horizons','new_evidence':'G1 3-day/7-day Holm: XGB–SeasonalHA non-significant; G2 four key tests non-significant','difference':'QUALIFY','recommended_revision':'State descriptive ranking with intervals and uncertainty','reviewer_mapping':'R1-01;R1-09;R2-04','evidence_file':'04_EXPERIMENTS/FINAL_TARGETED_CHECKS/Final_Statistical_Inference.csv','final_status':'REVISE_WITH_ACCEPTED_EVIDENCE','final_source_relative':'04_EXPERIMENTS/FINAL_TARGETED_CHECKS/Final_Statistical_Inference.csv'},
 {'manuscript_section':'Methods/Results','equation':'Ridge solver','figure_table':'Ridge table','original_claim':'Cholesky Ridge results final','new_evidence':'93 SVD diagnostic fits; 18/90 3-decimal MAE changes; 0/90 XGB-Ridge fold winner flips','difference':'NUMERICAL_CORRECTION','recommended_revision':'Use SVD corrected Ridge overlay and cite original frozen source','reviewer_mapping':'R1-06;R6-04','evidence_file':'04_EXPERIMENTS/FINAL_TARGETED_CHECKS/Ridge_Corrected_Aggregates.csv','final_status':'REVISE_WITH_ACCEPTED_EVIDENCE','final_source_relative':'04_EXPERIMENTS/FINAL_TARGETED_CHECKS/Ridge_Corrected_Aggregates.csv'},
 {'manuscript_section':'Study area','equation':'','figure_table':'map/length','original_claim':'130 km precise corridor and uniform 2.6 km spacing','new_evidence':'historical length unverified; current OSM undirected path sum 156.274 km, not mainline length','difference':'LIMITATION','recommended_revision':'Remove exact historical length claim; label current GIS illustrative and review flagged nodes','reviewer_mapping':'R1-05;R1-10;R3-11','evidence_file':'04_EXPERIMENTS/FINAL_TARGETED_CHECKS/GIS_Corridor_Length_Reconciliation.csv','final_status':'REVISE_WITH_ACCEPTED_EVIDENCE','final_source_relative':'04_EXPERIMENTS/FINAL_TARGETED_CHECKS/GIS_Corridor_Length_Reconciliation.csv'},
 {'manuscript_section':'Methods/Discussion','equation':'','figure_table':'E08','original_claim':'Independent validation obtained','new_evidence':'No independent local archive; E08 not executed','difference':'PENDING','recommended_revision':'Explicitly disclose historical test exposure and no independent/cross-corridor/ground-truth validation','reviewer_mapping':'R1-08;R2-01;R2-04;R3-12','evidence_file':'04_EXPERIMENTS/FINAL_TARGETED_CHECKS/E08_Data_Feasibility_and_Decision.csv','final_status':'LIMITATION_TO_DISCLOSE','final_source_relative':'04_EXPERIMENTS/FINAL_TARGETED_CHECKS/E08_Data_Feasibility_and_Decision.csv'}
]
g2wb=load_workbook(G2/'G2_05_Manuscript_Consistency_Matrix.xlsx',read_only=True,data_only=True)
g2rows=list(g2wb['G2 evidence map'].values)
g2head=list(g2rows[2]);g2map=pd.DataFrame(g2rows[3:],columns=g2head).fillna('')
g2extra=[]
for x in g2map.itertuples(index=False):
 source='04_EXPERIMENTS/G2_E04_E07_ACCEPTANCE/'+str(x.source_result_file)
 if not (R/source).exists():source='04_EXPERIMENTS/E07_SPATIAL_OPERATIONAL/'+str(x.source_result_file)
 g2extra.append({'manuscript_section':x.manuscript_section,'equation':x.equation,'figure_table':x.figure_table,'original_claim':x.original_value,'new_evidence':str(x.corrected_or_new_value)+' | '+str(x.new_evidence),'difference':'G2_NEW_EVIDENCE','recommended_revision':x.pending_revision,'reviewer_mapping':x.reviewer_mapping,'evidence_file':source,'final_status':'REVISE_WITH_ACCEPTED_EVIDENCE','final_source_relative':source})
cons=pd.concat([cons,pd.DataFrame(g2extra),pd.DataFrame(extra)],ignore_index=True)
save('FINAL_05_Manuscript_Consistency_Matrix.csv',cons)
plan=pd.DataFrame([
 {'item':'Coverage/return funnel','format':'Figure+Table','source':'G1 E01 coverage and attrition CSV','claim':'separate slot return, eligible observation, daily measures','status':'READY_FOR_DRAFT'},
 {'item':'Target/state distribution','format':'Figure','source':'G1 E01 and E02 state stratification','claim':'provider speed target; congestion coverage','status':'READY_FOR_DRAFT'},
 {'item':'Model performance H1/H3/H6','format':'Table','source':'G1 accepted metrics; Ridge SVD overlay','claim':'within-horizon descriptive comparison','status':'READY_FOR_DRAFT'},
 {'item':'Inference forest plot','format':'Figure','source':'Final_Statistical_Inference.csv; 7-day sensitivity','claim':'show effect/CI/Holm; do not imply universal ranking','status':'READY_FOR_DRAFT'},
 {'item':'E04–E06 sensitivity','format':'Tables','source':'G2 accepted integrated results and matched contrasts','claim':'only applicable executed conditions','status':'READY_FOR_DRAFT'},
 {'item':'GIS corridor','format':'Figure','source':'GIS local GPKG and CSV','claim':'current OSM illustrative only; historical 130 km unverified','status':'AUTHOR_MANUAL_REVIEW_NEEDED'},
 {'item':'Inference timing','format':'Table','source':'Final_Computational_Efficiency_Table.csv','claim':'different timing boundaries explicitly labeled','status':'READY_WITH_CAVEAT'},
 {'item':'References','format':'Reference list','source':'Final_Reviewer_Recommended_Literature.csv; Final_Required_Method_References.csv','claim':'include only relevant verified metadata, do not cite wrong DOIs','status':'FULLTEXT_CHECK_PENDING'}
])
save('FINAL_06_Figure_Table_and_Reference_Plan.csv',plan)
index=[]
for group,files in [('statistics',[T/'Final_Statistical_Inference.csv',T/'Final_Statistical_Sensitivity_3d_7d.csv',T/'Final_Scientific_Claims_Registry.csv']),('ridge',[T/'Ridge_Corrected_Aggregates.csv',T/'Ridge_Corrected_Experiment_Metrics.csv',T/'Ridge_Stability_Conclusion_CN.md']),('GIS',[T/'GIS_Corridor_Length_Reconciliation.csv',T/'GIS_Final_Evidence_Report_CN.md']),('efficiency',[T/'Final_Computational_Efficiency_Table.csv']),('review',[T/'FINAL_04_Reviewer_Evidence_Matrix.csv',T/'FINAL_05_Manuscript_Consistency_Matrix.csv']),('literature',[T/'Final_Reviewer_Recommended_Literature.csv',T/'Final_Required_Method_References.csv'])]:
 for p in files:index.append({'group':group,'path':str(p.relative_to(R)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'role':'LOCAL_EVIDENCE_INDEX_ONLY'})
save('Final_Evidence_Library_Index.csv',index)

payload={'workbooks':[
 {'file':'FINAL_01_Statistical_and_Scientific_Claims.xlsx','sheets':[tab('Claims','S01 accepted comparisons',claims),tab('Primary inference','G1 3d + G2 3d accepted aggregate CSV',stats),tab('3d and 7d','G1 independent Holm recomputation; G2 7d descriptive',sens)]},
 {'file':'FINAL_03_E08_External_Validation_Decision.xlsx','sheets':[tab('E08 decision','local asset inventory and official DCRNN README',e08)]},
 {'file':'FINAL_04_Reviewer_Evidence_Matrix.xlsx','sheets':[tab('31 comments','G2 accepted reviewer matrix with S01–S08 closure',m)]},
 {'file':'FINAL_05_Manuscript_Consistency_Matrix.xlsx','sheets':[tab('Revision mapping','G1 accepted mapping plus final corrections',cons)]},
 {'file':'FINAL_06_Figure_Table_and_Reference_Plan.xlsx','sheets':[tab('Figures and tables','accepted evidence source index',plan),tab('Literature','publisher and official source metadata',litdf),tab('Method refs','original method papers',pd.DataFrame(methods))]},
 {'file':'Final_Reviewer_Recommended_Literature.xlsx','dir':'target','sheets':[tab('Reviewer literature','publisher and official source metadata',litdf)]},
 {'file':'E08_Data_Feasibility_and_Decision.xlsx','dir':'target','sheets':[tab('E08 feasibility','local inventory and official DCRNN README',e08)]}
]}
(R/'03_CODE/FINAL_EVIDENCE_CLOSURE/workbook_payload.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print('PREPARED',len(m),len(cons),len(litdf),len(index))
