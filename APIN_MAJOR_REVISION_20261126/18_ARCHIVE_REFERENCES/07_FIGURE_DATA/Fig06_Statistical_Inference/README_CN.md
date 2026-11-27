# Fig. 6 绘图数据

建议英文图题：Dependence-aware statistical comparison of forecasting models

本目录的每个CSV为独立面板或其辅助矩阵；对应XLSX列出全部面板。
- Fig06A_H1_Paired_Effects.csv: 5 行；字段 family, horizon, comparison, effect, CI_low, CI_high, raw_p, holm_adjusted_p, dates, block_days, role, significant_holm_0_05；X/Y及分组按字段名和统计口径选择。
- Fig06B_H3_Paired_Effects.csv: 5 行；字段 family, horizon, comparison, effect, CI_low, CI_high, raw_p, holm_adjusted_p, dates, block_days, role, significant_holm_0_05；X/Y及分组按字段名和统计口径选择。
- Fig06C_H6_Paired_Effects.csv: 5 行；字段 family, horizon, comparison, effect, CI_low, CI_high, raw_p, holm_adjusted_p, dates, block_days, role, significant_holm_0_05；X/Y及分组按字段名和统计口径选择。
- Fig06D_Three_vs_Seven_Day_Blocks.csv: 30 行；字段 family, horizon, comparison, effect, CI_low, CI_high, raw_p, holm_adjusted_p, dates, block_days, role, significant_holm_0_05；X/Y及分组按字段名和统计口径选择。
- Fig06D_Alternative_Weighting_Estimands.csv: 144 行；字段 method, estimand, horizon, model, MAE, n, dates, folds, nodes, spatial_cells, weight_definition, delta_XGBoost_minus_SeasonalHA；X/Y及分组按字段名和统计口径选择。

样本量、单位、显著性及实现体系应从表内字段和全局来源清单读取；空值不得改作0。Fig.1当前OSM与历史主线不同，Fig.4折线/标准差为描述性，Fig.6点置信区间不是Holm同时区间，Fig.8 Ridge特殊共同目标配对结果未获SVD逐样本修正。E08未运行。原图对应：Fig.1–Fig.6分别对应原稿同号；Fig.7与Fig.8为新增建议。
