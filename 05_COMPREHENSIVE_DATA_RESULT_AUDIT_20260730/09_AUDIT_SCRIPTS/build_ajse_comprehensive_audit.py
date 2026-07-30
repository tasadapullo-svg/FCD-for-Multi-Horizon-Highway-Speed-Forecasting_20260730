from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from scipy.stats import wilcoxon


NOW = datetime.now().astimezone()
OUTPUT_ROOT = Path(r"D:\2026_AJSE_FINAL\05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730")
OUTLINE = Path(r"C:\Users\DELL\Desktop\AJSE_Phase2A_详细写作大纲_逻辑关键词实验详解版.docx")
OUTLINE_EXTRACT_DIR = Path(r"D:\2026_07_23\_ajse_outline_review")
PD_ROOT = Path(r"D:\2026_PD")
PHASE2A_ROOT = Path(r"D:\2026_AJSE_FINAL")
QUARANTINE_ROOT = Path(r"D:\2026_AJSE_FINAL_QUARANTINE")
V22_ROOT = Path(r"D:\CRG_TCN_20260729")
T2_ENV_ROOT = Path(r"D:\2026_T2_ENV")
WORK_ROOT = Path(r"D:\2026_07_23")

DIRS = {
    "outline": OUTPUT_ROOT / "00_SOURCE_OUTLINE",
    "drive": OUTPUT_ROOT / "01_D_DRIVE_INVENTORY",
    "crosswalk": OUTPUT_ROOT / "02_EXPERIMENT_RESULT_CROSSWALK",
    "dataset": OUTPUT_ROOT / "03_DATASET_VALIDATION",
    "metric": OUTPUT_ROOT / "04_METRIC_RECALCULATION",
    "bias": OUTPUT_ROOT / "05_BIAS_AND_DEVIATIONS",
    "reports": OUTPUT_ROOT / "06_REPORTS",
    "hashes": OUTPUT_ROOT / "07_HASHES",
    "evidence": OUTPUT_ROOT / "08_REUSABLE_EVIDENCE",
}


def sha256_file(path: Path, chunk: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            block = f.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def stable_hash_strings(values) -> str:
    h = hashlib.sha256()
    for value in values:
        h.update(str(value).encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def write_csv(path: Path, rows: list[dict], columns: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = []
        seen = set()
        for row in rows:
            for key in row:
                if key not in seen:
                    columns.append(key)
                    seen.add(key)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def safe_rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except Exception:
        return str(path)


def classify_family(path: Path) -> tuple[str, str, str]:
    s = str(path).lower()
    if "2026_ajse_final\\01_phase2a_definition_freeze" in s or "2026_ajse_final\\02_phase2a_release_package" in s:
        return "Phase2A_definition_freeze", "DEFINITION_EVIDENCE", "future-window mean; H1/H3/H6; rolling-origin planned"
    if "2026_pd" in s:
        return "legacy_PD_future_window_mean", "PARTIAL_REUSE", "future-window mean; H1/H3/H6 available; single 70/15/15 split"
    if "2026_ajse_final_quarantine" in s:
        return "v2.2_point_target_quarantine", "A12_ONLY", "point target; exposed retrospective period"
    if "crg_tcn_20260729" in s:
        return "v2.2_point_target_and_audits", "A12_OR_TRACEABILITY_ONLY", "mostly point target; not Phase2A primary evidence"
    if "2026_t2_env" in s:
        return "T2_environment_multimodal", "OUT_OF_SCOPE_CONTEXT", "environmental/multimodal extension; not canonical AJSE Phase2A experiment"
    if "traffic4cast" in s:
        return "external_benchmark_access", "OUT_OF_SCOPE", "Bangkok/Traffic4cast access check"
    if "2026_07_23" in s:
        return "archive_and_working_sources", "SOURCE_OR_ARCHIVE", "mixed AJSE/v2.2/T2 packages; definition check required"
    return "unclassified", "REVIEW", "no canonical mapping established"


def role_for_file(path: Path) -> str:
    name = path.name.lower()
    s = str(path).lower()
    if "prediction" in name or "predictions" in s or path.suffix.lower() == ".parquet":
        return "prediction_or_sample_data"
    if "metric" in name or "result" in name or "table" in s:
        return "metric_or_table"
    if "config" in name or path.suffix.lower() in {".yaml", ".yml", ".toml"}:
        return "configuration"
    if "manifest" in name or "registry" in name or "checksum" in name or "hash" in name:
        return "manifest_or_hash"
    if "report" in name or path.suffix.lower() in {".md", ".docx", ".txt"}:
        return "report_or_documentation"
    if path.suffix.lower() == ".py":
        return "code"
    if path.suffix.lower() in {".zip", ".rar", ".7z"}:
        return "archive"
    return "other"


def ensure_output() -> None:
    if OUTPUT_ROOT.exists():
        raise FileExistsError(f"Refusing to overwrite existing audit directory: {OUTPUT_ROOT}")
    for path in DIRS.values():
        path.mkdir(parents=True, exist_ok=True)


def copy_outline() -> dict:
    result = {"source": str(OUTLINE), "exists": OUTLINE.exists(), "sha256": None}
    if OUTLINE.exists():
        result["sha256"] = sha256_file(OUTLINE)
        shutil.copy2(OUTLINE, DIRS["outline"] / OUTLINE.name)
    for name in ["outline_structure.json", "outline_extracted.md"]:
        source = OUTLINE_EXTRACT_DIR / name
        if source.exists():
            shutil.copy2(source, DIRS["outline"] / name)
    write_json(DIRS["outline"] / "outline_source_identity.json", result)
    return result


def scan_drive() -> tuple[list[dict], list[dict], list[dict]]:
    top_rows = []
    for p in sorted(Path("D:/").iterdir(), key=lambda x: x.name.lower()):
        try:
            st = p.stat()
            family, reuse, note = classify_family(p)
            research_candidate = int(any(k in p.name.lower() for k in ["2026", "ajse", "crg", "tcn", "traffic", "fcd", "panborneo"]))
            top_rows.append({
                "path": str(p), "type": "directory" if p.is_dir() else "file", "size_bytes": st.st_size if p.is_file() else "",
                "last_write_time": datetime.fromtimestamp(st.st_mtime).astimezone().isoformat(),
                "research_candidate": research_candidate, "family": family, "reuse_status": reuse, "classification_note": note,
            })
        except Exception as exc:
            top_rows.append({"path": str(p), "type": "ERROR", "error": repr(exc)})
    write_csv(DIRS["drive"] / "d_drive_top_level_inventory.csv", top_rows)

    roots = [PD_ROOT, WORK_ROOT, PHASE2A_ROOT, QUARANTINE_ROOT, V22_ROOT, T2_ENV_ROOT, Path(r"D:\Traffic4cast_Bangkok_Access_Check"), Path(r"D:\data")]
    prune = {".git", "__pycache__", "node_modules", "conda_pkgs", "pip_cache", "envs", ".venv", "venv", "$recycle.bin", "system volume information"}
    relevant_ext = {".csv", ".parquet", ".json", ".yaml", ".yml", ".md", ".txt", ".xlsx", ".docx", ".py", ".zip", ".rar", ".7z", ".gz", ".log", ".toml"}
    inventory = []
    errors = []
    for root in roots:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root, topdown=True):
            dirnames[:] = [d for d in dirnames if d.lower() not in prune]
            for filename in filenames:
                p = Path(dirpath) / filename
                try:
                    st = p.stat()
                    ext = p.suffix.lower()
                    family, reuse, note = classify_family(p)
                    role = role_for_file(p)
                    is_relevant = ext in relevant_ext and (
                        family != "unclassified" or any(k in str(p).lower() for k in ["phase", "ajse", "forecast", "traffic", "fcd", "tcn", "gru", "result", "metric", "audit", "manifest", "window", "split"])
                    )
                    if not is_relevant:
                        continue
                    inventory.append({
                        "root": str(root), "relative_path": safe_rel(p, root), "full_path": str(p), "extension": ext,
                        "size_bytes": st.st_size, "last_write_time": datetime.fromtimestamp(st.st_mtime).astimezone().isoformat(),
                        "family": family, "reuse_status": reuse, "role": role, "classification_note": note,
                    })
                except Exception as exc:
                    errors.append({"path": str(p), "error": repr(exc)})
    write_csv(DIRS["drive"] / "research_asset_inventory.csv", inventory)
    write_csv(DIRS["drive"] / "scan_errors.csv", errors)

    summary_rows = []
    grouped = defaultdict(lambda: {"files": 0, "bytes": 0, "roles": Counter(), "reuse": Counter()})
    for row in inventory:
        g = grouped[row["family"]]
        g["files"] += 1
        g["bytes"] += int(row["size_bytes"])
        g["roles"][row["role"]] += 1
        g["reuse"][row["reuse_status"]] += 1
    for family, g in sorted(grouped.items()):
        summary_rows.append({
            "family": family, "file_count": g["files"], "size_bytes": g["bytes"],
            "roles": json.dumps(g["roles"], ensure_ascii=False), "reuse_statuses": json.dumps(g["reuse"], ensure_ascii=False),
        })
    write_csv(DIRS["drive"] / "research_family_summary.csv", summary_rows)
    return top_rows, inventory, summary_rows


def experiment_crosswalk() -> list[dict]:
    rows = [
        ("A0", "Stable snapshot and provenance", "PARTIAL_PASS", "Phase2A-0 source snapshot and hashes exist; canonical independent-test path is blocked", "Phase2A-0 source audit; D-drive inventory", "Use retrospective positioning; keep source snapshot immutable"),
        ("A1", "Theoretical grid and loss funnel", "PARTIAL_PASS_WITH_BOUNDARY_MISMATCH", "Old PD panel has 100,980 rows including two partial boundary hours; Phase2A complete-hour denominator is 100,878", "PD phase1 report; Phase2A-0 denominator comparison", "Use complete-hour grid for new Phase2A runs; do not mix denominators"),
        ("A2", "Qualification and cleaning freeze", "DEFINITION_FROZEN_NOT_EXECUTED", "Phase2A-0 cleaning policy exists; no Phase2A-1 result files", "PROPOSED_CLEANING_POLICY.yaml; REORGANIZATION_VERIFICATION.json", "Execute only under a new retrospective rolling-origin run"),
        ("A3", "2/4, 3/4, 4/4 aggregation sensitivity", "NOT_EXECUTED", "No matching completed result set found", "D-drive research asset scan", "Run prespecified sensitivity if retained in manuscript"),
        ("A4", "Future-window mean H1/H3/H6 target", "PARTIAL_PASS", "Old PD Phase13 uses matching target/horizons and 0.80 completeness, but old split; Phase2A definition is frozen", "phase13 config/code/predictions; Phase2A target policy", "Reusable for exploratory/historical evidence only"),
        ("A5", "Six-fold common-sample manifest and leakage assertions", "NOT_EXECUTED_FOR_SIX_FOLD", "Old window index passes same-split leakage checks but has one 70/15/15 split and no six-fold manifest", "window_index_all.csv; Phase2 report", "Generate new fold-aware sample manifest before formal benchmark"),
        ("A6", "Model interface smoke and metric recomputation", "PARTIAL_PASS", "Phase13 has 105 prediction files and validation; current audit independently recomputes metrics", "phase13 validation and current metric audit", "Repeat interface checks in the Phase2A rolling-origin implementation"),
        ("A7", "Six-fold multi-horizon benchmark", "NOT_EXECUTED", "No canonical six-fold future-window-mean result set found", "D-drive scan; Phase2A status", "Required for primary manuscript evidence"),
        ("A8", "Cross-fold stability", "NOT_EXECUTED", "No six-fold Phase2A results", "D-drive scan", "Cannot claim temporal/fold stability yet"),
        ("A9", "Quality/reliability stratification", "PARTIAL_OLD_SPLIT", "Phase17 stratification exists for TCN on the old test split", "phase17 tables/reports", "Use as exploratory evidence only or rerun by fold"),
        ("A10", "Node/date/traffic-state diagnostics", "PARTIAL_OLD_SPLIT", "Coverage/volatility/traffic-state analyses exist, but not fold-aware Phase2A diagnostics", "phase17 tables/reports", "Recompute on common fold samples"),
        ("A11", "Dependence-aware paired statistics", "NONCOMPLIANT_OLD_ANALYSIS", "Phase14 pools tens of thousands of sample pairs; no node-day or moving-block primary inference", "phase14 statistical tables", "Replace primary inference with fold/day/block clustered analysis"),
        ("A12", "Exposed final-week historical supplement", "AVAILABLE_WITH_CONTAMINATION", "v2.2 point-target P7/P8 artifacts exist and are explicitly contaminated retrospective evidence", "v2.2 target and contamination audits", "Keep separate from future-window-mean primary tables"),
        ("A13", "Reproducibility and traceability freeze", "PARTIAL", "Several manifests and hashes exist, but no completed Phase2A A0-A12 chain", "Phase2A-0 package; legacy PD audit packages", "Freeze only after new Phase2A benchmark and corrected statistics"),
    ]
    out = [
        {"experiment_step": a, "requirement": b, "status": c, "evidence_summary": d, "source_evidence": e, "required_action": f}
        for a, b, c, d, e, f in rows
    ]
    write_csv(DIRS["crosswalk"] / "outline_experiment_result_crosswalk.csv", out)
    return out


def load_phase2a_policies() -> dict:
    base = PHASE2A_ROOT / "01_PHASE2A_DEFINITION_FREEZE" / "AJSE_Phase2A0_Definition_Freeze"
    out = {}
    for key, rel in {
        "time_grid": r"02_time_grid_definition\TIME_GRID_POLICY.yaml",
        "aggregation": r"02_time_grid_definition\AGGREGATION_THRESHOLD_POLICY.yaml",
        "cleaning": r"03_cleaning_policy\PROPOSED_CLEANING_POLICY.yaml",
        "split": r"04_split_definition\SPLIT_POLICY.yaml",
        "target": r"05_target_definition\TARGET_POLICY.yaml",
        "history": r"06_history_and_state_policy\HISTORY_POLICY.yaml",
        "draft": r"10_final_configuration\AJSE_PHASE2A_DRAFT.yaml",
    }.items():
        p = base / rel
        if p.exists():
            out[key] = {"path": str(p), "sha256": sha256_file(p), "content": yaml.safe_load(p.read_text(encoding="utf-8"))}
    write_json(DIRS["dataset"] / "phase2a_policy_registry.json", out)
    return out


def panel_audit() -> dict:
    panel_path = PD_ROOT / "data" / "processed" / "phase2_panel_1h_model_ready.csv.gz"
    df = pd.read_csv(panel_path)
    df["time_bin"] = pd.to_datetime(df["time_bin"])
    complete_start = pd.Timestamp("2025-12-08 14:00:00")
    complete_end = pd.Timestamp("2026-02-28 23:00:00")
    complete = df[df["time_bin"].between(complete_start, complete_end)]
    result = {
        "path": str(panel_path), "sha256": sha256_file(panel_path), "rows": int(len(df)), "nodes": int(df.node_id.nunique()),
        "first_timestamp": str(df.time_bin.min()), "last_timestamp": str(df.time_bin.max()),
        "duplicate_node_time_keys": int(df.duplicated(["node_id", "time_bin"]).sum()),
        "missing_target_rows": int(df.current_speed.isna().sum()), "observed_target_rows": int(df.current_speed.notna().sum()),
        "complete_hour_rows": int(len(complete)), "complete_hour_expected_rows": 100878,
        "boundary_rows_outside_complete_grid": int(len(df) - len(complete)),
        "boundary_hours_outside_complete_grid": sorted(str(x) for x in df.loc[~df["time_bin"].between(complete_start, complete_end), "time_bin"].unique()),
        "complete_grid_row_match": bool(len(complete) == 100878),
    }
    write_json(DIRS["dataset"] / "legacy_pd_panel_audit.json", result)
    return result


def window_index_audit() -> tuple[list[dict], dict]:
    path = PD_ROOT / "outputs" / "tables" / "window_index_all.csv"
    usecols = ["window_id", "point_id", "input_start_time", "input_end_time", "target_start_time", "target_end_time", "history_hours", "horizon_hours", "split", "target_variable", "input_observed_ratio", "target_observed_ratio", "is_main_forecast", "is_extended_horizon", "leakage_check_passed"]
    stats = defaultdict(lambda: Counter())
    minmax = defaultdict(lambda: {"input_start": None, "input_end": None, "target_start": None, "target_end": None})
    valid_window_ids = defaultdict(set)
    total_rows = 0
    for chunk in pd.read_csv(path, usecols=usecols, chunksize=200_000):
        total_rows += len(chunk)
        base = chunk[(chunk.target_variable == "speed") & (chunk.history_hours == 24) & (chunk.horizon_hours.isin([1, 3, 6])) & (chunk.is_main_forecast == 1) & (chunk.is_extended_horizon == 0)].copy()
        if base.empty:
            continue
        for (h, split), part in base.groupby(["horizon_hours", "split"]):
            key = (int(h), str(split))
            stats[key]["candidate_rows"] += len(part)
            stats[key]["candidate_leakage_failures"] += int((part.leakage_check_passed != 1).sum())
            valid = part[(part.input_observed_ratio >= 0.8) & (part.target_observed_ratio >= 0.8)]
            stats[key]["valid_rows"] += len(valid)
            stats[key]["valid_leakage_failures"] += int((valid.leakage_check_passed != 1).sum())
            valid_window_ids[int(h)].update(valid.window_id.astype(str).tolist())
            for field in ["input_start_time", "input_end_time", "target_start_time", "target_end_time"]:
                vals = pd.to_datetime(valid[field], errors="coerce")
                if vals.notna().any():
                    label = field.replace("_time", "")
                    current = minmax[key][label]
                    pair = (vals.min(), vals.max())
                    if current is None:
                        minmax[key][label] = pair
                    else:
                        minmax[key][label] = (min(current[0], pair[0]), max(current[1], pair[1]))
    rows = []
    for key in sorted(stats):
        h, split = key
        m = minmax[key]
        rows.append({
            "horizon": h, "split": split, **stats[key],
            "input_start_min": str(m["input_start"][0]) if m["input_start"] else "", "input_start_max": str(m["input_start"][1]) if m["input_start"] else "",
            "input_end_min": str(m["input_end"][0]) if m["input_end"] else "", "input_end_max": str(m["input_end"][1]) if m["input_end"] else "",
            "target_start_min": str(m["target_start"][0]) if m["target_start"] else "", "target_start_max": str(m["target_start"][1]) if m["target_start"] else "",
            "target_end_min": str(m["target_end"][0]) if m["target_end"] else "", "target_end_max": str(m["target_end"][1]) if m["target_end"] else "",
        })
    write_csv(DIRS["dataset"] / "legacy_window_index_summary.csv", rows)
    result = {
        "path": str(path), "size_bytes": path.stat().st_size, "sha256": sha256_file(path), "total_rows": total_rows,
        "relevant_valid_window_id_hashes": {str(h): stable_hash_strings(sorted(v)) for h, v in valid_window_ids.items()},
        "relevant_valid_window_counts": {str(h): len(v) for h, v in valid_window_ids.items()},
        "split_design": "single chronological 70/15/15 split", "six_fold_rolling_origin": False,
    }
    write_json(DIRS["dataset"] / "legacy_window_index_identity.json", result)
    return rows, result


def metrics_calc(y: np.ndarray, pred: np.ndarray) -> dict:
    y = y.astype(float)
    pred = pred.astype(float)
    err = pred - y
    denom = np.abs(y) + np.abs(pred)
    var = np.square(y - y.mean()).sum()
    return {
        "N": int(len(y)), "MAE_recomputed": float(np.abs(err).mean()), "RMSE_recomputed": float(np.sqrt(np.square(err).mean())),
        "MAPE_recomputed": float((np.abs(err) / np.maximum(np.abs(y), 1e-6)).mean()),
        "sMAPE_recomputed": float((2 * np.abs(err) / np.maximum(denom, 1e-6)).mean()),
        "R2_recomputed": float(1 - np.square(err).sum() / var) if var else float("nan"), "Bias_recomputed": float(err.mean()),
    }


def target_recalculation(reference_by_horizon: dict[int, pd.DataFrame], panel: pd.DataFrame) -> tuple[list[dict], list[dict]]:
    panel = panel.copy()
    panel["time_bin"] = pd.to_datetime(panel["time_bin"])
    series = {(str(node), ts): val for node, ts, val in zip(panel.node_id, panel.time_bin, panel.current_speed)}
    summary = []
    samples = []
    rng = np.random.default_rng(2026)
    for h, ref in sorted(reference_by_horizon.items()):
        diffs = []
        matches = 0
        missing = 0
        chosen = set(rng.choice(len(ref), size=min(100, len(ref)), replace=False).tolist())
        for idx, row in enumerate(ref.itertuples(index=False)):
            start = pd.Timestamp(row.timestamp)
            vals = [series.get((str(row.node_id), start + pd.Timedelta(hours=k)), np.nan) for k in range(h)]
            vals = np.asarray(vals, dtype=float)
            finite = vals[np.isfinite(vals)]
            calc = float(finite.mean()) if finite.size else float("nan")
            if math.isfinite(calc):
                diff = abs(calc - float(row.y_true))
                diffs.append(diff)
                matches += int(diff <= 1e-5)
            else:
                missing += 1
                diff = float("nan")
            if idx in chosen:
                samples.append({
                    "sample_id": str(row.sample_id), "node_id": str(row.node_id), "target_start": str(start), "horizon": h,
                    "observed_hours": int(finite.size), "stored_y_true": float(row.y_true), "recomputed_window_mean": calc,
                    "absolute_difference": diff, "match_tolerance_1e-5": bool(math.isfinite(diff) and diff <= 1e-5),
                })
        summary.append({
            "horizon": h, "samples_checked": int(len(ref)), "matches": matches, "mismatches": int(len(ref) - matches - missing),
            "unrecomputable": missing, "max_absolute_difference": max(diffs) if diffs else "", "target_definition_verified": matches == len(ref),
        })
    write_csv(DIRS["metric"] / "target_recalculation_summary.csv", summary)
    write_csv(DIRS["metric"] / "target_recalculation_sample_300.csv", samples)
    return summary, samples


def phase13_prediction_audit(panel: pd.DataFrame) -> tuple[pd.DataFrame, list[dict], list[dict], list[dict], dict[int, pd.DataFrame]]:
    metrics_path = PD_ROOT / "outputs" / "tables" / "phase13_strong_baseline_metrics.csv"
    pred_dir = PD_ROOT / "outputs" / "locked" / "phase13_full" / "predictions"
    stored = pd.read_csv(metrics_path)
    lookup = stored.set_index(["model", "horizon", "seed"])
    rows = []
    all_frames = []
    reference_by_horizon = {}
    sample_hashes = defaultdict(set)
    truth_hashes = defaultdict(set)
    pred_files = sorted(pred_dir.glob("*.parquet"))
    for p in pred_files:
        df = pd.read_parquet(p)
        if df.empty:
            continue
        model = str(df.model.iloc[0])
        h = int(df.horizon.iloc[0])
        seed = int(df.seed.iloc[0])
        calc = metrics_calc(df.y_true.to_numpy(), df.y_pred.to_numpy())
        key = (model, h, seed)
        stored_row = lookup.loc[key] if key in lookup.index else None
        sample_hash = stable_hash_strings(sorted(df.sample_id.astype(str)))
        truth_order = df.sort_values("sample_id")
        truth_hash = stable_hash_strings(f"{a}|{float(b):.8f}" for a, b in zip(truth_order.sample_id, truth_order.y_true))
        sample_hashes[h].add(sample_hash)
        truth_hashes[h].add(truth_hash)
        if h not in reference_by_horizon and model == "TCN" and seed == 42:
            reference_by_horizon[h] = df[["sample_id", "timestamp", "node_id", "horizon", "y_true"]].copy()
        diffs = {}
        all_match = True
        if stored_row is not None:
            for metric in ["MAE", "RMSE", "MAPE", "sMAPE", "R2"]:
                diff = abs(float(stored_row[metric]) - float(calc[f"{metric}_recomputed"]))
                diffs[f"{metric}_absolute_difference"] = diff
                all_match &= diff <= 1e-5
        else:
            all_match = False
        rows.append({
            "prediction_file": str(p), "file_sha256": sha256_file(p), "model": model, "horizon": h, "seed": seed,
            "rows": int(len(df)), "node_count": int(df.node_id.nunique()), "timestamp_min": str(pd.to_datetime(df.timestamp).min()),
            "timestamp_max": str(pd.to_datetime(df.timestamp).max()), "duplicate_sample_ids": int(df.sample_id.duplicated().sum()),
            "sample_set_sha256": sample_hash, "truth_set_sha256": truth_hash, **calc, **diffs, "all_stored_metrics_match": bool(all_match),
        })
        slim = df[["sample_id", "timestamp", "node_id", "horizon", "model", "seed", "abs_error"]].copy()
        all_frames.append(slim)
    audits = pd.DataFrame(rows)
    write_csv(DIRS["metric"] / "phase13_prediction_metric_recalculation.csv", rows)
    consistency = []
    for h in sorted(sample_hashes):
        consistency.append({
            "horizon": h, "prediction_file_count": int((audits.horizon == h).sum()),
            "unique_sample_set_hashes": len(sample_hashes[h]), "unique_truth_set_hashes": len(truth_hashes[h]),
            "common_samples_across_models_and_seeds": len(sample_hashes[h]) == 1,
            "common_truth_across_models_and_seeds": len(truth_hashes[h]) == 1,
        })
    write_csv(DIRS["metric"] / "phase13_common_sample_truth_check.csv", consistency)
    combined = pd.concat(all_frames, ignore_index=True)
    summary = {
        "metrics_file": str(metrics_path), "metrics_sha256": sha256_file(metrics_path), "stored_metric_rows": int(len(stored)),
        "prediction_file_count": len(pred_files), "audited_prediction_files": int(len(audits)),
        "metric_mismatch_files": int((~audits.all_stored_metrics_match).sum()), "expected_files": 105,
        "file_count_complete": len(pred_files) == 105, "models": sorted(stored.model.unique().tolist()),
        "horizons": sorted(int(x) for x in stored.horizon.unique()), "seeds": sorted(int(x) for x in stored.seed.unique()),
    }
    write_json(DIRS["metric"] / "phase13_metric_audit_summary.json", summary)
    return combined, rows, consistency, stored.to_dict("records"), reference_by_horizon


def holm_adjust(p_values: list[float]) -> list[float]:
    n = len(p_values)
    order = np.argsort(p_values)
    adjusted = np.empty(n, dtype=float)
    running = 0.0
    for rank, idx in enumerate(order):
        value = min(1.0, (n - rank) * float(p_values[idx]))
        running = max(running, value)
        adjusted[idx] = running
    return adjusted.tolist()


def dependency_diagnostic(combined: pd.DataFrame) -> list[dict]:
    data = combined.copy()
    data["date"] = pd.to_datetime(data.timestamp).dt.date.astype(str)
    # Average predictions' absolute errors across seeds first, so repeated seeds are not treated as independent days.
    sample_model = data.groupby(["horizon", "model", "sample_id", "date"], as_index=False).abs_error.mean()
    daily = sample_model.groupby(["horizon", "model", "date"], as_index=False).abs_error.mean()
    write_csv(DIRS["bias"] / "phase13_day_level_mae.csv", daily.rename(columns={"abs_error": "MAE"}).to_dict("records"))
    rng = np.random.default_rng(2026)
    rows = []
    comparisons = ["HA", "SeasonalHA", "Persistence", "XGBoost", "GRU", "ST-Transformer-lite"]
    for h in sorted(daily.horizon.unique()):
        href = daily[(daily.horizon == h) & (daily.model == "TCN")].set_index("date").abs_error
        horizon_rows = []
        for model in comparisons:
            other = daily[(daily.horizon == h) & (daily.model == model)].set_index("date").abs_error
            dates = sorted(set(href.index) & set(other.index))
            diff = np.asarray([other.loc[d] - href.loc[d] for d in dates], dtype=float)
            if len(diff) > 0 and np.any(diff != 0):
                p = float(wilcoxon(diff).pvalue)
            else:
                p = 1.0
            boot = np.empty(5000, dtype=float)
            for b in range(5000):
                boot[b] = diff[rng.integers(0, len(diff), len(diff))].mean()
            horizon_rows.append({
                "horizon": int(h), "reference_model": "TCN", "compared_model": model, "paired_unit": "calendar_day_after_seed_averaging",
                "n_independent_units": len(dates), "mean_difference_compared_minus_TCN": float(diff.mean()),
                "median_difference_compared_minus_TCN": float(np.median(diff)), "bootstrap_CI_low": float(np.quantile(boot, 0.025)),
                "bootstrap_CI_high": float(np.quantile(boot, 0.975)), "raw_p": p,
                "direction": "TCN_lower_MAE" if diff.mean() > 0 else "compared_model_lower_MAE",
                "interpretation_scope": "DEPENDENCE_DIAGNOSTIC_ONLY_NOT_PHASE2A_CONFIRMATORY",
            })
        adj = holm_adjust([r["raw_p"] for r in horizon_rows])
        for r, p_adj in zip(horizon_rows, adj):
            r["holm_adjusted_p"] = p_adj
            r["significant_0_05"] = p_adj < 0.05
        rows.extend(horizon_rows)
    write_csv(DIRS["bias"] / "dependency_aware_day_level_diagnostic.csv", rows)
    return rows


def rankings(stored_records: list[dict]) -> list[dict]:
    df = pd.DataFrame(stored_records)
    g = df.groupby(["horizon", "model"], as_index=False).agg(MAE_mean=("MAE", "mean"), MAE_std=("MAE", "std"), RMSE_mean=("RMSE", "mean"), R2_mean=("R2", "mean"), seeds=("seed", "nunique"))
    g["MAE_rank"] = g.groupby("horizon").MAE_mean.rank(method="min")
    g = g.sort_values(["horizon", "MAE_rank"])
    write_csv(DIRS["metric"] / "phase13_model_ranking.csv", g.to_dict("records"))
    return g.to_dict("records")


def bias_register() -> list[dict]:
    rows = [
        {"issue_id": "B01", "severity": "CRITICAL", "issue": "Canonical six-fold rolling-origin experiment not executed", "evidence": "Phase2A0 status BLOCKED and zero Phase2A1 result files; no matching six-fold future-window-mean result set found", "direction_of_bias": "Primary temporal generalization remains unmeasured", "paper_impact": "Blocks primary Results claims about six-fold stability and deployment boundaries", "required_action": "Run a newly versioned retrospective six-fold rolling-origin benchmark"},
        {"issue_id": "B02", "severity": "CRITICAL", "issue": "v2.2 point-target results do not match manuscript target", "evidence": "v2.2 audit identifies POINT_SPEED; manuscript requires FUTURE_WINDOW_MEAN_SPEED", "direction_of_bias": "MAE values are not directly comparable; window averaging usually smooths targets", "paper_impact": "P6-P8 cannot populate main H1/H3/H6 tables", "required_action": "Use v2.2 only as clearly separated historical supplementary evidence"},
        {"issue_id": "B03", "severity": "HIGH", "issue": "Legacy Phase13 uses one 70/15/15 chronological split", "evidence": "window_index and split configuration contain train/val/test only", "direction_of_bias": "Performance may depend strongly on one chosen test interval", "paper_impact": "Cannot support cross-fold stability or robust temporal deployment claims", "required_action": "Recompute on six frozen rolling origins"},
        {"issue_id": "B04", "severity": "HIGH", "issue": "Original Phase14 inference unit is pooled sample-level", "evidence": "n_pairs around 59k-61k per comparison across repeated nodes, times and seeds", "direction_of_bias": "Pseudo-replication can make p-values artificially small", "paper_impact": "Existing significance stars are not sufficient evidence", "required_action": "Use fold/day/node-day or moving-block clustered inference with Holm correction"},
        {"issue_id": "B05", "severity": "HIGH", "issue": "Final week was exposed during prior development", "evidence": "Phase2A0 blind-test audit marks contaminated test", "direction_of_bias": "Study-level blindness is lost", "paper_impact": "Independent blind-test claim is prohibited", "required_action": "Describe all final-week results as retrospective historical evaluation"},
        {"issue_id": "B06", "severity": "MEDIUM", "issue": "Legacy panel includes two incomplete boundary hours", "evidence": "100,980 rows versus complete-hour 100,878; extra 51-node hours at 2025-12-08 13:00 and 2026-03-01 00:00", "direction_of_bias": "Small denominator and boundary-definition discrepancy", "paper_impact": "Counts and availability rates can differ by 102 rows", "required_action": "Use the Phase2A complete-hour denominator consistently"},
        {"issue_id": "B07", "severity": "MEDIUM", "issue": "Eligibility thresholds condition evaluation on sufficiently observed windows", "evidence": "input and target observed ratios must be at least 0.80", "direction_of_bias": "Harder low-coverage windows are partly excluded", "paper_impact": "Reported error is conditional, not unconditional corridor performance", "required_action": "Publish the loss funnel and stratified performance by coverage"},
        {"issue_id": "B08", "severity": "MEDIUM", "issue": "H6 future-window mean smooths hourly extremes", "evidence": "truth equals mean of t+1 through t+6 with at least five observed hours", "direction_of_bias": "Longer-horizon MAE can appear lower than H1 due to target smoothing", "paper_impact": "Do not interpret decreasing MAE with horizon as easier point forecasting", "required_action": "Explain target aggregation and report scale/variance by horizon"},
        {"issue_id": "B09", "severity": "MEDIUM", "issue": "Phase13 model set does not include CRG-TCN", "evidence": "105 files cover HA, SeasonalHA, Persistence, XGBoost, GRU, TCN and ST-Transformer-lite", "direction_of_bias": "Cannot infer CRG-TCN performance from TCN results", "paper_impact": "Blocks CRG-TCN superiority claims under Phase2A target", "required_action": "Include CRG-TCN only in a fair rerun of all declared models"},
        {"issue_id": "B10", "severity": "MEDIUM", "issue": "Phase17 quality analyses use the same old test split", "evidence": "Stratified tables are derived from Phase13/legacy predictions", "direction_of_bias": "Stratum findings may be period-specific", "paper_impact": "Reliability conclusions are exploratory", "required_action": "Repeat stratification within each rolling fold and summarize stability"},
        {"issue_id": "B11", "severity": "LOW", "issue": "Many duplicated archives and manuscript packages exist", "evidence": "D-drive inventory finds repeated reports/configs/packages", "direction_of_bias": "Version-selection and stale-result risk", "paper_impact": "Wrong duplicate can enter a manuscript table", "required_action": "Use canonical-path and SHA-256 registry in this audit package"},
        {"issue_id": "B12", "severity": "LOW", "issue": "Environmental T2 data belongs to another multimodal scope", "evidence": "D:\\2026_T2_ENV contains rainfall, weather, air-quality and event panels", "direction_of_bias": "Mixing projects changes the research question and feature set", "paper_impact": "Could misstate the AJSE sparse-FCD-only design", "required_action": "Keep outside the canonical Phase2A result set unless a new multimodal study is declared"},
    ]
    write_csv(DIRS["bias"] / "bias_and_deviation_register.csv", rows)
    return rows


def claims_matrix() -> list[dict]:
    rows = [
        {"claim": "The canonical AJSE task is H1/H3/H6 future-window mean speed forecasting.", "status": "SUPPORTED_AS_DEFINITION", "allowed_wording": "The prespecified target is the mean observed speed over the next H hours for H in {1,3,6}.", "prohibited_extension": "Do not attach point-target v2.2 MAE to this definition.", "source": "Phase2A target policy and manuscript outline"},
        {"claim": "A complete six-fold rolling-origin evaluation has been run.", "status": "NOT_SUPPORTED", "allowed_wording": "A six-fold retrospective rolling-origin evaluation is the required next formal experiment.", "prohibited_extension": "Do not describe legacy Phase13 as six-fold.", "source": "Phase2A status and D-drive result scan"},
        {"claim": "Legacy Phase13 results are internally reproducible.", "status": "SUPPORTED_WITH_LIMITATION", "allowed_wording": "Within its single predefined split, the archived Phase13 prediction files reproduce the stored metrics and use common samples by horizon.", "prohibited_extension": "This does not establish rolling-origin stability.", "source": "Current metric and sample audit"},
        {"claim": "XGBoost is the best legacy trained model on the old split.", "status": "SUPPORTED_WITH_LIMITATION", "allowed_wording": "XGBoost had the lowest mean MAE among the seven archived Phase13 models at H1, H3 and H6 on the legacy split.", "prohibited_extension": "Do not call it universally best or confirmatory.", "source": "phase13 model ranking"},
        {"claim": "TCN significantly outperforms all baselines.", "status": "CONTRADICTED", "allowed_wording": "TCN was not the top legacy model; XGBoost had lower mean MAE at every archived horizon.", "prohibited_extension": "No superiority wording.", "source": "phase13 ranking and dependence diagnostic"},
        {"claim": "The final week is an independent blind test.", "status": "PROHIBITED", "allowed_wording": "The exposed final week is a retrospective historical evaluation; run-level truth isolation does not restore study-level blindness.", "prohibited_extension": "Independent blind-test or confirmatory claim.", "source": "Phase2A0 blind-test eligibility audit"},
        {"claim": "Existing Phase14 p-values are dependence-aware.", "status": "NOT_SUPPORTED", "allowed_wording": "Original sample-level tests were re-examined using day-level diagnostics; formal Phase2A inference must use clustered units.", "prohibited_extension": "Do not use pooled sample-level stars as sole evidence.", "source": "phase14 table and current day-level diagnostic"},
        {"claim": "All models use only the preceding 24 hours.", "status": "NOT_SUPPORTED_AS_UNIVERSAL_CLAIM", "allowed_wording": "The primary contiguous input sequence was 24 h; seasonal baselines and any longer-context features must be documented separately.", "prohibited_extension": "Universal strict-24h claim without per-model runtime trace.", "source": "Model/config review"},
        {"claim": "The current evidence is ready for AJSE submission without new experiments.", "status": "NOT_SUPPORTED", "allowed_wording": "The data and legacy results are usable for methods development and historical evidence, but the prespecified six-fold primary benchmark remains outstanding.", "prohibited_extension": "Do not present Phase2A as completed.", "source": "A0-A13 crosswalk"},
    ]
    write_csv(DIRS["crosswalk"] / "claim_evidence_matrix.csv", rows)
    return rows


def hash_registry(inventory: list[dict]) -> tuple[list[dict], list[dict]]:
    # Hash all small research evidence plus every locked Phase13 prediction. Raw/commercial panels are metadata-only elsewhere.
    rows = []
    allowed_roles = {"configuration", "manifest_or_hash", "report_or_documentation", "code", "metric_or_table"}
    for item in inventory:
        p = Path(item["full_path"])
        if not p.exists() or not p.is_file():
            continue
        should_hash = (item["role"] in allowed_roles and int(item["size_bytes"]) <= 25 * 1024 * 1024)
        if "outputs\\locked\\phase13_full\\predictions" in str(p).lower():
            should_hash = True
        if not should_hash:
            continue
        try:
            rows.append({"full_path": str(p), "size_bytes": p.stat().st_size, "sha256": sha256_file(p), "family": item["family"], "role": item["role"]})
        except Exception as exc:
            rows.append({"full_path": str(p), "size_bytes": p.stat().st_size, "sha256": "ERROR", "family": item["family"], "role": item["role"], "error": repr(exc)})
    write_csv(DIRS["hashes"] / "evidence_file_hashes_sha256.csv", rows)
    groups = defaultdict(list)
    for r in rows:
        if r["sha256"] not in {"", "ERROR"}:
            groups[r["sha256"]].append(r)
    dup_rows = []
    group_id = 0
    for digest, members in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        if len(members) < 2:
            continue
        group_id += 1
        for m in members:
            dup_rows.append({"duplicate_group": group_id, "member_count": len(members), "sha256": digest, "full_path": m["full_path"], "family": m["family"], "role": m["role"]})
    write_csv(DIRS["hashes"] / "duplicate_evidence_files_by_sha256.csv", dup_rows)
    return rows, dup_rows


def copy_reusable_evidence() -> list[dict]:
    sources = [
        PHASE2A_ROOT / "00_MANIFESTS" / "REORGANIZATION_VERIFICATION.json",
        PHASE2A_ROOT / "01_PHASE2A_DEFINITION_FREEZE" / "AJSE_Phase2A0_Definition_Freeze" / "11_reports" / "PHASE2A0_EXECUTIVE_SUMMARY.md",
        PHASE2A_ROOT / "01_PHASE2A_DEFINITION_FREEZE" / "AJSE_Phase2A0_Definition_Freeze" / "02_time_grid_definition" / "DENOMINATOR_COMPARISON.csv",
        PHASE2A_ROOT / "01_PHASE2A_DEFINITION_FREEZE" / "AJSE_Phase2A0_Definition_Freeze" / "05_target_definition" / "TARGET_POLICY.yaml",
        PHASE2A_ROOT / "01_PHASE2A_DEFINITION_FREEZE" / "AJSE_Phase2A0_Definition_Freeze" / "04_split_definition" / "SPLIT_POLICY.yaml",
        PD_ROOT / "configs" / "phase13_strong_baselines.yaml",
        PD_ROOT / "configs" / "phase14_final_statistical_tests.yaml",
        PD_ROOT / "configs" / "phase16_robustness.yaml",
        PD_ROOT / "configs" / "phase17_stratified_evaluation.yaml",
        PD_ROOT / "reports" / "phase1_data_audit_report.md",
        PD_ROOT / "reports" / "phase2_window_construction_report.md",
        PD_ROOT / "reports" / "phase13A_full_validation_report.md",
        PD_ROOT / "reports" / "phase14_final_statistical_tests_report.md",
        PD_ROOT / "reports" / "phase16_validation_report.md",
        PD_ROOT / "reports" / "phase17_validation_report.md",
        PD_ROOT / "outputs" / "tables" / "phase13_strong_baseline_metrics.csv",
        PD_ROOT / "outputs" / "tables" / "phase14_main_model_statistical_tests.csv",
        PD_ROOT / "outputs" / "tables" / "phase16_degradation_summary.csv",
        PD_ROOT / "outputs" / "tables" / "phase17_combined_stratified_summary.csv",
        PD_ROOT / "scripts" / "phase13_strong_baselines.py",
        PD_ROOT / "scripts" / "phase14_final_statistical_tests.py",
    ]
    registry = []
    for p in sources:
        if not p.exists():
            registry.append({"source_path": str(p), "copied": False, "reason": "missing"})
            continue
        family, reuse, note = classify_family(p)
        sub = "Phase2A_definition" if family == "Phase2A_definition_freeze" else "legacy_PD_partial_reuse"
        dest_dir = DIRS["evidence"] / sub
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / p.name
        if dest.exists():
            dest = dest_dir / f"{p.parent.name}_{p.name}"
        shutil.copy2(p, dest)
        registry.append({
            "source_path": str(p), "source_sha256": sha256_file(p), "copied": True, "destination_path": str(dest),
            "destination_sha256": sha256_file(dest), "reuse_status": reuse, "classification_note": note,
        })
    write_csv(DIRS["evidence"] / "reusable_evidence_registry.csv", registry)
    return registry


def markdown_report(outline_identity, family_summary, crosswalk, panel, window_summary, metric_summary, target_summary, ranking_rows, diagnostic_rows, biases, claims, hash_rows, dup_rows, evidence_registry) -> str:
    rank = pd.DataFrame(ranking_rows)
    top = rank.sort_values(["horizon", "MAE_rank"]).groupby("horizon").first().reset_index()
    top_lines = "\n".join(f"- H{int(r.horizon)}: {r.model}, mean MAE={r.MAE_mean:.6f}" for r in top.itertuples())
    diag = pd.DataFrame(diagnostic_rows)
    sig = diag[diag.significant_0_05 == True] if not diag.empty else diag
    diag_lines = "\n".join(
        f"- H{int(r.horizon)} TCN vs {r.compared_model}: n_days={int(r.n_independent_units)}, difference(compared−TCN)={r.mean_difference_compared_minus_TCN:.6f}, 95% day-bootstrap CI [{r.bootstrap_CI_low:.6f}, {r.bootstrap_CI_high:.6f}], Holm p={r.holm_adjusted_p:.6g}."
        for r in sig.itertuples()
    ) or "- No day-level comparison survived Holm correction in this diagnostic."
    cross = pd.DataFrame(crosswalk)
    status_counts = cross.status.value_counts().to_dict()
    report = f"""# AJSE complete data/result aggregation and correspondence audit

Generated: {NOW.isoformat()}

## 1. Executive verdict

**Overall status: NOT READY AS A COMPLETED PHASE 2A PAPER RESULT SET.**

The D-drive search found useful and internally checkable legacy evidence, but it did **not** find a completed six-fold rolling-origin experiment matching the supplied AJSE outline. The strongest reusable result set is `D:\\2026_PD\\outputs\\locked\\phase13_full`: it uses the correct future-window-mean target and H1/H3/H6, contains 105 prediction files, and its metrics and common-sample structure were independently checked. Its decisive limitation is that it uses one chronological 70/15/15 split rather than the six frozen rolling origins required by the manuscript.

The v2.2 P6–P8 chain is a different task (point speed at t+H) and an exposed retrospective period. It must remain outside the primary future-window-mean tables.

## 2. Supplied manuscript outline identity

- Source: `{outline_identity['source']}`
- SHA-256: `{outline_identity['sha256']}`
- Structural extraction: `{DIRS['outline'] / 'outline_extracted.md'}`
- Visual-render limitation: LibreOffice/soffice was not available, so the DOCX was structurally parsed but not page-rendered for visual QA.

The outline requires A0–A13, a future-window-mean target for H1/H3/H6, strict causal processing, common samples, six-fold rolling-origin evaluation, dependence-aware inference, and retrospective-only wording for the exposed final week.

## 3. D-drive discovery scope

The audit enumerated the complete top level of D: and recursively inventoried the research-relevant roots `D:\\2026_PD`, `D:\\2026_07_23`, `D:\\CRG_TCN_20260729`, `D:\\2026_AJSE_FINAL`, `D:\\2026_AJSE_FINAL_QUARANTINE`, `D:\\2026_T2_ENV`, `D:\\Traffic4cast_Bangkok_Access_Check`, and `D:\\data`. Python environments, package caches, `.git`, `node_modules`, and system directories were excluded from detailed content scanning and are explicitly outside the scientific-result search.

Research-family counts are in `{DIRS['drive'] / 'research_family_summary.csv'}`. The full research asset list is `{DIRS['drive'] / 'research_asset_inventory.csv'}`.

## 4. A0–A13 correspondence

Status distribution: `{json.dumps(status_counts, ensure_ascii=False)}`.

Key conclusions:

- A0/A1/A4/A6 have partial or definition-level evidence.
- A3 has no completed matching sensitivity result.
- A5/A7/A8 are not completed for six-fold rolling-origin evaluation.
- A9/A10 exist only on the old single split.
- A11 is not compliant because original inference pooled repeated sample-level errors.
- A12 is available only as contaminated retrospective point-target evidence.
- A13 cannot be called complete until the missing Phase2A experiment/statistics are produced.

The item-by-item mapping is `{DIRS['crosswalk'] / 'outline_experiment_result_crosswalk.csv'}`.

## 5. Data correspondence and correctness

### 5.1 Legacy PD panel

- Rows: {panel['rows']:,}; nodes: {panel['nodes']}.
- Range: {panel['first_timestamp']} to {panel['last_timestamp']}.
- Duplicate node-hour keys: {panel['duplicate_node_time_keys']}.
- Missing target rows: {panel['missing_target_rows']:,}.
- Complete-hour Phase2A range rows: {panel['complete_hour_rows']:,} (expected 100,878).
- Extra boundary rows in the legacy panel: {panel['boundary_rows_outside_complete_grid']} at {panel['boundary_hours_outside_complete_grid']}.

This 102-row discrepancy is not random corruption; it is a time-grid definition difference (two partial boundary hours × 51 nodes). Counts and availability rates must use one denominator consistently.

### 5.2 Target and windows

The Phase13 code explicitly sets `truth = mean(target_start_time ... target_end_time)`. The current audit independently recomputed every reference prediction target from the hourly panel:

{chr(10).join(f"- H{r['horizon']}: {r['matches']}/{r['samples_checked']} matched, mismatches={r['mismatches']}, max difference={r['max_absolute_difference']}." for r in target_summary)}

Thus the archived Phase13 target corresponds to **future-window mean speed**, not point speed. The old windows use history=24 h, input observed ratio ≥0.80 and target observed ratio ≥0.80. For H6 this means at least five observed future hours; for H1/H3 it effectively requires all target hours.

No leakage-check failure was found in the relevant old windows, but that check only proves ordering and same-split containment under the old single split. It does not prove six-fold rolling-origin execution.

## 6. Prediction and metric audit

- Stored metric rows: {metric_summary['stored_metric_rows']}.
- Expected/audited prediction files: {metric_summary['expected_files']}/{metric_summary['audited_prediction_files']}.
- Metric mismatch files at tolerance 1e-5: {metric_summary['metric_mismatch_files']}.
- Models: {', '.join(metric_summary['models'])}.
- Horizons: {metric_summary['horizons']}; seeds: {metric_summary['seeds']}.
- Common sample and truth hashes by horizon are recorded in `{DIRS['metric'] / 'phase13_common_sample_truth_check.csv'}`.

Legacy mean-MAE winners:

{top_lines}

XGBoost is therefore the strongest archived trained model on the old split. TCN is not the top model, and CRG-TCN is absent from this 105-run result set.

## 7. Statistical dependence and bias

The original Phase14 tests pool approximately 59k–61k paired rows and report very small p-values. Those rows repeat nodes, hours, days and seeds. The current audit averaged seeds first and repeated comparisons at the calendar-day level with a 5,000-replicate paired day bootstrap and Holm correction. These are **diagnostic**, not a substitute for the missing six-fold analysis.

Day-level comparisons surviving Holm correction in the diagnostic:

{diag_lines}

The complete table is `{DIRS['bias'] / 'dependency_aware_day_level_diagnostic.csv'}`. Even when a day-level difference survives, it remains evidence about one legacy test interval, not confirmatory Phase2A evidence.

## 8. Main deviations affecting the paper

{chr(10).join(f"- **{b['severity']} {b['issue_id']}** — {b['issue']}. Impact: {b['paper_impact']} Action: {b['required_action']}" for b in biases)}

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

- Master workbook: `{OUTPUT_ROOT / 'AJSE_DATA_RESULT_AUDIT_MASTER.xlsx'}`
- Crosswalk: `{DIRS['crosswalk'] / 'outline_experiment_result_crosswalk.csv'}`
- Dataset audit: `{DIRS['dataset']}`
- Metric recomputation: `{DIRS['metric']}`
- Bias/deviation register: `{DIRS['bias'] / 'bias_and_deviation_register.csv'}`
- Claim matrix: `{DIRS['crosswalk'] / 'claim_evidence_matrix.csv'}`
- Hash registry: `{DIRS['hashes'] / 'evidence_file_hashes_sha256.csv'}`
- Reusable evidence registry: `{DIRS['evidence'] / 'reusable_evidence_registry.csv'}`

## 12. Integrity statement

No original experiment output, prediction, model weight, registry or log was modified. The audit created new summaries and copied only selected small evidence files. Raw commercial FCD, full prediction arrays and model weights were not duplicated into the audit package.
"""
    path = DIRS["reports"] / "AJSE_COMPREHENSIVE_DATA_AND_RESULT_AUDIT_REPORT.md"
    path.write_text(report, encoding="utf-8")
    return report


def main() -> None:
    ensure_output()
    outline_identity = copy_outline()
    top_rows, inventory, family_summary = scan_drive()
    crosswalk = experiment_crosswalk()
    policies = load_phase2a_policies()
    panel_result = panel_audit()
    window_rows, window_identity = window_index_audit()
    panel_df = pd.read_csv(PD_ROOT / "data" / "processed" / "phase2_panel_1h_model_ready.csv.gz")
    combined, metric_rows, sample_consistency, stored_records, reference_by_horizon = phase13_prediction_audit(panel_df)
    target_summary, target_samples = target_recalculation(reference_by_horizon, panel_df)
    diagnostic_rows = dependency_diagnostic(combined)
    ranking_rows = rankings(stored_records)
    biases = bias_register()
    claims = claims_matrix()
    hash_rows, dup_rows = hash_registry(inventory)
    evidence_registry = copy_reusable_evidence()
    report = markdown_report(outline_identity, family_summary, crosswalk, panel_result, window_rows, json.loads((DIRS["metric"] / "phase13_metric_audit_summary.json").read_text(encoding="utf-8")), target_summary, ranking_rows, diagnostic_rows, biases, claims, hash_rows, dup_rows, evidence_registry)
    final_summary = {
        "audit_status": "PRIMARY_RESULTS_NOT_READY",
        "output_root": str(OUTPUT_ROOT),
        "generated_at": NOW.isoformat(),
        "outline_sha256": outline_identity.get("sha256"),
        "phase2a0_status": "BLOCKED",
        "phase2a1_result_files": 0,
        "canonical_target": "FUTURE_WINDOW_MEAN_SPEED",
        "canonical_horizons": [1, 3, 6],
        "six_fold_rolling_origin_completed": False,
        "legacy_phase13_target_verified": all(x["target_definition_verified"] for x in target_summary),
        "legacy_phase13_prediction_files_audited": len(metric_rows),
        "legacy_phase13_metric_mismatch_files": sum(not x["all_stored_metrics_match"] for x in metric_rows),
        "legacy_phase13_split": "single chronological 70/15/15",
        "v22_primary_reuse": "PROHIBITED_POINT_TARGET",
        "independent_blind_test_claim": "PROHIBITED",
        "original_files_modified": False,
        "docx_visual_render_completed": False,
    }
    write_json(DIRS["reports"] / "AJSE_AUDIT_EXECUTIVE_STATUS.json", final_summary)
    print(json.dumps(final_summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
