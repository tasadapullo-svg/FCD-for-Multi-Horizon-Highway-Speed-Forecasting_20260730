# AJSE comprehensive data and result audit — start here

Generated: 2026-07-30T10:29:29.074187+08:00

## Primary deliverables

- `06_REPORTS/AJSE_COMPREHENSIVE_DATA_AND_RESULT_AUDIT_REPORT.md` — detailed scientific verdict and deviations.
- `AJSE_DATA_RESULT_AUDIT_MASTER.xlsx` — 16-sheet review workbook.
- `02_EXPERIMENT_RESULT_CROSSWALK/outline_experiment_result_crosswalk.csv` — A0–A13 status map.
- `04_METRIC_RECALCULATION/phase13_prediction_metric_recalculation.csv` — all 105 archived Phase13 prediction files independently recomputed.
- `04_METRIC_RECALCULATION/target_recalculation_summary.csv` — full target verification for H1/H3/H6.
- `05_BIAS_AND_DEVIATIONS/bias_and_deviation_register.csv` — critical/high/medium/low bias register.
- `07_HASHES/evidence_file_hashes_sha256.csv` — source evidence hash registry.
- `10_FINAL_VALIDATION/FINAL_AUDIT_VALIDATION.json` — machine-readable delivery validation.

## Short verdict

The legacy Phase13 result set is internally consistent, uses future-window mean targets, has common samples within each horizon, and reproduces all stored metrics. It is not the completed AJSE Phase2A result set because it uses a single 70/15/15 split, its H6 set contains 51 boundary samples per file beyond the canonical complete-hour grid, and it lacks six-fold rolling-origin evaluation. The v2.2 P6–P8 chain uses a point target and is limited to contaminated retrospective supplementary evidence.

## Integrity

No original experiment output was modified. Selected small evidence files were copied with source/destination hashes. Raw commercial FCD, full prediction arrays, model weights and environment caches are not included in this audit folder or ZIP.
