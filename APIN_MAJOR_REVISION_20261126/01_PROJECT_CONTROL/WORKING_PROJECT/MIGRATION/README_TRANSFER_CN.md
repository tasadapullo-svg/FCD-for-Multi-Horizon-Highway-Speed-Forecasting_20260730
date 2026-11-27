# Applied Intelligence：作者新电脑完整迁移包

这是受控迁移包，不是已完成的G2实验结果包。作者已要求旧电脑停止训练。

## 新电脑操作顺序

1. 将压缩包复制至新电脑，优先用7-Zip或支持长路径的解压工具解压。默认项目根目录为D:\Desktop\大修_Applied Intelligence_2026112_论文修改；保留2026112。
2. 将项目根目录作为新Codex工作目录。
3. 读取并执行00_PROJECT_CONTROL/MIGRATION/NEW_PC_RESUME_PROMPT_CN.md。原Prompt03也完整保存在同目录PROMPTS子目录。
4. 用新电脑可用的Python运行verify_transfer.py进行传输哈希校验，再运行relocate_project.py更新G2缓存路径。不要更改历史G0/G1证据。
5. 依新电脑真实硬件建立环境，再修复门槛中的具体特征差异。六模型SOURCE_GATE通过后继续正式实验。

## 包含的资料

- 当前工程中所有研究文件、G0/G1代码与交付、E01–E03已验收结果、本机受控中间层。
- 新G2实现草稿、具体门槛失败证据、环境记录、小范围OSM道路资料。
- 原冻结仓库完整文件（含正式配置、180预测、18manifest、冻结特征矩阵与原权重），置于01_ORIGINAL_BASELINE/FROZEN_REPOSITORY。
- 原商业FCD数据包（含83天原返回CSV、cleaned与节点表），置于01_ORIGINAL_BASELINE/RAW_SOURCE。
- 已使用的历史G0审计证据，置于01_ORIGINAL_BASELINE/PRIOR_G0_AUDIT。
- G0、Prompt02、Prompt03原指令与新电脑续跑Prompt。
- 文件SHA256清单、源路径映射和迁移校验工具。

未打包可重新安装的Python/Node依赖、node_modules目录联接和临时缓存。这些是旧电脑环境文件，不是研究资产；依赖版本单独记录。没有遗漏正式模型训练输入。

## 本机执行状态

已停止。没有新模型完成拟合，也没有正式E04–E06结果；SOURCE_GATE在特征核对时发现hours_since_last_observation不一致而停止。样本与目标及其他12特征已定位证据，不需要重启G0/G1。

新电脑必须明确区分“当前已验收的G1结果”“尚未通过的G2新实现”“未执行的训练”。不要将迁移交付当作G2验收通过。

## 数据使用限制

本迁移包含商业原始FCD、逐样本预测、特征和权重，仅用于作者自己的新电脑受控科研。不得上传公开GitHub或将完整迁移包用作公开论文附件。后续对外G2成果包必须排除这些受限明细。
