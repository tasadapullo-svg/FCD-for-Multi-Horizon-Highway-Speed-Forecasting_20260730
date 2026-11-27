# Figure 6 数据复算与证明逻辑审计报告

生成时间：2026-08-06T16:06:55.873512+00:00

## 1. 最终判定

- **Figure 6(a)：PASS_WITH_LIMITATIONS，可用于正文。**
- **Figure 6(b)：性能与部署属性 PASS；运行时间定量可比性未通过。**
- **最终绘图方案：2 个子图。**
  - (a) fold-level primary inference + cluster supplementary forest plot
  - (b) objective horizon-oriented engineering selection matrix
- **无需重新训练。**
- **不得使用 quantitative performance–runtime scatter，除非后续补齐统一 timer scope、per-run device/thread、硬件一致性和并发干扰审计。**

## 2. 独立复算结果

- 18 个 model×horizon 六折均值：最大绝对差 `0.000e+00`
- 18 个 fold SD：最大绝对差 `0.000e+00`
- 15 个配对平均差：最大绝对差 `1.110e-16`
- 15 个 exact Wilcoxon p：最大绝对差 `0.000e+00`
- 每个 horizon 内 Holm 校正：最大绝对差 `0.000e+00`
- Holm 校正后显著比较：`0/15`
- 测试样本：H1 `38,201`，H3 `24,805`，H6 `29,141`，合计 `92,147`
- 正式运行：`180/180` 完成，失败 `0`
- 全样本泄漏断言：`20/20` 通过，检查 `1,053,618` 条 sample-manifest 记录

## 3. Figure 6(a) 证明逻辑

差值统一定义为 `MAE_A − MAE_B`，负值有利于模型 A。主推断单位为 rolling-origin fold（n=6），每个 horizon 内进行 5 项预设比较和 Holm 校正。cluster bootstrap 使用 41 天、205 个 date-block 单元和 10,000 次重采样，仅作为补充推断。

XGBoost 相对 SeasonalHA 的 cluster 结果为：

- H1: +0.0684，95% CI [-0.1510, 0.3762]
- H3: +0.0252，95% CI [-0.1116, 0.1891]
- H6: +0.0226，95% CI [-0.0945, 0.2110]

三个区间均跨 0。该结果与等折宏平均中 XGBoost 略低的 MAE 不冲突，因为两者对应不同加权 estimand。允许结论是“差异小且方向对加权口径敏感”，禁止解释为完全等效。

## 4. Figure 6(b) 决策逻辑

- H1：XGBoost 0.949、Persistence 0.950、SeasonalHA 0.961 km/h。Persistence 是低维护候选，但不能写成强制唯一选择。
- H3：XGBoost 0.829、SeasonalHA 0.853 km/h。分别作为精度导向和透明性导向候选。
- H6：XGBoost 0.752、SeasonalHA 0.774 km/h。两者仍是主要候选，差异未形成确认性统计优势。
- GRU 未显示与序列训练、early stopping 和 checkpoint 维护相匹配的误差收益。
- elapsed_seconds 虽存在，但 timer scope、per-run device/thread 和并发干扰控制未完整记录，因此不能转化为通用计算成本倍数。

## 5. 结论边界

可以证明：描述性排名、统计不确定性、时距依赖的工程选模逻辑和运行登记完整性。

不能证明：XGBoost 普遍显著最优、XGBoost 与 SeasonalHA 完全等效、recorded elapsed 等同部署总成本、在线部署成功、独立 blind test、跨走廊泛化或商业 FCD 等同地面真值。
