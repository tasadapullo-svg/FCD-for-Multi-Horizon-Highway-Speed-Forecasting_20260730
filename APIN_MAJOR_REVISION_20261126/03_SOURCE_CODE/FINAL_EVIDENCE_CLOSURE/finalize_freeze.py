"""Produce final Prompt04 reports, frozen manifest and controlled evidence ZIP."""
from pathlib import Path
import json,csv,hashlib,zipfile,datetime,platform
import pandas as pd
R=Path(__file__).resolve().parents[2];O=R.parent;T=R/'04_EXPERIMENTS/FINAL_TARGETED_CHECKS';F=R/'05_FINAL_RESULTS/FINAL_EVIDENCE_CLOSURE';L=R/'05_FINAL_RESULTS/FINAL_EVIDENCE_LIBRARY';G1=R/'04_EXPERIMENTS/G1_E01_E03_ACCEPTANCE';G2=R/'04_EXPERIMENTS/G2_E04_E07_ACCEPTANCE'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def rel(p):return str(p.relative_to(R)).replace('\\','/')
st=json.loads((T/'Final_Statistics_Receipt.json').read_text(encoding='utf-8'))
ri=json.loads((T/'Ridge_Impact_Summary.json').read_text(encoding='utf-8'))
gi=json.loads((T/'GIS_Final_Summary.json').read_text(encoding='utf-8'))
b=pd.read_csv(T/'Simple_Baseline_Inference_Benchmark.csv')
m=pd.read_csv(T/'FINAL_04_Reviewer_Evidence_Matrix.csv')
bench='; '.join(f"{r.model} H{r.horizon} {r.mean_batch_seconds*1000:.3f} ms (P95 {r.p95_batch_seconds*1000:.3f} ms)" for r in b.itertuples())
(F/'FINAL_02_Targeted_Closure_Report_CN.md').write_text(f'''# APIN-D-26-12623 定向证据关闭报告

工程：`{R}`；输出根：`{O}`。本阶段沿用 G0/G1/G2 验收，不重跑原 180 次或 G2 651 次正式运行；新增 93 次 Ridge SVD 诊断拟合、0 次空间邻居拟合、0 次 E08 拟合。原 G2 ZIP 保持冻结。

## S01 统计

以已有 G1 3 日块正式结果及 7 日块原始 p 值，独立重算 7 日 Holm；未重做 bootstrap。3 日正式比较显著 7 项，7 日敏感性也为 7 项且原 7 项均保留。XGBoost–SeasonalHA 在三个时距均不显著。G2 四项预设关键对照经 Holm 均不显著；严格 H6 原始 p=0.03410，四项 Holm p=0.13639。见 `Final_Statistical_Inference.csv`、`Final_Statistical_Sensitivity_3d_7d.csv`；跨时距 MAE 不直接比较。

## S02 Ridge

原 93 个 Ridge Run ID 中 78 个日志带病态矩阵警告，全部映射成功。预先冻结逐预测容差 1e-4 km/h、MAE 容差 1e-5 km/h，唯一变更 Cholesky→SVD，在相同清单、特征、目标和 α 下完成 93 次诊断拟合（90 个有测试指标、3 个仅验证候选）。测试结果中 89/90 超出逐预测容差，87/90 超出 MAE 容差，18/90 的三位小数 MAE 改变；最大逐样本预测差 0.693176 km/h、最大 MAE 差 0.001462 km/h。三个时距的验证选择均仍为 α=10；90 个 XGBoost–Ridge 匹配 fold 排序方向改变 0。故原 Cholesky 数值不可继续当最终 Ridge 数字，写作采用 SVD 修正覆盖表，历史 G2 包不覆盖。G1 原始检验和 G2 四项关键检验不含该 Ridge 修正对象。

## S03 GIS

只复用 2026-11-25 本地 OSM 快照。51 节点全部匹配，中位横向偏差 3.591 m、最大 86.403 m；15 个节点需要人工复查。当前无方向 OSM 图上 50 对相邻编号可连通，WGS84 直线段和 137.395 km、当前路图逐对最短路径和 156.274 km，其中重复图边累计 44.010 km。因此 156.274 km 不等于研究期主线实际里程；原稿约 130 km 缺乏可追溯历史中心线测量，状态 `HISTORICAL_CORRIDOR_LENGTH_NOT_VERIFIED`。当前图不能证明历史道路方向、上下游和 API 到达时间。含原节点坐标的 GPKG 仅本机使用，不进 ZIP。使用 OSM 时标注 © OpenStreetMap contributors / ODbL。

## S04 效率

CPU Fold1 H1/H6，1024 个共同样本、20 次预热、100 次实测，简单基准平均批次时间：{bench}。HA/SeasonalHA 计入内存训练参考表 groupby 与查表，Persistence 使用已装载数组；G2 学习模型原计时只含预处理后模型预测，两者边界不同，不能作严格速度名次，也不能推算经济效益。明细见 `Final_Computational_Efficiency_Table.csv`。

## S05–S08 决策

空间邻居模型历史方向拓扑、因果邻居特征和到达时间未获核验，故为 `CLOSED_WITH_LIMITATION`、0 次拟合；静态 GRU 不冒充邻居时空模型。E08 为 `NOT_FEASIBLE_WITH_CURRENT_DATA`：本机无新的独立 Pan Borneo 时段或其他走廊商业 FCD；METR-LA 仅是一个待核数据许可的固定检测器候选，不能替代同址真实速度。未下载外部交通数据。

商业 FCD 合同/订阅条款未见，公开原始数据、派生矩阵、逐样本预测、权重、聚合发表和代码权限逐项标 `AUTHOR_CONFIRMATION_REQUIRED`。文献核查确认 R2-03 的两个指定 DOI 分别是图像特征选择和接触角测量，均不能支持评论中的复杂度论证。其他审稿建议论文按主题相关性筛选；未读全文者未声称全文核验。

## 遗留

31 条原意见均已登记，证据形成不等于审稿问题全部解决。独立评价时期、跨走廊泛化、同址物理真值、历史主线里程、商业许可及论文正文图表/回复均仍待实际处理。本阶段内部定向实验至此停止。
''',encoding='utf-8')
e08='NOT_FEASIBLE_WITH_CURRENT_DATA'
(F/'FINAL_07_Experiment_Freeze_Report_CN.md').write_text(f'''# APIN-D-26-12623 全部内部实验冻结报告

**冻结判定：INTERNAL_EXPERIMENTS_FROZEN_WITH_LIMITATIONS。可以开始受证据约束的论文图表、正文及回复草稿；尚不具备无条件最终投稿状态。**

## 阶段与实际规模

G0、G1、G2 均为 `CONDITIONAL_PASS`；SOURCE_GATE 实际 `PASS_NEW_IMPLEMENTATION`。G0 的 180 次历史预测只继承；G2 共 651 唯一 Run ID（489 模型拟合、162 确定性基准、642 含测试结果、9 仅验证候选，失败 0，414 次复用事件）。G2 E04–E06 适用核心执行完成；E07 当前 GIS、日历、效率证据已完成。本阶段 93 次 Ridge SVD **诊断拟合**用于数值修正，另无空间模型或 E08 模型拟合。原训练源码未恢复，G2 为独立新实现；原 G0/G1 历史预测与 G2 正式产物未覆盖。

## 允许采用的结果

G1 3 日块 Holm 显著 7 项，7 日敏感性保留全部 7 项；XGBoost–SeasonalHA 各时距不显著。G2 四项预设日均对照 Holm 后均不显著，不能以严格 H6 单项原始 p<0.05 宣称家族显著。描述性模型排序只限该研究走廊、供应商报告速度、已观察评价期及已登记共同样本。Ridge 数值采用本阶段 SVD 修正覆盖表；90 个匹配 fold 的 XGBoost–Ridge 优胜方向未改变。4/4 完整度条件因验证支持不足 `NOT_ESTIMABLE`，不补造结果。

## 已解决与仍受限

已完成原始来源审计、时间目标与共同样本核验、G1 日块推断、E04–E06 适用敏感性/公平性、Ridge 数值定向修正和简单基准效率补测。当前 OSM 51 节点和 50 个连接段只证明当前无方向图可连通；原约130 km 历史主线里程未获证实，15 节点须人工复核，空间邻居模型未训练。原 API 到达延迟、商业 FCD 真实缺失机制及独立地面真值未获证明。原测试集历史暴露仍需明示；本机无独立新时段或其他走廊数据。E08 决定 `{e08}`，公开 METR-LA 仅待核候选，未执行。

## 许可与投稿闸门

本轮未见作者适用的商业订阅合同；各类公开发布权限仍为 `AUTHOR_CONFIRMATION_REQUIRED`。最终 ZIP 不含原始商业数据、逐样本预测、派生矩阵、模型权重、坐标 GPKG 或受限文献全文。论文图表与正文须使用本冻结证据库、区分显著与描述性、明确旧测试暴露和外部验证缺口。正式投稿前需要作者核定许可、完成 GIS 人工复查/历史里程措辞、核对必要文献全文与全部图表数字，完成正文与 31 条审稿回复，并再次做稿件一致性审查。本报告不代表审稿人接受或论文已修改。

证据索引：`05_FINAL_RESULTS/FINAL_EVIDENCE_LIBRARY/Final_Evidence_Library_Index.csv`；具体结果见八份核心交付及定向 CSV。
''',encoding='utf-8')
# Library index is an index, not a copy of restricted sources.
index=pd.read_csv(T/'Final_Evidence_Library_Index.csv')
source_paths=[
 R/'01_ORIGINAL_BASELINE/PRIOR_G0_AUDIT/05_REPORTS/G0_EXECUTIVE_VERDICT.md',
 G1/'G1_06_Acceptance_Report_CN.md',
 G2/'G2_07_Acceptance_Report_CN.md',
 G2/'G2_02_Experiment_Run_Registry.csv',
 G2/'G2_Key_Comparisons_Actual.csv',
 R/'04_EXPERIMENTS/SOURCE_GATE/source_gate_verdict.json',
 R/'00_PROJECT_CONTROL/G1_Analysis_Protocol.yaml',
 R/'00_PROJECT_CONTROL/G2_Training_Protocol.yaml'
]
records=index.to_dict('records')
for p in source_paths:
 if p.exists():records.append({'group':'inherited_frozen','path':rel(p),'sha256':sha(p),'role':'LOCAL_EVIDENCE_INDEX_ONLY'})
pd.DataFrame(records).drop_duplicates('path').to_csv(L/'Final_Evidence_Library_Index.csv',index=False,encoding='utf-8-sig')
core=[F/f'FINAL_{i:02d}_{name}' for i,name in [(1,'Statistical_and_Scientific_Claims.xlsx'),(2,'Targeted_Closure_Report_CN.md'),(3,'E08_External_Validation_Decision.xlsx'),(4,'Reviewer_Evidence_Matrix.xlsx'),(5,'Manuscript_Consistency_Matrix.xlsx'),(6,'Figure_Table_and_Reference_Plan.xlsx'),(7,'Experiment_Freeze_Report_CN.md')]]
assert all(p.exists() and p.stat().st_size>100 for p in core)
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
manifest={'manuscript_id':'APIN-D-26-12623','completed_at_Asia_Shanghai':now,'output_root':str(O),'project_root':str(R),'final_state':'INTERNAL_EXPERIMENTS_FROZEN_WITH_LIMITATIONS','inherited_status':{'G0':'CONDITIONAL_PASS','G1':'CONDITIONAL_PASS','G2':'CONDITIONAL_PASS','SOURCE_GATE':'PASS_NEW_IMPLEMENTATION'},'original_source_recovered':False,'G2_unique_runs':651,'G2_model_fits':489,'G2_deterministic_executions':162,'G2_test_runs':642,'G2_validation_only_runs':9,'G2_failed_runs':0,'new_model_fits':{'Ridge_SVD_diagnostic':93,'spatial_neighbor':0,'E08_external':0},'statistics':st,'ridge':ri,'GIS':gi,'E08_status':e08,'commercial_data_public_rights':'AUTHOR_CONFIRMATION_REQUIRED','inputs':{rel(p):sha(p) for p in source_paths if p.exists()},'core_outputs_01_to_07':{rel(p):sha(p) for p in core},'G2_frozen_zip':{'path':str(O/'APIN_G2_E04_E07_Results_20261126.zip'),'sha256':sha(O/'APIN_G2_E04_E07_Results_20261126.zip')},'limitations':['historical_test_exposure','no_independent_period_or_cross_corridor_validation','no_independent_colocated_speed_ground_truth','historical_corridor_length_unverified','historical_directional_topology_unverified','commercial_data_rights_unverified']}
out8=F/'FINAL_08_Execution_Manifest.json';out8.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
allow=core+[out8,L/'Final_Evidence_Library_Index.csv']
allow += [T/n for n in ['Final_Statistical_Inference.csv','Final_Statistical_Sensitivity_3d_7d.csv','Final_Scientific_Claims_Registry.csv','Ridge_Corrected_Aggregates.csv','Ridge_Corrected_Experiment_Metrics.csv','Ridge_Stability_Conclusion_CN.md','GIS_Corridor_Length_Reconciliation.csv','GIS_Final_Evidence_Report_CN.md','GIS_Final_Summary.json','Simple_Baseline_Inference_Benchmark.csv','Final_Computational_Efficiency_Table.csv','Efficiency_Comparison_Notes.md','Spatial_Eligibility_Evidence.csv','Spatial_Model_Final_Decision.md','E08_Data_Feasibility_and_Decision.xlsx','E08_Minimum_External_Validation_Plan.md','Data_Licensing_and_Distribution_Matrix.csv','Reproducibility_Evidence_Statement.md','Author_Permission_Decisions.md','Final_Reviewer_Recommended_Literature.xlsx','Final_Required_Method_References.csv','Literature_Missing_FullText_List.csv','FINAL_04_Reviewer_Evidence_Matrix.csv','FINAL_05_Manuscript_Consistency_Matrix.csv','FINAL_06_Figure_Table_and_Reference_Plan.csv']]
allow += list((R/'03_CODE/FINAL_EVIDENCE_CLOSURE').glob('*.py'))
allow += [R/'00_PROJECT_CONTROL/FINAL_Closure_Protocol.json']
allow=list(dict.fromkeys(allow));assert all(p.exists() for p in allow)
for p in allow:
 s=rel(p).lower()
 assert not any(x in s for x in ['raw_source','predictions_test','model.joblib','weights.pt','.gpkg','node_matching','node_coordinates'])
hashlist=F/'FINAL_Delivery_SHA256.csv'
with hashlist.open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['path','size_bytes','sha256']);w.writerows((rel(p),p.stat().st_size,sha(p)) for p in allow)
allow.append(hashlist)
z=O/('APIN_FINAL_EVIDENCE_FREEZE_'+datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime('%Y%m%d')+'.zip')
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for p in allow:f.write(p,rel(p))
with zipfile.ZipFile(z) as f:
 bad=f.testzip();names=f.namelist()
 assert bad is None and len(names)==len(allow)
 for p in allow:
  with f.open(rel(p)) as stream:
   h=hashlib.sha256()
   for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
   assert h.hexdigest()==sha(p)
print(json.dumps({'zip':str(z),'zip_sha256':sha(z),'entries':len(allow),'crc':'PASS','core_files':len(core)+1,'review_comments':len(m),'status':manifest['final_state']},ensure_ascii=False))
