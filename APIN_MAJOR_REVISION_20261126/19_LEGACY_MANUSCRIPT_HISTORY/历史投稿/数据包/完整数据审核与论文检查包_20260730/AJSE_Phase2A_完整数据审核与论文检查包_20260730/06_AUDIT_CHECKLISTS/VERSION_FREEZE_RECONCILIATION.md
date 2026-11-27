# Git版本冻结核对表

## 当前待核对的两个版本

| 角色 | Commit | Tag | 来源 |
|---|---|---|---|
| 报告内部冻结 | `245055057b2427a804eb45515131dd258fe85359` | `ajse-phase2a1-final-audit-freeze-20260730` | Executive status/report package |
| 用户最新冻结 | `5545c42ee7e111bfe2bd3f19c2920a31c06ac502` | `ajse-phase2a1-final-freeze-20260730-v3` | 用户最终说明 |

## 建议最终登记

```text
experiment_commit = <生成180个正式预测的commit>
result_audit_commit = <生成终审报告和工作簿的commit>
final_release_tag = <最终公开或投稿归档tag>
repository_status = CLEAN
```

## 必须一致的文件

- README.md
- frozen YAML
- executive status
- master workbook
- SHA-256 manifest
- GitHub release说明
- 论文Data Availability
- Supplementary reproducibility statement
