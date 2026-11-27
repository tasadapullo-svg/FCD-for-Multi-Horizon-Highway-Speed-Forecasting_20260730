# 论文数据检查清单

## Title与Abstract

- [ ] 标题没有XGBoost superiority导向
- [ ] 使用retrospective rolling-origin
- [ ] Abstract声明6 folds和3 future-window horizons
- [ ] Abstract说明XGBoost最低平均MAE但无Holm显著结果
- [ ] Abstract没有blind或external validation

## Methods

- [ ] H1/H3/H6定义为未来窗口平均速度
- [ ] 24小时历史窗口明确
- [ ] 数据资格规则与冻结YAML一致
- [ ] 共同manifest和20项泄漏断言明确
- [ ] 6个正式模型名称完整
- [ ] CRG-TCN未被写入本次模型集
- [ ] fold-level为主要推断单位

## Results

- [ ] 180/180和0失败有证据
- [ ] 1,053,618写成fold-specific audited sample records
- [ ] 报告每个horizon的实际样本数
- [ ] MAE、RMSE、sMAPE和Bias与工作簿一致
- [ ] SeasonalHA稳定性被报告
- [ ] Persistence在H1的竞争力被报告
- [ ] H6较低MAE没有被解释为更容易的远期点预测
- [ ] Holm显著比较为0
- [ ] 展示fold级变化而非只展示总体均值

## Discussion

- [ ] 重点讨论评价协议和数据证据
- [ ] 不把模型排名写成普遍优越性
- [ ] 解释短历史下简单季节性基线为何强
- [ ] 解释XGBoost RMSE和Bias的权衡
- [ ] 讨论n=6导致统计功效有限
- [ ] 讨论单走廊、约三个月和商业平台偏差
- [ ] 讨论无固定检测器ground truth

## Conclusion

- [ ] 结论只概括正文展示过的结果
- [ ] 使用can support under the evaluated protocol等边界表达
- [ ] 不写replace fixed sensors
- [ ] 不写generalize to all corridors
- [ ] 不写significantly outperformed all baselines
