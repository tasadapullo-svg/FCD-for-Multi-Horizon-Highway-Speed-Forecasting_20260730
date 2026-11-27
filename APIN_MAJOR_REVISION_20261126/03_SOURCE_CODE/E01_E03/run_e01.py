from common import *
def future_arrays(values,H):
 a=values.reshape(51,len(HOURS));valid=np.isfinite(a);count=np.zeros_like(a,dtype=np.int16);total=np.zeros_like(a)
 for step in range(1,H+1):count[:,:-step]+=valid[:,step:];total[:,:-step]+=np.nan_to_num(a[:,step:],nan=0)
 return count.ravel(),np.divide(total,count,out=np.full_like(total,np.nan),where=count>0).ravel()
def main():
 if '--summary-only' in sys.argv:
  expected=list(E01.glob('*.csv'));assert len(expected)>=12
  counts=pd.read_csv(E01/'E01_02_Hourly_Threshold_Coverage.csv');h6=pd.read_csv(E01/'E01_06_H6_Target_Completeness.csv');attr=pd.read_csv(E01/'E01_10_Fold_Sample_Attrition.csv')
  text=f'# E01真实计算结果\n\n协议：{PROTOCOL_SHA}。所有CSV已在生成报告时因缺少tabulate报错之前保存；本次仅补报告和receipt，不重算数据。\n\n小时覆盖率：\n\n```text\n{counts.to_string(index=False)}\n```\n\nH6测试完整度：\n\n```text\n{h6[h6.fold=="ALL_TEST"].to_string(index=False)}\n```\n\n54个split组合的样本重建键差异总数：{attr.key_mismatches.sum()}。新规则支持仅为ESTIMATED_SUPPORT；6/6子集评价不代表重新训练。归档无返回原因未知，日期修复代码仍未闭环。97.30% DEFINITION_UNRESOLVED — REMOVE_OR_REPLACE_IN_REVISION。每日分母使用实际网格；H3/H6目标不同，不用跨时距MAE证明优劣。\n'
  (E01/'E01_Summary_CN.md').write_text(text,encoding='utf-8');stamp('run_e01',[DER/'hourly_analysis.parquet',DER/'target_completeness_and_reliability.parquet'],expected+[E01/'E01_Summary_CN.md'],{'attrition_key_mismatches':int(attr.key_mismatches.sum()),'resume':'report only'});log('E01 DONE report recovered; key mismatches='+str(attr.key_mismatches.sum()));return
 log('E01 START');obs=read('observation_analysis');slots=read('returned_slot_index');q=read('quality_deduplicated_15min');hourly=read('hourly_analysis');m=read('target_completeness_and_reliability');reliability=read('reliability_conditioned_predictions')
 outputs=[];lineage=[]
 def row(metric,value,level,denominator=np.nan,reference=np.nan,definition=''):
  lineage.append(dict(metric=metric,value=value,statistical_level=level,denominator=denominator,ratio=value/denominator if denominator>0 else np.nan,historical_value=reference,difference=value-reference if np.isfinite(reference) else np.nan,definition=definition,version='REVISION_E01_E03'))
 plan15=len(HOURS)*51*4;planhour=len(hourly);good=obs.quality_pass
 row('planned_15min_slots',plan15,'node-quarter',reference=403512);row('planned_hourly_slots',planhour,'node-hour',reference=100878)
 row('returned_parsed_rows_all_span',len(obs),'return-row',reference=244477);row('quality_pass_rows_all_span',good.sum(),'return-row',reference=243307);row('quality_fail_rows_all_span',(~good).sum(),'return-row',reference=1170)
 row('quality_dedup_all_span',len(q),'node-quarter',reference=241727);row('quality_dedup_in_grid',int((slots.quality_rows>0).sum()),'node-quarter',plan15,241601)
 row('returned_rows_in_grid',int(obs.in_grid.sum()),'return-row');row('returned_rows_outside_grid',int((~obs.in_grid).sum()),'return-row')
 row('quality_dedup_outside_grid',int((~q.quarter_hour.between(GRID_START,GRID_END+pd.Timedelta(minutes=45))).sum()),'node-quarter',reference=126)
 row('unique_returned_slots',len(slots),'node-quarter',plan15);row('has_quality_slots',int((slots.quality_rows>0).sum()),'node-quarter',plan15)
 row('only_ineligible_slots',int((slots.quality_rows==0).sum()),'node-quarter',plan15);row('no_archived_return_slots',plan15-len(slots),'node-quarter',plan15)
 row('duplicate_return_rows_in_grid',int((slots.returned_rows-1).sum()),'return-row');row('duplicate_quality_rows_in_grid',int((slots.quality_rows-1).clip(lower=0).sum()),'return-row')
 assert plan15==int((slots.quality_rows>0).sum())+int((slots.quality_rows==0).sum())+plan15-len(slots)
 save(pd.DataFrame(lineage),E01/'E01_01_Data_Lineage_and_Coverage.csv');outputs.append(E01/'E01_01_Data_Lineage_and_Coverage.csv')
 threshold=[];daily=[];coverage=[]
 historical={1:96968,2:83439,3:45356,4:15838}
 for t in range(1,5):
  val=hourly[f'eligible_{t}'];eligible=int(val.sum());threshold.append(dict(threshold=t,eligible_hours=eligible,ineligible_hours=len(hourly)-eligible,planned_hours=len(hourly),coverage=eligible/len(hourly),historical_eligible=historical[t],difference=eligible-historical[t],loss_from_previous_threshold=0 if t==1 else int(hourly[f'eligible_{t-1}'].sum())-eligible,nested_in_previous=True if t==1 else bool((~val|hourly[f'eligible_{t-1}']).all())))
  for date,x in hourly.groupby('date',sort=True):daily.append(dict(resolution='hourly',threshold=t,date=date,planned=len(x),observed=int(x[f'eligible_{t}'].sum()),coverage=x[f'eligible_{t}'].mean(),incomplete_start_day=date==GRID_START.normalize()))
  for dims in [['node_id'],['hour_of_day'],['node_id','hour_of_day'],['node_id','date'],['weekend']]:
   for k,x in hourly.groupby(dims,observed=True,sort=True):
    k=k if isinstance(k,tuple) else(k,);r={c:None for c in ['node_id','hour_of_day','date','weekend']};r.update(dict(zip(dims,k)));r.update(dimension='x'.join(dims),threshold=t,planned=len(x),observed=int(x[f'eligible_{t}'].sum()),coverage=x[f'eligible_{t}'].mean());coverage.append(r)
 # Explicit counts for valid-quarter support, including zeros.
 freq=hourly.valid_quarters.value_counts().reindex(range(5),fill_value=0)
 save(freq.rename_axis('valid_quarters').reset_index(name='hour_count'),E01/'E01_02b_Quarter_Count_Frequency.csv')
 for date in pd.date_range(GRID_START.normalize(),GRID_END.normalize(),freq='D'):
  planned=int(((HOURS>=date)&(HOURS<date+pd.Timedelta(days=1))).sum()*51*4);x=slots[slots.quarter_hour.dt.normalize()==date]
  for label,n in [('ARCHIVED_RETURN',len(x)),('QUALITY_DEDUP',int((x.quality_rows>0).sum()))]:daily.append(dict(resolution='15min_'+label,threshold=np.nan,date=date,planned=planned,observed=n,coverage=n/planned,incomplete_start_day=date==GRID_START.normalize()))
 save(pd.DataFrame(threshold),E01/'E01_02_Hourly_Threshold_Coverage.csv');save(pd.DataFrame(daily),E01/'E01_03_Daily_Coverage.csv');save(pd.DataFrame(coverage),E01/'E01_04_Node_Hour_Coverage.csv')
 runs=[]
 for t in range(1,5):
  for node,x in hourly.groupby('node_id',sort=True):
   missing=(~x[f'eligible_{t}']).to_numpy();edges=np.diff(np.r_[False,missing,False].astype(int));starts=np.where(edges==1)[0];ends=np.where(edges==-1)[0]
   for start,end in zip(starts,ends):runs.append(dict(threshold=t,node_id=node,length_hours=end-start,left_censored=start==0,right_censored=end==len(x)))
 run_df=pd.DataFrame(runs);run_dist=run_df.groupby(['threshold','length_hours'],observed=True).agg(run_count=('node_id','size'),nodes=('node_id','nunique'),left_censored_runs=('left_censored','sum'),right_censored_runs=('right_censored','sum')).reset_index();save(run_dist,E01/'E01_05_Missing_Run_Distribution.csv')
 complete=m[m.horizon==6].groupby(['fold','split','h6_group'],observed=True).agg(n=('sample_id','size'),target_mean=('target','mean'),target_sd=('target',lambda s:s.std(ddof=0)),target_median=('target','median'),target_p05=('target',lambda s:s.quantile(.05)),target_p95=('target',lambda s:s.quantile(.95))).reset_index();complete['fraction_within_fold_split']=complete.n/complete.groupby(['fold','split']).n.transform('sum')
 pooled=m[(m.horizon==6)&(m.split=='test')].groupby('h6_group',observed=True).agg(n=('sample_id','size'),target_mean=('target','mean'),target_sd=('target',lambda s:s.std(ddof=0)),target_median=('target','median'),target_p05=('target',lambda s:s.quantile(.05)),target_p95=('target',lambda s:s.quantile(.95))).reset_index();pooled['fold']='ALL_TEST';pooled['split']='test';pooled['fraction_within_fold_split']=pooled.n/pooled.n.sum();save(pd.concat([complete,pooled],ignore_index=True),E01/'E01_06_H6_Target_Completeness.csv')
 position=m[(m.horizon==6)&(m.h6_group=='PARTIAL_5_OF_6')].groupby(['fold','split','missing_position'],observed=True).size().rename('n').reset_index();posall=position[position.split=='test'].groupby('missing_position').n.sum().reset_index();posall['fold']='ALL_TEST';posall['split']='test';save(pd.concat([position,posall],ignore_index=True),E01/'E01_07_H6_Missing_Position.csv')
 hh=reliability[reliability.horizon==6];pr=perf(hh,['fold','horizon','h6_group','model']);allpr=perf(hh,['horizon','h6_group','model']);allpr['fold']='ALL_TEST';save(pd.concat([pr,allpr],ignore_index=True),E01/'E01_08_H6_Stratified_Model_Performance.csv')
 # Frozen eligibility reconstruction and disjoint/non-disjoint attrition.
 candidates=[];attr=[];feas=[];hidx=np.tile(np.arange(len(HOURS)),51)
 for t in range(1,5):
  for length in ([12,24,48] if t==2 else [24]):
   for H in HS:
    cnt,targ=future_arrays(hourly[f'speed_{t}_of_4'].to_numpy(),H)
    for required in ([5,6] if H==6 else [H]):
     for fold,splits in FOLDS.items():
      for split,(lo,hi) in splits.items():
       in_split=hourly.hour.ge(lo)&hourly.hour.lt(hi);ix=np.where(in_split)[0];times=hourly.hour.iloc[ix]
       boundary=(times+pd.Timedelta(hours=H)>=hi).to_numpy()|(times+pd.Timedelta(hours=H)>GRID_END).to_numpy();history=hidx[ix]<length-1;incomplete=cnt[ix]<required
       eligible=~boundary&~history&~incomplete
       r=dict(fold=fold,horizon=H,split=split,threshold=t,history_hours=length,target_required=required,theoretical_candidates=len(ix),estimated_eligible=int(eligible.sum()),empty=not eligible.any(),support_label='ESTIMATED_SUPPORT' if t!=2 or length!=24 or (H==6 and required==6) else 'RECONSTRUCTED_BASELINE_RULES')
       feas.append(r)
       if t==2 and length==24 and required==({1:1,3:3,6:5}[H]):
        reason=np.select([boundary,history,incomplete],['TARGET_OUTSIDE_SPLIT','HISTORY_GRID_SHORT','TARGET_INCOMPLETE'],default='ELIGIBLE')
        df=hourly.iloc[ix][['panel_row_id','node_id','hour','coverage_rebuilt','gap_rebuilt','age_rebuilt','observable_history_speed','observable_history_confidence','observable_history_ratio']].copy().rename(columns={'hour':'forecast_origin'});df['fold']=fold;df['horizon']=H;df['split']=split;df['target_count']=cnt[ix];df['partial_observed_target_mean']=targ[ix];df['target_boundary']=boundary;df['history_short']=history;df['target_incomplete']=incomplete;df['exclusion_reason']=reason;df['eligible_rebuilt']=eligible
        actual=m[(m.fold==fold)&(m.horizon==H)&(m.split==split)];keys=pd.MultiIndex.from_frame(df[['node_id','forecast_origin']]);actualkeys=pd.MultiIndex.from_frame(actual[['node_id','forecast_origin']]);df['in_frozen_manifest']=keys.isin(actualkeys)
        mismatch=int((df.eligible_rebuilt!=df.in_frozen_manifest).sum());candidates.append(df)
        counts=pd.Series(reason).value_counts();attr.append(dict(fold=fold,horizon=H,split=split,theoretical_candidates=len(ix),exclusive_target_boundary=int(counts.get('TARGET_OUTSIDE_SPLIT',0)),exclusive_history_short=int(counts.get('HISTORY_GRID_SHORT',0)),exclusive_target_incomplete=int(counts.get('TARGET_INCOMPLETE',0)),other_verified=0,eligible_rebuilt=int(eligible.sum()),actual_manifest=len(actual),key_mismatches=mismatch,nonexclusive_target_boundary=int(boundary.sum()),nonexclusive_history_short=int(history.sum()),nonexclusive_target_incomplete=int(incomplete.sum()),status='PASS' if mismatch==0 else 'CONDITIONAL_PASS_RECONSTRUCTION_MISMATCH'))
 candidates=pd.concat(candidates,ignore_index=True);save(candidates,DER/'forecast_origin_eligibility.parquet');save(pd.DataFrame(attr),E01/'E01_10_Fold_Sample_Attrition.csv');save(pd.DataFrame(feas),E01/'E01_11_E04_Sample_Feasibility.csv')
 common=[]
 for fold in range(1,7):
  x=candidates[(candidates.fold==fold)&(candidates.split=='test')];x3=x[x.horizon==3];x6=x[x.horizon==6]
  a=x3[['node_id','forecast_origin','in_frozen_manifest','partial_observed_target_mean']].merge(x6[['node_id','forecast_origin','in_frozen_manifest','partial_observed_target_mean']],on=['node_id','forecast_origin'],suffixes=('_H3','_H6'),validate='one_to_one');both=a.in_frozen_manifest_H3&a.in_frozen_manifest_H6
  common.append(dict(fold=fold,theoretical_origin_universe=len(a),both_valid=int(both.sum()),H3_only=int((a.in_frozen_manifest_H3&~a.in_frozen_manifest_H6).sum()),H6_only=int((~a.in_frozen_manifest_H3&a.in_frozen_manifest_H6).sum()),neither_valid=int((~a.in_frozen_manifest_H3&~a.in_frozen_manifest_H6).sum()),H3_common_target_mean=a.loc[both,'partial_observed_target_mean_H3'].mean(),H6_common_target_mean=a.loc[both,'partial_observed_target_mean_H6'].mean(),H3_common_target_variance=a.loc[both,'partial_observed_target_mean_H3'].var(ddof=0),H6_common_target_variance=a.loc[both,'partial_observed_target_mean_H6'].var(ddof=0),H6_partial5_test=int(((m.fold==fold)&(m.horizon==6)&(m.split=='test')&(m.h6_group=='PARTIAL_5_OF_6')).sum()),interpretation='different targets, no cross-horizon MAE superiority claim'))
 save(pd.DataFrame(common),E01/'E01_09_H3_H6_Common_Origins.csv')
 ds=pd.DataFrame(daily);sums=[]
 for (resolution,t),x in ds.groupby(['resolution','threshold'],dropna=False):sums.append(dict(resolution=resolution,threshold=t,slot_weighted=x.observed.sum()/x.planned.sum(),day_macro=x.coverage.mean(),dates=len(x)))
 save(pd.DataFrame(sums),E01/'E01_03b_Coverage_Weighting.csv')
 summary=f'''# E01真实计算结果

协议：{PROTOCOL_SHA}。正式15min分母{plan15}；小时分母{planhour}。记录行与槽位分别登记，槽位互斥分解恒等式通过。

{pd.DataFrame(threshold).to_string(index=False)}

H6完整度测试样本：
{pooled.to_string(index=False)}

样本漏斗重建键差异总计：{sum(a['key_mismatches'] for a in attr)}；54个split组合。原因优先级已预冻结，同时输出非互斥原因。新规则支持为ESTIMATED_SUPPORT，不是新训练数据验收。

97.30%：DEFINITION_UNRESOLVED — REMOVE_OR_REPLACE_IN_REVISION；本阶段不再追查候选Excel。日分母按实际网格，首日只有10小时/节点。

H3/H6共同origin与方差已计算，不同未来均值不可直接跨时距比较MAE。6/6子集性能不代表6/6重训。归档无返回原因未知，日期修复程序仍未找回。
'''
 (E01/'E01_Summary_CN.md').write_text(summary,encoding='utf-8');outputs=list(E01.glob('*.csv'))+[E01/'E01_Summary_CN.md'];stamp('run_e01',[DER/'hourly_analysis.parquet',DER/'target_completeness_and_reliability.parquet'],outputs,{'attrition_key_mismatches':sum(a['key_mismatches'] for a in attr)});log('E01 DONE '+str({'slot_plan':plan15,'H6_test':pooled[['h6_group','n']].to_dict('records'),'attrition_mismatches':sum(a['key_mismatches'] for a in attr)}))
if __name__=='__main__':main()
