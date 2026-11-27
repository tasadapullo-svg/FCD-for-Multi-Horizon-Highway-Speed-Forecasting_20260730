# 新电脑迁移修复日志

2026-11-25：复用现有 PROJECT_ROOT，仅使用已核验的 `APIN_PRIVATE_NewPC_Transfer_20261125.zip`。执行 Python zipfile 定向恢复，检查每个相对路径无 `..`、目标位于 PROJECT_ROOT 内、不覆盖已有文件，恢复 816 项（冻结仓库 746、G0 审计 69、原始 FCD 1）。原 `verify_transfer.py` 将 JSON 顶层对象当作数组而报错；为保持 1052 项原清单哈希，原文件恢复原样，另建 `verify_transfer_fixed.py` 读取 `files` 并核对路径、字节数、SHA-256。执行 `py ...\verify_transfer_fixed.py`，结果 `checked=1052, errors=[], status=PASS`，见 `NEW_PC_TRANSFER_VERIFY_RESULT.json`。ZIP 使用 Python hashlib/zipfile 核对大小、SHA-256、条目数和 CRC。随后执行 `py ...\relocate_project.py`，仅处理 G2 操作性缓存路径。MIGRATION_PASS；后续代码修改不再属于原迁移快照。

## 实际命令与失败记录

在 PowerShell 中先设 `$env:APIN_ROOT='E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改'`，以 `@' ... '@ | py -` 执行 Python `zipfile` 定向恢复脚本（按清单逐项检查路径，并对不存在的目标使用 `open('xb')`）。其输出为 `RESTORED 816 SECONDS 3.93`。随后：

```powershell
py 'E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改\00_PROJECT_CONTROL\MIGRATION\verify_transfer.py'
py 'E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改\00_PROJECT_CONTROL\MIGRATION\verify_transfer_fixed.py'
py 'E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改\00_PROJECT_CONTROL\MIGRATION\relocate_project.py'
```

第一条因原脚本清单结构解析错误失败；曾试图原位修正后又因脚本自身在清单中而产生该文件大小与哈希不符，已从准确 ZIP 恢复原文件并保持其哈希。第二条结果为 1052 项全部通过、0 错误；第三条仅重定位 G2 缓存路径，完整回执见 `relocation_receipt.json`。哈希核验发生在代码及缓存重定位之前，后续 G2 实现修改不回写原迁移快照。
