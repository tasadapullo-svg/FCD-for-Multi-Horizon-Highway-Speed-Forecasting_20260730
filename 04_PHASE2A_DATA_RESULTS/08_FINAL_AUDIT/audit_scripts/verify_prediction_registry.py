from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--result-root", required=True)
    args = ap.parse_args()
    root = Path(args.result_root)
    registry = pd.read_csv(root / "03_FORMAL_PREDICTIONS" / "formal_run_registry.csv")
    rows = []
    required = {"sample_id", "fold", "split", "node_id", "forecast_origin", "horizon", "y_true", "y_pred", "model", "seed", "run_name", "absolute_error", "squared_error", "smape_component"}
    for r in registry.itertuples(index=False):
        pred = Path(r.prediction_file)
        manifest = Path(r.sample_manifest)
        pred_exists = pred.exists()
        manifest_exists = manifest.exists()
        pred_hash = digest(pred) if pred_exists else "MISSING"
        manifest_hash = digest(manifest) if manifest_exists else "MISSING"
        readable = columns_ok = row_count_ok = sample_ids_ok = False
        error = ""
        try:
            p = pd.read_parquet(pred)
            m = pd.read_parquet(manifest, columns=["sample_id", "split"])
            readable = True
            columns_ok = required.issubset(p.columns)
            row_count_ok = len(p) == int(r.test_samples)
            expected_ids = set(m.loc[m["split"] == "test", "sample_id"].astype(str))
            actual_ids = set(p["sample_id"].astype(str))
            sample_ids_ok = actual_ids == expected_ids and len(actual_ids) == len(p)
        except Exception as exc:
            error = repr(exc)
        passed = bool(
            pred_exists and manifest_exists and pred_hash.lower() == str(r.prediction_sha256).lower()
            and manifest_hash.lower() == str(r.sample_manifest_sha256).lower()
            and readable and columns_ok and row_count_ok and sample_ids_ok
        )
        rows.append({
            "run_name": r.run_name, "model": r.model, "fold": int(r.fold), "horizon": int(r.horizon), "seed": int(r.seed),
            "prediction_exists": pred_exists, "prediction_hash_match": pred_hash.lower() == str(r.prediction_sha256).lower(),
            "manifest_exists": manifest_exists, "manifest_hash_match": manifest_hash.lower() == str(r.sample_manifest_sha256).lower(),
            "parquet_readable": readable, "required_columns_present": columns_ok,
            "test_row_count_match": row_count_ok, "test_sample_ids_exact_match": sample_ids_ok,
            "pass": passed, "error": error,
        })
    out = pd.DataFrame(rows)
    audit = root / "08_FINAL_AUDIT"
    out.to_csv(audit / "PREDICTION_REGISTRY_HASH_RECHECK.csv", index=False)
    status = {
        "status": "PASS" if out["pass"].all() and len(out) == 180 else "FAIL",
        "registry_rows": int(len(out)), "passed_rows": int(out["pass"].sum()),
        "failed_rows": int((~out["pass"]).sum()),
        "prediction_hash_mismatches": int((~out["prediction_hash_match"]).sum()),
        "manifest_hash_mismatches": int((~out["manifest_hash_match"]).sum()),
        "unreadable_parquet": int((~out["parquet_readable"]).sum()),
        "sample_id_mismatches": int((~out["test_sample_ids_exact_match"]).sum()),
    }
    (audit / "PREDICTION_REGISTRY_HASH_RECHECK.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))
    if status["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
