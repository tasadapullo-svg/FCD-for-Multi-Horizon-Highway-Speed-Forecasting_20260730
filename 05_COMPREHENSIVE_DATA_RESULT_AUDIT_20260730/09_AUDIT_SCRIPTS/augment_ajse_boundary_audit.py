from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(r"D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730")
PRED = Path(r"D:\2026_PD\outputs\locked\phase13_full\predictions")
END = pd.Timestamp("2026-02-28 23:00:00")


def calc(df: pd.DataFrame) -> dict:
    y = df.y_true.to_numpy(float)
    p = df.y_pred.to_numpy(float)
    e = p - y
    den = np.abs(y) + np.abs(p)
    var = np.square(y - y.mean()).sum()
    return {
        "N": len(df), "MAE": float(np.abs(e).mean()), "RMSE": float(np.sqrt(np.square(e).mean())),
        "sMAPE": float((2 * np.abs(e) / np.maximum(den, 1e-6)).mean()),
        "R2": float(1 - np.square(e).sum() / var) if var else np.nan, "Bias": float(e.mean()),
    }


rows = []
for p in sorted(PRED.glob("*.parquet")):
    df = pd.read_parquet(p)
    h = int(df.horizon.iloc[0])
    target_end = pd.to_datetime(df.timestamp) + pd.to_timedelta(h - 1, unit="h")
    keep = target_end <= END
    original = calc(df)
    canonical = calc(df.loc[keep])
    rows.append({
        "prediction_file": str(p), "model": str(df.model.iloc[0]), "horizon": h, "seed": int(df.seed.iloc[0]),
        "original_N": original["N"], "boundary_excluded_N": int((~keep).sum()), "canonical_complete_hour_N": canonical["N"],
        "original_MAE": original["MAE"], "canonical_complete_hour_MAE": canonical["MAE"],
        "MAE_change_after_boundary_exclusion": canonical["MAE"] - original["MAE"],
        "original_RMSE": original["RMSE"], "canonical_complete_hour_RMSE": canonical["RMSE"],
        "original_sMAPE": original["sMAPE"], "canonical_complete_hour_sMAPE": canonical["sMAPE"],
        "original_R2": original["R2"], "canonical_complete_hour_R2": canonical["R2"],
        "original_Bias": original["Bias"], "canonical_complete_hour_Bias": canonical["Bias"],
        "canonical_sample_boundary_match": int((~keep).sum()) == 0,
    })

out = pd.DataFrame(rows)
out.to_csv(ROOT / "04_METRIC_RECALCULATION" / "phase13_complete_hour_boundary_sensitivity.csv", index=False, encoding="utf-8-sig")
summary = out.groupby("horizon", as_index=False).agg(
    prediction_files=("prediction_file", "count"),
    boundary_excluded_rows_per_file=("boundary_excluded_N", "max"),
    mean_MAE_change=("MAE_change_after_boundary_exclusion", "mean"),
    max_absolute_MAE_change=("MAE_change_after_boundary_exclusion", lambda s: float(np.abs(s).max())),
    all_files_match_boundary=("canonical_sample_boundary_match", "all"),
)
summary.to_csv(ROOT / "03_DATASET_VALIDATION" / "phase13_complete_hour_boundary_summary.csv", index=False, encoding="utf-8-sig")

bias_path = ROOT / "05_BIAS_AND_DEVIATIONS" / "bias_and_deviation_register.csv"
bias = pd.read_csv(bias_path)
if "B13" not in set(bias.issue_id.astype(str)):
    extra = pd.DataFrame([{
        "issue_id": "B13", "severity": "HIGH", "issue": "Legacy Phase13 H6 includes one target hour beyond the canonical complete-hour grid",
        "evidence": "51 H6 test samples per prediction file start at 2026-02-28 19:00 and end at 2026-03-01 00:00; Phase2A grid ends at 2026-02-28 23:00",
        "direction_of_bias": "H6 sample set and MAE differ slightly when the boundary hour is excluded",
        "paper_impact": "Legacy H6 values are not exactly aligned with the Phase2A denominator/sample definition",
        "required_action": "Do not transplant legacy H6 values into canonical Phase2A tables; use the complete-hour grid in the new run",
    }])
    bias = pd.concat([bias, extra], ignore_index=True)
    bias.to_csv(bias_path, index=False, encoding="utf-8-sig")

cross_path = ROOT / "02_EXPERIMENT_RESULT_CROSSWALK" / "outline_experiment_result_crosswalk.csv"
cross = pd.read_csv(cross_path)
mask = cross.experiment_step == "A4"
cross.loc[mask, "status"] = "PARTIAL_PASS_WITH_H6_BOUNDARY_MISMATCH"
cross.loc[mask, "evidence_summary"] = "Old PD Phase13 uses the matching future-window-mean target and H1/H3/H6; however, it uses the old split and 51 H6 test samples extend to 2026-03-01 00:00 beyond the Phase2A complete-hour grid."
cross.to_csv(cross_path, index=False, encoding="utf-8-sig")

status_path = ROOT / "06_REPORTS" / "AJSE_AUDIT_EXECUTIVE_STATUS.json"
status = json.loads(status_path.read_text(encoding="utf-8"))
status["legacy_phase13_complete_hour_alignment"] = {"H1": True, "H3": True, "H6": False, "H6_affected_samples_per_file": 51}
status["canonical_result_set_exact_match"] = False
status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")

report_path = ROOT / "06_REPORTS" / "AJSE_COMPREHENSIVE_DATA_AND_RESULT_AUDIT_REPORT.md"
report = report_path.read_text(encoding="utf-8")
needle = "Thus the archived Phase13 target corresponds to **future-window mean speed**, not point speed. The old windows use history=24 h, input observed ratio ≥0.80 and target observed ratio ≥0.80. For H6 this means at least five observed future hours; for H1/H3 it effectively requires all target hours."
replacement = needle + "\n\n**Canonical-boundary warning:** every H6 prediction file contains 51 samples whose target window ends at `2026-03-01 00:00`, while the Phase2A complete-hour grid ends at `2026-02-28 23:00`. The file `phase13_complete_hour_boundary_sensitivity.csv` recomputes all metrics after excluding those samples. Therefore H6 is target-semantics compatible but not an exact canonical sample-set match."
report = report.replace(needle, replacement)
insert = "\n- **HIGH B13** — Legacy Phase13 H6 includes 51 samples per prediction file whose target window extends one hour beyond the canonical complete-hour grid. Impact: old H6 metrics are not an exact Phase2A sample-set match. Action: use the canonical grid in the new rolling-origin run and do not transplant old H6 values.\n"
marker = "\n## 9. What can and cannot be reused"
if "**HIGH B13**" not in report:
    report = report.replace(marker, insert + marker)
report_path.write_text(report, encoding="utf-8")

print(summary.to_string(index=False))
