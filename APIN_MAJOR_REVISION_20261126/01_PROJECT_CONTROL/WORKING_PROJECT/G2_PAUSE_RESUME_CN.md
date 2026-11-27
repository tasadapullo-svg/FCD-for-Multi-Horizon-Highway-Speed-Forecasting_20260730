# G2 暂停与恢复记录

用户要求：五小时额度剩余低于 5% 时停止，并在停止后 2 小时 15 分继续工程。停工前须中断仍在运行的 E06/E04 进程；`run_one` 已完成运行以 Run ID 复用，正在拟合的 `RUNNING` 可在恢复时重试，不能计作已完成。恢复后先读取本文件、SOURCE_GATE 状态、E06/E04 控制台日志与 Run Registry，再按相同脚本继续，不重算有效运行。

- SOURCE_GATE：`PASS_NEW_IMPLEMENTATION`；六模型完成。
- 迁移：1052/1052 哈希通过；补齐 816 项。
- 环境：CPU 训练环境及独立 CUDA 验证环境已建立；GPU 张量检查通过。当前正式运行 CPU。
- 已启动：`03_CODE\E04_E07_REVISION\run_e06_core.py` 与 `run_e04_core.py threshold1`。两者均可重复执行并复用相同 Run ID 的有效结果。
- 尚待：E04 其余条件、E05、E06 汇总、E07 效率及来源核查、八份 G2 核心交付与受控 ZIP。E08/论文修改/审稿回复不属本轮。

暂停时间（Asia/Shanghai）：2026-11-25 21:59:56；最早恢复时间：2026-11-26 00:14:56。五小时额度实测剩余4%。两训练进程已 Ctrl+C 停止。Run状态：{"COMPLETED":128,"RUNNING":2,"COMPLETED_VALIDATION_ONLY":15}。恢复时仅对 RUNNING 的未完成单元重试。

第二次暂停（Asia/Shanghai）：2026-11-26 02:11:39；最早恢复时间：2026-11-26 04:26:39。五小时额度实测剩余 4%，已对 E06 会话 Ctrl+C，E04、E05 全部适用阶段已正常完成。当前本地 Run 状态：`COMPLETED=634`、`COMPLETED_VALIDATION_ONLY=9`、`RUNNING=1`；最后中断的运行是 E06 H6/F6/seed42 的 GRU，恢复时按相同 `run_e06_core.py` 入口重试该未完成单元，其余有效 Run ID 复用。E06 H6/F1–F5 已完成，F6 的 Ridge 与 XGBoost 已完成。四项预冻结关键配对检验已完成；E07 GIS/日历资料和首轮推理基准已完成，但推理基准需在训练结束、CPU 空闲时按原协议再测。恢复后完成 E06、最终汇总、工作簿、验收与 ZIP；不得启动 E08 或改论文正文。
