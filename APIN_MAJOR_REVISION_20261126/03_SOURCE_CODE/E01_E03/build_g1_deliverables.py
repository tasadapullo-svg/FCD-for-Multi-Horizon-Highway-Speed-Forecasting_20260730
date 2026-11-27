from common import *
def main():
 log('G1 core deliverable assembly START from completed aggregate results only')
 load=lambda folder,n:pd.read_csv(folder/n)
 line=load(E01,'E01_01_Data_Lineage_and_Coverage.csv');thr=load(E01,'E01_02_Hourly_Threshold_Coverage.csv');h6=load(E01,'E01_06_H6_Target_Completeness.csv');feas=load(E01,'E01_11_E04_Sample_Feasibility.csv');attr=load(E01,'E01_10_Fold_Sample_Attrition.csv');dist=load(E02,'E02_01_Speed_and_Target_Distribution.csv');eq=load(E02,'E02_02_FreeFlow_Equality.csv');traffic=load(E02,'E02_04_Traffic_Regime_Distribution.csv');reg=load(E02,'E02_05_Regime_Model_Performance.csv');reliab=load(E02,'E02_07_Coverage_Gap_Volatility.csv');select=load(E02,'E02_08_Sample_Selection_Diagnostics.csv');ff=load(E02,'E02_10_FreeFlow_Baseline.csv');seed=load(E03,'E03_01_Seed_Aggregation_Reconciliation.csv');tab=load(E03,'E03_03_Original_vs_Recomputed_Table7.csv');est=load(E03,'E03_04_Weighting_Estimands.csv');holm=load(E03,'E03_08_Holm_Adjusted_Comparisons.csv');lofo=load(E03,'E03_10_LOFO_Stability.csv');practical=load(E03,'E03_09_H1_Practical_Differences.csv');validation=json.loads((G1/'G1_Validation_Receipt.json').read_text(encoding='utf-8'))
 assert validation['overall_status']=='CONDITIONAL_PASS'
 gaps=[]
 def plan(id,q,review,ev,unresolved,inputs,support,models,hs,folds,budget,formula,necessity,reuse,details):
  gaps.append(dict(experiment_id=id,scientific_question=q,reviewer_mapping=review,existing_evidence=ev,unresolved_issue=unresolved,required_inputs=inputs,sample_support=support,source_code_dependency='恢复原源码或作者批准新实现及最小基准验证' if budget else '无需新训练源码',proposed_models=models,proposed_horizons=hs,proposed_folds=folds,maximum_run_budget=budget,budget_basis=formula,reuse_possible=reuse,necessity=necessity,author_approval_required='YES_FOR_NEW_TRAINING_OR_DATA',candidate_details=details,execution_status='NOT_EXECUTED',selection_basis='scientific question and data support, not favorable observed test rank'))
 plan('SOURCE_GATE','独立新实现能否用于后续公平对照','跨意见',str(CTL/'PROJECT_RULES.md'),'三个正式训练入口仍缺失','原配置/特征/scaler/manifest/预测','已有冻结完整基准','原六模型','H1','Fold1（最早fold，固定用于实现验证）',6,'6模型×1H×1fold×seed42','MUST_RUN','原预测只读作为目标，不重跑180','先恢复源码；失败需作者批准新实现。先6个实现验证执行；未通过则所有后续训练预算0。固定最早fold不是按表现挑选。')
 plan('E04_T1','1/4规则是否改变预测结论','R1-03;R2-02',str(E01/'E01_11_E04_Sample_Feasibility.csv'),'覆盖统计不能替代预测对照','新小时规则、共同交集与policy-native manifest','各fold测试最少7154/6686/6826（H1/H3/H6），验证最少同量级','原六模型','H1/H3/H6','1–6',108,'6模型×3H×6fold×1seed','MUST_RUN','2/4原seed42模型/结果可作固定基准；仅同源实现验收后','单因素改阈值，不交叉窗口/插补；随机模型先seed42作为敏感性，不能冒充三seed主结果；共享预测分别评价原生与交集。')
 plan('E04_T3_H1','3/4规则可评价部分的六模型敏感性','R2-02',str(E01/'E01_11_E04_Sample_Feasibility.csv'),'H3/H6某fold仅19/1有效验证或测试','3/4面板与新manifest','H1每fold验证/测试最少541；H3/H6低支持','原六模型','H1','1–6',36,'6模型×1H×6fold×seed42','MUST_RUN','2/4基准复用','3/4 H3/H6不做六fold主模型结论；如作者要求局部描述需另定支持标准，不能删不利fold。')
 plan('E04_T4','4/4规则是否值得强行训练','R2-02',str(E01/'E01_11_E04_Sample_Feasibility.csv'),'H6所有fold验证为空；H3仅8条验证总支持','无需新数据','H6验证0；H3验证合计8；H1最小验证21','NONE','NONE','NONE',0,'无可支持完整公平实验，0','EXPLANATION_ONLY','覆盖与潜在样本结果已验收','不为形成四条MAE曲线强制训练或放宽资格；完整报告样本损失及不可评价边界。')
 plan('E04_H6_STRICT','严格6/6目标的训练敏感性','R1-02',str(E01/'E01_06_H6_Target_Completeness.csv'),'原6/6子集并非严格6/6训练','原2/4历史；新H6 6/6标签/训练样本','测试14521；各fold验证最少1006，训练最少29713','原六模型','H6','1–6',36,'6模型×1H×6fold×seed42','MUST_RUN','现有完整目标子集评价只复用作描述','重新定义训练目标支持，禁止把新MAE当作旧表更正。')
 plan('E04_IMPUTE','长缺失下原因果填补的反事实影响','R1-03;R3-01',str(E02/'E02_06_Gap_Conditioned_Performance.csv'),'分层关联不能证明替代插补收益','训练期节点×时段中位数；缺则训练节点/走廊中位数','原共同测试92147；按训练支持固定回退','XGBoost;GRU;Persistence','H1/H3/H6','1–6',54,'3模型×3H×6fold×1替代×seed42','MUST_RUN','原协议预测及未受输入变化的HA/SeasonalHA只按可证明条件复用','只一种训练期季节中位数因果替代，与原24h不交叉；不同插补配对同target，不在测试上挑规则。')
 plan('E04_HISTORY','24h历史选择的最小端点检验','R3-02',str(E01/'E01_11_E04_Sample_Feasibility.csv'),'E01只证明样本可行，不能说明预测增量','12h/48h新输入；目标保持原H1/H6','测试支持不变；训练首段有效样本变化，使用预定共同训练/验证策略','XGBoost;GRU','H1/H6（时距端点，预先固定）','1–6',48,'2模型×2H×6fold×2新增窗口×seed42','MUST_RUN','24h原seed42为对照','不新增168h；不做完整度×窗口交叉；若结论需要H3拓展另由科学问题触发审批，不能按有利表现挑时距。')
 plan('E05_GRID_CAUSAL','网格与因果预处理是否影响结论','R1-07;R6-01',str(E01/'E01_10_Fold_Sample_Attrition.csv'),'数据审计不能替代预测反事实','两个独立单组件对照；固定真实墙钟target','原共同样本；returned-only需额外验时距与公平可比性','Ridge;XGBoost','H1/H6','1–6',48,'2模型×2H×6fold×2独立对照×seed42','MUST_RUN','原基准；共享同目标损失表','非因果全期scaling仅无效泄漏示范，不作为合法优胜模型；returned-only不得把第H条记录冒充H小时。')
 plan('E05_MANIFEST','per-model origin是否形成有意义反事实','R1-07',str(E01/'E01_10_Fold_Sample_Attrition.csv'),'若原模型均接受相同填补，放宽集合未必是独立可解释组件','先定义模型实际可用信息与可评价target','有资格漏斗，模型特定资格尚需规则证据','Ridge;XGBoost','H1/H6','1–6',24,'2模型×2H×6fold×seed42，仅规则能定义时','CONDITIONAL_RUN','先做集合差异检查；集合相同则0训练','不可人为制造不同集合来迎合消融；先检查可识别性。')
 plan('E06_TUNE','Ridge/XGB/GRU有限验证预算公平性','R1-06;R3-06;R6-04',str(E03/'E03_03_Original_vs_Recomputed_Table7.csv'),'聚合修正使GRU均值改变，但原模型仍未验证调参','恢复训练/验证输入；预定候选；禁止测试选型','原训练/验证全18任务可用','Ridge;XGBoost;GRU','H1/H3/H6','1–6',234,'3模型×3候选×18任务×seed42=162；选中XGB/GRU补2seed×2模型×18=72；合计上限234','MUST_RUN','仅在同实现同输入哈希证明后可复用冻结候选seed42；已完成候选不重训','Ridge alpha{0.1,1,10}；XGB固定500树仅depth{4,8,12}；GRU hidden{32,64,128}其余训练预算一致，validation早停；每任务以validation MAE固定选择，测试不参与。')
 plan('E06_GRU_STATIC','GRU是否因缺节点静态信息受不公平影响','R1-06;R6-04',str(E03/'E03_11_Seed_Stability.csv'),'原GRU没有静态节点输入','节点identity/坐标在预测时可得；固定合理注入结构','同原共同样本','GRU_with_static','H1/H3/H6','1–6',54,'1配置×18任务×3seed=54','MUST_RUN','原GRU动态输入选中配置直接复用作对照','采用验证阶段选定动态GRU设置，静态分支尺寸预定；不另外大规模调参。')
 plan('E06_SPATIAL','一个轻量邻节点模型候选','R1-06;R6-04',str(E02/'E02_05_Regime_Model_Performance.csv'),'原模型没有邻节点；GIS拓扑仍待核实','真实节点顺序/邻接；因果邻节点特征','原有效样本；邻接缺失处理须冻结','one lightweight neighbor-GRU candidate','H1/H3/H6','1–6',54,'1架构×18任务×3seed上限54；先seed42共18，追加2seed36须过验证门','CONDITIONAL_RUN','复用E06训练工程和节点特征，不增其他深度架构','仅一个候选，预算与GRU相当；确认邻接与作者批准后才执行。')
 plan('E07_FREEFLOW','Free-flow基准回应R6','R6-03',str(E02/'E02_10_FreeFlow_Baseline.csv'),'仍无独立ingestion日志','已完成保守历史滞后基准','92147共同样本已覆盖','FreeFlow_Lagged','H1/H3/H6','1–6',0,'已完成，不重复','REUSE_EXISTING','直接复用E02表，记录时间戳可得性限制','不混入原六模型排名，不用未来target freeflow。')
 plan('E07_GIS_CALENDAR_COST','道路里程、节日解释与运行成本','R1-05;R3-04;R3-11;R6-05',str(E03/'E03_12_Fold_Regime_Diagnostics.csv'),'无真实道路距离；节日因果未证；历史推理成本未记录','作者已有roadline/授权小范围路网；官方日历；同硬件模型推理接口','节点51；各fold目标与误差诊断已有','original/approved models for timing only','H1/H3/H6','不以有利测试fold选场景',0,'训练预算0；运行成本仅后续warmup20+重复100批的测量计划','MUST_RUN','复用E02/E03所有分布与LOFO，不重算','数据/日历核实和性能测量不是新模型训练。来源/模型接口不齐先保留限制，不能反推经济收益。')
 plan('E08_EXTERNAL','独立时段/走廊能回答哪些泛化问题','R1-08;R2-01;R3-12','G0外部数据清单及本轮回顾性证据','公开外地检测器不能验证Sarawak同址速度，也不能消除已见测试','作者决定最多一套外部速度基准或真正未见时段','尚无新独立数据，不因内部排名扩大范围','UNDECIDED','UNDECIDED','UNDECIDED',0,'本阶段预算0；获数据与独立协议后另定','CONDITIONAL_RUN','现有协议可复用，原FCD不能外传','先判断科学目标；不下载METR-LA/PEMS-BAY，外部预算不在本次冻结训练上限。')
 plan_df=pd.DataFrame(gaps);save(plan_df,G1/'G1_Next_Experiment_Scope.csv')
 core_budget=int(plan_df[plan_df.necessity=='MUST_RUN'].maximum_run_budget.sum());conditional_budget=int(plan_df[plan_df.necessity=='CONDITIONAL_RUN'].maximum_run_budget.sum())
 limitations=[dict(issue='97.30%',status='DEFINITION_UNRESOLVED_REMOVE_OR_REPLACE',impact='后续Fig2/§3.3修订；本阶段不追查不改文',evidence=str(E01/'E01_03b_Coverage_Weighting.csv')),dict(issue='Equation12/Table7',status='CONFIRMED_AGGREGATION_MISMATCH',impact='六个随机模型×时距均值与正文不一致；B原样保留，主要A另列',evidence=str(E03/'E03_03_Original_vs_Recomputed_Table7.csv')),dict(issue='API请求失败原因',status='NOT_ESTIMABLE',impact='可计算归档无返回槽位，不能判网络失败/无车辆/MNAR',evidence=str(E01/'E01_01_Data_Lineage_and_Coverage.csv')),dict(issue='Road closure',status='NOT_ESTIMABLE',impact='没有观测到封闭事件，不补造效应',evidence=str(E02/'E02_09_Closure_and_Quality_Filter.csv')),dict(issue='Free-flow可得性',status='CONDITIONAL_PASS',impact='保守>=1h滞后和全部可解析时间上界；仍缺独立到达日志',evidence=str(E02/'E02_10_FreeFlow_Baseline.csv')),dict(issue='短序列及非平稳',status='INFERENCE_LIMITATION',impact='41日期；MBB与LOFO只缓解部分依赖，不证明独立外推/等效',evidence=str(E03/'E03_08_Holm_Adjusted_Comparisons.csv')),dict(issue='训练源码',status='SOURCE_MISSING',impact='后续训练先恢复，失败需批准独立新实现和最小6运行验证',evidence=str(G1/'G1_Next_Experiment_Scope.csv')),dict(issue='GIS/日历/真值/许可',status='UNRESOLVED',impact='不推断道路里程/节日因果/真实车速；商业明细只限本机，不上传',evidence=str(ROOT/'04_EXPERIMENTS/G0_DATA_READINESS/G0_05_Acceptance_Report_CN.md'))]
 save(pd.DataFrame(limitations),G1/'G1_Limitations.csv')
 # Update all31 original comments without altering G0.
 g0=pd.read_csv(ROOT/'04_EXPERIMENTS/G0_DATA_READINESS/G0_02_Reviewer_Experiment_Matrix.csv');progress=[]
 completed={'R1-01','R1-09','R2-04','R3-03','R3-08','R3-10','R6-02'};literature={'R2-03','R3-05','R3-09'};gis={'R1-05','R3-04','R3-07','R3-11','R6-05'};external={'R1-04','R1-08','R2-01','R3-12'}
 key={
 'R1-01':f'15项预设比较；Holm显著{int(holm.significant_holm_0_05.sum())}项，未证明XGB优于SeasonalHA；日块不是独立92147样本',
 'R1-02':'H6测试6/6=14521、5/6=14620；子集误差和六位置齐全；严格6/6训练仍需执行',
 'R1-03':'403512=241601合格槽+1156仅不合格槽+160755无归档返回；删除97.30%；插补敏感性仍待',
 'R1-05':'54组合候选与资格重建键差异0；GIS道路距离仍缺',
 'R1-08':'A口径排除Fold6：H1 SeasonalHA领先，H3/H6 XGB仍领先；旧B结论不能直接沿用',
 'R1-09':'A H1 fold-macro XGB0.935267/Persistence0.950409/SeasonalHA0.961016；实际效应及区间独立报告',
 'R1-10':'Table7六个随机模型均值对应B，与Equation12不一致；图表后续统一改',
 'R2-02':'1/4支持充分；3/4 H3/H6严重稀疏；4/4 H6全部验证0，不能强做完整训练',
 'R2-04':'B历史205个day×block单元格精确重建；A/B与四种权重分别解释方向变化',
 'R3-01':'gap/age分开，volatility恢复原km/h；替代因果插补仍需预测对照',
 'R3-02':'12/24/48h测试支持相同，训练首段样本不同；预测性能尚未验证',
 'R3-03':'有效/排除/部分可观测目标以历史代理比较，未对无真值样本算误差或声称MNAR',
 'R3-06':'GRU A MAE=1.046958/0.947604/0.868938；恢复种子聚合不等于解决调参公平性',
 'R3-08':'与R1-01共享MBB/7日敏感性和LOFO，统计不足仍明确',
 'R3-10':'coverage、gap、原单位volatility单变量和有限联合分层均含支持标记',
 'R6-02':'3日主块、7日敏感性、10000次中心化检验已完成；HAC/DM按预定理由不适用',
 'R6-03':'原返回行85.4886%速度等于freeflow；拥堵proxy样本H1/H3/H6为952/614/700；freeflow基准已完成',
 'R6-04':'A/B差异已定位，HA/SeasonalHA真实实现未恢复；GRU静态信息和邻节点仍待验证',
 'R6-05':'Fold5/6目标与交通状态/coverage/误差分布已计算；无官方日历核验，不声称节日因果'}
 for _,row in g0.iterrows():
  cid=row.comment_id;tasks=plan_df[plan_df.reviewer_mapping.str.contains(cid,regex=False)]
  if cid in completed:readiness='ANALYSIS_EVIDENCE_SUFFICIENT_FOR_ISSUE; MANUSCRIPT_PENDING'
  elif cid in literature:readiness='LITERATURE_RELEVANCE_PENDING'
  elif cid in gis:readiness='PARTIAL_EVIDENCE; GIS_CALENDAR_OR_OPERATIONAL_EXPLANATION_PENDING'
  elif cid in external:readiness='PARTIAL_EVIDENCE; EXTERNAL_VALIDATION_OR_LIMITATION_RESPONSE'
  else:readiness='PARTIAL_EVIDENCE; TRAINING_OR_EDITORIAL_WORK_PENDING'
  e01=str(E01/'E01_Summary_CN.md') if 'E01' in str(row.required_experiment) or cid in ['R1-10','R6-03'] else 'NA';e02=str(E02/'E02_Summary_CN.md') if 'E02' in str(row.required_experiment) or cid=='R6-03' else 'NA';e03=str(E03/'E03_Summary_CN.md') if 'E03' in str(row.required_experiment) or cid in ['R1-10','R3-06','R6-04'] else 'NA'
  progress.append(dict(reviewer_id=row.reviewer_id,comment_id=cid,original_comment=row.original_comment,G0_status=row.completion_status,E01_evidence=e01,E02_evidence=e02,E03_evidence=e03,evidence_file=';'.join(x for x in [e01,e02,e03] if x!='NA') or str(G1/'G1_Limitations.csv'),key_result=key.get(cid,'已有研究边界或对应分析证据；未完成部分见剩余方案，不冒充正式回复'),remaining_experiment=';'.join(tasks.experiment_id) or '方法/局限/文献或图文修订',remaining_data='原源码/道路/日历或真正独立真值按任务；不自动下载' if cid not in completed|literature else '无必须新增数据',planned_manuscript_section=row.required_manuscript_section,response_readiness=readiness,limitation='阶段证据不是审稿人满意度；正文和正式回复尚未撰写'))
 progress=pd.DataFrame(progress);assert len(progress)==31;save(progress,G1/'G1_03_Reviewer_Response_Progress.csv')
 consistency=[]
 def con(section,eqno,figure,original,new,difference,change,review,evidence):consistency.append(dict(manuscript_section=section,equation=eqno,figure_table=figure,original_claim=original,new_evidence=new,difference=difference,recommended_revision=change,reviewer_mapping=review,evidence_file=str(evidence)))
 con('§3.3','NA','Fig2','mean daily availability97.30%','无法追溯；原始归档返回槽位60.1610%，合格去重59.8746%；新日均另表','YES_DEFINITION','移除97.30，以实算分母/质量层级重绘','R1-03;R1-10',E01/'E01_03b_Coverage_Weighting.csv')
 con('§3.2–3.4','Eq7','Table1/3/5','H1 1/1、H3 3/3、H6≥5/6','54组合重建主键差异0；H6 50.1699%为5/6','ADDITIONAL_EVIDENCE','增加互斥漏斗、H6完整性与缺失位置','R1-02;R1-05',E01/'E01_10_Fold_Sample_Attrition.csv')
 con('§4.3/§5.3','Eq12','Table7','逐样本三seed平均后算指标','未舍入历史值证明实际Table7采用B；A均值另列','YES_CONFIRMED','保留原基准记录；后续按A重置主文全部对应表图','R1-09;R3-06;R6-04',E03/'E03_03_Original_vs_Recomputed_Table7.csv')
 con('§5.2–5.4','Eq14','Fig6','六fold+Holm无显著支持稳定性','日块估计；15项中7项Holm<.05，XGB-SeasonalHA全不显著','YES_INFERENCE','主文明确estimand、依赖限制与CI；不称等效','R1-01;R2-04;R6-02',E03/'E03_08_Holm_Adjusted_Comparisons.csv')
 con('§5.3','Eq12','Fig4','H1/H3/H6同轴且随机模型原均值','不同未来均值不可跨H比较；A/B数值不一致','YES','按时距分面，A为主、B补充','R1-09;R1-10',E03/'E03_03_Original_vs_Recomputed_Table7.csv')
 con('§5.5–5.6','NA','Fig5','coverage分组/节点顺序解释可靠性','现有可靠性分层含gap、age、volatility和支持；道路里程仍缺','ADDITIONAL_LIMITED','只解释关联；空间横轴暂不能标道路km','R3-10;R3-11',E02/'E02_07_Coverage_Gap_Volatility.csv')
 con('Appendix C','NA','LOFO','排除Fold6令H1/H3 SeasonalHA领先','B重现旧方向；A只有H1转SeasonalHA，H3仍XGB','YES_AGGREGATION_DEPENDENT','主文呈现完整LOFO并分别标明A/B','R1-08;R6-05',E03/'E03_10_LOFO_Stability.csv')
 con('§5.7','NA','Free-flow baseline','缺自由流基准/独立真值','历史滞后FF MAE2.169594/2.172871/2.193327；不是独立真值','NEW_BASELINE_LIMITED','在相同测试交集新增，保留timestamp来源限制','R6-03;R3-12',E02/'E02_10_FreeFlow_Baseline.csv')
 con('§3.4','reliability equation','Table2','7/8特征计数、缺失mask和imputed重复','原特征恢复验证ddof0波动率maxdiff2.26e-6 km/h，重复列定义保留','EDITORIAL_COUNT_ISSUE','后续更正特征计数和等价性说明，不重做本轮分析','R1-10',DER/'feature_recovery_audit.csv')
 consistency=pd.DataFrame(consistency);save(consistency,G1/'G1_Manuscript_Consistency.csv')
 summary=[dict(item='Overall status',value='CONDITIONAL_PASS',evidence='G1_Validation_Checks.csv'),dict(item='formal15min slots',value='403512=241601 quality +1156 only invalid +160755 no archived return',evidence='E01_01'),dict(item='H6 test completeness',value='14521 complete;14620 partial (50.1699% partial)',evidence='E01_06'),dict(item='seed/Table7',value='all18 B means match; 6 stochastic means differ from Equation12 A',evidence='E03_03'),dict(item='A XGBoost foldMAE H1/H3/H6',value='0.935267 /0.819415 /0.744363 km/h',evidence='E03_03'),dict(item='A GRU foldMAE H1/H3/H6',value='1.046958 /0.947604 /0.868938 km/h',evidence='E03_03'),dict(item='XGB-SeasonalHA Daymacro H1/H3/H6',value='+0.077330 /+0.012295 /-0.012050 km/h; all CI include0',evidence='E03_08'),dict(item='Holm15 comparisons',value=f'{int(holm.significant_holm_0_05.sum())}/15 below.05; significance not acceptance criterion',evidence='E03_08'),dict(item='closure',value='NOT_ESTIMABLE no observed events',evidence='E02_09'),dict(item='future maximum training execution budget',value=f'core cap{core_budget}; conditional cap{conditional_budget}; not authorized/executed; failed source gate makes downstream0',evidence='G1_Next_Experiment_Scope.csv')]
 jsonable=lambda df:json.loads(df.where(pd.notna(df),None).to_json(orient='records',force_ascii=False,date_format='iso'))
 books={
 'G1_02_Integrated_Results.xlsx':{'00_Executive_Summary':pd.DataFrame(summary),'01_Data_Coverage':line,'02_Threshold_Comparison':thr,'03_Sample_Attrition':attr,'04_H6_Completeness':h6,'05_Traffic_Distribution':dist[dist.node_id=='ALL'],'06_Traffic_Regime_MAE':reg,'07_Missingness_Reliability':reliab,'08_Selection_Diagnostics':select[select.record_type=='NUMERIC_PROXY'],'09_FreeFlow_Baseline':ff,'10_Seed_Aggregation':seed,'11_Table7_Reconciliation':tab,'12_Statistical_Estimands':est,'13_Bootstrap_Holm':holm,'14_LOFO_Stability':lofo,'15_Next_Experiment_Scope':plan_df,'16_Limitations':pd.DataFrame(limitations)},
 'G1_04_Manuscript_Consistency_Matrix.xlsx':{'Consistency':consistency},
 'G1_05_Minimum_Remaining_Experiment_Plan.xlsx':{'Minimum_Scope':plan_df,'Sample_Feasibility':feas,'Stage_Gates':pd.DataFrame([dict(gate='G1 accepted outputs',rule='Do not repeat E01-E03; reuse unless specific scientific/code issue with recorded change scope'),dict(gate='Source approval',rule='Restore original code; otherwise author approval for independent implementation and6 implementation checks; failure stops all training'),dict(gate='No factor crossing',rule='Each sensitivity one factor only; shared baseline and tuning outputs reused'),dict(gate='Author decision',rule='All proposed training is unexecuted; source/GIS/external approvals remain pending')])}}
 jwrite(CTL/'G1_workbooks_content.json',{file:{sheet:jsonable(df) for sheet,df in sheets.items()} for file,sheets in books.items()})
 counts=progress.response_readiness.value_counts().to_dict();a=est[(est.method=='A_ENSEMBLE_PREDICTION')&(est.model=='XGBoost')]
 report=f'''# APPLIED INTELLIGENCE MAJOR REVISION — G1 E01–E03 FINAL ACCEPTANCE

总体：**CONDITIONAL_PASS**。本阶段实际完成E01/E02/E03全部可执行计算；非可估计问题逐项保留。未训练、未调参、未下载外部交通数据、未改文、未写正式回复。协议冻结于新误差统计之前：`{PROTOCOL}`，SHA256 `{PROTOCOL_SHA}`。

## G0继承与本轮执行

复用G0的544项哈希和180次预测历史验收，没有重新全量G0审核。只对本轮使用的数据进行主键/字段/真值/层级和单位关联。原83天返回CSV经ID+速度/置信度等字段及重复次序，与cleaned一对一映射，日期仍沿用cleaned修复时间，未宣称恢复原日期修复程序。共享中间层和商业明细只在`{DER}`本机保存，不入ZIP。

180份预测已按共同key对齐；A/B比较需要补充提取两种随机模型108个文件的逐样本B损失，该补充只做一次并缓存，没有重跑模型或重复连接全部180份。原始与新计算分开标记ORIGINAL_FROZEN_BASELINE/REVISION_E01_E03。

## E01主要实算发现

15min正式分母403512，小时分母100878。403512=241601有合格记录槽位+1156仅不合格返回槽位+160755归档无返回槽位。原始唯一返回242757槽位，比例60.160995%（不等于原文把241601称原返回的59.87%）；质量合格去重覆盖59.874552%。行级244477=243307合格+1170不合格，与槽位漏斗明确区分。网格外126行/合格唯一槽位另列，不混分母。

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
{holm[holm.comparison=='XGBoost_vs_SeasonalHA'][['horizon','effect','CI_low','CI_high','raw_p','holm_adjusted_p']].to_string(index=False)}
```

三项区间均跨0，没有支持XGB稳定优于SeasonalHA。15项预设比较中{int(holm.significant_holm_0_05.sum())}项Holm<.05，显著性不作为验收标准。全体41个真实有效测试日期连续，3日可用39个起点、7日35个起点；10000次固定种子20261125，日期整体含全部节点。双侧p来自零假设中心化重采样并作(B+1)有限修正，不是未经中心化的正负比例。普通95%区间非同时区间，percentile CI与中心化检验不必严格互为对偶。

四权重及A/B：

```text
{a[['horizon','estimand','MAE','delta_XGBoost_minus_SeasonalHA']].to_string(index=False)}
```

B重建原205个day×spatial-block MAE单元格至浮点精度；原XGB−SeasonalHA点估计+0.068424/+0.025185/+0.022590由B及原空间权重共同产生。新A的日块效应不是原fold均值，方向变化由实际分解证明，不能全部归于单一因素。旧bootstrap程序未恢复，旧CI只保留，不声称完整复现。HAC/DM按冻结方案不另做，不能依p值临时添加。

LOFO的六种单fold排除完整呈现，非重新训练CV。A下排除Fold6：H1 SeasonalHA领先，H3/H6仍XGB；旧文H1/H3均转SeasonalHA属于B口径，必须后续一起修正。H1排除Fold3或4又有Persistence领先，稳定性依赖估计量与测试区间。Fold5/6分布和误差只用于描述，没有下载日历或宣称节日导致误差。

## 审稿证据、未解决问题与下一阶段范围

31条原始意见完整保留，不覆盖G0矩阵。进度分类：{counts}。这些是数据证据进度，不代表审稿满意或录用概率。仅方法说明、GIS/日历、文献、训练反事实、独立外推分别保留，正式回复与论文尚未修改。

基于实际支持冻结的下一阶段建议：1/4规则全六模型×全三时距，3/4只H1可做完整六fold；4/4不强做预测训练；H6严格6/6需训练；一种因果插补对照；12/48h仅代表性XGB/GRU与H1/H6端点；框架两组件分别用Ridge/XGB端点对照；有限Ridge/XGB/GRU验证候选；GRU静态信息；最多一个轻量时空候选保持条件性。未做全因子交叉。

运行上限计算见`{G1/'G1_Next_Experiment_Scope.csv'}`及计划工作簿：核心建议上限{core_budget}个“模型×时距×fold×seed/配置执行”（含廉价确定性基准计算，不全是梯度训练），条件项额外上限{conditional_budget}。这是各门均通过时的保守最大和，不是自动执行任务量。调参上限162候选+72选中模型额外seed=234，选中seed42候选不重复训练；任何已证明同实现/输入/协议的基准和候选复用。源码门先6个实现验证，不通过则所有后续训练预算归0；不能据新测试排名挑参数。三个正式入口仍缺失，作者需批准独立新实现，或提供原源码。

E07 freeflow基准REUSE_EXISTING；道路中心线与累计公里、官方节日日历和公平硬件成本仍待核实，不需要重新跑E01–E03。E08仍条件性，不因内部结果不好扩大数据范围；独立时段验证时间外推，外部走廊验证域差，外地检测器不能验证Sarawak原位车速或取消已暴露测试历史。

## 验收与执行限制

统一验收记录：`{G1/'G1_Validation_Checks.csv'}`。曾发现历史空间块对照join日期层名称不一和CSV p值舍入机械下界误报，均保留失败记录，定向修复；没有修改协议、主要估计量、p值或已通过计算。没有重复整个E01–E03。

后续遵守：已验收且输入/协议/代码未变的结果直接REUSED_PASS；只对具体科学或代码问题登记原因、影响和受影响任务后定向处理。原始FCD、逐样本预测、派生速度、特征张量和权重不入ZIP。聚合结果及诊断只含统计摘要；商业公开许可仍未确认，本机交付不代表公开授权。

七核心交付绝对路径：

'''
 names=['G1_01_E01_E03_Result_Registry.csv','G1_02_Integrated_Results.xlsx','G1_03_Reviewer_Response_Progress.csv','G1_04_Manuscript_Consistency_Matrix.xlsx','G1_05_Minimum_Remaining_Experiment_Plan.xlsx','G1_06_Acceptance_Report_CN.md','G1_07_Execution_Manifest.json']
 report+='\n'.join(f'- `{G1/n}`' for n in names)
 report+=f'\n\n最终ZIP：`{ROOT/"APIN_G1_E01_E03_Results_20261125.zip"}`。本阶段停止，等待作者检查和确认下一阶段建议规模；不自动训练或修文。\n'
 (G1/'G1_06_Acceptance_Report_CN.md').write_text(report,encoding='utf-8')
 jwrite(CTL/'G1_deliverable_context.json',{'core_budget_cap':core_budget,'conditional_budget_cap':conditional_budget,'reviewer_progress_counts':counts,'validation_status':validation['overall_status'],'outputs':[str(G1/n) for n in names],'report_ready_at':now()})
 log(f'G1 report/scopes assembled; core cap{core_budget}; conditional cap{conditional_budget}; all training pending author/source gate')
if __name__=='__main__':main()
