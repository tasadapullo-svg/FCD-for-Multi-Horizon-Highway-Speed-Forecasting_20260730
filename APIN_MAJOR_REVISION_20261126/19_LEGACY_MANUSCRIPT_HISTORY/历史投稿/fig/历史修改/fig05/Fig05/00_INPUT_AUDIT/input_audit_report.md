# Figure 5 input audit

- Mandatory 10-file size/hash audit: **PASS**
- Formal manifest registry audit (18 files): **PASS**
- Formal input root used: `E:\20260730_AJSE_FINAL_bak\04_PHASE2A_DATA_RESULTS`
- Output root: `D:\2026_AJSE_FINAL\Fig05_DERIVATION_20260807`
- Model retraining: **NO**
- Formal result modification: **NO**

## Documented source correction

The hash-matched `05_STATISTICS/forecast_origin_metrics.csv` contains 16,566 aggregated model-origin rows and does not contain sample IDs or reliability variables. Unique origin reliability records are therefore derived from the hash-registered Phase 2A-1 test sample manifests under `01_DATA_PIPELINE/folds`. This is recorded explicitly rather than silently remapping the aggregated file.

## Environment limitation

Python 3.10 is not installed on this workstation. The derivation uses the existing Python 3.14.3 runtime. This affects environment conformity, not the frozen inputs or statistical definitions.
