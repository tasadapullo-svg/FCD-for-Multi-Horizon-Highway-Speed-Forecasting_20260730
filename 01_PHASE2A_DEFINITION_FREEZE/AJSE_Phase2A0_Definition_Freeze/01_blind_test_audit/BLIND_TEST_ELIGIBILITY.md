# Blind-test eligibility

## Status: C. CONTAMINATED_TEST

The current v2 repository has no P7 result directory, P7 log, P7 manifest, final-week prediction export, or locked-truth output. Its `data/blind` and `data/locked_truth` folders contain no final-week data artifact.

However, the candidate final week (2026-02-22T00:00:00 through 2026-02-28T23:00:00) is fully contained in the legacy Phase13/15/16 test period. Timestamp-only inspection—without reading any prediction or error values—found:

- Phase13: 105 prediction files, 105 overlapping the candidate week.
- Phase15: 75 prediction files, 75 overlapping the candidate week.
- Legacy feature-ablation, robustness, regime, history-sensitivity, and model-comparison artifacts use the same historical test manifest or predictions.

Those experiments and their interpretation expose the same calendar outcomes and have already informed model/task understanding. Therefore the week cannot be presented as a new independent blind test. The old test period is frozen as **historical development/comparison period**.

No final-week MAE, RMSE, sMAPE, prediction values, target values, or error values were read or calculated in this Phase 2A-0 audit.

Required path forward: collect a new independent time period, or use a transparently retrospective rolling-origin evaluation. Phase 2A-1 confirmatory test design is stopped.
