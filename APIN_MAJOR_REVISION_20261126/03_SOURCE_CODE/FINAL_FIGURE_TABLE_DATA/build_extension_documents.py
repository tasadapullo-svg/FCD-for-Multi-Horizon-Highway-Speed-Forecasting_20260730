from pathlib import Path
import json,shutil,hashlib,re
import pandas as pd

R=Path(r'E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改');B=R/'07_FIGURES_TABLES/FINAL_FIGURE_TABLE_DATA';M=B/'08_MASTER_RESEARCH_RESULTS';V=B/'09_QGIS_VALIDATION';P=B/'GPT_SCI_PLOTTING_DATA';P.mkdir(exist_ok=True)
S=R/'04_EXPERIMENTS'
def src(n):return next(S.rglob(n+'.csv'))
def csv(n):return pd.read_csv(src(n))
def save(x,p):x.to_csv(p,index=False,encoding='utf-8-sig')
def rel(p):return str(p.relative_to(B)).replace('\\','/')
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(x,n=8):
 y=x.head(n).fillna('');cols=list(y.columns)
 def cell(v):return str(round(v,4) if isinstance(v,float) else v).replace('|','/').replace('\n',' ')
 return '\n'.join(['| '+' | '.join(map(str,cols))+' |','| '+' | '.join(['---']*len(cols))+' |']+['| '+' | '.join(cell(v) for v in row)+' |' for row in y.itertuples(index=False,name=None)])
lineage=csv('E01_01_Data_Lineage_and_Coverage'); main=csv('E03_03_Original_vs_Recomputed_Table7'); stat=csv('E03_08_Holm_Adjusted_Comparisons'); claims=csv('Final_Scientific_Claims_Registry'); g2=csv('G2_02_Experiment_Run_Registry').rename(columns={'test_MAE':'test_mae'}); review=csv('FINAL_Reviewer_Evidence_Matrix_v2').fillna(''); ridge=csv('Ridge_Corrected_Aggregates'); gis=csv('GIS_Corridor_Length_Reconciliation'); h6=csv('E01_06_H6_Target_Completeness')
main_small=main[['model','horizon','method_A_value','method_B_value','method_A_fold_sd']].sort_values(['model','horizon']); stat_small=stat[['horizon','comparison','effect','CI_low','CI_high','raw_p','holm_adjusted_p','significant_holm_0_05']]
groups=[('R01','Data collection and availability','数据采集与可用性','Observation availability',lineage[['metric','value','statistical_level']],'E01_01_Data_Lineage_and_Coverage.csv','Fig02 / Table01','Different row and slot denominators; missingness is not zero speed.'),('R02','Forecast target and eligibility','预测目标与样本资格','H1/H3/H6 support',h6.head(12),'E01_06_H6_Target_Completeness.csv','Fig03 / Table03,05','H6 partial 5/6 and complete 6/6 targets must remain distinct.'),('R03','Original six-model results','原六模型预测结果','Method A versus Method B',main_small,'E03_03_Original_vs_Recomputed_Table7.csv','Fig04 / Table07','Original Method A uses per-sample three-seed ensemble; Method B is mean seed metric.'),('R04','Statistical inference','统计推断','15 prespecified contrasts',stat_small,'E03_08_Holm_Adjusted_Comparisons.csv','Fig06 / Table07','Three-day block bootstrap is primary; ordinary CIs are not simultaneous Holm CIs.'),('R05','Traffic regime and reliability','交通状态与可靠性','Conditional error',csv('E02_04_Traffic_Regime_Distribution'),'E02_04_Traffic_Regime_Distribution.csv','Fig05,07 / Table07','Provider speed and free-flow proxies are not independent observed true speed.'),('R06','Data and protocol sensitivity','数据与协议敏感性','Native and common-origin estimands',g2[g2.condition.isin(['base','threshold1','threshold3','strict6','seasonal_impute','history12','history48'])][['condition','model','horizon','fold','test_n','test_mae']].head(20),'G2_02_Experiment_Run_Registry.csv','Fig08 / Table08','Threshold 4/4 was not estimable; native and common-origin supports differ.'),('R07','GATE-FCD ablation','GATE-FCD消融','Protocol contrast',csv('E05_Native_Eligibility_Set_Check'),'E05_Native_Eligibility_Set_Check.csv','Fig08 / Table08','Noncausal scaling is leakage diagnostic, not a valid performance rank.'),('R08','Model fairness and numerical correction','模型公平性与数值修正','Ridge SVD corrected native metrics',ridge,'Ridge_Corrected_Aggregates.csv','Fig08 / Table04,08','Do not reuse old Cholesky paired contrasts as corrected SVD paired inference.'),('R09','Spatial and operational evidence','空间与运行证据','Distance estimands',gis,'GIS_Corridor_Length_Reconciliation.csv','Fig01 / Table09','Current OSM paths do not verify historical 130 km mainline.'),('R10','Claims and limitations','科学结论与限制','Claim registry',claims,'Final_Scientific_Claims_Registry.csv','All figures and reviewer matrix','E08 target asset absent; no external validation or trained spatial-neighbor model.')]
def report(lang):
 cn=lang=='CN';title='# 全部科研结果汇总（冻结证据，非论文正文）' if cn else '# Complete Research Results Summary (Frozen Evidence; Not Manuscript Text)'
 t=[title,'',f"**Project:** APIN-D-26-12623. **Historical runs:** 180 original, 651 G2, 93 Ridge diagnostic. **New fits:** 0. **New traffic datasets:** 0.",'',('主结果：G1 Method A，三种子逐样本集成。原稿部分数字对应Method B，不能互换。G2是独立返修实现。' if cn else 'Primary original result: G1 Method A, a per-sample three-seed ensemble. Some manuscript numbers reflect Method B and are not interchangeable. G2 is an independent revision implementation.'),'']
 for eid,en,zh,q,x,file,fig,limit in groups:
  t += [f'## {eid} — {zh if cn else en}','',f"- **Experiment ID:** {eid}",f"- **Scientific question:** {zh if cn else q}",f"- **Input data:** Frozen accepted aggregate `{file}`; source and SHA-256 in Master_Aggregate_Provenance.csv.",f"- **Experimental design / models / horizons:** {('按冻结协议；详见本组完整CSV，未重训。' if cn else 'Frozen protocol; see complete category CSV. No retraining.')}",f"- **Sample support:** {len(x)} rows in the display summary; full counts in source CSV.",f"- **Main numerical results:**",'',table(x,10),'',f"- **Statistical significance:** {('仅R04所列预设比较及相应冻结证据用于推断；其他描述性。' if cn else 'Only prespecified R04 comparisons and their frozen evidence support inference; other summaries are descriptive.')}",f"- **Scientific interpretation / limitations:** {limit}",f"- **Reviewer comments:** See APIN_03 mapping, original 31 comments preserved.",f"- **Proposed manuscript section / figures and tables:** {fig}",f"- **Source data file:** `08_MASTER_RESEARCH_RESULTS/{next(k for k in [d.name for d in M.iterdir() if d.is_dir()] if k.startswith(eid))}/{file}`",'']
 t += ['## '+('数值边界与未完成事项' if cn else 'Numerical boundaries and unavailable evidence'),'',table(claims[['claim_id','proposed_claim','support_status','scope_or_limitation']],20),'',('E08未运行；51个GIS节点与50段当前OSM路径不证明历史主线；15节点需作者人工复核。商业数据分发许可未确认。' if cn else 'E08 was not run. The 51 GIS nodes and 50 current-OSM routes do not prove the historical mainline. Fifteen nodes require author review. Commercial data distribution rights remain unconfirmed.'),'']
 return '\n'.join(t)
(M/'APIN_01_Complete_Research_Results_Summary_CN.md').write_text(report('CN'),encoding='utf-8');(M/'APIN_01_Complete_Research_Results_Summary_EN.md').write_text(report('EN'),encoding='utf-8')

# Copy plotting data into a self-contained review layout; restricted node-level and geographic coordinates remain local only.
figure_dirs=sorted((B/'01_FIGURE_DATA').iterdir());fregistry=[]
for idx,d in enumerate(figure_dirs,1):
 dest=P/(['Fig01_GIS_Review_Evidence','Fig02_Data_Completeness','Fig03_Gate_FCD_Framework','Fig04_Model_Performance','Fig05_Reliability_and_Spatial_Error','Fig06_Statistical_Inference','Fig07_Traffic_Regime','Fig08_Sensitivity_and_Model_Fairness'][idx-1]);dest.mkdir(exist_ok=True)
 copied=[]
 for p in d.glob('*.csv'):
  if idx==1:continue
  if idx in [2,3,5] and any(k in p.name.lower() for k in ['node_','_nodes','data_dictionary']):continue
  shutil.copy2(p,dest/p.name);copied.append(p.name)
 if idx==1:
  for p in [src('GIS_Corridor_Length_Reconciliation'),V/'GIS_00_File_and_Layer_Inventory.csv']:
   shutil.copy2(p,dest/p.name);copied.append(p.name)
 wb=next((p for p in d.glob('*.xlsx') if 'Plot_Data' in p.name or p.name.endswith('Design.xlsx')),None)
 if wb and idx not in [2,3,5]:shutil.copy2(wb,dest/'Plot_Data.xlsx')
 else:
  from openpyxl import Workbook
  w=Workbook();s=w.active;s.title='Panel registry';s.append(['panel_csv','rows','columns'])
  for name in copied:
   x=pd.read_csv(dest/name);s.append([name,len(x),len(x.columns)])
   if idx==1:
    t=w.create_sheet(name[:31]);t.append(list(x.columns))
    for row in x.fillna('').itertuples(index=False,name=None):t.append(list(row))
  w.save(dest/'Plot_Data.xlsx')
 prov=pd.DataFrame([{'panel_csv':n,'sha256':sh(dest/n),'source':f'Original Prompt06 figure dataset {d.name}','status':'AGGREGATE_GPT_REVIEW'} for n in copied]);save(prov,dest/'Data_Provenance.csv')
 diction=pd.DataFrame([{'panel_csv':n,'column':c,'dtype':str(pd.read_csv(dest/n,nrows=1)[c].dtype)} for n in copied for c in pd.read_csv(dest/n,nrows=1).columns]);save(diction,dest/'Data_Dictionary.csv')
 caption=(d/'README_CN.md').read_text(encoding='utf-8').split('建议英文图题：')[-1].split('\n')[0] if (d/'README_CN.md').exists() else d.name
 (dest/'Recommended_English_Caption.md').write_text(caption+'\n',encoding='utf-8')
 spec=f'# {d.name} design specification\n\nObjective: {caption}.\n\n'
 for n in copied:
  x=pd.read_csv(dest/n,nrows=1);cols=list(x.columns);spec+=f'## {n}\n\nPlot: choose line/bar/point according to variable type; X: {cols[0] if cols else "N/A"}; Y: '+(', '.join(c for c in cols if c.lower() in ['value','mae','coverage','effect','count','ratio']) or 'see actual numeric columns')+'; grouping: model/horizon/condition when present. Axis units, sample annotation, CI/p-value and category order must follow actual columns and source README. No missing CI or p-value should be filled.\n\n'
 (dest/'Figure_Design_Specification.md').write_text(spec,encoding='utf-8');(dest/'README_CN.md').write_text(f'{d.name}：{len(copied)}个可独立读取的聚合CSV。受限节点级或坐标数据仅留作者本地包；Fig.1只供GIS汇总证据，完整空间文件在本地QGIS包。\n',encoding='utf-8')
 fregistry.append({'figure_id':f'Fig{idx:02d}','copied_panel_csv':len(copied),'plot_workbook':str((dest/'Plot_Data.xlsx').relative_to(P))})
save(pd.DataFrame(fregistry),P/'Figure_Package_Registry.csv')

prior=pd.read_csv(B/'06_REVIEWER_MAPPING/Final_31_Reviewer_Figure_Table_Mapping.csv').fillna('');fig_by_id=dict(zip(prior.comment_id,prior.related_figure_table))
revmap=pd.DataFrame([{'reviewer_id':r.reviewer_id,'comment_id':r.comment_id,'original_comment':r.original_comment,'scientific_issue':r.scientific_issue,'completed_experiment_evidence':r.actual_final_evidence,'main_numerical_result':r.G1_key_result,'statistical_basis':r.statistical_basis,'significance_status':r.significance_status,'related_figure_table':fig_by_id.get(r.comment_id,''),'figure_panel':'See related figure panel CSV; no artificial panel assignment','supplementary_data':'See R01–R10 source groups','result_files':r.final_evidence_paths,'manuscript_section':r.manuscript_section,'resolved_status':r.final_adoption_status,'unresolved':r.remaining_work,'scientific_interpretation':r.response_strategy,'author_confirmation':r.remaining_author_action} for r in review.itertuples()]);save(revmap,M/'APIN_03_Reviewer_31_Evidence_and_Figure_Mapping.csv')

# Payloads for the existing spreadsheet exporter.
def sheetspec(name,x):return {'name':name[:31],'title':name,'source':'frozen accepted evidence','headers':list(x.columns),'rows':x.fillna('').values.tolist()}
gfiles=sorted(V.glob('GIS_*.csv'));gis_sheets=[sheetspec(p.stem,pd.read_csv(p).head(1000)) for p in gfiles]
gis_sheets.insert(0,sheetspec('00_Executive_Summary',pd.DataFrame([{'original_nodes':51,'matched_nodes':51,'routes':50,'review_candidates':15,'road_features':1598,'qgz':'QGIS_PROJECT_NOT_RUNTIME_VERIFIED','historical_length':'NOT_VERIFIED'}])))
payload={'workbooks':[{'file':'APIN_QGIS_Validation_Master.xlsx','dir':str(V.relative_to(R)).replace('\\','/'),'sheets':gis_sheets},{'file':'APIN_03_Reviewer_31_Evidence_and_Figure_Mapping.xlsx','dir':str(M.relative_to(R)).replace('\\','/'),'sheets':[sheetspec('31 Reviewer comments',revmap)]}]}
(R/'03_CODE/FINAL_FIGURE_TABLE_DATA/extension_workbook_payload.json').write_text(json.dumps(payload,ensure_ascii=False,default=str),encoding='utf-8')
print('REPORTS 2 FIGURES',len(fregistry),'REVIEWER',len(revmap),'GIS_SHEETS',len(gis_sheets))
