# GATE-FCD Statistical Claim Audit

The final English document was scanned for `significant`, `superior`, `outperform`, `best`, `equivalent`, `universal`, `robust`, `evidence`, `supports`, `demonstrates`, and `proves`, followed by contextual review of every hit.

| Claim boundary | Finding | Status |
| --- | --- | --- |
| Descriptive ranking | XGBoost is described as having the lowest descriptive fold-macro mean MAE at H1, H3, and H6; the language does not convert this ordering into statistical superiority. | PASS |
| SeasonalHA comparison | SeasonalHA remains close, and the XGBoost differences are described as small and conditional. | PASS |
| Holm correction | The manuscript states that `0/15` prespecified comparisons reached significance after Holm adjustment. | PASS |
| XGBoost–SeasonalHA intervals | All three fold-level intervals are reported as crossing zero, with p = 0.5625, 0.8438, and 1.000. | PASS |
| Non-significance | Non-significance is not interpreted as model equivalence. | PASS |
| Universal winner | The document rejects a universal-winner claim and supports horizon- and reliability-conditioned selection. | PASS |
| Cluster bootstrap | The day×spatial-block cluster bootstrap remains supplementary uncertainty analysis and does not replace the fold-level primary inference. | PASS |
| Inferential unit | The rolling-origin fold (`n = 6` paired folds per horizon) remains the primary inferential unit; sample rows are not treated as independent replicates. | PASS |
| Evidence level | The evaluation remains retrospective rolling-origin; the Fold 6 historical-exposure limitation is explicit. | PASS |
| Claim verbs | Uses of “supports,” “suggests,” “indicates,” and “evidence” are scoped to observed associations or engineering interpretation. No prohibited proof or superiority language remains. | PASS |

## High-risk phrase scan

No occurrences were found for the prohibited phrases: `commercial FCD`, `ground truth speed`, `ground-truth traffic speed`, `independent blind test`, `independent test`, `blind final test`, `significantly superior`, `statistically superior`, `universally superior`, `proved`, `proves`, `best model`, or `outperformed all models`.

`STATISTICAL_CLAIM_AUDIT = PASS`
