import argparse
from pathlib import Path
import pandas as pd
from fig05_pipeline import reproduce_mae

parser = argparse.ArgumentParser(); parser.add_argument("--formal", type=Path, required=True); parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args(); joined = pd.read_parquet(args.out / "01_DERIVED_DATA" / "Fig05_joined_sample_errors.parquet"); reproduce_mae(joined, args.formal, args.out)
