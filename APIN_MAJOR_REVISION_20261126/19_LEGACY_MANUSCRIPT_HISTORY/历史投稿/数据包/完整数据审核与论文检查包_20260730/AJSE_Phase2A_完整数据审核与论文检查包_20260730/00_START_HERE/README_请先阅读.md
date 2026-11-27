# AJSE Phase 2A 完整数据审核与论文检查包

## 1. 本包用途

本包用于下一阶段的：

1. 数据完整性复核；
2. 模型结果和统计结果复核；
3. 论文表格、图片和数值回填；
4. GitHub仓库整理；
5. 投稿前证据链检查。

## 2. 当前正式状态

```text
AJSE_RESULT_LEVEL_AUDIT_STATUS = PASS_WITH_LIMITATIONS
AJSE_PRIMARY_RESULTS_READY = YES
FORMAL_RUNS = 180/180
FAILED_RUNS = 0
ROLLING_ORIGIN_FOLDS = 6
FORECAST_HORIZONS = H1, H3, H6
COMMON_FOLD_HORIZON_MANIFESTS = 18
FULL_SAMPLE_LEAKAGE_ASSERTIONS = 20/20 PASS
AUDITED_FOLD_SPECIFIC_SAMPLE_RECORDS = 1,053,618
FUTURE_INFORMATION_VIOLATIONS = 0
TARGET_RECALCULATION_MISMATCHES = 0
PREDICTION_FILES_VERIFIED = 180
RESULT_FILES_HASHED = 519
HASH_MISMATCHES = 0
```

## 3. 核心结果

| Future-window target | XGBoost fold-mean MAE | 解释 |
|---|---:|---|
| H1 | 0.949 ± 0.258 km/h | 最低平均MAE，但与Persistence和SeasonalHA接近 |
| H3 | 0.829 ± 0.168 km/h | 最低平均MAE，但优势未通过Holm校正 |
| H6 | 0.752 ± 0.142 km/h | 最低平均MAE，但目标本身因6小时平均而更平滑 |

允许写：

> XGBoost achieved the lowest fold-averaged MAE at all three future-window horizons.

必须同时写：

> None of the prespecified fold-level pairwise comparisons remained significant after Holm correction.

## 4. 证据边界

- 这是六折回顾性rolling-origin评价，不是独立盲测。
- 最后一周曾被旧开发过程暴露，不能称为blind test、untouched test或external validation。
- CRG-TCN不属于本次AJSE正式模型集。
- 1,053,618表示折内样本审计记录数量，不表示105万条统计独立观测。
- H1、H3、H6是未来1、3、6小时窗口平均速度，不是单点的t+1、t+3、t+6预测。
- XGBoost平均误差最低，不等于显著优于全部基线。

## 5. 推荐使用顺序

1. 阅读 `00_START_HERE/PACKAGE_SCOPE_AND_LIMITATIONS.md`；
2. 检查 `03_AUDIT_REPORTS` 中的终审结论；
3. 打开 `02_RESULT_MASTER/AJSE_PHASE2A_RESULT_MASTER.xlsx`；
4. 按 `06_AUDIT_CHECKLISTS/DATA_AUDIT_CHECKLIST.md` 进行数据审核；
5. 按 `06_AUDIT_CHECKLISTS/PAPER_DATA_CHECKLIST.md` 进行论文数据回填；
6. 最后核对 `06_AUDIT_CHECKLISTS/CLAIMS_BOUNDARY.md`。

## 6. 重要提醒

本包仅整合了当前对话中已经上传或生成的文件。它不包含用户本地 `D:\2026_AJSE_FINAL` 中尚未上传的180个原始预测文件、18个原始manifest、冻结YAML、519项完整哈希清单以及全部脚本。完整可复现审核仍应以本地冻结工程为准。
