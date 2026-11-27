# Fig. 8 绘图数据

建议英文图题：Sensitivity, protocol ablation, and model-fairness evidence

本目录的每个CSV为独立面板或其辅助矩阵；对应XLSX列出全部面板。
- Fig08A_Threshold_Sensitivity.csv: 432 行；字段 run_id, status, experiment_first_use, condition, implementation, model, fold, horizon, seed, config_id, configuration_json, manifest_sha256；X/Y及分组按字段名和统计口径选择。
- Fig08A_Threshold4_Not_Estimable.csv: 18 行；字段 fold, horizon, train_n, train_nodes, train_dates, validation_n, validation_nodes, validation_dates, test_n, test_nodes, test_dates, status；X/Y及分组按字段名和统计口径选择。
- Fig08B_H6_Target_Completeness.csv: 132 行；字段 run_id, status, experiment_first_use, condition, implementation, model, fold, horizon, seed, config_id, configuration_json, manifest_sha256；X/Y及分组按字段名和统计口径选择。
- Fig08C_Imputation_Sensitivity.csv: 342 行；字段 run_id, status, experiment_first_use, condition, implementation, model, fold, horizon, seed, config_id, configuration_json, manifest_sha256；X/Y及分组按字段名和统计口径选择。
- Fig08D_History_Window_Sensitivity.csv: 144 行；字段 run_id, status, experiment_first_use, condition, implementation, model, fold, horizon, seed, config_id, configuration_json, manifest_sha256；X/Y及分组按字段名和统计口径选择。
- Fig08E_Grid_Protocol_Ablation.csv: 96 行；字段 run_id, status, experiment_first_use, condition, implementation, model, fold, horizon, seed, config_id, configuration_json, manifest_sha256；X/Y及分组按字段名和统计口径选择。
- Fig08E_Causal_Scaling_Diagnostic.csv: 24 行；字段 run_id, status, experiment_first_use, condition, implementation, model, fold, horizon, seed, config_id, configuration_json, manifest_sha256；X/Y及分组按字段名和统计口径选择。
- Fig08E_Native_Eligibility_Check.csv: 12 行；字段 fold, horizon, ridge_native_n, xgboost_native_n, common_n, symmetric_difference_n, basis, decision；X/Y及分组按字段名和统计口径选择。
- Fig08F_Validation_Based_Tuning.csv: 27 行；字段 model, horizon, candidate, validation_MAE, run_id, fit_seconds, status；X/Y及分组按字段名和统计口径选择。
- Fig08F_Configuration_Contrasts.csv: 72 行；字段 model, fold, horizon, comparison, fixed_value, selected_value, common_test_n, fixed_test_MAE, selected_test_MAE, delta_selected_minus_fixed, fixed_run_id, selected_run_id；X/Y及分组按字段名和统计口径选择。
- Fig08F_Three_Seed_Ensemble_Results.csv: 54 行；字段 model, fold, horizon, n, method_A_MAE, method_A_RMSE, method_A_Bias, method_A_sMAPE, method_B_MAE, method_B_RMSE, method_B_Bias, method_B_sMAPE；X/Y及分组按字段名和统计口径选择。
- Fig08_Matched_Common_Origin_Contrasts.csv: 330 行；字段 condition, reference_condition, model, fold, horizon, seed, common_n, reference_MAE_on_common_origin, alternative_MAE_on_reference_target, paired_MAE_delta_alt_minus_ref, alternative_own_target_MAE, target_values_equal_on_common_origin；X/Y及分组按字段名和统计口径选择。
- Fig08_Key_Statistical_Comparisons.csv: 4 行；字段 comparison_id, paired_samples, test_days, sample_weighted_MAE_delta_alt_minus_ref, day_mean_MAE_delta_alt_minus_ref, block3_CI_low, block3_CI_high, block3_p_two_sided, block7_CI_low, block7_CI_high, block7_p_descriptive, seed；X/Y及分组按字段名和统计口径选择。

样本量、单位、显著性及实现体系应从表内字段和全局来源清单读取；空值不得改作0。Fig.1当前OSM与历史主线不同，Fig.4折线/标准差为描述性，Fig.6点置信区间不是Holm同时区间，Fig.8 Ridge特殊共同目标配对结果未获SVD逐样本修正。E08未运行。原图对应：Fig.1–Fig.6分别对应原稿同号；Fig.7与Fig.8为新增建议。
