from common import *
sys.path.insert(0,str(CTL/'plotting_deps'))
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=ROOT/'07_FIGURES_TABLES/G1_DIAGNOSTICS';OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':130,'savefig.dpi':180})
COLORS={'XGBoost':'#1565C0','SeasonalHA':'#D46A18','Persistence':'#238B58','GRU':'#8242A8','Ridge':'#6C7781','HA':'#B95260'}
sources=[]
def done(fig,name,caption,paths):
 fig.suptitle(caption,fontsize=13,fontweight='bold');fig.tight_layout(rect=[0,.03,1,.91]);fig.text(.01,.008,'REVISION_E01_E03 | Diagnostic only | provider-reported speed; not independent ground truth',fontsize=8,color='#555555');p=OUT/(name+'.png');fig.savefig(p,facecolor='white');plt.close(fig);sources.append(dict(figure=str(p),source_csv=';'.join(str(p) for p in paths),classification='aggregate diagnostic; no sample records; not original SCI figure'))
thr=pd.read_csv(E01/'E01_02_Hourly_Threshold_Coverage.csv');daily=pd.read_csv(E01/'E01_03_Daily_Coverage.csv');fig,ax=plt.subplots(1,2,figsize=(12,4.4));ax[0].bar(thr.threshold,thr.coverage*100,color='#2D718E');ax[0].set(xlabel='Eligible quarter-hours required (of 4)',ylabel='Hourly coverage (%)',ylim=(0,110));
for _,x in thr.iterrows():ax[0].text(x.threshold,x.coverage*100+2,f'{x.coverage:.1%}\nn={x.eligible_hours:,}',ha='center',fontsize=9)
x=daily[(daily.resolution=='hourly')&(daily.threshold==2)];ax[1].plot(pd.to_datetime(x.date),x.coverage*100,color='#2D718E');ax[1].set(xlabel='Local date (UTC+08)',ylabel='Primary hourly coverage (%)',ylim=(0,105));ax[1].tick_params(axis='x',rotation=25)
done(fig,'G1_D01_Coverage','Coverage: complete-hour grid, 100,878 node-hours; daily denominators retained',[E01/'E01_02_Hourly_Threshold_Coverage.csv',E01/'E01_03_Daily_Coverage.csv'])
hist=pd.read_csv(E02/'E02_01b_Distribution_Histograms.csv');fig,axes=plt.subplots(1,3,figsize=(13,4))
for ax,col,label in zip(axes,['current_speed','free_flow_speed','confidence'],['Current speed (km/h)','Free-flow speed (km/h)','Provider confidence']):
 x=hist[hist.variable==col];ax.bar((x.bin_left+x.bin_right)/2,x.n,width=(x.bin_right-x.bin_left)*.92,color='#2D718E');ax.set(xlabel=label,ylabel='Returned-row count');ax.ticklabel_format(axis='y',style='sci',scilimits=(0,0))
done(fig,'G1_D02_Return_Distributions','Unfiltered parsed returned rows (n=244,477); confidence is a provider field',[E02/'E02_01b_Distribution_Histograms.csv'])
reg=pd.read_csv(E02/'E02_05_Regime_Model_Performance.csv');fig,axes=plt.subplots(1,3,figsize=(13,4.5));states=['congested_proxy','intermediate','near_free_flow_proxy']
for H,ax in zip(HS,axes):
 for j,model in enumerate(['XGBoost','SeasonalHA','Persistence']):
  x=reg[(reg.horizon==H)&(reg.model==model)].set_index('traffic_regime').reindex(states);ax.plot(range(3),x.MAE,marker='o',label=model,color=COLORS[model])
 x=reg[(reg.horizon==H)&(reg.model=='XGBoost')].set_index('traffic_regime').reindex(states)
 ax.set_xticks(range(3),['Congested\n'+str(int(x.iloc[0]['n'])), 'Intermediate\n'+str(int(x.iloc[1]['n'])),'Near FF\n'+str(int(x.iloc[2]['n']))]);ax.set(title=f'H{H} future-window task',ylabel='MAE (km/h)',xlabel='Target-window ratio class; n shown')
axes[0].legend(fontsize=8);done(fig,'G1_D03_Regime_MAE','Descriptive performance on identical valid targets; state uses observed target hours',[E02/'E02_05_Regime_Model_Performance.csv'])
gap=pd.read_csv(E02/'E02_06_Gap_Conditioned_Performance.csv');fig,axes=plt.subplots(1,3,figsize=(13,4.5));bins=['0','1-2','3-6','7-12','13-24']
for H,ax in zip(HS,axes):
 for model in ['XGBoost','SeasonalHA','Persistence']:
  x=gap[(gap.horizon==H)&(gap.model==model)&(gap.conditioning_variable=='gap_bin')].set_index('group').reindex(bins);ax.plot(range(5),x.MAE,marker='o',label=model,color=COLORS[model])
 ax.set_xticks(range(5),bins,rotation=25);ax.set(title=f'H{H}',xlabel='Longest missing run in prior 24h (hours)',ylabel='MAE (km/h)')
axes[0].legend(fontsize=8);done(fig,'G1_D04_Gap_MAE','Descriptive reliability conditioning; support and other coverage/volatility strata in CSV',[E02/'E02_06_Gap_Conditioned_Performance.csv',E02/'E02_07_Coverage_Gap_Volatility.csv'])
est=pd.read_csv(E03/'E03_04_Weighting_Estimands.csv');boot=pd.read_csv(E03/'E03_08_Holm_Adjusted_Comparisons.csv');fig,axes=plt.subplots(1,3,figsize=(13,4.7));weights=['Fold-macro','Sample-weighted','Day-macro','Day-spatial-block']
for H,ax in zip(HS,axes):
 x=est[(est.horizon==H)&(est.model=='XGBoost')&(est.method=='A_ENSEMBLE_PREDICTION')].set_index('estimand').reindex(weights);ax.scatter(x.delta_XGBoost_minus_SeasonalHA,range(4),color='#1565C0',s=35)
 b=boot[(boot.horizon==H)&(boot.comparison=='XGBoost_vs_SeasonalHA')].iloc[0];ax.plot([b.CI_low,b.CI_high],[2,2],color='#1565C0',lw=2);ax.axvline(0,color='#777777',ls='--',lw=.8);ax.set_yticks(range(4),weights);ax.set(title=f'H{H}; 41 valid dates',xlabel='XGB - SeasonalHA absolute loss (km/h)');ax.invert_yaxis()
done(fig,'G1_D05_Weighting_Effects','A ensemble: four estimands; interval ONLY for primary Day-macro (3-day MBB, unadjusted 95%)',[E03/'E03_04_Weighting_Estimands.csv',E03/'E03_08_Holm_Adjusted_Comparisons.csv'])
lf=pd.read_csv(E03/'E03_10_LOFO_Stability.csv');fig,axes=plt.subplots(1,3,figsize=(13,4.5));order=['NONE','1','2','3','4','5','6']
for H,ax in zip(HS,axes):
 for model in ['XGBoost','SeasonalHA','Persistence']:
  x=lf[(lf.horizon==H)&(lf.model==model)&(lf.method=='A_ENSEMBLE_PREDICTION')].copy();x['excluded_fold']=x.excluded_fold.astype(str);x=x.set_index('excluded_fold').reindex(order);ax.plot(range(7),x.MAE,marker='o',label=model,color=COLORS[model])
 ax.set_xticks(range(7),['All','-F1','-F2','-F3','-F4','-F5','-F6'],rotation=30);ax.set(title=f'H{H}',ylabel='Equal-fold MAE (km/h)',xlabel='Existing-fold exclusion; no retraining')
axes[0].legend(fontsize=8);done(fig,'G1_D06_LOFO','A ensemble descriptive stability: all six exclusions retained; retrospective evaluation',[E03/'E03_10_LOFO_Stability.csv'])
save(pd.DataFrame(sources),OUT/'Diagnostic_Source_Index.csv');jwrite(LOG/'plotting_environment.json',{'python':sys.version,'numpy':np.__version__,'matplotlib':matplotlib.__version__,'output_count':6,'output_paths':[s['figure'] for s in sources]});log('six aggregate diagnostic figures generated')
