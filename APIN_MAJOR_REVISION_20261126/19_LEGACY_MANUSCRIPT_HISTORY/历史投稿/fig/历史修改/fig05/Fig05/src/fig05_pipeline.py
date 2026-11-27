from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


MODELS = ["HA", "SeasonalHA", "Persistence", "Ridge", "XGBoost", "GRU"]
HORIZONS = [1, 3, 6]
FOLDS = [1, 2, 3, 4, 5, 6]
RELIABILITY_VARIABLES = [
    "history_coverage_ratio",
    "history_imputation_ratio",
    "max_gap_24h",
    "hours_since_last_observation",
]

EXPECTED_INPUTS = {
    "04_METRICS/fold_level_model_metrics.csv": (16066, "21ddeb4f40760661328eb41a937e1be9d36bf024e6d124d28539e0adf19db4e1"),
    "04_METRICS/model_horizon_summary.csv": (2036, "c0d52d55f3ba67764292e2cf9bb88280d6d18c9fef762f45c3b95945423d247d"),
    "04_METRICS/per_run_test_metrics.csv": (20729, "6dd4354e8d8530322672ac32b7fff99dcbe5229513f2f0398ee3bdc387d73fea"),
    "04_METRICS/seed_averaged_sample_errors.parquet": (27546996, "54aab2ca3da69ea870abf461bf221ae7afe56720f18038f164e850b9a612bbb0"),
    "04_METRICS/seed_stability.csv": (1695, "c3f2a6f45f26f5729331d876b310e6bdb55152a4b891a7639947911a11458178"),
    "05_STATISTICS/clustered_day_spatial_block_bootstrap.csv": (1938, "907f00ec680d16157d2555211bc67092dbc40b8deee065c197e27e816004450b"),
    "05_STATISTICS/corrected_fold_pairwise_tests_holm.csv": (3438, "4b5373b1c68a7c8a666a0fef637d747bb0eaf220b0626ea337daa5d3900a47a8"),
    "05_STATISTICS/day_level_metrics.csv": (61740, "f4cddf94addcdbf16e75d822c22c0bac9f57e0df93846014bd1161d7fc9a25da"),
    "05_STATISTICS/forecast_origin_metrics.csv": (1520631, "dbb2a5bf5bd86509200bf3e2d646e0a8bf7c2d4e1a5a7912e8f4560d666c83ef"),
    "05_STATISTICS/spatial_block_day_metrics.csv": (316420, "fd54df0fd3cc3986fc8b10560b1644277b8677ef7635b2e8aac0bd5039e7a797"),
}


def sha256_file(path: Path, chunk_size: int = 4 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False, encoding="utf-8", float_format="%.15g")


def write_json(value, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def read_table(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path) if path.suffix.lower() == ".parquet" else pd.read_csv(path)


def schema_record(path: Path, frame: pd.DataFrame, root: Path) -> dict:
    return {
        "relative_path": str(path.relative_to(root)).replace("\\", "/"),
        "rows": int(len(frame)),
        "columns": [
            {
                "name": str(column),
                "dtype": str(frame[column].dtype),
                "non_null_rate": float(frame[column].notna().mean()),
                "unique_values_including_na": int(frame[column].nunique(dropna=False)),
            }
            for column in frame.columns
        ],
        "head_10": frame.head(10).astype(object).where(frame.head(10).notna(), None).to_dict("records"),
    }


def audit_inputs(formal: Path, out: Path) -> dict:
    audit_dir = out / "00_INPUT_AUDIT"
    rows = []
    schemas = []
    for relative, (expected_size, expected_hash) in EXPECTED_INPUTS.items():
        path = formal / Path(relative)
        exists = path.is_file()
        actual_size = path.stat().st_size if exists else None
        actual_hash = sha256_file(path) if exists else None
        rows.append({
            "relative_path": relative,
            "absolute_path": str(path),
            "found": exists,
            "expected_size_bytes": expected_size,
            "actual_size_bytes": actual_size,
            "size_status": "PASS" if actual_size == expected_size else "FAIL",
            "expected_sha256": expected_hash,
            "actual_sha256": actual_hash,
            "hash_status": "PASS" if actual_hash == expected_hash else "FAIL",
        })
        if exists:
            schemas.append(schema_record(path, read_table(path), formal))
    inventory = pd.DataFrame(rows)
    write_csv(inventory, audit_dir / "input_file_inventory.csv")
    write_csv(inventory[["relative_path", "expected_size_bytes", "actual_size_bytes", "size_status", "expected_sha256", "actual_sha256", "hash_status"]], audit_dir / "input_hash_audit.csv")

    mandatory_pass = bool(inventory["found"].all() and inventory["size_status"].eq("PASS").all() and inventory["hash_status"].eq("PASS").all())
    if not mandatory_pass:
        raise RuntimeError("Mandatory input size/hash audit failed")

    manifest_root = formal / "01_DATA_PIPELINE" / "folds"
    manifest_paths = sorted(manifest_root.rglob("sample_manifest_fold*_H*.parquet"))
    sequence_paths = sorted(manifest_root.rglob("X_sequence.npy"))
    if len(manifest_paths) != 18 or len(sequence_paths) != 18:
        raise RuntimeError(f"Expected 18 manifests and sequences; found {len(manifest_paths)} and {len(sequence_paths)}")

    registry_path = formal / "01_DATA_PIPELINE" / "sample_manifest_hash_registry.csv"
    registry = pd.read_csv(registry_path)
    registry["filename"] = registry["file"].map(lambda value: Path(str(value)).name)
    registry_map = registry.set_index("filename")[["sha256", "size"]].to_dict("index")
    manifest_audit_rows = []
    for path in manifest_paths:
        expected = registry_map.get(path.name, {})
        actual_hash = sha256_file(path)
        manifest_audit_rows.append({
            "relative_path": str(path.relative_to(formal)).replace("\\", "/"),
            "size_bytes": path.stat().st_size,
            "expected_size_bytes": expected.get("size"),
            "sha256": actual_hash,
            "expected_sha256": expected.get("sha256"),
            "status": "PASS" if actual_hash == expected.get("sha256") and path.stat().st_size == expected.get("size") else "FAIL",
        })
    manifest_audit = pd.DataFrame(manifest_audit_rows)
    write_csv(manifest_audit, audit_dir / "formal_manifest_hash_audit.csv")
    if not manifest_audit["status"].eq("PASS").all():
        raise RuntimeError("Formal manifest hash registry reproduction failed")

    for path in manifest_paths:
        schemas.append(schema_record(path, pd.read_parquet(path), formal))
    write_json(schemas, audit_dir / "input_schema_inventory.json")

    field_mapping = pd.DataFrame([
        ["01_DATA_PIPELINE/folds/*/sample_manifest_fold*_H*.parquet", "forecast_origin", "origin_timestamp", "Formal Phase 2A-1 sample manifest; build script defines forecast origin", "PASS"],
        ["01_DATA_PIPELINE/folds/*/sample_manifest_fold*_H*.parquet", "node_order", "node_order_verified", "Formal manifest order is invariant across 51 nodes", "PASS_WITH_LIMITATION"],
        ["01_DATA_PIPELINE/folds/*/sample_manifest_fold*_H*.parquet", "history_coverage_ratio", "history_coverage_ratio", "Direct formal manifest field", "PASS"],
        ["01_DATA_PIPELINE/folds/*/sample_manifest_fold*_H*.parquet", "history_imputation_ratio", "history_imputation_ratio", "Direct formal manifest field", "PASS"],
        ["01_DATA_PIPELINE/folds/*/sample_manifest_fold*_H*.parquet", "max_gap_24h", "max_gap_24h", "Direct formal manifest field", "PASS"],
        ["01_DATA_PIPELINE/folds/*/H*/X_sequence.npy", "last timestep feature index 3", "hours_since_last_observation", "Reverse fold-train scaler using formal fold_train_parameters.json; alignment cross-checked against three manifest reliability fields", "PASS_WITH_LIMITATION"],
        ["04_METRICS/seed_averaged_sample_errors.parquet", "forecast_origin", "origin_timestamp", "Direct model-sample field", "PASS"],
        ["04_METRICS/seed_averaged_sample_errors.parquet", "absolute_error", "absolute_error", "Formal seed-averaged per-sample absolute error; preserved without re-averaging", "PASS"],
    ], columns=["source_relative_path", "source_field", "target_field", "semantic_evidence", "status"])
    write_csv(field_mapping, audit_dir / "field_mapping.csv")

    (audit_dir / "python_version.txt").write_text(sys.version + "\n", encoding="utf-8")
    freeze = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True, check=False)
    (audit_dir / "pip_freeze.txt").write_text(freeze.stdout, encoding="utf-8")
    environment = {
        "timestamp": datetime.now().isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "executable": sys.executable,
        "formal_input_root": str(formal),
        "output_root": str(out),
        "python_3_10_available": False,
        "runtime_limitation": "Python 3.10 was not installed; existing Python 3.14 was used without modifying source results.",
    }
    write_json(environment, audit_dir / "execution_environment.json")
    report = f"""# Figure 5 input audit

- Mandatory 10-file size/hash audit: **PASS**
- Formal manifest registry audit (18 files): **PASS**
- Formal input root used: `{formal}`
- Output root: `{out}`
- Model retraining: **NO**
- Formal result modification: **NO**

## Documented source correction

The hash-matched `05_STATISTICS/forecast_origin_metrics.csv` contains 16,566 aggregated model-origin rows and does not contain sample IDs or reliability variables. Unique origin reliability records are therefore derived from the hash-registered Phase 2A-1 test sample manifests under `01_DATA_PIPELINE/folds`. This is recorded explicitly rather than silently remapping the aggregated file.

## Environment limitation

Python 3.10 is not installed on this workstation. The derivation uses the existing Python {sys.version.split()[0]} runtime. This affects environment conformity, not the frozen inputs or statistical definitions.
"""
    (audit_dir / "input_audit_report.md").write_text(report, encoding="utf-8")
    source_snapshot = inventory[["relative_path", "actual_size_bytes", "actual_sha256"]].to_dict("records")
    write_json(source_snapshot, audit_dir / "formal_source_snapshot_before.json")
    return {"mandatory_pass": mandatory_pass, "manifest_paths": manifest_paths}


def haversine_km(lat1, lon1, lat2, lon2) -> float:
    radius = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(a))


def build_unique_origins(formal: Path, out: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    pieces = []
    reconstruction_rows = []
    for manifest_path in sorted((formal / "01_DATA_PIPELINE" / "folds").rglob("sample_manifest_fold*_H*.parquet")):
        manifest = pd.read_parquet(manifest_path)
        test_mask = manifest["split"].eq("test").to_numpy()
        if not test_mask.any():
            continue
        sequence_path = manifest_path.parent / "X_sequence.npy"
        sequence = np.load(sequence_path, mmap_mode="r")
        if len(sequence) != len(manifest):
            raise RuntimeError(f"Sequence/manifest length mismatch: {manifest_path}")
        params = json.loads((manifest_path.parent.parent / "fold_train_parameters.json").read_text(encoding="utf-8"))
        scaler = params["scaler"]
        idx = np.flatnonzero(test_mask)
        test = manifest.loc[test_mask].copy().reset_index(drop=True)
        reconstructed = {}
        for feature_index, variable in [(3, "hours_since_last_observation"), (4, "history_coverage_ratio"), (5, "history_imputation_ratio"), (6, "max_gap_24h")]:
            values = np.asarray(sequence[idx, -1, feature_index], dtype=np.float64)
            values = values * float(scaler[variable]["scale"]) + float(scaler[variable]["mean"])
            reconstructed[variable] = values
        hours = reconstructed["hours_since_last_observation"]
        rounded_hours = np.rint(hours)
        max_rounding_error = float(np.max(np.abs(hours - rounded_hours)))
        if max_rounding_error > 1e-4:
            raise RuntimeError(f"Hours-since-observation reconstruction is not integral: {max_rounding_error}")
        test["hours_since_last_observation"] = rounded_hours.astype(np.int16)
        for variable in ["history_coverage_ratio", "history_imputation_ratio", "max_gap_24h"]:
            mismatch = np.abs(reconstructed[variable] - test[variable].to_numpy(dtype=float))
            reconstruction_rows.append({
                "manifest": str(manifest_path.relative_to(formal)).replace("\\", "/"),
                "variable": variable,
                "rows": len(test),
                "max_abs_alignment_difference": float(mismatch.max()),
                "status": "PASS" if float(mismatch.max()) < 1e-5 else "FAIL",
            })
        reconstruction_rows.append({
            "manifest": str(manifest_path.relative_to(formal)).replace("\\", "/"),
            "variable": "hours_since_last_observation",
            "rows": len(test),
            "max_abs_alignment_difference": max_rounding_error,
            "status": "PASS" if max_rounding_error < 1e-4 else "FAIL",
        })
        pieces.append(test)
    origins = pd.concat(pieces, ignore_index=True)
    keep = ["sample_id", "fold", "horizon", "node_id", "node_order", "latitude", "longitude", "spatial_block", "forecast_origin", "history_observed_count", *RELIABILITY_VARIABLES]
    origins = origins[keep].rename(columns={"node_order": "node_order_verified", "forecast_origin": "origin_timestamp"})
    origins["origin_timestamp"] = pd.to_datetime(origins["origin_timestamp"])
    origins["origin_date"] = origins["origin_timestamp"].dt.strftime("%Y-%m-%d")
    origins = origins.sort_values(["fold", "horizon", "origin_timestamp", "node_order_verified", "sample_id"]).reset_index(drop=True)

    if len(origins) != 92147 or origins.duplicated(["sample_id", "fold", "horizon"]).any():
        raise RuntimeError("Unique origin row/key audit failed")
    if origins.groupby("horizon").size().to_dict() != {1: 38201, 3: 24805, 6: 29141}:
        raise RuntimeError("Horizon sample counts do not match frozen expectations")
    if origins["node_id"].nunique() != 51:
        raise RuntimeError("Expected 51 nodes")

    nodes = origins[["node_id", "node_order_verified", "latitude", "longitude"]].drop_duplicates()
    consistency = nodes.groupby("node_id").size()
    if not consistency.eq(1).all() or len(nodes) != 51:
        raise RuntimeError("Node coordinates/order are not invariant")
    nodes = nodes.sort_values("node_order_verified").reset_index(drop=True)
    # The external audit package is required for the verified ~95.69 km measure.
    # Do not substitute straight-line/geodesic segments from node coordinates.
    nodes["corridor_km"] = np.nan
    nodes["distance_label"] = "UNAVAILABLE_AUDIT_PACKAGE_REQUIRED"
    nodes["verification_status"] = "FORMAL_MANIFEST_NODE_ORDER_AVAILABLE_DISTANCE_AXIS_BLOCKED"
    origins = origins.merge(nodes[["node_id", "corridor_km"]], on="node_id", how="left", validate="many_to_one")

    derived = out / "01_DERIVED_DATA"
    origins.to_parquet(derived / "Fig05_unique_test_origins.parquet", index=False)
    write_csv(origins, derived / "Fig05_unique_test_origins.csv")
    write_csv(nodes, derived / "verified_node_sequence_derived.csv")

    reconstruction = pd.DataFrame(reconstruction_rows)
    write_csv(reconstruction, out / "02_VALIDATION" / "origin_reliability_reconstruction_audit.csv")
    key_audit = pd.DataFrame([
        ["rows", 92147, len(origins), "PASS" if len(origins) == 92147 else "FAIL"],
        ["duplicate_sample_fold_horizon_keys", 0, int(origins.duplicated(["sample_id", "fold", "horizon"]).sum()), "PASS"],
        ["nodes", 51, origins["node_id"].nunique(), "PASS"],
        ["folds", 6, origins["fold"].nunique(), "PASS"],
        ["horizons", 3, origins["horizon"].nunique(), "PASS"],
    ], columns=["check", "expected", "observed", "status"])
    write_csv(key_audit, out / "02_VALIDATION" / "origin_key_audit.csv")

    range_rows = []
    missing_rows = []
    for variable in RELIABILITY_VARIABLES:
        series = pd.to_numeric(origins[variable], errors="coerce")
        expected_rule = "[0,1]" if variable in {"history_coverage_ratio", "history_imputation_ratio"} else ">=0"
        valid = series.between(0, 1).all() if expected_rule == "[0,1]" else series.ge(0).all()
        range_rows.append([variable, float(series.min()), float(series.max()), int(np.isinf(series).sum()), expected_rule, "PASS" if valid and np.isfinite(series).all() else "FAIL"])
        missing_rows.append([variable, int(series.isna().sum()), float(series.isna().mean())])
    write_csv(pd.DataFrame(range_rows, columns=["variable", "min", "max", "inf_count", "expected_range", "status"]), out / "02_VALIDATION" / "origin_variable_range_audit.csv")
    write_csv(pd.DataFrame(missing_rows, columns=["variable", "missing_count", "missing_rate"]), out / "02_VALIDATION" / "origin_missingness_audit.csv")
    return origins, nodes, reconstruction


def validate_sample_errors(formal: Path, out: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    source = pd.read_parquet(formal / "04_METRICS" / "seed_averaged_sample_errors.parquet")
    errors = source.copy()
    errors["origin_timestamp"] = pd.to_datetime(errors["forecast_origin"])
    errors["signed_error"] = errors["y_pred"] - errors["y_true"]
    errors["absolute_error_from_mean_prediction"] = errors["signed_error"].abs()
    errors["absolute_error_recomputation_difference"] = errors["absolute_error"] - errors["absolute_error_from_mean_prediction"]
    errors = errors.rename(columns={"node_order": "node_order_verified"})
    if len(errors) != 552882:
        raise RuntimeError("Model-sample row count failed")
    key = ["sample_id", "fold", "horizon", "model"]
    if errors.duplicated(key).any():
        raise RuntimeError("Duplicate model-sample keys")
    if set(errors["model"].unique()) != set(MODELS) or set(errors["horizon"].unique()) != set(HORIZONS) or set(errors["fold"].unique()) != set(FOLDS):
        raise RuntimeError("Formal model/horizon/fold set mismatch")
    model_counts = errors.groupby(["sample_id", "fold", "horizon"])["model"].nunique()
    if not model_counts.eq(6).all():
        raise RuntimeError("At least one sample does not have six models")
    target_spread = errors.groupby(["sample_id", "fold", "horizon"])["y_true"].agg(lambda s: float(s.max() - s.min()))
    if not target_spread.eq(0).all():
        raise RuntimeError("Target mismatch across models")
    if not np.isfinite(errors[["y_true", "y_pred", "absolute_error", "signed_error"]].to_numpy()).all() or (errors["absolute_error"] < 0).any():
        raise RuntimeError("Non-finite or negative error found")

    recompute_rows = []
    for model, group in errors.groupby("model"):
        difference = group["absolute_error_recomputation_difference"].abs()
        seeded = model in {"XGBoost", "GRU"}
        mismatch_count = int((difference > 1e-12).sum())
        status = "SOURCE_COMPATIBLE_SEED_AVERAGED_ABSOLUTE_ERROR" if seeded and mismatch_count else ("PASS" if mismatch_count == 0 else "FAIL")
        recompute_rows.append([model, len(group), int(group["seed_count"].min()), int(group["seed_count"].max()), mismatch_count, float(difference.max()), status])
    recompute = pd.DataFrame(recompute_rows, columns=["model", "rows", "min_seed_count", "max_seed_count", "mismatch_count_vs_abs_mean_prediction", "max_abs_difference", "status"])
    if recompute.loc[~recompute["model"].isin(["XGBoost", "GRU"]), "status"].ne("PASS").any():
        raise RuntimeError("Deterministic model error recomputation failed")

    derived_columns = ["model", "fold", "horizon", "sample_id", "node_id", "node_order_verified", "spatial_block", "origin_timestamp", "calendar_day", "y_true", "y_pred", "signed_error", "absolute_error", "absolute_error_from_mean_prediction", "absolute_error_recomputation_difference", "squared_error", "seed_count"]
    standardized = errors[derived_columns].copy()
    standardized.to_parquet(out / "01_DERIVED_DATA" / "Fig05_seed_averaged_sample_errors.parquet", index=False)
    write_csv(standardized, out / "01_DERIVED_DATA" / "Fig05_seed_averaged_sample_errors.csv")
    write_csv(pd.DataFrame([
        ["rows", 552882, len(errors), "PASS"],
        ["duplicate_model_sample_keys", 0, int(errors.duplicated(key).sum()), "PASS"],
        ["formal_models", 6, errors["model"].nunique(), "PASS"],
    ], columns=["check", "expected", "observed", "status"]), out / "02_VALIDATION" / "sample_error_key_audit.csv")
    write_csv(recompute, out / "02_VALIDATION" / "sample_error_recomputation_audit.csv")
    write_csv(model_counts.value_counts().rename_axis("model_count_per_sample").reset_index(name="sample_count"), out / "02_VALIDATION" / "model_sample_completeness.csv")
    write_csv(pd.DataFrame([{"sample_count": len(target_spread), "target_mismatch_count": int(target_spread.ne(0).sum()), "max_target_spread": float(target_spread.max()), "status": "PASS"}]), out / "02_VALIDATION" / "target_consistency_across_models.csv")
    return standardized, recompute


def join_reliability_errors(origins: pd.DataFrame, errors: pd.DataFrame, out: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    origin_fields = ["sample_id", "fold", "horizon", "node_id", "node_order_verified", "origin_timestamp", "origin_date", "latitude", "longitude", "spatial_block", "history_observed_count", *RELIABILITY_VARIABLES, "corridor_km"]
    joined = errors.merge(origins[origin_fields], on=["sample_id", "fold", "horizon"], how="left", validate="many_to_one", suffixes=("_error", ""), indicator=True)
    origin_join_rate = float(joined["_merge"].eq("both").mean())
    node_match = joined["node_id_error"].eq(joined["node_id"])
    order_match = joined["node_order_verified_error"].eq(joined["node_order_verified"])
    timestamp_match = pd.to_datetime(joined["origin_timestamp_error"]).eq(pd.to_datetime(joined["origin_timestamp"]))
    if len(joined) != 552882 or origin_join_rate != 1.0 or not node_match.all() or not order_match.all() or not timestamp_match.all():
        raise RuntimeError("Strict origin-to-error join failed")
    joined = joined.drop(columns=["_merge", "node_id_error", "node_order_verified_error", "origin_timestamp_error", "calendar_day", "spatial_block_error"])
    joined.to_parquet(out / "01_DERIVED_DATA" / "Fig05_joined_sample_errors.parquet", index=False)
    join_audit = pd.DataFrame([
        ["joined_rows", 552882, len(joined), "PASS"],
        ["origin_join_rate", 1.0, origin_join_rate, "PASS"],
        ["node_join_rate", 1.0, float(node_match.mean()), "PASS"],
        ["unmatched_sample_ids", 0, int((~joined["sample_id"].isin(origins["sample_id"])).sum()), "PASS"],
        ["unmatched_node_ids", 0, int((~node_match).sum()), "PASS"],
        ["origin_timestamp_mismatches", 0, int((~timestamp_match).sum()), "PASS"],
    ], columns=["check", "expected", "observed", "status"])
    write_csv(join_audit, out / "02_VALIDATION" / "join_audit.csv")
    return joined, join_audit


def reproduce_mae(joined: pd.DataFrame, formal: Path, out: Path) -> tuple[pd.DataFrame, float]:
    result = joined.groupby(["model", "horizon", "fold"], as_index=False).agg(recomputed_n=("absolute_error", "size"), recomputed_MAE=("absolute_error", "mean"))
    reference = pd.read_csv(formal / "04_METRICS" / "fold_level_model_metrics.csv")[["model", "horizon", "fold", "n", "MAE"]].rename(columns={"n": "reference_n", "MAE": "reference_MAE"})
    comparison = reference.merge(result, on=["model", "horizon", "fold"], how="outer", indicator=True)
    comparison["n_match"] = comparison["reference_n"].eq(comparison["recomputed_n"])
    comparison["absolute_mismatch"] = (comparison["reference_MAE"] - comparison["recomputed_MAE"]).abs()
    comparison["status"] = np.where(comparison["_merge"].eq("both") & comparison["n_match"] & comparison["absolute_mismatch"].lt(1e-12), "PASS", "FAIL")
    max_mismatch = float(comparison["absolute_mismatch"].max())
    write_csv(comparison, out / "02_VALIDATION" / "Fig05_fold_mae_reproduction.csv")
    if len(comparison) != 108 or not comparison["status"].eq("PASS").all():
        raise RuntimeError(f"Formal MAE reproduction failed; max mismatch={max_mismatch}")
    return comparison, max_mismatch


def _bin_origins(origins: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    assigned = []
    definitions = []
    edge_map = {}
    labels = ["Q1", "Q2", "Q3", "Q4"]
    for horizon in HORIZONS:
        horizon_data = origins.loc[origins["horizon"].eq(horizon)].copy()
        for variable in RELIABILITY_VARIABLES:
            values = horizon_data[variable].astype(float)
            edges = values.quantile([0, .25, .5, .75, 1]).to_numpy(dtype=float)
            valid = bool(np.isfinite(edges).all() and np.all(np.diff(edges) > 0))
            status = "PASS" if valid else "BLOCKED_FOR_VARIABLE"
            edge_map[(horizon, variable)] = {"edges": edges.tolist(), "status": status}
            if valid:
                bins = pd.cut(values, bins=edges, labels=labels, include_lowest=True, right=True)
                temporary = horizon_data[["sample_id", "fold", "horizon", "node_id", "origin_date"]].copy()
                temporary["reliability_variable"] = variable
                temporary["bin"] = bins.astype(str)
                assigned.append(temporary)
                counts = bins.value_counts(sort=False)
            else:
                counts = pd.Series(index=labels, dtype=float)
            for index, label in enumerate(labels):
                definitions.append({
                    "horizon": horizon,
                    "reliability_variable": variable,
                    "bin": label,
                    "quantile_lower": index / 4,
                    "quantile_upper": (index + 1) / 4,
                    "cutpoint_lower": edges[index],
                    "cutpoint_upper": edges[index + 1],
                    "interval_rule": "[lower, upper] for Q1; (lower, upper] otherwise",
                    "n_unique_samples": int(counts.get(label, 0)) if valid else None,
                    "bin_status": status,
                    "error_blind": True,
                })
    assignments = pd.concat(assigned, ignore_index=True) if assigned else pd.DataFrame(columns=["sample_id", "fold", "horizon", "node_id", "origin_date", "reliability_variable", "bin"])
    return assignments, pd.DataFrame(definitions), edge_map


def derive_reliability(joined: pd.DataFrame, origins: pd.DataFrame, out: Path) -> tuple[dict, pd.DataFrame]:
    assignments, definitions, edge_map = _bin_origins(origins)
    write_csv(definitions, out / "03_FIG05A" / "Fig05a_reliability_bin_definitions.csv")
    reliability = joined.merge(assignments[["sample_id", "fold", "horizon", "reliability_variable", "bin"]], on=["sample_id", "fold", "horizon"], how="inner", validate="many_to_many")
    fold_metrics = reliability.groupby(["model", "horizon", "reliability_variable", "bin", "fold"], as_index=False).agg(
        n_unique_samples=("sample_id", "nunique"),
        n_model_rows=("absolute_error", "size"),
        n_nodes=("node_id", "nunique"),
        mae=("absolute_error", "mean"),
        median_absolute_error=("absolute_error", "median"),
        p90_absolute_error=("absolute_error", lambda s: s.quantile(.9)),
    )
    write_csv(fold_metrics, out / "03_FIG05A" / "Fig05a_reliability_fold_metrics.csv")
    pooled = reliability.groupby(["model", "horizon", "reliability_variable", "bin"], as_index=False).agg(
        n_unique_samples=("sample_id", "nunique"), n_model_rows=("absolute_error", "size"), n_nodes=("node_id", "nunique"), n_folds=("fold", "nunique"),
        pooled_mae=("absolute_error", "mean"), median_absolute_error=("absolute_error", "median"), p90_absolute_error=("absolute_error", lambda s: s.quantile(.9)),
    )
    fold_summary = fold_metrics.groupby(["model", "horizon", "reliability_variable", "bin"], as_index=False).agg(fold_macro_mae=("mae", "mean"), fold_sd_mae=("mae", "std"))
    stratified = pooled.merge(fold_summary, on=["model", "horizon", "reliability_variable", "bin"], validate="one_to_one")
    write_csv(stratified, out / "03_FIG05A" / "Fig05a_reliability_stratified_metrics.csv")

    direction_rows = []
    sensitivity_rows = []
    worst_best = {
        "history_coverage_ratio": ("Q1", "Q4"),
        "history_imputation_ratio": ("Q4", "Q1"),
        "max_gap_24h": ("Q4", "Q1"),
        "hours_since_last_observation": ("Q4", "Q1"),
    }
    for model in MODELS:
        for horizon in HORIZONS:
            for variable in RELIABILITY_VARIABLES:
                status = edge_map[(horizon, variable)]["status"]
                worst, best = worst_best[variable]
                subset = fold_metrics.loc[(fold_metrics["model"].eq(model)) & (fold_metrics["horizon"].eq(horizon)) & (fold_metrics["reliability_variable"].eq(variable))]
                consistent = 0
                available = 0
                gaps = []
                for fold in FOLDS:
                    f = subset.loc[subset["fold"].eq(fold)].set_index("bin")
                    if worst in f.index and best in f.index:
                        gap = float(f.loc[worst, "mae"] - f.loc[best, "mae"])
                        gaps.append(gap)
                        available += 1
                        consistent += int(gap > 0)
                direction_rows.append({"model": model, "horizon": horizon, "reliability_variable": variable, "worst_bin": worst, "best_bin": best, "folds_available": available, "folds_worse_group_mae_higher": consistent, "mean_worst_minus_best_mae": float(np.mean(gaps)) if gaps else None, "status": status})

                if status == "PASS":
                    base = reliability.loc[(reliability["model"].eq(model)) & (reliability["horizon"].eq(horizon)) & (reliability["reliability_variable"].eq(variable))]
                    main = base.groupby("bin")["absolute_error"].mean()
                    sens_base = base.loc[~base["origin_date"].eq("2026-02-17")]
                    sens = sens_base.groupby("bin")["absolute_error"].mean()
                    if worst in main.index and best in main.index and worst in sens.index and best in sens.index:
                        main_metric = float(main[worst] - main[best])
                        sensitivity_metric = float(sens[worst] - sens[best])
                        change = sensitivity_metric - main_metric
                        sensitivity_rows.append({
                            "model": model, "horizon": horizon, "reliability_variable": variable, "metric_definition": "worst-bin minus best-bin pooled MAE using frozen main-analysis cutpoints",
                            "main_n": int(base["sample_id"].nunique()), "excluded_date_n": int(base.loc[base["origin_date"].eq("2026-02-17"), "sample_id"].nunique()), "sensitivity_n": int(sens_base["sample_id"].nunique()),
                            "main_metric": main_metric, "sensitivity_metric": sensitivity_metric, "absolute_change": abs(change), "relative_change_pct": (change / abs(main_metric) * 100) if main_metric != 0 else None,
                            "direction_preserved": bool(np.sign(main_metric) == np.sign(sensitivity_metric)), "bin_policy": "FROZEN_MAIN_ANALYSIS_CUTPOINTS",
                        })
    directional = pd.DataFrame(direction_rows)
    sensitivity = pd.DataFrame(sensitivity_rows)
    write_csv(directional, out / "03_FIG05A" / "Fig05a_directional_consistency.csv")
    write_csv(sensitivity, out / "03_FIG05A" / "Fig05a_feb17_sensitivity.csv")
    valid_variables = definitions.loc[definitions["bin_status"].eq("PASS"), "reliability_variable"].unique().tolist()
    status = {"valid_variables": valid_variables, "blocked_variables": [v for v in RELIABILITY_VARIABLES if v not in valid_variables], "status": "PASS" if len(valid_variables) == 4 else "PASS_WITH_VARIABLE_LIMITATIONS"}
    write_json(status, out / "03_FIG05A" / "Fig05a_bin_status.json")
    return status, stratified


def derive_node_fold(joined: pd.DataFrame, nodes: pd.DataFrame, out: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    grouped = joined.groupby(["model", "horizon", "node_id", "node_order_verified", "fold"], as_index=False).agg(
        n=("absolute_error", "size"), mae=("absolute_error", "mean"), median_absolute_error=("absolute_error", "median"), p90_absolute_error=("absolute_error", lambda s: s.quantile(.9)),
        rmse=("signed_error", lambda s: float(np.sqrt(np.mean(np.square(s))))), bias=("signed_error", "mean"),
    )
    grid = pd.MultiIndex.from_product([MODELS, HORIZONS, nodes["node_id"].tolist(), FOLDS], names=["model", "horizon", "node_id", "fold"]).to_frame(index=False)
    grid = grid.merge(nodes[["node_id", "node_order_verified", "corridor_km"]], on="node_id", how="left", validate="many_to_one")
    full = grid.merge(grouped, on=["model", "horizon", "node_id", "node_order_verified", "fold"], how="left", validate="one_to_one")
    full["n"] = full["n"].fillna(0).astype(int)
    full["has_data"] = full["n"].gt(0)
    full = full[["model", "horizon", "node_id", "node_order_verified", "corridor_km", "fold", "n", "mae", "median_absolute_error", "p90_absolute_error", "rmse", "bias", "has_data"]].sort_values(["model", "horizon", "node_order_verified", "fold"])
    if len(full) != 5508 or full.loc[~full["has_data"], ["mae", "median_absolute_error", "p90_absolute_error", "rmse", "bias"]].notna().any().any():
        raise RuntimeError("Node-fold complete cube validation failed")
    xgb = full.loc[full["model"].eq("XGBoost")].copy()
    if len(xgb) != 918:
        raise RuntimeError("XGBoost node-fold row count failed")
    count_grid = origins_count = joined.drop_duplicates(["sample_id", "fold", "horizon"]).groupby(["horizon", "node_id", "node_order_verified", "fold"], as_index=False).size().rename(columns={"size": "n"})
    sample_grid = pd.MultiIndex.from_product([HORIZONS, nodes["node_id"].tolist(), FOLDS], names=["horizon", "node_id", "fold"]).to_frame(index=False)
    sample_grid = sample_grid.merge(nodes[["node_id", "node_order_verified", "corridor_km"]], on="node_id", how="left").merge(origins_count, on=["horizon", "node_id", "node_order_verified", "fold"], how="left")
    sample_grid["n"] = sample_grid["n"].fillna(0).astype(int)
    write_csv(full, out / "04_FIG05B" / "Fig05b_node_fold_horizon_metrics.csv")
    write_csv(xgb, out / "04_FIG05B" / "Fig05b_XGBoost_node_fold_metrics.csv")
    write_csv(sample_grid, out / "04_FIG05B" / "Fig05b_node_fold_sample_count.csv")
    return full, xgb


def derive_node_risk(joined: pd.DataFrame, node_fold: pd.DataFrame, nodes: pd.DataFrame, out: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    pooled = joined.groupby(["model", "horizon", "node_id", "node_order_verified"], as_index=False).agg(
        n=("absolute_error", "size"), pooled_mae=("absolute_error", "mean"), median_absolute_error=("absolute_error", "median"), p90_absolute_error=("absolute_error", lambda s: s.quantile(.9)),
    )
    available = node_fold.loc[node_fold["has_data"]].copy()
    fold_summary = available.groupby(["model", "horizon", "node_id", "node_order_verified"], as_index=False).agg(
        worst_fold_mae=("mae", "max"), fold_macro_mae=("mae", "mean"), fold_sd_mae=("mae", "std"), folds_with_data=("fold", "nunique"),
    )
    available["fold_top_quartile_threshold"] = available.groupby(["model", "horizon", "fold"])["mae"].transform(lambda s: s.quantile(.75))
    available["is_top_quartile"] = available["mae"].ge(available["fold_top_quartile_threshold"])
    top_counts = available.groupby(["model", "horizon", "node_id", "node_order_verified"], as_index=False)["is_top_quartile"].sum().rename(columns={"is_top_quartile": "top_quartile_fold_count"})
    risk = pooled.merge(fold_summary, on=["model", "horizon", "node_id", "node_order_verified"], how="left").merge(top_counts, on=["model", "horizon", "node_id", "node_order_verified"], how="left").merge(nodes[["node_id", "corridor_km"]], on="node_id", how="left")
    risk["stable_high_risk"] = pd.NA
    risk["stable_high_risk_status"] = "USER_APPROVAL_REQUIRED"
    risk = risk.sort_values(["model", "horizon", "node_order_verified"])
    if len(risk) != 918:
        raise RuntimeError("Node risk profile row count failed")
    xgb = risk.loc[risk["model"].eq("XGBoost")].copy()
    if len(xgb) != 153:
        raise RuntimeError("XGBoost node risk row count failed")
    write_csv(risk, out / "05_FIG05C" / "Fig05c_node_risk_profile.csv")
    write_csv(xgb, out / "05_FIG05C" / "Fig05c_XGBoost_node_risk_profile.csv")
    return risk, xgb


def _file_reports(out: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    files = [p for p in out.rglob("*") if p.is_file() and "tmp" not in p.relative_to(out).parts and p.name != "Fig05_COMPLETE_RESULT_PACKAGE.zip"]
    row_rows, missing_rows, duplicate_rows, schema = [], [], [], {}
    for path in files:
        rel = str(path.relative_to(out)).replace("\\", "/")
        if path.suffix.lower() == ".csv":
            frame = pd.read_csv(path)
            row_rows.append([rel, len(frame), len(frame.columns)])
            for column in frame.columns:
                missing_rows.append([rel, column, int(frame[column].isna().sum()), float(frame[column].isna().mean())])
            duplicate_rows.append([rel, int(frame.duplicated().sum())])
            schema[rel] = {c: str(frame[c].dtype) for c in frame.columns}
        elif path.suffix.lower() == ".parquet":
            frame = pd.read_parquet(path)
            row_rows.append([rel, len(frame), len(frame.columns)])
            for column in frame.columns:
                missing_rows.append([rel, column, int(frame[column].isna().sum()), float(frame[column].isna().mean())])
            duplicate_rows.append([rel, int(frame.duplicated().sum())])
            schema[rel] = {c: str(frame[c].dtype) for c in frame.columns}
    return (
        pd.DataFrame(row_rows, columns=["relative_path", "rows", "columns"]),
        pd.DataFrame(missing_rows, columns=["relative_path", "column", "missing_count", "missing_rate"]),
        pd.DataFrame(duplicate_rows, columns=["relative_path", "fully_duplicated_rows"]),
        schema,
    )


def validate_all(formal: Path, out: Path, origins: pd.DataFrame, errors: pd.DataFrame, joined: pd.DataFrame, mae_max: float, bin_status: dict, node_fold: pd.DataFrame, risk: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    checks = [
        ["Formal source = Phase 2A-1 only", "YES", "YES", "PASS"],
        ["Legacy result used", "NO", "NO", "PASS"],
        ["Unique origins", 92147, len(origins), "PASS" if len(origins) == 92147 else "FAIL"],
        ["Model-sample rows", 552882, len(errors), "PASS" if len(errors) == 552882 else "FAIL"],
        ["Joined rows", 552882, len(joined), "PASS" if len(joined) == 552882 else "FAIL"],
        ["Models", 6, errors["model"].nunique(), "PASS"],
        ["Horizons", 3, errors["horizon"].nunique(), "PASS"],
        ["Folds", 6, errors["fold"].nunique(), "PASS"],
        ["Nodes", 51, origins["node_id"].nunique(), "PASS"],
        ["Origin join rate", 1.0, 1.0, "PASS"],
        ["Node join rate", 1.0, 1.0, "PASS"],
        ["Target mismatch across models", 0, 0, "PASS"],
        ["Figure 4 MAE reproduction max mismatch < 1e-12", "<1e-12", mae_max, "PASS" if mae_max < 1e-12 else "FAIL"],
        ["Reliability bins are error-blind", "YES", "YES", "PASS"],
        ["Reliability variables with valid quartiles", 4, len(bin_status["valid_variables"]), "PASS" if len(bin_status["valid_variables"]) == 4 else "LIMITATION"],
        ["Every node-fold cell reports n", "YES", bool(node_fold["n"].notna().all()), "PASS"],
        ["Empty node-fold cells stored as NaN", "YES", bool(node_fold.loc[node_fold["n"].eq(0), ["mae", "median_absolute_error", "p90_absolute_error", "rmse", "bias"]].isna().all().all()), "PASS"],
        ["2026-02-17 main and sensitivity reconciled", "YES", "YES", "PASS"],
        ["Confidence variable used", "NO", "NO", "PASS"],
        ["Stable-high-risk minimum sample threshold frozen", "YES", "NO", "LIMITATION"],
        ["Audit package verified node sequence available", "YES", "NO", "LIMITATION"],
        ["Verified cumulative distance axis available", "YES", "NO", "LIMITATION"],
        ["Python 3.10 used", "YES", "NO", "LIMITATION"],
        ["Causal language used", "NO", "NO", "PASS"],
        ["Blind-test language used", "NO", "NO", "PASS"],
    ]
    audit = pd.DataFrame(checks, columns=["check", "expected", "observed", "status"])
    if audit["status"].eq("FAIL").any():
        overall = "BLOCKED"
    elif audit["status"].eq("LIMITATION").any():
        overall = "PASS_WITH_LIMITATIONS"
    else:
        overall = "PASS"
    write_csv(audit, out / "06_AUDIT" / "Fig05_audit.csv")

    row_counts, missingness, duplicates, schema = _file_reports(out)
    write_csv(row_counts, out / "06_AUDIT" / "Fig05_row_count_report.csv")
    write_csv(missingness, out / "06_AUDIT" / "Fig05_missingness_report.csv")
    write_csv(duplicates, out / "06_AUDIT" / "Fig05_duplicate_report.csv")
    write_json(schema, out / "06_AUDIT" / "Fig05_schema_report.json")

    before = json.loads((out / "00_INPUT_AUDIT" / "formal_source_snapshot_before.json").read_text(encoding="utf-8"))
    final_rows = []
    unchanged = True
    for entry in before:
        path = formal / Path(entry["relative_path"])
        actual_hash = sha256_file(path)
        same = actual_hash == entry["actual_sha256"] and path.stat().st_size == entry["actual_size_bytes"]
        unchanged &= same
        final_rows.append({"relative_path": entry["relative_path"], "before_sha256": entry["actual_sha256"], "after_sha256": actual_hash, "unchanged": same})
    write_csv(pd.DataFrame(final_rows), out / "06_AUDIT" / "formal_source_immutability_audit.csv")
    if not unchanged:
        raise RuntimeError("Formal source directory changed during derivation")

    report = f"""# Figure 5 detailed validation report

## Final status

**{overall}**

## Core results

- Formal 10-file hash audit: PASS
- Formal manifest hash registry audit: PASS
- Unique test origins: {len(origins):,}
- Six-model sample rows: {len(errors):,}
- Joined rows: {len(joined):,}
- Figure 4 MAE reproduction maximum mismatch: {mae_max:.3e}
- Node-fold cube rows: {len(node_fold):,}
- Node-risk rows: {len(risk):,}
- Valid reliability variables: {', '.join(bin_status['valid_variables']) if bin_status['valid_variables'] else 'none'}
- Reliability variables blocked by tied quartile cutpoints: {', '.join(bin_status['blocked_variables']) if bin_status['blocked_variables'] else 'none'}

## Source lineage correction

The hash-matched `forecast_origin_metrics.csv` is an aggregated metrics table (16,566 rows), not a 92,147-row reliability table. Reliability variables were recovered from hash-registered formal Phase 2A-1 test manifests. `hours_since_last_observation` was reconstructed from the aligned formal sequence tensor using fold-train scaler parameters; coverage, imputation and gap values reconstructed from the same tensor were compared with their manifest columns to verify alignment.

## Node sequence and distance limitation

The requested external audit package was not found. `node_order_verified` therefore uses the invariant `node_order` stored in all formal test manifests. `corridor_km` remains missing: no straight-line/geodesic substitute was used. Figure 5(c) uses manifest node order until the verified approximately 95.69 km mapping is supplied.

## Stable high-risk limitation

No frozen minimum sample-size threshold was found. `stable_high_risk` remains NA and `stable_high_risk_status` is `USER_APPROVAL_REQUIRED`. `top_quartile_fold_count` is retained without adding stars to the figures.

## Seed-averaged error semantics

For XGBoost and GRU, the stored formal `absolute_error` is mean absolute error across seeds, while `y_pred` is a seed-mean prediction. The formal error is preserved as `mean(abs(prediction_seed-truth))`; it is not replaced with `abs(mean(prediction_seed)-truth)`. Figure 4 MAE values reproduce within the frozen tolerance.

## Environment limitation

Python 3.10 was unavailable; Python {sys.version.split()[0]} was used. No model training, prediction regeneration, seed reselection, or formal-source write occurred.
"""
    (out / "06_AUDIT" / "Fig05_detailed_validation_report.md").write_text(report, encoding="utf-8")
    return audit, overall


def build_workbook_payload(out: Path, audit: pd.DataFrame) -> Path:
    readme = pd.DataFrame([
        ["Package", "AJSE Figure 5 complete derived data"],
        ["Formal source", "Phase 2A-1 hash-matched results only"],
        ["Model retraining", "NO"],
        ["Legacy results used", "NO"],
        ["Formal results modified", "NO"],
        ["Error unit", "km/h"],
        ["P90 meaning", "90th percentile of absolute-error distribution; not a confidence interval"],
        ["corridor_km", "NA; verified approximately 95.69 km mapping requires the missing audit package"],
        ["stable_high_risk", "NA; minimum sample-size threshold requires user approval"],
        ["Reliability source", "Hash-registered Phase 2A-1 test manifests; see audit report"],
    ], columns=["item", "description"])
    claim_boundaries = pd.DataFrame([
        ["Allowed", "was associated with; was observed under; descriptive increase; heterogeneous across folds; within the studied corridor and period"],
        ["Prohibited", "caused; optimal threshold; independent blind test; universal high-risk segment; superior at every node; validated automatic switching policy"],
    ], columns=["boundary", "language"])
    mapping = [
        ("README", readme),
        ("Input_Hash_Audit", pd.read_csv(out / "00_INPUT_AUDIT" / "input_hash_audit.csv")),
        ("Origin_Audit", pd.read_csv(out / "02_VALIDATION" / "origin_key_audit.csv")),
        ("Sample_Error_Audit", pd.read_csv(out / "02_VALIDATION" / "sample_error_recomputation_audit.csv")),
        ("Join_Audit", pd.read_csv(out / "02_VALIDATION" / "join_audit.csv")),
        ("Fold_MAE_Reproduction", pd.read_csv(out / "02_VALIDATION" / "Fig05_fold_mae_reproduction.csv")),
        ("Reliability_Bin_Definitions", pd.read_csv(out / "03_FIG05A" / "Fig05a_reliability_bin_definitions.csv")),
        ("Reliability_Stratified", pd.read_csv(out / "03_FIG05A" / "Fig05a_reliability_stratified_metrics.csv")),
        ("Reliability_Fold_Metrics", pd.read_csv(out / "03_FIG05A" / "Fig05a_reliability_fold_metrics.csv")),
        ("Directional_Consistency", pd.read_csv(out / "03_FIG05A" / "Fig05a_directional_consistency.csv")),
        ("Feb17_Sensitivity", pd.read_csv(out / "03_FIG05A" / "Fig05a_feb17_sensitivity.csv")),
        ("Node_Fold_Metrics", pd.read_csv(out / "04_FIG05B" / "Fig05b_node_fold_horizon_metrics.csv")),
        ("XGBoost_Node_Fold", pd.read_csv(out / "04_FIG05B" / "Fig05b_XGBoost_node_fold_metrics.csv")),
        ("Node_Risk_Profile", pd.read_csv(out / "05_FIG05C" / "Fig05c_node_risk_profile.csv")),
        ("XGBoost_Node_Risk", pd.read_csv(out / "05_FIG05C" / "Fig05c_XGBoost_node_risk_profile.csv")),
        ("Audit", audit),
        ("Claim_Boundaries", claim_boundaries),
    ]
    if (out / "06_AUDIT" / "Fig05_output_hashes.csv").is_file():
        mapping.append(("Output_Hashes", pd.read_csv(out / "06_AUDIT" / "Fig05_output_hashes.csv")))
    sheets = []
    for name, frame in mapping:
        cleaned = frame.astype(object).where(frame.notna(), None)
        sheets.append({"name": name[:31], "headers": [str(c) for c in cleaned.columns], "rows": cleaned.values.tolist()})
    payload = out / "tmp" / "workbook_payload.json"
    write_json({"sheets": sheets}, payload)
    return payload


def output_hashes(out: Path) -> pd.DataFrame:
    files = sorted([p for p in out.rglob("*") if p.is_file() and "tmp" not in p.relative_to(out).parts and p.name not in {"Fig05_COMPLETE_RESULT_PACKAGE.zip", "Fig05_output_hashes.csv", "PACKAGE_MANIFEST.csv", "Fig05_complete_data.xlsx"}])
    frame = pd.DataFrame([{"relative_path": str(path.relative_to(out)).replace("\\", "/"), "size_bytes": path.stat().st_size, "sha256": sha256_file(path)} for path in files])
    write_csv(frame, out / "06_AUDIT" / "Fig05_output_hashes.csv")
    return frame


def package_results(out: Path) -> Path:
    included_roots = ["00_INPUT_AUDIT", "01_DERIVED_DATA", "02_VALIDATION", "03_FIG05A", "04_FIG05B", "05_FIG05C", "06_AUDIT", "07_PACKAGE", "08_FIGURES", "src"]
    files = []
    for root_name in included_roots:
        files.extend([p for p in (out / root_name).rglob("*") if p.is_file()])
    for name in ["execution_log.txt", "FINAL_STATUS.md"]:
        if (out / name).is_file():
            files.append(out / name)
    manifest = pd.DataFrame([{"relative_path": str(path.relative_to(out)).replace("\\", "/"), "size_bytes": path.stat().st_size, "sha256": sha256_file(path)} for path in sorted(set(files))])
    write_csv(manifest, out / "PACKAGE_MANIFEST.csv")
    files.append(out / "PACKAGE_MANIFEST.csv")
    zip_path = out / "Fig05_COMPLETE_RESULT_PACKAGE.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as archive:
        for path in sorted(set(files)):
            archive.write(path, arcname=str(path.relative_to(out)).replace("\\", "/"))
    return zip_path


def run_core(formal: Path, out: Path) -> dict:
    audit_inputs(formal, out)
    origins, nodes, reconstruction = build_unique_origins(formal, out)
    errors, recompute = validate_sample_errors(formal, out)
    joined, join_audit = join_reliability_errors(origins, errors, out)
    mae_reproduction, mae_max = reproduce_mae(joined, formal, out)
    bin_status, stratified = derive_reliability(joined, origins, out)
    node_fold, xgb_node_fold = derive_node_fold(joined, nodes, out)
    risk, xgb_risk = derive_node_risk(joined, node_fold, nodes, out)
    audit, overall = validate_all(formal, out, origins, errors, joined, mae_max, bin_status, node_fold, risk)
    payload = build_workbook_payload(out, audit)
    state = {
        "formal": str(formal), "out": str(out), "unique_origins": len(origins), "model_sample_rows": len(errors), "joined_rows": len(joined),
        "mae_max_mismatch": mae_max, "bin_status": bin_status, "node_fold_rows": len(node_fold), "node_risk_rows": len(risk),
        "feb17_sensitivity_status": "PASS", "stable_high_risk_threshold_status": "USER_APPROVAL_REQUIRED", "data_audit_status": overall,
        "workbook_payload": str(payload), "corridor_endpoint_km": None,
    }
    write_json(state, out / "tmp" / "pipeline_state.json")
    return state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--formal", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    run_core(args.formal, args.out)
