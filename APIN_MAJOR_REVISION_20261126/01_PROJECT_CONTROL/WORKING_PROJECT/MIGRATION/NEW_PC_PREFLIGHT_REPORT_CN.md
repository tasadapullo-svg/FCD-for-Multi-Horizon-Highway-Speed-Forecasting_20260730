# 新电脑迁移核验与 G2 启动前评估（2026-11-25）

- OUTPUT_ROOT：`E:\20261125_论文修改_Applied Intelligence`
- PROJECT_ROOT：`E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改`
- 指定迁移包：`E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改\APIN_PRIVATE_NewPC_Transfer_20261125.zip`
- 发现两套相似工程及两个顶层 ZIP：另有 `E:\20261125_论文修改_Applied Intelligence\大修_20261124-低成本稀疏浮动车数据采集与可靠性感知预测框架：面向数据稀缺高速走廊_Applied Intelligence` 及其同名 ZIP（2,390,442,524 字节），以及本工程同名 ZIP（1,214,696,138 字节）。选用含 `00_PROJECT_CONTROL`、`02_DATA`、`03_CODE`、迁移清单和指定迁移包的现有 `2026112` 工程。未混用另一工程或 ZIP 的文件；目录名未改。

## 1. 迁移包、清单与关键输入

指定 ZIP 实测 611,916,943 字节，SHA-256 为 `4579fa79da3ec76a78657caec67543b21698d4a317bec2678d29be08e2999729`；1053 个 ZIP 条目，逐条 CRC 检查通过。清单列出 1052 项，1052 个相对路径均在 ZIP 内。故**迁移包本身的身份和压缩内容得到完整核验**。

落地工程**未完整解压**：先运行原 `verify_transfer.py`，它把顶层 JSON 对象误当数组，报 `TypeError: string indices must be integers`，无法出具核验结果。随后按清单 `files` 字段逐项复核相对路径、大小和 SHA-256：236 项通过；816 项缺失；已存在项没有大小或哈希不一致。缺失分布：`01_ORIGINAL_BASELINE\FROZEN_REPOSITORY` 746 项、`01_ORIGINAL_BASELINE\PRIOR_G0_AUDIT` 69 项、`01_ORIGINAL_BASELINE\RAW_SOURCE` 1 项。全部 816 个**绝对路径**见 `E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改\00_PROJECT_CONTROL\MIGRATION\NEW_PC_MISSING_FILES_CN.txt`。关键缺项包括 `E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改\01_ORIGINAL_BASELINE\RAW_SOURCE\PanBorneo_TomTom_Cleaned_Experiment_Package.zip`，以及同工程 `01_ORIGINAL_BASELINE\FROZEN_REPOSITORY` 下冻结特征、manifest、预测、权重等全部文件。不能写“解压工程数据完整”。ZIP 已验证包含这些路径；可仅从**该准确 ZIP**补全，随后修复核验脚本并重跑。旧 Python 依赖未迁移属预期，不计为研究文件缺失。

现有 `MIGRATION\PROMPTS` 下 Prompt 01、02、03 均存在且通过清单哈希；G0/G1 协议、验收锁、成果 ZIP、E01–E03 代码和派生数据、G2 草稿代码、SOURCE_GATE 日志/差异 CSV、E07 GIS 来源文件均存在且通过清单哈希。G1 锁定状态为 `CONDITIONAL_PASS`，不是 G2 通过。只读格式检查：`hourly_analysis.parquet` 100878 行×36 列；`aligned_predictions.parquet` 552882 行×12 列；G2 缓存 manifest 50269 行×19 列，`history_indices.npy` 为 (50269,24) int32，`scaled.npy` 为 (100878,13) float32；与 SOURCE_GATE 记录的 50269 样本、24 小时、13 特征相符。原始 FCD 和冻结仓库在落地目录缺失，无法对其内部数组或 CSV 做本机只读形状复核。E07 OSM 抓取记录为 1,971,117 字节，已有坐标与 acquisition manifest；当前道路快照不能证明历史时段道路状态。商业 FCD 仅限作者本机受控使用，不得公开上传。

## 2. 新电脑环境

Windows 10 专业工作站版 10.0.19045；Intel Xeon W-11855M，6 核/12 线程；物理内存约 63.2 GiB，检查时空闲约 49.9 GiB；E 盘空闲约 410.9 GiB。NVIDIA RTX A3000 Laptop GPU，6 GiB 显存，NVIDIA 驱动 596.72。`py` 为 Python 3.14.3；`python` 命令指向 WindowsApps 别名且本次未成功执行。当前 `py` 环境：NumPy 2.5.0、pandas 2.3.3、scikit-learn 1.9.1、PyArrow 25.0.0；XGBoost 和 PyTorch 未安装，故当前 PyTorch **不能识别或使用 GPU**。工程 `00_PROJECT_CONTROL\G2_torch` 有旧 CPU 版 torch 文件，不作为新电脑可用 GPU 环境。未进行 GPU 训练测速。

## 3. G2 静态审查与启动判定

Prompt 03 的核心上限 534 执行单元；三项条件性实验加总上限 648，不能全视为必做。独立新实现的匹配基准另有最多 108 单元（已做的应扣除）；必要时 24 小时窗口匹配基准最多另加 24。单元包括确定性基准，不全是模型拟合。已有：G0/G1 验收证据、E01–E03 派生数据、G2 数据与模型草稿、时间语义协议、SOURCE_GATE 样本/目标/特征诊断；未有 G2 正式结果。`source_gate.py` 在拟合前因特征差异退出，六次门槛训练均未完成。

差异仅集中于 `hours_since_last_observation`：标准化后最大差 203.490524，其余 12 特征约为浮点精度差。`data_engine.py` 当前按节点顺序在每个缺测小时把 age 加一并封顶 168，起值 168；这与冻结特征的确切起始、截断、观测事件定义尚未对照确认，**原因尚未证实**。修复须先从冻结仓库读取原特征生成口径/代码及若干逐小时样本，对比原值、标准化均值方差、首观测前/长缺测段/观测当小时；再仅修正该字段。更新 `revision_data_v1` 缓存版本，废弃旧 `ready.json` 指向的缓存，重建受影响缓存；逐样本复核 50269 键、目标、13 特征及时间边界，再运行 SOURCE_GATE 六次模型门槛，检查日志、预测签名与状态。未经此步骤不得宣称通过。

静态代码检查：`data_engine.py` 定义 fold 内训练区间插补、H1/H3/H6 目标、决策时点和分割边界；`models.py` 提供模型实现；`source_gate.py` 含六模型执行及状态输出。但这些代码未在本机端到端验证。`g2_common.py` 在冻结库缺失时会回退旧 D 盘路径，协议还记录 CPU 设备、10 个 XGBoost 线程及 2 个 torch 线程；迁移后必须只使用 E 盘绝对来源、重审 GPU/线程策略且冻结新协议。当前目录没有可执行的 E04–E07 批量编排入口、完整运行矩阵/预算扣账、跨阶段结果登记和验收打包实现；仅有数据引擎、模型、门槛与 GIS 准备草稿。断点续跑目前只见数据缓存 `ready.json`，模型级幂等、失败恢复、完整预测和权重登记尚未验证。E04 依赖门槛、配置与支持检查；E05 依赖同实现匹配基准和新 manifest；E06 依赖 Fold 1 验证选参与冻结后跨 fold/seed 执行；E07 邻接与空间实验依赖 GIS 来源核实，无法核实则延期空间条件项。所有阶段还需日志、指标与样本支持核验、失败恢复和最终打包。时间边界记录在协议中为小时结束后决策；实时数据到达延迟无证据，不能作实时运营主张。

逐项判定：

| 条件 | 当前判定 |
|---|---|
| 迁移数据完整 | **ZIP 完整；落地工程不完整**，缺 816 项 |
| 新电脑环境就绪 | **否**，缺 XGBoost、PyTorch/GPU 验证，Python 3.14 兼容性待验证 |
| 可开始修复并重做 SOURCE_GATE | **可以在补全 816 项并建立环境后开始**；现状无法运行冻结对照 |
| SOURCE_GATE 已实际通过 | **否**，状态 `BLOCKED`，六模型未拟合 |
| 可开始 G2 正式批量训练 | **否**；须 SOURCE_GATE 实际通过且实验编排、登记和恢复机制经检查 |

解除顺序：从指定 ZIP 补齐 `01_ORIGINAL_BASELINE` → 修复清单脚本并使 1052 项全通过 → 配置兼容依赖和 GPU 检查 → 查明并修复 age 特征、升级缓存版本 → 逐样本复核与六模型 SOURCE_GATE → 完成 E04–E07 编排、预算和恢复/验收机制 → 才启动正式训练。本轮未执行这些修复或训练。

## 4. 初步耗时（无本机拟合测速）

以下是以 6 核/12 线程、6 GiB GPU、约 5 万个 F1H1 门槛样本、最高 534 核心执行单元估算的**规划范围**；折算不等于 534 次 GRU 训练。假设训练集规模、fold/horizon 分布、GPU 适配、磁盘吞吐及散热正常，且单元从秒级确定性基准到分钟/小时级学习模型不等。机器时间为累计运行时间，人工时间为必要审查，部分可并行；总历时含串行依赖和修复返工。

| 阶段 | 机器时间 | 人工检查 | 预计历时 |
|---|---:|---:|---:|
| 环境配置、ZIP 补全及 1052 项复核 | 0.5–3 小时 | 1–3 小时 | 2–6 小时 |
| 特征定位/修复、缓存重建、六次 SOURCE_GATE | 1–8 小时 | 3–8 小时 | 0.5–2 天 |
| E04 核心敏感性 | 4–24 小时 | 2–5 小时 | 1–3 天 |
| E05 核心消融 | 3–18 小时 | 2–5 小时 | 1–3 天 |
| E06 核心有限选参及公平性 | 10–60 小时 | 3–8 小时 | 2–7 天 |
| E07 资料核实/运营证据（核心） | 1–8 小时 | 3–8 小时 | 1–3 天 |
| G2 汇总核验、受控打包 | 1–4 小时 | 3–8 小时 | 0.5–2 天 |

核心阶段按串行关键路径粗估约 **1–3 周**，包含尚缺编排的实现与人工核验；不是实测承诺。条件性实验仅在 Prompt 03 的样本支持、科学必要性、GIS 邻接有效性和资源预算满足时追加，约 0.5–5 天，不能自动并入核心总量。最大不确定性：冻结特征 age 口径、Python 3.14 与依赖兼容性、6 GiB 显存限制、GRU/XGBoost 每单元实测速率、各 fold/H 的样本支持、热降频与 E07 历史道路可核实性。SOURCE_GATE 通过后记录六模型实测用时，再用真实执行矩阵更新估算。

## 5. 下一步可直接执行的 Prompt 草案（下一轮使用）

> 仅在 `E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改` 工作。从已验证的 `APIN_PRIVATE_NewPC_Transfer_20261125.zip` 只补全清单缺失的 816 项，不混用其他 ZIP；修复 `verify_transfer.py` 读取 `files`，逐项完成 1052 项大小与 SHA-256 复核。建立新电脑兼容 Python 环境并验证 PyTorch GPU。只读对照冻结库的 age 特征口径，局部修复 `data_engine.py`，更新缓存版本后重建受影响缓存并逐样本复核。通过后执行六次 SOURCE_GATE，保留日志与状态；若失败立即停止，报告差异。SOURCE_GATE 实际通过前不得启动 E04–E07 正式批量训练。所有新输出限 E 盘上述工程；商业 FCD 不得公开上传。

本轮未启动 G2 正式训练、未批量执行 E04–E07、未重算 G0/G1，也未生成正式 G2 权重或预测。
