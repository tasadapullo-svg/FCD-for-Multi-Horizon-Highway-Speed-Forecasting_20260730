# AJSE Phase 2A-1 formal results

The six-fold retrospective rolling-origin experiment is complete.

- Target: future-window mean speed.
- Horizons: H1, H3 and H6.
- History: strict causal contiguous 24-hour input.
- Models: HA, SeasonalHA, Persistence, Ridge, XGBoost and GRU.
- Formal runs: 180/180 completed; 0 failed.
- Full-sample leakage assertions: 20/20 passed.
- Future-information violations: 0.
- Target recalculation mismatches: 0.
- Common model sample-manifest checks: passed for all 18 fold × horizon cells.
- Result-level audit: `PASS_WITH_LIMITATIONS`.
- AJSE primary results ready: `YES`.

Interpretation boundary:

- Results are retrospective rolling-origin evidence, not an independent blind test.
- The final calendar week must not be described as blind.
- XGBoost had the lowest mean fold-level MAE at H1/H3/H6, but no prespecified comparison remained significant after fold-level pairing and Holm correction.
- CRG-TCN and the separate CRG-TCN paper are outside this result set.

Start with:

- `06_REPORTS/AJSE_PHASE2A_RESULT_LEVEL_FINAL_AUDIT_REPORT.md`
- `06_REPORTS/AJSE_PHASE2A_PAPER_RESULT_INTERPRETATION.md`
- `06_REPORTS/AJSE_PHASE2A_RESULT_MASTER.xlsx`
- `08_FINAL_AUDIT/PHASE2A_RESULT_LEVEL_AUDIT_STATUS.json`
- `07_HASHES/PHASE2A_RESULT_FILE_SHA256.csv`

The original pre-run placeholder README is retained under
`00_DEFINITION_FREEZE/README_PRE_RUN_STATUS_20260730.md`.
