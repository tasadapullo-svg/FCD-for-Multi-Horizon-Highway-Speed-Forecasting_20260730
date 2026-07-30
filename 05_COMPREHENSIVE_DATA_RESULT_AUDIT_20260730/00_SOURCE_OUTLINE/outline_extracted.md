# Extracted AJSE Phase 2A outline

Source: `C:\Users\DELL\Desktop\AJSE_Phase2A_详细写作大纲_逻辑关键词实验详解版.docx`
SHA-256: `264699f1962b0060edcdc41c3812c59955030ae44c75240ca27b956468ac6e88`
Paragraphs: 262; tables: 61; images: 3

Arabian Journal for Science and Engineering（AJSE）

Phase 2A 详细写作大纲、实验回填蓝图与多子图规划

Provisional manuscript focus

Retrospective Rolling-Origin Evaluation of Sparse Floating-Car Data
for Multi-Horizon Traffic Speed Forecasting on a Data-Scarce Highway Corridor

### Table 1

用途：在最终实验完成前固定文章逻辑、证据等级、章节结构、图表架构和数据回填位置；实验结束后再进行整体一致性校验与投稿版本重写。

### Table 2

项目 | 当前定义
目标期刊 | Arabian Journal for Science and Engineering（AJSE，Springer Nature）
建议稿件类型 | Full-length Original Article / Research Article
研究主轴 | 稀疏商业FCD的数据完整性、严格因果处理、六折滚动来源评价与工程适用边界
当前证据状态 | Phase 2A-0 = BLOCKED；旧最终周已暴露，不能作为独立盲测
主要评价证据 | 六折回顾性滚动来源评价；最后一周仅作历史补充比较
编制日期 | 2026年7月29日
后续动作 | 待稳定数据快照和正式结果完成后，回填数值并执行全篇一致性审计

材料依据：前序项目对话、上传的 AJSE Phase 2A 文章说明、SCI 写作提示词框架，以及 2026-07-29 核验的 AJSE 官方投稿规范。

# 目录与使用方式

### Table 3

本修订版新增：①整篇论文从现实问题到工程结论的九步逻辑；②六个推荐关键词的逐项含义、选择依据和替换条件；③AJSE-A0至AJSE-A13实验的目的、输入、执行、输出、通过标准、论文位置和结论边界。

1. 历史对话与上传材料校验结论

2. AJSE 当前投稿规范及对原写作框架的修正

3. 文章定位、证据边界与题目方案

4. 研究问题、研究目标与贡献链

## 4.3 整篇文章的总体逻辑：这篇论文到底要证明什么

这篇文章不是先拿几个模型比一遍，然后宣布误差最低的模型最好。它真正要建立的是一条完整证据链：先证明原始商业FCD在时间和空间上被正确整理，再证明每个预测样本没有偷看未来，然后在多个连续时间段上公平比较模型，最后说明在什么数据质量和预测时距下结果可以使用、在什么条件下不应使用。换句话说，模型结果只是证据链中的一环，数据合同、时间切分和可复算审计同样是论文的核心结果。

### Table 4

全文一句话逻辑：先把“数据是否可信、样本是否公平、时间是否无泄漏”讲清楚，再回答“模型是否准确、结果是否稳定、工程上什么时候能用”。

### 4.3.1 为什么必须先讲数据，再讲模型

在数据稀缺走廊中，模型误差低并不自动等于模型可靠。若某些缺失时间戳被直接忽略、不同模型使用了不同样本、训练统计量混入验证期，或者最后一周已经被研究者反复查看，那么表面上很好的MAE也可能被高估。因此，本文的叙事顺序必须是“数据形成—样本形成—时间评价—模型结果—失效边界”，不能反过来。

先讲完整理论网格：让读者知道理论上应该有多少条记录，缺了多少条，缺失发生在哪里。

再讲数据资格规则：让读者知道哪些记录被保留、哪些被排除，以及排除是否在看结果之前确定。

再讲共同sample manifest：保证所有模型比较的是同一批节点、同一批预测起点和同一批目标。

再讲六折rolling-origin：保证模型只用过去预测未来，并检验结果是否依赖某一个星期。

最后才讲模型和工程意义：模型是否更准只是问题之一，还要看最差折、最差节点、低覆盖条件和长期时距是否失效。

### 4.3.2 从现实问题到论文结论的九步逻辑链

### Table 5

步骤 | 需要回答的问题 | 论文中的证据 | 大白话解释
1. 现实场景 | 为什么需要这项研究？ | 数据稀缺的长距离公路、固定检测设施有限、商业FCD可提供速度观测。 | 这条路上没有足够密集的地面传感器，所以管理者可能只能依赖平台速度数据。
2. 数据风险 | 商业FCD为什么不能直接拿来训练？ | 缺失、低confidence、节点掉线、时间戳不连续、历史期短。 | 平台有数据不等于每个点、每个时刻都有可靠数据。
3. 网格重建 | 理论上应有多少记录？ | node×15-min和node×hour完整理论网格、缺失标记与数据流失表。 | 先把所有应该出现的格子画出来，空格子才是真正的缺失。
4. 资格冻结 | 什么数据算有效？ | confidence、速度范围、provider status策略、2/4主聚合、H6标签规则。 | 提前写清楚“什么样的数据能进考场”，不能看到成绩后再改门槛。
5. 样本统一 | 模型是否比较同一批题目？ | 统一sample_id、history和target边界、共同样本评价。 | 所有模型必须做同一套试卷，不能一个模型挑容易题，另一个模型做全部题。
6. 时间评价 | 模型是否偷看未来？ | 六折rolling-origin、purge、fold-wise scaler/imputer/HA。 | 每一折都只能用当时已经发生的数据，未来信息不能进入训练。
7. 性能与稳定性 | 模型在不同时间和时距是否都有效？ | H1/H3/H6指标、每折结果、最差折、排名变化。 | 不能只看平均分，还要看有没有某一周突然失灵。
8. 可靠性边界 | 什么条件下误差变大？ | coverage、gap、confidence、节点、日期和交通状态分层。 | 告诉管理者什么情况下可以相信预测，什么情况下要谨慎。
9. 工程结论 | 研究最终能给出什么建议？ | 精度、稳定性、数据要求、模型复杂度和可复现性综合判断。 | 最终不是宣布冠军，而是给出一套可实施、可审计的使用条件。

### 4.3.3 各章节在逻辑链中的职责

### Table 6

章节 | 主要职责 | 应该写什么 | 不应该写什么
Introduction | 把现实问题收缩为可研究的问题。 | 数据稀缺走廊、FCD机会与风险、现有评价不足、本文目标和贡献。 | 不要提前写模型排名或未经最终实验确认的结果。
Related Work | 证明研究空白具体存在。 | FCD预测、缺失/短历史、时间序列评价、数据泄漏与复现。 | 不要按模型名称罗列文献，也不要把“文献少”当作唯一空白。
Study Area and Data | 说明数据从哪里来、代表什么。 | 走廊、节点、时间范围、变量、许可、平台数据边界。 | 不要把平台速度说成全部车辆的真实交通流。
Methodology | 让其他人能够重复整个证据形成过程。 | 网格、资格、聚合、目标、fold、manifest、模型、指标、统计与审计。 | 不要在方法中提前夸大模型效果。
Results | 按RQ报告事实。 | 样本形成、主benchmark、跨折稳定性、质量分层、统计和敏感性。 | 不要在每段中重复全部表格数值，也不要过度解释原因。
Discussion | 解释结果为什么重要以及何时成立。 | 与文献比较、可能机制、工程含义、局限和未来研究。 | 不要把相关性写成因果，不要重新抄Results。
Conclusion | 压缩成可被引用的最终判断。 | 在何种协议和条件下FCD可用、最可靠时距、失效边界和下一步。 | 不要加入正文没有的新结果或普遍化结论。

### 4.3.4 读者最后应该得到的五个“大白话答案”

这些商业FCD究竟有多少能用，不能用的数据主要坏在哪里？

在完全相同的样本和严格时间切分下，简单模型、树模型和轻量序列模型谁更准、谁更稳定？

1、3、6小时预测中，哪个时距最可靠，误差从哪个时距开始明显增加？

当coverage低、连续缺失长或某些节点质量较差时，预测会退化到什么程度？

实际部署时需要满足哪些最低数据条件，哪些结果只能视为历史开发比较而不能视为独立验证？

## 4.4 Keywords：关键词为什么这样选

AJSE通常要求4–6个关键词。关键词不是把标题拆成几个词，也不是把所有模型名称都放进去。它们的作用是让数据库和目标读者准确找到文章，因此应同时覆盖“数据来源、预测任务、评价方法、数据问题和应用场景”。本文建议先使用6个关键词，最终可根据正式结果删减或替换其中1个。

### Table 7

推荐关键词：Floating-car data; Traffic speed forecasting; Rolling-origin evaluation; Data reliability; Sparse traffic observations; Highway corridor

### Table 8

英文关键词 | 中文和大白话含义 | 为什么放入本文 | 使用边界与注意事项
Floating-car data (FCD) | 浮动车数据。车辆或导航平台在道路上形成的速度/旅行时间类观测。 | 这是本文最核心的数据来源，也是检索本文的首要入口。 | 首次出现要给全称和缩写；不要称为完整车辆轨迹，除非确实拥有轨迹级数据。
Traffic speed forecasting | 交通速度预测。利用过去信息估计未来速度。 | 明确论文的任务是预测速度，不是交通流量、事故检测或拥堵分类。 | 正文应统一写speed forecasting；目标若是未来窗口平均速度，要在方法中明确。
Rolling-origin evaluation | 滚动来源评价。训练窗口在时间上向前推进，每次只用过去预测后续连续时段。 | 这是本文区别于随机切分和单一测试周的关键评价设计。 | 不要与普通随机K-fold混用；每一折的预处理和模型拟合都要独立。
Data reliability | 数据可靠性。关注coverage、confidence、缺失、连续断档及其对可用性的影响。 | 对应本文工程贡献：不仅问预测准不准，还问数据质量差时还能不能用。 | 如果最终没有完成质量分层分析，应替换为Reproducible evaluation或Multi-horizon forecasting。
Sparse traffic observations | 稀疏交通观测。并非指完全没有数据，而是时间/节点覆盖不均、有效历史短或连续缺失。 | 准确概括研究场景，比泛泛的big data或artificial intelligence更有区分度。 | 正文需要给出“稀疏”的操作性定义，例如有效槽位、覆盖率或gap长度。
Highway corridor | 公路走廊。强调研究对象是按物理顺序排列的长距离道路节点。 | 帮助交通工程读者识别应用场景，并区分城市路网级研究。 | 若道路分类最终不能严格称为highway，可改为interurban road corridor或regional road corridor。

### 4.4.1 关键词的替换规则

若正式结果的最大亮点是H1/H3/H6差异，可用“Multi-horizon forecasting”替换“Highway corridor”。

若主要贡献更偏复现协议而不是质量分层，可用“Reproducible evaluation”替换“Data reliability”。

若最终只保留HA、Persistence和XGBoost，不建议把XGBoost或Machine learning作为核心关键词；模型不是本文的主要创新。

不要同时使用Sparse FCD、Data-scarce、Missing data三个近义关键词，占用有限名额。正文可以解释三者差异，关键词保留最具检索价值的一个。

最终关键词必须在Abstract和Introduction中自然出现，但不应为了关键词密度机械重复。

### 4.4.2 关键词、标题和摘要的一致性检查

### Table 9

检查项 | 通过标准
数据来源一致 | 标题/摘要写commercial FCD时，Methods必须说明数据提供商、粒度和字段边界。
任务一致 | 关键词写traffic speed forecasting时，目标变量、时间窗口和单位必须清楚。
评价一致 | 关键词写rolling-origin时，正文必须报告折数、边界、purge和fold-wise拟合。
可靠性一致 | 关键词写data reliability时，Results至少包含一种质量分层或失效边界分析。
场景一致 | 关键词写highway corridor时，研究区描述和地图必须支持该道路场景。

## 4.5 实验体系全景：每个实验为什么要做、做完能说明什么

为避免与旧文章中的E0–E6、P系列编号混淆，本大纲使用“AJSE-A0至AJSE-A13”作为写作层面的建议编号。它们不强制替换本地脚本名称；正式论文和补充材料中应建立“写作编号—脚本—配置—输出目录”的一一对照。实验不能只列模型和次数，而要说明每一步在证据链中解决什么风险。

### 4.5.1 三类实验的证据等级

### Table 10

类型 | 包含实验 | 作用 | 能否支撑主结论
主要证据 | A0、A1、A5、A7、A8、A11 | 证明数据稳定、样本公平、时间无泄漏、主模型性能和统计差异。 | 可以；正文结论必须优先依据这些结果。
稳健性/敏感性 | A2、A3、A4、A9、A10 | 检查规则或数据质量变化后，结论是否仍成立。 | 用于限定结论和增强可信度，不能取代主benchmark。
接口与补充证据 | A6、A12、A13 | 验证管线能运行，解释旧最终周，记录复现成本。 | 不能单独证明模型优越；通常放方法、补充材料或讨论。

### 4.5.2 为什么必须按这个顺序执行

1. 先停止写入并冻结快照，否则后面所有样本数、哈希和结果都可能变化。

2. 再重建完整网格和资格规则，否则不知道缺失发生在哪一步。

3. 再定义目标、fold和共同manifest，否则模型比较不公平或存在时间泄漏。

4. 先做冒烟实验，只验证接口、文件和指标是否正确，不对模型优劣下结论。

5. 主benchmark通过后，再做稳定性、质量分层、节点诊断和统计检验。

6. 最后才比较已暴露的旧最终周，并把它降级为历史补充证据。

7. 全部结果冻结后再写Abstract、Results、Discussion和Conclusion，避免先写结论后找数字。

### 4.5.3 建议的实验—研究问题—图表对应关系

### Table 11

实验 | 主要回答 | 主要输出 | 论文位置
A0–A4 | 数据能否形成合格、可追溯的预测样本？ | 快照、理论网格、资格流失、聚合和标签敏感性。 | Methods 4.1–4.4；Results 5.1；Fig.2；Tables 1–3。
A5–A8 | 模型是否在共同样本和六折时间评价中准确且稳定？ | manifest、泄漏审计、冒烟、正式benchmark、折间稳定性。 | Methods 4.5–4.9；Results 5.2–5.3；Figs.3–5；Tables 4–6。
A9–A11 | 预测在什么质量、节点和时间条件下失效？差异是否可靠？ | 质量分层、节点/日期诊断、配对统计和置信区间。 | Results 5.4–5.6；Figs.6–8；Tables 7–9。
A12–A13 | 旧最终周和复现成本应如何解释？ | 历史比较、运行清单、哈希、环境和效率。 | Results补充；Discussion；Supplementary Information。

### AJSE-A0 稳定快照与数据来源审计

### Table 12

项目 | 详细说明
研究目的 | 确认实验使用的是一个不会再变化的数据版本，并明确每个文件从哪里来。
大白话解释 | 先给数据“拍一张定妆照”。只要后台程序还在写文件，今天和明天得到的样本数就可能不同，任何结果都不能正式写入论文。
主要输入 | 原始FCD目录、中间数据目录、最终面板目录、运行日志、进程状态、文件修改时间。
执行要点 | 停止或等待所有写入任务结束；生成文件清单、大小、时间戳和SHA-256；记录快照时间；确认51节点、日期范围、时区和唯一键。
主要输出 | snapshot_manifest.csv、hashes.txt、process_check.txt、data_lineage.md。
通过标准 | 结果目录无活动写入；同一文件重复计算哈希一致；节点、时间和文件数与数据合同一致。
写入论文 | Methods中的Data sources and reproducibility；Supplementary中的provenance和checksum。
不能据此主张 | A0只证明数据版本稳定，不证明数据本身完整，也不证明模型准确。

### AJSE-A1 完整理论时间网格与数据流失审计

### Table 13

项目 | 详细说明
研究目的 | 计算理论上应该存在的node×15-min和node×hour记录，并区分真正缺失、低质量记录和聚合不足。
大白话解释 | 不能只数“现有文件里有多少行”，因为没有出现的时间戳本身就是信息。要先把所有应该出现的格子补出来，再看哪些格子是空的。
主要输入 | 冻结节点清单、开始/结束时间、15分钟频率、原始FCD唯一键。
执行要点 | 建立节点和时间的笛卡尔积；左连接原始记录；标记observed、timestamp-missing、duplicate、quality-ineligible和hourly-ineligible。
主要输出 | 完整网格、节点/日期覆盖率、数据流失漏斗、缺失热图、重复记录清单。
通过标准 | 理论行数可由公式复算；每一步行数守恒；无未解释的节点或时间；重复处理可追溯。
写入论文 | Methods 4.2；Results 5.1；Fig.2(a–d)；Table 2。
不能据此主张 | 覆盖率高不等于预测一定准确；网格审计只回答数据存在性和资格问题。

### AJSE-A2 数据资格规则冻结

### Table 14

项目 | 详细说明
研究目的 | 在看正式模型结果之前，固定confidence、速度范围、provider status和异常记录处理规则。
大白话解释 | 先写清楚“什么数据能进考场”。如果看完模型成绩再改confidence或速度上限，就有后验挑规则的嫌疑。
主要输入 | 原始字段分布、TomTom字段定义、道路工程常识、异常记录样例。
执行要点 | 记录主阈值和理由；对低confidence、负速度、极高速度、缺失状态分别定义保留/排除/仅标记策略；不得把缺失status伪造成normal。
主要输出 | data_contract.yaml、资格前后记录数、阈值敏感性配置和规则版本号。
通过标准 | 所有阈值在正式benchmark前冻结；代码与文档一致；任何排除都能追溯到具体规则。
写入论文 | Methods 4.3；Table 1；Supplementary Methods。
不能据此主张 | 本研究的confidence阈值不能宣称为适用于所有提供商和所有道路的普遍标准。

### AJSE-A3 小时聚合规则敏感性

### Table 15

项目 | 详细说明
研究目的 | 比较2/4、3/4和4/4有效15分钟槽位规则对样本量、速度统计和预测性能的影响。
大白话解释 | 一个小时有4个15分钟观测。要求至少2个、3个或4个才算有效，会在“样本多”和“数据更完整”之间形成不同取舍。
主要输入 | 通过A2资格的15分钟记录。
执行要点 | 主规则建议2/4；敏感性为3/4和4/4；聚合统计量先冻结为算术平均；必要时中位数仅作为补充。
主要输出 | 各规则下有效小时数、节点保留率、速度差异和主模型性能变化。
通过标准 | 三个规则使用相同日期、节点和资格字段；差异仅来自有效槽位门槛；样本流失可解释。
写入论文 | Methods 4.3；Results 5.1和5.6；Fig.7；Table 8。
不能据此主张 | 样本更多的2/4不一定最好，样本更严格的4/4也不自动更真实；需要结合稳定性解释。

### AJSE-A4 预测目标和标签有效性敏感性

### Table 16

项目 | 详细说明
研究目的 | 固定H1、H3、H6目标的时间定义，并检查H6采用5/6或6/6有效小时规则时结论是否变化。
大白话解释 | 必须说清楚“预测未来第6个小时”还是“预测未来6小时平均速度”。本文建议采用未来窗口平均速度，并明确窗口中允许缺几个小时。
主要输入 | 小时速度面板、预测起点、H={1,3,6}。
执行要点 | 定义target_start和target_end；H1/H3/H6按统一公式生成；主H6标签至少5/6有效，敏感性要求6/6；禁止目标跨fold边界。
主要输出 | 每个horizon的合格标签数、目标分布、5/6与6/6差异和边界样本清单。
通过标准 | 每个sample的目标窗口长度正确；无未来窗口越界；公式、代码、manifest和图表口径一致。
写入论文 | Methods 4.4；Table 3；敏感性放Results 5.6或SI。
不能据此主张 | 不同目标定义不可直接与其他论文数值横向比较，除非预测对象和窗口完全一致。

### AJSE-A5 共同Sample Manifest与全样本防泄漏审计

### Table 17

项目 | 详细说明
研究目的 | 为所有模型建立完全相同的预测样本清单，并逐样本检查历史、目标、fold和训练统计量边界。
大白话解释 | 所有模型必须做同一套试卷，而且每一道题都不能在输入中出现答案或未来提示。
主要输入 | 小时面板、历史窗口、目标窗口、六折边界、资格规则。
执行要点 | 生成唯一sample_id；记录node、origin、history_start/end、target_start/end、fold和质量字段；执行全部时间断言、train-only统计量检查和共同样本比对。
主要输出 | sample_manifest.parquet/csv、assertion_report.csv、common_sample_hash.txt、失败样本清单。
通过标准 | sample_id唯一；history_end<target_start；最长H6目标不跨验证边界；各模型正式评价sample集合一致；全部关键断言通过。
写入论文 | Methods 4.5、4.9；Fig.3；Table 4和Table 8。
不能据此主张 | 审计通过只说明设计无明显泄漏，不代表模型没有过拟合或数据没有测量误差。

### AJSE-A6 模型接口冒烟实验

### Table 18

项目 | 详细说明
研究目的 | 用少量样本或少量折验证HA、Persistence、XGBoost等模型的输入输出、指标和文件格式是否正确。
大白话解释 | 这一步相当于开机检查。目的是确认管道能跑、结果能复算，不是为了决定谁是最好模型。
主要输入 | A5生成的少量训练/验证样本、固定配置和随机种子。
执行要点 | 检查特征维度、目标对齐、预测行数、指标重算、NaN/Inf、文件schema和运行日志；不做正式模型结论。
主要输出 | smoke_predictions、smoke_metrics、schema_check、recompute_check。
通过标准 | 预测行数与manifest一致；独立重算指标一致；无未来字段；所有模型接口可复用。
写入论文 | 通常不作为Results；可在Methods或Supplementary说明质量控制。
不能据此主张 | 冒烟结果不能作为正式benchmark、模型排名或统计显著性证据。

### AJSE-A7 六折多时距正式Benchmark

### Table 19

项目 | 详细说明
研究目的 | 在共同样本上比较有限数量的基线和模型在H1、H3、H6上的精度。
大白话解释 | 这是文章的主比赛，但比赛规则已经由A0–A5提前固定。每个模型在六个连续时间段上都要接受检验。
主要输入 | 冻结manifest、六折配置、模型注册表、训练期特征和目标。
执行要点 | 每折独立拟合scaler/imputer/HA/模型；超参数只用训练/验证信息；报告MAE、RMSE、sMAPE、R²、Bias和N；模型建议控制在4–6种。
主要输出 | fold×model×horizon指标、逐样本预测、配置、日志、种子和运行时间。
通过标准 | 六折全部完成；共同样本数一致；指标可从预测文件重算；无失败折被静默删除；模型选择过程可追溯。
写入论文 | Results 5.2；Fig.4；Table 5。
不能据此主张 | 平均MAE最低不等于在所有折、节点和质量条件下都最好，也不等于复杂模型具有普遍优势。

### AJSE-A8 跨折稳定性与排名一致性

### Table 20

项目 | 详细说明
研究目的 | 判断模型优势是否跨时间稳定，还是被单个容易或困难的fold驱动。
大白话解释 | 不能只看六次考试的平均分，还要看哪一次最差、排名是否经常换、模型有没有突然失灵。
主要输入 | A7的每折指标和逐样本预测。
执行要点 | 计算fold均值、标准差、最差折、最佳/最差差距、胜率和排名；必要时报告rank correlation或Friedman整体比较。
主要输出 | fold分布图、排名热图、最差折表、模型胜率。
通过标准 | 每一折都被报告；不存在仅选择有利折的情况；平均性能与最差性能同时解释。
写入论文 | Results 5.3；Fig.5；Table 6。
不能据此主张 | 折间波动不能直接解释为季节效应，因为数据期短且可能同时受多种未观测因素影响。

### AJSE-A9 数据质量分层与可靠性边界

### Table 21

项目 | 详细说明
研究目的 | 检验coverage、confidence、连续缺失和历史有效数变化时，预测误差是否系统性增加。
大白话解释 | 回答“数据差到什么程度以后，模型开始不靠谱”。这是实际部署比单一平均MAE更需要的信息。
主要输入 | 逐样本预测误差和manifest中的质量字段。
执行要点 | 阈值优先预注册或按训练数据分位数确定；按相同sample配对或node-day汇总；报告每层N、误差和置信区间；避免样本极不平衡。
主要输出 | coverage/gap/confidence分层表、误差曲线、可用/谨慎/不建议区间。
通过标准 | 分层规则不使用测试误差后验挑选；每层样本足够；结论在多个fold或节点中有一致方向。
写入论文 | Results 5.4；Fig.6；Table 7；Discussion中的部署边界。
不能据此主张 | 观察到低coverage与高误差相关，不代表低coverage单独“造成”误差；只能使用关联性语言。

### AJSE-A10 节点、日期和交通状态诊断

### Table 22

项目 | 详细说明
研究目的 | 找出误差集中在哪些节点、日期、时段或速度/波动状态，并识别最差案例。
大白话解释 | 平均值可能把局部问题盖住。要看是不是某几个节点一直很差，或者某几天所有模型都失灵。
主要输入 | 逐样本预测、节点顺序、日期、小时、速度、波动和质量字段。
执行要点 | 生成node×horizon误差热图、daily error、weekday/weekend、低速/高波动分层；选择典型案例必须使用预先定义的规则。
主要输出 | 节点热图、日误差曲线、典型节点预测—观测图、最差样本清单。
通过标准 | 节点编号与地图一致；案例选择不只挑最漂亮结果；每个分层报告样本量。
写入论文 | Results 5.5；Figs.7–8；Supplementary完整节点结果。
不能据此主张 | 某节点误差高不能直接归因于道路几何、事故或天气，除非有对应数据和分析支持。

### AJSE-A11 配对统计、移动块Bootstrap与工程意义

### Table 23

项目 | 详细说明
研究目的 | 判断模型差异是否稳定、置信区间是否跨零，并区分统计显著与实际有用。
大白话解释 | 两个模型差0.01 km/h即使统计上显著，也可能没有工程价值；反过来，差异方向一致但样本相关性强时，普通t检验可能过于乐观。
主要输入 | 共同sample上的绝对误差/平方误差、node-day或day汇总、模型配对。
执行要点 | 优先按node-day或保留全节点的24小时移动块Bootstrap；多模型使用Friedman/配对Wilcoxon并进行Holm校正；同时报告ΔMAE、95%CI和效果大小。
主要输出 | 配对差异表、Bootstrap分布、校正后p值、工程阈值解释。
通过标准 | 比较使用共同样本；统计单位考虑时间/空间依赖；多重比较已校正；实际差值和CI完整报告。
写入论文 | Results 5.6；Table 9；Discussion解释“显著但很小”或“方向不稳定”。
不能据此主张 | p<0.05不等于模型具有重大工程优势；p≥0.05也不等于两个模型完全相同。

### AJSE-A12 已暴露最终周的历史补充比较

### Table 24

项目 | 详细说明
研究目的 | 透明展示2026-02-22至2026-02-28旧结果与六折主结论是否一致，但不把该周当独立盲测。
大白话解释 | 这周的数据还能看，但证据等级降低。它更像“以前开发时看过的一次历史考试”，不能再说是从未见过的最终考试。
主要输入 | 旧Phase 13/15预测文件、旧配置、当前六折模型结果和证据暴露清单。
执行要点 | 明确标注previously exposed；只做描述性或一致性比较；若与六折冲突，以六折为主；不得用该周重新选模型或阈值。
主要输出 | 旧周与rolling-origin结果对照、差异说明、证据等级声明。
通过标准 | 正文和图表不出现blind/unseen/external test；旧周不参与主模型选择；冲突被透明报告。
写入论文 | Results末段或Supplementary；Discussion中的研究过程限制。
不能据此主张 | 不能宣称独立外部验证、未见测试集或最终盲测成功。

### AJSE-A13 可复现性、运行效率与最终一致性审计

### Table 25

项目 | 详细说明
研究目的 | 证明数据、代码、配置、图表和正文中的数字可以互相追溯，并记录实际运行成本。
大白话解释 | 别人应该能从一个表格数字找到对应预测文件、配置和脚本，而不是只能相信作者手工复制的结果。
主要输入 | 所有配置、manifest、预测、指标、图表数据、环境版本、日志和稿件表格。
执行要点 | 建立claim–evidence matrix；重算所有表图；记录软件版本、硬件、运行时间和种子；检查图表—正文—补充材料数字一致。
主要输出 | release目录、README、environment文件、哈希、claim_evidence_matrix、final_audit_report。
通过标准 | 随机抽取或全量重算结果一致；正文数字能定位到文件；无API密钥/隐私泄漏；表图和正文无矛盾。
写入论文 | Software and reproducibility、Data/Code Availability、Supplementary和投稿前核对。
不能据此主张 | 代码公开不自动证明结果可推广；复现性与外部泛化是两件不同的事。

### 4.5.4 每个实验结束后应立即保存的最小结果包

### Table 26

类别 | 必须保存的文件 | 原因
配置 | 数据规则、fold、模型、超参数、随机种子和软件环境。 | 防止后续无法解释某个结果使用了哪套规则。
样本 | sample manifest、共同样本哈希、训练/验证边界。 | 证明模型比较公平且没有时间越界。
预测 | 包含sample_id、观测值、预测值、model、fold、horizon，不提前写入后验选择信息。 | 所有指标和统计都应能从逐样本预测重算。
指标 | fold级、horizon级、node级和质量分层结果，带N和单位。 | 防止只保留平均值而丢失稳定性信息。
审计 | 断言报告、失败样本、哈希和日志。 | 证明管线执行状态，而不是只展示最终图。
图表数据 | 每幅图对应的CSV/Parquet和生成脚本。 | 保证图和表不是手工修改出来的。

### 4.5.5 实验结果写入论文时的统一表达顺序

1. 先报告样本数量和适用范围，再报告性能数字。

2. 先报告六折总体趋势，再报告最佳、最差和异常折。

3. 先报告实际误差差值和置信区间，再报告p值。

4. 先说明结果在哪些条件下成立，再讨论可能原因。

5. 所有“better、improved、robust、reliable”后面都必须有明确的参照模型、指标、样本和证据。

6. 当不同实验结论冲突时，优先级为：冻结的主要六折证据 > 预注册稳健性 > 探索性分层 > 已暴露历史周。

5. 全文详细写作大纲（段落级）

6. 多子图总体设计与逐图面板规划

7. 主要表格与补充材料规划

8. 最终实验数据回填清单

9. 当前可写内容与必须等待内容

10. 实验结束后的整体校验流程

11. 审稿风险清单与预防性写法

12. 附录A. 可直接回填的英文句式骨架

13. 附录B. 最终交付文件和结果包目录建议

### Table 27

建议使用方式：先按第5章完成不依赖结果数值的正文；实验结束后按第8章收集结果包；再按第10章执行证据—图表—文本三向校验。

# 1. 历史对话与上传材料校验结论

本章把前序对话中已经形成的判断、当前仍在运行的实验、AJSE Phase 2A 的独立整改路线，以及两份上传材料中的写作要求统一到一个可执行版本。

### Table 28

问题 | 历史状态 | 校验后的统一结论 | 论文处理
文章主定位 | 不是“提出新深度学习结构”的模型论文。 | 以数据完整性、滚动评价、可审核性和工程适用边界为主。 | 保留
旧最终周 | 原拟作为2026-02-22至2026-02-28独立盲测。 | 已被旧Phase 13/15预测、比较、消融与解释暴露。 | 降级为 historical development comparison
主证据 | 单一最终周或原固定测试集。 | 改为六折回顾性 rolling-origin；各折独立拟合。 | 必须执行
原始数据是否还能使用 | 曾出现“为什么不能沿用原数据”的疑问。 | 可以沿用原始FCD；受影响的是证据独立性，不是原始观测本身的有效性。 | 明确声明证据等级
v2.2 P系列与AJSE Phase 2A | 两条工程路线并行。 | P系列结果不能自动转为AJSE正式结果，除非使用同一数据合同、manifest、fold和评价样本。 | 严格隔离
理论网格与实际样本 | 理论15分钟网格约406,368条；理论小时网格约101,592条。 | 实际有效数须由最终数据合同和manifest决定；不能用旧数量代替新审计。 | 结果回填
节点数量 | 当前研究设计为51个固定节点。 | 最终论文须以冻结节点manifest和哈希为准。 | 最终核验
confidence阈值 | 0.80被建议为主规则。 | 尚不能在结果后选择；须在正式benchmark前冻结，并做阈值/聚合敏感性。 | 待冻结
speed_max | Phase 2A-0阻塞项。 | 缺少可靠依据时不应任意删除高速度；先标记、审计，再冻结规则。 | 作者批准
provider_status | 原数据无此字段。 | 应明确“未提供，因此不作为资格条件”，不能伪造normal状态。 | 固定写法
文章边界 | 与CRG-TCN/可靠性感知模型文章存在潜在重叠。 | AJSE只保留有限模型benchmark和协议创新；复杂模型结构、广泛消融、24步直接预测留给另一篇。 | 必须去重

## 1.1 为什么原来的数据仍可沿用

可以沿用的部分：原始TomTom FCD、节点位置、时间戳、速度、confidence/coverage及其可审计派生变量。

不能沿用的证据标签：“untouched final test”“independent blind week”“external validation”等表述。

必须重算的部分：完整理论网格、资格规则后的小时数据、rolling-origin fold、共同sample manifest、训练期统计量、正式预测和配对统计。

核心原则：污染是研究过程中的信息暴露问题，不等同于原始数据损坏；解决办法是降低旧结果证据等级并重建主要评价协议。

## 1.2 当前文章应采用的证据层级

### Table 29

证据等级 | 内容 | 使用位置
Level A：主要证据 | 六折rolling-origin正式benchmark；共同样本；fold-wise独立拟合；全样本防泄漏审计 | 正文Results核心
Level B：稳健性证据 | 2/4、3/4、4/4聚合；H6标签规则；均值/中位数；coverage/gap分层 | 正文或SI
Level C：历史比较 | 已暴露最终周、旧Phase 13/15结果 | 仅补充，不用于“独立验证”
Level D：探索性证据 | 尚未预先冻结的模型、阈值或后验分组 | 明确标注exploratory

图A  本写作蓝图采用的数据合同—因果样本—滚动评价—工程解释证据链（用于规划，不是最终论文结果图）

# 2. AJSE 当前投稿规范及对原写作框架的修正

上传的“SCI 1区论文深度写作与润色提示词系统”适合作为通用写作检查表，但其中若干固定格式与AJSE官方要求不一致。正式写作应以AJSE作者指南为准。

### Table 30

事项 | AJSE核验要求 | 对本稿的执行
稿件范围 | AJSE-Engineering覆盖Civil、Computer Science and Engineering、Systems Engineering等；本研究可按交通/土木—系统工程交叉定位。 | 题目与摘要突出engineering evaluation，不写成纯算法竞赛。
稿件类型 | Research Article / Full-length Original Article。 | 采用完整研究论文结构。
摘要 | 150–250 words；需覆盖目的、方法、结果和结论。 | 删除“必须120–130词、10句话”的限制。
关键词 | 4–6个。 | 建议6个以内。
引用 | 正文使用方括号数字引用，参考文献按出现顺序编号。 | 不采用APA作者—年份格式。
标题层级 | 十进制编号，不超过三级。 | 正文最多如4.2.1，避免过碎。
正文格式 | LaTeX推荐iicol；Word也接受。 | 当前DOCX用于写作蓝图，最终可转Springer Nature LaTeX。
图件 | 多子图用(a)(b)(c)…；矢量优先EPS；照片/半色调TIFF；组合图至少600 dpi；图中文字8–12 pt。 | 不能把所有图机械固定为16:9。
图宽 | 按84 mm单栏或174 mm双栏设计，高度不超过234 mm。 | 大多数多子图建议174 mm双栏。
图题 | 图内不放完整标题/图注；caption写在正文文件中。 | 图内只保留panel label、轴、图例和必要注释。
声明 | 需有Statements and Declarations；至少包括Competing Interests，按情况加Funding、Data/Code Availability等。 | 投稿前单独检查。
审稿人建议 | 官方指南要求建议4名国际审稿人，来自不同机构/国家且无近期合作冲突。 | 投稿准备阶段建立候选清单。
出版模式 | Hybrid；可选择subscription route，不收APC。 | 符合用户偏好，但与文章写作无直接关系。

### Table 31

关键修正：多子图的正确约束是“最终版面可读、符合84/174 mm宽度、面板标注清楚、组合图600 dpi或矢量输出”，不是统一16:9。

## 2.1 建议的内部篇幅目标（非期刊硬性限制）

### Table 32

部分 | 建议篇幅 | 当前可完成程度
Title page + Abstract + Keywords | 250–350词（不含作者信息） | 最后完成
1 Introduction | 1,100–1,400词 | 现在可写80%
2 Related Work | 900–1,200词 | 现在可写70%，文献需最终核验
3 Study Area and Data | 900–1,200词 | 现在可写80%，数量待回填
4 Methodology | 2,000–2,600词 | 现在可写85%，参数待冻结
5 Results | 1,500–2,000词 | 等待正式结果
6 Discussion | 1,300–1,700词 | 等待结果后写
7 Conclusions | 300–450词 | 最后写
Statements and Declarations | 150–300词 | 投稿前确认
总正文工作目标 | 约8,000–10,000词 | 用于控制完整性，不是AJSE官方上限

# 3. 文章定位、证据边界与题目方案

## 3.1 一句话定位

### Table 33

在固定检测设施不足、历史样本较短且商业FCD覆盖不均的长距离高速走廊中，本研究建立完整时间网格、统一数据资格合同和六折滚动来源评价，以检验1、3和6小时速度预测的可用性、稳定性及失效边界。

## 3.2 推荐题目

### Table 34

优先级 | 英文题目 | 适用条件
首选 | Retrospective Rolling-Origin Evaluation of Sparse Floating-Car Data for Multi-Horizon Traffic Speed Forecasting on a Data-Scarce Highway Corridor | 最准确，避免过度模型创新承诺；突出证据重建。
备选A | A Reproducible Rolling-Origin Framework for Traffic Speed Forecasting Using Sparse Commercial FCD on a Data-Scarce Highway Corridor | 强化工程复现性。
备选B | Data-Reliability-Aware Evaluation of Sparse Floating-Car Data for Short-Term Highway Speed Forecasting | 更短，但“reliability-aware”需有充分分层证据。
结果后备选 | When Is Sparse Commercial FCD Sufficient for Multi-Horizon Highway Speed Forecasting? Evidence from a Retrospective Rolling-Origin Study | 问句式更醒目，但需最终结果形成明确适用边界。

## 3.3 中心论点与保守结论边界

### Table 35

类型 | 表述 | 证据要求/原因
可主张 | 严格的数据资格和时间评价协议能改变对模型稳定性与适用性的判断。 | 需要六折、敏感性和旧周对比支持。
可主张 | 稀疏FCD在部分时距和质量条件下可支持速度预测。 | 必须报告条件、误差和最差折。
可主张 | 简单基线或树模型在短历史数据中可能比复杂模型更稳定。 | 只有正式共同样本比较成立后才能写。
不可主张 | 最终周是完全独立盲测。 | 已被历史实验暴露。
不可主张 | 0.80 confidence或2/4规则具有普遍最优性。 | 仅是本研究冻结规则和敏感性对象。
不可主张 | 稀疏商业FCD可完全替代固定检测器。 | 缺少独立地面真值和跨地区验证。
不可主张 | 模型在所有高速走廊可泛化。 | 单走廊、约三个月数据。

## 3.4 与另一篇CRG-TCN文章的边界

### Table 36

文章 | 应保留内容 | 边界原则
AJSE Phase 2A | 数据合同、理论网格、统一manifest、六折评价、泄漏审计、有限benchmark、数据质量—误差关系 | 协议与工程证据
CRG-TCN/T1 | 模型结构、可靠性门控、多尺度/空间模块、24步直接预测、大规模模块消融、训练预算和冷启动 | 模型与算法贡献
可共享基础材料 | 研究区、原始FCD来源、节点背景 | 文字与图不得重复到构成实质性重叠；研究问题、目标、结果集必须不同

# 4. 研究问题、研究目标与贡献链

为避免六个独立RQ导致文章过碎，建议把原有六项问题压缩为四个主RQ，并在Results中设置子分析。

### Table 37

RQ | 研究问题 | 对应目标 | Results主线
RQ1 | 在完整理论时间网格和预先冻结的数据资格规则下，稀疏商业FCD能形成多少可用预测样本，且样本保留对聚合和标签规则有多敏感？ | 重建网格；比较2/4、3/4、4/4及H6标签资格。 | 数据资格与样本形成
RQ2 | 在共同样本和六折滚动来源评价下，HA、Persistence、Ridge/XGBoost及一个轻量序列模型在H1、H3、H6上的精度与时间稳定性如何？ | 完成正式benchmark；报告均值、标准差、最差折和排名稳定性。 | 预测性能与稳定性
RQ3 | coverage、confidence、连续缺失、节点位置和交通波动与预测误差之间存在什么可重复的关联？ | 按预先定义的质量/状态分层；估计配对误差差异和置信区间。 | 失效边界
RQ4 | 严格rolling-origin协议与单一已暴露历史周会否产生不同的模型判断或模型排序？ | 把旧最终周降级为历史补充；对比整体排名、误差和不确定性。 | 协议对结论的影响

## 4.1 贡献链

### Table 38

贡献类型 | 具体增加的内容 | 验证载体
数据贡献 | 从“只看已有记录”转为完整15分钟/小时理论网格，区分真正缺失、低质量记录和槽位不足。 | 理论网格及审计表
方法贡献 | 把资格规则、时间边界、共同sample manifest、fold-wise处理和全样本断言整合为可复算协议。 | 流程图、manifest、审计结果
实证贡献 | 用六个连续时间折评估多时距预测，而非依赖单一周。 | 每折性能、最差折、排名稳定性
工程贡献 | 识别在何种coverage、gap、节点或波动条件下误差显著上升。 | 分层结果和失败案例
研究规范贡献 | 明确披露历史测试周暴露并降低其证据等级。 | 方法与限制章节

## 4.2 不建议设置强因果假设

本研究是回顾性观察性预测评价，不具备因果识别设计。正文可使用“associated with”“corresponded to”“was observed under”等表达，不应写“low coverage caused error”或“confidence determined performance”。

# 5. 全文详细写作大纲（段落级）

## 5.0 Title Page, Abstract and Keywords

### Table 39

单元 | 写作内容 | 状态/限制
Title | 先用首选题目；结果结束后检查是否需要加入“reliability”或“reproducible”。 | 不含未被结果证明的best/novel/accurate。
Abstract sentence 1 | 工程背景：数据稀缺高速走廊依赖商业FCD。 | 现在可写。
Abstract sentence 2 | 问题：覆盖不均、短历史和单一测试期会削弱证据可信度。 | 现在可写。
Abstract sentence 3 | 方法：理论网格、资格规则、共同manifest、六折rolling-origin和全样本审计。 | 参数冻结后定稿。
Abstract sentence 4 | 结果：填入主模型、H1/H3/H6、折间稳定性和最差质量条件。 | 等待结果。
Abstract sentence 5 | 结论：稀疏FCD在明确边界内可用；复杂度与稳定性需共同考虑。 | 等待结果。
Keywords | Floating-car data; traffic speed forecasting; data-scarce highway; rolling-origin evaluation; data reliability; reproducibility | 最终保留4–6个。

## 5.1 Introduction

### Table 40

段落 | 核心任务 | 证据与写作约束
P1 宏观背景 | 长距离高速走廊需要连续运行状态信息，但固定检测设施部署和维护受成本、地形与覆盖制约。 | 交通工程背景文献；不要夸大Pan Borneo代表性。
P2 FCD机会 | 商业FCD提供高频、多点速度观测，适合补充数据稀缺环境。 | 说明平台数据是provider-reported observations，不是真实全体车辆流。
P3 数据问题 | 稀疏性不是单一缺失率：还包括未生成时间戳、低confidence、连续掉线、小时槽位不足和节点差异。 | 引出完整理论网格。
P4 评价问题 | 随机切分、单一测试期和模型各自删样本可产生乐观或不可比结果。 | 引出rolling-origin和共同manifest。
P5 现有研究不足 | 交通预测研究多聚焦模型精度，较少把数据资格、时间泄漏、折间稳定性和工程失效边界作为一个协议评价。 | 需近5年文献支持，不写“no study”。
P6 研究目的与RQ | 提出四个RQ，说明本文是回顾性评估，不是新网络结构竞赛。 | 可直接采用第4章。
P7 贡献与结构 | 列出数据、方法、实证和工程贡献；最后说明各章节。 | 贡献必须与Results一一对应。

## 5.2 Related Work

### Table 41

小节 | 写作任务 | 输出要求
2.1 FCD-based traffic forecasting | 按数据来源与任务组织：商业FCD/探针车、速度或流量、城市或高速、预测时距。 | 不要按LSTM/XGBoost逐篇罗列。
2.2 Forecasting under sparse and missing observations | 总结缺失处理、数据质量特征、短历史与低覆盖研究。 | 区分imputation performance与forecasting performance。
2.3 Time-series evaluation and leakage control | 滚动来源、purge、train-only transformations、common test samples、可复现性。 | 跨领域时间序列方法可引用，但须连接交通场景。
2.4 Synthesis and gap | 形成矩阵：已有研究解决了什么、未充分解决什么、本文如何回应。 | 最后一段直接导向四个RQ。

## 5.3 Study Area and Data

### Table 42

小节 | 应写内容 | 待最终核验
3.1 Study corridor | Pan Borneo Highway, Sarawak；走廊长度、节点分布、道路环境和选择原因。 | 长度与节点坐标以最终GIS/manifest为准；避免超出证据的“高速公路”等分类。
3.2 FCD acquisition | TomTom商业FCD；采集日期、15分钟频率、固定节点、API/存储流程。 | API密钥不公开；说明provider字段。
3.3 Raw variables | timestamp、node_id/segment_id、current_speed、confidence、coverage、free_flow_speed（如真实存在）。 | 最终data dictionary核验字段、单位、缺失率。
3.4 Theoretical observation universe | 83天×96×51理论15分钟网格；83×24×51理论小时网格。 | 实际日期端点和时区一经manifest确认后重算。
3.5 Data governance | 商业数据许可、共享限制、可公开的聚合数据、代码和manifest。 | Data Availability中保持一致。

## 5.4 Methodology

### Table 43

小节 | 应写内容 | 关键约束
4.1 Research design and evidence classification | 定量观察性案例研究；回顾性rolling-origin评价；旧最终周为previously exposed historical period。 | 必须在方法前部透明声明。
4.2 Time-grid reconstruction | 建立node×15-min完整笛卡尔网格；标记observed、missing timestamp、quality-ineligible。 | 报告每一步行数和唯一键。
4.3 Eligibility contract | confidence阈值、速度范围、重复值、provider_status缺失策略、时区和边界。 | 所有阈值在正式结果前冻结。
4.4 Hourly aggregation | 主规则2/4或最终批准规则；均值/中位数；生成valid_slots、coverage、gap特征。 | 主规则与敏感性规则分开。
4.5 Forecast sample definition | 历史窗口、forecast origin、H1/H3/H6目标、未来窗口平均、目标有效性。 | 明确点目标或窗口平均，全文不得混用。
4.6 Six rolling folds | 扩展训练窗口、连续验证窗口、最长H6 purge；每折重新拟合处理器和模型。 | 最终给出精确日期表。
4.7 Common sample manifest | sample_id、fold、node、history/target边界、valid counts、quality字段。 | 所有模型仅在同一eligible sample集合评价。
4.8 Models | HA、Persistence、Ridge或XGBoost、一个轻量序列模型；统一输入和训练预算。 | 控制4–6种，避免与CRG-TCN文章重叠。
4.9 Leakage and reproducibility audit | 时间断言、train-only scaler/imputation、禁止backfill/centered rolling、文件SHA-256、环境和随机种子。 | 至少20项全样本断言。
4.10 Metrics and statistical analysis | MAE主指标；RMSE、sMAPE、R²、Bias；node-day配对；移动块bootstrap、Wilcoxon/Friedman+Holm。 | 统计单位和block长度须预先固定。

### 5.4.1 方法公式清单

### Table 44

对象 | 推荐表达 | 说明
小时速度 | v_{n,h} = (1/m_{n,h}) Σ v_{n,q} | m满足资格阈值；说明是否加权。
未来窗口目标 | y_{n,t}^{(H)} = (1/k) Σ_{j=1}^{H} v_{n,t+j} | H=1,3,6；k为有效未来小时数。
MAE | (1/N) Σ |ŷ_i-y_i| | 主精度指标，单位km/h。
RMSE | sqrt[(1/N) Σ(ŷ_i-y_i)^2] | 强调大误差。
sMAPE | (100/N) Σ 2|ŷ_i-y_i|/(|y_i|+|ŷ_i|+ε) | 固定ε并说明。
R² | 1-Σ(y_i-ŷ_i)^2/Σ(y_i-ȳ)^2 | 仅在分母非零时报告。
Bias | (1/N) Σ(ŷ_i-y_i) | 正值=高估速度，负值=低估。
Coverage | eligible slots / theoretical slots | 需区分小时、历史窗和目标窗coverage。

图B  六折回顾性滚动来源评价示意；正式论文须用最终冻结日期替换示意边界

## 5.5 Results

### Table 45

小节 | 结果叙事 | 图表与约束
5.1 Data integrity and sample formation | 先报告理论网格、原始记录、去重、quality eligibility、小时聚合、history/target资格和最终样本数。 | Fig.2 + Tables 1–2；回答RQ1。
5.2 Main multi-horizon benchmark | 共同样本下按H1/H3/H6报告各模型MAE、RMSE、sMAPE、R²和Bias。 | Fig.4 + Table 5；先总体后时距。
5.3 Fold stability and ranking | 报告每折结果、均值±SD、最差折、模型胜率、排名变化。 | Fig.5 + Table 6；回答RQ2。
5.4 Reliability-stratified performance | coverage、confidence、gap、volatility、node、weekday/weekend或speed regime。 | Fig.6 + Table 7；分层阈值预先定义。
5.5 Sensitivity analyses | 2/4 vs 3/4 vs 4/4；H6 5/6 vs 6/6；均值/中位数；可选阈值敏感性。 | Fig.7 + Table 8；回答RQ1/RQ3。
5.6 Historical final-week comparison | 只比较六折结论与旧暴露周是否一致，不称external validation。 | Fig.8或SI；回答RQ4。

### 5.5.1 Results段落固定结构

1. 第一句给出该段的主要发现，不先堆数值。

2. 第二至三句报告支撑该发现的核心数值、置信区间和样本量。

3. 第四句指出跨折、跨时距或跨节点是否一致。

4. 最后一句只说明证据边界，不在Results中展开机制解释。

### Table 46

禁止写法：只按模型逐行复述表格；只报告平均MAE而不报告最差折；把未显著差异写成“improved”；忽略模型共同样本数。

## 5.6 Discussion

### Table 47

小节 | 讨论任务 | 写作限制
6.1 Main findings by research question | 用4个RQ组织，不重复全部数值。 | 每个RQ一段或一组段落。
6.2 Why protocol changes the evidence | 解释理论网格、共同样本和rolling-origin为何比单一测试周更可靠。 | 与RQ4连接；承认回顾性限制。
6.3 Model complexity under short and sparse histories | 解释简单模型/树模型/序列模型的稳定性差异。 | 只有正式结果支持后写；避免事后故事。
6.4 Data reliability and failure boundaries | 解释coverage、gap、confidence、波动与误差的关联。 | 使用may/could/was associated with。
6.5 Engineering implications | 给交通管理者：最低数据资格、可靠预测时距、监控告警、何时不应自动使用预测。 | 必须由结果形成明确边界。
6.6 Limitations | 单走廊、短时间、商业平台偏差、无固定检测器真值、provider_status缺失、最终周暴露、外部泛化不足。 | 每个限制说明影响及未来补救。

## 5.7 Conclusions

### Table 48

段落 | 内容 | 限制
段1 | 目的与方法：用一句话重申数据问题和rolling-origin设计。 | 不重复引言。
段2 | 主要结果：最可靠时距、稳定模型、质量失效边界。 | 仅填最关键数值或不填具体数值。
段3 | 工程意义：部署时同时检查精度、折间稳定性和数据资格。 | 不宣称替代固定传感器。
段4 | 限制与下一步：更长时间、跨走廊、独立传感器真值、前瞻性锁定测试。 | 保持简短。

## 5.8 Statements and Declarations

### Table 49

声明 | 准备内容
Funding | 填写真实项目/奖学金/无专项资助。
Competing Interests | 通常写作者声明无相关财务或非财务利益；需全体作者确认。
Author Contributions | 按CRediT或期刊接受格式，明确数据、软件、分析、写作和监督。
Data Availability | 商业FCD不可完全公开时，说明限制；公开代码、manifest、派生聚合数据或合成样例。
Code Availability | GitHub/Zenodo版本、release tag、DOI和commit hash。
Ethics | 若不涉及人/动物，说明not applicable；仍需核对平台数据许可。
AI assistance | 仅语言copy editing通常无需声明；若生成性参与实质内容，需按Springer政策处理并由作者负责。

# 6. 多子图总体设计与逐图面板规划

建议主文控制在6–8幅多子图。每幅图围绕一个研究问题组织，而不是把互不相关的小图机械拼接。多数多子图使用174 mm双栏宽度；单一简图可使用84 mm单栏宽度。

图C  推荐的主文多子图架构；最终可将部分敏感性和案例移入Supplementary Information

### Table 50

图 | 面板设计 | 回答问题 | 质量控制 | 当前状态
Fig. 1 Study area and observation design | (a) Malaysia–Sarawak定位；(b) Pan Borneo走廊与51节点；(c) 按里程排序的节点/间距；(d) 2025-12-08至2026-02-28采集时间线 | 研究场景、空间分析单位、节点顺序 | 地图比例尺、指北针、坐标系、节点编号；不在地图上堆过多文字 | 现在可生成框架；最终坐标核验后导出
Fig. 2 Data integrity and eligibility | (a) 理论网格与原始记录流；(b) daily×node coverage heatmap；(c) confidence分布；(d) valid slots分布；(e) missing-run length；(f) 数据筛选Sankey/flow counts | RQ1：数据完整性和样本资格 | 每个面板使用同一时间/节点定义；flow counts必须与表2一致 | 等待稳定快照
Fig. 3 Forecasting protocol and audit | (a) 总体流程；(b) 24h history和H1/H3/H6目标；(c) 六折rolling-origin；(d) H6 purge；(e) common manifest字段；(f) leakage audit gates | 方法可复现性 | 纯矢量；不包含结果；可先完成 | 现在可生成，日期后替换
Fig. 4 Main model performance | (a) H1 MAE；(b) H3 MAE；(c) H6 MAE；(d) RMSE；(e) Bias；(f) R²或sMAPE/模型排名 | RQ2：主benchmark | 显示fold点+均值/CI，不只画柱状均值；共同样本 | 等待正式结果
Fig. 5 Temporal stability | (a) model×fold MAE heatmap H1；(b) H3；(c) H6；(d) rank stability；(e) worst-fold penalty | RQ2：时间稳定性 | 颜色同时配数字或符号；报告fold样本量 | 等待正式结果
Fig. 6 Reliability–error relationships | (a) coverage strata；(b) confidence strata；(c) gap length；(d) volatility；(e) node-level spatial MAE；(f) error reliability surface/heatmap | RQ3：失效边界 | 分层阈值在看结果前冻结；同时报告样本量 | 等待正式结果
Fig. 7 Sensitivity and robustness | (a) 2/4、3/4、4/4样本量；(b) 各规则MAE；(c) H6 5/6 vs 6/6；(d) mean vs median aggregation；(e) 阈值敏感性；(f) ranking consistency | RQ1/RQ3：规则敏感性 | 主分析与敏感性结果不能混在同一数值列 | 等待正式结果
Fig. 8 Historical comparison and cases | (a) rolling-origin vs exposed-week ranking；(b) 差异分布；(c) 典型稳定节点时序；(d) 典型失败节点时序 | RQ4和工程解释 | 图题明确historical/previously exposed；不能使用blind/external | 等待正式结果

## 6.1 图件统一视觉规范

### Table 51

要素 | 执行标准
尺寸 | 单栏84 mm；双栏174 mm；高度≤234 mm。多子图优先双栏。
面板标记 | 左上角使用粗体(a)、(b)…；所有图统一位置和字号。
字体 | Arial/Helvetica；最终版8–12 pt；轴标题和图例大小尽量一致。
线宽 | 线图在最终尺寸下≥0.3 pt；关键线建议更清晰。
颜色 | RGB；即使转灰度仍可区分；结合线型、点型、纹理或直接标签。
分辨率 | 线稿优先EPS/PDF/SVG矢量；半色调≥300 dpi；组合图≥600 dpi；纯位图线稿≥1200 dpi。
图内文字 | 不放完整标题和长句；caption在稿件中解释所有panel。
统计表达 | 优先显示fold点、置信区间、样本量或分布；避免只有柱形均值。
输出文件 | Fig1.eps / Fig1.tif等规范命名；保留绘图代码和原始数据CSV。
可访问性 | 对比度≥4.5:1；不能只依赖颜色传达信息。

## 6.2 哪些图现在可以生成

### Table 52

类别 | 内容
可以现在生成 | Fig.3方法流程的(a)–(f)；Fig.1基础地图框架；所有结果图的空白模板、颜色/符号/面板布局。
需等稳定数据 | Fig.2所有审计数值；Fig.4–8所有模型和质量分层结果。
可先做但需替换 | 六折时间线、节点数量、日期、模型名称和阈值标签。
不建议用生成式图像 | 统计结果、地图、流程中的具体科学对象应由代码/矢量工具生成，保证可复算。

# 7. 主要表格与补充材料规划

### Table 53

编号 | 内容 | 位置 | 关键检查
Table 1 | Data fields, units, source, temporal resolution, role, missingness | Study Area and Data | 字段与单位最终核验
Table 2 | Data attrition from theoretical grid to eligible samples | Results 5.1 | 必须与Fig.2(f)完全一致
Table 3 | Six rolling-origin training, purge and validation boundaries | Methodology | 精确到时区和时间戳
Table 4 | Models, inputs, hyperparameters, tuning budget and seeds | Methodology | 公平比较与可复现
Table 5 | Primary performance by model and horizon, aggregated across folds | Results 5.2 | MAE主指标；同时样本量/CI
Table 6 | Fold-wise metrics, worst-fold performance and rank stability | Results 5.3 | 不只给均值
Table 7 | Performance by reliability and traffic strata | Results 5.4 | 每组样本量和阈值
Table 8 | Sensitivity analyses and model-ranking agreement | Results 5.5 | 主规则与替代规则
Table S1 | Node inventory and coverage statistics | SI | 51节点完整列表
Table S2 | Full leakage assertion checklist | SI | 断言、范围、结果、证据文件
Table S3 | Pairwise statistical comparisons with Holm adjustment | SI/主文压缩版 | 实际差值+CI+adjusted p
Table S4 | Software, package versions, hardware and runtime | SI | 环境锁定
Table S5 | Historical exposed-week comparison | SI | 明确证据等级

## 7.1 建议补充材料结构

Supplementary Methods：全部资格规则、伪代码、fold生成逻辑和断言定义。

Supplementary Figures：全部节点热图、完整预测时序、额外敏感性、残差诊断。

Supplementary Tables：节点inventory、模型超参数、全部fold×horizon结果、统计检验和文件哈希。

Reproducibility Package：配置文件、环境、manifest、脚本入口、README、输出schema和checksum。

不公开商业原始FCD时，提供脱敏/聚合样例和可运行的synthetic example。

# 8. 最终实验数据回填清单

实验结束后，不应直接把零散截图或汇总表粘进论文。应先形成稳定结果包，再按以下顺序回填。

### Table 54

包 | 必须提供 | 建议文件
A. 稳定快照 | 原始/中间/最终数据目录清单；运行结束时间；无写入进程；文件数量与SHA-256。 | snapshot_manifest.csv / hashes.txt
B. 数据合同 | 时区、日期、节点、唯一键、confidence、speed范围、provider_status策略、聚合和标签规则。 | data_contract.yaml
C. 数据审计 | 理论网格、原始行数、重复、缺失、quality-ineligible、小时有效数、最终sample数。 | data_audit_summary.csv
D. Fold定义 | 每折train/purge/validation起止；各horizon样本数；目标不越界证明。 | fold_manifest.csv
E. Common manifest | 全部sample_id及history/target时间、node、quality字段。 | sample_manifest.parquet
F. 模型配置 | 模型版本、特征、超参数、seed、训练预算、早停、硬件。 | model_registry.yaml
G. 预测文件 | 每个model×fold×horizon的y_true、y_pred、sample_id；不得混入旧结果。 | predictions/*.parquet
H. 指标结果 | 总体、折、节点、日、质量分层的MAE/RMSE/sMAPE/R²/Bias和N。 | metrics_long.csv
I. 统计结果 | paired differences、block bootstrap CI、Wilcoxon/Friedman、Holm校正、effect size。 | statistics/*.csv
J. 效率 | 训练时间、推理时间、参数量/模型大小、峰值显存或CPU/RAM。 | efficiency.csv
K. 审计证据 | 20+全样本断言、PASS/FAIL、失败行样例、日志。 | leakage_audit.json
L. 图形数据 | 每个panel对应的独立CSV/Parquet和绘图脚本。 | figure_data/FigX_panelY.csv

## 8.1 结果回填时必须回答的判定问题

1. 正式benchmark是否使用了完全相同的sample_id集合？若不同，差异是否仅来自模型无法处理的输入，且是否另做common-sample分析？

2. 六个fold的训练、purge和验证边界是否满足最长H6目标不跨界？

3. 所有scaler、imputer、HA统计量和类别编码是否只使用各折训练期？

4. 主规则是在查看正式结果前冻结，还是后验选择？后验部分是否明确标为exploratory？

5. 模型优势是否跨折一致，还是由单一折驱动？

6. 统计显著是否同时具有工程意义？实际MAE差值是多少？

7. 最差节点、最差日期和低coverage条件下是否仍满足使用要求？

8. 已暴露最终周与六折结论是否冲突？若冲突，应以六折为主并解释证据等级。

## 8.2 Results回填矩阵

### Table 55

研究问题 | 必要结果 | 图表 | 最终结论形式
RQ1 | 理论/有效记录、样本保留率、规则敏感性 | Fig.2、Fig.7；Tables 1–2、8 | 是否能形成足够且可追溯样本
RQ2 | 模型×horizon×fold指标、最差折、排名 | Fig.4–5；Tables 5–6 | 谁更准、谁更稳定、差异是否实质
RQ3 | coverage/confidence/gap/volatility/node分层 | Fig.6；Table 7 | 何时可靠、何时失效
RQ4 | 六折与历史暴露周的排名/误差差异 | Fig.8；Table S5 | 协议是否改变模型判断

# 9. 当前可写内容与必须等待内容

### Table 56

阶段 | 内容 | 执行规则
现在可完成 | Title候选、Introduction前5段、Related Work框架、研究区背景、数据来源描述、方法协议、公式、图表caption草案、声明模板。 | 使用【待最终核验】标记数量和参数。
现在可完成约80% | Study Area and Data、Methodology、Fig.1/3、Table 1/3/4框架。 | 最终manifest后统一替换日期、数量、阈值和模型配置。
必须等待 | Abstract结果句、Results全部数值、Discussion的模型机制、Conclusion的最优模型/时距、Fig.2和Fig.4–8、Tables 2/5–8。 | 不得用旧P系列或暴露周结果提前定结论。
可并行准备 | 近3–5年文献池、AJSE相近期刊文章结构、图形代码模板、数据可用性和代码仓库README。 | 引用最终改为AJSE数字格式。

## 9.1 推荐写作顺序

1. 先冻结文章定位、四个RQ和与CRG-TCN文章的边界。

2. 完成Introduction和Related Work的论证骨架，但暂不写任何未经核验的结果导向句。

3. 完成Study Area and Data，所有数量使用统一占位符或最终manifest。

4. 完成Methodology和Fig.3，确保代码/配置与文字一一对应。

5. 实验稳定后，先生成Table 2/3/4和Fig.2/3，证明数据与协议正确。

6. 再生成主benchmark和统计表，之后写Results。

7. Results锁定后再写Discussion、Conclusion、Abstract和最终Title。

8. 最后做AJSE格式、引用、图件、声明和投稿文件检查。

# 10. 实验结束后的整体校验流程

### Table 57

门控 | 通过标准 | 失败处理
Gate 1 稳定性 | 结果目录无运行进程写入；快照时间和哈希固定。 | 未通过：不写Results。
Gate 2 数据完整性 | 理论网格、唯一键、节点和时间范围一致；所有筛选可追溯。 | 未通过：回到数据管线。
Gate 3 协议冻结 | 主规则、fold、模型集、统计单位和seed在正式结果前已确定。 | 未通过：后验分析降级为exploratory。
Gate 4 防泄漏 | 全样本断言PASS；train-only transformations有证据。 | 未通过：结果不可用于论文。
Gate 5 公平比较 | 共同sample manifest和预测文件可配对。 | 未通过：只能做有限或分开比较。
Gate 6 数值复算 | 从prediction文件独立重算表格和图，误差在容差内一致。 | 未通过：修复统计/汇总脚本。
Gate 7 文本一致性 | Abstract、Results、Discussion、Conclusion中的所有数字与表图一致。 | 未通过：统一数据源自动回填。
Gate 8 证据措辞 | 旧最终周、因果表达、普适性和外部验证措辞符合证据等级。 | 未通过：重写结论。
Gate 9 文章去重 | 与CRG-TCN文章的研究问题、模型结果、图表和贡献不实质重复。 | 未通过：删减/迁移内容。
Gate 10 AJSE合规 | 摘要、关键词、数字引用、三级标题、图分辨率、声明、审稿人候选。 | 未通过：投稿前整改。

## 10.1 全文三向一致性审计

### Table 58

方向 | 检查问题 | 建议工具/产物
证据→表图 | 每项主张是否有对应表格/图panel/统计文件？ | 建立claim_evidence_matrix.xlsx
表图→正文 | 每张表和每个panel是否在正文被解释，且没有未使用结果？ | 逐图逐表检查
正文→方法 | 每个结果是否在Methods预先定义；是否出现后验指标或分组？ | 后验内容标为exploratory
数字一致性 | 同一数值在Abstract、Results、Discussion、Conclusion是否一致？ | 从单一CSV生成
样本一致性 | N是否随模型、时距、fold和分层变化；变化是否解释？ | 表注强制报告N
术语一致性 | node/segment、origin、target window、coverage、confidence、missingness定义是否统一？ | 术语表

# 11. 审稿风险清单与预防性写法

### Table 59

风险 | 可能质疑 | 预防措施
创新性不足 | 审稿人认为只是常规模型比较。 | 把贡献落在数据合同、共同manifest、全样本审计、六折稳定性和失效边界；不要只写XGBoost优于基线。
数据期太短 | 约三个月难以覆盖季节性。 | 定位为short-history/data-scarce证据；不做年度泛化；讨论跨季节未来研究。
没有真正外部测试 | 最后一周已暴露。 | 主动披露；主要证据用rolling-origin；建议未来前瞻性锁定测试。
商业FCD不是地面真值 | provider speed存在采样和聚合偏差。 | 使用provider-reported speed；避免“ground truth”；说明缺少固定传感器验证。
阈值后验选择 | confidence/速度/聚合规则可能被结果驱动。 | 在正式benchmark前冻结；敏感性明确区分。
模型输入不公平 | 不同模型可能使用不同历史/特征。 | 统一赛道或明确分层比较；共同manifest；相同训练信息边界。
相邻样本不独立 | 逐节点小时t检验夸大显著性。 | node-day汇总、块bootstrap、非参数配对和Holm。
结果过多 | 多图多表导致主线分散。 | 主文只保留RQ驱动的6–8图、6–8表；完整细节进SI。
与另一篇文章重叠 | 同一数据和模型被认为salami slicing。 | 清晰区分研究问题、预测任务、结果集和贡献；交叉引用已发表/在投工作并避免重复文本。
可复现性不足 | 商业数据不可公开。 | 公开代码、配置、manifest schema、哈希、聚合结果和synthetic example。

## 11.1 建议使用的谨慎术语

### Table 60

建议表述 | 英文 | 避免表述
retrospective rolling-origin evaluation | 用于主要评价 | blind final test
previously exposed historical evaluation period | 用于旧最终周 | unseen/external test week
commercial FCD observations / provider-reported speed | 用于数据描述 | ground-truth traffic speed
was associated with / corresponded to | 用于关联解释 | caused / determined
within the studied corridor and period | 用于泛化边界 | generally applicable to highways
competitive / more stable under the evaluated protocol | 用于模型比较 | state-of-the-art / universally superior
data eligibility rule used in this study | 用于阈值说明 | optimal universal threshold

# 附录A. 可直接回填的英文句式骨架

## A.1 Introduction末段

This study evaluates whether sparse commercial floating-car data can support multi-horizon speed forecasting on a data-scarce highway corridor under a fully auditable retrospective protocol. Specifically, the study (1) reconstructs the complete theoretical observation grid and applies a pre-specified data-eligibility contract, (2) evaluates forecasting models on a common sample manifest using six rolling-origin folds, (3) quantifies performance variation across horizons, folds, nodes, and data-reliability conditions, and (4) compares the rolling-origin evidence with a previously exposed historical evaluation period. The intended contribution is therefore methodological and engineering-oriented rather than the introduction of a new deep-learning architecture.

## A.2 Methods中的证据状态声明

The period from 22 to 28 February 2026 had been examined in earlier development experiments and was therefore not treated as an untouched or independent test set. The primary evidence in this study was obtained from six retrospective rolling-origin folds. Results for the previously exposed period were retained only as a supplementary historical comparison.

## A.3 Provider status缺失

Provider operational status was not available in the source dataset and was therefore not used as an eligibility criterion. No missing status value was imputed or recoded as a normal operating state.

## A.4 Results段落模板

Across the six rolling-origin folds, [MODEL] achieved the lowest mean MAE at the [H]-h horizon ([VALUE] km h−1; 95% CI [LOWER, UPPER]), but the magnitude and consistency of the advantage varied across folds. The worst-fold MAE was [VALUE], and [MODEL] ranked first in [X] of the six folds. These results indicate [CAUTIOUS INTERPRETATION], rather than a uniform advantage across all evaluation periods.

## A.5 质量分层模板

Forecast errors were higher in samples with [LOW COVERAGE/LONGER GAPS] than in the corresponding reference stratum. The paired difference in MAE was [VALUE] km h−1 (95% CI [LOWER, UPPER]). This pattern was observed across [NUMBER] folds and may reflect reduced information continuity, although the observational design does not establish a causal effect.

## A.6 Limitations模板

Several limitations constrain the interpretation of the results. First, the study covers one corridor and approximately three months of observations, so seasonal and cross-network generalization cannot be inferred. Second, the commercial FCD represents provider-reported aggregated speed observations rather than vehicle-level trajectories or an independent fixed-sensor reference. Third, one historical week had been exposed during previous model development and was used only as a supplementary comparison. Future work should use a prospectively locked test period, a longer observation window, and independent traffic sensors where available.

# 附录B. 最终交付文件和结果包目录建议

AJSE_Phase2A_release/
├── 00_README/
│   ├── README.md
│   └── evidence_status.md
├── 01_config/
│   ├── data_contract.yaml
│   ├── folds.yaml
│   └── model_registry.yaml
├── 02_manifests/
│   ├── raw_snapshot_manifest.csv
│   ├── node_manifest.csv
│   ├── fold_manifest.csv
│   └── sample_manifest.parquet
├── 03_audits/
│   ├── data_audit_summary.csv
│   ├── leakage_audit.json
│   └── hashes_sha256.txt
├── 04_predictions/
│   └── model_fold_horizon_predictions.parquet
├── 05_metrics/
│   ├── metrics_long.csv
│   ├── stratified_metrics.csv
│   └── efficiency.csv
├── 06_statistics/
│   ├── paired_differences.csv
│   ├── block_bootstrap.csv
│   └── multiple_comparisons.csv
├── 07_figures/
│   ├── source_data/
│   ├── scripts/
│   └── final/
├── 08_tables/
│   ├── manuscript_tables.xlsx
│   └── supplementary_tables.xlsx
├── 09_manuscript/
│   ├── AJSE_manuscript.docx_or_tex
│   ├── figure_captions.docx
│   └── declarations.docx
└── 10_logs/
    ├── environment.txt
    └── run_logs/

# 附录C. 最终投稿前一页核对表

□ Phase 2A正式结果来自稳定快照，不再有后台写入。

□ 主规则、fold、模型、统计单位和随机种子有冻结记录。

□ 旧最终周仅称historical / previously exposed。

□ Abstract为150–250词，Keywords为4–6个。

□ 正文为方括号数字引用，参考文献按出现顺序。

□ 标题层级不超过三级。

□ 所有图按84/174 mm检查，panel label和8–12 pt字体可读。

□ 组合图≥600 dpi或矢量；半色调≥300 dpi。

□ 每张表/图均在正文按顺序引用，caption准确。

□ 每个性能表都报告N，主比较使用共同sample。

□ 报告折间差异、最差折和置信区间，不只报告平均值。

□ 统计检验考虑时空依赖并完成多重比较校正。

□ 结论不把相关性写成因果，不宣称普遍泛化。

□ Data/Code Availability与商业数据许可一致。

□ 与CRG-TCN文章无实质重复。

□ 四名潜在国际审稿人满足机构、国家和利益冲突要求。

### Table 61

最终定调：这篇AJSE论文的价值不在于展示一个更复杂的网络，而在于证明稀疏商业FCD在什么数据资格、时间评价和可靠性条件下能够形成可信的多时距预测证据。

□ 关键词为4–6个，并覆盖数据、任务、评价、可靠性和场景；每个关键词均能在正文找到对应方法或结果。

□ 每个正式实验均明确目的、输入、规则、输出、通过标准和论文落点。

□ 主证据、稳健性证据、冒烟结果和历史补充结果没有混为同一证据等级。

□ 所有实验编号与脚本、配置、输出目录建立一一对照。

□ Results中的每个结论均可追溯到sample manifest、预测文件、指标表和统计文件。

# 资料核验说明

本大纲综合了上传的《AJSE Phase 2A 文章详细说明》与《SCI 1区论文深度写作与润色 AI 提示词系统》。对期刊格式的修正依据2026年7月29日核验的Springer Nature AJSE官方Aims and Scope、Submission Guidelines和How to Publish with Us页面。其中，摘要150–250词、4–6关键词、方括号数字引用、三级以内标题、图件分辨率与84/174 mm版面宽度等要求均按官方指南处理。
