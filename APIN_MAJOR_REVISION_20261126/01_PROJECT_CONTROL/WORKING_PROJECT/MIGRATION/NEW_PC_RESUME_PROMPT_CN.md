# 新电脑续跑指令：Applied Intelligence G2

你是接续本工程的科研工程师。先读取本目录的README_TRANSFER_CN.md、PROMPTS/PROMPT_03_G2_ORIGINAL.txt，再按Prompt03原授权完成SOURCE_GATE、E04–E06和E07准备。保持研究主线和最小充分实验，不停留在计划。

## 当前用户的最新指令（优先级最高）

旧电脑配置低，作者要求停止在旧电脑上训练，将完整文件及Prompt迁至新电脑完成。旧电脑的CPU、GPU、驱动和耗时不能作为新电脑训练规模、模型能力或实验必要性的依据。

本次迁移不等于G2已完成。当前没有任何新模型完成拟合，SOURCE_GATE六模型训练尚未启动；新实现停在特征验证阶段。不得声称已经获得E04–E07结果。

## 唯一工作与输出根目录

默认恢复到：D:\Desktop\大修_Applied Intelligence_2026112_论文修改

严格保留目录名中的2026112。若新电脑没有D盘，由作者指定一个新的唯一根目录后再运行；不要在无关研究目录写正式结果。所有代码基于自身文件位置确定项目根目录。不得改动任何冻结原数据或G0/G1历史文件。

先验证迁移包。使用本目录verify_transfer.py，对包内清单做一次迁移完整性检查；这是传输校验，不是重启G0/G1科学审计。随后运行relocate_project.py，仅更新G2运行缓存中的绝对路径，不修改G0/G1证据及其哈希。

原冻结仓库随包位于01_ORIGINAL_BASELINE/FROZEN_REPOSITORY；原始83天CSV及cleaned/节点表归档位于01_ORIGINAL_BASELINE/RAW_SOURCE/PanBorneo_TomTom_Cleaned_Experiment_Package.zip。旧绝对路径仍保存在历史报告中，作为来源记录，不代表新电脑必须存在旧路径。

## 直接继承的已验收成果

- G0、G1为CONDITIONAL_PASS。
- E01–E03已实际计算并验收，全部保留，不整体重跑。
- 原Table7是方法B，Equation12是方法A；主要分析固定方法A。
- XGB对SeasonalHA三时域日均配对区间均跨零，不以取得显著或维持模型第一为目标。
- 4/4 H6所有fold验证为空，H3验证总计仅8；不得强行全六模型三时域训练。
- Free-flow baseline已完成，直接复用。
- 97.30%不再追查，后续删除或用可复算指标替代。

## SOURCE_GATE的已知具体问题：必须先修复

旧电脑运行source_gate.py时仅进行了数据特征检查，尚未进入六模型拟合。关键记录：

04_EXPERIMENTS/SOURCE_GATE/data_feature_time_checks.json
04_EXPERIMENTS/SOURCE_GATE/feature_contract_diagnostic.csv
04_EXPERIMENTS/SOURCE_GATE/status.json

样本主键集合对应；y_true最大差0；静态节点特征最大差0。13个序列特征中，12项与冻结X_sequence对应至约1e-6浮点精度；hours_since_last_observation差异约203.49个标准化单位。

具体优先检查03_CODE/E04_E07_REVISION/data_engine.py的年龄初始状态：当前从168开始，而历史特征的“节点尚未出现首条有效观测”规则可能按网格累计小时再截断168。不要直接凭此猜测修改。应以冻结X_sequence、fold_train_parameters.json及manifest.history_row_ids反标准化核实这一项的真实初始化，再做最小修正。不要重算全部E01–E03。

修正时保留失败证据，提升独立实现/预处理版本，使用新的缓存键或共享特征目录，禁止误复用旧的有问题特征缓存。原数据、原特征和原配置不改。

修正后按Prompt03完成Fold1/H1/seed42六模型SOURCE_GATE。通过后才创建G2_Training_Protocol.yaml并正式训练。

## 已获得的GRU架构证据与尚未证实事项

安全weights_only读取原GRU_F1_H1_S42.pt后确认：单层GRU，输入13维、hidden64；head为LayerNorm64后Linear1。检查点还包含y_mean、y_std、best_epoch、best_validation_mae和seed。

新代码已按该架构实现。原loss、优化器、shuffle、初始化微版本仍未由原源码证明；当前新实现选用标准化目标上的MSE、AdamW、种子化逐epoch shuffle，必须明确作为返修独立实现假设。不得称恢复了原始Phase2A1源码。

SOURCE_GATE_Protocol.yaml是旧电脑冻结的门槛记录；如果修正具体错误需要新版本，保留旧文件及变更说明。不能为了匹配历史平均MAE而调参数或保留泄漏。

## 新电脑环境与训练执行

依赖安装在本工程的受控虚拟环境或子目录。requirements_recorded_old_pc.txt记录旧电脑实际版本；不是要求新电脑沿用旧CPU设置。PyTorch应按新电脑GPU、驱动及官方兼容矩阵安装合适构建，记录真实版本及设备。

当前models.py按旧电脑使用CPU、2线程写成，尚未做新机器GPU适配。新电脑可在训练前将device/线程设为环境参数，在所有配对条件间保持一致并冻结；将张量、模型和推理正确放在选定设备上。不要将这个硬件适配解释为算法性能改进，不改变batch256、30epochs、patience5等科学训练预算来迎合硬件。

新代码目前包含数据引擎、模型、唯一运行ID、断点复用、门槛验证和小范围GIS获取；完整E04–E06调度、训练后比较统计、G2汇总交付仍须按Prompt03继续实现。不要把这些未实现部分当成已完成的自动训练流水线。

## 本轮预算必须遵守Prompt03，覆盖G1旧建议

核心执行上限534（含门槛6）。条件项合计上限114：4/4 H1最多36、共同样本反事实最多24、唯一轻量邻节点模型最多54。合计648不代表全部必须执行。

独立新实现确需匹配基准时，完整6模型×18任务×seed42总上限108，门槛已完成的相同运行必须扣除；12/24/48公平支持所需匹配24h基准额外最多24，分别记账。

E06参数搜索仅用最早Fold1的验证集：3模型×3时域×3候选×seed42最多27；选中配置沿用Fold2–6最多45；选中XGB/GRU补seed2026/3407最多72；合计144，不能沿用G1旧234方案。

所有完全相同的实现、条件、模型、fold、时域、seed、配置、train/val/test manifest、schema和目标，直接REUSED_RUN。配对比较用同一新实现的匹配基准，不能将新实现和原历史实现差值当成单因素效应。

## E07已有进展及剩余工作

已通过小范围Overpass获取研究节点边界附近的OSM主要道路数据，位于02_DATA/02_EXTERNAL_DATA/E07_GIS/osm_corridor_overpass.json；来源、查询范围和许可记录见acquisition_manifest.json。尚未完成节点道路匹配、沿路距离、累计里程或真实邻接验收。

不得仅按N001–N051假设上下游邻接。只有真实空间依赖通过检查后才允许条件性NEIGHBOR_AWARE_GRU；否则DEFERRED_SPATIAL_DEPENDENCY，非空间训练继续。

官方日历目前只有检索到的入口，未完成本地存档与适用性核对。可继续从Sarawak官方日历、马来西亚内阁官方节假日表、JAKIM/e-Solat和马来西亚官方广播公告核实。春节为公共假日与斋月开始属于不同类别，不能直接声称节日导致误差。

本阶段不下载任何外部交通速度数据，不执行E08，不改正文、不制作最终投稿图件、不写正式回复。G2完成后按Prompt03输出8个核心文件与APIN_G2_E04_E07_Results_实际完成日期.zip，统一验收后停止。

完整迁移包含受限商业原始及逐样本资料，仅供作者新电脑受控使用。G2对外成果ZIP必须另行筛选，不能直接上传本迁移包。
