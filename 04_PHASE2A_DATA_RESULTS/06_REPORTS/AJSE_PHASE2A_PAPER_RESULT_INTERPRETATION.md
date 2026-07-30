# AJSE Phase 2A-1 paper-result interpretation

## Result status

The formal six-fold rolling-origin campaign is complete (180/180 runs; zero failures). These are retrospective primary results, not an independent blind test.

## Descriptive model performance

- H1: XGBoost, MAE 0.949 ± 0.258 km/h across folds.
- H3: XGBoost, MAE 0.829 ± 0.168 km/h across folds.
- H6: XGBoost, MAE 0.752 ± 0.142 km/h across folds.

XGBoost had the lowest mean fold-level MAE at all three horizons. SeasonalHA was close to XGBoost at all horizons, and Persistence was competitive at H1 but degraded as the future window length increased.

## Corrected inference

The primary independent unit was the rolling-origin fold (n=6). Five prespecified comparisons were tested separately within H1, H3 and H6 using paired fold differences, 10,000 bootstrap resamples, and Holm correction within each horizon. No comparison retained adjusted p < 0.05. Therefore, observed performance differences are descriptive/limited evidence and must not be written as statistically significant superiority.

## Manuscript-ready wording

> Across six retrospective rolling-origin folds, XGBoost achieved the lowest mean MAE at H1, H3 and H6, while a seasonal historical-average baseline remained close at each horizon. Because the primary paired unit was the rolling-origin fold (n=6), none of the prespecified pairwise differences remained significant after Holm correction. We therefore interpret the ranking as descriptive evidence of temporal stability rather than confirmatory proof of universal model superiority.

## Prohibited wording

- “XGBoost significantly outperformed all baselines.”
- “The final week was an independent blind test.”
- “The results prove transferability beyond this corridor.”
- Any claim that CRG-TCN was evaluated in this AJSE Phase 2A-1 benchmark.

## Sources

- `D:\2026_AJSE_FINAL\04_PHASE2A_DATA_RESULTS\04_METRICS\model_horizon_summary.csv`; SHA-256 `c0d52d55f3ba67764292e2cf9bb88280d6d18c9fef762f45c3b95945423d247d`
- `D:\2026_AJSE_FINAL\04_PHASE2A_DATA_RESULTS\05_STATISTICS\corrected_fold_pairwise_tests_holm.csv`; SHA-256 `4b5373b1c68a7c8a666a0fef637d747bb0eaf220b0626ea337daa5d3900a47a8`

## Figure-render note

Standalone PNG rendering was not used because the archived Python environment has an unstable Matplotlib DLL. The audited Excel workbook contains the presentation layer, while all chart-ready source tables are preserved as CSV.
