# Fig. 2 绘图数据

建议英文图题：Observation availability and data completeness of sparse floating car data

本目录的每个CSV为独立面板或其辅助矩阵；对应XLSX列出全部面板。
- Fig02A_Observation_Eligibility.csv: 5 行；字段 metric, value, statistical_level, denominator, ratio, historical_value, difference, definition, version；X/Y及分组按字段名和统计口径选择。
- Fig02A_Record_Level_Funnel.csv: 5 行；字段 metric, value, statistical_level, denominator, ratio, historical_value, difference, definition, version；X/Y及分组按字段名和统计口径选择。
- Fig02B_Daily_Coverage.csv: 498 行；字段 resolution, threshold, date, planned_slots, eligible_slots, coverage, incomplete_start_day, coverage_percent；X/Y及分组按字段名和统计口径选择。
- Fig02C_Hourly_Threshold_Coverage.csv: 4 行；字段 threshold, eligible_hours, ineligible_hours, planned_hours, coverage, historical_eligible, difference, loss_from_previous_threshold, nested_in_previous, coverage_percent；X/Y及分组按字段名和统计口径选择。
- Fig02D_Missing_Run_Distribution.csv: 241 行；字段 threshold, length_hours, run_count, nodes, left_censored_runs, right_censored_runs；X/Y及分组按字段名和统计口径选择。
- Fig02D_Node_Date_Coverage.csv: 4233 行；字段 node_id, hour_of_day, date, weekend, dimension, threshold, planned, observed, coverage；X/Y及分组按字段名和统计口径选择。
- Fig02D_Node_Date_Coverage_Wide.csv: 51 行；字段 node_id, 2025-12-08, 2025-12-09, 2025-12-10, 2025-12-11, 2025-12-12, 2025-12-13, 2025-12-14, 2025-12-15, 2025-12-16, 2025-12-17, 2025-12-18；X/Y及分组按字段名和统计口径选择。
- Fig02D_Node_Hour_Coverage.csv: 1224 行；字段 node_id, hour_of_day, date, weekend, dimension, threshold, planned, observed, coverage；X/Y及分组按字段名和统计口径选择。
- Fig02D_Node_Hour_Coverage_Wide.csv: 51 行；字段 node_id, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0；X/Y及分组按字段名和统计口径选择。

样本量、单位、显著性及实现体系应从表内字段和全局来源清单读取；空值不得改作0。Fig.1当前OSM与历史主线不同，Fig.4折线/标准差为描述性，Fig.6点置信区间不是Holm同时区间，Fig.8 Ridge特殊共同目标配对结果未获SVD逐样本修正。E08未运行。原图对应：Fig.1–Fig.6分别对应原稿同号；Fig.7与Fig.8为新增建议。
