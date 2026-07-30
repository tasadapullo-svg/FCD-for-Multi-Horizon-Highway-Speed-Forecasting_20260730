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
    hash_file = root / "07_HASHES" / "PHASE2A_RESULT_FILE_SHA256.csv"
    verification_file = root / "08_FINAL_AUDIT" / "PHASE2A_HASH_VERIFICATION.json"
    workbook_file = root / "06_REPORTS" / "AJSE_PHASE2A_RESULT_MASTER.xlsx"
    workbook_inspect = Path(str(workbook_file) + ".inspect.ndjson")
    workbook_sidecar = root / "07_HASHES" / "AJSE_PHASE2A_RESULT_MASTER.xlsx.sha256"
    preview_root = (root / "08_FINAL_AUDIT" / "workbook_previews").resolve()
    excluded = {hash_file.resolve(), verification_file.resolve(), workbook_file.resolve(), workbook_inspect.resolve(), workbook_sidecar.resolve()}
    rows = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.resolve() not in excluded and preview_root not in path.resolve().parents:
            rows.append({"relative_path": str(path.relative_to(root)), "size_bytes": path.stat().st_size, "sha256": digest(path)})
    table = pd.DataFrame(rows)
    hash_file.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(hash_file, index=False)
    reread = pd.read_csv(hash_file)
    mismatches = []
    for row in reread.itertuples(index=False):
        path = root / row.relative_path
        actual = digest(path) if path.exists() else "MISSING"
        if actual.lower() != str(row.sha256).lower():
            mismatches.append({"relative_path": row.relative_path, "expected": row.sha256, "actual": actual})
    workbook_sha256 = digest(workbook_file) if workbook_file.exists() else "NOT_BUILT"
    workbook_sidecar.write_text(f"{workbook_sha256}  {workbook_file.name}\n", encoding="ascii")
    status = {
        "status": "PASS" if not mismatches else "FAIL",
        "hashed_file_count": int(len(reread)),
        "mismatch_count": len(mismatches),
        "missing_count": sum(x["actual"] == "MISSING" for x in mismatches),
        "hash_manifest": str(hash_file),
        "hash_manifest_sha256": digest(hash_file),
        "master_workbook_sha256": workbook_sha256,
        "master_workbook_sidecar": str(workbook_sidecar),
        "excluded_self_referential_files": [str(hash_file.relative_to(root)), str(verification_file.relative_to(root)), str(workbook_file.relative_to(root)), str(workbook_inspect.relative_to(root)), str(workbook_sidecar.relative_to(root)), str(preview_root.relative_to(root))],
        "mismatches": mismatches,
    }
    verification_file.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(status, indent=2, ensure_ascii=False))
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
