# GATE-FCD Numerical Consistency Audit

All frozen values were checked against the Chinese meaning source, the original English file, the final English file, the tables, captions, and the supplied figures where applicable. English word numerals, date formatting, and superscript unit glyphs were normalized during comparison.

## Study design and data contract

| Item | Chinese | English | Status |
| --- | ---: | ---: | --- |
| Corridor length | approximately 130 km | approximately 130 km | PASS |
| Fixed virtual observation nodes | 51 (N001–N051) | 51 (N001–N051) | PASS |
| Observation period | 2025-12-08 to 2026-02-28 | 2025-12-08 to 2026-02-28 | PASS |
| Raw resolution | 15 min | 15 min | PASS |
| Theoretical node×15-min slots | 403,512 | 403,512 | PASS |
| Theoretical node×hour slots | 100,878 | 100,878 | PASS |
| Speed eligibility | 0 < speed ≤ 130 km h⁻¹ | 0 < speed ≤ 130 km h⁻¹ | PASS |
| Confidence eligibility | ≥ 0.80 | ≥ 0.80 | PASS |
| Travel-time eligibility | > 0 | > 0 | PASS |
| Hourly aggregation | 2-of-4 | 2-of-4 | PASS |
| Causal history | 24 h before forecast origin | 24 h before forecast origin | PASS |
| H1 target eligibility | 1/1 | 1/1 | PASS |
| H3 target eligibility | 3/3 | 3/3 | PASS |
| H6 target eligibility | ≥5/6 | ≥5/6 | PASS |

## Experimental scale and audit counts

| Item | Chinese | English | Status |
| --- | ---: | ---: | --- |
| Rolling-origin folds | 6 | 6 | PASS |
| Forecast horizons | 3 | 3 | PASS |
| Fold×horizon benchmark units | 18 | 18 | PASS |
| Common manifests | 18 | 18 | PASS |
| Formal runs | 180 | 180 | PASS |
| Completed / failed | 180/180 / 0 | 180/180 / 0 | PASS |
| HA / SeasonalHA / Persistence / Ridge runs | 18 each | 18 each | PASS |
| XGBoost / GRU runs | 54 each | 54 each | PASS |
| Total manifest records | 1,053,618 | 1,053,618 | PASS |
| Training records | 873,874 | 873,874 | PASS |
| Validation records | 87,597 | 87,597 | PASS |
| Test records | 92,147 | 92,147 | PASS |
| H1 / H3 / H6 test records | 38,201 / 24,805 / 29,141 | 38,201 / 24,805 / 29,141 | PASS |
| Leakage assertions | 20/20 PASS | 20/20 PASS | PASS |
| Future-information violations | 0 | 0 | PASS |
| Target recomputation mismatches | 0 | 0 | PASS |
| Cross-split target-window violations | 0 | 0 | PASS |

## Fold-macro MAE (mean ± SD, km h⁻¹)

| Model | Chinese H1 / H3 / H6 | English H1 / H3 / H6 | Status |
| --- | --- | --- | --- |
| XGBoost | 0.949 ± 0.258 / 0.829 ± 0.168 / 0.752 ± 0.142 | 0.949 ± 0.258 / 0.829 ± 0.168 / 0.752 ± 0.142 | PASS |
| SeasonalHA | 0.961 ± 0.115 / 0.853 ± 0.105 / 0.774 ± 0.102 | 0.961 ± 0.115 / 0.853 ± 0.105 / 0.774 ± 0.102 | PASS |
| Persistence | 0.950 ± 0.155 / 1.170 ± 0.136 / 1.470 ± 0.182 | 0.950 ± 0.155 / 1.170 ± 0.136 / 1.470 ± 0.182 | PASS |
| GRU | 1.151 ± 0.230 / 1.043 ± 0.195 / 0.958 ± 0.199 | 1.151 ± 0.230 / 1.043 ± 0.195 / 0.958 ± 0.199 | PASS |
| Ridge | 1.225 ± 0.267 / 1.131 ± 0.213 / 1.086 ± 0.277 | 1.225 ± 0.267 / 1.131 ± 0.213 / 1.086 ± 0.277 | PASS |
| HA | 1.825 ± 0.119 / 1.704 ± 0.136 / 1.505 ± 0.120 | 1.825 ± 0.119 / 1.704 ± 0.136 / 1.505 ± 0.120 | PASS |

## Statistical values

| Item | Chinese | English | Status |
| --- | --- | --- | --- |
| XGBoost − SeasonalHA ΔMAE, H1/H3/H6 | −0.0117 / −0.0235 / −0.0222 | −0.0117 / −0.0235 / −0.0222 | PASS |
| Fold-level 95% CI, H1 | [−0.1574, 0.1825] | [−0.1574, 0.1825] | PASS |
| Fold-level 95% CI, H3 | [−0.1210, 0.0800] | [−0.1210, 0.0800] | PASS |
| Fold-level 95% CI, H6 | [−0.0837, 0.0397] | [−0.0837, 0.0397] | PASS |
| Holm-adjusted p, H1/H3/H6 | 0.5625 / 0.8438 / 1.000 | 0.5625 / 0.8438 / 1.000 | PASS |
| Holm-significant comparisons | 0/15 | 0/15 | PASS |
| Cluster estimate, H1/H3/H6 | +0.068 / +0.025 / +0.023 | +0.068 / +0.025 / +0.023 | PASS |
| Cluster 95% interval, H1 | [−0.151, 0.376] | [−0.151, 0.376] | PASS |
| Cluster 95% interval, H3 | [−0.112, 0.189] | [−0.112, 0.189] | PASS |
| Cluster 95% interval, H6 | [−0.094, 0.211] | [−0.094, 0.211] | PASS |

## Availability and spacing values

| Item | Chinese | English | Status |
| --- | ---: | ---: | --- |
| Availability mean / min / max | 97.30% / 94.21% / 99.03% | 97.30% / 94.21% / 99.03% | PASS |
| Mean / median / IQR spacing | 2.60 / 2.81 / 2.34 km | 2.60 / 2.81 / 2.34 km | PASS |
| Maximum spacing | 4.35 km | 4.35 km | PASS |

## Automated comparison note

The final English document differs from the original English digit-token inventory only where three semantically identical phrases, “none of the 15,” were normalized to the frozen notation `0/15`. The Chinese–English automated scan also flagged 19 paragraph locations and one table cell because of English word numerals, English date order, or superscript unit formatting; manual normalized review confirmed no value change.

`NUMERICAL_CONSISTENCY = PASS`
