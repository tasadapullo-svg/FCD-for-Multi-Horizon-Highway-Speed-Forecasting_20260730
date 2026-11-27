# Numerical and Statistical Audit

Status: PASS

The final manuscript retains the locked numerical and inferential statements:

- XGBoost MAE: 0.949, 0.829, and 0.752 km h⁻¹ at H1, H3, and H6.
- SeasonalHA MAE: 0.961, 0.853, and 0.774 km h⁻¹.
- XGBoost–SeasonalHA ΔMAE: −0.0117, −0.0235, and −0.0222 km h⁻¹.
- Holm-adjusted p values: 0.5625, 0.8438, and 1.000 for the three XGBoost–SeasonalHA comparisons.
- Holm-significant comparisons: 0/15.
- Formal runs: 180/180 completed; 0 failed.
- Leakage audit: 20/20 full-sample assertions passed.
- Future-information violations, target recomputation mismatches, and cross-split target-window violations: all zero.

The text keeps descriptive ranking separate from inferential evidence. It does not convert non-significance into equivalence and does not convert the lowest mean MAE into stable superiority. Fold-level paired inference remains the primary analysis, while the day × spatial-block bootstrap remains supplementary.

Tables, embedded media, and References are unchanged from the approved English source. All seven source figures were copied without numerical alteration.
