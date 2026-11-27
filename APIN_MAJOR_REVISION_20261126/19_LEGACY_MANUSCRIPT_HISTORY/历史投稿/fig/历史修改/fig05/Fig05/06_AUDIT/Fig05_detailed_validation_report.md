# Figure 5 detailed validation report

## Final status

**PASS_WITH_LIMITATIONS**

## Core results

- Formal 10-file hash audit: PASS
- Formal manifest hash registry audit: PASS
- Unique test origins: 92,147
- Six-model sample rows: 552,882
- Joined rows: 552,882
- Figure 4 MAE reproduction maximum mismatch: 2.220e-16
- Node-fold cube rows: 5,508
- Node-risk rows: 918
- Valid reliability variables: history_coverage_ratio, history_imputation_ratio
- Reliability variables blocked by tied quartile cutpoints: max_gap_24h, hours_since_last_observation

## Source lineage correction

The hash-matched `forecast_origin_metrics.csv` is an aggregated metrics table (16,566 rows), not a 92,147-row reliability table. Reliability variables were recovered from hash-registered formal Phase 2A-1 test manifests. `hours_since_last_observation` was reconstructed from the aligned formal sequence tensor using fold-train scaler parameters; coverage, imputation and gap values reconstructed from the same tensor were compared with their manifest columns to verify alignment.

## Node sequence and distance limitation

The requested external audit package was not found. `node_order_verified` therefore uses the invariant `node_order` stored in all formal test manifests. `corridor_km` remains missing: no straight-line/geodesic substitute was used. Figure 5(c) uses manifest node order until the verified approximately 95.69 km mapping is supplied.

## Stable high-risk limitation

No frozen minimum sample-size threshold was found. `stable_high_risk` remains NA and `stable_high_risk_status` is `USER_APPROVAL_REQUIRED`. `top_quartile_fold_count` is retained without adding stars to the figures.

## Seed-averaged error semantics

For XGBoost and GRU, the stored formal `absolute_error` is mean absolute error across seeds, while `y_pred` is a seed-mean prediction. The formal error is preserved as `mean(abs(prediction_seed-truth))`; it is not replaced with `abs(mean(prediction_seed)-truth)`. Figure 4 MAE values reproduce within the frozen tolerance.

## Environment limitation

Python 3.10 was unavailable; Python 3.14.3 was used. No model training, prediction regeneration, seed reselection, or formal-source write occurred.
