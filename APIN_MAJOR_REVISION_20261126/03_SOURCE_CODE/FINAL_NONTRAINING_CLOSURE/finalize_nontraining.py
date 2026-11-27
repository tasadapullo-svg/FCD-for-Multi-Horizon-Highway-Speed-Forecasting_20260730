"""Freeze Prompt05 nontraining closure, with scoped negative asset finding."""
from pathlib import Path
import json,hashlib,csv,zipfile,datetime
import pandas as pd
R=Path(__file__).resolve().parents[2];O=R.parent;T=R/'04_EXPERIMENTS/FINAL_NONTRAINING_CLOSURE';F=R/'05_FINAL_RESULTS/FINAL_NONTRAINING_CLOSURE';P4=R/'04_EXPERIMENTS/FINAL_TARGETED_CHECKS'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def rel(p):return str(p.relative_to(R)).replace('\\','/')
prior=O/'APIN_FINAL_EVIDENCE_FREEZE_20261126.zip'
assert sha(prior)=='77a1c43bffe6c786cc7a61304d6735cc348491dfdbdb36a3784e10d39d5a179b'
b=pd.read_csv(T/'Final_Unified_Inference_Benchmark.csv')
def latency(model,h,execution):
 r=b[(b.model==model)&(b.horizon==h)&(b.execution==execution)].iloc[0]
 return f"{r.mean_batch_seconds*1000:.4f} ms (P95 {r.p95_batch_seconds*1000:.4f} ms)"
(F/'E08_03_Minimum_Experiment_and_Decision_CN.md').write_text('''# E08 JB最小实验与决定

**最终状态：TARGET_ASSET_NOT_FOUND；本轮不建议执行E08；训练运行0。**

指定历史资产 `jb_fcd_panel_hourly_v1.csv` 未在限定范围内定位，`05_P0 正式数据资产.zip`、`2026-09-21道路分组冻结资料包`、`JB-SP.xlsx` 和指定审计报告亦未见。实际文件路径、大小、SHA-256、行列数、供应商、真实有效观测数、插补数、采样频率、道路组、许可、先前使用情况均未知。451,008=348×1,296只是历史登记的网格算式，不能当已核实的返回或有效速度。没有选择道路走廊、时间划分或样本支持，没有虚构预测结果。

候选科学价值原本仅可能是相对于Pan Borneo的跨走廊回顾性外部案例，不能证明同走廊新时期盲测或同址物理真实速度。当前连该外部案例的基本数据条件也未证实，因此按作者指示停止增加交通数据和模型实验。24–72个运行单元是未冻结的上限，本阶段实际0。R1-08、R2-01、R2-04及R3-12只能在正文和回复中如实陈述限制。

若作者以后改变决定，最小材料是唯一目标 CSV 或包含它的P0归档、直接采集/处理日志、JB-SP登记表及跨项目研究许可；先核真实观测与因果目标，再考虑实验。现阶段没有需要自动下载的材料。
''',encoding='utf-8')
report=f'''# APIN-D-26-12623 Prompt05 最终非训练收尾报告

## 继承范围

沿用 Prompt04 ZIP `{prior}`，SHA-256 `{sha(prior)}` 已核。G0/G1/G2 为 CONDITIONAL_PASS、SOURCE_GATE 为 PASS_NEW_IMPLEMENTATION。原历史180次、G2 651唯一运行（489拟合、162确定性、414复用事件）及Prompt04的93次Ridge SVD诊断均只读继承；本阶段新增拟合0、E08训练0、Ridge重拟合0。

## JB目标资产与E08

在E输出根的两套工程、四个顶层ZIP成员，以及C:\\Users\\DELL的Desktop、Downloads、Documents、OneDrive和WPS资料目录按指定准确文件名与索引名搜索，未找到 `jb_fcd_panel_hourly_v1.csv`、P0归档、道路分组冻结包、JB-SP登记表或指定审计报告；旧D盘历史目录不可用。按Prompt05限定范围停止扩搜。实际目标文件路径、哈希、行列数、有效观测、缺失/插补、供应商、原采样频率、数据许可和先前使用情况均未核实。历史451,008行只是348×1,296完整网格候选规模，不是实测观测数。无法选择连续道路走廊，也无法计算H1/H3/H6资格及训练/验证/测试支持。E08状态 `TARGET_ASSET_NOT_FOUND`；不执行24–72候选运行，也不转用其他JB或公开数据。

## Ridge关联结果

Prompt04既有90个含测试指标的SVD Ridge Run ID逐行映射到旧Cholesky数值，另有3个仅验证候选。覆盖固定基准、1/4与3/4 H1、严格6/6、返回记录网格、非因果缩放及有限α选择。现有指标可汇总原生测试MAE/RMSE/Bias及fold-macro/按样本数加权MAE；最终SVD逐样本预测未保存，不能重新计算特殊共同参考目标的配对结果。旧Cholesky逐样本分析不能与SVD聚合混称。G1历史结果和G2四项不含Ridge的关键检验不变。详见 `Final_Ridge_Result_Replacement_Map.csv` 与 `Ridge_Closure_Statement.md`。

## 统一纯推理边界

Fold1 H1/H6、同一1024测试样本、CPU、20预热/100计时，参考表/模型及输入在计时前准备。H1平均批次：HA {latency('HA',1,'single_deterministic')}，SeasonalHA {latency('SeasonalHA',1,'single_deterministic')}，Persistence {latency('Persistence',1,'single_deterministic')}，XGBoost单seed {latency('XGBoost',1,'single_seed')}、三seed {latency('XGBoost',1,'three_seed_ensemble')}，GRU单seed {latency('GRU',1,'single_seed')}、三seed {latency('GRU',1,'three_seed_ensemble')}。H6相应明细及准备/加载时间见CSV。最终SVD Ridge权重未保存，故不为计时重新拟合；其旧求解器计时不列为最终比较。批处理计时不代表线上API延迟或经济价值。

## GIS、许可与文献

51节点当前OSM诊断及里程口径只继承；15个候选节点的坐标、way、偏差和具体原因写入本机复核表，均仍为 `AUTHOR_GIS_REVIEW_REQUIRED`。原130km历史里程 `HISTORICAL_CORRIDOR_LENGTH_NOT_VERIFIED`，不把137.395km直线段和、156.274km当前无方向路径和或112.264km去重图边当作历史主线。正文应删去无依据的精确长度/平均间距。详细节点坐标不进入交付ZIP。

Pan Borneo及JB历史合同、跨项目研究许可与数据/预测/聚合/代码/权重公开权限均为 `AUTHOR_CONFIRMATION_REQUIRED`；未上传商业数据。沿用Prompt04文献核查；Künsch原方法全文与DCRNN具体架构描述仍须在写作前对照原文，错误的R2-03两个DOI继续排除。

## 31条审稿意见与写作闸门

31条原文均保留并同步实际证据。严格6/6、替代插补、有限调参、静态GRU、GATE-FCD消融、历史窗口与日历/LOFO均承认已完成；相邻节点模型未做，JB E08未做，LOFO不能消除历史测试暴露，同址真实速度仍无证据。已有内部证据足以开始有明确限制的图表、正文和回复草稿；尚不具备声称外部验证完成或直接最终投稿的条件。按作者指示，交通数据与模型实验在此停止。
'''
(F/'FINAL_06_Nontraining_Closure_Report_CN.md').write_text(report,encoding='utf-8')
core=[
 F/'E08_01_JB_Data_Asset_and_Compatibility.xlsx',
 F/'E08_02_JB_Corridor_and_Sample_Feasibility.xlsx',
 F/'E08_03_Minimum_Experiment_and_Decision_CN.md',
 F/'FINAL_04_Nontraining_Closure_Results.xlsx',
 F/'FINAL_05_Reviewer_and_Manuscript_Consistency.xlsx',
 F/'FINAL_06_Nontraining_Closure_Report_CN.md'
]
assert all(p.exists() and p.stat().st_size>100 for p in core)
inputs=[prior,P4/'Ridge_Corrected_Experiment_Metrics.csv',P4/'Ridge_Corrected_Aggregates.csv',P4/'FINAL_04_Reviewer_Evidence_Matrix.csv',P4/'GIS_Final_Node_Matching.csv',T/'Final_Unified_Inference_Benchmark.csv']
manifest={'manuscript_id':'APIN-D-26-12623','completed_at_Asia_Shanghai':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'output_root':str(O),'project_root':str(R),'target_asset':'jb_fcd_panel_hourly_v1.csv','target_status':'TARGET_ASSET_NOT_FOUND','target_actual_path':None,'target_sha256':None,'target_rows_verified':None,'true_observation_count':None,'imputed_count':None,'sampling_frequency':None,'source_provider':None,'selected_corridor':None,'E08_sample_support':None,'data_license':'AUTHOR_CONFIRMATION_REQUIRED','search_scope':'two E projects, four E ZIP members, limited C user folders; old D historical location unavailable','inherited_prompt04_zip_sha256':sha(prior),'new_model_fits':0,'E08_training_runs':0,'ridge_refits':0,'unified_inference_measured_rows':int((b.status=='MEASURED').sum()),'svd_ridge_not_timed_reason':'final SVD weights not saved; no refit authorized','ridge_svd_test_runs_reused':90,'GIS_manual_review_nodes':15,'reviewer_comments':31,'status':'NONTRAINING_CLOSURE_TARGET_ASSET_NOT_FOUND_MANUSCRIPT_DRAFT_READY_WITH_LIMITATIONS','inputs':{str(p):sha(p) for p in inputs},'outputs_01_to_06':{rel(p):sha(p) for p in core},'executed_commands':['bounded rg --files exact filename/index searches in named E and C folders','zipfile member-name inspection of four E root ZIPs','g2_venv python unified_inference.py (read-only inference; no fit)','python build_nontraining_evidence.py','node artifact-tool build_nontraining_workbooks.mjs','python finalize_nontraining.py'],'prohibited_actions_not_done':['no E08 training','no new FCD download','no G0/G1/G2 rerun','no Ridge refit','no GitHub push']}
p7=F/'FINAL_07_Execution_Manifest.json';p7.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
allowed=core+[p7]
allowed += [T/n for n in ['JB01_Target_Asset_Location.csv','JB02_Field_Compatibility.csv','JB03_Data_Coverage_and_Provenance.csv','JB04_Sampling_Frequency_Assessment.csv','JB05_Independence_and_Prior_Exposure.csv','JB06_Leakage_and_Target_Eligibility.csv','JB07_Corridor_Candidate_Registry.csv','JB08_Selected_Corridor_Decision.md','JB09_E08_Sample_Feasibility.csv','JB10_E08_Minimum_Experiment_Matrix.xlsx','JB11_E08_Protocol_Adaptation.md','JB12_E08_Final_Feasibility_Decision_CN.md','JB_E08_Gate_Receipt.csv','Final_Ridge_Result_Replacement_Map.csv','Final_Ridge_Corrected_Associated_Tables.xlsx','Ridge_Closure_Statement.md','Final_Unified_Inference_Benchmark.csv','Final_Computational_Cost_Comparison.xlsx','Computational_Efficiency_Boundary_Notes.md','GIS_Figure1_Ready_Asset_Index.csv','GIS_Final_Manuscript_Decision.md','Final_Author_Permission_Checklist.xlsx','Final_Mandatory_Missing_References.csv','FINAL_Reviewer_Evidence_Matrix_v2.xlsx','FINAL_Reviewer_Evidence_Matrix_v2.csv','FINAL_Manuscript_Consistency_v2.csv']]
allowed += list((R/'03_CODE/FINAL_NONTRAINING_CLOSURE').glob('*.py'))
allowed=list(dict.fromkeys(allowed));assert all(p.exists() for p in allowed)
for p in allowed:
 s=rel(p).lower()
 assert not any(x in s for x in ['gis_author_review_checklist','gis_final_node_matching','node_coordinates','raw_source','predictions_test','weights.pt','model.joblib','.gpkg'])
hashlist=F/'FINAL_NONTRAINING_Delivery_SHA256.csv'
with hashlist.open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['path','size_bytes','sha256']);w.writerows((rel(p),p.stat().st_size,sha(p)) for p in allowed)
allowed.append(hashlist)
zip_path=O/('APIN_E08_JB_FEASIBILITY_AND_FINAL_CLOSURE_'+datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime('%Y%m%d')+'.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in allowed:z.write(p,rel(p))
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None and len(z.namelist())==len(allowed)
 for p in allowed:
  h=hashlib.sha256()
  with z.open(rel(p)) as f:
   for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
  assert h.hexdigest()==sha(p)
print(json.dumps({'zip':str(zip_path),'sha256':sha(zip_path),'entries':len(allowed),'crc':'PASS','core':7,'target':'TARGET_ASSET_NOT_FOUND','E08_runs':0},ensure_ascii=False))
