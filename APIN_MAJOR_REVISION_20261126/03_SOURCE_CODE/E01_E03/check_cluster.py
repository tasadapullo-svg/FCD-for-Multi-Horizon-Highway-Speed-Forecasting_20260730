from common import *
p=read('paired_loss');m=read('target_completeness_and_reliability');old=pd.read_csv(BASE/'05_STATISTICS/spatial_block_day_metrics.csv');print('MANIFEST spatial',m.groupby('spatial_block').node_order.agg(['min','max']).to_string());print('old blocks',old.spatial_block.unique());print(pd.read_csv(E03/'E03_04b_Historical_Cluster_Reconstruction.csv').head().to_string(index=False))
p['calendar_day']=p.forecast_origin.dt.strftime('%Y-%m-%d');pb=read('method_B_sample_losses');pb['calendar_day']=pb.forecast_origin.dt.strftime('%Y-%m-%d')
for H in HS:
 x=pb[pb.horizon==H].groupby(['calendar_day','spatial_block'])[MODELS].mean().reset_index();z=old[(old.horizon==H)&(old.model=='XGBoost')]
 print('keys',H,x.spatial_block.unique(),z.spatial_block.unique())
 a=x.merge(z,on=['calendar_day','spatial_block']);print('max direct', (a.XGBoost-a.MAE).abs().max(),'mean direct', (a.XGBoost-a.MAE).mean())
 for shift in [-1,1]:
  shifted=x.assign(spatial_block=x.spatial_block+shift).merge(z,on=['calendar_day','spatial_block']);print('shift',shift,'matches',len(shifted),'maxdiff', (shifted.XGBoost-shifted.MAE).abs().max())
 print('means',x.XGBoost.mean(),z.MAE.mean())
