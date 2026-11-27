# GATE-FCD Numerical Consistency Audit

The final DOCX was compared with `Humanizer_english.docx` after excluding only the new Abstract, Keywords, and Data and Code Availability paragraphs. The comparison found `0` numeric-token mismatches and `0` citation-token mismatches across all 202 aligned source paragraphs.

## Study design and data contract

| Item | Locked value | Status |
| --- | ---: | --- |
| Corridor length | approximately 130 km | PASS |
| Fixed virtual nodes | 51 (N001–N051) | PASS |
| Observation period | 2025-12-08 to 2026-02-28 | PASS |
| Raw resolution | 15 min | PASS |
| Theoretical node×15-min slots | 403,512 | PASS |
| Theoretical node×hour slots | 100,878 | PASS |
| Speed eligibility | 0 < speed ≤ 130 km h⁻¹ | PASS |
| Confidence eligibility | ≥ 0.80 | PASS |
| Hourly aggregation | 2-of-4 | PASS |
| Causal history | 24 h | PASS |
| H1 / H3 / H6 eligibility | 1/1 / 3/3 / at least 5/6 | PASS |

## Experimental scale and audit counts

| Item | Locked value | Status |
| --- | ---: | --- |
| Rolling-origin folds | 6 | PASS |
| Fold×horizon benchmark units | 18 | PASS |
| Formal runs | 180/180 completed; 0 failed | PASS |
| Total manifest records | 1,053,618 | PASS |
| Training / validation / test | 873,874 / 87,597 / 92,147 | PASS |
| H1 / H3 / H6 test records | 38,201 / 24,805 / 29,141 | PASS |
| Leakage assertions | 20/20 PASS | PASS |
| Future-information violations | 0 | PASS |
| Target recomputation mismatches | 0 | PASS |
| Cross-split target-window violations | 0 | PASS |

## Fold-macro MAE (mean ± SD, km h⁻¹)

| Model | H1 | H3 | H6 |
| --- | ---: | ---: | ---: |
| XGBoost | 0.949 ± 0.258 | 0.829 ± 0.168 | 0.752 ± 0.142 |
| SeasonalHA | 0.961 ± 0.115 | 0.853 ± 0.105 | 0.774 ± 0.102 |
| Persistence | 0.950 ± 0.155 | 1.170 ± 0.136 | 1.470 ± 0.182 |
| GRU | 1.151 ± 0.230 | 1.043 ± 0.195 | 0.958 ± 0.199 |
| Ridge | 1.225 ± 0.267 | 1.131 ± 0.213 | 1.086 ± 0.277 |
| HA | 1.825 ± 0.119 | 1.704 ± 0.136 | 1.505 ± 0.120 |

## Statistical values

| Item | H1 / H3 / H6 | Status |
| --- | --- | --- |
| XGBoost − SeasonalHA ΔMAE | −0.0117 / −0.0235 / −0.0222 | PASS |
| Holm-adjusted p | 0.5625 / 0.8438 / 1.000 | PASS |
| Holm-significant comparisons | 0/15 | PASS |
| Cluster estimates | +0.068 / +0.025 / +0.023 | PASS |

`NUMERICAL_CONSISTENCY = PASS`

