# E03真实统计结果

主要口径A：三seed逐样本均值预测，Day-macro配对绝对损失。方法B独立保留，不按排名选择口径。原Table7对照：

```text
      model  horizon  manuscript_reported_value  method_A_value  method_B_value best_supported_original_definition
        GRU        1                      1.151        1.046958        1.150567                        B_MEAN_SEED
        GRU        3                      1.043        0.947604        1.043036                        B_MEAN_SEED
        GRU        6                      0.958        0.868938        0.958291                        B_MEAN_SEED
         HA        1                      1.825        1.824689        1.824689                         A_ENSEMBLE
         HA        3                      1.704        1.704279        1.704279                         A_ENSEMBLE
         HA        6                      1.505        1.504807        1.504807                         A_ENSEMBLE
Persistence        1                      0.950        0.950409        0.950409                         A_ENSEMBLE
Persistence        3                      1.170        1.170180        1.170180                         A_ENSEMBLE
Persistence        6                      1.470        1.469736        1.469736                         A_ENSEMBLE
      Ridge        1                      1.225        1.225137        1.225137                         A_ENSEMBLE
      Ridge        3                      1.131        1.131491        1.131491                         A_ENSEMBLE
      Ridge        6                      1.086        1.086178        1.086178                         A_ENSEMBLE
 SeasonalHA        1                      0.961        0.961016        0.961016                         A_ENSEMBLE
 SeasonalHA        3                      0.853        0.852857        0.852857                         A_ENSEMBLE
 SeasonalHA        6                      0.774        0.773757        0.773757                         A_ENSEMBLE
    XGBoost        1                      0.949        0.935267        0.949308                        B_MEAN_SEED
    XGBoost        3                      0.829        0.819415        0.829350                        B_MEAN_SEED
    XGBoost        6                      0.752        0.744363        0.751542                        B_MEAN_SEED
```

固定3日块10000次中心化双侧检验、每horizon五项Holm；7日敏感性。15项比较齐全，显著结果不是通过条件。

```text
 horizon            comparison    effect    CI_low   CI_high    raw_p  holm_adjusted_p
       1        XGBoost_vs_GRU -0.105127 -0.171156  0.002895 0.028497         0.056994
       1      XGBoost_vs_Ridge -0.256917 -0.307694 -0.181766 0.000100         0.000500
       1 XGBoost_vs_SeasonalHA  0.077330 -0.145534  0.445115 0.639836         0.639836
       1     Persistence_vs_HA -0.889201 -0.957391 -0.818806 0.000100         0.000500
       1          GRU_vs_Ridge -0.151790 -0.229197 -0.091589 0.000300         0.000900
       3        XGBoost_vs_GRU -0.231581 -0.484401 -0.074521 0.043396         0.086791
       3      XGBoost_vs_Ridge -0.402088 -0.698924 -0.197759 0.005599         0.016798
       3 XGBoost_vs_SeasonalHA  0.012295 -0.104316  0.173723 0.875412         0.875412
       3     Persistence_vs_HA -0.522363 -0.593331 -0.455163 0.000100         0.000500
       3          GRU_vs_Ridge -0.170507 -0.253136 -0.089534 0.000100         0.000500
       6        XGBoost_vs_GRU -0.258504 -0.586625 -0.064457 0.065293         0.195880
       6      XGBoost_vs_Ridge -0.465417 -0.880902 -0.207881 0.015198         0.060794
       6 XGBoost_vs_SeasonalHA -0.012050 -0.087033  0.085894 0.787421         0.951905
       6     Persistence_vs_HA -0.030043 -0.108395  0.054663 0.475952         0.951905
       6          GRU_vs_Ridge -0.206913 -0.330352 -0.104098 0.001700         0.008499
```

H1竞争比较EXPLORATORY单独标记。LOFO完整保留全部六种排除以及A/B，非重训CV。HAC/DM NOT_APPLICABLE：预冻结采用MBB长度敏感性和LOFO，短回顾序列及变化模型不额外承诺平稳假设。

普通95%区间不是同时区间。保留日期内全部节点只能缓解部分依赖，41日期仍有限；不称独立盲测、无差异或等效。Fold5/6诊断只有分布与误差证据，没有核查日历或宣称节日因果。


本实验包实际输出绝对路径：

- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_01_Seed_Aggregation_Reconciliation.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_02_Fold_Model_Metrics.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_03_Original_vs_Recomputed_Table7.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_04_Weighting_Estimands.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_04b_Historical_Cluster_Reconstruction.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_05_Daily_Paired_Loss.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_05b_Daily_Support_Diagnostics.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_06_Block_Bootstrap_Results.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_07_Block_Length_Sensitivity.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_08_Holm_Adjusted_Comparisons.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_09_H1_Practical_Differences.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_10_LOFO_Stability.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_11_Seed_Stability.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_12_Fold_Regime_Diagnostics.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_13_Estimand_Reversal_Explanation.md`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_Summary_CN.md`
