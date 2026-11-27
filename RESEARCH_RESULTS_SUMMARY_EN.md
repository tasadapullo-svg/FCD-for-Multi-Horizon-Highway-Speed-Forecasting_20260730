# Source-version note

This consolidated report is a preserved earlier summary. Use current FIGURE_DATA_INDEX.csv, TABLE_DATA_INDEX.csv and CANONICAL_RESULT_INDEX.csv for corrected Prompt12 views and final numerical sources. No experiment was rerun for publication.

# Complete Research Results Summary (Frozen Evidence; Not Manuscript Text)

**Project:** APIN-D-26-12623. **Historical runs:** 180 original, 651 G2, 93 Ridge diagnostic. **New fits:** 0. **New traffic datasets:** 0.

Primary original result: G1 Method A, a per-sample three-seed ensemble. Some manuscript numbers reflect Method B and are not interchangeable. G2 is an independent revision implementation.

## R01 — Data collection and availability

- **Experiment ID:** R01
- **Scientific question:** Observation availability
- **Input data:** Frozen accepted aggregate `E01_01_Data_Lineage_and_Coverage.csv`; source and SHA-256 in Master_Aggregate_Provenance.csv.
- **Experimental design / models / horizons:** Frozen protocol; see complete category CSV. No retraining.
- **Sample support:** 16 rows in the display summary; full counts in source CSV.
- **Main numerical results:**

| metric | value | statistical_level |
| --- | --- | --- |
| planned_15min_slots | 403512 | node-quarter |
| planned_hourly_slots | 100878 | node-hour |
| returned_parsed_rows_all_span | 244477 | return-row |
| quality_pass_rows_all_span | 243307 | return-row |
| quality_fail_rows_all_span | 1170 | return-row |
| quality_dedup_all_span | 241727 | node-quarter |
| quality_dedup_in_grid | 241601 | node-quarter |
| returned_rows_in_grid | 244351 | return-row |
| returned_rows_outside_grid | 126 | return-row |
| quality_dedup_outside_grid | 126 | node-quarter |

- **Statistical significance:** Only prespecified R04 comparisons and their frozen evidence support inference; other summaries are descriptive.
- **Scientific interpretation / limitations:** Different row and slot denominators; missingness is not zero speed.
- **Reviewer comments:** See APIN_03 mapping, original 31 comments preserved.
- **Proposed manuscript section / figures and tables:** Fig02 / Table01
- **Source data file:** `08_MASTER_RESEARCH_RESULTS/R01_Data_Collection_and_Availability/E01_01_Data_Lineage_and_Coverage.csv`

## R02 — Forecast target and eligibility

- **Experiment ID:** R02
- **Scientific question:** H1/H3/H6 support
- **Input data:** Frozen accepted aggregate `E01_06_H6_Target_Completeness.csv`; source and SHA-256 in Master_Aggregate_Provenance.csv.
- **Experimental design / models / horizons:** Frozen protocol; see complete category CSV. No retraining.
- **Sample support:** 12 rows in the display summary; full counts in source CSV.
- **Main numerical results:**

| fold | split | h6_group | n | target_mean | target_sd | target_median | target_p05 | target_p95 | fraction_within_fold_split |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | test | COMPLETE_6_OF_6 | 1006 | 89.1762 | 15.2833 | 94.0 | 60.6042 | 100 | 0.2865 |
| 1 | test | PARTIAL_5_OF_6 | 2505 | 88.9608 | 15.8338 | 94.0 | 52.3067 | 100 | 0.7135 |
| 1 | train | COMPLETE_6_OF_6 | 29713 | 88.9729 | 15.8197 | 94.0 | 48.9667 | 100 | 0.8092 |
| 1 | train | PARTIAL_5_OF_6 | 7005 | 88.3956 | 16.9127 | 94.0 | 43.0 | 100 | 0.1908 |
| 1 | validation | COMPLETE_6_OF_6 | 1460 | 89.0635 | 15.7429 | 94.0 | 46.1417 | 100 | 0.3555 |
| 1 | validation | PARTIAL_5_OF_6 | 2647 | 89.1615 | 16.1347 | 94.0 | 46.73 | 100 | 0.6445 |
| 2 | test | COMPLETE_6_OF_6 | 1797 | 89.3774 | 15.8604 | 94.0 | 51.6139 | 100 | 0.3725 |
| 2 | test | PARTIAL_5_OF_6 | 3027 | 88.6986 | 16.5154 | 94.0 | 43.9 | 100 | 0.6275 |
| 2 | train | COMPLETE_6_OF_6 | 31323 | 88.9766 | 15.8093 | 94.0 | 48.8347 | 100 | 0.7623 |
| 2 | train | PARTIAL_5_OF_6 | 9766 | 88.6374 | 16.6773 | 94.0 | 43.0 | 100 | 0.2377 |

- **Statistical significance:** Only prespecified R04 comparisons and their frozen evidence support inference; other summaries are descriptive.
- **Scientific interpretation / limitations:** H6 partial 5/6 and complete 6/6 targets must remain distinct.
- **Reviewer comments:** See APIN_03 mapping, original 31 comments preserved.
- **Proposed manuscript section / figures and tables:** Fig03 / Table03,05
- **Source data file:** `08_MASTER_RESEARCH_RESULTS/R02_Forecast_Target_and_Eligibility/E01_06_H6_Target_Completeness.csv`

## R03 — Original six-model results

- **Experiment ID:** R03
- **Scientific question:** Method A versus Method B
- **Input data:** Frozen accepted aggregate `E03_03_Original_vs_Recomputed_Table7.csv`; source and SHA-256 in Master_Aggregate_Provenance.csv.
- **Experimental design / models / horizons:** Frozen protocol; see complete category CSV. No retraining.
- **Sample support:** 18 rows in the display summary; full counts in source CSV.
- **Main numerical results:**

| model | horizon | method_A_value | method_B_value | method_A_fold_sd |
| --- | --- | --- | --- | --- |
| GRU | 1 | 1.047 | 1.1506 | 0.1898 |
| GRU | 3 | 0.9476 | 1.043 | 0.1646 |
| GRU | 6 | 0.8689 | 0.9583 | 0.1648 |
| HA | 1 | 1.8247 | 1.8247 | 0.1192 |
| HA | 3 | 1.7043 | 1.7043 | 0.1363 |
| HA | 6 | 1.5048 | 1.5048 | 0.1199 |
| Persistence | 1 | 0.9504 | 0.9504 | 0.1547 |
| Persistence | 3 | 1.1702 | 1.1702 | 0.1362 |
| Persistence | 6 | 1.4697 | 1.4697 | 0.1824 |
| Ridge | 1 | 1.2251 | 1.2251 | 0.2668 |

- **Statistical significance:** Only prespecified R04 comparisons and their frozen evidence support inference; other summaries are descriptive.
- **Scientific interpretation / limitations:** Original Method A uses per-sample three-seed ensemble; Method B is mean seed metric.
- **Reviewer comments:** See APIN_03 mapping, original 31 comments preserved.
- **Proposed manuscript section / figures and tables:** Fig04 / Table07
- **Source data file:** `08_MASTER_RESEARCH_RESULTS/R03_Original_Six_Model_Forecasting/E03_03_Original_vs_Recomputed_Table7.csv`

## R04 — Statistical inference

- **Experiment ID:** R04
- **Scientific question:** 15 prespecified contrasts
- **Input data:** Frozen accepted aggregate `E03_08_Holm_Adjusted_Comparisons.csv`; source and SHA-256 in Master_Aggregate_Provenance.csv.
- **Experimental design / models / horizons:** Frozen protocol; see complete category CSV. No retraining.
- **Sample support:** 15 rows in the display summary; full counts in source CSV.
- **Main numerical results:**

| horizon | comparison | effect | CI_low | CI_high | raw_p | holm_adjusted_p | significant_holm_0_05 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | XGBoost_vs_GRU | -0.1051 | -0.1712 | 0.0029 | 0.0285 | 0.057 | False |
| 1 | XGBoost_vs_Ridge | -0.2569 | -0.3077 | -0.1818 | 0.0001 | 0.0005 | True |
| 1 | XGBoost_vs_SeasonalHA | 0.0773 | -0.1455 | 0.4451 | 0.6398 | 0.6398 | False |
| 1 | Persistence_vs_HA | -0.8892 | -0.9574 | -0.8188 | 0.0001 | 0.0005 | True |
| 1 | GRU_vs_Ridge | -0.1518 | -0.2292 | -0.0916 | 0.0003 | 0.0009 | True |
| 3 | XGBoost_vs_GRU | -0.2316 | -0.4844 | -0.0745 | 0.0434 | 0.0868 | False |
| 3 | XGBoost_vs_Ridge | -0.4021 | -0.6989 | -0.1978 | 0.0056 | 0.0168 | True |
| 3 | XGBoost_vs_SeasonalHA | 0.0123 | -0.1043 | 0.1737 | 0.8754 | 0.8754 | False |
| 3 | Persistence_vs_HA | -0.5224 | -0.5933 | -0.4552 | 0.0001 | 0.0005 | True |
| 3 | GRU_vs_Ridge | -0.1705 | -0.2531 | -0.0895 | 0.0001 | 0.0005 | True |

- **Statistical significance:** Only prespecified R04 comparisons and their frozen evidence support inference; other summaries are descriptive.
- **Scientific interpretation / limitations:** Three-day block bootstrap is primary; ordinary CIs are not simultaneous Holm CIs.
- **Reviewer comments:** See APIN_03 mapping, original 31 comments preserved.
- **Proposed manuscript section / figures and tables:** Fig06 / Table07
- **Source data file:** `08_MASTER_RESEARCH_RESULTS/R04_Statistical_Inference/E03_08_Holm_Adjusted_Comparisons.csv`

## R05 — Traffic regime and reliability

- **Experiment ID:** R05
- **Scientific question:** Conditional error
- **Input data:** Frozen accepted aggregate `E02_04_Traffic_Regime_Distribution.csv`; source and SHA-256 in Master_Aggregate_Provenance.csv.
- **Experimental design / models / horizons:** Frozen protocol; see complete category CSV. No retraining.
- **Sample support:** 15 rows in the display summary; full counts in source CSV.
- **Main numerical results:**

| level | horizon | state | n | fraction | nodes | dates | threshold |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RETURN_ROW_UNFILTERED |  | near_free_flow_proxy | 210640 | 0.8616 | 51 | 82 | 0.7 |
| RETURN_ROW_UNFILTERED |  | intermediate | 27901 | 0.1141 | 51 | 82 | 0.7 |
| RETURN_ROW_UNFILTERED |  | congested_proxy | 5936 | 0.0243 | 51 | 82 | 0.7 |
| RETURN_ROW_QUALITY_PASS |  | near_free_flow_proxy | 210435 | 0.8649 | 51 | 82 | 0.7 |
| RETURN_ROW_QUALITY_PASS |  | intermediate | 26953 | 0.1108 | 51 | 82 | 0.7 |
| RETURN_ROW_QUALITY_PASS |  | congested_proxy | 5919 | 0.0243 | 51 | 82 | 0.7 |
| FUTURE_OBSERVED_TARGET_HOURS | 1.0 | congested_proxy | 952 | 0.0249 | 22 | 40 | 0.7 |
| FUTURE_OBSERVED_TARGET_HOURS | 1.0 | intermediate | 4072 | 0.1066 | 51 | 40 | 0.7 |
| FUTURE_OBSERVED_TARGET_HOURS | 1.0 | near_free_flow_proxy | 33177 | 0.8685 | 51 | 41 | 0.7 |
| FUTURE_OBSERVED_TARGET_HOURS | 3.0 | congested_proxy | 614 | 0.0248 | 8 | 40 | 0.7 |

- **Statistical significance:** Only prespecified R04 comparisons and their frozen evidence support inference; other summaries are descriptive.
- **Scientific interpretation / limitations:** Provider speed and free-flow proxies are not independent observed true speed.
- **Reviewer comments:** See APIN_03 mapping, original 31 comments preserved.
- **Proposed manuscript section / figures and tables:** Fig05,07 / Table07
- **Source data file:** `08_MASTER_RESEARCH_RESULTS/R05_Traffic_Regime_and_Reliability/E02_04_Traffic_Regime_Distribution.csv`

## R06 — Data and protocol sensitivity

- **Experiment ID:** R06
- **Scientific question:** Native and common-origin estimands
- **Input data:** Frozen accepted aggregate `G2_02_Experiment_Run_Registry.csv`; source and SHA-256 in Master_Aggregate_Provenance.csv.
- **Experimental design / models / horizons:** Frozen protocol; see complete category CSV. No retraining.
- **Sample support:** 20 rows in the display summary; full counts in source CSV.
- **Main numerical results:**

| condition | model | horizon | fold | test_n | test_mae |
| --- | --- | --- | --- | --- | --- |
| history12 | XGBoost | 1 | 4 | 6357 | 1.0397 |
| threshold1 | Persistence | 3 | 2 | 7895 | 1.0219 |
| base | Ridge | 3 | 1 | 2919 | 1.1655 |
| threshold1 | SeasonalHA | 1 | 3 | 8410 | 0.7777 |
| threshold3 | SeasonalHA | 1 | 1 | 541 | 0.9899 |
| base | Ridge | 1 | 3 | 7164 | 0.9062 |
| strict6 | Persistence | 6 | 2 | 1797 | 1.3786 |
| threshold1 | Persistence | 6 | 2 | 8213 | 1.3038 |
| base | GRU | 1 | 1 | 5978 |  |
| base | XGBoost | 1 | 3 | 7164 | 0.642 |

- **Statistical significance:** Only prespecified R04 comparisons and their frozen evidence support inference; other summaries are descriptive.
- **Scientific interpretation / limitations:** Threshold 4/4 was not estimable; native and common-origin supports differ.
- **Reviewer comments:** See APIN_03 mapping, original 31 comments preserved.
- **Proposed manuscript section / figures and tables:** Fig08 / Table08
- **Source data file:** `08_MASTER_RESEARCH_RESULTS/R06_Data_and_Protocol_Sensitivity/G2_02_Experiment_Run_Registry.csv`

## R07 — GATE-FCD ablation

- **Experiment ID:** R07
- **Scientific question:** Protocol contrast
- **Input data:** Frozen accepted aggregate `E05_Native_Eligibility_Set_Check.csv`; source and SHA-256 in Master_Aggregate_Provenance.csv.
- **Experimental design / models / horizons:** Frozen protocol; see complete category CSV. No retraining.
- **Sample support:** 12 rows in the display summary; full counts in source CSV.
- **Main numerical results:**

| fold | horizon | ridge_native_n | xgboost_native_n | common_n | symmetric_difference_n | basis | decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 50269 | 50269 | 50269 | 0 | Both use the same verified base Data.tabular() manifest and no model-specific eligibility gate | NO_ADDITIONAL_TRAINING_REQUIRED |
| 2 | 1 | 56858 | 56858 | 56858 | 0 | Both use the same verified base Data.tabular() manifest and no model-specific eligibility gate | NO_ADDITIONAL_TRAINING_REQUIRED |
| 3 | 1 | 64056 | 64056 | 64056 | 0 | Both use the same verified base Data.tabular() manifest and no model-specific eligibility gate | NO_ADDITIONAL_TRAINING_REQUIRED |
| 4 | 1 | 70441 | 70441 | 70441 | 0 | Both use the same verified base Data.tabular() manifest and no model-specific eligibility gate | NO_ADDITIONAL_TRAINING_REQUIRED |
| 5 | 1 | 76015 | 76015 | 76015 | 0 | Both use the same verified base Data.tabular() manifest and no model-specific eligibility gate | NO_ADDITIONAL_TRAINING_REQUIRED |
| 6 | 1 | 82698 | 82698 | 82698 | 0 | Both use the same verified base Data.tabular() manifest and no model-specific eligibility gate | NO_ADDITIONAL_TRAINING_REQUIRED |
| 1 | 6 | 44336 | 44336 | 44336 | 0 | Both use the same verified base Data.tabular() manifest and no model-specific eligibility gate | NO_ADDITIONAL_TRAINING_REQUIRED |
| 2 | 6 | 49424 | 49424 | 49424 | 0 | Both use the same verified base Data.tabular() manifest and no model-specific eligibility gate | NO_ADDITIONAL_TRAINING_REQUIRED |
| 3 | 6 | 55776 | 55776 | 55776 | 0 | Both use the same verified base Data.tabular() manifest and no model-specific eligibility gate | NO_ADDITIONAL_TRAINING_REQUIRED |
| 4 | 6 | 60653 | 60653 | 60653 | 0 | Both use the same verified base Data.tabular() manifest and no model-specific eligibility gate | NO_ADDITIONAL_TRAINING_REQUIRED |

- **Statistical significance:** Only prespecified R04 comparisons and their frozen evidence support inference; other summaries are descriptive.
- **Scientific interpretation / limitations:** Noncausal scaling is leakage diagnostic, not a valid performance rank.
- **Reviewer comments:** See APIN_03 mapping, original 31 comments preserved.
- **Proposed manuscript section / figures and tables:** Fig08 / Table08
- **Source data file:** `08_MASTER_RESEARCH_RESULTS/R07_GATE_FCD_Ablation/E05_Native_Eligibility_Set_Check.csv`

## R08 — Model fairness and numerical correction

- **Experiment ID:** R08
- **Scientific question:** Ridge SVD corrected native metrics
- **Input data:** Frozen accepted aggregate `Ridge_Corrected_Aggregates.csv`; source and SHA-256 in Master_Aggregate_Provenance.csv.
- **Experimental design / models / horizons:** Frozen protocol; see complete category CSV. No retraining.
- **Sample support:** 15 rows in the display summary; full counts in source CSV.
- **Main numerical results:**

| condition | horizon | alpha | fold_runs | test_samples_sum | old_fold_macro_MAE | svd_fold_macro_MAE | delta_fold_macro_MAE | old_sample_weighted_MAE | svd_sample_weighted_MAE | round3_changed_folds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | 1 | 1.0 | 6 | 38201 | 1.2209 | 1.2207 | -0.0002 | 1.2018 | 1.2016 | 1 |
| base | 1 | 10.0 | 6 | 38201 | 1.2187 | 1.2185 | -0.0002 | 1.1996 | 1.1994 | 1 |
| base | 3 | 1.0 | 6 | 24805 | 1.1285 | 1.1285 | 0.0001 | 1.1067 | 1.1068 | 2 |
| base | 3 | 10.0 | 6 | 24805 | 1.1271 | 1.1272 | 0.0001 | 1.1057 | 1.1058 | 1 |
| base | 6 | 1.0 | 6 | 29141 | 1.0812 | 1.0812 | 0.0 | 1.0457 | 1.0458 | 0 |
| base | 6 | 10.0 | 6 | 29141 | 1.0808 | 1.0808 | 0.0 | 1.0455 | 1.0455 | 0 |
| leaky_scaling | 1 | 1.0 | 6 | 38201 | 1.2204 | 1.2205 | 0.0001 | 1.2013 | 1.2014 | 2 |
| leaky_scaling | 6 | 1.0 | 6 | 29141 | 1.0812 | 1.0812 | -0.0001 | 1.0458 | 1.0457 | 0 |
| returned_only | 1 | 1.0 | 6 | 30767 | 1.2294 | 1.2292 | -0.0002 | 1.207 | 1.2068 | 2 |
| returned_only | 6 | 1.0 | 6 | 24037 | 1.4428 | 1.4428 | 0.0 | 1.3807 | 1.3807 | 2 |

- **Statistical significance:** Only prespecified R04 comparisons and their frozen evidence support inference; other summaries are descriptive.
- **Scientific interpretation / limitations:** Do not reuse old Cholesky paired contrasts as corrected SVD paired inference.
- **Reviewer comments:** See APIN_03 mapping, original 31 comments preserved.
- **Proposed manuscript section / figures and tables:** Fig08 / Table04,08
- **Source data file:** `08_MASTER_RESEARCH_RESULTS/R08_Model_Fairness_and_Ridge/Ridge_Corrected_Aggregates.csv`

## R09 — Spatial and operational evidence

- **Experiment ID:** R09
- **Scientific question:** Distance estimands
- **Input data:** Frozen accepted aggregate `GIS_Corridor_Length_Reconciliation.csv`; source and SHA-256 in Master_Aggregate_Provenance.csv.
- **Experimental design / models / horizons:** Frozen protocol; see complete category CSV. No retraining.
- **Sample support:** 6 rows in the display summary; full counts in source CSV.
- **Main numerical results:**

| measure | km | status | basis |
| --- | --- | --- | --- |
| Original manuscript approximate corridor length | 130.0 | UNVERIFIED_APPROXIMATE_CLAIM | Original manuscript; no dated centreline, endpoints or GIS measurement recovered |
| Sum of adjacent-node WGS84 straight geodesics | 137.3949 | VERIFIED_FROM_51_COORDINATES | Original node coordinate sequence; not road mileage |
| Sum of adjacent-node current OSM graph shortest paths | 156.2741 | CURRENT_OSM_ANCHOR_PROXY_ONLY | Undirected graph, each node anchored to nearest segment endpoint; can detour or repeat edges |
| Unique current OSM graph edge length in selected paths | 112.2639 | CURRENT_OSM_PROXY_ONLY | Deduplicated selected path edges; not necessarily original research mainline |
| Repeated selected graph edge length | 44.0102 | DIAGNOSTIC_ONLY | Maximum per-edge path reuse 5 times |
| Historically verified mainline corridor length |  | HISTORICAL_CORRIDOR_LENGTH_NOT_VERIFIED | No dated matched mainline/endpoint record or directed topology evidence |

- **Statistical significance:** Only prespecified R04 comparisons and their frozen evidence support inference; other summaries are descriptive.
- **Scientific interpretation / limitations:** Current OSM paths do not verify historical 130 km mainline.
- **Reviewer comments:** See APIN_03 mapping, original 31 comments preserved.
- **Proposed manuscript section / figures and tables:** Fig01 / Table09
- **Source data file:** `08_MASTER_RESEARCH_RESULTS/R09_Spatial_and_Operational/GIS_Corridor_Length_Reconciliation.csv`

## R10 — Claims and limitations

- **Experiment ID:** R10
- **Scientific question:** Claim registry
- **Input data:** Frozen accepted aggregate `Final_Scientific_Claims_Registry.csv`; source and SHA-256 in Master_Aggregate_Provenance.csv.
- **Experimental design / models / horizons:** Frozen protocol; see complete category CSV. No retraining.
- **Sample support:** 11 rows in the display summary; full counts in source CSV.
- **Main numerical results:**

| claim_id | proposed_claim | support_status | scope_or_limitation | evidence_file |
| --- | --- | --- | --- | --- |
| C01 | XGBoost vs Ridge obtains significant day-macro evidence at H1 and H3 | STATISTICALLY_SUPPORTED | G1 3-day Holm; H6 is not included | E03_08_Holm_Adjusted_Comparisons.csv |
| C02 | GRU vs Ridge obtains significant day-macro evidence at H1, H3 and H6 | STATISTICALLY_SUPPORTED | Same corridor; retrospective 41 test dates | E03_08_Holm_Adjusted_Comparisons.csv |
| C03 | XGBoost is stably superior to SeasonalHA across all horizons | NOT_SUPPORTED | All three G1 primary confidence intervals span zero | E03_08_Holm_Adjusted_Comparisons.csv |
| C04 | GATE-FCD supports transparent data auditing and a common evaluation contract | DESCRIPTIVELY_SUPPORTED | Protocol and denominators audited; not an accuracy superiority claim | G1_06_Acceptance_Report_CN.md |
| C05 | GATE-FCD guarantees lower forecasting MAE | NOT_SUPPORTED | G2 ablations and key tests do not establish a universal improvement | G2_Key_Comparisons_Actual.csv |
| C06 | Stricter sample eligibility always improves forecasting | NOT_SUPPORTED | 3/4 and strict H6 comparisons do not show universal improvement; 4/4 lacks validation support | G2_Actual_Common_Origin_Contrasts.csv |
| C07 | Current outcomes validate true road-speed accuracy | NOT_SUPPORTED | Target is provider-returned speed without synchronous independent truth | G1_06_Acceptance_Report_CN.md |
| C08 | Current outcomes establish generalisation to another corridor | NOT_SUPPORTED | Single commercial FCD corridor; E08 not run | G2_07_Acceptance_Report_CN.md |
| C09 | Current outcomes establish reliable live production availability | NOT_SUPPORTED | Original API arrival latency unavailable | G2_01_Source_and_Implementation_Report_CN.md |
| C10 | 4/4 completeness yields a six-fold model comparison at H6 | NOT_ESTIMABLE | All H6 validation folds empty | E04_Threshold4_Sample_Support.csv |

- **Statistical significance:** Only prespecified R04 comparisons and their frozen evidence support inference; other summaries are descriptive.
- **Scientific interpretation / limitations:** E08 target asset absent; no external validation or trained spatial-neighbor model.
- **Reviewer comments:** See APIN_03 mapping, original 31 comments preserved.
- **Proposed manuscript section / figures and tables:** All figures and reviewer matrix
- **Source data file:** `08_MASTER_RESEARCH_RESULTS/R10_Claims_and_Limitations/Final_Scientific_Claims_Registry.csv`

## Numerical boundaries and unavailable evidence

| claim_id | proposed_claim | support_status | scope_or_limitation |
| --- | --- | --- | --- |
| C01 | XGBoost vs Ridge obtains significant day-macro evidence at H1 and H3 | STATISTICALLY_SUPPORTED | G1 3-day Holm; H6 is not included |
| C02 | GRU vs Ridge obtains significant day-macro evidence at H1, H3 and H6 | STATISTICALLY_SUPPORTED | Same corridor; retrospective 41 test dates |
| C03 | XGBoost is stably superior to SeasonalHA across all horizons | NOT_SUPPORTED | All three G1 primary confidence intervals span zero |
| C04 | GATE-FCD supports transparent data auditing and a common evaluation contract | DESCRIPTIVELY_SUPPORTED | Protocol and denominators audited; not an accuracy superiority claim |
| C05 | GATE-FCD guarantees lower forecasting MAE | NOT_SUPPORTED | G2 ablations and key tests do not establish a universal improvement |
| C06 | Stricter sample eligibility always improves forecasting | NOT_SUPPORTED | 3/4 and strict H6 comparisons do not show universal improvement; 4/4 lacks validation support |
| C07 | Current outcomes validate true road-speed accuracy | NOT_SUPPORTED | Target is provider-returned speed without synchronous independent truth |
| C08 | Current outcomes establish generalisation to another corridor | NOT_SUPPORTED | Single commercial FCD corridor; E08 not run |
| C09 | Current outcomes establish reliable live production availability | NOT_SUPPORTED | Original API arrival latency unavailable |
| C10 | 4/4 completeness yields a six-fold model comparison at H6 | NOT_ESTIMABLE | All H6 validation folds empty |
| C11 | G2 key paired changes are significant after four-test Holm correction | NOT_SUPPORTED | All four G2 adjusted p values exceed 0.05 |

E08 was not run. The 51 GIS nodes and 50 current-OSM routes do not prove the historical mainline. Fifteen nodes require author review. Commercial data distribution rights remain unconfirmed.
