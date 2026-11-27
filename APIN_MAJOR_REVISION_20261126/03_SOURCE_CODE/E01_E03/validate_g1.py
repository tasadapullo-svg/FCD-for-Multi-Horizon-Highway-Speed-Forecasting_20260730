from common import *
def main():
 log('G1 one-time scientific acceptance validation START');checks=[]
 def check(id,passed,detail,status='PASS'):checks.append(dict(check_id=id,status=status if passed else 'BLOCKED',detail=detail))
 def csvr(path):return pd.read_csv(path)
 line=csvr(E01/'E01_01_Data_Lineage_and_Coverage.csv').set_index('metric');threshold=csvr(E01/'E01_02_Hourly_Threshold_Coverage.csv');attr=csvr(E01/'E01_10_Fold_Sample_Attrition.csv');align=csvr(DER/'prediction_alignment_checks.csv');feature=csvr(DER/'feature_recovery_audit.csv');hol=csvr(E03/'E03_08_Holm_Adjusted_Comparisons.csv');recon=csvr(E03/'E03_01_Seed_Aggregation_Reconciliation.csv');tab=csvr(E03/'E03_03_Original_vs_Recomputed_Table7.csv');daily=csvr(E03/'E03_05_Daily_Paired_Loss.csv');lofo=csvr(E03/'E03_10_LOFO_Stability.csv');hist=csvr(E03/'E03_04b_Historical_Cluster_Reconstruction.csv')
 check('PROTOCOL_UNCHANGED',PROTOCOL_SHA==json.loads((CTL/'G1_Protocol_Freeze_Receipt.json').read_text(encoding='utf-8'))['sha256'],PROTOCOL_SHA)
 count=lambda k:int(line.loc[k,'value'])
 check('SLOT_PARTITION',count('planned_15min_slots')==count('has_quality_slots')+count('only_ineligible_slots')+count('no_archived_return_slots'),f"{count('planned_15min_slots')}={count('has_quality_slots')}+{count('only_ineligible_slots')}+{count('no_archived_return_slots')}")
 check('RECORD_PARTITION',count('returned_parsed_rows_all_span')==count('quality_pass_rows_all_span')+count('quality_fail_rows_all_span'),'row-level distinct from slot-level')
 check('THRESHOLDS',threshold.difference.eq(0).all()&threshold.nested_in_previous.all(),'four counts independently recomputed from input and nested')
 check('54_ATTRITION_COMBINATIONS',len(attr)==54 and attr.key_mismatches.eq(0).all(),'mutually exclusive reconstruction matches all original manifests')
 check('ATTRITION_IDENTITIES',(attr.theoretical_candidates==attr.exclusive_target_boundary+attr.exclusive_history_short+attr.exclusive_target_incomplete+attr.other_verified+attr.eligible_rebuilt).all(),'exclusive reason totals equal theoretical')
 check('TEST_COUNTS',attr[attr.split=='test'].groupby('horizon').actual_manifest.sum().to_dict()=={1:38201,3:24805,6:29141},'test total92147')
 check('ALIGNED_6_MODELS_18_TASKS',len(align)==108 and align.key_match.all() and align.truth_match.all() and align.predictions_finite.all(),'all six models x18 common tasks; raw180 runs three seeds explicitly checked')
 check('FEATURE_UNITS',feature.coverage_restore_max_diff.max()<1e-5 and feature.gap_restore_max_diff.max()<1e-4 and feature.volatility_rebuild_max_diff.max()<1e-4,'restored original scaler units, causal ddof0 volatility maxdiff '+str(feature.volatility_rebuild_max_diff.max()))
 check('SEED_JENSEN',recon.Jensen_MAE_check.all(),'ensemble MAE <= mean seed-level MAE')
 stochastic=tab[tab.model.isin(['XGBoost','GRU'])];check('TABLE7_DISCREPANCY_RECORDED',len(stochastic)==6 and stochastic.best_supported_original_definition.eq('B_MEAN_SEED').all(),'Table7 six stochastic cells match B not Equation12 A','CONDITIONAL_PASS')
 check('15_PRESPECIFIED_TESTS',len(hol)==15 and hol.groupby('horizon').size().eq(5).all(),'all horizon families retained')
 effectcheck=True
 for _,r in hol.iterrows():
  d=daily[(daily.horizon==r.horizon)&(daily.model_a==r.model_a)&(daily.model_b==r.model_b)]
  effectcheck &= abs(d.mean_loss_difference.mean()-r.effect)<1e-10
 check('DAILY_EFFECT_ESTIMAND',effectcheck,'each bootstrap point estimate equals mean daily paired loss')
 holmok=True
 for H,x in hol.groupby('horizon'):
  x=x.sort_values('raw_p');p=x.raw_p.to_numpy();expected=np.maximum.accumulate([min(1,(5-i)*value) for i,value in enumerate(p)]);holmok &= np.max(np.abs(expected-x.holm_adjusted_p.to_numpy()))<1e-9
 check('HOLM_ALGORITHM',holmok,'independent sorted family calculation verified')
 check('BOOTSTRAP_P_FINITE',hol.raw_p.between(1/10001-5e-13,1+5e-13).all() and hol.CI_low.le(hol.CI_high).all(),'centered bootstrap test plus finite correction; CSV12-digit serialization tolerance5e-13; CI ordinary percentile')
 check('LOFO_FULL',len(lofo)==252 and lofo.groupby(['method','horizon','model']).size().eq(7).all(),'A/B x3 horizons x6models xall+6 exclusions')
 check('HISTORICAL_BLOCK_B',hist[hist.method=='B_MEAN_SEED_LOSS'].max_abs_difference.max()<1e-9 and hist.cells.eq(205).all() and hist.missing_pairs.eq(0).all(),'205 old day-block point estimates exactly reconstructed; old CI resampling remains partial')
 base=read('freeflow_baseline_predictions');check('FREEFLOW_NO_FUTURE',base.freeflow_return_age_hours.dropna().ge(1).all(),'conservative >=1hour historical return plus parsed known timestamps; ingestion logs unavailable','CONDITIONAL_PASS')
 m=read('target_completeness_and_reliability');check('TARGET_NO_IMPUTATION',np.array_equal(m.target_count_rebuilt,m.target_observed_count),'all1053618 manifest targets rebuilt solely from observed source hours')
 closure=csvr(E02/'E02_09_Closure_and_Quality_Filter.csv');check('CLOSURE_NONESTIMABILITY',closure[closure.analysis=='ROAD_CLOSURE_DISTRIBUTION'].status.str.contains('NOT_ESTIMABLE').all(),'no observed closure events, no synthetic effects','NOT_ESTIMABLE')
 save(pd.DataFrame(checks),G1/'G1_Validation_Checks.csv');status='BLOCKED' if any(c['status']=='BLOCKED' for c in checks) else 'CONDITIONAL_PASS';jwrite(G1/'G1_Validation_Receipt.json',{'overall_status':status,'created_at':now(),'protocol_sha256':PROTOCOL_SHA,'checks':checks,'policy':'accepted outputs immutable; only concrete scientific/code issue reopens affected tasks; no whole E01-E03 repeat'})
 log('G1 validation '+status+' '+str(collections.Counter(c['status'] for c in checks)) if False else 'G1 validation '+status);print(pd.DataFrame(checks).to_string(index=False))
if __name__=='__main__':main()
