# AJSE Phase 2A：稀疏商业 FCD 多时距交通速度预测

本目录是 AJSE Phase 2A 论文的本地完整证据库，包含研究定义、数据处理代码、六折 rolling-origin 正式实验、逐级审计、聚合论文结果，以及受许可限制而不能公开的本地数据载荷。

> 重要：本地目录保留全部内容，但 GitHub 提交必须遵守根目录 `.gitignore`。不要使用 `git add -f` 绕过限制，也不要把 `07_LOCAL_RESTRICTED_DATA_DO_NOT_UPLOAD`、逐样本输入/目标/预测、模型权重或旧实验的大型输出上传到公开仓库。

## 论文与实验边界

- 任务：稀疏商业 FCD 条件下的未来窗口平均速度预测。
- 目标：`FUTURE_WINDOW_MEAN_SPEED`。
- 时距：H1、H3、H6。
- 输入：严格因果、连续 24 小时历史，不允许更长离散 lag 或 weekly context。
- 评估：六折 retrospective rolling-origin。
- 模型：HA、SeasonalHA、Persistence、Ridge、XGBoost、GRU。
- 正式运行：180/180 完成，0 失败。
- 全样本防泄漏断言：20/20 通过；未来信息违规 0；目标复算不一致 0。
- 结果级审计：`PASS_WITH_LIMITATIONS`；AJSE 主结果可用于论文，但必须保留限制。
- 推断单位：rolling-origin fold，`n=6`；按 horizon 进行 Holm 校正；预注册比较中校正后显著项为 0。
- 研究角色：回顾性 rolling-origin 评估，不是独立盲测；禁止把最终日历周描述为 blind test。
- CRG-TCN v2.2、P6/P7/P8 及另一篇论文不属于本仓库证据。

权威结果入口：

- `04_PHASE2A_DATA_RESULTS/06_REPORTS/AJSE_PHASE2A_RESULT_LEVEL_FINAL_AUDIT_REPORT.md`
- `04_PHASE2A_DATA_RESULTS/06_REPORTS/AJSE_PHASE2A_PAPER_RESULT_INTERPRETATION.md`
- `04_PHASE2A_DATA_RESULTS/06_REPORTS/AJSE_PHASE2A_RESULT_MASTER.xlsx`
- `04_PHASE2A_DATA_RESULTS/08_FINAL_AUDIT/PHASE2A_RESULT_LEVEL_AUDIT_STATUS.json`
- `04_PHASE2A_DATA_RESULTS/07_HASHES/PHASE2A_RESULT_FILE_SHA256.csv`

## 目录说明

| 目录 | 内容 | GitHub 默认状态 |
|---|---|---|
| `00_AJSE_SCOPE` | 论文写作大纲与研究边界 | 跟踪候选 |
| `00_MANIFESTS` | 早期整理、迁移与哈希记录 | 跟踪候选；部分路径是历史路径 |
| `01_PHASE2A_DEFINITION_FREEZE` | Phase 2A-0 定义冻结与审计证据 | 跟踪候选 |
| `02_PHASE2A_RELEASE_PACKAGE` | 冻结发布包及校验 | ZIP 本地保留，不默认跟踪 |
| `03_PHASE2A_BUILD_CODE` | Phase 2A-0 构建代码 | 跟踪候选 |
| `04_PHASE2A_DATA_RESULTS` | 六折正式结果、统计、报告和哈希 | 聚合证据跟踪；逐样本与权重本地保留 |
| `05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730` | 全盘检索、结果对应和偏差审计 | 跟踪候选 |
| `06_LEGACY_SINGLE_SPLIT_FUTURE_WINDOW_MEAN_EVIDENCE` | 旧 70/15/15 单划分探索性链 | 代码/配置/报告跟踪；大型 outputs 本地保留 |
| `07_LOCAL_RESTRICTED_DATA_DO_NOT_UPLOAD` | 商业原始及可还原逐时速度的派生数据 | 严禁公开上传 |
| `08_INTEGRITY_AND_CLASSIFICATION` | 早期目录完整性与论文范围核验 | 跟踪候选；状态先于正式实验完成 |
| `09_INDEPENDENT_REVIEW_20260730` | 早期独立复核 | 跟踪候选；状态先于正式实验完成 |
| `AJSE_sparse_FCD_rolling_v1` | 原始独立 Git 冻结仓库 | 原位保留、顶层提交忽略 |
| `10_GITHUB_PREPARATION` | GitHub 公共快照、两轮检查和上传说明 | 跟踪候选 |

## 状态时间线与冲突解释

早期文件 `00_README_START_HERE.md`、`00_START_HERE_AJSE_ONLY.md`、`08_INTEGRITY_AND_CLASSIFICATION/AJSE_SCOPE_DECISION.json` 和 `09_INDEPENDENT_REVIEW_20260730/INDEPENDENT_REVIEW_STATUS.json` 记录的是 Phase 2A-1 正式运行前状态，可能写有 `NOT_FOUND`、`NOT_READY` 或旧根目录 `D:\2026_AJSE_FINAL`。这些文件为审计历史，未被改写或删除。

当前结果状态以 `04_PHASE2A_DATA_RESULTS/08_FINAL_AUDIT/PHASE2A_RESULT_LEVEL_AUDIT_STATUS.json` 为准：`PHASE2A1_RESULTS=COMPLETE`、`AJSE_PRIMARY_RESULTS_READY=YES`、`PASS_WITH_LIMITATIONS`。

## GitHub 提交边界

根目录 `.gitignore` 把以下内容保留在本机但排除出公开提交：

- 商业原始 FCD 和可还原逐时速度的派生数据；
- fold 级完整输入张量、样本目标、panel；
- 逐样本预测与逐样本误差；
- 模型 checkpoints；
- 旧单划分实验的 bulk outputs；
- ZIP/GZ 等重复归档；
- 嵌套 `.git` 仓库及缓存、密钥类文件。

`10_GITHUB_PREPARATION/PUBLIC_REPOSITORY_CORE` 是 `AJSE_sparse_FCD_rolling_v1` 在提交 `5545c42ee7e111bfe2bd3f19c2920a31c06ac502` 的无 `.git` 工作树快照，用于避免顶层仓库把它误识别为 submodule。

## 复现顺序

1. 阅读 `10_GITHUB_PREPARATION/DATA_AVAILABILITY_AND_LICENSE.md`，取得商业 FCD 的合法本地访问权限。
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

- 尚未选择代码许可证与数据许可证；公开前必须由作者决定。
- 作者列表、单位、仓库 URL、论文 DOI/预印本 DOI 未提供，因此未生成最终 `CITATION.cff`。
- 精确 Python 包冻结未找到；现有记录确认实验使用 Python 3.10.20，根目录 `requirements.txt` 仅列运行依赖，不冒充原始精确环境。
- 历史报告中存在旧绝对路径；严格 UTF-8 扫描未确认编码异常，但旧版 Windows 控制台可能把中文显示为乱码。原始证据未被改写，新的顶层文档使用 UTF-8。
- 商业 FCD 许可不允许通过公开 GitHub 仓库重新分发。

## 完整性与两轮检查

查看：

- `10_GITHUB_PREPARATION/PASS1/GITHUB_READINESS_REPORT.md`
- `10_GITHUB_PREPARATION/PASS2/GITHUB_READINESS_REPORT.md`
- `10_GITHUB_PREPARATION/FINAL_GITHUB_READINESS_STATUS.json`
- `10_GITHUB_PREPARATION/ORIGINAL_BASELINE_SHA256.csv`

两轮核验均对整理前原始文件重新计算 SHA-256；原文件只允许 `MATCH`，不得出现 `MISSING` 或 `MISMATCH`。
