# 数据审核清单

## A. 原始数据与理论网格

- [ ] 数据时间范围与论文一致
- [ ] 冻结节点数量与论文一致
- [ ] 15分钟理论记录数可复算
- [ ] 小时理论记录数可复算
- [ ] 缺失时间槽没有被误当作不存在
- [ ] 重复记录处理规则固定
- [ ] 时区和夏令时规则明确

## B. 数据资格

- [ ] confidence主阈值固定
- [ ] 低confidence记录保留审计痕迹
- [ ] 速度有效范围有来源或合理说明
- [ ] provider status缺失策略明确
- [ ] 2/4小时聚合为主规则
- [ ] 3/4和4/4作为敏感性规则
- [ ] H1、H3、H6标签规则明确
- [ ] H6 5/6与6/6边界明确

## C. 时间因果性

- [ ] history_end < target_start
- [ ] 输入不含预测起点后的信息
- [ ] scaler仅由训练期拟合
- [ ] 训练中位数或回退统计量仅来自训练期
- [ ] 无backward fill
- [ ] 无中心滚动统计
- [ ] 无未来merge
- [ ] 最长horizon设置purge

## D. Manifest

- [ ] 18个fold×horizon manifest均存在
- [ ] sample_id唯一
- [ ] 6个模型使用共同样本集合
- [ ] 每个manifest行数可独立复算
- [ ] 每个manifest有SHA-256
- [ ] history和target边界可追溯

## E. 模型运行

- [ ] 180/180正式运行存在
- [ ] 失败数为0
- [ ] 模型和seed配置与冻结YAML一致
- [ ] 每个预测文件行数与manifest一致
- [ ] 预测文件不预存真实标签或误差列
- [ ] 预测值无NaN或Inf

## F. 指标与统计

- [ ] MAE独立复算一致
- [ ] RMSE独立复算一致
- [ ] sMAPE定义一致
- [ ] Bias采用prediction minus observation
- [ ] fold为主要独立统计单位
- [ ] Holm校正在每个horizon内执行
- [ ] 不显著没有被解释为等效
- [ ] cluster bootstrap只作为辅助证据
