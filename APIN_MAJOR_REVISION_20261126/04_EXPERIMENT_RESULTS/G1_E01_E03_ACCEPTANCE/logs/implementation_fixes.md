# 本阶段程序错误与定向修正

2026-11-25 prepare_shared首次运行：Pandas GroupBy的observed属性与同名列冲突，报AttributeError。在尚未读取新预测误差前，将列访问改为显式['observed']。分析协议、阈值、统计方案均未变；部分中间文件尚无完成receipt，不视为已验收结果。原始来源未改动。

2026-11-25：共享数据全部输出后，环境版本读取遇缺失scipy metadata，仅恢复receipt，未重算中间层。E01报告缺tabulate，仅补报告；E02 confidence_mean重复字典键已修正。

E03历史空间块数值核对发现MultiIndex日期层名称不一致，join只按空间块产生笛卡尔连接（8405行而非205）；仅修复E03_04b历史点估计对照为显式date×spatial_block一对一连接。主要estimands、bootstrap、Holm和LOFO未受影响，不重算。修复后B方法历史205单元格逐项精确对应，A差异来自seed聚合，不是空间块重划。

G1验收p值下界检查：CSV12有效位存储的0.000099990001较精确1/10001低约3e-17，导致机械下界误报。仅将验收数值序列化容差设为5e-13，定向复核该项；保存原验收记录，不更改p值/CI/协议或重跑分析。
