# Ridge 数值稳定性定向结论

**状态：CLOSED_WITH_LIMITATION；最终写作采用本目录 SVD 修正汇总，原 G2 651 次运行与成果包保留为冻结来源。**

在查看对照前，`00_PROJECT_CONTROL/FINAL_Closure_Protocol.json` 冻结逐预测最大差 `1e-4 km/h`、MAE 最大差 `1e-5 km/h`。唯一改动是 Ridge 求解器由 `cholesky` 改为 `svd`；训练/验证/测试样本、manifest SHA-256、特征、目标、α、`fit_intercept` 均逐 Run ID 保持一致。未重训 XGBoost、GRU 或 G1 原始模型，也未覆盖原权重及预测。

日志在 93 个 Ridge Run ID 中定位到 78 个具有病态矩阵警告，所有警告均映射到有效 Run ID；最小记录 `rcond=1.21537e-9`。首批 15 个代表性对照发现 α≥1 超过预设容差，因此将定向检查扩大到全部既有 93 个 Ridge 配置（90 个 α≥1、3 个 α=0.1 的 Fold1 候选），共新增 **93 次 SVD 诊断拟合**，未超过原有 Ridge 范围。三个 α=0.1 候选在容差内。

90 个含测试结果的 Ridge 运行中，89 个超出逐预测容差，87 个超出 MAE 容差；最大逐样本测试预测差 `0.693176 km/h`，最大测试 MAE 绝对差 `0.001462 km/h`，18 个运行的测试 MAE 三位小数发生变化。三个时距的 Fold1 验证集最优 α 均仍为 10；在 90 个匹配的 XGBoost–Ridge 单 fold 排序对照中，优胜方向改变 0 次。原 G1 显著性检验使用冻结原始预测，G2 四项预设关键检验不含 Ridge，二者无需重算。

这不是“数值完全一致”。后续论文数字应引用 `Ridge_Corrected_Experiment_Metrics.csv` 与 `Ridge_Corrected_Aggregates.csv` 的 SVD 列，并在方法中说明独立新实现的求解器修正；原 G2 注册表、ZIP 和 Cholesky 数值用于变更追踪。`Ridge_Numerical_Stability_Check.csv` 保存逐运行验证/测试 MAE、RMSE、Bias、预测差及三位小数变化。当前修正未改变 Fold1 超参数选择或已检查的 XGBoost–Ridge fold 优胜方向，但不等于证明所有可能的排名口径均稳定。
