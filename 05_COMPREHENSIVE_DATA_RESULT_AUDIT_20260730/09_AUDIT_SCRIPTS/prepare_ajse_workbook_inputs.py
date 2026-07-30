from pathlib import Path
import json
import pandas as pd

ROOT = Path(r"D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730")

rows = [
    {
        "result_family": "Canonical AJSE Phase2A",
        "target": "FUTURE_WINDOW_MEAN_SPEED",
        "horizons": "H1/H3/H6",
        "history": "24 h contiguous sequence; longer-context fields must be separately declared",
        "split_design": "Six-fold retrospective rolling origin (required)",
        "time_grid": "Complete hours: 2025-12-08 14:00 to 2026-02-28 23:00",
        "nodes": 51,
        "result_status": "NOT_EXECUTED",
        "independent_blind_test": "NO; final week contaminated",
        "primary_manuscript_use": "REQUIRED BUT MISSING",
        "exact_definition_match": "CANONICAL",
        "notes": "Phase2A-0 is BLOCKED for confirmatory use; no Phase2A-1 result files found",
    },
    {
        "result_family": "Legacy D:\\2026_PD Phase13",
        "target": "FUTURE_WINDOW_MEAN_SPEED",
        "horizons": "H1/H3/H6",
        "history": "24 h input sequence",
        "split_design": "Single chronological 70/15/15",
        "time_grid": "Legacy panel includes 2025-12-08 13:00 and 2026-03-01 00:00 partial boundary hours",
        "nodes": 51,
        "result_status": "105 prediction files verified; 0 metric mismatches",
        "independent_blind_test": "NO",
        "primary_manuscript_use": "EXPLORATORY/HISTORICAL ONLY",
        "exact_definition_match": "PARTIAL; H6 has 51 boundary samples/file outside canonical grid",
        "notes": "Common samples/truth within horizon; XGBoost lowest legacy mean MAE at H1/H3/H6",
    },
    {
        "result_family": "v2.2 P6-P8",
        "target": "POINT_SPEED_AT_t_PLUS_H",
        "horizons": "various v2.2 horizons",
        "history": "v2.2 model-specific",
        "split_design": "v2.2 development/final-week chain",
        "time_grid": "Includes exposed final week 2026-02-22 to 2026-02-28",
        "nodes": 51,
        "result_status": "COMPLETED HISTORICAL CHAIN",
        "independent_blind_test": "PROHIBITED CLAIM",
        "primary_manuscript_use": "A12 SUPPLEMENT ONLY",
        "exact_definition_match": "NO: point target differs from window mean",
        "notes": "Keep quarantined from canonical Phase2A tables",
    },
    {
        "result_family": "D:\\2026_T2_ENV",
        "target": "Multimodal/environmental extension",
        "horizons": "Not established as canonical Phase2A",
        "history": "Weather/rain/air-quality/event context",
        "split_design": "Separate project",
        "time_grid": "Separate multimodal panel",
        "nodes": "",
        "result_status": "OUT OF SCOPE FOR CURRENT OUTLINE",
        "independent_blind_test": "NOT ASSESSED",
        "primary_manuscript_use": "DO NOT MIX",
        "exact_definition_match": "NO",
        "notes": "Use only if a new multimodal research question is declared",
    },
]
pd.DataFrame(rows).to_csv(ROOT / "02_EXPERIMENT_RESULT_CROSSWALK" / "result_family_definition_comparison.csv", index=False, encoding="utf-8-sig")

hashes = pd.read_csv(ROOT / "07_HASHES" / "evidence_file_hashes_sha256.csv")
mask = (
    hashes.full_path.str.contains(r"outputs\\locked\\phase13_full\\predictions", case=False, regex=True)
    | hashes.full_path.str.contains(r"Phase2A0_Definition_Freeze", case=False, regex=False)
    | hashes.full_path.str.contains(r"phase13_strong_baseline_metrics|phase13_strong_baselines.yaml|phase13_strong_baselines.py|phase14_final|phase16_|phase17_", case=False, regex=True)
    | hashes.full_path.str.contains("AJSE_Phase2A_详细写作大纲", case=False, regex=False)
)
critical = hashes[mask].drop_duplicates(["sha256", "full_path"]).copy()
critical.to_csv(ROOT / "07_HASHES" / "critical_hashes_for_workbook.csv", index=False, encoding="utf-8-sig")

dup = pd.read_csv(ROOT / "07_HASHES" / "duplicate_evidence_files_by_sha256.csv")
if not dup.empty:
    summary = dup.groupby(["duplicate_group", "sha256"], as_index=False).agg(
        member_count=("full_path", "count"),
        families=("family", lambda s: " | ".join(sorted(set(map(str, s))))),
        example_paths=("full_path", lambda s: " | ".join(list(map(str, s))[:3])),
    ).sort_values(["member_count", "duplicate_group"], ascending=[False, True]).head(500)
else:
    summary = pd.DataFrame(columns=["duplicate_group", "sha256", "member_count", "families", "example_paths"])
summary.to_csv(ROOT / "07_HASHES" / "duplicate_group_summary_for_workbook.csv", index=False, encoding="utf-8-sig")

status = json.loads((ROOT / "06_REPORTS" / "AJSE_AUDIT_EXECUTIVE_STATUS.json").read_text(encoding="utf-8"))
exec_rows = [
    {"item": "Overall audit status", "value": status["audit_status"], "interpretation": "Primary manuscript result set is incomplete"},
    {"item": "Canonical target", "value": status["canonical_target"], "interpretation": "Mean observed speed over next H hours"},
    {"item": "Canonical horizons", "value": "/".join(map(str, status["canonical_horizons"])), "interpretation": "H1/H3/H6"},
    {"item": "Phase2A-0 status", "value": status["phase2a0_status"], "interpretation": "Independent confirmatory route blocked by contamination"},
    {"item": "Phase2A-1 result files", "value": status["phase2a1_result_files"], "interpretation": "No six-fold canonical result set found"},
    {"item": "Six-fold rolling origin completed", "value": status["six_fold_rolling_origin_completed"], "interpretation": "Required primary experiment remains outstanding"},
    {"item": "Legacy Phase13 predictions audited", "value": status["legacy_phase13_prediction_files_audited"], "interpretation": "Expected 105"},
    {"item": "Legacy metric mismatch files", "value": status["legacy_phase13_metric_mismatch_files"], "interpretation": "0 means stored metrics reproduced"},
    {"item": "Legacy H6 canonical boundary", "value": "MISMATCH: 51 samples/file", "interpretation": "Target windows extend to 2026-03-01 00:00"},
    {"item": "v2.2 primary reuse", "value": status["v22_primary_reuse"], "interpretation": "Point target differs from manuscript task"},
    {"item": "Independent blind-test claim", "value": status["independent_blind_test_claim"], "interpretation": "Use retrospective historical wording"},
    {"item": "Original experiment files modified", "value": status["original_files_modified"], "interpretation": "Audit is read-only with new outputs"},
    {"item": "DOCX visual render QA", "value": status["docx_visual_render_completed"], "interpretation": "Structural parse completed; LibreOffice unavailable"},
]
pd.DataFrame(exec_rows).to_csv(ROOT / "06_REPORTS" / "executive_summary_for_workbook.csv", index=False, encoding="utf-8-sig")

print("Workbook input tables prepared", len(critical), len(summary))
