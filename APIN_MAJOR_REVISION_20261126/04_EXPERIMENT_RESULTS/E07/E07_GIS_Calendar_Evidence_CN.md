# E07 道路与日历资料核查（本地诊断）

道路来源为工程内定向抓取的 OpenStreetMap 当前快照，查询范围和时间、许可记录在 `02_DATA/02_EXTERNAL_DATA/E07_GIS/acquisition_manifest.json`。51 个原节点坐标映射到 OSM 路段，使用 WGS84→UTM 49N 米制投影计算横向偏差和道路图边长。51 个节点均找到路段，横向偏差中位数约 3.59 m、最大约 86.40 m；按既有节点排序的 50 对相邻节点在无方向 OSM 道路图上均连通，所走图路径总和约 156.27 km。另列 OSM 图度数≥3 的近邻交叉口候选。结果是**当前道路图的近似匹配诊断**，端点锚定、道路方向、主要交叉口类别与 2025-12 至 2026-02 历史代表性仍需人工/历史来源核实；不能据此宣称真实上下游拓扑或运行条件已验证。空间邻居模型条件项暂标记 `DEFERRED_SPATIAL_DEPENDENCY`。

日期来源：马来西亚首相署 [2025 官方节假日表](https://www.kabinet.gov.my/storage/2024/11/hka_2025.pdf) 和 [2026 官方节假日表](https://www.kabinet.gov.my/storage/2025/08/HKA-2026.pdf)，另参考 [JAKIM 2026 伊斯兰重要日期表](https://muftiwp.gov.my/images/falak/takwim/tarikh_penting/TARIKH_Penting_Islam_2026.pdf)。Sarawak 适用的 2026-02-17/18 春节假日已在官方表核对；2026-02-19 斋月开始是宗教节期日期，不是 Sarawak 公共假日声明。与 Fold 5/6 的训练、验证和测试时段关联见 `E07_Fold5_Fold6_Calendar_Association.csv`；只报告日期关联，不作节日导致预测误差变化的因果结论。斋月最终官方宣布时点是否早于各预测时点仍未证实。

原自由流基准的 92,147 个共同测试样本为 G1 已验收证据，本轮标记 `REUSE_EXISTING`，未重算。新电脑模型效率另以实际运行的训练/推理时间登记，不能用旧电脑计时或虚构原权重训练耗时。
