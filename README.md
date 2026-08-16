# AJSE Phase 2A：稀疏 FCD 多时距交通速度预测

本目录是 AJSE Phase 2A 论文的本地完整证据库，包含研究定义、数据处理代码、六折 rolling-origin 正式实验、逐级审计、聚合论文结果，以及受许可限制而不能公开的本地数据载荷。

> **重要：** 本地目录保留全部内容，但 GitHub 提交必须遵守根目录 `.gitignore`。不要使用 `git add -f` 绕过限制，也不要把 `07_LOCAL_RESTRICTED_DATA_DO_NOT_UPLOAD`、逐样本输入/目标/预测、模型权重或旧实验的大型输出上传到公开仓库。

## 论文与实验边界

* 任务：稀疏 FCD 条件下的未来窗口平均速度预测。
* 目标：`FUTURE_WINDOW_MEAN_SPEED`。
* 时距：H1、H3、H6。
* 输入：严格因果、连续 24 小时历史，不允许更长离散 lag 或 weekly context。
* 评估：六折 retrospective rolling-origin。
* 模型：HA、SeasonalHA、Persistence、Ridge、XGBoost、GRU。
* 正式运行：180/180 完成，0 失败。
* 全样本防泄漏断言：20/20 通过；未来信息违规 0；目标复算不一致 0。
* 结果级审计：`PASS_WITH_LIMITATIONS`；AJSE 主结果可用于论文，但必须保留限制。
* 推断单位：rolling-origin fold，`n=6`；按 horizon 进行 Holm 校正；预注册比较中校正后显著项为 0。
* 研究角色：回顾性 rolling-origin 评估，不是独立盲测；禁止把最终日历周描述为 blind test。
* CRG-TCN v2.2、P6/P7/P8 及另一篇论文不属于本仓库证据。

权威结果入口：

* `04_PHASE2A_DATA_RESULTS/06_REPORTS/AJSE_PHASE2A_RESULT_LEVEL_FINAL_AUDIT_REPORT.md`
* `04_PHASE2A_DATA_RESULTS/06_REPORTS/AJSE_PHASE2A_PAPER_RESULT_INTERPRETATION.md`
* `04_PHASE2A_DATA_RESULTS/06_REPORTS/AJSE_PHASE2A_RESULT_MASTER.xlsx`
* `04_PHASE2A_DATA_RESULTS/08_FINAL_AUDIT/PHASE2A_RESULT_LEVEL_AUDIT_STATUS.json`
* `04_PHASE2A_DATA_RESULTS/07_HASHES/PHASE2A_RESULT_FILE_SHA256.csv`

## 目录说明

| 目录                                                   | 内容                    | GitHub 默认状态                |
| ---------------------------------------------------- | --------------------- | -------------------------- |
| `00_AJSE_SCOPE`                                      | 论文写作大纲与研究边界           | 跟踪候选                       |
| `00_MANIFESTS`                                       | 早期整理、迁移与哈希记录          | 跟踪候选；部分路径是历史路径             |
| `01_PHASE2A_DEFINITION_FREEZE`                       | Phase 2A-0 定义冻结与审计证据  | 跟踪候选                       |
| `02_PHASE2A_RELEASE_PACKAGE`                         | 冻结发布包及校验              | ZIP 本地保留，不默认跟踪             |
| `03_PHASE2A_BUILD_CODE`                              | Phase 2A-0 构建代码       | 跟踪候选                       |
| `04_PHASE2A_DATA_RESULTS`                            | 六折正式结果、统计、报告和哈希       | 聚合证据跟踪；逐样本与权重本地保留          |
| `05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730`        | 全盘检索、结果对应和偏差审计        | 跟踪候选                       |
| `06_LEGACY_SINGLE_SPLIT_FUTURE_WINDOW_MEAN_EVIDENCE` | 旧 70/15/15 单划分探索性链    | 代码/配置/报告跟踪；大型 outputs 本地保留 |
| `07_LOCAL_RESTRICTED_DATA_DO_NOT_UPLOAD`             | 原始 FCD 及可还原逐时速度的派生数据  | 严禁公开上传                     |
| `08_INTEGRITY_AND_CLASSIFICATION`                    | 早期目录完整性与论文范围核验        | 跟踪候选；状态先于正式实验完成            |
| `09_INDEPENDENT_REVIEW_20260730`                     | 早期独立复核                | 跟踪候选；状态先于正式实验完成            |
| `AJSE_sparse_FCD_rolling_v1`                         | 原始独立 Git 冻结仓库         | 原位保留、顶层提交忽略                |
| `10_GITHUB_PREPARATION`                              | GitHub 公共快照、两轮检查和上传说明 | 跟踪候选                       |

## 状态时间线与冲突解释

早期文件 `00_README_START_HERE.md`、`00_START_HERE_AJSE_ONLY.md`、`08_INTEGRITY_AND_CLASSIFICATION/AJSE_SCOPE_DECISION.json` 和 `09_INDEPENDENT_REVIEW_20260730/INDEPENDENT_REVIEW_STATUS.json` 记录的是 Phase 2A-1 正式运行前状态，可能写有 `NOT_FOUND`、`NOT_READY` 或旧根目录 `D:\2026_AJSE_FINAL`。这些文件为审计历史，未被改写或删除。

当前结果状态以 `04_PHASE2A_DATA_RESULTS/08_FINAL_AUDIT/PHASE2A_RESULT_LEVEL_AUDIT_STATUS.json` 为准：`PHASE2A1_RESULTS=COMPLETE`、`AJSE_PRIMARY_RESULTS_READY=YES`、`PASS_WITH_LIMITATIONS`。

## GitHub 提交边界

根目录 `.gitignore` 把以下内容保留在本机但排除出公开提交：

* 原始 FCD 和可还原逐时速度的派生数据；
* fold 级完整输入张量、样本目标、panel；
* 逐样本预测与逐样本误差；
* 模型 checkpoints；
* 旧单划分实验的 bulk outputs；
* ZIP/GZ 等重复归档；
* 嵌套 `.git` 仓库及缓存、密钥类文件。

`10_GITHUB_PREPARATION/PUBLIC_REPOSITORY_CORE` 是 `AJSE_sparse_FCD_rolling_v1` 在提交 `5545c42ee7e111bfe2bd3f19c2920a31c06ac502` 的无 `.git` 工作树快照，用于避免顶层仓库把它误识别为 submodule。

## 复现顺序

1. 阅读 `10_GITHUB_PREPARATION/DATA_AVAILABILITY_AND_LICENSE.md`，取得 FCD 的合法本地访问权限。
2. 使用 `10_GITHUB_PREPARATION/PUBLIC_REPOSITORY_CORE/configs/phase2a1_frozen.yaml` 检查目标、fold、purge、seed 与模型集。
3. 运行 `src/build_phase2a1_data.py` 构建六折共同样本和防泄漏证据。
4. 冻结配置、代码和 manifest 后运行 `src/run_phase2a1_campaign.py`。
5. 运行 `src/finalize_phase2a1.py` 独立复算指标、依赖结构修正统计并生成审计报告。

这些脚本含有本机历史绝对路径痕迹；在另一台机器复现前，应通过参数或配置替换路径，不能改动冻结实验定义。

## 本地 Git 上传

请先阅读 `10_GITHUB_PREPARATION/GITHUB_UPLOAD_CHECKLIST.md`。根目录目前未自动 `git init`、未提交、未配置远端、未上传。建议先运行：

```powershell
cd D:\20260730_AJSE_FINAL
git init
git branch -M main
git add .
git status --short
```

在 commit 前必须确认 `git status` 中没有 `07_LOCAL_RESTRICTED_DATA_DO_NOT_UPLOAD`、`.npy`、`.pt`、逐样本 prediction、`window_index_all.csv` 或任何凭据。不要执行 `git add -f`。

## 已知限制与待作者处理事项

* 尚未选择代码许可证与数据许可证；公开前必须由作者决定。
* 作者列表、单位、仓库 URL、论文 DOI/预印本 DOI 未提供，因此未生成最终 `CITATION.cff`。
* 精确 Python 包冻结未找到；现有记录确认实验使用 Python 3.10.20，根目录 `requirements.txt` 仅列运行依赖，不冒充原始精确环境。
* 历史报告中存在旧绝对路径；严格 UTF-8 扫描未确认编码异常，但旧版 Windows 控制台可能把中文显示为乱码。原始证据未被改写，新的顶层文档使用 UTF-8。
* FCD 数据许可不允许通过公开 GitHub 仓库重新分发。

## 完整性与两轮检查

查看：

* `10_GITHUB_PREPARATION/PASS1/GITHUB_READINESS_REPORT.md`
* `10_GITHUB_PREPARATION/PASS2/GITHUB_READINESS_REPORT.md`
* `10_GITHUB_PREPARATION/FINAL_GITHUB_READINESS_STATUS.json`
* `10_GITHUB_PREPARATION/ORIGINAL_BASELINE_SHA256.csv`

两轮核验均对整理前原始文件重新计算 SHA-256；原文件只允许 `MATCH`，不得出现 `MISSING` 或 `MISMATCH`。

---

# AJSE Phase 2A: Sparse FCD Multi-Horizon Traffic Speed Forecasting

This repository contains the complete local evidence base for the AJSE Phase 2A study, including the frozen research definition, data-processing code, six-fold rolling-origin experiments, multi-stage audits, aggregated paper-level results, and locally retained data payloads that cannot be publicly redistributed because of licensing restrictions.

> **Important:** The complete evidence base is retained locally. Any public GitHub submission must comply with the root-level `.gitignore`. Do not use `git add -f` to bypass these restrictions. In particular, do not upload `07_LOCAL_RESTRICTED_DATA_DO_NOT_UPLOAD`, sample-level inputs, targets or predictions, model weights, or large outputs from legacy experiments to the public repository.

## Study and Experimental Scope

* **Task:** Future-window mean traffic speed forecasting under sparse FCD conditions.
* **Target:** `FUTURE_WINDOW_MEAN_SPEED`.
* **Forecast horizons:** H1, H3, and H6.
* **Input history:** Strictly causal continuous 24-hour history. Longer discrete lags or weekly-context features are not permitted.
* **Evaluation protocol:** Six-fold retrospective rolling-origin evaluation.
* **Models:** HA, SeasonalHA, Persistence, Ridge, XGBoost, and GRU.
* **Formal experiment campaign:** 180/180 runs completed, with 0 failures.
* **Full-sample leakage-control assertions:** 20/20 passed; 0 future-information violations; 0 target-recomputation inconsistencies.
* **Result-level audit status:** `PASS_WITH_LIMITATIONS`. The primary AJSE results are suitable for manuscript reporting, subject to the documented limitations.
* **Inference unit:** Rolling-origin fold, `n=6`. Holm correction is applied separately within each forecast horizon. The number of Holm-adjusted significant comparisons among the preregistered comparisons is 0.
* **Study interpretation:** This is a retrospective rolling-origin evaluation, not an independent blind test. The final calendar week must not be described as a blind test.
* **Out-of-scope evidence:** CRG-TCN v2.2, P6/P7/P8, and evidence belonging to another manuscript are outside the evidentiary scope of this repository.

Authoritative result entry points:

* `04_PHASE2A_DATA_RESULTS/06_REPORTS/AJSE_PHASE2A_RESULT_LEVEL_FINAL_AUDIT_REPORT.md`
* `04_PHASE2A_DATA_RESULTS/06_REPORTS/AJSE_PHASE2A_PAPER_RESULT_INTERPRETATION.md`
* `04_PHASE2A_DATA_RESULTS/06_REPORTS/AJSE_PHASE2A_RESULT_MASTER.xlsx`
* `04_PHASE2A_DATA_RESULTS/08_FINAL_AUDIT/PHASE2A_RESULT_LEVEL_AUDIT_STATUS.json`
* `04_PHASE2A_DATA_RESULTS/07_HASHES/PHASE2A_RESULT_FILE_SHA256.csv`

## Repository Structure

| Directory                                            | Description                                                              | Default GitHub Status                                                                |
| ---------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| `00_AJSE_SCOPE`                                      | Manuscript outline and study-scope definitions                           | Candidate for tracking                                                               |
| `00_MANIFESTS`                                       | Early organization, migration, and hash records                          | Candidate for tracking; some paths are historical                                    |
| `01_PHASE2A_DEFINITION_FREEZE`                       | Phase 2A-0 definition freeze and audit evidence                          | Candidate for tracking                                                               |
| `02_PHASE2A_RELEASE_PACKAGE`                         | Frozen release package and validation materials                          | ZIP files retained locally and not tracked by default                                |
| `03_PHASE2A_BUILD_CODE`                              | Phase 2A-0 data-build code                                               | Candidate for tracking                                                               |
| `04_PHASE2A_DATA_RESULTS`                            | Six-fold formal results, statistics, reports, and hashes                 | Aggregated evidence tracked; sample-level data and model weights retained locally    |
| `05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730`        | Repository-wide retrieval, result correspondence, and bias audit         | Candidate for tracking                                                               |
| `06_LEGACY_SINGLE_SPLIT_FUTURE_WINDOW_MEAN_EVIDENCE` | Legacy 70/15/15 single-split exploratory evidence chain                  | Code/configuration/reports tracked; large outputs retained locally                   |
| `07_LOCAL_RESTRICTED_DATA_DO_NOT_UPLOAD`             | Raw FCD and derived data capable of reconstructing hourly traffic speeds | Strictly prohibited from public upload                                               |
| `08_INTEGRITY_AND_CLASSIFICATION`                    | Early repository-integrity and manuscript-scope verification             | Candidate for tracking; status predates completion of the formal experiment campaign |
| `09_INDEPENDENT_REVIEW_20260730`                     | Early independent review                                                 | Candidate for tracking; status predates completion of the formal experiment campaign |
| `AJSE_sparse_FCD_rolling_v1`                         | Original independently frozen Git repository                             | Retained in place and ignored by the top-level repository                            |
| `10_GITHUB_PREPARATION`                              | Public repository snapshot, two-pass checks, and upload instructions     | Candidate for tracking                                                               |

## Status Timeline and Interpretation of Historical Conflicts

The early files `00_README_START_HERE.md`, `00_START_HERE_AJSE_ONLY.md`, `08_INTEGRITY_AND_CLASSIFICATION/AJSE_SCOPE_DECISION.json`, and `09_INDEPENDENT_REVIEW_20260730/INDEPENDENT_REVIEW_STATUS.json` document the repository state before the formal Phase 2A-1 campaign was completed.

These historical files may therefore contain status labels such as `NOT_FOUND` or `NOT_READY`, or may refer to the former root directory `D:\2026_AJSE_FINAL`. They have intentionally been retained without rewriting or deletion because they form part of the audit history.

The current authoritative result status is defined by:

`04_PHASE2A_DATA_RESULTS/08_FINAL_AUDIT/PHASE2A_RESULT_LEVEL_AUDIT_STATUS.json`

The current status is:

* `PHASE2A1_RESULTS=COMPLETE`
* `AJSE_PRIMARY_RESULTS_READY=YES`
* `PASS_WITH_LIMITATIONS`

## Public GitHub Submission Boundary

The root-level `.gitignore` keeps the following materials on the local machine while excluding them from the public repository:

* Raw FCD and derived data capable of reconstructing hourly traffic speeds;
* Complete fold-level input tensors, sample targets, and panels;
* Sample-level predictions and sample-level errors;
* Model checkpoints;
* Bulk outputs from legacy single-split experiments;
* Duplicate archives such as ZIP and GZ files;
* Nested `.git` repositories;
* Cache files, credentials, keys, and other sensitive files.

`10_GITHUB_PREPARATION/PUBLIC_REPOSITORY_CORE` is a `.git`-free working-tree snapshot of `AJSE_sparse_FCD_rolling_v1` at commit:

`5545c42ee7e111bfe2bd3f19c2920a31c06ac502`

This snapshot is included to prevent the top-level repository from mistakenly interpreting the original nested repository as a Git submodule.

## Reproduction Workflow

1. Read `10_GITHUB_PREPARATION/DATA_AVAILABILITY_AND_LICENSE.md` and obtain legitimate local access to the required FCD data.
2. Review `10_GITHUB_PREPARATION/PUBLIC_REPOSITORY_CORE/configs/phase2a1_frozen.yaml` to verify the target definition, rolling-origin folds, purge rules, random seeds, and model set.
3. Run `src/build_phase2a1_data.py` to construct the common six-fold samples and generate leakage-control evidence.
4. After freezing the configuration, code, and manifests, run `src/run_phase2a1_campaign.py`.
5. Run `src/finalize_phase2a1.py` to independently recompute the performance metrics, conduct dependence-aware statistical analyses, and generate the final audit reports.

Some scripts retain historical absolute paths from the original local machine. Before reproducing the workflow on another machine, these paths should be replaced through command-line parameters or configuration settings.

The frozen experimental definitions themselves must not be altered.

## Local Git Upload Procedure

Read `10_GITHUB_PREPARATION/GITHUB_UPLOAD_CHECKLIST.md` before preparing a public commit.

The original local root was not automatically initialized, committed, configured with a remote, or uploaded during repository preparation. The recommended initialization sequence was:

```powershell
cd D:\20260730_AJSE_FINAL
git init
git branch -M main
git add .
git status --short
```

Before committing, verify that `git status` does **not** contain any of the following:

* `07_LOCAL_RESTRICTED_DATA_DO_NOT_UPLOAD`
* `.npy` files
* `.pt` files
* sample-level prediction files
* `window_index_all.csv`
* credentials, access tokens, or other sensitive information

Do **not** use `git add -f`.

## Known Limitations and Author Actions

* A final code license and data license have not yet been selected and must be determined by the authors before formal release.
* The final author list, affiliations, repository citation metadata, manuscript DOI, and preprint DOI were not available during repository preparation; therefore, a final `CITATION.cff` was not generated.
* An exact frozen Python package environment was not found. Existing records confirm that the experiment used Python 3.10.20. The root-level `requirements.txt` lists runtime dependencies only and must not be interpreted as an exact reconstruction of the original environment.
* Historical reports contain legacy absolute paths. A strict UTF-8 scan did not identify confirmed encoding corruption, although older Windows terminals may display Chinese text incorrectly. Historical evidence files were intentionally left unchanged, while newly created top-level documentation uses UTF-8.
* The FCD data license does not permit redistribution of the restricted source or reconstructable data through a public GitHub repository.

## Integrity Verification and Two-Pass Review

See:

* `10_GITHUB_PREPARATION/PASS1/GITHUB_READINESS_REPORT.md`
* `10_GITHUB_PREPARATION/PASS2/GITHUB_READINESS_REPORT.md`
* `10_GITHUB_PREPARATION/FINAL_GITHUB_READINESS_STATUS.json`
* `10_GITHUB_PREPARATION/ORIGINAL_BASELINE_SHA256.csv`

Both verification passes recomputed SHA-256 checksums against the original files as they existed before repository preparation.

For preserved original files, only the status `MATCH` is acceptable. No preserved original file should report `MISSING` or `MISMATCH`.
