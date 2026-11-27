# Fig. 7 绘图数据

建议英文图题：Provider-reported speed distributions and traffic-regime-dependent forecast errors

本目录的每个CSV为独立面板或其辅助矩阵；对应XLSX列出全部面板。
- Fig07A_Current_and_FreeFlow_Speed_Distribution.csv: 76 行；字段 variable, level, bin_left, bin_right, n；X/Y及分组按字段名和统计口径选择。
- Fig07B_FreeFlow_Equality_and_Speed_Ratio.csv: 111 行；字段 level, dimension, group, total_rows, valid_ratio_rows, invalid_ratio_rows, exact_equal_fraction, within_1kmh_fraction, mean_abs_difference, median_abs_difference, p95_abs_difference, ratio_mean；X/Y及分组按字段名和统计口径选择。
- Fig07C_Confidence_Distribution.csv: 517 行；字段 level, dimension, group, confidence_bin, n, fraction, current_speed_mean, ratio_mean, confidence_missing_or_invalid, confidence_mean, confidence_median, confidence_sd；X/Y及分组按字段名和统计口径选择。
- Fig07D_Traffic_Regime_Model_Performance.csv: 54 行；字段 horizon, traffic_regime, model, n, MAE, RMSE, Bias, Median_AE, P90_AE, P95_AE, nodes, dates；X/Y及分组按字段名和统计口径选择。
- Fig07D_FreeFlow_Baseline.csv: 87 行；字段 horizon, model, n, MAE, RMSE, Bias, Median_AE, P90_AE, P95_AE, nodes, dates, support；X/Y及分组按字段名和统计口径选择。

样本量、单位、显著性及实现体系应从表内字段和全局来源清单读取；空值不得改作0。Fig.1当前OSM与历史主线不同，Fig.4折线/标准差为描述性，Fig.6点置信区间不是Holm同时区间，Fig.8 Ridge特殊共同目标配对结果未获SVD逐样本修正。E08未运行。原图对应：Fig.1–Fig.6分别对应原稿同号；Fig.7与Fig.8为新增建议。
