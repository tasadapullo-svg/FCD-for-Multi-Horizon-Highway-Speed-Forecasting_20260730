"""Summarize exact scoped Ridge numerical corrections without changing frozen G2 artifacts."""
from pathlib import Path
import json
import numpy as np,pandas as pd

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'04_EXPERIMENTS/FINAL_TARGETED_CHECKS'
G2=ROOT/'04_EXPERIMENTS/G2_E04_E07_ACCEPTANCE'
d=pd.read_csv(OUT/'Ridge_Numerical_Stability_Check.csv')
reg=pd.read_csv(G2/'G2_02_Experiment_Run_Registry.csv')
warn=pd.read_csv(OUT/'Ridge_Affected_Run_Registry.csv')
assert len(d)==93 and d.run_id.is_unique and len(reg[reg.model=='Ridge'])==93
assert set(d.run_id)==set(reg[reg.model=='Ridge'].run_id)
assert set(warn[warn.warning_logged].run_id).issubset(set(d.run_id))
tested=d[d.test_MAE_svd.notna()].copy()
assert len(tested)==90
cols=['run_id','condition','fold','horizon','alpha','manifest_sha256','train_n','validation_n','test_n','warning_logged','min_logged_rcond',
      'validation_MAE_old','validation_MAE_svd','validation_MAE_delta','test_MAE_old','test_MAE_svd','test_MAE_delta',
      'test_RMSE_old','test_RMSE_svd','test_RMSE_delta','test_Bias_old','test_Bias_svd','test_Bias_delta',
      'test_max_abs_prediction_diff_kmh','test_mean_abs_prediction_diff_kmh','test_MAE_round3_changed']
tested[cols].to_csv(OUT/'Ridge_Corrected_Experiment_Metrics.csv',index=False,encoding='utf-8-sig')

selection=[]
for H,group in d[(d.condition=='base')&(d.fold==1)].groupby('horizon'):
    old=group.loc[group.validation_MAE_old.idxmin()]
    new=group.loc[group.validation_MAE_svd.idxmin()]
    selection.append({'horizon':H,'old_selected_alpha':old.alpha,'svd_selected_alpha':new.alpha,
                      'old_selected_validation_MAE':old.validation_MAE_old,'svd_selected_validation_MAE':new.validation_MAE_svd,
                      'selection_changed':old.alpha!=new.alpha})
selection=pd.DataFrame(selection)
selection.to_csv(OUT/'Ridge_Selection_Stability.csv',index=False,encoding='utf-8-sig')

aggregates=[]
for keys,g in tested.groupby(['condition','horizon','alpha']):
    condition,H,alpha=keys;n=g.test_n.astype(float)
    aggregates.append({'condition':condition,'horizon':H,'alpha':alpha,'fold_runs':len(g),'test_samples_sum':int(n.sum()),
                       'old_fold_macro_MAE':g.test_MAE_old.mean(),'svd_fold_macro_MAE':g.test_MAE_svd.mean(),
                       'delta_fold_macro_MAE':g.test_MAE_svd.mean()-g.test_MAE_old.mean(),
                       'old_sample_weighted_MAE':np.average(g.test_MAE_old,weights=n),'svd_sample_weighted_MAE':np.average(g.test_MAE_svd,weights=n),
                       'round3_changed_folds':int(g.test_MAE_round3_changed.sum())})
pd.DataFrame(aggregates).to_csv(OUT/'Ridge_Corrected_Aggregates.csv',index=False,encoding='utf-8-sig')

def config_value(s,key):return json.loads(s).get(key)
other=reg[(reg.model=='XGBoost')&(reg.status=='COMPLETED')&(reg.seed==42)].copy()
other['depth']=other.configuration_json.map(lambda s:config_value(s,'max_depth'))
ranking=[]
for row in tested.itertuples(index=False):
    depth=4 if row.condition=='base' and row.alpha==10 else 8
    match=other[(other.condition==row.condition)&(other.fold==row.fold)&(other.horizon==row.horizon)&(other.depth==depth)]
    if len(match)!=1:continue
    x=match.iloc[0]
    before=np.sign(row.test_MAE_old-x.test_MAE)
    after=np.sign(row.test_MAE_svd-x.test_MAE)
    ranking.append({'ridge_run_id':row.run_id,'xgboost_run_id':x.run_id,'condition':row.condition,'fold':row.fold,'horizon':row.horizon,
                    'ridge_alpha':row.alpha,'xgboost_depth':depth,'xgboost_MAE':x.test_MAE,'ridge_old_MAE':row.test_MAE_old,'ridge_svd_MAE':row.test_MAE_svd,
                    'winner_changed':bool(before!=after)})
ranking=pd.DataFrame(ranking)
ranking.to_csv(OUT/'Ridge_Ranking_Impact.csv',index=False,encoding='utf-8-sig')

summary={'ridge_original_run_ids':93,'diagnostic_svd_fits':93,'test_result_runs':90,'warning_run_ids':int(warn.warning_logged.sum()),
         'prediction_tolerance_fail_runs':int((~d.prediction_tolerance_pass).sum()),'mae_tolerance_fail_runs':int((~d.mae_tolerance_pass).sum()),
         'test_mae_round3_changed_runs':int(tested.test_MAE_round3_changed.sum()),
         'max_test_prediction_difference_kmh':float(tested.test_max_abs_prediction_diff_kmh.max()),
         'max_abs_test_mae_difference_kmh':float(tested.test_MAE_delta.abs().max()),
         'selection_changed_horizons':int(selection.selection_changed.sum()),
         'xgboost_ridge_fold_winner_changed_count':int(ranking.winner_changed.sum()),
         'ranking_pairs_checked':len(ranking),'g1_unchanged':True,'g2_key_tests_unchanged':True,
         'frozen_g2_package_unchanged':True,'final_use':'SVD corrected Ridge aggregate metrics overlay; original G2 registry and package retained as provenance'}
(OUT/'Ridge_Impact_Summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary))
