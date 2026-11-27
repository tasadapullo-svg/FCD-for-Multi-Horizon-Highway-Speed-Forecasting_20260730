# 文件包范围与限制

## 已包含

- AJSE Phase 2A详细写作大纲；
- 多子图规划和逻辑解释版文档；
- 结果主工作簿；
- 模型×horizon汇总CSV；
- 结果级终审报告；
- 论文结果解释报告；
- 执行状态文件；
- 工作簿inspection NDJSON；
- 三张方法与证据结构示意图；
- GitHub仓库模板；
- 数据审核和论文数据检查清单；
- 本包文件清单与SHA-256。

## 当前对话中未获得，因此未包含

以下文件只在用户本地路径中被提及，但未上传到当前会话：

- 180个逐项预测文件；
- 18个原始共同sample manifest；
- `model_horizon_summary.csv`原文件；
- `corrected_fold_pairwise_tests_holm.csv`原文件；
- `PREDICTION_REGISTRY_HASH_RECHECK.json`；
- `PHASE2A_RESULT_FILE_SHA256.csv`；
- `PHASE2A_HASH_VERIFICATION.json`；
- `phase2a1_frozen.yaml`；
- 正式训练、评价、审计脚本；
- 原始或派生FCD面板；
- Git仓库对象和完整commit历史。

因此，本包适合：结果级复核、论文规划、数值检查和GitHub结构准备。

本包暂不能单独完成：从原始数据重新训练180次模型、逐预测文件重算、重新生成全部manifest或复核本地Git对象。

## 版本不一致事项

当前材料中存在两套版本标识：

### 报告内部记录

```text
CONFIG_GIT_COMMIT = 245055057b2427a804eb45515131dd258fe85359
CONFIG_GIT_TAG_AT_FINALIZE = ajse-phase2a1-final-audit-freeze-20260730
```

### 用户最新提供

```text
Git commit = 5545c42ee7e111bfe2bd3f19c2920a31c06ac502
Git tag = ajse-phase2a1-final-freeze-20260730-v3
```

投稿前必须明确：

- 哪个commit生成正式预测；
- 哪个commit生成最终审计报告；
- 哪个tag对应公开release；
- 工作簿、README、YAML和论文Data Availability中的版本是否一致。
