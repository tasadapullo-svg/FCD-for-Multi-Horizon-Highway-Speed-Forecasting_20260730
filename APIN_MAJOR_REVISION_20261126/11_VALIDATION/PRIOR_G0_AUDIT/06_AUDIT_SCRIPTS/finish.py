import sys,json,csv,re,hashlib,zipfile,io,datetime,os
from pathlib import Path
C=json.loads(Path(__file__).with_name('config.json').read_text(encoding='utf8')); O=Path(C['out']); R=Path(C['root']); H=Path(C['hist']); repo=H/'20260730_AJSE_FINAL_GitHub'; P=repo/'04_PHASE2A_DATA_RESULTS'
sys.path.insert(0,str(O/'06_AUDIT_SCRIPTS/deps'))
import pandas as pd,numpy as np
from pypdf import PdfReader
def save(name,rows,fields=None):
 rows=list(rows); fields=fields or list(dict.fromkeys(k for r in rows for k in r)) or ['status','reason']
 with (O/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

import yaml
inv=pd.read_csv(O/'00_MANIFESTS/G0_file_inventory.csv').fillna('');zi=pd.read_csv(O/'00_MANIFESTS/G0_zip_crc_inventory.csv').fillna('');cfg=yaml.safe_load((P/'00_DEFINITION_FREEZE/phase2a1_frozen.yaml').read_text());hp=P/'01_DATA_PIPELINE/panels/hourly_panel_all_thresholds.parquet';hour=pd.read_parquet(hp).set_index('panel_row_id');rebuild=[]
for p in (P/'01_DATA_PIPELINE/folds').rglob('sample_manifest*.parquet'):
 df=pd.read_parquet(p);bad=0;bad_hist=0
 idslist=[[int(s) for s in re.findall(r'\d+',s)] for s in df.target_row_ids]; allids=np.array([v for ids in idslist for v in ids]); lens=np.array([len(ids) for ids in idslist]); vals=hour.loc[allids,'observed_speed'].to_numpy(); labels=np.repeat(np.arange(len(df)),lens); sums=np.bincount(labels,weights=np.nan_to_num(vals),minlength=len(df)); ns=np.bincount(labels,weights=np.isfinite(vals).astype(int),minlength=len(df)); actual=sums/ns;bad=int((~np.isclose(actual,df.target.to_numpy(),rtol=0,atol=1e-12)).sum());bad_hist=int(sum(len(re.findall(r'\d+',s))!=24 for s in df.history_row_ids))
 rebuild.append(dict(path=str(p),rows=len(df),target_value_mismatches=bad,history_length_mismatches=bad_hist,status='PASS_RECALCULATED' if not bad and not bad_hist else 'MISMATCH'))
save('01_DATA_LINEAGE/G0_target_rebuild_audit.csv',rebuild)
print('TARGET DONE',flush=True)
# Checkpoint ZIP structure only; never unpickle.
cks=[]
for p in (P/'03_FORMAL_PREDICTIONS/checkpoints').glob('*.pt'):
 try:
  with zipfile.ZipFile(p) as z:names=z.namelist();bad=z.testzip()
  cks.append(dict(path=str(p),crc_ok=bad is None,has_data_pkl=any(s.endswith('data.pkl') for s in names),storage_members=sum('/data/' in s for s in names),status='PASS_HASH_ONLY',reason='容器CRC核验；未反序列化，结构形状及state_dict尚未核验'))
 except Exception as e:cks.append(dict(path=str(p),status='NOT_VERIFIED',reason=str(e)))
save('03_CODE_AND_RESULTS/G0_checkpoint_container_audit.csv',cks)
# Existing inferential numbers, signs and Holm arithmetic only.
a=pd.read_csv(P/'05_STATISTICS/corrected_fold_pairwise_tests_holm.csv');b=pd.read_csv(P/'05_STATISTICS/clustered_day_spatial_block_bootstrap.csv');ss=[]
for h,g in a.groupby('horizon'):
 order=g.sort_values('raw_p');calc=np.minimum(1,np.maximum.accumulate(order.raw_p.to_numpy()*np.arange(len(order),0,-1)))
 for (_,r),v in zip(order.iterrows(),calc):
  br=b[(b.horizon==h)&(b.comparison==r.comparison)];ss.append(dict(comparison=r.comparison,horizon=h,raw_p=r.raw_p,saved_adjusted_p=r.adjusted_p,recalculated_holm=v,fold_difference=r.mean_difference_a_minus_b,block_difference=br.mean_difference_a_minus_b.iloc[0] if len(br) else '',status='PASS_RECALCULATED' if abs(v-r.adjusted_p)<1e-12 else 'MISMATCH',reason='原始p值沿用既存统计；只复核Holm算术，未执行新检验/bootstrap'))
save('03_CODE_AND_RESULTS/G0_statistics_existing_results_alignment.csv',ss)
lineage=[]
for i,(name,inp,outp,code,status) in enumerate([
 ('API→cleaned','原始API归档候选','tomtom_cleaned_records.csv.gz','解析生成代码未定位','NOT_VERIFIED'),('cleaned→15min','ZIP中已匹配raw hash','deduplicated_15min_observations.parquet','src/build_phase2a1_data.py','MISSING_CODE'),('15min→hourly','deduplicated_15min_observations.parquet',str(hp),'src/build_phase2a1_data.py','MISSING_CODE'),('hourly→targets',str(hp),'18 manifests','target_rebuild_audit.csv','PASS_RECALCULATED'),('manifest→prediction','18 manifests','180 predictions','src/run_phase2a1_campaign.py','MISSING_CODE'),('prediction→metric','180 predictions','180 MAE/RMSE','data.py / extended.py','PASS_RECALCULATED'),('metric→Table7','180 metrics','36 mean/SD cells','extended.py','PASS_RECALCULATED'),('metric→statistics','saved stats','Holm adjusted p','finish.py','PASS_RECALCULATED')]):
 lineage.append(dict(stage_id=i+1,upstream_stage=i,input_path=inp,input_sha='',script_path=code,config_path=str(P/'00_DEFINITION_FREEZE/phase2a1_frozen.yaml'),output_path=outp,output_sha='',rows_in='',rows_out='',key_fields='sample_id / node_id×time',filter_rule=name,provenance_status=status,evidence='各专用核验CSV；PASS不代表缺失生成代码已恢复'))
save('01_DATA_LINEAGE/G0_data_lineage.csv',lineage)
gaps=[('BLOCKER','正式Phase2A1训练及构建源码','src/build_phase2a1_data.py; src/run_phase2a1_campaign.py; src/finalize_phase2a1.py','MISSING_CODE','从冻结commit原工作树或原运行机器恢复src及依赖模块'),('MAJOR','全部论文数字逐项语义核验','正文、附录、公式、图内标注','NOT_VERIFIED','完成数字索引人工语义分类及源表逐单元格关联'),('MAJOR','97.30%日级覆盖率','分子分母、原图生成脚本','AMBIGUOUS_DEFINITION','核实既有Fig2数据包定义与生成链'),('MAJOR','API响应至cleaned CSV','API ZIP候选存在；解析与清洗链尚未逐条桥接','NOT_VERIFIED','现有API源文件与source_file字段映射及原清洗入口'),('MAJOR','Fig1 GIS里程与图源','nodes/geojson候选已登记，真实roadline及里程生成链未证','NOT_VERIFIED','原roadline GIS和图像生成脚本、CRS/距离计算方法'),('LIMITATION','审稿原文','仅找到先前审稿审计摘要，非原始邮件','MISSING_LOCAL_DATA','原始Reviewer #1/#2/#3/#6邮件或导出正文'),('MAJOR','环境锁与硬件','requirements与记录候选存在；未证正式运行完整锁','NOT_VERIFIED','正式运行pip/conda lock、硬件与运行命令日志'),('LIMITATION','商业数据分发许可','公开仓库包含预测/面板，历史许可限制需核对','LICENSE_REVIEW_REQUIRED','TomTom许可及派生数据授权范围'),('MAJOR','所有图源与原PNG的生成关系','Fig1–6候选均已索引，尚未证明每个PNG的唯一来源','NOT_VERIFIED','原绘图脚本、输入哈希、输出图SHA记录')]
issues=[]
for i,(sev,claim,actual,status,fix) in enumerate(gaps,1):issues.append(dict(issue_id='G'+str(i),severity=sev,claim_or_file=claim,expected='完整可追溯',actual=actual,unit='',exact_evidence='G0_code_inventory.csv / G0_figure_alignment.csv / G0_paper_numeric_alignment.csv',root_cause_confirmed_or_hypothesis='缺失或本轮未完成核验，禁止推断不存在',minimal_fix=fix,owner_action='恢复现有证据或继续只读核验',blocks_G1=sev=='BLOCKER',status=status))
save('04_REVIEW_AND_GAPS/G0_missing_files_and_blockers.csv',issues);save('04_REVIEW_AND_GAPS/G0_discrepancy_register.csv',issues);save('04_REVIEW_AND_GAPS/G0_manual_verification_queue.csv',[x for x in issues if x['status']=='NOT_VERIFIED'])
reviews=[]
prior=Path('D:/Desktop/2026112_论文修改/APIN_D_26_12623_审稿意见_数据充分性与定向补实验审计_20261121.md').read_text(encoding='utf8')
for line in prior.splitlines():
 if re.match(r'\| R[1236]-',line):
  cols=[s.strip() for s in line.split('|')[1:-1]];key=cols[0];reviews.append(dict(reviewer=key.split('-')[0],comment_id=key,review_comment_excerpt=cols[1],paper_location='待与原始审稿信核对',existing_data_ref='01_DATA_LINEAGE/',existing_result_ref='03_CODE_AND_RESULTS/',alignment_status='NOT_VERIFIED',evidence_gap='当前引用为历史审稿摘要，不是原始审稿原文；各意见所需证据见缺口表',requires_G1_decision=True))
save('04_REVIEW_AND_GAPS/G0_review_comment_evidence_map.csv',reviews)
# Submission ZIP/source byte relationships.
versions=[]
for n in ['main.tex','Fig1.png','Fig2.png','Fig3.png','Fig4.png','Fig5.png','Fig6.png','references.bib']:
 p=R/'Applied_Intelligence_20260905'/n;h=sha(p);copies=inv[inv.relative_path.map(lambda s:Path(s).name==n)];z=zi[zi.entry.map(lambda s:Path(s).name==n)];versions.append(dict(name=n,authoritative_source_sha256=h,physical_matching_copies=int((copies.sha256==h).sum()),zip_matching_copies=int((z.sha256==h).sum()),status='PASS_HASH_ONLY',reason='同哈希仅证明字节版本对应'))
save('02_PAPER_ALIGNMENT/G0_submission_version_alignment.csv',versions)
claims=pd.read_csv(O/'02_PAPER_ALIGNMENT/G0_paper_numeric_alignment.csv');counts=claims.status.value_counts().to_dict();integrity=pd.read_csv(O/'03_CODE_AND_RESULTS/G0_formal_180_run_integrity.csv');metrics=pd.read_csv(O/'03_CODE_AND_RESULTS/G0_saved_metrics_recalculation.csv');comparison=pd.read_csv(O/'00_MANIFESTS/G0_github_freeze_comparison.csv');summary=json.loads((O/'00_MANIFESTS/inventory_summary.json').read_text());stage=pd.read_csv(O/'01_DATA_LINEAGE/G0_pipeline_stage_counts.csv');primary=pd.read_csv(O/'02_PAPER_ALIGNMENT/G0_primary_table_cell_verification.csv')
tree=json.loads((O/'00_MANIFESTS/github_tree.json').read_text())
report=f'''# G0审计报告（未达到全量验收）
生成时间：{datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()}。

结论：G0_BLOCKED。已完成资产冻结及正式预测核心核验；未完成所有数字、图内标注、全部图源、原始API解析链与训练源码的全面对应。不得把本报告视为G0全部要求已完成。未进入G1/G2/G3。

1. 范围：投稿目录、同项目历史投稿全树、当前工作目录；依元数据检查D:/2026_07_23及D:/2026_AJSE_FINAL，均不存在。无全D盘扫描。物理文件{summary['files']}，含文件目录{summary['dirs']}，字节{summary['bytes']}，ZIP条目{summary['zip_entries']}，CRC错误{summary['errors']}；SHA均计算。目录数是含文件目录去重数，不含空目录总数。
2. 仓库：实际读取公开main树 {tree['sha']}；通过本地文件Git blob SHA1与远端对象比较（不是远端SHA256下载比较）。状态{comparison.status.value_counts().to_dict()}。本地是导出目录，不能据此声称本地git clean；历史freeze json中的clean仅为历史记录。
3. 投稿版本：EM稿61页，PDF提取已保存，含重复Supporting File；数字候选从唯一投稿main.tex提取，不重复计Supporting稿。preview仅作版本登记，不作正式原稿。源文件/图片与ZIP字节对应见G0_submission_version_alignment.csv。未重新编译论文，PDF逐页视觉和全文与TeX逐字对应未完成。
4. 数据：cleaned输入在PanBorneo_TomTom_Cleaned_Experiment_Package.zip中，SHA与pipeline raw_sha一致；51节点输入SHA同样一致。CSV有34列，历史RAW_INPUT_METADATA只列14项，不能将历史列清单当作完整schema。raw=244477，quality-pass=243307，confidence fail=1170；原始全时段去重241727，冻结完整小时网格去重241601，边界差126条。首个不完整小时导致全原始span planned=403665，与正式complete-hour grid 403512分开。完整小时1/4、2/4、3/4、4/4计数96968、83439、45356、15838已从原始CSV独立复算。冻结面板逐速度与raw去重结果的全量连接尚未完成，因此不把每个箭头判为复现通过。
5. 180运行：注册180，预测180，18份manifest，54份GRU checkpoint容器存在且CRC检查；模型不加载、不推理、不反序列化。预测哈希、manifest哈希、测试ID和标签精确对应、有限数、行数通过{int((integrity.status=='PASS_RECALCULATED').sum())}/180。MAE/RMSE独立复算与已存逐运行指标通过{int((metrics.status=='PASS_RECALCULATED').sum())}/180。样本时间边界及目标由panel_row_id复算另见专表；尚未独立证明全部scaler/填补fit scope及训练真实实现。
6. 真正Phase2A1训练源码：三入口在已扫描物理文件、全部嵌套ZIP、公开tree未定位，MISSING_CODE。Phase2A0及Phase13均未冒充正式训练实现。环境记录并非完整版本锁。
7. 论文数字：自动候选{len(claims)}，状态{counts}。其中Table7主MAE表36单元格通过{int((primary.status=='PASS_RECALCULATED').sum())}/36。候选含编号/引文等待语义剔除，不能当作全部事实数字分母；真正全量数字核验覆盖率未确定，绝不声称100%。其余表、正文、附录、公式、图内标注未全量核验，详见索引与人工队列。当前不能给出“全部数字无冲突”的结论，也不虚构十大已确认冲突。
8. Fig1–Fig6：PNG哈希与候选数据/脚本索引已保存；Fig1 nodes CSV和GeoJSON实际在归档中存在。未证明道路中心线里程、所有图内标注及投稿图唯一生成链。97.30%尚未澄清，不判PASS。
9. 统计：未重做Wilcoxon/bootstrap；仅对原存raw p复核Holm算术，保存fold/block差值。6折exact双侧最小p=2/64=0.03125，五项Holm第一项最低0.15625；此为算术边界，不是新推断。污染测试及许可限制沿用冻结配置与原有证据，不能称独立盲测或真实地面速度验证。
10. 可复用：已核验预测、manifest、逐运行MAE/RMSE、主MAE表；须保留原样并注明供应商速度目标与回顾性评估。数据链全追溯、完整训练复现、所有表图来源仍不能证明。原始审稿信未找到，只从历史审稿摘要建立31条映射，不冒充原文核对。
11. G1：当前不具备用户要求的G0全量验收基础。至少先恢复正式src或明确接受不可复现限制，并完成数字/图表/原始API现有证据的剩余只读核验。任何新实验仅留待用户决定；本轮未训练、未采集、未改原始文件或论文、未绘图、未上传。

输出按规定目录保存；各CSV中NOT_VERIFIED是未做完或未获证，不能等同文件缺失。G0_missing_files_and_blockers.csv给出最小补件，G0_manual_verification_queue.csv列未完成核验。本轮交付文件虽齐，但任务的全量审计验收尚未完成。
'''
(O/'05_REPORTS/G0_FULL_AUDIT_REPORT.md').write_text(report,encoding='utf8');(O/'05_REPORTS/G0_EXECUTIVE_VERDICT.md').write_text(report,encoding='utf8');(O/'05_REPORTS/G0_G1_HANDOFF_NO_EXPERIMENTS.md').write_text('G0_BLOCKED。尚未完成全量数字/表图/API链及训练源码验证。详见缺口登记；不得开始训练、修文、绘图或统计推断。仅登记后续决策，不制定G1实验定稿。',encoding='utf8')
(O/'README_G0_SCOPE.md').write_text('仅G0只读审计；当前未达到全量验收，见05_REPORTS。全部原始文件只读。审计运行顺序：python -X utf8 06_AUDIT_SCRIPTS/audit.py；core.py；data.py；extended.py；finish.py。配置在config.json。依赖仅安装于审计输出目录deps。派生CSV不含逐样本商业记录，PDF提取仅本机。重跑脚本会覆盖本轮派生审计表，须先另建新输出目录并更新config。',encoding='utf8')
(O/'07_LOGS/G0_environment_snapshot.txt').write_text(sys.version+'\npandas '+pd.__version__+'\nnumpy '+np.__version__,encoding='utf8')
print('REPORT DONE',flush=True)
