# 论文主张边界

## 可以写

- XGBoost呈现三个horizon最低的fold平均MAE。
- SeasonalHA与XGBoost的误差接近，并具有较低的fold间波动。
- Persistence在H1具有竞争力，但在较长未来窗口中退化。
- 六折回顾性rolling-origin协议下，所有模型使用共同sample manifest。
- 全样本时间和泄漏断言均通过。
- 结果支持稀疏商业FCD在当前走廊和协议下的预测可行性。

## 必须谨慎写

- “better”应说明是描述性平均值，不是统计确认。
- “stable”应配合fold SD、worst fold或win count。
- “multi-horizon”必须说明是future-window average targets。
- “data-scarce”必须由固定检测器不足、短历史或稀疏覆盖证据支撑。
- “reproducible”应由配置、manifest、hash和commit记录支撑。

## 禁止写

- XGBoost significantly outperformed all baselines.
- The final week was an independent blind test.
- The study provides external validation.
- The results prove transferability to other corridors.
- CRG-TCN was evaluated in the AJSE benchmark.
- H6 point forecasting was easier than H1.
- 1,053,618 independent traffic observations were tested.
- Sparse FCD can replace fixed traffic sensors.
