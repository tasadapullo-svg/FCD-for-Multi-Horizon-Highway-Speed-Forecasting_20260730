# APIN-D-26-12623 Prompt05 最终非训练收尾报告

## 继承范围

沿用 Prompt04 ZIP `E:\20261125_论文修改_Applied Intelligence\APIN_FINAL_EVIDENCE_FREEZE_20261126.zip`，SHA-256 `77a1c43bffe6c786cc7a61304d6735cc348491dfdbdb36a3784e10d39d5a179b` 已核。G0/G1/G2 为 CONDITIONAL_PASS、SOURCE_GATE 为 PASS_NEW_IMPLEMENTATION。原历史180次、G2 651唯一运行（489拟合、162确定性、414复用事件）及Prompt04的93次Ridge SVD诊断均只读继承；本阶段新增拟合0、E08训练0、Ridge重拟合0。

## JB目标资产与E08

在E输出根的两套工程、四个顶层ZIP成员，以及C:\Users\DELL的Desktop、Downloads、Documents、OneDrive和WPS资料目录按指定准确文件名与索引名搜索，未找到 `jb_fcd_panel_hourly_v1.csv`、P0归档、道路分组冻结包、JB-SP登记表或指定审计报告；旧D盘历史目录不可用。按Prompt05限定范围停止扩搜。实际目标文件路径、哈希、行列数、有效观测、缺失/插补、供应商、原采样频率、数据许可和先前使用情况均未核实。历史451,008行只是348×1,296完整网格候选规模，不是实测观测数。无法选择连续道路走廊，也无法计算H1/H3/H6资格及训练/验证/测试支持。E08状态 `TARGET_ASSET_NOT_FOUND`；不执行24–72候选运行，也不转用其他JB或公开数据。

## Ridge关联结果

Prompt04既有90个含测试指标的SVD Ridge Run ID逐行映射到旧Cholesky数值，另有3个仅验证候选。覆盖固定基准、1/4与3/4 H1、严格6/6、返回记录网格、非因果缩放及有限α选择。现有指标可汇总原生测试MAE/RMSE/Bias及fold-macro/按样本数加权MAE；最终SVD逐样本预测未保存，不能重新计算特殊共同参考目标的配对结果。旧Cholesky逐样本分析不能与SVD聚合混称。G1历史结果和G2四项不含Ridge的关键检验不变。详见 `Final_Ridge_Result_Replacement_Map.csv` 与 `Ridge_Closure_Statement.md`。

## 统一纯推理边界

Fold1 H1/H6、同一1024测试样本、CPU、20预热/100计时，参考表/模型及输入在计时前准备。H1平均批次：HA 0.0007 ms (P95 0.0009 ms)，SeasonalHA 0.1267 ms (P95 0.1561 ms)，Persistence 0.0013 ms (P95 0.0016 ms)，XGBoost单seed 2.8709 ms (P95 3.2614 ms)、三seed 8.6681 ms (P95 9.7725 ms)，GRU单seed 26.5099 ms (P95 32.1116 ms)、三seed 80.7078 ms (P95 89.2375 ms)。H6相应明细及准备/加载时间见CSV。最终SVD Ridge权重未保存，故不为计时重新拟合；其旧求解器计时不列为最终比较。批处理计时不代表线上API延迟或经济价值。

## GIS、许可与文献

51节点当前OSM诊断及里程口径只继承；15个候选节点的坐标、way、偏差和具体原因写入本机复核表，均仍为 `AUTHOR_GIS_REVIEW_REQUIRED`。原130km历史里程 `HISTORICAL_CORRIDOR_LENGTH_NOT_VERIFIED`，不把137.395km直线段和、156.274km当前无方向路径和或112.264km去重图边当作历史主线。正文应删去无依据的精确长度/平均间距。详细节点坐标不进入交付ZIP。

Pan Borneo及JB历史合同、跨项目研究许可与数据/预测/聚合/代码/权重公开权限均为 `AUTHOR_CONFIRMATION_REQUIRED`；未上传商业数据。沿用Prompt04文献核查；Künsch原方法全文与DCRNN具体架构描述仍须在写作前对照原文，错误的R2-03两个DOI继续排除。

## 31条审稿意见与写作闸门

31条原文均保留并同步实际证据。严格6/6、替代插补、有限调参、静态GRU、GATE-FCD消融、历史窗口与日历/LOFO均承认已完成；相邻节点模型未做，JB E08未做，LOFO不能消除历史测试暴露，同址真实速度仍无证据。已有内部证据足以开始有明确限制的图表、正文和回复草稿；尚不具备声称外部验证完成或直接最终投稿的条件。按作者指示，交通数据与模型实验在此停止。
