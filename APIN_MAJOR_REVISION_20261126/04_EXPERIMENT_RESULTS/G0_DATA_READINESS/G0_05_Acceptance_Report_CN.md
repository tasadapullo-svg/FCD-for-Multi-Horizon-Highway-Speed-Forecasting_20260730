# APPLIED INTELLIGENCE REVISION — G0 FINAL ACCEPTANCE

生成时间：2026-11-25T18:55:16.288993+08:00。Manuscript ID：APIN-D-26-12623。

**Overall Status: CONDITIONAL_PASS。** 本结论仅针对本次有限G0数据准备度要求。历史2026-11-21全量审计的BLOCKED记录原样保留；未宣称历史全量数字、图表和训练复现已经通过。关键预测/样本数据的冻结版本可以确认，E01–E03可在明确限制下推进；本阶段结束后等待作者检查，不自动进入下一阶段。

## 1. 本地访问与实际来源

唯一输出根：`D:\Desktop\大修_Applied Intelligence_2026112_论文修改`。

原投稿目录：`D:\Desktop\论文\2027年投稿期刊\论文项目\已完成大修_20260905-低成本稀疏浮动车数据采集与可靠性感知预测框架：面向数据稀缺高速走廊_Applied Intelligence\20260905Applied Intelligence 投稿`，实际可访问，保持只读。Windows长路径使用`\\?\`访问前缀；登记表输出人可读的绝对路径，归档成员用`归档绝对路径!成员路径`表示，不能误认为独立磁盘文件。

本轮对指定两目录盘点得到905项（盘点时点含少量本轮脚本），依据历史明确索引定向定位2888个历史物理资产中的2882项；没有扫描无关桌面目录或全盘。未找到的6项不是自动认定关键数据缺失。清单详见`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\00_PROJECT_CONTROL\local_inventory.json`与`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\00_PROJECT_CONTROL\prior_assets_located.json`。

实际使用的审稿原文为`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\APIN_D_26_12623_Reviewer_Comments20261122.docx`，31项已逐条保留英文原文；R6五项是该文档注明的编辑追踪编号。该文件解决历史审计“仅有摘要”的缺口，但未另获Editorial Manager原始邮件字节。

投稿PDF：`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\APIN-D-26-12623.pdf`，61页；已进行正文相关位置文本提取，证据`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\00_PROJECT_CONTROL\submission_text_evidence.json`。未重新编译论文，未声称全文视觉或逐字核对完成。原Overleaf ZIP：`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\Applied_Intelligence_20260905.zip`。

## 2. GitHub访问与冻结版本

本轮只读实际访问指定仓库main及递归树，main commit为`0a4d2e00ac509d4f4e64f950df5a7d35238d6e4c`，804个树项且未截断，与历史远端SHA一致。元数据保存在`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\00_PROJECT_CONTROL\github_branch_20261125.json`及`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\00_PROJECT_CONTROL\github_tree_20261125.json`。本地是历史导出目录，不是已证明clean的Git工作树。

历史GIT_RESULT_FREEZE记录definition commit=`14f0a7547147051c583753a3e44cce9c967ca23e`，independent-file-audit commit=`5545c42ee7e111bfe2bd3f19c2920a31c06ac502`；这些是历史原工作树版本声明，不能当成当前公开仓库可达提交。实际查询后者返回422 No commit found，tags refs请求返回404，已保存原响应。当前main不是默认认定的原投稿冻结版本；本轮以历史配置/注册表/预测/manifest的内容哈希链确认可用基准。

本地已有必要资产，故未下载商业数据或重复下载仓库，也未修改/提交/推送。实际访问日期2026-11-25。

## 3. 已有资产与历史验收复用

- 正式数据/结果相关544文件的当前SHA256全部与历史文件登记一致；8份关键历史验收表/报告与历史输出哈希清单一致。
- 180份预测和18份manifest版本一致，复用历史180/180主键、真值、finite、哈希与MAE/RMSE验收，状态REUSED_PASS。本轮未重算180组指标。
- 复用18/18目标重建、54/54 split边界与因果检查、冻结15min面板逐键速度对应证据；这些不等于已证明真实训练代码全部fit scope。
- 54份GRU权重存在且哈希一致，仅复用历史容器/CRC检查；没有反序列化、加载模型或执行推理。
- 正式15min观测241601行、小时面板100878行，列模式已实际读取。历史1/4–4/4计数96968、83439、45356、15838仅作已验收记录引用，本轮不提前执行E01正式统计。

证据根：`D:\Desktop\论文\2027年投稿期刊\论文项目\已完成大修_20260905-低成本稀疏浮动车数据采集与可靠性感知预测框架：面向数据稀缺高速走廊_Applied Intelligence\20260905Applied Intelligence 投稿\APIN_R1_G0_AUDIT_20261121`。关键复用表的实际路径及当前/历史哈希在`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\00_PROJECT_CONTROL\gap_closure_evidence.json`。全部544项比较在`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\00_PROJECT_CONTROL\verification_evidence.json`。

## 4. 新增定向核验与真实字段映射

筛选前每日CSV归档实际存在：`D:\Desktop\论文\2027年投稿期刊\论文项目\已完成大修_20260905-低成本稀疏浮动车数据采集与可靠性感知预测框架：面向数据稀缺高速走廊_Applied Intelligence\历史投稿\历史投稿文章\20260623\PanBorneo_TomTom_Cleaned_Experiment_Package.zip!00_raw_original/output_tomtom_data完整数据(4).zip`，83份CSV，244477行，15列，含confidence低于0.8的1170行；该数量与另一份日期修正版相同。它们是已解析的返回CSV，不是原API JSON，也不能证明全部请求或失败均已记录。日期修复及CSV→cleaned逐行映射还未完全闭环。

cleaned实际来源：`D:\Desktop\论文\2027年投稿期刊\论文项目\已完成大修_20260905-低成本稀疏浮动车数据采集与可靠性感知预测框架：面向数据稀缺高速走廊_Applied Intelligence\历史投稿\历史投稿文章\20260623\PanBorneo_TomTom_Cleaned_Experiment_Package.zip!02_cleaned_records/tomtom_cleaned_records.csv.gz`，244477行、34列、51节点，时间2025-12-08 13:15至2026-02-28 23:45。成员SHA256=`915e2f50d30752c7fdb666cae83a4e49945d0d81913ea791531043ae84fdf5c3`，与pipeline raw_sha256一致。10个关键字段本轮读取均无空值。

|概念|实际字段|限制|
|---|---|---|
|节点|cleaned.node_id；上游point_uuid|上游节点映射仍需原生成代码闭环|
|时间|cleaned.event_time；上游capture_time/pd_create_time/flow_create_time|保留三种原时间；不擅自选替代字段|
|经纬度|pd_latitude/pd_longitude|节点表为latitude/longitude|
|当前与自由流速度|current_speed/free_flow_speed|供应商速度而非独立真值|
|当前与自由流时间|current_travel_time/free_flow_travel_time|语义与时间可得性需分析时说明|
|置信度与封闭|confidence/road_closure|筛选前返回CSV的closure只有0，没有可观察封闭样本|

历史数据链必须区分：244477解析CSV行、243307质量合格行、全跨度去重241727、完整小时网格内去重241601、126条边界差。完整小时计划网格403512槽位不同于含不完整起始小时的403665槽位。重复返回与质量剔除存在重叠层级，不能简单相减称为互斥漏斗。无返回槽位的速度未知；请求失败/无探针/无供应商记录不能凭CSV区分。

本轮实际试读F1/H6 manifest主键唯一。对XGBoost与GRU的F1/H1三种子分别读取六份预测，sample_id/node_id/forecast_origin/fold/horizon及y_true一致，可按键均值聚合。其余文件采用版本一致的历史全量主键核验。**逐seed指标平均不等于均值预测的指标；正式E03需先明确估计量，不能静默替换原表。**

## 5. 97.30%与Fig2判定

**97.30% Verification Status: DEFINITION_UNRESOLVED。** 没有证据证明原稿97.30%的分子、分母、质量层级和聚合方式。本轮有界追溯停止，不继续搜索无关工程。

两个同名候选工作簿SHA不同：

- `D:\Desktop\论文\2027年投稿期刊\论文项目\已完成大修_20260905-低成本稀疏浮动车数据采集与可靠性感知预测框架：面向数据稀缺高速走廊_Applied Intelligence\历史投稿\fig\历史修改\fig02\AJSE_Fig_ABC_Daily_Data_20260806_missing13_completed.xlsx`：SHA256 `f0c1c13c3ed5128c6f16c8e8f4456cc59f4919a8e4f443246fc5dffe04385efa`；日均98.70068509%，分子总和100272/分母总和101592。
- `D:\Desktop\论文\2027年投稿期刊\论文项目\已完成大修_20260905-低成本稀疏浮动车数据采集与可靠性感知预测框架：面向数据稀缺高速走廊_Applied Intelligence\历史投稿\数据包\历史数据\AJSE_Fig_ABC_Daily_Data_20260806_missing13_completed.xlsx`：SHA256 `afe4161fe01da26a568d69da7d7e03c3fd9aac3d82353208e7dff294b154582c`；日均98.53630207%，分子总和100105/分母总和101592。

两表均按83天、每天1224小时节点记录计分母，包括不完整起始日；首日1191/1224=97.3039%恰与97.30接近，但不能据此认定原稿误用了首日。候选表有“missing13_adjusted”声明，且其整期均值均非97.30%；不得用它们修正正式基准。某历史导出manifest写source=imagegen.png，仅证明该候选导出来源声明，不足以证明投稿图生成链。

59.87%对应241601/403512的合格去重15min观测覆盖；82.71%对应83439/100878的2/4小时资格率。两者分母/层级不同，均不能推出97.30%。历史Fig2(a)100%标签与max=99.03%冲突记录保留，未重新宣称图内正确值已确定。

后续建议：删除未经证实的97.30%汇总指标，以明确分子分母、起止边界和质量层级的冻结面板指标重绘Fig2。当前不改图或正文。

## 6. 源码、GIS和许可缺口

三个正式入口src/build_phase2a1_data.py、src/run_phase2a1_campaign.py、src/finalize_phase2a1.py，在已索引本地资产及本轮公开树中仍未定位。Phase2A0或Phase13脚本不得冒充。六模型HA、SeasonalHA、Persistence、Ridge、XGBoost、GRU均为SOURCE_PARTIAL（配置、输出存在，正式训练入口SOURCE_MISSING）；若原源码无法恢复，新增训练需REIMPLEMENTATION_REQUIRED并单独批准。HA节点均值、SeasonalHA季节匹配与回退未能由真实源码证明。网格、插补、特征、fold/目标/manifest和统计的产物存在，但生成关系不能宣称全部复现。正式环境锁缺失。

51节点CSV存在，实际ID为N001–N051；后续N01–N51只能作为保留原ID的一一展示映射。原字段order_index和latitude/longitude已确认；坐标完整，不从图片反推。道路沿线距离、真实累计里程、道路中心线及QGIS工程未完成验证，候选邻接距离不能当作已验证道路距离。GeoJSON可能在嵌套包内，历史仅存在性证据不得当成完整GIS准备通过。G0不制图、不获取路网。

商业许可文件明确表示原FCD及逐记录派生小时速度、目标、特征、预测和图源的公开授权未获本地文件证明；公开仓库却包含相关文件。Data Availability与实际公开类型存在需要作者解决的许可一致性问题。LICENSE_REVIEW_REQUIRED，不自行认定已获授权；本轮没有上传、删除或修改历史仓库。模型权重是否受数据合同影响也需作者确认。

## 7. E01–E03任务级准备度

E01: READY_WITH_LIMITATIONS。覆盖率、日/节点/小时缺失、H6完整数与位置有输入；边界剔除和漏斗须按冻结规则重建候选与互斥原因。原始返回和质量可区分，但完全无返回的请求原因缺计划/失败日志。

E02: READY_WITH_LIMITATIONS。速度/自由流/置信度字段实际存在，可用对应时空键分析。交通状态须预设，不能给无返回样本计算真实速度或误差；closure样本无变化无法估计封闭效应。Coverage/gap可从manifest取得，volatility可由history_row_ids及小时面板计算。

E03: READY_WITH_LIMITATIONS。共同主键、真值、逐seed预测、日期/空间块可得。统计方案尚待Prompt02预先锁定，不按测试结果挑方法。日及空间块仍有依赖；不能将92147测试记录或205个day×spatial-block当成相互独立样本。已暴露测试集不能改称独立盲测。

28项计算任务的输入、缺口与解决方案逐项见工作簿07_E01_E03_Readiness。本轮未计算正式分层MAE、效应区间、bootstrap、Holm新检验或LOFO结果。

## 8. 冻结范围、外部数据与作者决策

E04=有限敏感性，E05=协议消融，E06=模型公平性，E07=空间运营，E08=条件外部验证。旧审计文件的E4/E5顺序和旧工作簿24项编号与本轮不同，以G0_03为准。不做完整度×插补×窗口×模型×超参数全因子实验，不自动新增模型。

E01–E03没有必须下载的外部数据。作者补原训练源码/日志/许可属于恢复既有证据，不可由其他地区数据替代。

条件来源已核对官方入口，但未下载：[DCRNN数据入口](https://github.com/liyaguang/DCRNN)、[Caltrans PeMS](https://pems.dot.ca.gov/)、[Geofabrik马来西亚区域](https://download.geofabrik.de/asia/malaysia-singapore-brunei/)。METR-LA与PEMS-BAY直接文件下载地址及大小未验证，工作簿标UNVERIFIED；Geofabrik整区PBF入口显示约242MB，实际走廊提取规模未知。PeMS官方字段包括% Observed和Avg Speed，速度单位mph，不能当成TomTom置信度或直接与km/h混用。PEMS-BAY首轮NOT_REQUIRED，其余CONDITIONAL，不自行切换成DOWNLOAD_BY_CODEX。

作者需检查：①接受先做受限E01–E03；②97.30%后续删除与替代方案；③是否补已有源码/采集日志/roadline；④TomTom公开许可；⑤外部数据最小集与获取方式。科学上无法回答的部分保留限制，不为PASS降低标准。

## 9. 已完成、已复用、未完成与交付

已完成：本地实际路径与有界定位、关键哈希版本核对、原文31项映射、原始解析CSV/cleaned字段试读、最小种子键检查、97.30%候选冲突关闭、任务级准备度、有限范围冻结及七表工作簿。

已复用：正式180运行核验/指标复算、manifest目标及split检查、15min→panel对应。未完成：历史全量论文数字与所有图内标注、完整API解析链、正式源码恢复、全训练复现、道路里程验证、商业公开许可确认。未执行：新模型训练/统计推断、付费采集、批量外部下载、论文改写、QGIS制图、GitHub写操作。

本次验收不同于旧全量G0审计：缺源码/GIS/97.30%不自动阻断冻结预测统计；关键预测与目标、主键与哈希均有可用证据，所以是CONDITIONAL_PASS而非PASS或整体BLOCKED。仅原返回失败原因、封闭效应和独立地面真值等任务受限或无法完成。

六份核心交付（实际绝对路径）：

- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\G0_DATA_READINESS\G0_01_Data_Asset_Registry.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\G0_DATA_READINESS\G0_02_Reviewer_Experiment_Matrix.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\G0_DATA_READINESS\G0_03_Frozen_Experiment_Scope.md`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\G0_DATA_READINESS\G0_04_Missing_Data_and_Download_List.xlsx`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\G0_DATA_READINESS\G0_05_Acceptance_Report_CN.md`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\G0_DATA_READINESS\G0_06_Execution_Manifest.json`

阶段ZIP：`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\APIN_G0_Data_Readiness_20261125.zip`。ZIP仅包含本轮六核心文件、脚本与汇总证据，不复制商业原始记录、预测明细、特征或模型权重。

Recommended Next Action：作者检查G0和工作簿06_Author_Decisions，确定外部数据获取方式后，再发起Prompt02 E01–E03。当前停止。
