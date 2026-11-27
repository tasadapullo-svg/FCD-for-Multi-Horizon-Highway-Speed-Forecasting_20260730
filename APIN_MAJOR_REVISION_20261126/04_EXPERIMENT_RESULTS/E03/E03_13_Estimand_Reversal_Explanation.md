# 权重与种子聚合方向变化：实际核验
原稿Equation(12)指定A，B是逐seed指标均值。以下为实际计算，不能把全部反转先验归因于权重。

## H1

```text
               method          estimand  delta_XGBoost_minus_SeasonalHA
A_ENSEMBLE_PREDICTION        Fold-macro                       -0.025749
A_ENSEMBLE_PREDICTION   Sample-weighted                       -0.040900
A_ENSEMBLE_PREDICTION         Day-macro                        0.077330
A_ENSEMBLE_PREDICTION Day-spatial-block                        0.053894
     B_MEAN_SEED_LOSS        Fold-macro                       -0.011708
     B_MEAN_SEED_LOSS   Sample-weighted                       -0.026925
     B_MEAN_SEED_LOSS         Day-macro                        0.091405
     B_MEAN_SEED_LOSS Day-spatial-block                        0.068424
```

历史保存的day×block点估计：
```text
           comparison  horizon metric            paired_unit  n_days  n_block_days  bootstrap_replicates  mean_difference_a_minus_b    CI_low  CI_high
XGBoost_vs_SeasonalHA        1    MAE day_then_spatial_block      41           205                 10000                   0.068424 -0.150971  0.37622
```

## H3

```text
               method          estimand  delta_XGBoost_minus_SeasonalHA
A_ENSEMBLE_PREDICTION        Fold-macro                       -0.033442
A_ENSEMBLE_PREDICTION   Sample-weighted                       -0.053296
A_ENSEMBLE_PREDICTION         Day-macro                        0.012295
A_ENSEMBLE_PREDICTION Day-spatial-block                        0.013670
     B_MEAN_SEED_LOSS        Fold-macro                       -0.023507
     B_MEAN_SEED_LOSS   Sample-weighted                       -0.043727
     B_MEAN_SEED_LOSS         Day-macro                        0.023076
     B_MEAN_SEED_LOSS Day-spatial-block                        0.025185
```

历史保存的day×block点估计：
```text
           comparison  horizon metric            paired_unit  n_days  n_block_days  bootstrap_replicates  mean_difference_a_minus_b    CI_low  CI_high
XGBoost_vs_SeasonalHA        3    MAE day_then_spatial_block      41           205                 10000                   0.025185 -0.111556 0.189095
```

## H6

```text
               method          estimand  delta_XGBoost_minus_SeasonalHA
A_ENSEMBLE_PREDICTION        Fold-macro                       -0.029394
A_ENSEMBLE_PREDICTION   Sample-weighted                       -0.044142
A_ENSEMBLE_PREDICTION         Day-macro                       -0.012050
A_ENSEMBLE_PREDICTION Day-spatial-block                        0.015109
     B_MEAN_SEED_LOSS        Fold-macro                       -0.022214
     B_MEAN_SEED_LOSS   Sample-weighted                       -0.037087
     B_MEAN_SEED_LOSS         Day-macro                       -0.004809
     B_MEAN_SEED_LOSS Day-spatial-block                        0.022590
```

历史保存的day×block点估计：
```text
           comparison  horizon metric            paired_unit  n_days  n_block_days  bootstrap_replicates  mean_difference_a_minus_b   CI_low  CI_high
XGBoost_vs_SeasonalHA        6    MAE day_then_spatial_block      41           205                 10000                    0.02259 -0.09449 0.210998
```

原空间块ID直接取manifest，未新造空间划分。历史点估计的数值重建范围见E03_04b；未恢复旧bootstrap源程序，因此旧CI不声称完全再现。新MBB处理日期相关性，不将205个块视为独立。跨fold连续块保留相邻日期但不同fold模型训练状态不同，仍有短样本与非平稳局限。

定向核验：原day×block表的205个单元格在B方法下逐项重建至浮点精度；历史点估计与新A的差异包括seed聚合和统计权重两部分。E03_04b已修正日期层连接错误；未更动主要推断。旧重采样程序未恢复，仍不声称CI完全复现。


补充日期支持解释：H1每天样本数范围35–1203，LOW_SUPPORT_DATE数量0。H3每天样本数范围18–1161，LOW_SUPPORT_DATE数量1。H6每天样本数范围28–1222，LOW_SUPPORT_DATE数量1。 Day-macro给每个有效日期等权，低观测日期不会按样本量自动降权；这会放大少数低支持日期影响，属于预先选定估计对象的实际限制。未据测试误差删除日期或改变主要统计方案，须与Sample-weighted及7日块敏感性共同阅读。证据：`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_05b_Daily_Support_Diagnostics.csv`。
