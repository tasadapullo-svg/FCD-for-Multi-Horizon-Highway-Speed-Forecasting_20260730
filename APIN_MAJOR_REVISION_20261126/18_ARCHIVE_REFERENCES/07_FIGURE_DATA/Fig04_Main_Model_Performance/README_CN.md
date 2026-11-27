# Fig. 4 绘图数据

建议英文图题：Multi-horizon forecasting performance under the common-sample evaluation protocol

本目录的每个CSV为独立面板或其辅助矩阵；对应XLSX列出全部面板。
- Fig04A_H1_Model_Performance.csv: 36 行；字段 fold, horizon, model, n_test, MAE, RMSE, Bias, Median_AE, P90_AE, P95_AE, nodes, dates；X/Y及分组按字段名和统计口径选择。
- Fig04B_H3_Model_Performance.csv: 36 行；字段 fold, horizon, model, n_test, MAE, RMSE, Bias, Median_AE, P90_AE, P95_AE, nodes, dates；X/Y及分组按字段名和统计口径选择。
- Fig04C_H6_Model_Performance.csv: 36 行；字段 fold, horizon, model, n_test, MAE, RMSE, Bias, Median_AE, P90_AE, P95_AE, nodes, dates；X/Y及分组按字段名和统计口径选择。
- Fig04D_Model_Ranking_and_Fold_Variation.csv: 18 行；字段 model, horizon, method_A_value, method_A_fold_sd, rank；X/Y及分组按字段名和统计口径选择。
- Fig04D_LOFO_Model_Performance.csv: 252 行；字段 method, horizon, excluded_fold, model, MAE, rank, descriptive_winner, all6_winner, winner_reversal, XGBoost_minus_SeasonalHA, XGBoost_minus_Persistence, folds；X/Y及分组按字段名和统计口径选择。
- Fig04D_Within_Fold_Seed_Ranges.csv: 108 行；字段 fold, horizon, model, seed, seed_MAE, mean_seed_MAE, seed_sd_ddof1, seed_min, seed_max, seed_range, ensemble_MAE, ensemble_minus_mean_seed_MAE；X/Y及分组按字段名和统计口径选择。

样本量、单位、显著性及实现体系应从表内字段和全局来源清单读取；空值不得改作0。Fig.1当前OSM与历史主线不同，Fig.4折线/标准差为描述性，Fig.6点置信区间不是Holm同时区间，Fig.8 Ridge特殊共同目标配对结果未获SVD逐样本修正。E08未运行。原图对应：Fig.1–Fig.6分别对应原稿同号；Fig.7与Fig.8为新增建议。
