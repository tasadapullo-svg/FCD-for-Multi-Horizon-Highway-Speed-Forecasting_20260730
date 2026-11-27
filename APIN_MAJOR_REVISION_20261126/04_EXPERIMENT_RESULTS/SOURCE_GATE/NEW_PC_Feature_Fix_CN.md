# 新电脑 SOURCE_GATE 特征修复与实测

原缓存 `revision_data_v1` 的 `hours_since_last_observation` 在 50,269×24 个门槛历史位置中仅 3 处与冻结矩阵不一致。差异都在节点序列起始且尚无真实观测的小时：草稿设 `current=168`，冻结矩阵的对应原始计数为 1 或 2。其余位置匹配。旧代码备份为 `03_CODE\E04_E07_REVISION\data_engine.py.pre_age_fix_v1`。

新实现把节点起始计数设为 0，在缺测小时递增；不使用未来观测。缓存键从 `revision_data_v1` 升级到 `revision_data_v2`，共享小时特征目录加 `_v2`，Run ID 的预处理版本也升级，避免复用旧缓存。新缓存为 `02_DATA\03_DERIVED_DATA\E04_E07\d9e0a5542b59dcea869f`。只读逐样本复核：50,269 个样本键全匹配，目标最大差 0，13 特征最大绝对差 9.5367431640625e-07，静态特征最大差 0。Fold 1/H1 的训练、验证、测试分别为 38,044、6,247、5,978 样本。

2026-11-25 21:22（Asia/Shanghai）使用新电脑 CPU 实际执行六模型 SOURCE_GATE，状态为 `PASS_NEW_IMPLEMENTATION`；XGBoost 拟合 11.34 秒，GRU 拟合 33.82 秒。原训练源码仍未恢复；原实时 API 到达延迟仍无证据。`status.json` 与 `new_pc_gate_console.log` 保存完整结果和日志。门槛通过后方冻结新 G2 训练协议并启动正式实验。
