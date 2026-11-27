# GATE-FCD Statistical Claim Audit

| Claim boundary | Final finding | Status |
| --- | --- | --- |
| Descriptive ranking | XGBoost is described as having the lowest descriptive fold-macro mean MAE at all three horizons. | PASS |
| SeasonalHA comparison | SeasonalHA remains close; differences are small and conditional. | PASS |
| Holm correction | The manuscript retains `0/15` significant comparisons after Holm adjustment. | PASS |
| Confidence intervals | All three XGBoost–SeasonalHA fold-level intervals cross zero. | PASS |
| Non-significance | Non-significance is not interpreted as complete equivalence. | PASS |
| Universal winner | The text rejects a universal-winner claim. | PASS |
| Cluster bootstrap | The cluster bootstrap remains supplementary uncertainty analysis. | PASS |
| Inferential unit | The rolling-origin fold (`n = 6`) remains the primary paired unit. | PASS |
| Evidence level | Evaluation remains retrospective; Fold 6 historical exposure is explicit. | PASS |
| Target semantics | Results concern FCD-reported speed, not independent ground-truth speed. | PASS |

No hits were found for the high-risk phrases `significantly superior`, `statistically superior`, `universally superior`, `best model`, `outperformed all models`, `independent blind test`, `blind final test`, `proves that`, or `proved that`.

`STATISTICAL_CLAIM_AUDIT = PASS`

