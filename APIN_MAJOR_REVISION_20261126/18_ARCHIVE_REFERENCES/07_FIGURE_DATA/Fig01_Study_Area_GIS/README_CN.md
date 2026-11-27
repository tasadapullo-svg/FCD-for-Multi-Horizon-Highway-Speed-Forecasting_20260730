# Fig. 1 绘图数据

建议英文图题：Study area and current-OSM spatial audit of FCD observation nodes

本目录的每个CSV为独立面板或其辅助矩阵；对应XLSX列出全部面板。
- Fig01B_Inter_Node_Distance_Diagnostic.csv: 50 行；字段 from_node, to_node, order_from, order_to, straight_geodesic_m, current_osm_undirected_shortest_path_m, road_to_straight_ratio, cumulative_straight_m, cumulative_road_graph_m, connected_current_graph, historical_connection_verified, direction_verified；X/Y及分组按字段名和统计口径选择。
- Fig01_Observation_Nodes.csv: 51 行；字段 node_id_original, node_id_display, node_order, latitude, longitude, road_name, data_source, observation_period, coordinate_crs, match_status；X/Y及分组按字段名和统计口径选择。

样本量、单位、显著性及实现体系应从表内字段和全局来源清单读取；空值不得改作0。Fig.1当前OSM与历史主线不同，Fig.4折线/标准差为描述性，Fig.6点置信区间不是Holm同时区间，Fig.8 Ridge特殊共同目标配对结果未获SVD逐样本修正。E08未运行。原图对应：Fig.1–Fig.6分别对应原稿同号；Fig.7与Fig.8为新增建议。
