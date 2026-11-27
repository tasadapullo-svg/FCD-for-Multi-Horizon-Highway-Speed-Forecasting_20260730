from common import *
d=pd.read_csv(E03/'E03_05_Daily_Paired_Loss.csv');x=d[(d.model_a=='XGBoost')&(d.model_b=='SeasonalHA')].copy();x['LOW_SUPPORT_DATE']=(x.n<30)|(x.nodes<3)
save(x,E03/'E03_05b_Daily_Support_Diagnostics.csv')
print(x.groupby('horizon').agg(days=('date','size'),min_n=('n','min'),max_n=('n','max'),low_support_days=('LOW_SUPPORT_DATE','sum')).to_string())
print(x.sort_values('n').head(6).to_string(index=False))
line=pd.read_csv(E01/'E01_01_Data_Lineage_and_Coverage.csv').set_index('metric')
report=G1/'G1_06_Acceptance_Report_CN.md';text=report.read_text(encoding='utf-8');text=text.replace('60.160995%',f"{line.loc['unique_returned_slots','ratio']*100:.6f}%").replace('59.874552%',f"{line.loc['quality_dedup_in_grid','ratio']*100:.6f}%")
notes=[]
for H,z in x.groupby('horizon'):notes.append(f'H{H}每天样本数范围{z.n.min()}–{z.n.max()}，LOW_SUPPORT_DATE数量{int(z.LOW_SUPPORT_DATE.sum())}。')
note='\n\n补充日期支持解释：'+''.join(notes)+' Day-macro给每个有效日期等权，低观测日期不会按样本量自动降权；这会放大少数低支持日期影响，属于预先选定估计对象的实际限制。未据测试误差删除日期或改变主要统计方案，须与Sample-weighted及7日块敏感性共同阅读。证据：`'+str(E03/'E03_05b_Daily_Support_Diagnostics.csv')+'`。\n'
text=text.replace('## 审稿证据、未解决问题与下一阶段范围',note+'\n## 审稿证据、未解决问题与下一阶段范围');report.write_text(text,encoding='utf-8')
with (E03/'E03_13_Estimand_Reversal_Explanation.md').open('a',encoding='utf-8') as f:f.write(note)
log('added actual daily support limitation; primary stats unchanged')
