import argparse
from pathlib import Path
import pandas as pd
from fig05_pipeline import build_workbook_payload, output_hashes

parser = argparse.ArgumentParser(); parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args(); output_hashes(args.out); build_workbook_payload(args.out, pd.read_csv(args.out / "06_AUDIT" / "Fig05_audit.csv"))
