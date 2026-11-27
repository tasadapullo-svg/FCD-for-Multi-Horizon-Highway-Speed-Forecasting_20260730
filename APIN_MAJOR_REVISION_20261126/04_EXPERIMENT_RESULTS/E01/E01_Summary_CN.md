# E01真实计算结果

协议：e7e82b7260ebbc81585c4c7f7034d7a2d80a92730aa8d907687693c2cb2699f4。所有CSV已在生成报告时因缺少tabulate报错之前保存；本次仅补报告和receipt，不重算数据。

小时覆盖率：

```text
 threshold  eligible_hours  ineligible_hours  planned_hours  coverage  historical_eligible  difference  loss_from_previous_threshold  nested_in_previous
         1           96968              3910         100878  0.961240                96968           0                             0                True
         2           83439             17439         100878  0.827128                83439           0                         13529                True
         3           45356             55522         100878  0.449612                45356           0                         38083                True
         4           15838             85040         100878  0.157002                15838           0                         29518                True
```

H6测试完整度：

```text
    fold split        h6_group     n  target_mean  target_sd  target_median  target_p05  target_p95  fraction_within_fold_split
ALL_TEST  test COMPLETE_6_OF_6 14521    89.157623  15.986299           94.0   48.583333         100                    0.498301
ALL_TEST  test  PARTIAL_5_OF_6 14620    88.686768  16.514867           94.0   43.584167         100                    0.501699
```

54个split组合的样本重建键差异总数：0。新规则支持仅为ESTIMATED_SUPPORT；6/6子集评价不代表重新训练。归档无返回原因未知，日期修复代码仍未闭环。97.30% DEFINITION_UNRESOLVED — REMOVE_OR_REPLACE_IN_REVISION。每日分母使用实际网格；H3/H6目标不同，不用跨时距MAE证明优劣。


本实验包实际输出绝对路径：

- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E01_DATA_COMPLETENESS\E01_01_Data_Lineage_and_Coverage.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E01_DATA_COMPLETENESS\E01_02_Hourly_Threshold_Coverage.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E01_DATA_COMPLETENESS\E01_02b_Quarter_Count_Frequency.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E01_DATA_COMPLETENESS\E01_03_Daily_Coverage.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E01_DATA_COMPLETENESS\E01_03b_Coverage_Weighting.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E01_DATA_COMPLETENESS\E01_04_Node_Hour_Coverage.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E01_DATA_COMPLETENESS\E01_05_Missing_Run_Distribution.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E01_DATA_COMPLETENESS\E01_06_H6_Target_Completeness.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E01_DATA_COMPLETENESS\E01_07_H6_Missing_Position.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E01_DATA_COMPLETENESS\E01_08_H6_Stratified_Model_Performance.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E01_DATA_COMPLETENESS\E01_09_H3_H6_Common_Origins.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E01_DATA_COMPLETENESS\E01_10_Fold_Sample_Attrition.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E01_DATA_COMPLETENESS\E01_11_E04_Sample_Feasibility.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E01_DATA_COMPLETENESS\E01_Summary_CN.md`
