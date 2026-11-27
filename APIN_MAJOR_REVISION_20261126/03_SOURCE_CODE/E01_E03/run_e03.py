from common import *
import zipfile
def moving_indices(dates,L,rng,B=10000):
 dates=np.asarray(dates,dtype='datetime64[D]');n=len(dates);starts=[]
 for i in range(n-L+1):
  if np.all(np.diff(dates[i:i+L]).astype(int)==1):starts.append(i)
 if n<max(2*L,10) or len(starts)<2:return None,len(starts)
 starts=np.array(starts);chosen=rng.choice(starts,size=(B,int(np.ceil(n/L))),replace=True);ix=(chosen[:,:,None]+np.arange(L)[None,None,:]).reshape(B,-1)[:,:n];return ix,len(starts)
def boot(x,ix):
 effect=float(x.mean());means=x[ix].mean(axis=1);lo,hi=np.quantile(means,[.025,.975]);centered=(x-effect)[ix].mean(axis=1);p=(1+np.count_nonzero(np.abs(centered)>=abs(effect)))/(len(ix)+1)
 return effect,float(lo),float(hi),float(p)
def main():
 log('E03 START');aligned=read('aligned_predictions');paired=read('paired_loss');seed=pd.read_csv(DER/'seed_metrics.csv');m=read('target_completeness_and_reliability');r=read('reliability_conditioned_predictions');hourly=read('hourly_analysis')
 fold=perf(aligned,['fold','horizon','model']);fold['aggregation']='A_ENSEMBLE_PREDICTION';save(fold,E03/'E03_02_Fold_Model_Metrics.csv')
 b=seed.groupby(['fold','horizon','model'],observed=True).agg(B_mean_seed_MAE=('MAE','mean'),B_mean_seed_RMSE=('RMSE','mean'),n=('n','first')).reset_index()
 recon=fold.merge(b,on=['fold','horizon','model'],validate='one_to_one',suffixes=('','_B'));saved=pd.read_csv(BASE/'04_METRICS/fold_level_model_metrics.csv');recon=recon.merge(saved[['fold','horizon','model','MAE','RMSE']],on=['fold','horizon','model'],validate='one_to_one',suffixes=('_A','_original_saved'))
 recon['A_minus_B']=recon.MAE_A-recon.B_mean_seed_MAE;recon['A_minus_saved']=recon.MAE_A-recon.MAE_original_saved;recon['B_minus_saved']=recon.B_mean_seed_MAE-recon.MAE_original_saved
 recon['best_supported_original_definition']=np.where(recon.A_minus_saved.abs()<1e-9,'A_ENSEMBLE',np.where(recon.B_minus_saved.abs()<1e-9,'B_MEAN_SEED','NEITHER_EXACT'))
 recon['Jensen_MAE_check']=recon.MAE_A<=recon.B_mean_seed_MAE+1e-10;assert recon.Jensen_MAE_check.all();save(recon,E03/'E03_01_Seed_Aggregation_Reconciliation.csv')
 with zipfile.ZipFile(ROOT/'Applied_Intelligence_20260905.zip') as z:tex=z.read('main.tex').decode('utf-8')
 block=tex[tex.find('\\label{tab:main_mae}'):];block=block[:block.find('\\end{table}')];reported={}
 for model in MODELS:
  line=next(line for line in block.splitlines() if re.match(r'^'+model+r'\s*&',line))
  nums=re.findall(r'\$([0-9.]+)\\pm([0-9.]+)\$',line);assert len(nums)==3
  for H,(mean,sd) in zip(HS,nums):reported[model,H]=(float(mean),float(sd))
 original=pd.read_csv(BASE/'04_METRICS/model_horizon_summary.csv');tab=[]
 for (model,H),x in recon.groupby(['model','horizon']):
  hist=original[(original.model==model)&(original.horizon==H)].iloc[0];value,sd=reported[model,H];A=x.MAE_A.mean();B=x.B_mean_seed_MAE.mean();A_sd=x.MAE_A.std(ddof=1);B_sd=x.B_mean_seed_MAE.std(ddof=1)
  tab.append(dict(model=model,horizon=H,manuscript_reported_value=value,manuscript_reported_sd=sd,historical_unrounded_mean=hist.MAE_mean,method_A_value=A,method_B_value=B,method_A_fold_sd=A_sd,method_B_fold_sd=B_sd,difference_A_vs_reported=A-value,difference_B_vs_reported=B-value,difference_A_vs_saved=A-hist.MAE_mean,difference_B_vs_saved=B-hist.MAE_mean,A_round3_match=round(A,3)==value,B_round3_match=round(B,3)==value,best_supported_original_definition='A_ENSEMBLE' if abs(A-hist.MAE_mean)<1e-9 else 'B_MEAN_SEED' if abs(B-hist.MAE_mean)<1e-9 else 'NEITHER_EXACT',discrepancy_status='MATCH' if abs(A-hist.MAE_mean)<1e-9 else 'EQUATION12_VS_SAVED_AGGREGATION_MISMATCH',explanation='full precision saved metrics compared; manuscript rounding alone is not implementation proof'))
 tab=pd.DataFrame(tab);save(tab,E03/'E03_03_Original_vs_Recomputed_Table7.csv')
 # Recover only missing B per-sample losses once, not another full 180-file join.
 bp=DER/'method_B_sample_losses.parquet'
 if bp.exists():pb=pd.read_parquet(bp);log('reuse cached B sample losses')
 else:
  pb=paired[['fold','horizon','sample_id','node_id','forecast_origin','spatial_block','y_true',*MODELS]].copy()
  for (fold_id,H),idx in pb.groupby(['fold','horizon'],observed=True).groups.items():
   order=pb.loc[idx].sort_values('sample_id').index
   for model in ['XGBoost','GRU']:
    losses=[]
    for s in SEEDS:
     p=BASE/f'03_FORMAL_PREDICTIONS/predictions/{model}_F{fold_id}_H{H}_S{s}.parquet';x=pd.read_parquet(p,columns=['sample_id','y_true','y_pred']).sort_values('sample_id');assert np.array_equal(x.sample_id,pb.loc[order,'sample_id']);losses.append(np.abs(x.y_pred.to_numpy()-x.y_true.to_numpy()))
    pb.loc[order,model]=np.mean(losses,axis=0)
  save(pb,bp);log('targeted B-loss extraction saved once for seed/weight attribution')
 estimands=[];daily_rows=[];history_cells=pd.read_csv(BASE/'05_STATISTICS/spatial_block_day_metrics.csv');history_days=pd.read_csv(BASE/'05_STATISTICS/day_level_metrics.csv');hist_boot=pd.read_csv(BASE/'05_STATISTICS/clustered_day_spatial_block_bootstrap.csv');decomp=[]
 for method,wide in [('A_ENSEMBLE_PREDICTION',paired),('B_MEAN_SEED_LOSS',pb)]:
  for H,x in wide.groupby('horizon',observed=True):
   x=x.copy();x['date']=x.forecast_origin.dt.normalize();fm=x.groupby('fold')[MODELS].mean().mean();sw=x[MODELS].mean();dm=x.groupby('date')[MODELS].mean();cell=x.groupby(['date','spatial_block'])[MODELS].mean();historical=history_cells[history_cells.horizon==H].pivot(index=['calendar_day','spatial_block'],columns='model',values='MAE');historical.index=historical.index.set_levels(pd.to_datetime(historical.index.levels[0]),level=0)
   for label,means,weight in [('Fold-macro',fm,'equal fold means'),('Sample-weighted',sw,'equal common test rows'),('Day-macro',dm.mean(),'equal valid local forecast-origin dates'),('Day-spatial-block',cell.mean(),'equal observed date x historical spatial_block cells')]:
    for model in MODELS:estimands.append(dict(method=method,estimand=label,horizon=H,model=model,MAE=means[model],n=len(x),dates=x.date.nunique(),folds=x.fold.nunique(),nodes=x.node_id.nunique(),spatial_cells=len(cell),weight_definition=weight,delta_XGBoost_minus_SeasonalHA=means.XGBoost-means.SeasonalHA,delta_XGBoost_minus_Persistence=means.XGBoost-means.Persistence))
   if method=='A_ENSEMBLE_PREDICTION':
    for date,z in x.groupby('date'):
     for a,bb in PAIRS+[('XGBoost','Persistence'),('Persistence','SeasonalHA')]:daily_rows.append(dict(horizon=H,date=date,model_a=a,model_b=bb,mean_loss_difference=(z[a]-z[bb]).mean(),n=len(z),nodes=z.node_id.nunique(),folds=';'.join(map(str,sorted(z.fold.unique())))))
   historical.index=historical.index.set_names(['date','spatial_block'])
   compare=cell.join(historical,lsuffix='_new',rsuffix='_saved',how='outer')
   for model in MODELS:
    decomp.append(dict(horizon=H,method=method,component='historical_cell_MAE_reconstruction',model=model,max_abs_difference=float((compare[model+'_new']-compare[model+'_saved']).abs().max()),cells=len(compare),missing_pairs=int(compare[[model+'_new',model+'_saved']].isna().any(axis=1).sum()),status='POINT_ESTIMATES_ONLY_UNKNOWN_OLD_RESAMPLING'))
 estimands=pd.DataFrame(estimands);daily=pd.DataFrame(daily_rows);save(estimands,E03/'E03_04_Weighting_Estimands.csv');save(daily,E03/'E03_05_Daily_Paired_Loss.csv');save(pd.DataFrame(decomp),E03/'E03_04b_Historical_Cluster_Reconstruction.csv')
 rng=np.random.default_rng(20261125);bootstrap=[];explore_ci={}
 for H in HS:
  x=daily[daily.horizon==H];dates=sorted(x.date.unique());matrix=x.pivot(index='date',columns=['model_a','model_b'],values='mean_loss_difference').reindex(dates)
  for L in [3,7]:
   ix,starts=moving_indices(dates,L,rng);log(f'E03 bootstrap H{H}, L={L}, dates={len(dates)}, admissible blocks={starts}')
   for a,bb in PAIRS+[('XGBoost','Persistence'),('Persistence','SeasonalHA')]:
    values=matrix[(a,bb)].to_numpy();valid=ix is not None and np.isfinite(values).all();status='CONDITIONAL_PASS_DEPENDENCE_LIMITS' if valid else 'NOT_ESTIMABLE_INFERENCE_LIMITED'
    effect=float(values.mean());lo=hi=p=np.nan
    if valid:
     effect,lo,hi,p=boot(values,ix)
     if np.std(values)==0:status='DEGENERATE';p=1. if effect==0 else np.nan
    record=dict(horizon=H,model_a=a,model_b=bb,comparison=a+'_vs_'+bb,estimand='Day-macro absolute-loss difference',effect=effect,CI_low=lo,CI_high=hi,raw_p=p,dates=len(dates),block_length=L,admissible_blocks=starts,replicates=10000,seed=20261125,role='PRESPECIFIED' if (a,bb) in PAIRS else 'EXPLORATORY',status=status,limitations='41 retrospective dates; overlapping horizons; changing fitted model at fold boundaries; entire date spatial field retained; ordinary CI not simultaneous')
    if (a,bb) in PAIRS:bootstrap.append(record)
    if H==1:explore_ci[(a,bb,L)]=record
 primary=pd.DataFrame([r for r in bootstrap if r['block_length']==3]);sensitivity=pd.DataFrame([r for r in bootstrap if r['block_length']==7]);save(primary,E03/'E03_06_Block_Bootstrap_Results.csv');save(sensitivity,E03/'E03_07_Block_Length_Sensitivity.csv')
 adjusted=[]
 for H,x in primary.groupby('horizon'):
  assert len(x)==5;pvals=x.raw_p.fillna(1).to_numpy();order=np.argsort(pvals,kind='stable');adj=np.empty(5);adj[order]=np.minimum(1,np.maximum.accumulate((5-np.arange(5))*pvals[order]))
  x=x.copy();x['holm_adjusted_p']=np.where(x.raw_p.notna(),adj,np.nan);x['family_size']=5;x['significant_holm_0_05']=x.holm_adjusted_p<.05;adjusted.append(x)
 holm=pd.concat(adjusted,ignore_index=True);assert len(holm)==15;save(holm,E03/'E03_08_Holm_Adjusted_Comparisons.csv')
 practical=[]
 h1=paired[paired.horizon==1].copy();h1['date']=h1.forecast_origin.dt.normalize()
 for a,bb in [('XGBoost','Persistence'),('XGBoost','SeasonalHA'),('Persistence','SeasonalHA')]:
  for label,x in [('ALL',h1)]:
   fd=x.groupby('fold')[[a,bb]].mean();dd=x.groupby('date')[[a,bb]].mean();ci=explore_ci.get((a,bb,3));practical.append(dict(model_a=a,model_b=bb,horizon=1,role='PRESPECIFIED_PAIR' if (a,bb) in PAIRS else 'EXPLORATORY',sample_weighted_MAE_a=x[a].mean(),sample_weighted_MAE_b=x[bb].mean(),fold_macro_delta=(fd[a]-fd[bb]).mean(),day_macro_delta=(dd[a]-dd[bb]).mean(),sample_weighted_delta=(x[a]-x[bb]).mean(),relative_improvement_percent=100*(x[bb].mean()-x[a].mean())/x[bb].mean(),fold_wins_a=int((fd[a]<fd[bb]).sum()),fold_ties=int((fd[a]==fd[bb]).sum()),fold_wins_b=int((fd[a]>fd[bb]).sum()),day_wins_a=int((dd[a]<dd[bb]).sum()),day_ties=int((dd[a]==dd[bb]).sum()),day_wins_b=int((dd[a]>dd[bb]).sum()),day_macro_CI_low=ci['CI_low'],day_macro_CI_high=ci['CI_high'],interpretation='descriptive magnitude, no unvalidated deployment value threshold'))
 save(pd.DataFrame(practical),E03/'E03_09_H1_Practical_Differences.csv')
 lofo=[]
 for method in ['A_ENSEMBLE_PREDICTION','B_MEAN_SEED_LOSS']:
  ff=fold[['fold','horizon','model','MAE']].copy() if method.startswith('A') else b[['fold','horizon','model','B_mean_seed_MAE']].rename(columns={'B_mean_seed_MAE':'MAE'})
  for H,x in ff.groupby('horizon'):
   full=x.groupby('model').MAE.mean();winner=full.idxmin()
   for exclude in [0,1,2,3,4,5,6]:
    xx=x if exclude==0 else x[x.fold!=exclude];mean=xx.groupby('model').MAE.mean();rank=mean.rank(method='min');best=mean.idxmin()
    for model in MODELS:lofo.append(dict(method=method,horizon=H,excluded_fold='NONE' if exclude==0 else exclude,model=model,MAE=mean[model],rank=int(rank[model]),descriptive_winner=best,all6_winner=winner,winner_reversal=best!=winner,XGBoost_minus_SeasonalHA=mean.XGBoost-mean.SeasonalHA,XGBoost_minus_Persistence=mean.XGBoost-mean.Persistence,folds=xx.fold.nunique()))
 save(pd.DataFrame(lofo),E03/'E03_10_LOFO_Stability.csv')
 stability=[]
 for (fold_id,H,model),x in seed[seed.model.isin(['XGBoost','GRU'])].groupby(['fold','horizon','model']):
  ensemble=fold[(fold.fold==fold_id)&(fold.horizon==H)&(fold.model==model)].MAE.iloc[0]
  for _,sr in x.iterrows():stability.append(dict(fold=fold_id,horizon=H,model=model,seed=int(sr.seed),seed_MAE=sr.MAE,mean_seed_MAE=x.MAE.mean(),seed_sd_ddof1=x.MAE.std(ddof=1),seed_min=x.MAE.min(),seed_max=x.MAE.max(),seed_range=x.MAE.max()-x.MAE.min(),ensemble_MAE=ensemble,ensemble_minus_mean_seed_MAE=ensemble-x.MAE.mean()))
 save(pd.DataFrame(stability),E03/'E03_11_Seed_Stability.csv')
 diagnostics=perf(r,['fold','horizon','traffic_regime','model']);dist=m[m.split=='test'].groupby(['fold','horizon'],observed=True).agg(target_mean=('target','mean'),target_sd=('target',lambda s:s.std(ddof=0)),target_p05=('target',lambda s:s.quantile(.05)),target_p95=('target',lambda s:s.quantile(.95)),history_coverage_mean=('history_coverage_ratio','mean'),max_gap_mean=('max_gap_24h','mean')).reset_index();diagnostics=diagnostics.merge(dist,on=['fold','horizon'],validate='many_to_one');regcounts=m[m.split=='test'].groupby(['fold','horizon','traffic_regime'],observed=True).size().rename('regime_n').reset_index();regcounts['regime_fraction']=regcounts.regime_n/regcounts.groupby(['fold','horizon']).regime_n.transform('sum');diagnostics=diagnostics.merge(regcounts,on=['fold','horizon','traffic_regime'],validate='many_to_one');save(diagnostics,E03/'E03_12_Fold_Regime_Diagnostics.csv')
 explanation=['# 权重与种子聚合方向变化：实际核验','原稿Equation(12)指定A，B是逐seed指标均值。以下为实际计算，不能把全部反转先验归因于权重。']
 for H in HS:
  xx=estimands[(estimands.horizon==H)&(estimands.model=='XGBoost')][['method','estimand','delta_XGBoost_minus_SeasonalHA']];savedhist=hist_boot[(hist_boot.horizon==H)&(hist_boot.comparison=='XGBoost_vs_SeasonalHA')]
  explanation.append(f'\n## H{H}\n\n```text\n{xx.to_string(index=False)}\n```\n\n历史保存的day×block点估计：\n```text\n{savedhist.to_string(index=False)}\n```')
 explanation.append('\n原空间块ID直接取manifest，未新造空间划分。历史点估计的数值重建范围见E03_04b；未恢复旧bootstrap源程序，因此旧CI不声称完全再现。新MBB处理日期相关性，不将205个块视为独立。跨fold连续块保留相邻日期但不同fold模型训练状态不同，仍有短样本与非平稳局限。')
 (E03/'E03_13_Estimand_Reversal_Explanation.md').write_text('\n'.join(explanation),encoding='utf-8')
 text=f'''# E03真实统计结果

主要口径A：三seed逐样本均值预测，Day-macro配对绝对损失。方法B独立保留，不按排名选择口径。原Table7对照：

```text
{tab[['model','horizon','manuscript_reported_value','method_A_value','method_B_value','best_supported_original_definition']].to_string(index=False)}
```

固定3日块10000次中心化双侧检验、每horizon五项Holm；7日敏感性。15项比较齐全，显著结果不是通过条件。

```text
{holm[['horizon','comparison','effect','CI_low','CI_high','raw_p','holm_adjusted_p']].to_string(index=False)}
```

H1竞争比较EXPLORATORY单独标记。LOFO完整保留全部六种排除以及A/B，非重训CV。HAC/DM NOT_APPLICABLE：预冻结采用MBB长度敏感性和LOFO，短回顾序列及变化模型不额外承诺平稳假设。

普通95%区间不是同时区间。保留日期内全部节点只能缓解部分依赖，41日期仍有限；不称独立盲测、无差异或等效。Fold5/6诊断只有分布与误差证据，没有核查日历或宣称节日因果。
'''
 (E03/'E03_Summary_CN.md').write_text(text,encoding='utf-8');stamp('run_e03',[DER/'aligned_predictions.parquet',DER/'paired_loss.parquet',DER/'seed_metrics.csv'],list(E03.glob('*.csv'))+list(E03.glob('*.md')),{'prespecified_comparisons':15,'table7_A_matches':int(tab.A_round3_match.sum()),'table7_B_matches':int(tab.B_round3_match.sum()),'holm_significant_count':int(holm.significant_holm_0_05.sum())});log('E03 DONE '+str({'A_table7_matches':int(tab.A_round3_match.sum()),'B_table7_matches':int(tab.B_round3_match.sum()),'Holm_significant':int(holm.significant_holm_0_05.sum())}))
if __name__=='__main__':main()
