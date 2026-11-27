import argparse
from pathlib import Path
import pandas as pd
from fig05_pipeline import derive_reliability

parser = argparse.ArgumentParser(); parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args(); joined = pd.read_parquet(args.out / "01_DERIVED_DATA" / "Fig05_joined_sample_errors.parquet"); origins = pd.read_parquet(args.out / "01_DERIVED_DATA" / "Fig05_unique_test_origins.parquet"); derive_reliability(joined, origins, args.out)
