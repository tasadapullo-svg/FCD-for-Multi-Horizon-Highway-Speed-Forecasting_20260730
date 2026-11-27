"""Prepare frozen, author-local plot CSVs, table CSV/TeX, supplements, and workbook payload."""
from pathlib import Path
import json,hashlib,datetime,re
import numpy as np,pandas as pd,pyogrio,geopandas as gpd
R=Path(__file__).resolve().parents[2];B=R/'07_FIGURES_TABLES/FINAL_FIGURE_TABLE_DATA';E=R/'04_EXPERIMENTS';D=R/'02_DATA/03_DERIVED_DATA/E01_E03'
FIG=B/'01_FIGURE_DATA';TAB=B/'02_TABLE_DATA';SUP=B/'03_SUPPLEMENTARY_DATA';LAT=B/'04_LATEX_TABLES';META=B/'05_SOURCE_AND_DATA_DICTIONARY';REV=B/'06_REVIEWER_MAPPING';DEL=B/'07_FINAL_DELIVERY'
for x in (FIG,TAB,SUP,LAT,META,REV,DEL):x.mkdir(parents=True,exist_ok=True)
def src(s):return E/s
def read(s):return pd.read_csv(src(s))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def rel(p):return str(p.relative_to(R)).replace('\\','/')
registry=[];books=[];figs={};tables={};sups={};today=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).date().isoformat()
FIG_NAMES=['Study_Area_GIS','Data_Completeness','Gate_FCD_Protocol','Main_Model_Performance','Reliability_and_Spatial_Error','Statistical_Inference','Traffic_Regime','Sensitivity_and_Model_Fairness']
FIG_CAPS=['Study area and current-OSM spatial audit of FCD observation nodes','Observation availability and data completeness of sparse floating car data','An auditable GATE-FCD forecasting and evaluation protocol','Multi-horizon forecasting performance under the common-sample evaluation protocol','Reliability-conditioned forecasting errors and spatial variation','Dependence-aware statistical comparison of forecasting models','Provider-reported speed distributions and traffic-regime-dependent forecast errors','Sensitivity, protocol ablation, and model-fairness evidence']
for i,n in enumerate(FIG_NAMES,1):(FIG/f'Fig{i:02d}_{n}').mkdir(exist_ok=True)
def save(df,path,source,system,notes=''):
 assert isinstance(df,pd.DataFrame) and len(df)>0,(path,'empty')
 path.parent.mkdir(parents=True,exist_ok=True)
 df=df.copy();df.to_csv(path,index=False,encoding='utf-8-sig')
 registry.append({'output_file':rel(path),'source_file':rel(source) if isinstance(source,Path) and source.is_relative_to(R) else str(source),'source_sha256':sha(source) if isinstance(source,Path) and source.exists() else 'MULTIPLE_OR_PROTOCOL','source_fields':'|'.join(map(str,df.columns)),'rows':len(df),'columns':len(df.columns),'experiment_system':system,'statistical_rule':notes,'filter_rule':'see build_plot_tables.py','generation_date':today,'script':'03_CODE/FINAL_FIGURE_TABLE_DATA/build_plot_tables.py'})
 return df
def panel(n,filename,df,source,system,notes=''):
 path=FIG/f'Fig{n:02d}_{FIG_NAMES[n-1]}'/filename
 save(df,path,source,system,notes);figs.setdefault(n,[]).append((filename,df));return path
def table(n,df,source,system,caption,cols=None,notes=''):
 folder=TAB/f'Table{n:02d}_{["Data_Source","Features","Forecast_Targets","Model_Configurations","Fold_and_Sample_Support","Experimental_Design","Main_Results","Sensitivity_and_Ablation","Model_Efficiency"][n-1]}';folder.mkdir(exist_ok=True)
 save(df,folder/f'Table{n:02d}.csv',source,system,notes);tables[n]=(df,caption,folder)
 x=df[cols].copy() if cols else df.copy()
 if len(x)>30:x=x.head(30).copy()
 def esc(v):
  if pd.isna(v):return 'N/A'
  if isinstance(v,float):v=f'{v:.4g}'
  return str(v).replace('\\','\\textbackslash{}').replace('&','\\&').replace('%','\\%').replace('_','\\_').replace('#','\\#')
 head=' & '.join(esc(c) for c in x.columns)
 body='\n'.join(' & '.join(esc(v) for v in row)+' \\\\' for row in x.itertuples(index=False,name=None))
 tex='\\begin{table}[!htbp]\n\\centering\n\\caption{'+caption+'}\n\\begin{tabular}{'+'l'*len(x.columns)+'}\n\\hline\n'+head+' \\\\ \n\\hline\n'+body+'\n\\hline\n\\end{tabular}\n\\end{table}\n'
 (folder/f'Table{n:02d}.tex').write_text(tex,encoding='utf-8')
 (LAT/f'Table{n:02d}.tex').write_text(tex,encoding='utf-8')
 (folder/'README_CN.md').write_text(f'# Table {n}\n\n英文标题：{caption}\n来源：{rel(source) if isinstance(source,Path) and source.is_relative_to(R) else source}\n实现体系：{system}\n口径与限制：{notes}\n正文TeX为紧凑展示，完整数据以CSV/XLSX为准。\n',encoding='utf-8')

# Figure 1: all spatial records stay in the local packages.
gdir=FIG/'Fig01_Study_Area_GIS'
gdist=save(pd.read_csv(gdir/'Fig01_Inter_Node_Distance_Diagnostic.csv'),gdir/'Fig01B_Inter_Node_Distance_Diagnostic.csv',src('FINAL_TARGETED_CHECKS/GIS_Final_Inter_Node_Distance.csv'),'REVISION_OPERATIONAL_EVIDENCE','current undirected OSM; not historical mainline')
figs[1]=[('Fig01B_Inter_Node_Distance_Diagnostic.csv',gdist),('Fig01_Observation_Nodes.csv',pd.read_csv(gdir/'Fig01_Observation_Nodes.csv'))]
glen=pd.read_csv(gdir/'Fig01_Corridor_Length_Reconciliation.csv')

# Figure 2.
lin=read('E01_DATA_COMPLETENESS/E01_01_Data_Lineage_and_Coverage.csv')
slot=lin[lin.metric.isin(['planned_15min_slots','unique_returned_slots','has_quality_slots','only_ineligible_slots','no_archived_return_slots'])].copy()
row=lin[lin.metric.isin(['returned_parsed_rows_all_span','quality_pass_rows_all_span','quality_fail_rows_all_span','returned_rows_in_grid','duplicate_return_rows_in_grid'])].copy()
panel(2,'Fig02A_Observation_Eligibility.csv',slot,src('E01_DATA_COMPLETENESS/E01_01_Data_Lineage_and_Coverage.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','slot-level; denominator 403512')
panel(2,'Fig02A_Record_Level_Funnel.csv',row,src('E01_DATA_COMPLETENESS/E01_01_Data_Lineage_and_Coverage.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','row-level; never subtract from slot counts')
daily=read('E01_DATA_COMPLETENESS/E01_03_Daily_Coverage.csv');daily['coverage_percent']=daily.coverage*100;daily=daily.rename(columns={'planned':'planned_slots','observed':'eligible_slots'})
panel(2,'Fig02B_Daily_Coverage.csv',daily,src('E01_DATA_COMPLETENESS/E01_03_Daily_Coverage.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','daily actual denominator; incomplete first day retained')
thr=read('E01_DATA_COMPLETENESS/E01_02_Hourly_Threshold_Coverage.csv');thr['coverage_percent']=thr.coverage*100
panel(2,'Fig02C_Hourly_Threshold_Coverage.csv',thr,src('E01_DATA_COMPLETENESS/E01_02_Hourly_Threshold_Coverage.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','common planned hourly denominator 100878')
miss=read('E01_DATA_COMPLETENESS/E01_05_Missing_Run_Distribution.csv')
panel(2,'Fig02D_Missing_Run_Distribution.csv',miss,src('E01_DATA_COMPLETENESS/E01_05_Missing_Run_Distribution.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','missing hours, not zero speed')
cov=read('E01_DATA_COMPLETENESS/E01_04_Node_Hour_Coverage.csv')
for dimension,filename,ix in [('node_idxdate','Fig02D_Node_Date_Coverage.csv','date'),('node_idxhour_of_day','Fig02D_Node_Hour_Coverage.csv','hour_of_day')]:
 c=cov[(cov.dimension==dimension)&(cov.threshold==2)].copy()
 if c.empty:
  c=cov[(cov.dimension.str.contains('node_id')&cov.dimension.str.contains('date' if ix=='date' else 'hour_of_day'))&(cov.threshold==2)].copy()
 if not c.empty:
  panel(2,filename,c,src('E01_DATA_COMPLETENESS/E01_04_Node_Hour_Coverage.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','threshold 2/4; node/date or node/hour')
  wide=c.pivot_table(index='node_id',columns=ix,values='coverage',aggfunc='first').reset_index()
  panel(2,filename.replace('.csv','_Wide.csv'),wide,src('E01_DATA_COMPLETENESS/E01_04_Node_Hour_Coverage.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','matrix for heatmap')

# Figure 3 protocol data and time semantics (no figure drawn).
names=['Raw FCD retrieval','Scheduled observation grid','Quality screening','Slot deduplication','Hourly observation eligibility','Causal missing-data handling','Historical feature construction','Future-window target','Chronological common-sample evaluation','Audit and interpretation']
rules=['Historical 15-minute source records','51 nodes x scheduled 15-minute times','speed/confidence/travel-time/closure flags','node x quarter-hour deduplication','2 of 4 valid quarter-hours','forward fill within history; training medians','24-hour causal history; 13 dynamic features','H1=1/1,H3=3/3,H6>=5/6 observed hours','six folds; common model samples; no target crosses split','Method A, day-block inference, provenance']
nodes=pd.DataFrame([{'step_id':i+1,'step_name_en':name,'step_name_cn':'见协议原文','stage':(i//2)+1,'input':names[i-1] if i else 'frozen source','processing_rule':rules[i],'output':names[i+1] if i<9 else 'audited evidence','eligibility_condition':'see G1 protocol','causal_constraint':'no future information; target never imputed','evidence_source':'00_PROJECT_CONTROL/G1_Analysis_Protocol.yaml','reviewer_mapping':'R1-01;R1-03;R1-07;R6-01'} for i,name in enumerate(names)])
panel(3,'Fig03A_Protocol_Nodes.csv',nodes,R/'00_PROJECT_CONTROL/G1_Analysis_Protocol.yaml','ORIGINAL_FROZEN_BASELINE','schematic design, not model output')
edges=pd.DataFrame([{'from_step':i,'to_step':i+1,'edge_type':'forward','condition':'passed eligibility'} for i in range(1,10)])
panel(3,'Fig03B_Protocol_Edges.csv',edges,R/'00_PROJECT_CONTROL/G1_Analysis_Protocol.yaml','ORIGINAL_FROZEN_BASELINE','schematic arrows')
time=pd.DataFrame([{'horizon':h,'history_hours':24,'decision_time':'end of origin hour t','target_interval':f'next {h} hours after t','required_observed_target_hours':{1:1,3:3,6:5}[h],'target_imputation':'NONE','target_must_remain_in_split':True} for h in [1,3,6]])
panel(3,'Fig03C_Time_Semantics.csv',time,R/'00_PROJECT_CONTROL/G1_Analysis_Protocol.yaml','ORIGINAL_FROZEN_BASELINE','retrospective forecast convention; API arrival latency unverified')

# Figure 4 primary original model Method A, separate new implementation elsewhere.
fold=read('E03_STATISTICAL_INFERENCE/E03_01_Seed_Aggregation_Reconciliation.csv')
sumtab=read('E03_STATISTICAL_INFERENCE/E03_03_Original_vs_Recomputed_Table7.csv')
weight=read('E03_STATISTICAL_INFERENCE/E03_04_Weighting_Estimands.csv')
day=weight[(weight.method=='A_ENSEMBLE_PREDICTION')&(weight.estimand=='Day-macro')][['horizon','model','MAE']].rename(columns={'MAE':'day_macro_MAE'})
fold=fold.merge(sumtab[['model','horizon','method_A_value','method_A_fold_sd']],on=['model','horizon'],validate='many_to_one').merge(day,on=['model','horizon'],how='left')
fold['sample_weighted_MAE']=fold.groupby(['model','horizon']).MAE_A.transform(lambda x:np.average(x,weights=fold.loc[x.index,'n']))
fold=fold.rename(columns={'MAE_A':'MAE','RMSE_A':'RMSE','n':'n_test','method_A_value':'fold_macro_MAE','method_A_fold_sd':'fold_sd_MAE'})
fold['seed_aggregation']='METHOD_A_PER_SAMPLE_ENSEMBLE_THEN_ERROR';fold['implementation_id']='ORIGINAL_FROZEN_BASELINE'
for h,l in [(1,'A'),(3,'B'),(6,'C')]:panel(4,f'Fig04{l}_H{h}_Model_Performance.csv',fold[fold.horizon==h],src('E03_STATISTICAL_INFERENCE/E03_01_Seed_Aggregation_Reconciliation.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','fold SD is not confidence interval')
ranking=sumtab[['model','horizon','method_A_value','method_A_fold_sd']].copy();ranking['rank']=ranking.groupby('horizon').method_A_value.rank(method='min')
panel(4,'Fig04D_Model_Ranking_and_Fold_Variation.csv',ranking,src('E03_STATISTICAL_INFERENCE/E03_03_Original_vs_Recomputed_Table7.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','descriptive ranking')
lofo=read('E03_STATISTICAL_INFERENCE/E03_10_LOFO_Stability.csv')
panel(4,'Fig04D_LOFO_Model_Performance.csv',lofo,src('E03_STATISTICAL_INFERENCE/E03_10_LOFO_Stability.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','LOFO does not cure historical test exposure')
seeds=read('E03_STATISTICAL_INFERENCE/E03_11_Seed_Stability.csv')
panel(4,'Fig04D_Within_Fold_Seed_Ranges.csv',seeds,src('E03_STATISTICAL_INFERENCE/E03_11_Seed_Stability.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','seed range not uncertainty interval')

# Figure 5 conditioned historical results and aggregated node error from frozen predictions.
joint=read('E02_TRAFFIC_RELIABILITY/E02_07_Coverage_Gap_Volatility.csv')
for filename,mask in [('Fig05A_Coverage_Conditioned_Error.csv',joint.conditioning=='cov_bin'),('Fig05C_Volatility_Conditioned_Error.csv',joint.conditioning=='vol_bin'),('Fig05C_Coverage_Gap_Volatility_Joint.csv',joint.conditioning=='cov_binxgap_binxvol_bin')]:
 x=joint[mask].copy()
 if not x.empty:panel(5,filename,x,src('E02_TRAFFIC_RELIABILITY/E02_07_Coverage_Gap_Volatility.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','conditioned descriptive; n and support included')
gap=read('E02_TRAFFIC_RELIABILITY/E02_06_Gap_Conditioned_Performance.csv')
panel(5,'Fig05B_Gap_Conditioned_Error.csv',gap,src('E02_TRAFFIC_RELIABILITY/E02_06_Gap_Conditioned_Performance.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','conditioning_variable distinguishes max gap from observation age')
aligned=pd.read_parquet(D/'aligned_predictions.parquet',columns=['fold','horizon','node_id','model','signed_error','absolute_error','squared_error'])
node=aligned.groupby(['node_id','horizon','model'],observed=True).agg(n_samples=('absolute_error','size'),MAE=('absolute_error','mean'),MSE=('squared_error','mean'),Bias=('signed_error','mean')).reset_index()
node['RMSE']=np.sqrt(node.pop('MSE'));node['sample_support_status']=np.where(node.n_samples>=30,'SUPPORTED','LOW_SUPPORT')
panel(5,'Fig05D_Node_Level_Model_Error.csv',node,D/'aligned_predictions.parquet','G1_RECOMPUTED_ORIGINAL_PREDICTIONS','node-level aggregate; ID/order is not distance')
geo=pyogrio.read_dataframe(FIG/'Fig01_Study_Area_GIS/Fig01_Pan_Borneo_Study_Area.gpkg',layer='Original_Observation_Nodes')
nodegeo=geo[['node_id_original','geometry']].rename(columns={'node_id_original':'node_id'}).merge(node,on='node_id',validate='one_to_many')
pyogrio.write_dataframe(nodegeo,FIG/'Fig05_Reliability_and_Spatial_Error/Fig05D_Node_Error_GIS.gpkg',layer='Node_Error_Aggregates',driver='GPKG')

# Figure 6 primary and existing seven-day sensitivity; no bootstrap.
inf=read('FINAL_TARGETED_CHECKS/Final_Statistical_Inference.csv')
primary=inf[inf.family.str.startswith('G1')].copy()
for h,l in [(1,'A'),(3,'B'),(6,'C')]:
 x=primary[primary.horizon==h].copy();x['effect_direction']='negative favors first model';x['CI_type']='pointwise 95%, not Holm simultaneous'
 panel(6,f'Fig06{l}_H{h}_Paired_Effects.csv',x,src('FINAL_TARGETED_CHECKS/Final_Statistical_Inference.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','3-day block; Holm family 5 per horizon')
sens=read('FINAL_TARGETED_CHECKS/Final_Statistical_Sensitivity_3d_7d.csv')
panel(6,'Fig06D_Three_vs_Seven_Day_Blocks.csv',sens[sens.family.str.startswith('G1')],src('FINAL_TARGETED_CHECKS/Final_Statistical_Sensitivity_3d_7d.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','7-day Holm independently recomputed from frozen p; no bootstrap rerun')
panel(6,'Fig06D_Alternative_Weighting_Estimands.csv',weight,src('E03_STATISTICAL_INFERENCE/E03_04_Weighting_Estimands.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','different estimands and weights')

# Figure 7 supplier speed proxies.
hist=read('E02_TRAFFIC_RELIABILITY/E02_01b_Distribution_Histograms.csv')
panel(7,'Fig07A_Current_and_FreeFlow_Speed_Distribution.csv',hist,src('E02_TRAFFIC_RELIABILITY/E02_01b_Distribution_Histograms.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','binned counts, no raw commercial records')
equality=read('E02_TRAFFIC_RELIABILITY/E02_02_FreeFlow_Equality.csv')
panel(7,'Fig07B_FreeFlow_Equality_and_Speed_Ratio.csv',equality,src('E02_TRAFFIC_RELIABILITY/E02_02_FreeFlow_Equality.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','provider-reported equality, not physical absence of congestion')
conf=read('E02_TRAFFIC_RELIABILITY/E02_03_Confidence_Distribution.csv')
panel(7,'Fig07C_Confidence_Distribution.csv',conf,src('E02_TRAFFIC_RELIABILITY/E02_03_Confidence_Distribution.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','quality threshold 0.80')
regime=read('E02_TRAFFIC_RELIABILITY/E02_05_Regime_Model_Performance.csv')
panel(7,'Fig07D_Traffic_Regime_Model_Performance.csv',regime,src('E02_TRAFFIC_RELIABILITY/E02_05_Regime_Model_Performance.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','target-defined regime is retrospective, not available at forecast time')
ff=read('E02_TRAFFIC_RELIABILITY/E02_10_FreeFlow_Baseline.csv')
panel(7,'Fig07D_FreeFlow_Baseline.csv',ff,src('E02_TRAFFIC_RELIABILITY/E02_10_FreeFlow_Baseline.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','supplier free-flow benchmark')

# Figure 8 actual revision runs: primary G2 metrics, corrected Ridge overlay.
reg=read('G2_E04_E07_ACCEPTANCE/G2_02_Experiment_Run_Registry.csv')
reg=reg[reg.status=='COMPLETED'].copy()
reg['seed_aggregation']='SINGLE_SEED_OR_DETERMINISTIC';reg['experiment_system']=np.select([reg.condition.str.startswith('threshold')|reg.condition.eq('strict6')|reg.condition.eq('seasonal_impute')|reg.condition.str.startswith('history'),reg.condition.isin(['returned_only','leaky_scaling'])],['REVISION_SENSITIVITY','REVISION_ABLATION'],default='REVISION_MATCHED_BASELINE')
ridge=read('FINAL_TARGETED_CHECKS/Ridge_Corrected_Experiment_Metrics.csv')
correction=ridge[['run_id','test_MAE_svd','test_RMSE_svd','test_Bias_svd']]
reg=reg.merge(correction,on='run_id',how='left',validate='one_to_one')
reg['final_MAE']=np.where(reg.model=='Ridge',reg.test_MAE_svd,reg.test_MAE)
reg['final_RMSE']=np.where(reg.model=='Ridge',reg.test_RMSE_svd,reg.test_RMSE)
reg['final_Bias']=np.where(reg.model=='Ridge',reg.test_Bias_svd,reg.test_Bias)
reg['numerical_status']=np.where(reg.model=='Ridge','SVD_CORRECTED_NATIVE_METRIC','ORIGINAL_G2_METRIC')
def g8(filename,x,note):panel(8,filename,x,src('G2_E04_E07_ACCEPTANCE/G2_02_Experiment_Run_Registry.csv'),'REVISION_SENSITIVITY','G2 independent implementation; '+note)
g8('Fig08A_Threshold_Sensitivity.csv',reg[reg.condition.isin(['base','threshold1','threshold3'])],'native condition metrics; compare on common origins separately')
support4=read('E04_SENSITIVITY/E04_Threshold4_Sample_Support.csv')
panel(8,'Fig08A_Threshold4_Not_Estimable.csv',support4,src('E04_SENSITIVITY/E04_Threshold4_Sample_Support.csv'),'REVISION_SENSITIVITY','not trained; do not render missing as zero')
g8('Fig08B_H6_Target_Completeness.csv',reg[reg.condition.isin(['base','strict6'])&(reg.horizon==6)],'strict6 condition, differing target support')
g8('Fig08C_Imputation_Sensitivity.csv',reg[reg.condition.isin(['base','seasonal_impute'])],'same-implementation baseline')
g8('Fig08D_History_Window_Sensitivity.csv',reg[reg.condition.isin(['base','history12','history48'])&(reg.model.isin(['XGBoost','GRU']))&(reg.horizon.isin([1,6]))],'use matched24 common-origin contrasts for claims')
g8('Fig08E_Grid_Protocol_Ablation.csv',reg[reg.condition.isin(['base','returned_only'])&(reg.model.isin(['Ridge','XGBoost']))&(reg.horizon.isin([1,6]))],'return-only history span differs')
leaky=reg[reg.condition=='leaky_scaling'].copy();leaky['comparison_scope']='LEAKAGE_DIAGNOSTIC_ONLY'
g8('Fig08E_Causal_Scaling_Diagnostic.csv',leaky,'not valid ranking')
native=read('E05_ABLATION/E05_Native_Eligibility_Set_Check.csv')
panel(8,'Fig08E_Native_Eligibility_Check.csv',native,src('E05_ABLATION/E05_Native_Eligibility_Set_Check.csv'),'REVISION_ABLATION','no separate training where identical')
vc=read('E06_MODEL_FAIRNESS/E06_Fold1_Validation_Candidates.csv')
panel(8,'Fig08F_Validation_Based_Tuning.csv',vc,src('E06_MODEL_FAIRNESS/E06_Fold1_Validation_Candidates.csv'),'REVISION_TUNED_MODELS','validation selection, no test tuning')
configs=read('G2_E04_E07_ACCEPTANCE/G2_E06_Configuration_Contrasts.csv')
panel(8,'Fig08F_Configuration_Contrasts.csv',configs,src('G2_E04_E07_ACCEPTANCE/G2_E06_Configuration_Contrasts.csv'),'REVISION_TUNED_MODELS','matched common test')
ens=read('G2_E04_E07_ACCEPTANCE/G2_E06_Method_A_B_Actual.csv')
panel(8,'Fig08F_Three_Seed_Ensemble_Results.csv',ens,src('G2_E04_E07_ACCEPTANCE/G2_E06_Method_A_B_Actual.csv'),'REVISION_TUNED_MODELS','Method A vs B explicitly separated')
contrast=read('G2_E04_E07_ACCEPTANCE/G2_Actual_Common_Origin_Contrasts.csv')
panel(8,'Fig08_Matched_Common_Origin_Contrasts.csv',contrast,src('G2_E04_E07_ACCEPTANCE/G2_Actual_Common_Origin_Contrasts.csv'),'REVISION_SENSITIVITY','Ridge old Cholesky paired contrasts not used for final Ridge interpretation')
key=read('G2_E04_E07_ACCEPTANCE/G2_Key_Comparisons_Actual.csv')
panel(8,'Fig08_Key_Statistical_Comparisons.csv',key,src('G2_E04_E07_ACCEPTANCE/G2_Key_Comparisons_Actual.csv'),'REVISION_SENSITIVITY','4 predeclared, all Holm nonsignificant')

# Nine main tables from actual evidence, retaining full-precision CSV.
table(1,lin,src('E01_DATA_COMPLETENESS/E01_01_Data_Lineage_and_Coverage.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','Data source and observation eligibility.',cols=['metric','value','statistical_level','denominator'],notes='row vs slot denominator distinguished; 97.30% excluded')
features=['input_speed_filled','hourly_missing_mask','imputed_flag','hours_since_last_observation','history_coverage_ratio','history_imputation_ratio','max_gap_24h','volatility_24h','hour_sin','hour_cos','dow_sin','dow_cos','weekend_flag']
feat=pd.DataFrame([{'feature':f,'kind':'dynamic','input_scope':'24-hour causal sequence','unit':'km/h' if f in ['input_speed_filled','volatility_24h'] else 'hours' if f in ['hours_since_last_observation','max_gap_24h'] else 'ratio/indicator','causal_rule':'history only; train-fit fallback'} for f in features]+[{'feature':f,'kind':'static','input_scope':'Ridge/XGBoost and static-GRU condition only','unit':'index' if f=='node_order' else 'degrees','causal_rule':'known node metadata'} for f in ['node_order','latitude','longitude']])
table(2,feat,R/'03_CODE/E04_E07_REVISION/g2_common.py','REVISION_MATCHED_BASELINE','Dynamic and static feature definitions.',cols=['feature','kind','unit'],notes='13 dynamic and 3 static; historical duplicate masks preserved')
h6=read('E01_DATA_COMPLETENESS/E01_06_H6_Target_Completeness.csv')
target=pd.DataFrame([{'horizon':h,'history_hours':24,'target_window_hours':h,'required_observed_hours':{1:1,3:3,6:5}[h],'target_imputation':'NONE','test_samples':int(fold[fold.horizon==h].query("model=='HA'").n_test.sum())} for h in [1,3,6]])
table(3,target,src('E01_DATA_COMPLETENESS/E01_06_H6_Target_Completeness.csv'),'ORIGINAL_FROZEN_BASELINE','Forecast horizons and observed-target requirements.',notes='H6 partial 5/6 detailed in supplement; future-window means')
cfg=reg[(reg.condition=='base')&(reg.fold==1)&(reg.seed==42)][['model','horizon','configuration_json','implementation','seed','train_n','validation_n','test_n']].drop_duplicates(['model','horizon'])
cfg['historical_original_details']='ORIGINAL_TRAINING_SOURCE_NOT_RECOVERED'
table(4,cfg,src('G2_E04_E07_ACCEPTANCE/G2_02_Experiment_Run_Registry.csv'),'REVISION_MATCHED_BASELINE','Model configurations and implementation roles.',cols=['model','horizon','seed','implementation'],notes='G2 independent implementation; original details unverified')
attr=read('E01_DATA_COMPLETENESS/E01_10_Fold_Sample_Attrition.csv')
table(5,attr,src('E01_DATA_COMPLETENESS/E01_10_Fold_Sample_Attrition.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','Rolling-origin fold support and sample attrition.',cols=['fold','horizon','split','theoretical_candidates','eligible_rebuilt'],notes='target window entirely within split; 54 fold-horizon-split records')
design=pd.DataFrame([{'stage':s,'unique_runs':n,'meaning':m,'source':source} for s,n,m,source in [('original frozen',180,'historical model run records','G0'),('G2 revision',651,'489 fits, 162 deterministic executions','G2'),('Ridge SVD diagnosis',93,'numerical correction only','Prompt04'),('E08 external',0,'target asset not found','Prompt05')]])
table(6,design,R/'05_FINAL_RESULTS/FINAL_NONTRAINING_CLOSURE/FINAL_07_Execution_Manifest.json','REVISION_OPERATIONAL_EVIDENCE','Experimental and audit scope.',notes='unique runs not independent scientific comparisons')
main=sumtab[['model','horizon','method_A_value','method_A_fold_sd']].merge(weight[(weight.method=='A_ENSEMBLE_PREDICTION')&(weight.estimand=='Sample-weighted')][['horizon','model','MAE']].rename(columns={'MAE':'sample_weighted_MAE'}),on=['horizon','model'],how='left')
table(7,main,src('E03_STATISTICAL_INFERENCE/E03_03_Original_vs_Recomputed_Table7.csv'),'G1_RECOMPUTED_ORIGINAL_PREDICTIONS','Primary six-model fold-macro MAE under Method A.',notes='Method A per-sample ensemble; original implementation')
table(8,contrast,src('G2_E04_E07_ACCEPTANCE/G2_Actual_Common_Origin_Contrasts.csv'),'REVISION_SENSITIVITY','Sensitivity and ablation on matched forecast origins.',cols=['condition','model','horizon','fold','common_n','paired_MAE_delta_alt_minus_ref'],notes='Ridge paired contrasts are Cholesky historical and excluded from corrected Ridge claims')
eff=read('FINAL_NONTRAINING_CLOSURE/Final_Unified_Inference_Benchmark.csv')
table(9,eff,src('FINAL_NONTRAINING_CLOSURE/Final_Unified_Inference_Benchmark.csv'),'REVISION_OPERATIONAL_EVIDENCE','Prepared-input CPU batch inference time for 1024 samples.',cols=['model','horizon','execution','status','mean_batch_seconds','p95_batch_seconds'],notes='Ridge SVD weight unavailable; not end-to-end latency')

# Eight supplemental data groups, each with key accepted records; CSV source copies only.
supp_sources={
1:[('Coverage',lin),('Thresholds',thr),('Daily',daily),('Missing_runs',miss)],
2:[('Attrition_54',attr),('H6_target',h6)],
3:[('Fold_models',fold),('Seed_stability',seeds),('LOFO',lofo)],
4:[('Primary_Holm',primary),('3d_7d',sens),('Weighting',weight)],
5:[('G2_common_origin',contrast),('Threshold4_support',support4)],
6:[('Native_eligibility',native),('G2_key',key)],
7:[('Validation_tuning',vc),('Method_A_B',ens),('Ridge_SVD_aggregates',read('FINAL_TARGETED_CHECKS/Ridge_Corrected_Aggregates.csv'))],
8:[('GIS_lengths',glen),('Unified_efficiency',eff),('Official_calendar',read('E07_SPATIAL_OPERATIONAL/E07_Official_Calendar_Source_Table.csv'))]}
for i,items in supp_sources.items():
 folder=SUP/f'S{i:02d}_{["Data_Eligibility","Sample_Attrition","Model_and_Seed_Results","Statistical_Inference","Sensitivity","Protocol_Ablation","Model_Fairness","GIS_and_Reproducibility"][i-1]}';folder.mkdir(exist_ok=True)
 sups[i]=[]
 for name,df in items:
  p=folder/f'S{i:02d}_{name}.csv';save(df,p,'frozen accepted aggregate sources','MIXED_ACCEPTED','see group README');sups[i].append((name,df))
 (folder/'README_CN.md').write_text(f'# Supplementary S{i}\n\n本组直接整理冻结的聚合结果；各CSV保留来源字段。G1历史模型与G2独立新实现不可混用，SVD Ridge修正单列。商业逐样本速度、预测和模型权重未复制。\n',encoding='utf-8')

# Per-figure descriptions and dictionaries. Source details in global provenance.
for i,n in enumerate(FIG_NAMES,1):
 folder=FIG/f'Fig{i:02d}_{n}';data=figs.get(i,[])
 lines=[f'# Fig. {i} 绘图数据',f'\n建议英文图题：{FIG_CAPS[i-1]}','\n本目录的每个CSV为独立面板或其辅助矩阵；对应XLSX列出全部面板。']
 for file,df in data:lines.append(f'- {file}: {len(df)} 行；字段 {", ".join(map(str,df.columns[:12]))}；X/Y及分组按字段名和统计口径选择。')
 lines.append('\n样本量、单位、显著性及实现体系应从表内字段和全局来源清单读取；空值不得改作0。Fig.1当前OSM与历史主线不同，Fig.4折线/标准差为描述性，Fig.6点置信区间不是Holm同时区间，Fig.8 Ridge特殊共同目标配对结果未获SVD逐样本修正。E08未运行。原图对应：Fig.1–Fig.6分别对应原稿同号；Fig.7与Fig.8为新增建议。')
 (folder/'README_CN.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 dictionary=pd.DataFrame([{'file':file,'column':c,'dtype':str(df[c].dtype),'sample_values':str(df[c].dropna().iloc[0])[:80] if df[c].notna().any() else 'NOT_AVAILABLE'} for file,df in data for c in df.columns])
 dictionary.to_csv(folder/'Data_Dictionary.csv',index=False,encoding='utf-8-sig')

prov=pd.DataFrame(registry);prov.to_csv(META/'Final_Figure_Table_Data_Provenance.csv',index=False,encoding='utf-8-sig')
pd.DataFrame([{'original_figure':f'Fig{i}' if i<=6 else 'NEW','planned_figure':f'Fig{i}','caption':FIG_CAPS[i-1],'status':'DATA_PREPARED_AUTHOR_DRAWING_PENDING'} for i in range(1,9)]).to_csv(META/'Original_to_Planned_Figure_Map.csv',index=False)
payload={'workbooks':[]}
payload['workbooks'].append({'file':'Fig01_Study_Area_GIS_Plot_Data.xlsx','dir':rel(gdir),'sheets':[{'name':'Original nodes','title':'51 original observation nodes','source':'frozen original coordinates','headers':list(figs[1][1][1].columns),'rows':figs[1][1][1].fillna('').values.tolist()},{'name':'Inter node routes','title':'50 current OSM diagnostic routes','source':'Prompt04 GIS','headers':list(gdist.columns),'rows':gdist.fillna('').values.tolist()},{'name':'Length reconciliation','title':'Distinct length estimands','source':'Prompt04 GIS','headers':list(glen.columns),'rows':glen.fillna('').values.tolist()}]})
payload['workbooks'].append({'file':'Fig01_Corridor_Length_Reconciliation.xlsx','dir':rel(gdir),'sheets':[{'name':'Lengths','title':'Not historical mainline length','source':'Prompt04 GIS','headers':list(glen.columns),'rows':glen.fillna('').values.tolist()}]})
review15=pd.read_csv(gdir/'Fig01_GIS_Review_15_Nodes.csv')
payload['workbooks'].append({'file':'Fig01_GIS_Review_15_Nodes.xlsx','dir':rel(gdir),'sheets':[{'name':'15 candidates','title':'Author manual GIS review required','source':'Prompt04 matched nodes','headers':list(review15.columns),'rows':review15.fillna('').values.tolist()}]})
for i,n in enumerate(FIG_NAMES,1):
 if i==1:continue
 payload['workbooks'].append({'file':f'Fig{i:02d}_{n}_Plot_Data.xlsx' if i not in [3,7] else ('Fig03_Gate_FCD_Protocol_Design.xlsx' if i==3 else 'Fig07_Traffic_Regime_Plot_Data.xlsx'),'dir':rel(FIG/f'Fig{i:02d}_{n}'),'sheets':[{'name':f'{j+1:02d}_{file.removesuffix(".csv")[:22]}','title':file,'source':'frozen accepted records','headers':list(df.columns),'rows':df.fillna('').values.tolist()} for j,(file,df) in enumerate(figs[i])]})
for i,(df,caption,folder) in tables.items():
 payload['workbooks'].append({'file':f'Table{i:02d}.xlsx','dir':rel(folder),'sheets':[{'name':f'Table{i:02d}','title':caption,'source':'see Table README','headers':list(df.columns),'rows':df.fillna('').values.tolist()}]})
for i,items in sups.items():
 folder=next(SUP.glob(f'S{i:02d}_*'))
 payload['workbooks'].append({'file':f'S{i:02d}.xlsx','dir':rel(folder),'sheets':[{'name':name[:29],'title':name,'source':'accepted aggregate records','headers':list(df.columns),'rows':df.fillna('').values.tolist()} for name,df in items]})
payload['workbooks'].append({'file':'APIN_Final_Main_Text_Tables.xlsx','dir':rel(TAB),'sheets':[{'name':f'Table_{i:02d}','title':caption,'source':'accepted source; see table CSV','headers':list(df.columns),'rows':df.fillna('').values.tolist()} for i,(df,caption,folder) in tables.items()]})
(R/'03_CODE/FINAL_FIGURE_TABLE_DATA/workbook_payload.json').write_text(json.dumps(payload,ensure_ascii=False,default=str),encoding='utf-8')
print('PLOTS',len(figs),'PANEL_CSVS',sum(len(v) for v in figs.values()),'TABLES',len(tables),'SUPPS',len(sups),'WORKBOOKS',len(payload['workbooks']))
