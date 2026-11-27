# Fig. 5 绘图数据

建议英文图题：Reliability-conditioned forecasting errors and spatial variation

本目录的每个CSV为独立面板或其辅助矩阵；对应XLSX列出全部面板。
- Fig05A_Coverage_Conditioned_Error.csv: 72 行；字段 horizon, cov_bin, model, n, MAE, RMSE, Bias, Median_AE, P90_AE, P95_AE, nodes, dates；X/Y及分组按字段名和统计口径选择。
- Fig05C_Volatility_Conditioned_Error.csv: 54 行；字段 horizon, cov_bin, model, n, MAE, RMSE, Bias, Median_AE, P90_AE, P95_AE, nodes, dates；X/Y及分组按字段名和统计口径选择。
- Fig05C_Coverage_Gap_Volatility_Joint.csv: 522 行；字段 horizon, cov_bin, model, n, MAE, RMSE, Bias, Median_AE, P90_AE, P95_AE, nodes, dates；X/Y及分组按字段名和统计口径选择。
- Fig05B_Gap_Conditioned_Error.csv: 198 行；字段 horizon, group, model, n, MAE, RMSE, Bias, Median_AE, P90_AE, P95_AE, nodes, dates；X/Y及分组按字段名和统计口径选择。
- Fig05D_Node_Level_Model_Error.csv: 918 行；字段 node_id, horizon, model, n_samples, MAE, Bias, RMSE, sample_support_status；X/Y及分组按字段名和统计口径选择。

样本量、单位、显著性及实现体系应从表内字段和全局来源清单读取；空值不得改作0。Fig.1当前OSM与历史主线不同，Fig.4折线/标准差为描述性，Fig.6点置信区间不是Holm同时区间，Fig.8 Ridge特殊共同目标配对结果未获SVD逐样本修正。E08未运行。原图对应：Fig.1–Fig.6分别对应原稿同号；Fig.7与Fig.8为新增建议。
