# AJSE Phase 2A-1 result-level final audit

## Verdict

**PASS_WITH_LIMITATIONS**

- Formal runs: 180/180; failed: 0
- Data/leakage assertions: PASS
- Future-information violations: 0
- Target recomputation mismatches: 0
- Common sample manifest: PASS
- Primary statistical unit: rolling-origin fold (n=6)
- Holm-significant prespecified comparisons: 0

## Interpretation boundary

These are the primary **retrospective six-fold rolling-origin** AJSE results. They are not an independent blind test. The final calendar week must not be described as blind because it was previously exposed in other development work. CRG-TCN and the separate CRG-TCN manuscript were excluded from this benchmark.

## Statistical correction

Sample-level paired tests are retained only as descriptive evidence because repeated node/hour observations are dependent. Primary inference uses six fold-level pairs, supplemented by day × spatial-block clustered bootstrap with 10,000 resamples and Holm correction within each horizon.

## Significant corrected comparisons

No prespecified comparison remained significant after fold-level pairing and Holm correction.

## Paper-use rule

Report effect sizes, fold variability and confidence intervals. Do not claim universal model superiority, independent blind validation, or transfer beyond the observed corridor.
