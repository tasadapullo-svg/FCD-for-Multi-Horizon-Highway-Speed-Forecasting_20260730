# Fig. 3 绘图数据

建议英文图题：An auditable GATE-FCD forecasting and evaluation protocol

本目录的每个CSV为独立面板或其辅助矩阵；对应XLSX列出全部面板。
- Fig03A_Protocol_Nodes.csv: 10 行；字段 step_id, step_name_en, step_name_cn, stage, input, processing_rule, output, eligibility_condition, causal_constraint, evidence_source, reviewer_mapping；X/Y及分组按字段名和统计口径选择。
- Fig03B_Protocol_Edges.csv: 9 行；字段 from_step, to_step, edge_type, condition；X/Y及分组按字段名和统计口径选择。
- Fig03C_Time_Semantics.csv: 3 行；字段 horizon, history_hours, decision_time, target_interval, required_observed_target_hours, target_imputation, target_must_remain_in_split；X/Y及分组按字段名和统计口径选择。

样本量、单位、显著性及实现体系应从表内字段和全局来源清单读取；空值不得改作0。Fig.1当前OSM与历史主线不同，Fig.4折线/标准差为描述性，Fig.6点置信区间不是Holm同时区间，Fig.8 Ridge特殊共同目标配对结果未获SVD逐样本修正。E08未运行。原图对应：Fig.1–Fig.6分别对应原稿同号；Fig.7与Fig.8为新增建议。
