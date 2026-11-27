# 下一阶段审核工作流

## 阶段1：文件和版本审核

- 确认本地正式工程路径；
- 确认Git工作树为clean；
- 区分experiment commit、result-audit commit和release tag；
- 对照本包SHA-256清单；
- 检查正式配置、manifest和结果文件是否属于同一冻结版本。

## 阶段2：数据资格审核

- 完整15分钟理论网格；
- 完整小时理论网格；
- confidence阈值；
- 速度范围规则；
- 2/4主聚合规则；
- H1/H3/H6标签资格；
- 训练期专属回退统计量；
- 缺失和插补标识。

## 阶段3：样本和泄漏审核

- 18个fold×horizon manifest；
- sample ID唯一；
- 模型共同样本；
- history_end < target_start；
- 最长horizon purge；
- 禁止backward fill和中心滚动；
- target从源数据独立复算；
- 20项断言逐项留证。

## 阶段4：结果审核

- 180/180运行状态；
- 每个fold、horizon、model和seed的行数；
- MAE、RMSE、sMAPE、Bias复算；
- seed稳定性；
- fold均值、标准差和最差fold；
- SeasonalHA、Persistence与XGBoost的实际差值；
- Holm校正后的统计结论。

## 阶段5：论文补充分析

优先使用现有预测文件完成，不建议重新训练主模型：

- coverage分层；
- confidence分层；
- 连续缺失长度分层；
- 51节点误差；
- 工作日与周末；
- 低速和高波动状态；
- 2/4、3/4、4/4聚合敏感性；
- H6 5/6与6/6标签敏感性；
- 排除已暴露终端fold的敏感性；
- 共同forecast-origin跨horizon比较。

## 阶段6：论文回填和一致性审核

- Abstract只填写最终稳定数值；
- Methods中的规则与冻结YAML一致；
- Results中的样本数与工作簿一致；
- 图表数值可从CSV或工作簿复算；
- Discussion不将描述性排名写成显著优势；
- Limitations明确回顾性评价和单走廊边界；
- Conclusion不引入正文未展示的新结论。
