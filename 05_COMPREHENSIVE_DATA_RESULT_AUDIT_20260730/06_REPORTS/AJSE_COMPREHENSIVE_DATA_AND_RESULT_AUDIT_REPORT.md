# AJSE complete data/result aggregation and correspondence audit

Generated: 2026-07-30T10:19:20.215605+08:00

## 1. Executive verdict

`AJSE_DATA_RESULT_STATUS = PRIMARY_RESULTS_NOT_READY`

**Overall status: NOT READY AS A COMPLETED PHASE 2A PAPER RESULT SET.**

The D-drive search found useful and internally checkable legacy evidence, but it did **not** find a completed six-fold rolling-origin experiment matching the supplied AJSE outline. The strongest reusable result set is `D:\2026_PD\outputs\locked\phase13_full`: it uses the correct future-window-mean target and H1/H3/H6, contains 105 prediction files, and its metrics and common-sample structure were independently checked. Its decisive limitation is that it uses one chronological 70/15/15 split rather than the six frozen rolling origins required by the manuscript.

The v2.2 P6–P8 chain is a different task (point speed at t+H) and an exposed retrospective period. It must remain outside the primary future-window-mean tables.

## 2. Supplied manuscript outline identity

- Source: `C:\Users\DELL\Desktop\AJSE_Phase2A_详细写作大纲_逻辑关键词实验详解版.docx`
- SHA-256: `264699f1962b0060edcdc41c3812c59955030ae44c75240ca27b956468ac6e88`
- Structural extraction: `D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730\00_SOURCE_OUTLINE\outline_extracted.md`
- Visual-render limitation: LibreOffice/soffice was not available, so the DOCX was structurally parsed but not page-rendered for visual QA.

The outline requires A0–A13, a future-window-mean target for H1/H3/H6, strict causal processing, common samples, six-fold rolling-origin evaluation, dependence-aware inference, and retrospective-only wording for the exposed final week.

## 3. D-drive discovery scope

The audit enumerated the complete top level of D: and recursively inventoried the research-relevant roots `D:\2026_PD`, `D:\2026_07_23`, `D:\CRG_TCN_20260729`, `D:\2026_AJSE_FINAL`, `D:\2026_AJSE_FINAL_QUARANTINE`, `D:\2026_T2_ENV`, `D:\Traffic4cast_Bangkok_Access_Check`, and `D:\data`. Python environments, package caches, `.git`, `node_modules`, and system directories were excluded from detailed content scanning and are explicitly outside the scientific-result search.

Research-family counts are in `D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730\01_D_DRIVE_INVENTORY\research_family_summary.csv`. The full research asset list is `D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730\01_D_DRIVE_INVENTORY\research_asset_inventory.csv`.

## 4. A0–A13 correspondence

Status distribution: `{"PARTIAL_PASS": 3, "NOT_EXECUTED": 3, "PARTIAL_OLD_SPLIT": 2, "DEFINITION_FROZEN_NOT_EXECUTED": 1, "PARTIAL_PASS_WITH_BOUNDARY_MISMATCH": 1, "NOT_EXECUTED_FOR_SIX_FOLD": 1, "NONCOMPLIANT_OLD_ANALYSIS": 1, "AVAILABLE_WITH_CONTAMINATION": 1, "PARTIAL": 1}`.

Key conclusions:

- A0/A1/A4/A6 have partial or definition-level evidence.
- A3 has no completed matching sensitivity result.
- A5/A7/A8 are not completed for six-fold rolling-origin evaluation.
- A9/A10 exist only on the old single split.
- A11 is not compliant because original inference pooled repeated sample-level errors.
- A12 is available only as contaminated retrospective point-target evidence.
- A13 cannot be called complete until the missing Phase2A experiment/statistics are produced.

The item-by-item mapping is `D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730\02_EXPERIMENT_RESULT_CROSSWALK\outline_experiment_result_crosswalk.csv`.

## 5. Data correspondence and correctness

### 5.1 Legacy PD panel

- Rows: 100,980; nodes: 51.
- Range: 2025-12-08 13:00:00 to 2026-03-01 00:00:00.
- Duplicate node-hour keys: 0.
- Missing target rows: 3,886.
- Complete-hour Phase2A range rows: 100,878 (expected 100,878).
- Extra boundary rows in the legacy panel: 102 at ['2025-12-08 13:00:00', '2026-03-01 00:00:00'].

This 102-row discrepancy is not random corruption; it is a time-grid definition difference (two partial boundary hours × 51 nodes). Counts and availability rates must use one denominator consistently.

### 5.2 Target and windows

The Phase13 code explicitly sets `truth = mean(target_start_time ... target_end_time)`. The current audit independently recomputed every reference prediction target from the hourly panel:

- H1: 12265/12265 matched, mismatches=0, max difference=2.543131529364473e-06.
- H3: 11878/11878 matched, mismatches=0, max difference=3.390842024941776e-06.
- H6: 12166/12166 matched, mismatches=0, max difference=3.5603841155307236e-06.

Thus the archived Phase13 target corresponds to **future-window mean speed**, not point speed. The old windows use history=24 h, input observed ratio ≥0.80 and target observed ratio ≥0.80. For H6 this means at least five observed future hours; for H1/H3 it effectively requires all target hours.

**Canonical-boundary warning:** every H6 prediction file contains 51 samples whose target window ends at `2026-03-01 00:00`, while the Phase2A complete-hour grid ends at `2026-02-28 23:00`. The file `phase13_complete_hour_boundary_sensitivity.csv` recomputes all metrics after excluding those samples. Therefore H6 is target-semantics compatible but not an exact canonical sample-set match.

No leakage-check failure was found in the relevant old windows, but that check only proves ordering and same-split containment under the old single split. It does not prove six-fold rolling-origin execution.

## 6. Prediction and metric audit

- Stored metric rows: 105.
- Expected/audited prediction files: 105/105.
- Metric mismatch files at tolerance 1e-5: 0.
- Models: GRU, HA, Persistence, ST-Transformer-lite, SeasonalHA, TCN, XGBoost.
- Horizons: [1, 3, 6]; seeds: [42, 2024, 2025, 2026, 3407].
- Common sample and truth hashes by horizon are recorded in `D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730\04_METRIC_RECALCULATION\phase13_common_sample_truth_check.csv`.

Legacy mean-MAE winners:

- H1: XGBoost, mean MAE=0.973587
- H3: XGBoost, mean MAE=0.868904
- H6: XGBoost, mean MAE=0.786682

XGBoost is therefore the strongest archived trained model on the old split. TCN is not the top model, and CRG-TCN is absent from this 105-run result set.

## 7. Statistical dependence and bias

The original Phase14 tests pool approximately 59k–61k paired rows and report very small p-values. Those rows repeat nodes, hours, days and seeds. The current audit averaged seeds first and repeated comparisons at the calendar-day level with a 5,000-replicate paired day bootstrap and Holm correction. These are **diagnostic**, not a substitute for the missing six-fold analysis.

Day-level comparisons surviving Holm correction in the diagnostic:

- H1 TCN vs HA: n_days=11, difference(compared−TCN)=0.709526, 95% day-bootstrap CI [0.546486, 0.829907], Holm p=0.00585938.
- H3 TCN vs HA: n_days=11, difference(compared−TCN)=0.699105, 95% day-bootstrap CI [0.525905, 0.845506], Holm p=0.00585938.
- H3 TCN vs Persistence: n_days=11, difference(compared−TCN)=0.419115, 95% day-bootstrap CI [0.172055, 0.750141], Holm p=0.0244141.
- H3 TCN vs XGBoost: n_days=11, difference(compared−TCN)=-0.198030, 95% day-bootstrap CI [-0.348449, -0.090360], Holm p=0.0244141.
- H6 TCN vs HA: n_days=11, difference(compared−TCN)=0.607677, 95% day-bootstrap CI [0.489826, 0.727920], Holm p=0.00585938.
- H6 TCN vs Persistence: n_days=11, difference(compared−TCN)=0.803476, 95% day-bootstrap CI [0.492106, 1.233154], Holm p=0.00585938.
- H6 TCN vs XGBoost: n_days=11, difference(compared−TCN)=-0.185401, 95% day-bootstrap CI [-0.291931, -0.092208], Holm p=0.0195312.

The complete table is `D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730\05_BIAS_AND_DEVIATIONS\dependency_aware_day_level_diagnostic.csv`. Even when a day-level difference survives, it remains evidence about one legacy test interval, not confirmatory Phase2A evidence.

## 8. Main deviations affecting the paper

- **CRITICAL B01** — Canonical six-fold rolling-origin experiment not executed. Impact: Blocks primary Results claims about six-fold stability and deployment boundaries Action: Run a newly versioned retrospective six-fold rolling-origin benchmark
- **CRITICAL B02** — v2.2 point-target results do not match manuscript target. Impact: P6-P8 cannot populate main H1/H3/H6 tables Action: Use v2.2 only as clearly separated historical supplementary evidence
- **HIGH B03** — Legacy Phase13 uses one 70/15/15 chronological split. Impact: Cannot support cross-fold stability or robust temporal deployment claims Action: Recompute on six frozen rolling origins
- **HIGH B04** — Original Phase14 inference unit is pooled sample-level. Impact: Existing significance stars are not sufficient evidence Action: Use fold/day/node-day or moving-block clustered inference with Holm correction
- **HIGH B05** — Final week was exposed during prior development. Impact: Independent blind-test claim is prohibited Action: Describe all final-week results as retrospective historical evaluation
- **MEDIUM B06** — Legacy panel includes two incomplete boundary hours. Impact: Counts and availability rates can differ by 102 rows Action: Use the Phase2A complete-hour denominator consistently
- **MEDIUM B07** — Eligibility thresholds condition evaluation on sufficiently observed windows. Impact: Reported error is conditional, not unconditional corridor performance Action: Publish the loss funnel and stratified performance by coverage
- **MEDIUM B08** — H6 future-window mean smooths hourly extremes. Impact: Do not interpret decreasing MAE with horizon as easier point forecasting Action: Explain target aggregation and report scale/variance by horizon
- **MEDIUM B09** — Phase13 model set does not include CRG-TCN. Impact: Blocks CRG-TCN superiority claims under Phase2A target Action: Include CRG-TCN only in a fair rerun of all declared models
- **MEDIUM B10** — Phase17 quality analyses use the same old test split. Impact: Reliability conclusions are exploratory Action: Repeat stratification within each rolling fold and summarize stability
- **LOW B11** — Many duplicated archives and manuscript packages exist. Impact: Wrong duplicate can enter a manuscript table Action: Use canonical-path and SHA-256 registry in this audit package
- **LOW B12** — Environmental T2 data belongs to another multimodal scope. Impact: Could misstate the AJSE sparse-FCD-only design Action: Keep outside the canonical Phase2A result set unless a new multimodal study is declared

- **HIGH B13** — Legacy Phase13 H6 includes 51 samples per prediction file whose target window extends one hour beyond the canonical complete-hour grid. Impact: old H6 metrics are not an exact Phase2A sample-set match. Action: use the canonical grid in the new rolling-origin run and do not transplant old H6 values.

## 9. What can and cannot be reused

Can be reused with explicit limitations:

- Phase2A-0 target, split, grid and cleaning definitions.
- Legacy PD data-quality counts after correcting the complete-hour denominator.
- Phase13 predictions/metrics as internally verified single-split exploratory evidence.
- Phase16/17 robustness and stratification as exploratory old-split analyses.
- v2.2 final-week artifacts only as a separate contaminated point-target retrospective supplement.

Cannot be used as primary evidence:

- Legacy Phase13 as if it were six-fold rolling origin.
- v2.2 point-target MAE as if it were future-window mean MAE.
- Phase14 pooled sample-level significance stars as the sole inference.
- Any statement that the exposed final week is an independent blind test.
- Any CRG-TCN superiority statement derived from Phase13, because CRG-TCN is not in that result set.

## 10. Submission readiness and required next work

Current readiness: **METHODS/DATA EVIDENCE PARTLY READY; PRIMARY RESULTS NOT READY.**

Minimum required work before the supplied outline can support an AJSE paper:

1. Execute a new versioned six-fold retrospective rolling-origin benchmark using the frozen future-window-mean H1/H3/H6 definition.
2. Generate a fold-aware common-sample manifest and per-fold scaler/imputer/model provenance.
3. Run the missing 2/4–4/4 aggregation sensitivity if it remains a manuscript claim.
4. Recompute reliability and node/date/traffic-state diagnostics within each fold.
5. Replace pooled sample-level inference with fold/day/node-day or moving-block clustered statistics and Holm correction.
6. Freeze the final code/result hashes only after these steps.

## 11. Evidence files produced

- Master workbook: `D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730\AJSE_DATA_RESULT_AUDIT_MASTER.xlsx`
- Crosswalk: `D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730\02_EXPERIMENT_RESULT_CROSSWALK\outline_experiment_result_crosswalk.csv`
- Dataset audit: `D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730\03_DATASET_VALIDATION`
- Metric recomputation: `D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730\04_METRIC_RECALCULATION`
- Bias/deviation register: `D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730\05_BIAS_AND_DEVIATIONS\bias_and_deviation_register.csv`
- Claim matrix: `D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730\02_EXPERIMENT_RESULT_CROSSWALK\claim_evidence_matrix.csv`
- Hash registry: `D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730\07_HASHES\evidence_file_hashes_sha256.csv`
- Reusable evidence registry: `D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730\08_REUSABLE_EVIDENCE\reusable_evidence_registry.csv`

## 12. Integrity statement

No original experiment output, prediction, model weight, registry or log was modified. The audit created new summaries and copied only selected small evidence files. Raw commercial FCD, full prediction arrays and model weights were not duplicated into the audit package.
