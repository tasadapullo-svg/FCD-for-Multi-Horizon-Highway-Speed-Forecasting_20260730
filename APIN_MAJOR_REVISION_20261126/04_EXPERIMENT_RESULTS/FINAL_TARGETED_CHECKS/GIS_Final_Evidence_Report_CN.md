# GIS 研究走廊最终定向核验

**状态：CLOSED_WITH_LIMITATION；历史主线里程 `HISTORICAL_CORRIDOR_LENGTH_NOT_VERIFIED`。** 本轮复用 2026-11-25 获取的工程内局部 OSM 快照、51 个原节点坐标及 G2 匹配结果；没有重下载路网，也没有调整原坐标以接近原稿约 130 km。

51 个节点均匹配到当前 OSM 道路；横向偏差中位数 `3.591 m`、最大 `86.403 m`（N007）。5 个节点偏差超过 30 m；3 个节点匹配到 `trunk_link`；两对相邻编号节点的当前无方向路图距离/直线距离超过 2（N015–N016、N037–N038）。按偏差、连接道路与路径筛查合计 **15 个需要人工复查的候选节点**，不把候选自动判为错配。节点附近 50 m 的其他 OSM way 仅记作可能歧义，不声称已确认平行道路。

按给定 51 节点顺序，50 对邻接编号在当前无方向 OSM 图中均可连通。相邻节点 WGS84 直线测地距离总和 **137.395 km**；以最近路段端点锚定后的无方向图最短路径逐对相加为 **156.274 km**。这些路径使用的唯一图边长度 **112.264 km**，重复经过的图边长度 **44.010 km**，一条边最多被五条相邻对路径重复使用。因此 156.274 km 是当前快照与当前锚定算法的路径和，不是已证实的研究主线里程。原稿约 130 km 缺少可追溯的历史端点/中心线测量，亦不能作为精确测量值继续使用。当前快照无法证明 2025-12 至 2026-02 的道路状态、通行方向或真实上下游关系。

输出 `GIS_Final_Node_Matching.csv`（保留原始与匹配坐标、way ID/名称/等级、偏差及审查原因）、`GIS_Final_Inter_Node_Distance.csv`、`GIS_Corridor_Length_Reconciliation.csv`、`GIS_Adjacency_Evidence.csv`，以及供 QGIS 使用的本机 `GIS_Final_Plot_Data_Local_Only.gpkg`（原节点、当前匹配节点、当前 OSM 道路中心线、选定无方向路径四层）。GeoPackage 含受控节点位置，不进入对外交付 ZIP。OSM 许可为 ODbL，署名 OpenStreetMap contributors；资料清单见 `02_DATA/02_EXTERNAL_DATA/E07_GIS/acquisition_manifest.json`。

后续正文应使用不依赖精确里程的研究区域表述，或由作者提供可核查的原研究期间主线、端点和测量依据后再写近似长度。本阶段不制作最终 Fig. 1。
