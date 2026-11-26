"""Targeted Ridge SVD refits against frozen Cholesky artifacts; never overwrites G2."""
from pathlib import Path
import json,sys,time
import numpy as np,pandas as pd,joblib
from sklearn.linear_model import Ridge

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'03_CODE/E04_E07_REVISION'))
from data_engine import prepare
from g2_common import metrics
OUT=ROOT/'04_EXPERIMENTS/FINAL_TARGETED_CHECKS'
reg=pd.read_csv(ROOT/'04_EXPERIMENTS/G2_E04_E07_ACCEPTANCE/G2_02_Experiment_Run_Registry.csv')
affected=pd.read_csv(OUT/'Ridge_Affected_Run_Registry.csv')
protocol=json.loads((ROOT/'00_PROJECT_CONTROL/FINAL_Closure_Protocol.json').read_text(encoding='utf-8'))['ridge_solver_comparison']
assert protocol['maximum_absolute_prediction_difference_kmh']==1e-4
assert protocol['maximum_absolute_mae_difference_kmh']==1e-5
mode=sys.argv[1] if len(sys.argv)>1 else 'initial'
if mode=='initial':
    candidates=affected[(affected.condition=='base')&(affected.fold==1)]
    worst=affected[affected.warning_logged].sort_values('min_rcond').groupby('condition',sort=False).head(1)
    selected=pd.concat([candidates,worst]).drop_duplicates('run_id')
elif mode=='all_warning':selected=affected[affected.warning_logged]
elif mode=='affected_alpha_ge_1':selected=affected[affected.configuration_json.map(lambda s:json.loads(s)['alpha']>=1.0)]
else:raise ValueError(mode)
selected=selected.sort_values(['condition','horizon','fold','run_id'])
path=OUT/'Ridge_Numerical_Stability_Check.csv'
done=pd.read_csv(path) if path.exists() else pd.DataFrame()
done_ids=set(done.run_id) if not done.empty else set()
start=time.perf_counter()

for row in selected.itertuples(index=False):
    if row.run_id in done_ids:continue
    cfg=json.loads(row.configuration_json)
    assert cfg['solver']=='cholesky' and cfg['fit_intercept'] is True
    data=prepare(row.condition,int(row.fold),int(row.horizon))
    assert data.meta['manifest_sha256']==row.manifest_sha256,(row.run_id,'manifest mismatch')
    tr=data.split('train');va=data.split('validation');te=data.split('test')
    x=data.tabular();y=data.manifest.y_true.to_numpy(dtype=np.float32)
    folder=ROOT/row.local_artifact_relpath
    old=joblib.load(folder/'model.joblib')
    assert old.alpha==cfg['alpha'] and old.solver=='cholesky' and old.fit_intercept
    svd=Ridge(alpha=cfg['alpha'],solver='svd',fit_intercept=True)
    fit_start=time.perf_counter();svd.fit(x[tr],y[tr]);fit_seconds=time.perf_counter()-fit_start
    result={'run_id':row.run_id,'condition':row.condition,'fold':int(row.fold),'horizon':int(row.horizon),
            'alpha':cfg['alpha'],'warning_logged':bool(row.warning_logged),'min_logged_rcond':row.min_rcond,
            'manifest_sha256':row.manifest_sha256,'train_n':len(tr),'validation_n':len(va),'test_n':len(te),
            'svd_fit_seconds':fit_seconds,'original_solver':'cholesky','diagnostic_solver':'svd'}
    for name,ix in [('validation',va),('test',te)]:
        original_file=folder/f'predictions_{name}.parquet'
        if not original_file.exists():continue
        old_pred=np.asarray(old.predict(x[ix]),dtype=float)
        svd_pred=np.asarray(svd.predict(x[ix]),dtype=float)
        archived=pd.read_parquet(original_file)
        assert archived.sample_id.tolist()==data.manifest.iloc[ix].sample_id.tolist()
        target=data.manifest.y_true.to_numpy()[ix]
        assert np.allclose(archived.y_true.to_numpy(),target,atol=0,rtol=0)
        old_m=metrics(y[ix] if name=='validation' else target,old_pred)
        new_m=metrics(y[ix] if name=='validation' else target,svd_pred)
        result[f'{name}_archived_vs_model_maxdiff']=float(np.max(np.abs(archived.y_pred.to_numpy()-old_pred)))
        result[f'{name}_max_abs_prediction_diff_kmh']=float(np.max(np.abs(svd_pred-old_pred)))
        result[f'{name}_mean_abs_prediction_diff_kmh']=float(np.mean(np.abs(svd_pred-old_pred)))
        result[f'{name}_all_predictions_finite']=bool(np.isfinite(svd_pred).all())
        for k in ['MAE','RMSE','Bias']:
            result[f'{name}_{k}_old']=old_m[k]
            result[f'{name}_{k}_svd']=new_m[k]
            result[f'{name}_{k}_delta']=new_m[k]-old_m[k]
            result[f'{name}_{k}_round3_changed']=round(new_m[k],3)!=round(old_m[k],3)
    result['prediction_tolerance_pass']=all(result.get(f'{name}_max_abs_prediction_diff_kmh',0)<=protocol['maximum_absolute_prediction_difference_kmh'] for name in ['validation','test'])
    result['mae_tolerance_pass']=all(abs(result.get(f'{name}_MAE_delta',0))<=protocol['maximum_absolute_mae_difference_kmh'] for name in ['validation','test'])
    done=pd.concat([done,pd.DataFrame([result])],ignore_index=True)
    done.to_csv(path,index=False,encoding='utf-8-sig')
    print(row.run_id,row.condition,'F',row.fold,'H',row.horizon,'a',cfg['alpha'],'max',result.get('test_max_abs_prediction_diff_kmh',result.get('validation_max_abs_prediction_diff_kmh')),'pass',result['prediction_tolerance_pass'],result['mae_tolerance_pass'],flush=True)
print('TOTAL_CHECKED',len(done),'MODE',mode,'NEW_ELAPSED_S',time.perf_counter()-start)
