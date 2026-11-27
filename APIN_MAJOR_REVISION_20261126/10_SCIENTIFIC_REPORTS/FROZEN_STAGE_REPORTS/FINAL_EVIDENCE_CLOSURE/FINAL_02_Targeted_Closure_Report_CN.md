# APIN-D-26-12623 定向证据关闭报告

工程：`E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改`；输出根：`E:\20261125_论文修改_Applied Intelligence`。本阶段沿用 G0/G1/G2 验收，不重跑原 180 次或 G2 651 次正式运行；新增 93 次 Ridge SVD 诊断拟合、0 次空间邻居拟合、0 次 E08 拟合。原 G2 ZIP 保持冻结。

## S01 统计

以已有 G1 3 日块正式结果及 7 日块原始 p 值，独立重算 7 日 Holm；未重做 bootstrap。3 日正式比较显著 7 项，7 日敏感性也为 7 项且原 7 项均保留。XGBoost–SeasonalHA 在三个时距均不显著。G2 四项预设关键对照经 Holm 均不显著；严格 H6 原始 p=0.03410，四项 Holm p=0.13639。见 `Final_Statistical_Inference.csv`、`Final_Statistical_Sensitivity_3d_7d.csv`；跨时距 MAE 不直接比较。

## S02 Ridge

原 93 个 Ridge Run ID 中 78 个日志带病态矩阵警告，全部映射成功。预先冻结逐预测容差 1e-4 km/h、MAE 容差 1e-5 km/h，唯一变更 Cholesky→SVD，在相同清单、特征、目标和 α 下完成 93 次诊断拟合（90 个有测试指标、3 个仅验证候选）。测试结果中 89/90 超出逐预测容差，87/90 超出 MAE 容差，18/90 的三位小数 MAE 改变；最大逐样本预测差 0.693176 km/h、最大 MAE 差 0.001462 km/h。三个时距的验证选择均仍为 α=10；90 个 XGBoost–Ridge 匹配 fold 排序方向改变 0。故原 Cholesky 数值不可继续当最终 Ridge 数字，写作采用 SVD 修正覆盖表，历史 G2 包不覆盖。G1 原始检验和 G2 四项关键检验不含该 Ridge 修正对象。

## S03 GIS

只复用 2026-11-25 本地 OSM 快照。51 节点全部匹配，中位横向偏差 3.591 m、最大 86.403 m；15 个节点需要人工复查。当前无方向 OSM 图上 50 对相邻编号可连通，WGS84 直线段和 137.395 km、当前路图逐对最短路径和 156.274 km，其中重复图边累计 44.010 km。因此 156.274 km 不等于研究期主线实际里程；原稿约 130 km 缺乏可追溯历史中心线测量，状态 `HISTORICAL_CORRIDOR_LENGTH_NOT_VERIFIED`。当前图不能证明历史道路方向、上下游和 API 到达时间。含原节点坐标的 GPKG 仅本机使用，不进 ZIP。使用 OSM 时标注 © OpenStreetMap contributors / ODbL。

## S04 效率

CPU Fold1 H1/H6，1024 个共同样本、20 次预热、100 次实测，简单基准平均批次时间：HA H1 1.615 ms (P95 1.807 ms); SeasonalHA H1 12.325 ms (P95 13.936 ms); Persistence H1 1.154 ms (P95 1.328 ms); HA H6 1.301 ms (P95 1.389 ms); SeasonalHA H6 11.769 ms (P95 12.913 ms); Persistence H6 1.127 ms (P95 1.346 ms)。HA/SeasonalHA 计入内存训练参考表 groupby 与查表，Persistence 使用已装载数组；G2 学习模型原计时只含预处理后模型预测，两者边界不同，不能作严格速度名次，也不能推算经济效益。明细见 `Final_Computational_Efficiency_Table.csv`。

## S05–S08 决策

空间邻居模型历史方向拓扑、因果邻居特征和到达时间未获核验，故为 `CLOSED_WITH_LIMITATION`、0 次拟合；静态 GRU 不冒充邻居时空模型。E08 为 `NOT_FEASIBLE_WITH_CURRENT_DATA`：本机无新的独立 Pan Borneo 时段或其他走廊商业 FCD；METR-LA 仅是一个待核数据许可的固定检测器候选，不能替代同址真实速度。未下载外部交通数据。

商业 FCD 合同/订阅条款未见，公开原始数据、派生矩阵、逐样本预测、权重、聚合发表和代码权限逐项标 `AUTHOR_CONFIRMATION_REQUIRED`。文献核查确认 R2-03 的两个指定 DOI 分别是图像特征选择和接触角测量，均不能支持评论中的复杂度论证。其他审稿建议论文按主题相关性筛选；未读全文者未声称全文核验。

## 遗留

31 条原意见均已登记，证据形成不等于审稿问题全部解决。独立评价时期、跨走廊泛化、同址物理真值、历史主线里程、商业许可及论文正文图表/回复均仍待实际处理。本阶段内部定向实验至此停止。
