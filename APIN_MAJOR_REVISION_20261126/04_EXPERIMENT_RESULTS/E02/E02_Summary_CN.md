# E02真实计算结果

原始返回行自由流一致性：
                  level dimension group  total_rows  valid_ratio_rows  invalid_ratio_rows  exact_equal_fraction  within_1kmh_fraction  mean_abs_difference  median_abs_difference  p95_abs_difference  ratio_mean  ratio_median  ratio_p05  ratio_p95
  RETURN_ROW_UNFILTERED   overall   ALL      244477            244477                   0              0.854886              0.855115             2.247483                    0.0                17.0    0.968735           1.0   0.782051        1.0
RETURN_ROW_QUALITY_PASS   overall   ALL      243307            243307                   0              0.858993              0.859145             2.176320                    0.0                17.0    0.969458           1.0   0.784091        1.0

未来有效目标小时交通状态支持：
                       level  horizon                state     n  fraction  nodes  dates  threshold
FUTURE_OBSERVED_TARGET_HOURS      1.0      congested_proxy   952  0.024921     22     40        0.7
FUTURE_OBSERVED_TARGET_HOURS      1.0         intermediate  4072  0.106594     51     40        0.7
FUTURE_OBSERVED_TARGET_HOURS      1.0 near_free_flow_proxy 33177  0.868485     51     41        0.7
FUTURE_OBSERVED_TARGET_HOURS      3.0      congested_proxy   614  0.024753      8     40        0.7
FUTURE_OBSERVED_TARGET_HOURS      3.0         intermediate  2344  0.094497     28     40        0.7
FUTURE_OBSERVED_TARGET_HOURS      3.0 near_free_flow_proxy 21847  0.880750     51     41        0.7
FUTURE_OBSERVED_TARGET_HOURS      6.0      congested_proxy   700  0.024021      2     40        0.7
FUTURE_OBSERVED_TARGET_HOURS      6.0         intermediate  2697  0.092550     12     40        0.7
FUTURE_OBSERVED_TARGET_HOURS      6.0 near_free_flow_proxy 25744  0.883429     51     41        0.7

交通分类为操作化proxy（0.70/0.90），0.60/0.80仅固定敏感性，不选有利阈值。LOW_SUPPORT: n<30或日期<3或节点<3；不得强作显著性或稳定性解释。

Volatility从冻结X_sequence最后一行按原fold scaler还原至km/h；coverage/gap恢复已与manifest核对。因果填充重建对照见共享feature_recovery_audit.csv；若存在实质差异，原特征与论文定义差异必须在G1单独报告，不能默称恢复的特征符合ddof=0公式。

道路封闭：NOT_ESTIMABLE — NO OBSERVED CLOSURE EVENTS。供应商confidence不是经独立验证的概率；速度相等不证明历史回填或真实道路无拥堵。选择诊断只基于可观测历史proxy，不能据此证明MCAR/MAR/MNAR。

Free-flow基准采用已知记录的保守至少1h滞后和时间戳上界，不读取目标窗freeflow；无独立网络到达日志，时间可得性保留CONDITIONAL_PASS。所有比较使用相同覆盖交集，新增基准不混入原六模型排名。


本实验包实际输出绝对路径：

- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E02_TRAFFIC_RELIABILITY\E02_01_Speed_and_Target_Distribution.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E02_TRAFFIC_RELIABILITY\E02_01b_Distribution_Histograms.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E02_TRAFFIC_RELIABILITY\E02_02_FreeFlow_Equality.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E02_TRAFFIC_RELIABILITY\E02_03_Confidence_Distribution.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E02_TRAFFIC_RELIABILITY\E02_04_Traffic_Regime_Distribution.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E02_TRAFFIC_RELIABILITY\E02_05_Regime_Model_Performance.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E02_TRAFFIC_RELIABILITY\E02_05b_Regime_Threshold_Sensitivity.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E02_TRAFFIC_RELIABILITY\E02_06_Gap_Conditioned_Performance.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E02_TRAFFIC_RELIABILITY\E02_07_Coverage_Gap_Volatility.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E02_TRAFFIC_RELIABILITY\E02_08_Sample_Selection_Diagnostics.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E02_TRAFFIC_RELIABILITY\E02_09_Closure_and_Quality_Filter.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E02_TRAFFIC_RELIABILITY\E02_10_FreeFlow_Baseline.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E02_TRAFFIC_RELIABILITY\E02_Summary_CN.md`
