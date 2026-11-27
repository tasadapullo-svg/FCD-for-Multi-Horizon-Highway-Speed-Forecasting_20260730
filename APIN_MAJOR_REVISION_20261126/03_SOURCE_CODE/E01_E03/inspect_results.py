from common import *
for folder,name,query in [
(E01,'E01_01_Data_Lineage_and_Coverage.csv',None),(E01,'E01_06_H6_Target_Completeness.csv','fold=="ALL_TEST"'),(E01,'E01_11_E04_Sample_Feasibility.csv',None),(E03,'E03_03_Original_vs_Recomputed_Table7.csv',None),(E03,'E03_04_Weighting_Estimands.csv','model=="XGBoost"'),(E03,'E03_04b_Historical_Cluster_Reconstruction.csv','model=="XGBoost"'),(E03,'E03_08_Holm_Adjusted_Comparisons.csv',None),(E03,'E03_10_LOFO_Stability.csv','model=="XGBoost" and method=="A_ENSEMBLE_PREDICTION"'),(E02,'E02_10_FreeFlow_Baseline.csv','record_type=="BASELINE_PERFORMANCE" and traffic_regime!=traffic_regime')]:
 df=pd.read_csv(folder/name)
 print('\nRESULT',name)
 if name=='E01_11_E04_Sample_Feasibility.csv':
  print(df.groupby(['threshold','history_hours','target_required','horizon','split']).estimated_eligible.agg(['min','max','sum']).to_string());continue
 if query:df=df.query(query)
 cols=['metric','value','denominator','ratio','h6_group','n','target_mean','model','horizon','manuscript_reported_value','method_A_value','method_B_value','method_A_fold_sd','best_supported_original_definition','method','estimand','MAE','delta_XGBoost_minus_SeasonalHA','component','max_abs_difference','comparison','effect','CI_low','CI_high','raw_p','holm_adjusted_p','excluded_fold','descriptive_winner','winner_reversal','XGBoost_minus_SeasonalHA','XGBoost_minus_Persistence','Bias','coverage','minimum_return_age_hours']
 print(df[[c for c in cols if c in df]].to_string(index=False))
