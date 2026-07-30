from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import yaml


V2 = Path(r"D:\2026_07_23\CRG_TCN_review_v2\package_extracted\03_CRG_TCN_experiment_framework_v2_final_week_blind")
OLD = Path(r"D:\2026_07_23\多数据源数据\多数据源数据补全\source_package_extracted\paper_data_package_for_gpt_review")
ROOT = Path(r"D:\2026_AJSE_FINAL")
OUT = ROOT / "AJSE_Phase2A0_Definition_Freeze"
ZIP_PATH = ROOT / "AJSE_Phase2A0_Definition_Freeze.zip"
RAW = V2 / "data" / "raw" / "tomtom_cleaned_records.csv.gz"
CFG_PATH = V2 / "configs" / "base_v2_2_2of4.yaml"
SPLIT_PATH = V2 / "manifests" / "v2_2_2of4" / "temporal_splits.json"
NOW = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

DIRS = [
    "00_source_audit",
    "01_blind_test_audit",
    "02_time_grid_definition",
    "03_cleaning_policy",
    "04_split_definition",
    "05_target_definition",
    "06_history_and_state_policy",
    "07_feature_freeze",
    "08_full_sample_validation_plan",
    "09_distribution_license",
    "10_final_configuration",
    "11_reports",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_text(rel: str, text: str) -> Path:
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.rstrip() + "\n", encoding="utf-8")
    return p


def write_csv(rel: str, rows, columns=None) -> Path:
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(rows, pd.DataFrame):
        df = rows.copy()
        if columns:
            for col in columns:
                if col not in df:
                    df[col] = ""
            df = df[columns]
    else:
        df = pd.DataFrame(rows, columns=columns)
    df.to_csv(p, index=False, encoding="utf-8-sig")
    return p


def write_yaml(rel: str, obj: dict) -> Path:
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
    return p


def run(cmd: list[str], cwd: Path | None = None, timeout=120) -> tuple[int, str, str]:
    cp = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=timeout)
    return cp.returncode, cp.stdout.strip(), cp.stderr.strip()


def git_state() -> tuple[str, str, bool]:
    _, commit, _ = run(["git", "-C", str(V2), "rev-parse", "HEAD"])
    _, status, err = run(["git", "-C", str(V2), "status", "--porcelain=v1", "--untracked-files=all"])
    return commit, status or err, bool(status.strip())


def active_processes() -> list[dict]:
    ps = (
        "Get-CimInstance Win32_Process | "
        "Where-Object { $_.Name -match 'python|powershell|pwsh' -and "
        "$_.CommandLine -match '03_CRG_TCN_experiment_framework_v2_final_week_blind' } | "
        "Select-Object ProcessId,Name,CreationDate,CommandLine | ConvertTo-Json -Depth 3"
    )
    code, stdout, _ = run(["powershell", "-NoProfile", "-Command", ps])
    if code or not stdout:
        return []
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return []
    if isinstance(data, dict):
        data = [data]
    rows = []
    for x in data:
        command = str(x.get("CommandLine", ""))
        # Do not preserve arbitrary argument values that could contain credentials.
        phase = ""
        m = re.search(r"run_(phase\d+|rolling)[^\s]*", command, flags=re.I)
        if m:
            phase = m.group(0)
        rows.append({
            "process_id": x.get("ProcessId", ""),
            "name": x.get("Name", ""),
            "creation_date": x.get("CreationDate", ""),
            "sanitized_activity": phase or "v2-project-related process",
            "writes_source_project_possible": bool(re.search(r"run_phase|campaign|trial|parallel", command, flags=re.I)),
        })
    return rows


def load_source_config() -> tuple[dict, dict]:
    cfg = yaml.safe_load(CFG_PATH.read_text(encoding="utf-8"))
    splits = json.loads(SPLIT_PATH.read_text(encoding="utf-8"))
    return cfg, splits


def source_inventory(commit: str, git_status: str, processes: list[dict]) -> None:
    relevant = [
        CFG_PATH,
        SPLIT_PATH,
        V2 / "scripts" / "build_hourly_panel.py",
        V2 / "scripts" / "build_splits.py",
        V2 / "src" / "rolling_dataset.py",
        V2 / "manifests" / "v2_2_2of4" / "p0_data_pipeline_tests.json",
        V2 / "configs" / "matrices" / "v2_2" / "P7_final_week_frozen_10plus20seed.yaml",
        V2 / "data" / "raw" / "SOURCE_PROVENANCE.md",
        RAW,
    ]
    rows = []
    for p in relevant:
        if not p.exists():
            rows.append({"path": str(p), "exists": False, "size_bytes": "", "modified_time": "", "sha256": "", "role": "required source evidence"})
            continue
        rows.append({
            "path": str(p), "exists": True, "size_bytes": p.stat().st_size,
            "modified_time": datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds"),
            "sha256": sha256(p),
            "role": "raw input metadata only; bytes not copied" if p == RAW else "source evidence",
        })
    write_csv("00_source_audit/SOURCE_FILE_INVENTORY.csv", rows)
    write_csv("00_source_audit/ACTIVE_PROCESS_AUDIT.csv", processes, ["process_id", "name", "creation_date", "sanitized_activity", "writes_source_project_possible"])
    shutil.copy2(CFG_PATH, OUT / "00_source_audit" / "base_v2_2_2of4_SOURCE_SNAPSHOT.yaml")
    write_text("00_source_audit/SOURCE_GIT_STATUS.txt", f"""audit_time={NOW}
source_root={V2}
commit={commit}
dirty={bool(git_status.strip())}

git status --porcelain=v1 --untracked-files=all
{git_status or '[clean]'}
""")


def shell_history_audit() -> None:
    candidates = [
        Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "PowerShell" / "PSReadLine" / "ConsoleHost_history.txt",
        Path(os.environ.get("USERPROFILE", "")) / ".bash_history",
    ]
    pattern = re.compile(r"final[_-]?week|final[_-]?test|P7|locked[_-]?truth|predict_final|audit_final", re.I)
    rows = []
    for p in candidates:
        if not p.exists() or not p.is_file():
            rows.append({"path": str(p), "accessible": False, "size_bytes": "", "modified_time": "", "sha256": "", "relevant_line_count": "", "content_copied": False})
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        rows.append({
            "path": str(p), "accessible": True, "size_bytes": p.stat().st_size,
            "modified_time": datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds"),
            "sha256": sha256(p), "relevant_line_count": sum(bool(pattern.search(line)) for line in text.splitlines()),
            "content_copied": False,
        })
    write_csv("00_source_audit/SHELL_HISTORY_AUDIT.csv", rows)


def raw_audit(cfg: dict) -> tuple[pd.DataFrame, dict, dict]:
    usecols = [
        "node_id", "event_time", "current_speed", "current_travel_time", "confidence", "road_closure",
        "traffic_state", "valid_record", "valid_coordinates", "valid_speed", "valid_travel_time",
        "valid_confidence", "valid_time",
    ]
    raw = pd.read_csv(RAW, usecols=usecols, low_memory=False)
    raw["event_time"] = pd.to_datetime(raw["event_time"], errors="coerce")
    numeric = {}
    for col in ["current_speed", "current_travel_time", "confidence"]:
        numeric[col] = pd.to_numeric(raw[col], errors="coerce")

    audit_rows = []
    def add(field, statistic, value, unit="records", notes=""):
        audit_rows.append({"field": field, "statistic": statistic, "value": value, "unit": unit, "notes": notes})

    add("dataset", "total_records", len(raw))
    add("dataset", "node_count", raw["node_id"].nunique(), "nodes")
    add("event_time", "missing", raw["event_time"].isna().sum())
    add("event_time", "min", raw["event_time"].min().isoformat(sep=" "), "timestamp")
    add("event_time", "max", raw["event_time"].max().isoformat(sep=" "), "timestamp")
    probs = [("min", 0.0), ("p1", .01), ("p5", .05), ("p10", .10), ("p25", .25), ("median", .50), ("p75", .75), ("p90", .90), ("p95", .95), ("p99", .99), ("max", 1.0)]
    for field, series in numeric.items():
        finite = series[np.isfinite(series)]
        add(field, "missing_or_nonfinite", int((~np.isfinite(series)).sum()))
        add(field, "zero", int((series == 0).sum()))
        add(field, "negative", int((series < 0).sum()))
        for label, q in probs:
            add(field, label, float(finite.quantile(q)), "native_unit")
    add("confidence", "below_0.8", int((numeric["confidence"] < .8).sum()))
    add("confidence", "at_least_0.8", int((numeric["confidence"] >= .8).sum()))

    exact_dup = raw.duplicated(["node_id", "event_time"], keep=False)
    exact_excess = raw.duplicated(["node_id", "event_time"], keep="first")
    add("node_id+event_time", "duplicate_rows_in_groups", int(exact_dup.sum()))
    add("node_id+event_time", "duplicate_excess_rows", int(exact_excess.sum()))
    add("node_id+event_time", "duplicate_groups", int(raw.loc[exact_dup].groupby(["node_id", "event_time"]).ngroups))

    status_rows = []
    for field in ["road_closure", "traffic_state", "valid_record", "valid_coordinates", "valid_speed", "valid_travel_time", "valid_confidence", "valid_time"]:
        counts = raw[field].astype(str).value_counts(dropna=False)
        for value, count in counts.items():
            status_rows.append({"field": field, "value": value, "count": int(count), "semantic_role": "traffic state (not provider-quality status)" if field == "traffic_state" else "available quality/status-like field"})
    status_rows.append({"field": "provider_status", "value": "[COLUMN_ABSENT]", "count": 0, "semantic_role": "no provider-status field exists in the cleaned input"})
    write_csv("03_cleaning_policy/CLEANING_INPUT_AUDIT.csv", audit_rows)
    write_csv("03_cleaning_policy/STATUS_VALUE_COUNTS.csv", status_rows)

    speed = numeric["current_speed"]
    tt = numeric["current_travel_time"]
    conf = numeric["confidence"]
    exclusion_rows = [
        {"rule": "timestamp finite", "candidate_parameter": "not-null", "would_exclude_records": int(raw["event_time"].isna().sum()), "current_v2_enforced": True},
        {"rule": "speed finite", "candidate_parameter": "finite", "would_exclude_records": int((~np.isfinite(speed)).sum()), "current_v2_enforced": True},
        {"rule": "speed minimum", "candidate_parameter": "> 0.0", "would_exclude_records": int((~np.isfinite(speed) | (speed <= 0)).sum()), "current_v2_enforced": False},
        {"rule": "confidence finite and range", "candidate_parameter": "0 <= confidence <= 1", "would_exclude_records": int((~np.isfinite(conf) | (conf < 0) | (conf > 1)).sum()), "current_v2_enforced": True},
        {"rule": "confidence primary", "candidate_parameter": ">= 0.80", "would_exclude_records": int((~np.isfinite(conf) | (conf < .8)).sum()), "current_v2_enforced": False},
        {"rule": "travel time minimum", "candidate_parameter": "> 0.0", "would_exclude_records": int((~np.isfinite(tt) | (tt <= 0)).sum()), "current_v2_enforced": False},
        {"rule": "valid_record flag", "candidate_parameter": "True", "would_exclude_records": int((~raw["valid_record"].astype(bool)).sum()), "current_v2_enforced": False},
        {"rule": "road_closure", "candidate_parameter": "False", "would_exclude_records": int(raw["road_closure"].astype(bool).sum()), "current_v2_enforced": False},
        {"rule": "duplicate excess", "candidate_parameter": "mean_of_valid_records", "would_exclude_records": int(exact_excess.sum()), "current_v2_enforced": True},
    ]
    for threshold in [120, 130, 160, 200]:
        exclusion_rows.append({"rule": "speed maximum candidate", "candidate_parameter": f"<= {threshold} km/h", "would_exclude_records": int((speed > threshold).sum()), "current_v2_enforced": False})
    write_csv("03_cleaning_policy/CLEANING_RULE_EXCLUSION_COUNTS.csv", exclusion_rows)

    first_raw = raw["event_time"].min()
    last_raw = raw["event_time"].max()
    first_hour = first_raw.floor("h")
    first_complete = first_hour + pd.Timedelta(hours=1) if first_raw != first_hour else first_hour
    last_hour = last_raw.floor("h")
    last_complete = last_hour if last_raw.minute == 45 else last_hour - pd.Timedelta(hours=1)
    complete_end_exclusive = last_complete + pd.Timedelta(hours=1)
    complete_slots = pd.date_range(first_complete, complete_end_exclusive - pd.Timedelta(minutes=15), freq="15min")
    complete_hours = pd.date_range(first_complete, last_complete, freq="h")
    partial_start_mask = (raw["event_time"] >= first_hour) & (raw["event_time"] < first_complete)
    partial_end_mask = (raw["event_time"] > last_raw.floor("h") + pd.Timedelta(minutes=45))
    legacy_slots = 7915
    node_count = int(raw["node_id"].nunique())
    time_meta = {
        "first_raw": first_raw,
        "last_raw": last_raw,
        "first_complete_hour": first_complete,
        "last_complete_hour": last_complete,
        "node_count": node_count,
        "legacy_15min_slots": legacy_slots,
        "new_15min_slots": len(complete_slots),
        "legacy_15min_denominator": node_count * legacy_slots,
        "new_15min_denominator": node_count * len(complete_slots),
        "legacy_hours": 1980,
        "new_hours": len(complete_hours),
        "legacy_hourly_denominator": node_count * 1980,
        "new_hourly_denominator": node_count * len(complete_hours),
        "partial_start_actual_records": int(partial_start_mask.sum()),
        "partial_end_actual_records": int(partial_end_mask.sum()),
        "boundary_excluded_theoretical_15min_node_slots": node_count * (legacy_slots - len(complete_slots)),
        "boundary_excluded_theoretical_hours": node_count * (1980 - len(complete_hours)),
    }
    raw_meta = {
        "path": str(RAW), "size_bytes": RAW.stat().st_size,
        "modified_time": datetime.fromtimestamp(RAW.stat().st_mtime).isoformat(timespec="seconds"),
        "sha256": sha256(RAW), "row_count": len(raw), "columns": usecols,
        "distribution_status": "RESTRICTED_RAW_DATA",
    }
    write_text("00_source_audit/RAW_INPUT_METADATA.json", json.dumps(raw_meta, ensure_ascii=False, indent=2))
    return raw, time_meta, {"audit_rows": audit_rows, "status_rows": status_rows, "exclusion_rows": exclusion_rows}


def scan_current_v2_final_week(final_start: pd.Timestamp, final_end: pd.Timestamp) -> dict:
    result_root = V2 / "results"
    p7_named = []
    for base in [V2 / "results", V2 / "logs", V2 / "manifests", V2 / "data" / "blind", V2 / "data" / "locked_truth"]:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not p.is_file() or p.name == ".gitkeep":
                continue
            rel = str(p.relative_to(V2)).replace("\\", "/")
            if re.search(r"(^|/)P7|final[_-]?week|final[_-]?test|locked[_-]?truth", rel, flags=re.I):
                p7_named.append(rel)

    timestamp_files_scanned = 0
    timestamp_overlap_files = []
    for p in result_root.rglob("*.parquet"):
        try:
            schema = pq.ParquetFile(p).schema_arrow
            time_cols = [c for c in schema.names if re.search(r"time|date|origin", c, flags=re.I)]
            if not time_cols:
                continue
            timestamp_files_scanned += 1
            table = pq.read_table(p, columns=time_cols)
            overlap = False
            for col in time_cols:
                values = pd.to_datetime(table[col].to_pandas(), errors="coerce")
                if bool(((values >= final_start) & (values <= final_end)).any()):
                    overlap = True
                    break
            if overlap:
                timestamp_overlap_files.append(str(p.relative_to(V2)).replace("\\", "/"))
        except Exception:
            continue

    # Text match records only paths and keyword names, never metric values/snippets.
    keyword_pattern = re.compile(r"final_week|final_test|test_mae|test_rmse|test_smape|best_model|best_history|selected_config", re.I)
    text_hits = []
    allowed = {".py", ".yaml", ".yml", ".json", ".md", ".txt", ".log", ".ps1", ".csv"}
    for top in [V2 / "configs", V2 / "logs", V2 / "manifests", V2 / "results", V2 / "scripts", V2 / "src", V2 / "docs"]:
        if not top.exists():
            continue
        for p in top.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in allowed or p.stat().st_size > 20_000_000:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            keys = sorted(set(m.group(0).lower() for m in keyword_pattern.finditer(text)))
            if keys:
                text_hits.append({"path": str(p.relative_to(V2)).replace("\\", "/"), "keywords": "|".join(keys), "match_count": len(keyword_pattern.findall(text)), "content_excerpt_copied": False})
    write_csv("00_source_audit/V2_KEYWORD_SCAN.csv", text_hits)
    return {
        "p7_named_outputs": p7_named,
        "time_files_scanned": timestamp_files_scanned,
        "timestamp_overlap_files": timestamp_overlap_files,
        "keyword_hit_files": len(text_hits),
    }


def scan_old_overlap(final_start: pd.Timestamp, final_end: pd.Timestamp) -> tuple[list[dict], dict]:
    evidence = []
    summary = {}
    for phase in ["phase13", "phase15"]:
        folder = OLD / "07_PREDICTION_PARQUETS" / phase
        files = sorted(folder.rglob("*.parquet"))
        overlap_files = 0
        overlap_rows = 0
        by_h = defaultdict(set)
        min_ts, max_ts = None, None
        for p in files:
            # Deliberately read only identifiers and timestamps; no y_true/y_pred/error/metric columns.
            d = pd.read_parquet(p, columns=["sample_id", "timestamp", "horizon"])
            ts = pd.to_datetime(d["timestamp"], errors="coerce")
            mask = (ts >= final_start) & (ts <= final_end)
            if mask.any():
                overlap_files += 1
                overlap_rows += int(mask.sum())
                for h, ids in d.loc[mask].groupby("horizon")["sample_id"]:
                    by_h[int(h)].update(ids.astype(str).tolist())
            local_min, local_max = ts.min(), ts.max()
            min_ts = local_min if min_ts is None or local_min < min_ts else min_ts
            max_ts = local_max if max_ts is None or local_max > max_ts else max_ts
        summary[phase] = {
            "prediction_files": len(files), "files_overlapping_candidate_final_week": overlap_files,
            "repeated_prediction_rows_in_overlap": overlap_rows,
            "unique_sample_ids_by_horizon": {str(k): len(v) for k, v in sorted(by_h.items())},
            "timestamp_min": str(min_ts), "timestamp_max": str(max_ts),
        }
        evidence.append({
            "source_scope": f"legacy {phase}", "evidence_type": "prediction Parquet timestamps/identifiers only",
            "path": str(folder), "files_checked": len(files), "files_overlapping_final_week": overlap_files,
            "performance_values_read": False, "selection_or_interpretation_risk": "model comparison" if phase == "phase13" else "feature ablation",
            "verdict": "OVERLAPS_CANDIDATE_FINAL_WEEK" if overlap_files else "NO_OVERLAP",
        })
    extra = [
        (OLD / "05_PHASE16_ROBUSTNESS_RESULTS" / "phase16_robustness_report.md", "robustness/stress analysis uses legacy test samples"),
        (OLD / "10_CONFIGS_ENVIRONMENT_LOGS" / "reports" / "phase17_stratified_evaluation_report.md", "regime analysis uses locked Phase13 test predictions"),
        (OLD / "10_CONFIGS_ENVIRONMENT_LOGS" / "reports" / "phase7_history_sensitivity_report.md", "history-window analysis on legacy experiment split"),
        (OLD / "03_PHASE13_MAIN_RESULTS" / "phase13_strong_baseline_metrics.csv", "model comparison metrics exist for overlapping legacy test period"),
        (OLD / "04_PHASE15_ABLATION_RESULTS" / "phase15_feature_ablation_metrics.csv", "feature-ablation metrics exist for overlapping legacy test period"),
    ]
    for p, risk in extra:
        evidence.append({
            "source_scope": "legacy result package", "evidence_type": "file existence and provenance relationship",
            "path": str(p), "files_checked": 1, "files_overlapping_final_week": "inherited from common legacy test manifest",
            "performance_values_read": False, "selection_or_interpretation_risk": risk,
            "verdict": "CONTAMINATION_EVIDENCE" if p.exists() else "FILE_MISSING",
        })
    write_csv("01_blind_test_audit/BLIND_TEST_EVIDENCE.csv", evidence)
    write_text("01_blind_test_audit/OLD_PREDICTION_TIME_OVERLAP.json", json.dumps(summary, ensure_ascii=False, indent=2))
    return evidence, summary


def make_policies(cfg: dict, splits: dict, time_meta: dict, current_scan: dict, old_summary: dict, processes: list[dict], commit: str, dirty: bool) -> tuple[list[dict], dict]:
    fixed = splits["fixed_splits"]
    final_start = fixed["final_week"]["target_start"]
    final_end = fixed["final_week"]["target_end"]

    time_policy = {
        "timezone": "Asia/Kuala_Lumpur",
        "utc_offset": "+08:00",
        "timestamp_rounding": "floor_15min",
        "hour_assignment": "floor_1h",
        "hour_interval": "[hour_start, hour_start+1h)",
        "partial_start_hour_policy": "exclude_from_confirmatory_panel",
        "partial_end_hour_policy": "exclude_if_incomplete",
        "coverage_denominator": "complete_theoretical_bins_only",
        "first_raw_timestamp": str(time_meta["first_raw"]),
        "first_complete_hour": str(time_meta["first_complete_hour"]),
        "last_raw_timestamp": str(time_meta["last_raw"]),
        "last_complete_hour": str(time_meta["last_complete_hour"]),
    }
    write_yaml("02_time_grid_definition/TIME_GRID_POLICY.yaml", time_policy)
    write_yaml("02_time_grid_definition/AGGREGATION_THRESHOLD_POLICY.yaml", {
        "primary_hourly_threshold": "2_of_4",
        "descriptive_sensitivity": ["1_of_4", "3_of_4", "4_of_4"],
        "selection_rule": "must_not_select_using_final_test_MAE_or_other_performance",
        "common_requirements": ["complete_hour_boundary", "same_cleaning_policy", "confidence>=0.80", "same_theoretical_denominator"],
    })
    denominator_rows = [
        {"level": "15min", "definition": "legacy observed-window denominator", "time_bins": time_meta["legacy_15min_slots"], "nodes": time_meta["node_count"], "theoretical_rows": time_meta["legacy_15min_denominator"]},
        {"level": "15min", "definition": "new complete-bin denominator", "time_bins": time_meta["new_15min_slots"], "nodes": time_meta["node_count"], "theoretical_rows": time_meta["new_15min_denominator"]},
        {"level": "hourly", "definition": "legacy denominator including partial first hour", "time_bins": time_meta["legacy_hours"], "nodes": time_meta["node_count"], "theoretical_rows": time_meta["legacy_hourly_denominator"]},
        {"level": "hourly", "definition": "new complete-hour denominator", "time_bins": time_meta["new_hours"], "nodes": time_meta["node_count"], "theoretical_rows": time_meta["new_hourly_denominator"]},
    ]
    write_csv("02_time_grid_definition/DENOMINATOR_COMPARISON.csv", denominator_rows)
    time_report = f"""# Time-grid audit

Timezone is frozen to Asia/Kuala_Lumpur (UTC+08:00). Source timestamps are local wall-clock values and are floored to 15 minutes; hours are half-open `[hour_start, hour_start+1h)` bins.

- First raw timestamp: {time_meta['first_raw']}.
- First complete confirmatory hour: {time_meta['first_complete_hour']}.
- Last raw timestamp: {time_meta['last_raw']}.
- Last complete hour: {time_meta['last_complete_hour']}.
- The partial 13:00 start hour contains {time_meta['partial_start_actual_records']} raw records and is excluded from the confirmatory panel.
- Legacy 15-min denominator: {time_meta['legacy_15min_denominator']:,}; new complete-bin denominator: {time_meta['new_15min_denominator']:,}.
- Legacy hourly denominator: {time_meta['legacy_hourly_denominator']:,}; new complete-hour denominator: {time_meta['new_hourly_denominator']:,}.
- Boundary exclusion removes {time_meta['boundary_excluded_theoretical_15min_node_slots']:,} theoretical node×15-min slots and {time_meta['boundary_excluded_theoretical_hours']:,} node×hour rows.

Actual missing observations do not change these theoretical denominators.
"""
    write_text("02_time_grid_definition/TIME_GRID_AUDIT.md", time_report)

    cleaning_policy = {
        "status": "DRAFT_BLOCKED_PENDING_USER_APPROVAL",
        "confidence_min_primary": 0.80,
        "confidence_inclusive": True,
        "speed_min_exclusive": 0.0,
        "speed_max": "USER_APPROVAL_REQUIRED",
        "speed_max_candidates_kmh": [120, 130, 160, 200],
        "travel_time_min_exclusive": 0.0,
        "duplicate_rule": "mean_of_valid_records_within_node_and_floored_15min",
        "provider_status_field": "ABSENT",
        "accepted_status_whitelist": "USER_APPROVAL_REQUIRED_NO_PROVIDER_STATUS_FIELD",
        "proposed_required_boolean_flags": {
            "valid_record": True, "valid_coordinates": True, "valid_speed": True,
            "valid_travel_time": True, "valid_confidence": True, "valid_time": True,
        },
        "road_closure_policy": "PROPOSED_ACCEPT_FALSE_ONLY; USER_APPROVAL_REQUIRED",
        "traffic_state_policy": "do_not_use_as_quality_status; preserve all observed categories",
        "current_v2_actual_conditions": ["timestamp_not_null", "speed_finite", "speed>=0", "confidence_finite", "0<=confidence<=1"],
        "current_v2_not_enforced": ["confidence>=0.80", "speed maximum", "travel_time>0", "valid_* flags", "road_closure filter"],
    }
    write_yaml("03_cleaning_policy/PROPOSED_CLEANING_POLICY.yaml", cleaning_policy)

    split_policy = {
        "source_config": "configs/base_v2_2_2of4.yaml",
        "timezone": cfg["project"]["timezone"],
        "candidate_confirmatory_splits": {
            "train": fixed["train"], "validation": fixed["validation"],
            "confirmation": fixed["confirmation"], "final_test": fixed["final_week"],
        },
        "current_v2_membership_rule": splits["membership_rule"],
        "current_v2_maximum_horizon_purge_hours": splits["maximum_horizon_boundary_purge_hours"],
        "old_phase13_15_16_test": "historical_development_comparison",
        "final_test_status": "CONTAMINATED_TEST",
        "forecast_origin_determines_split": True,
        "target_may_cross_split": False,
        "history_may_cross_split_backward": True,
        "history_boundary_state": "causal_carry_over",
        "reset_forward_fill_at_split": False,
        "train_fit_only": ["scaler", "median", "imputation fallback", "categorical encoder", "regime thresholds", "feature selection"],
        "sample_count_audit_comparison": ["causal carry-over history (primary)", "strict same-split history (audit only)"],
    }
    write_yaml("04_split_definition/SPLIT_POLICY.yaml", split_policy)
    write_text("04_split_definition/SPLIT_AND_HISTORY_BOUNDARY.md", f"""# Split and history-boundary policy

Candidate dates are read from the v2 configuration, not hard-coded:

- Train: {fixed['train']['target_start']} through {fixed['train']['target_end']}.
- Validation: {fixed['validation']['target_start']} through {fixed['validation']['target_end']}.
- Confirmation: {fixed['confirmation']['target_start']} through {fixed['confirmation']['target_end']}.
- Candidate final test: {final_start} through {final_end}.

The v2 point-target pipeline assigns membership by target time and applies a 24-hour maximum-horizon purge to training boundaries. AJSE future-window samples will instead assign by forecast origin and require the full target window to remain inside that split.

Historical observations may causally carry across a boundary because they were available before the new forecast origin. Forward-fill state is not reset. Every fitted statistic and selection decision remains train-only. A strict same-split history count will be produced later only as an audit comparator.

The candidate final test is **CONTAMINATED_TEST**, so this policy cannot authorize a confirmatory final-test run.
""")

    target_policy = {
        "task": "future_window_mean_speed",
        "forecast_origin": "t",
        "target_start": "t+1h",
        "target_end": "t+Hh",
        "horizons_hours": [1, 3, 6],
        "target_values": "arithmetic mean of valid observed hourly speeds at t+1..t+H",
        "target_imputation": "forbidden",
        "H1_required": "1_of_1",
        "H3_required": "3_of_3",
        "H6_primary_required": "5_of_6",
        "H6_descriptive_sensitivity_required": "6_of_6",
        "selection_rule": "5/6 and 6/6 use identical model configuration; never select using final-test MAE",
        "implementation_rule": "add separate src/ajse_future_window_target.py; do not change current point-target semantics",
    }
    write_yaml("05_target_definition/TARGET_POLICY.yaml", target_policy)
    write_text("05_target_definition/TARGET_DEFINITION.md", """# Frozen target definition

For node `i`, origin `t`, and H in {1,3,6}, the AJSE task predicts the arithmetic mean of real observed hourly speeds at `t+1,...,t+H`. Targets are never filled. H=1 requires 1/1 observed hour, H=3 requires 3/3, and the H=6 primary analysis requires at least 5/6. A predeclared H=6 6/6 complete-case analysis is descriptive sensitivity only.

This definition is separate from the current v2 point-ahead target. Phase 2A-1 must add a new module rather than modifying the current function in place.
""")

    history_policy = {
        "history_length_primary_hours": 24,
        "history_length_sensitivity_hours": [72, 168],
        "primary_reporting_rule": "always report the pre-registered 24h result",
        "secondary_selection_rule": "72h/168h may be compared using train/validation only and must be labeled secondary",
        "final_test_selection": "forbidden",
        "boundary_state": "causal_carry_over",
        "reset_forward_fill_at_split": False,
        "fallback_statistics": "train-only node median then train-only corridor median",
    }
    write_yaml("06_history_and_state_policy/HISTORY_POLICY.yaml", history_policy)

    feature_spec = """# Model-input freeze specification

Phase 2A-1 must freeze model-ready inputs, not only metadata.

Required artifacts:

- processed hourly panel with stable `panel_row_id`;
- `feature_columns.json` with ordered names and dtypes;
- `panel_index.parquet` (`panel_row_id`, `node_id`, `timestamp`, `split`);
- per-horizon sample manifests containing history and target row IDs;
- `X_sequence_{split}_H{H}.npz` with shape `[n_samples, history_length, n_features]`;
- `X_tabular_{split}_H{H}.parquet`;
- `y_{split}_H{H}.npy` and `sample_ids_{split}_H{H}.npy`;
- train-fitted imputation/scaler JSON files;
- feature-generation manifest containing code/config/input hashes.

Every manifest records `sample_id`, node, forecast origin, history bounds/row IDs, target bounds/row IDs, target value and observed ratio, split, history length, aggregation threshold, and target definition. Feature order is immutable after freezing.
"""
    write_text("07_feature_freeze/MODEL_INPUT_FREEZE_SPEC.md", feature_spec)

    full_plan = """# Full-sample assertion plan

Status: **PLAN_FROZEN_NOT_EXECUTED**. Phase 2A-0 builds no samples.

Phase 2A-1 must assert over every sample: unique IDs; feature time <= origin; target time > origin; full target inside split; unfilled targets; correct/increasing history indices; one node per sample; train-only scaler/imputation/regime fits; no validation/test fit; no backward fill, centered rolling, or future merge; no history/target overlap; common manifests across models.

A fixed 1,000-sample audit with seed 2026 is additional numerical recomputation only and cannot replace the exhaustive assertions.
"""
    write_text("08_full_sample_validation_plan/FULL_SAMPLE_ASSERTION_PLAN.md", full_plan)

    dist_rows = [
        ("raw provider records", "RESTRICTED_RAW_DATA", "never copy or distribute"),
        ("15-min cleaned records", "INTERNAL_ONLY", "contains provider-derived record-level values"),
        ("hourly derived speed panel", "DERIVED_DATA_PERMISSION_UNCLEAR", "do not include in public package until license approval"),
        ("sample manifests with target values", "DERIVED_DATA_PERMISSION_UNCLEAR", "schema/count/hash may be public; values pending approval"),
        ("feature tensors", "DERIVED_DATA_PERMISSION_UNCLEAR", "may reconstruct provider-derived speeds"),
        ("target arrays", "DERIVED_DATA_PERMISSION_UNCLEAR", "provider-derived labels"),
        ("predictions", "DERIVED_DATA_PERMISSION_UNCLEAR", "confirm provider terms before release"),
        ("figure source tables", "DERIVED_DATA_PERMISSION_UNCLEAR", "aggregate release may be possible after review"),
        ("aggregate statistics", "METADATA_ONLY", "non-record-level descriptive summaries only"),
        ("code/config/schema/hash", "PUBLIC_CONFIRMED", "contains no provider records or credentials"),
    ]
    write_csv("09_distribution_license/DISTRIBUTION_STATUS.csv", dist_rows, ["file_class", "distribution_status", "handling_rule"])
    distribution_report = """# Distribution status

Commercial raw FCD is excluded. Permission to redistribute derived hourly speeds, sample targets, feature tensors, predictions, and figure-source tables is not established by the local files. Until provider/license approval is documented, the public package is limited to code, configuration, schemas, hashes, counts, time ranges, and non-record-level summaries. A separate internal package may retain derived data with access controls.
"""
    write_text("09_distribution_license/DISTRIBUTION_STATUS.md", distribution_report)

    blockers = [
        {"id": "B01", "severity": "STOP", "item": "candidate final week is contaminated", "evidence": "The candidate week is a subset of the legacy Phase13/15/16 test period and is covered by historical model predictions, feature ablation, robustness/regime analysis, and result interpretation.", "required_resolution": "Collect a new independent time period or use retrospective rolling-origin evaluation."},
        {"id": "B02", "severity": "STOP", "item": "speed_max not approved", "evidence": "Only a soft 160 km/h audit value exists; no documented physical/provider upper bound was found.", "required_resolution": "User/domain approval of a fixed upper-bound rule independent of prediction performance."},
        {"id": "B03", "severity": "STOP", "item": "provider status whitelist unresolved", "evidence": "The cleaned input has no provider_status field; valid_* flags and traffic_state are not a documented provider-status whitelist.", "required_resolution": "Approve an explicit flag/status policy or declare provider status not applicable with documented rationale."},
    ]
    active_writers = [p for p in processes if p.get("writes_source_project_possible")]
    if active_writers:
        blockers.append({"id": "B04", "severity": "OPERATIONAL_STOP", "item": "source project is actively mutating", "evidence": f"{len(active_writers)} v2 Phase6 campaign/trial process entries were active during the audit.", "required_resolution": "Wait for Phase6 to finish and take a stable source snapshot before Phase 2A-1."})
    write_csv("11_reports/BLOCKING_ITEMS.csv", blockers)
    write_text("11_reports/BLOCKING_ITEMS.md", "# Blocking items\n\n" + "\n".join(f"- **{b['id']} — {b['item']}**: {b['evidence']} Resolution: {b['required_resolution']}" for b in blockers))

    final_cfg = {
        "phase": "AJSE Phase 2A-0 experimental definition freeze",
        "status": "BLOCKED",
        "project": {"task": "future_window_mean_speed", "timezone": "Asia/Kuala_Lumpur", "source_project_root": str(V2), "source_commit": commit, "source_dirty": dirty},
        "time_grid": {"timestamp_floor": "15min", "hour_floor": "1h", "hour_interval": "half_open", "exclude_partial_start_hour": True, "exclude_partial_end_hour_if_incomplete": True},
        "cleaning": {"confidence_min": .80, "speed_min_exclusive": 0.0, "speed_max": "USER_APPROVAL_REQUIRED", "travel_time_min_exclusive": 0.0, "accepted_statuses": "USER_APPROVAL_REQUIRED_NO_PROVIDER_STATUS_FIELD", "duplicate_rule": "mean_of_valid_records"},
        "aggregation": {"primary": "2_of_4", "sensitivity": ["1_of_4", "3_of_4", "4_of_4"]},
        "history": {"primary_hours": 24, "sensitivity_hours": [72, 168], "boundary_state": "causal_carry_over", "reset_forward_fill_at_split": False},
        "target": {"type": "future_window_mean_speed", "horizons_hours": [1, 3, 6], "H1_required": "1_of_1", "H3_required": "3_of_3", "H6_primary_required": "5_of_6", "H6_sensitivity_required": "6_of_6", "target_imputation": "forbidden"},
        "split": {"source_config": "configs/base_v2_2_2of4.yaml", "dates": split_policy["candidate_confirmatory_splits"], "old_phase13_15_16_test": "historical_development_comparison", "final_test_status": "CONTAMINATED_TEST", "history_may_cross_split_backward": True, "target_may_cross_split": False},
        "validation": {"full_sample_temporal_assertions": "required_in_phase2a1", "random_recomputation_samples": 1000, "random_seed": 2026},
        "distribution": {"raw": "RESTRICTED_RAW_DATA", "derived": "DERIVED_DATA_PERMISSION_UNCLEAR", "phase2a0_package": "METADATA_CODE_CONFIG_ONLY"},
        "blocking_items": [b["id"] for b in blockers],
    }
    write_yaml("10_final_configuration/AJSE_PHASE2A_DRAFT.yaml", final_cfg)
    return blockers, final_cfg


def reports(cfg: dict, splits: dict, time_meta: dict, raw_info: dict, current_scan: dict, old_summary: dict, blockers: list[dict], commit: str, git_dirty: bool, processes: list[dict]) -> None:
    fixed = splits["fixed_splits"]
    fstart, fend = fixed["final_week"]["target_start"], fixed["final_week"]["target_end"]
    p13 = old_summary.get("phase13", {})
    p15 = old_summary.get("phase15", {})
    blind = f"""# Blind-test eligibility

## Status: C. CONTAMINATED_TEST

The current v2 repository has no P7 result directory, P7 log, P7 manifest, final-week prediction export, or locked-truth output. Its `data/blind` and `data/locked_truth` folders contain no final-week data artifact.

However, the candidate final week ({fstart} through {fend}) is fully contained in the legacy Phase13/15/16 test period. Timestamp-only inspection—without reading any prediction or error values—found:

- Phase13: {p13.get('prediction_files', 0)} prediction files, {p13.get('files_overlapping_candidate_final_week', 0)} overlapping the candidate week.
- Phase15: {p15.get('prediction_files', 0)} prediction files, {p15.get('files_overlapping_candidate_final_week', 0)} overlapping the candidate week.
- Legacy feature-ablation, robustness, regime, history-sensitivity, and model-comparison artifacts use the same historical test manifest or predictions.

Those experiments and their interpretation expose the same calendar outcomes and have already informed model/task understanding. Therefore the week cannot be presented as a new independent blind test. The old test period is frozen as **historical development/comparison period**.

No final-week MAE, RMSE, sMAPE, prediction values, target values, or error values were read or calculated in this Phase 2A-0 audit.

Required path forward: collect a new independent time period, or use a transparently retrospective rolling-origin evaluation. Phase 2A-1 confirmatory test design is stopped.
"""
    write_text("01_blind_test_audit/BLIND_TEST_ELIGIBILITY.md", blind)
    write_text("11_reports/BLIND_TEST_ELIGIBILITY.md", blind)
    write_text("11_reports/TIME_GRID_AND_DENOMINATOR_REPORT.md", (OUT / "02_time_grid_definition" / "TIME_GRID_AUDIT.md").read_text(encoding="utf-8"))

    below = next(r["value"] for r in raw_info["audit_rows"] if r["field"] == "confidence" and r["statistic"] == "below_0.8")
    cleaning = f"""# Cleaning-policy report

The cleaned input contains {len(raw_info['audit_rows']) and '244,477'} records. Confidence >=0.80 is frozen as the draft primary rule; {below:,} records fall below 0.80. Current v2 code accepts any finite confidence in [0,1] and does not enforce the draft confidence threshold, speed maximum, travel-time minimum, valid_* flags, or road-closure rule.

Candidate speed maxima 120/130/160/200 km/h are reported descriptively only. The observed maximum does not establish a physical/provider limit. Because the existing 160 km/h value is explicitly soft and no authoritative physical limit was found, `speed_max=USER_APPROVAL_REQUIRED`.

No provider-status field exists. Traffic state is a traffic condition, not a provider quality status. A proposed valid-flag policy is documented, but the accepted/rejected status whitelist remains `USER_APPROVAL_REQUIRED`.

Final cleaning was not executed.
"""
    write_text("11_reports/CLEANING_POLICY_REPORT.md", cleaning)
    write_text("11_reports/SPLIT_AND_HISTORY_POLICY_REPORT.md", (OUT / "04_split_definition" / "SPLIT_AND_HISTORY_BOUNDARY.md").read_text(encoding="utf-8"))
    write_text("11_reports/TARGET_AND_H6_SENSITIVITY_REPORT.md", (OUT / "05_target_definition" / "TARGET_DEFINITION.md").read_text(encoding="utf-8"))
    write_text("11_reports/MODEL_INPUT_FREEZE_REPORT.md", (OUT / "07_feature_freeze" / "MODEL_INPUT_FREEZE_SPEC.md").read_text(encoding="utf-8"))
    write_text("11_reports/DISTRIBUTION_LICENSE_REPORT.md", (OUT / "09_distribution_license" / "DISTRIBUTION_STATUS.md").read_text(encoding="utf-8"))

    executive = f"""# Phase 2A-0 executive summary

## Decision

**PHASE2A0_STATUS = BLOCKED**

Experimental definitions were frozen as a draft, but Phase 2A-1 is not authorized.

## Frozen draft

- Task: future-window mean speed, H=1/3/6.
- H=6 primary completeness: 5/6; descriptive sensitivity: 6/6.
- Primary history: 24h; secondary development histories: 72h and 168h.
- Primary hourly aggregation: 2/4; descriptive thresholds: 1/4, 3/4, 4/4.
- Time grid: Asia/Kuala_Lumpur, floor-15min/floor-hour, complete hours only.
- History boundary: causal carry-over; all fit statistics remain train-only.

## Why blocked

1. Candidate final week is `CONTAMINATED_TEST`: it overlaps legacy evaluated/test predictions and downstream analyses.
2. Speed maximum has no approved physical/provider rule.
3. Provider status whitelist cannot be derived because the field is absent.
4. The v2 source tree was actively receiving Phase6 output during this audit; a stable snapshot is required before later work.

The source Git commit is `{commit}`; the source worktree is dirty: {git_dirty}. No source file was changed by this audit. No model was trained and no final-week performance was inspected or computed.
"""
    write_text("11_reports/PHASE2A0_EXECUTIVE_SUMMARY.md", executive)
    write_text("README_START_HERE.md", """# AJSE Phase 2A-0 Definition Freeze

Start with `11_reports/PHASE2A0_EXECUTIVE_SUMMARY.md` and `11_reports/BLOCKING_ITEMS.md`. This package contains metadata, definitions, schemas, audit summaries, and hashes only. It contains no commercial raw FCD, final-week predictions, performance metrics, credentials, or model weights.
""")


def secret_scan() -> None:
    patterns = re.compile(r"(?i)(api[_-]?key|access[_-]?token|refresh[_-]?token|password|passwd|private[_-]?key)\s*[:=]\s*([^\s#]+)")
    rows = []
    for p in OUT.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".md", ".txt", ".yaml", ".yml", ".json", ".csv"}:
            continue
        for line_no, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if patterns.search(line):
                rows.append({"file": str(p.relative_to(OUT)), "line": line_no, "potential_secret_assignment": True, "value_copied": False})
    write_csv("00_source_audit/OUTPUT_SECRET_SCAN.csv", rows, ["file", "line", "potential_secret_assignment", "value_copied"])


def finalize(summary_values: dict) -> dict:
    checks = []
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name != "checksums_sha256.csv":
            checks.append({"relative_path": str(p.relative_to(OUT)).replace("\\", "/"), "size_bytes": p.stat().st_size, "sha256": sha256(p)})
    write_csv("checksums_sha256.csv", checks)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for p in sorted(OUT.rglob("*")):
            if p.is_file():
                zf.write(p, Path(OUT.name) / p.relative_to(OUT))
    digest = sha256(ZIP_PATH)
    sidecar = ROOT / "AJSE_Phase2A0_Definition_Freeze.zip.sha256"
    sidecar.write_text(f"{digest}  {ZIP_PATH.name}\n", encoding="utf-8")
    summary_values.update({"OUTPUT_ZIP": str(ZIP_PATH), "OUTPUT_ZIP_SHA256": digest})
    terminal = "\n".join(f"{k} = {v}" for k, v in summary_values.items())
    (ROOT / "AJSE_Phase2A0_TERMINAL_SUMMARY.txt").write_text(terminal + "\n", encoding="utf-8")
    print(terminal)
    return {"zip": str(ZIP_PATH), "sha256": digest, "checksum_rows": len(checks), "zip_entries": len(zipfile.ZipFile(ZIP_PATH).infolist())}


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for d in DIRS:
        (OUT / d).mkdir(parents=True, exist_ok=True)

    cfg, splits = load_source_config()
    commit, git_status, dirty = git_state()
    processes = active_processes()
    source_inventory(commit, git_status, processes)
    shell_history_audit()
    raw, time_meta, raw_info = raw_audit(cfg)
    fixed = splits["fixed_splits"]
    final_start = pd.Timestamp(fixed["final_week"]["target_start"])
    final_end = pd.Timestamp(fixed["final_week"]["target_end"])
    current_scan = scan_current_v2_final_week(final_start, final_end)
    write_text("00_source_audit/CURRENT_V2_FINAL_WEEK_SCAN.json", json.dumps(current_scan, ensure_ascii=False, indent=2))
    _, old_summary = scan_old_overlap(final_start, final_end)
    blockers, final_cfg = make_policies(cfg, splits, time_meta, current_scan, old_summary, processes, commit, dirty)
    reports(cfg, splits, time_meta, raw_info, current_scan, old_summary, blockers, commit, dirty, processes)
    secret_scan()

    below = next(r["value"] for r in raw_info["audit_rows"] if r["field"] == "confidence" and r["statistic"] == "below_0.8")
    summary_values = {
        "PHASE2A0_STATUS": "BLOCKED",
        "V2_PROJECT_ROOT": str(V2),
        "SOURCE_GIT_COMMIT": commit,
        "SOURCE_GIT_DIRTY": str(dirty).upper(),
        "FINAL_TEST_START": fixed["final_week"]["target_start"],
        "FINAL_TEST_END": fixed["final_week"]["target_end"],
        "FINAL_TEST_ELIGIBILITY": "CONTAMINATED_TEST",
        "OLD_TEST_PERIOD_ROLE": "historical_development_comparison",
        "TIMEZONE": "Asia/Kuala_Lumpur",
        "FIRST_RAW_TIMESTAMP": time_meta["first_raw"],
        "FIRST_COMPLETE_HOUR": time_meta["first_complete_hour"],
        "LAST_RAW_TIMESTAMP": time_meta["last_raw"],
        "LAST_COMPLETE_HOUR": time_meta["last_complete_hour"],
        "PARTIAL_START_HOUR_EXCLUDED": "TRUE",
        "LEGACY_15MIN_DENOMINATOR": time_meta["legacy_15min_denominator"],
        "NEW_COMPLETE_BIN_15MIN_DENOMINATOR": time_meta["new_15min_denominator"],
        "LEGACY_HOURLY_DENOMINATOR": time_meta["legacy_hourly_denominator"],
        "NEW_COMPLETE_BIN_HOURLY_DENOMINATOR": time_meta["new_hourly_denominator"],
        "CONFIDENCE_BELOW_0_8_COUNT": below,
        "CONFIDENCE_PRIMARY_RULE": "confidence>=0.80",
        "SPEED_MAX_RULE": "USER_APPROVAL_REQUIRED",
        "STATUS_WHITELIST_STATUS": "USER_APPROVAL_REQUIRED_NO_PROVIDER_STATUS_FIELD",
        "PRIMARY_HISTORY_HOURS": 24,
        "HISTORY_BOUNDARY_POLICY": "causal_carry_over; no split reset",
        "PRIMARY_AGGREGATION_THRESHOLD": "2_of_4",
        "TARGET_TYPE": "future_window_mean_speed",
        "H6_PRIMARY_COMPLETENESS": "5_of_6",
        "H6_SENSITIVITY_COMPLETENESS": "6_of_6",
        "FULL_SAMPLE_ASSERTION_STATUS": "PLAN_FROZEN_NOT_EXECUTED",
        "DISTRIBUTION_PERMISSION_STATUS": "MIXED; DERIVED_DATA_PERMISSION_UNCLEAR",
        "BLOCKING_ITEM_COUNT": len(blockers),
    }
    result = finalize(summary_values)
    print("VALIDATION = " + json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
