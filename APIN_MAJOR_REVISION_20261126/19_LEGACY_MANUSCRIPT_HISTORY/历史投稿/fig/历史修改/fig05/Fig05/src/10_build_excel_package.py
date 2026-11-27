from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from fig05_pipeline import build_workbook_payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--node", type=Path, required=True)
    args = parser.parse_args()
    audit_path = args.out / "06_AUDIT" / "Fig05_audit.csv"
    import pandas as pd
    payload = build_workbook_payload(args.out, pd.read_csv(audit_path))
    builder = args.out / "src" / "build_workbook.mjs"
    destination = args.out / "07_PACKAGE" / "Fig05_complete_data.xlsx"
    previews = args.out / "tmp" / "workbook_previews"
    subprocess.run([str(args.node), str(builder), str(payload), str(destination), str(previews)], check=True)


if __name__ == "__main__":
    main()
