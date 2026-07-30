# AJSE Phase 2A 唯一工作目录

本目录只服务于 AJSE Phase 2A 论文：稀疏商业 FCD 的可审计、多时距交通速度预测评价。

## 论文边界

- 主目标：未来窗口平均速度（FUTURE_WINDOW_MEAN_SPEED）。
- 时距：H1、H3、H6。
- 计划中的主评价：六折 retrospective rolling-origin。
- 当前事实：Phase 2A-0 定义冻结完成但状态为 BLOCKED；未找到完成的六折 Phase 2A-1 主结果集。
- `06_LEGACY_SINGLE_SPLIT_FUTURE_WINDOW_MEAN_EVIDENCE` 是旧 70/15/15 单划分计算链，只能作探索性或历史证据，不能冒充六折主结果。
- `07_LOCAL_RESTRICTED_DATA_DO_NOT_UPLOAD` 含商业原始/派生 FCD，仅限本机审计，禁止上传 GitHub。

## 明确排除的另一篇文章

以下内容未复制进本目录：CRG_TCN_review_v2、v2.2 点预测 P0-P8、P6/P7/P8 冻结/解锁结果、CRG-TCN 收敛审计、T2 多模态环境数据，以及 CRG-TCN 文章稿件。

## 权威入口

- `00_AJSE_SCOPE`：AJSE 写作与实验蓝图。
- `00_MANIFESTS`：Phase 2A 既有清单。
- `01_PHASE2A_DEFINITION_FREEZE`：Phase 2A-0 冻结定义。
- `02_PHASE2A_RELEASE_PACKAGE`：冻结发布包。
- `03_PHASE2A_BUILD_CODE`：冻结包构建代码。
- `04_PHASE2A_DATA_RESULTS`：仅供真正的 Phase 2A-1 及后续六折结果；当前为空是正确状态。
- `05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730`：D 盘全量搜索与结果对应审计。
- `06_LEGACY_SINGLE_SPLIT_FUTURE_WINDOW_MEAN_EVIDENCE`：可复算但非主证据的旧单划分实验链。
- `07_LOCAL_RESTRICTED_DATA_DO_NOT_UPLOAD`：本地受限数据。
- `08_INTEGRITY_AND_CLASSIFICATION`：本次归集、排除、SHA-256与可读性核验。

## 当前论文结论边界

旧 Phase13 的 105 个预测文件已经独立复算，目标确为未来窗口平均速度，指标未发现数值不一致；但它不是六折 rolling-origin，H6 还存在 51 个越过规范完整小时边界的样本。因此 AJSE 的 Methods/数据审计可部分使用，正式主结果、跨折稳定性与确认性统计仍未完成。
