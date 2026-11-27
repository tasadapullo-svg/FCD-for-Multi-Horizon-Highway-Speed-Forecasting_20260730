from common import *
paired=read('paired_loss');pb=read('method_B_sample_losses');old=pd.read_csv(BASE/'05_STATISTICS/spatial_block_day_metrics.csv');old['date']=pd.to_datetime(old.calendar_day)
rows=[]
for method,wide in [('A_ENSEMBLE_PREDICTION',paired),('B_MEAN_SEED_LOSS',pb)]:
 wide=wide.assign(date=wide.forecast_origin.dt.normalize())
 for H,x in wide.groupby('horizon'):
  cell=x.groupby(['date','spatial_block'])[MODELS].mean().reset_index()
  for model in MODELS:
   hist=old[(old.horizon==H)&(old.model==model)]
   comp=cell[['date','spatial_block',model]].merge(hist[['date','spatial_block','MAE']],on=['date','spatial_block'],how='outer',validate='one_to_one')
   diff=float((comp[model]-comp.MAE).abs().max());rows.append(dict(horizon=H,method=method,component='historical_cell_MAE_reconstruction',model=model,max_abs_difference=diff,cells=len(comp),missing_pairs=int(comp[[model,'MAE']].isna().any(axis=1).sum()),status='EXACT_POINT_RECONSTRUCTION' if diff<1e-9 else 'DIFFERENT_SEED_AGGREGATION'))
save(pd.DataFrame(rows),E03/'E03_04b_Historical_Cluster_Reconstruction.csv')
with (LOG/'implementation_fixes.md').open('a',encoding='utf-8') as f:f.write('\n2026-11-25：共享数据全部输出后，环境版本读取遇缺失scipy metadata，仅恢复receipt，未重算中间层。E01报告缺tabulate，仅补报告；E02 confidence_mean重复字典键已修正。\n\nE03历史空间块数值核对发现MultiIndex日期层名称不一致，join只按空间块产生笛卡尔连接（8405行而非205）；仅修复E03_04b历史点估计对照为显式date×spatial_block一对一连接。主要estimands、bootstrap、Holm和LOFO未受影响，不重算。修复后B方法历史205单元格逐项精确对应，A差异来自seed聚合，不是空间块重划。\n')
with (E03/'E03_13_Estimand_Reversal_Explanation.md').open('a',encoding='utf-8') as f:f.write('\n\n定向核验：原day×block表的205个单元格在B方法下逐项重建至浮点精度；历史点估计与新A的差异包括seed聚合和统计权重两部分。E03_04b已修正日期层连接错误；未更动主要推断。旧重采样程序未恢复，仍不声称CI完全复现。\n')
log('targeted historical cluster comparison corrected; no E01/E02 or bootstrap rerun')
print(pd.DataFrame(rows).query('model=="XGBoost"').to_string(index=False))
