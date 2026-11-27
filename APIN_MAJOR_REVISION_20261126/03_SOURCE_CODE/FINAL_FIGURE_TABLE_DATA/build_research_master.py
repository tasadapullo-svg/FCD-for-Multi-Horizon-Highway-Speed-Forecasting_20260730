from pathlib import Path
import hashlib,json,shutil
import pandas as pd

R=Path(r'E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改')
S=R/'04_EXPERIMENTS';B=R/'07_FIGURES_TABLES/FINAL_FIGURE_TABLE_DATA';OUT=B/'08_MASTER_RESEARCH_RESULTS';OUT.mkdir(exist_ok=True)
groups={
'R01_Data_Collection_and_Availability':['E01_01_Data_Lineage_and_Coverage','E01_02_Hourly_Threshold_Coverage','E01_03_Daily_Coverage','E01_03b_Coverage_Weighting','E01_04_Node_Hour_Coverage','E01_05_Missing_Run_Distribution','E02_03_Confidence_Distribution'],
'R02_Forecast_Target_and_Eligibility':['E01_06_H6_Target_Completeness','E01_07_H6_Missing_Position','E01_09_H3_H6_Common_Origins','E01_10_Fold_Sample_Attrition','E01_11_E04_Sample_Feasibility'],
'R03_Original_Six_Model_Forecasting':['E03_01_Seed_Aggregation_Reconciliation','E03_02_Fold_Model_Metrics','E03_03_Original_vs_Recomputed_Table7','E03_04_Weighting_Estimands','E03_11_Seed_Stability'],
'R04_Statistical_Inference':['E03_06_Block_Bootstrap_Results','E03_07_Block_Length_Sensitivity','E03_08_Holm_Adjusted_Comparisons','E03_10_LOFO_Stability','Final_Statistical_Inference','Final_Statistical_Sensitivity_3d_7d'],
'R05_Traffic_Regime_and_Reliability':['E02_01_Speed_and_Target_Distribution','E02_01b_Distribution_Histograms','E02_02_FreeFlow_Equality','E02_04_Traffic_Regime_Distribution','E02_05_Regime_Model_Performance','E02_06_Gap_Conditioned_Performance','E02_07_Coverage_Gap_Volatility','E02_10_FreeFlow_Baseline'],
'R06_Data_and_Protocol_Sensitivity':['G2_02_Experiment_Run_Registry','G2_Actual_Common_Origin_Contrasts','E04_Threshold4_Sample_Support'],
'R07_GATE_FCD_Ablation':['E05_Native_Eligibility_Set_Check','G2_Key_Comparisons_Actual'],
'R08_Model_Fairness_and_Ridge':['E06_Fold1_Validation_Candidates','G2_E06_Configuration_Contrasts','G2_E06_Method_A_B_Actual','Ridge_Corrected_Aggregates','Ridge_Corrected_Experiment_Metrics','Ridge_Selection_Stability'],
'R09_Spatial_and_Operational':['GIS_Final_Node_Matching','GIS_Final_Inter_Node_Distance','GIS_Corridor_Length_Reconciliation','GIS_Author_Review_Checklist_15_Nodes','E07_Official_Calendar_Source_Table','Final_Unified_Inference_Benchmark'],
'R10_Claims_and_Limitations':['Final_Scientific_Claims_Registry','E08_Data_Feasibility_and_Decision','Data_Licensing_and_Distribution_Matrix','FINAL_Manuscript_Consistency_v2','FINAL_Reviewer_Evidence_Matrix_v2']}
source_index={p.stem:p for p in S.rglob('*.csv') if 'logs' not in p.parts}
source_index['Fig05D_Node_Level_Model_Error']=B/'01_FIGURE_DATA/Fig05_Reliability_and_Spatial_Error/Fig05D_Node_Level_Model_Error.csv'
rows=[]; sheets=[]
for group,names in groups.items():
 d=OUT/group;d.mkdir(exist_ok=True)
 for name in names:
  p=source_index.get(name)
  if not p:raise FileNotFoundError(name)
  x=pd.read_csv(p);q=d/p.name;shutil.copy2(p,q)
  h=hashlib.sha256(q.read_bytes()).hexdigest()
  rows.append({'category':group,'relative_path':str(q.relative_to(B)).replace('\\','/'),'source_path':str(p.relative_to(R)).replace('\\','/'),'source_sha256':h,'output_sha256':h,'rows':len(x),'columns':len(x.columns),'role':'FROZEN_AGGREGATE_COPY','license':'AUTHOR_LOCAL; GPT_REVIEW_ONLY_IF_AUTHORIZED'})
  if len(x)<=1000:sheets.append((name,x,group))
pd.DataFrame(rows).to_csv(OUT/'Master_Aggregate_Provenance.csv',index=False,encoding='utf-8-sig')
sheet_map=[
('00_Executive_Summary',None),('01_Data_Source','E01_01_Data_Lineage_and_Coverage'),('02_Observation_Coverage','E01_03_Daily_Coverage'),('03_Hourly_Thresholds','E01_02_Hourly_Threshold_Coverage'),('04_Missingness','E01_05_Missing_Run_Distribution'),('05_Confidence','E02_03_Confidence_Distribution'),('06_Forecast_Targets','E01_06_H6_Target_Completeness'),('07_Fold_Sample_Support','E01_10_Fold_Sample_Attrition'),('08_Main_MAE','E03_03_Original_vs_Recomputed_Table7'),('09_Secondary_Metrics','E03_04_Weighting_Estimands'),('10_Fold_Model_Results','E03_02_Fold_Model_Metrics'),('11_Seed_Aggregation','E03_01_Seed_Aggregation_Reconciliation'),('12_Statistical_Comparisons','E03_08_Holm_Adjusted_Comparisons'),('13_Bootstrap_Sensitivity','E03_07_Block_Length_Sensitivity'),('14_Weighting_Estimands','E03_04_Weighting_Estimands'),('15_LOFO','E03_10_LOFO_Stability'),('16_Traffic_Regimes','E02_04_Traffic_Regime_Distribution'),('17_Reliability_Conditions','E02_07_Coverage_Gap_Volatility'),('18_Node_Level_Error','GIS_Final_Node_Matching'),('19_Threshold_Sensitivity','G2_02_Experiment_Run_Registry'),('20_Strict_H6','E01_06_H6_Target_Completeness'),('21_Imputation_Sensitivity','G2_Actual_Common_Origin_Contrasts'),('22_History_Window','G2_Actual_Common_Origin_Contrasts'),('23_Grid_Ablation','E05_Native_Eligibility_Set_Check'),('24_Scaling_Diagnostic','G2_02_Experiment_Run_Registry'),('25_Common_Sample','G2_Actual_Common_Origin_Contrasts'),('26_Model_Tuning','E06_Fold1_Validation_Candidates'),('27_GRU_Static','G2_E06_Configuration_Contrasts'),('28_Ridge_SVD','Ridge_Corrected_Aggregates'),('29_Computational_Cost','Final_Unified_Inference_Benchmark'),('30_GIS_Summary','GIS_Corridor_Length_Reconciliation'),('31_Holiday_Diagnostics','E07_Official_Calendar_Source_Table'),('32_Scientific_Claims','Final_Scientific_Claims_Registry'),('33_Reviewer_Mapping','FINAL_Reviewer_Evidence_Matrix_v2'),('34_Limitations','E08_Data_Feasibility_and_Decision'),('35_Figure_Table_Index','FINAL_Manuscript_Consistency_v2'),('36_Source_Provenance','Master_Aggregate_Provenance')]
sheet_map=[(label,'Fig05D_Node_Level_Model_Error' if label=='18_Node_Level_Error' else key) for label,key in sheet_map]
payload=[]
for label,key in sheet_map:
 if key is None:x=pd.DataFrame([{'historical_original_runs':180,'g2_unique_executions':651,'ridge_svd_diagnostics':93,'new_model_fits':0,'new_traffic_datasets':0,'original_nodes':51,'review_comments':31,'E08':'NOT_RUN_TARGET_ASSET_NOT_FOUND'}])
 elif key=='Master_Aggregate_Provenance':x=pd.DataFrame(rows)
 elif key=='Fig05D_Node_Level_Model_Error':x=pd.read_csv(source_index[key])
 else:x=next(v for k,v,g in sheets if k==key)
 if len(x)>1000:x=x.head(1000)
 payload.append({'name':label[:31],'title':label,'source':key or 'frozen evidence rollup','headers':list(x.columns),'rows':x.fillna('').values.tolist()})
(R/'03_CODE/FINAL_FIGURE_TABLE_DATA/research_master_payload.json').write_text(json.dumps({'workbooks':[{'file':'APIN_00_All_Research_Results_Master.xlsx','dir':str(OUT.relative_to(R)).replace('\\','/'),'sheets':payload}]},ensure_ascii=False,default=str),encoding='utf-8')
print('GROUPS',len(groups),'AGGREGATE_FILES',len(rows),'SHEETS',len(payload))
