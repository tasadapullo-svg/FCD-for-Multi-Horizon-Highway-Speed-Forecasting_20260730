from common import *
def paired_columns(table,group):
 pivot=table.pivot(index=group,columns='model',values='MAE')
 for a,b in [('XGBoost','SeasonalHA'),('XGBoost','Persistence')]:
  if a in pivot and b in pivot:
   diff=(pivot[a]-pivot[b]).rename('delta_'+a+'_minus_'+b).reset_index();table=table.merge(diff,on=group,how='left',validate='many_to_one')
 return table
def main():
 log('E02 START');obs=read('observation_analysis');quarter=read('quality_deduplicated_15min');hourly=read('hourly_analysis');m=read('target_completeness_and_reliability');r=read('reliability_conditioned_predictions');c=read('forecast_origin_eligibility')
 distributions=[]
 for level,df,cols in [('RETURN_ROW_UNFILTERED',obs,{'current_speed':'current_speed','free_flow_speed':'free_flow_speed'}),('RETURN_ROW_QUALITY_PASS',obs[obs.quality_pass],{'current_speed':'current_speed','free_flow_speed':'free_flow_speed'}),('DEDUP_15MIN_QUALITY_GRID',quarter[quarter.quarter_hour.between(GRID_START,GRID_END+pd.Timedelta(minutes=45))],{'current_speed':'speed_15min','free_flow_speed':'freeflow_15min'}),('HOURLY_PRIMARY_2_OF_4',hourly[hourly.observed],{'current_speed':'observed_speed','free_flow_speed':'hourly_freeflow'})]:
  for node,x in [('ALL',df),*df.groupby('node_id',sort=True)]:
   for name,col in cols.items():distributions.append(dict(level=level,node_id=node,variable=name,horizon=np.nan,unit='km/h',**describe(x[col])))
 for H in HS:
  df=m[(m.horizon==H)&(m.split=='test')]
  for node,x in [('ALL',df),*df.groupby('node_id',sort=True)]:distributions.append(dict(level='FROZEN_TEST_TARGET',node_id=node,variable='future_window_mean_speed',horizon=H,unit='km/h',**describe(x.target)))
 save(pd.DataFrame(distributions),E02/'E02_01_Speed_and_Target_Distribution.csv')
 equality=[]
 for label,df in [('RETURN_ROW_UNFILTERED',obs),('RETURN_ROW_QUALITY_PASS',obs[obs.quality_pass])]:
  groups=[('overall','ALL',df)]+[('node_id',n,x) for n,x in df.groupby('node_id')]+[('confidence_bin',n,x) for n,x in df.groupby('confidence_bin')]
  for dim,key,x in groups:
   valid=np.isfinite(x.current_speed)&np.isfinite(x.free_flow_speed)&(x.free_flow_speed>0);d=(x.loc[valid,'current_speed']-x.loc[valid,'free_flow_speed']).abs();rat=x.loc[valid,'ratio']
   equality.append(dict(level=label,dimension=dim,group=key,total_rows=len(x),valid_ratio_rows=int(valid.sum()),invalid_ratio_rows=int((~valid).sum()),exact_equal_fraction=float((d==0).mean()),within_1kmh_fraction=float((d<=1).mean()),mean_abs_difference=d.mean(),median_abs_difference=d.median(),p95_abs_difference=d.quantile(.95),ratio_mean=rat.mean(),ratio_median=rat.median(),ratio_p05=rat.quantile(.05),ratio_p95=rat.quantile(.95)))
 save(pd.DataFrame(equality),E02/'E02_02_FreeFlow_Equality.csv')
 conf=[]
 for label,df in [('RETURN_ROW_UNFILTERED',obs),('RETURN_ROW_QUALITY_PASS',obs[obs.quality_pass])]:
  for dim,group,x in [('overall','ALL',df)]+[('node_id',n,x) for n,x in df.groupby('node_id')]+[('hour_of_day',str(n),x) for n,x in df.groupby(df.event_time.dt.hour)]:
   for band,z in x.groupby('confidence_bin',observed=True):conf.append(dict(level=label,dimension=dim,group=group,confidence_bin=band,n=len(z),fraction=len(z)/len(x),current_speed_mean=z.current_speed.mean(),ratio_mean=z.ratio.mean(),**{'confidence_'+k:v for k,v in describe(z.confidence).items() if k!='n'}))
 save(pd.DataFrame(conf),E02/'E02_03_Confidence_Distribution.csv')
 traffic=[]
 for level,df,rat in [('RETURN_ROW_UNFILTERED',obs,obs.ratio),('RETURN_ROW_QUALITY_PASS',obs[obs.quality_pass],obs.loc[obs.quality_pass,'ratio'])]:
  states=regime(rat)
  for name,n in pd.Series(states).value_counts().items():traffic.append(dict(level=level,horizon=np.nan,state=name,n=int(n),fraction=n/len(df),nodes=df.node_id.nunique(),dates=df.event_time.dt.normalize().nunique(),threshold=.7))
 for H in HS:
  df=m[(m.split=='test')&(m.horizon==H)]
  for state,z in df.groupby('traffic_regime',observed=True):traffic.append(dict(level='FUTURE_OBSERVED_TARGET_HOURS',horizon=H,state=state,n=len(z),fraction=len(z)/len(df),nodes=z.node_id.nunique(),dates=z.analysis_date.nunique(),threshold=.7))
 save(pd.DataFrame(traffic),E02/'E02_04_Traffic_Regime_Distribution.csv')
 reg=paired_columns(perf(r,['horizon','traffic_regime','model']),['horizon','traffic_regime']);save(reg,E02/'E02_05_Regime_Model_Performance.csv')
 sensitivity=[]
 for t in [.6,.7,.8]:
  rr=r.assign(congestion_sensitivity=np.where(np.isfinite(r.target_ratio)&(r.target_ratio<t),'BELOW_THRESHOLD',np.where(np.isfinite(r.target_ratio),'AT_OR_ABOVE_THRESHOLD','UNCLASSIFIED')))
  p=perf(rr,['horizon','congestion_sensitivity','model']);p['threshold']=t;sensitivity.append(p)
 save(pd.concat(sensitivity,ignore_index=True),E02/'E02_05b_Regime_Threshold_Sensitivity.csv')
 gaps=[]
 for field in ['gap_bin','age_bin']:
  p=paired_columns(perf(r,['horizon',field,'model']),['horizon',field]);p['conditioning_variable']=field;p=p.rename(columns={field:'group'});gaps.append(p)
 save(pd.concat(gaps,ignore_index=True),E02/'E02_06_Gap_Conditioned_Performance.csv')
 joints=[]
 for dims in [['cov_bin'],['gap_bin'],['vol_bin'],['cov_bin','gap_bin'],['cov_bin','gap_bin','vol_bin']]:
  table=paired_columns(perf(r,['horizon',*dims,'model']),['horizon',*dims]);table['conditioning']='x'.join(dims);joints.append(table)
 save(pd.concat(joints,ignore_index=True),E02/'E02_07_Coverage_Gap_Volatility.csv')
 # Selection proxies, observable historical values only; no error calculation on ineligible targets.
 selection=[]
 test=c[c.split=='test'].copy();test['selection_group']=np.where(test.in_frozen_manifest,'ELIGIBLE',np.where((test.target_count>0)&test.target_incomplete,'EXCLUDED_PARTIAL_TARGET','EXCLUDED_OTHER'))
 variables=['coverage_rebuilt','gap_rebuilt','age_rebuilt','observable_history_speed','observable_history_confidence','observable_history_ratio']
 for (fold,H),x in test.groupby(['fold','horizon'],observed=True):
  good=x[x.in_frozen_manifest];bad=x[~x.in_frozen_manifest]
  for variable in variables:
   av=pd.to_numeric(good[variable],errors='coerce').dropna();bv=pd.to_numeric(bad[variable],errors='coerce').dropna();den=np.sqrt((av.var(ddof=0)+bv.var(ddof=0))/2);smd=(av.mean()-bv.mean())/den if den>0 else np.nan
   for group,z in x.groupby('selection_group',observed=True):selection.append(dict(record_type='NUMERIC_PROXY',fold=fold,horizon=H,selection_group=group,variable=variable,group_value='ALL',candidate_n=len(z),observed_proxy_n=z[variable].notna().sum(),mean=z[variable].mean(),median=z[variable].median(),sd=z[variable].std(ddof=0),SMD_eligible_minus_all_excluded=smd,limitation='observable selection association only; no speed or forecast errors for unreturned targets'))
  for variable,vals in [('node_id',x.node_id),('date',x.forecast_origin.dt.normalize()),('hour_of_day',x.forecast_origin.dt.hour)]:
   xx=x.assign(category=vals.astype(str))
   for (group,value),z in xx.groupby(['selection_group','category'],observed=True):selection.append(dict(record_type='CATEGORY_SUPPORT',fold=fold,horizon=H,selection_group=group,variable=variable,group_value=value,candidate_n=len(z),observed_proxy_n=len(z),fraction_within_selection=len(z)/(xx.selection_group==group).sum()))
 save(pd.DataFrame(selection),E02/'E02_08_Sample_Selection_Diagnostics.csv')
 closure=[]
 for value,n in obs.road_closure.value_counts(dropna=False).items():closure.append(dict(analysis='ROAD_CLOSURE_DISTRIBUTION',group=str(value),n=n,mean_speed=np.nan,mean_ratio=np.nan,status='NOT_ESTIMABLE — NO OBSERVED CLOSURE EVENTS' if not obs.road_closure.eq(1).any() else 'DESCRIPTIVE'))
 for label,z in obs.groupby('quality_pass',observed=True):closure.append(dict(analysis='QUALITY_FILTER',group='PASS' if label else 'FAIL',n=len(z),mean_speed=z.current_speed.mean(),mean_ratio=z.ratio.mean(),mean_confidence=z.confidence.mean(),status='PASS_DESCRIPTIVE_ONLY'))
 save(pd.DataFrame(closure),E02/'E02_09_Closure_and_Quality_Filter.csv')
 # Free-flow baseline: conservative historical known-time values, never future FF target.
 mt=m[m.split=='test'];base=mt[['fold','horizon','sample_id','node_id','forecast_origin','target','freeflow_baseline_pred','freeflow_baseline_source','freeflow_return_age_hours','traffic_regime']].rename(columns={'target':'y_true','freeflow_baseline_pred':'y_pred'});base['model']='FreeFlow_Lagged';covered=base[base.y_pred.notna()].copy();baseperf=[]
 for dims in [['horizon','model'],['horizon','traffic_regime','model']]:
  t=perf(covered,dims);t['record_type']='BASELINE_PERFORMANCE';baseperf.append(t)
 common=r.merge(covered[['fold','horizon','sample_id']],on=['fold','horizon','sample_id'],how='inner',validate='many_to_one')
 for dims in [['horizon','model'],['horizon','traffic_regime','model']]:
  t=perf(common,dims);t['record_type']='ORIGINAL_MODELS_SAME_INTERSECTION';baseperf.append(t)
 for H,x in base.groupby('horizon'):
  for method,z in x.groupby('freeflow_baseline_source'):baseperf.append(pd.DataFrame([dict(record_type='PREDICTION_AVAILABILITY',horizon=H,model='FreeFlow_Lagged',source=method,n=len(z),total_common_samples=len(x),coverage=len(z)/len(x),minimum_return_age_hours=z.freeflow_return_age_hours.min(),median_return_age_hours=z.freeflow_return_age_hours.median(),status='CONDITIONAL_TIMESTAMP_PROVENANCE_NO_INGESTION_LOGS')]))
 save(pd.concat(baseperf,ignore_index=True),E02/'E02_10_FreeFlow_Baseline.csv');save(covered,DER/'freeflow_baseline_predictions.parquet')
 # Safe histogram counts only, for diagnostic figures.
 hist=[]
 for col,edges in [('current_speed',np.arange(0,141,5)),('free_flow_speed',np.arange(0,141,5)),('confidence',np.linspace(0,1,21))]:
  counts,bins=np.histogram(obs[col].dropna(),bins=edges)
  for lo,hi,n in zip(bins[:-1],bins[1:],counts):hist.append(dict(variable=col,level='RETURN_ROW_UNFILTERED',bin_left=lo,bin_right=hi,n=int(n)))
 save(pd.DataFrame(hist),E02/'E02_01b_Distribution_Histograms.csv')
 equal=pd.DataFrame(equality);overall=equal[(equal.dimension=='overall')];teststates=pd.DataFrame(traffic);teststates=teststates[teststates.level=='FUTURE_OBSERVED_TARGET_HOURS']
 summary=f'''# E02真实计算结果

原始返回行自由流一致性：
{overall.to_string(index=False)}

未来有效目标小时交通状态支持：
{teststates.to_string(index=False)}

交通分类为操作化proxy（0.70/0.90），0.60/0.80仅固定敏感性，不选有利阈值。LOW_SUPPORT: n<30或日期<3或节点<3；不得强作显著性或稳定性解释。

Volatility从冻结X_sequence最后一行按原fold scaler还原至km/h；coverage/gap恢复已与manifest核对。因果填充重建对照见共享feature_recovery_audit.csv；若存在实质差异，原特征与论文定义差异必须在G1单独报告，不能默称恢复的特征符合ddof=0公式。

道路封闭：NOT_ESTIMABLE — NO OBSERVED CLOSURE EVENTS。供应商confidence不是经独立验证的概率；速度相等不证明历史回填或真实道路无拥堵。选择诊断只基于可观测历史proxy，不能据此证明MCAR/MAR/MNAR。

Free-flow基准采用已知记录的保守至少1h滞后和时间戳上界，不读取目标窗freeflow；无独立网络到达日志，时间可得性保留CONDITIONAL_PASS。所有比较使用相同覆盖交集，新增基准不混入原六模型排名。
'''
 (E02/'E02_Summary_CN.md').write_text(summary,encoding='utf-8');stamp('run_e02',[DER/'observation_analysis.parquet',DER/'reliability_conditioned_predictions.parquet',DER/'forecast_origin_eligibility.parquet'],list(E02.glob('*.csv'))+[E02/'E02_Summary_CN.md']);log('E02 DONE '+str({'unfiltered_exact_freeflow':float(overall.iloc[0].exact_equal_fraction),'traffic_support':teststates[['horizon','state','n']].to_dict('records')}))
if __name__=='__main__':main()
