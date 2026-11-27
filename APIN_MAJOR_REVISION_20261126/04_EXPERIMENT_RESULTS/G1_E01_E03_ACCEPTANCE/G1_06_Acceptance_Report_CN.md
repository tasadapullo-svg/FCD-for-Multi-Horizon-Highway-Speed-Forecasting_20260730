# APPLIED INTELLIGENCE MAJOR REVISION — G1 E01–E03 FINAL ACCEPTANCE

总体：**CONDITIONAL_PASS**。本阶段实际完成E01/E02/E03全部可执行计算；非可估计问题逐项保留。未训练、未调参、未下载外部交通数据、未改文、未写正式回复。协议冻结于新误差统计之前：`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\00_PROJECT_CONTROL\G1_Analysis_Protocol.yaml`，SHA256 `e7e82b7260ebbc81585c4c7f7034d7a2d80a92730aa8d907687693c2cb2699f4`。

## G0继承与本轮执行

复用G0的544项哈希和180次预测历史验收，没有重新全量G0审核。只对本轮使用的数据进行主键/字段/真值/层级和单位关联。原83天返回CSV经ID+速度/置信度等字段及重复次序，与cleaned一对一映射，日期仍沿用cleaned修复时间，未宣称恢复原日期修复程序。共享中间层和商业明细只在`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\02_DATA\03_DERIVED_DATA\E01_E03`本机保存，不入ZIP。

180份预测已按共同key对齐；A/B比较需要补充提取两种随机模型108个文件的逐样本B损失，该补充只做一次并缓存，没有重跑模型或重复连接全部180份。原始与新计算分开标记ORIGINAL_FROZEN_BASELINE/REVISION_E01_E03。

## E01主要实算发现

15min正式分母403512，小时分母100878。403512=241601有合格记录槽位+1156仅不合格返回槽位+160755归档无返回槽位。原始唯一返回242757槽位，比例60.161036%（不等于原文把241601称原返回的59.87%）；质量合格去重覆盖59.874551%。行级244477=243307合格+1170不合格，与槽位漏斗明确区分。网格外126行/合格唯一槽位另列，不混分母。

四阈值有效小时96968/83439/45356/15838，嵌套集合核对通过。日均与槽位加权覆盖分别输出，首日按10小时×51而非24小时×51计分母。97.30%按作者决定登记DEFINITION_UNRESOLVED — REMOVE_OR_REPLACE_IN_REVISION，不再追查候选Excel，不改原图正文。

H6测试6/6为14521（49.8301%），5/6为14620（50.1699%）；缺失位置1–6、fold/split及六模型子集误差均已实算。6/6子集不是严格6/6训练。H3/H6共同origin、两种目标方差及各自有效/无效计数已计算，不以跨H MAE证明更远预测更优。

54个fold×horizon×split资格重建与原manifest主键完全相同，差异0；互斥剔除次序预冻结，同时保留非互斥计数。E04潜在支持432种组合已计算（含12/24/48h与严格H6）。4/4 H6所有fold验证为空；4/4 H3验证总计只有8；3/4 H3/H6存在极低支持。不能为四规则齐全强行训练或只保留有利fold。

## E02主要实算发现

原始返回行current_speed完全等于freeflow比例85.488614%；这不证明真实无拥堵，也不能证明供应商使用了历史回填。confidence分布、低于.8记录、节点/时段差异、速度与自由流分布和比值均按层级输出。

目标窗口同一有效小时比值定义拥堵proxy<.70、中间态[.70,.90)、近自由流≥.90。拥堵测试支持H1/H3/H6为952/614/700；不把未来状态当输入。0.60/.80阈值敏感性已完成，没有按误差选择阈值。分组含样本/节点/日期和LOW_SUPPORT标记。

原始可靠性特征从X_sequence按fold scaler还原，单位km/h；与因果填充ddof0 std重建最大差2.2604e-6，属于float32数值差。Gap与距最近观测年龄分别处理；coverage/gap/volatility训练分位点及有限联合分析已实算。选择诊断只讨论历史可观测proxy及标准化差异，不推断未返回真速度或MCAR/MAR/MNAR。

道路封闭：NOT_ESTIMABLE — NO OBSERVED CLOSURE EVENTS。FreeFlow_Lagged基准覆盖全部92147共同测试样本，保守使用至少1h前且所有可解析时间戳不晚于origin的记录；H1/H3/H6 MAE分别2.169594/2.172871/2.193327 km/h，明确与六模型同交集比较，未混入原六模型排名。仍缺独立API到达日志，时间可得性是CONDITIONAL_PASS，不能宣称线上延迟已验证。

## E03聚合差异、统计推断与稳定性

**确认Equation(12)与Table7实际计算不一致。** 表7全部18个均值与B的三位小数相同，六个随机模型×时距的未舍入历史均值均精确对应B。A并非重训或更换模型，只是按正文预定聚合。A的XGB三时距fold均值0.935267/0.819415/0.744363；GRU1.046958/0.947604/0.868938。四个确定性模型A/B相同。所有差异、SD、未舍入表与原稿都分列，不静默覆盖。

主要Day-macro XGB−SeasonalHA效应：

```text
 horizon    effect    CI_low  CI_high    raw_p  holm_adjusted_p
       1  0.077330 -0.145534 0.445115 0.639836         0.639836
       3  0.012295 -0.104316 0.173723 0.875412         0.875412
       6 -0.012050 -0.087033 0.085894 0.787421         0.951905
```

三项区间均跨0，没有支持XGB稳定优于SeasonalHA。15项预设比较中7项Holm<.05，显著性不作为验收标准。全体41个真实有效测试日期连续，3日可用39个起点、7日35个起点；10000次固定种子20261125，日期整体含全部节点。双侧p来自零假设中心化重采样并作(B+1)有限修正，不是未经中心化的正负比例。普通95%区间非同时区间，percentile CI与中心化检验不必严格互为对偶。

四权重及A/B：

```text
 horizon          estimand      MAE  delta_XGBoost_minus_SeasonalHA
       1        Fold-macro 0.935267                       -0.025749
       1   Sample-weighted 0.916642                       -0.040900
       1         Day-macro 1.018884                        0.077330
       1 Day-spatial-block 1.095629                        0.053894
       3        Fold-macro 0.819415                       -0.033442
       3   Sample-weighted 0.800130                       -0.053296
       3         Day-macro 0.856803                        0.012295
       3 Day-spatial-block 0.945564                        0.013670
       6        Fold-macro 0.744363                       -0.029394
       6   Sample-weighted 0.724947                       -0.044142
       6         Day-macro 0.762247                       -0.012050
       6 Day-spatial-block 0.877685                        0.015109
```

B重建原205个day×spatial-block MAE单元格至浮点精度；原XGB−SeasonalHA点估计+0.068424/+0.025185/+0.022590由B及原空间权重共同产生。新A的日块效应不是原fold均值，方向变化由实际分解证明，不能全部归于单一因素。旧bootstrap程序未恢复，旧CI只保留，不声称完整复现。HAC/DM按冻结方案不另做，不能依p值临时添加。

LOFO的六种单fold排除完整呈现，非重新训练CV。A下排除Fold6：H1 SeasonalHA领先，H3/H6仍XGB；旧文H1/H3均转SeasonalHA属于B口径，必须后续一起修正。H1排除Fold3或4又有Persistence领先，稳定性依赖估计量与测试区间。Fold5/6分布和误差只用于描述，没有下载日历或宣称节日导致误差。



补充日期支持解释：H1每天样本数范围35–1203，LOW_SUPPORT_DATE数量0。H3每天样本数范围18–1161，LOW_SUPPORT_DATE数量1。H6每天样本数范围28–1222，LOW_SUPPORT_DATE数量1。 Day-macro给每个有效日期等权，低观测日期不会按样本量自动降权；这会放大少数低支持日期影响，属于预先选定估计对象的实际限制。未据测试误差删除日期或改变主要统计方案，须与Sample-weighted及7日块敏感性共同阅读。证据：`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\E03_STATISTICAL_INFERENCE\E03_05b_Daily_Support_Diagnostics.csv`。

## 审稿证据、未解决问题与下一阶段范围

31条原始意见完整保留，不覆盖G0矩阵。进度分类：{'PARTIAL_EVIDENCE; TRAINING_OR_EDITORIAL_WORK_PENDING': 12, 'ANALYSIS_EVIDENCE_SUFFICIENT_FOR_ISSUE; MANUSCRIPT_PENDING': 7, 'PARTIAL_EVIDENCE; GIS_CALENDAR_OR_OPERATIONAL_EXPLANATION_PENDING': 5, 'PARTIAL_EVIDENCE; EXTERNAL_VALIDATION_OR_LIMITATION_RESPONSE': 4, 'LITERATURE_RELEVANCE_PENDING': 3}。这些是数据证据进度，不代表审稿满意或录用概率。仅方法说明、GIS/日历、文献、训练反事实、独立外推分别保留，正式回复与论文尚未修改。

基于实际支持冻结的下一阶段建议：1/4规则全六模型×全三时距，3/4只H1可做完整六fold；4/4不强做预测训练；H6严格6/6需训练；一种因果插补对照；12/48h仅代表性XGB/GRU与H1/H6端点；框架两组件分别用Ridge/XGB端点对照；有限Ridge/XGB/GRU验证候选；GRU静态信息；最多一个轻量时空候选保持条件性。未做全因子交叉。

运行上限计算见`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\G1_E01_E03_ACCEPTANCE\G1_Next_Experiment_Scope.csv`及计划工作簿：核心建议上限624个“模型×时距×fold×seed/配置执行”（含廉价确定性基准计算，不全是梯度训练），条件项额外上限78。这是各门均通过时的保守最大和，不是自动执行任务量。调参上限162候选+72选中模型额外seed=234，选中seed42候选不重复训练；任何已证明同实现/输入/协议的基准和候选复用。源码门先6个实现验证，不通过则所有后续训练预算归0；不能据新测试排名挑参数。三个正式入口仍缺失，作者需批准独立新实现，或提供原源码。

E07 freeflow基准REUSE_EXISTING；道路中心线与累计公里、官方节日日历和公平硬件成本仍待核实，不需要重新跑E01–E03。E08仍条件性，不因内部结果不好扩大数据范围；独立时段验证时间外推，外部走廊验证域差，外地检测器不能验证Sarawak原位车速或取消已暴露测试历史。

## 验收与执行限制

统一验收记录：`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\G1_E01_E03_ACCEPTANCE\G1_Validation_Checks.csv`。曾发现历史空间块对照join日期层名称不一和CSV p值舍入机械下界误报，均保留失败记录，定向修复；没有修改协议、主要估计量、p值或已通过计算。没有重复整个E01–E03。

后续遵守：已验收且输入/协议/代码未变的结果直接REUSED_PASS；只对具体科学或代码问题登记原因、影响和受影响任务后定向处理。原始FCD、逐样本预测、派生速度、特征张量和权重不入ZIP。聚合结果及诊断只含统计摘要；商业公开许可仍未确认，本机交付不代表公开授权。

七核心交付绝对路径：

- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\G1_E01_E03_ACCEPTANCE\G1_01_E01_E03_Result_Registry.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\G1_E01_E03_ACCEPTANCE\G1_02_Integrated_Results.xlsx`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\G1_E01_E03_ACCEPTANCE\G1_03_Reviewer_Response_Progress.csv`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\G1_E01_E03_ACCEPTANCE\G1_04_Manuscript_Consistency_Matrix.xlsx`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\G1_E01_E03_ACCEPTANCE\G1_05_Minimum_Remaining_Experiment_Plan.xlsx`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\G1_E01_E03_ACCEPTANCE\G1_06_Acceptance_Report_CN.md`
- `D:\Desktop\大修_Applied Intelligence_2026112_论文修改\04_EXPERIMENTS\G1_E01_E03_ACCEPTANCE\G1_07_Execution_Manifest.json`

最终ZIP：`D:\Desktop\大修_Applied Intelligence_2026112_论文修改\APIN_G1_E01_E03_Results_20261125.zip`。本阶段停止，等待作者检查和确认下一阶段建议规模；不自动训练或修文。
