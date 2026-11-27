import argparse
from pathlib import Path
import pandas as pd
from fig05_pipeline import join_reliability_errors

parser = argparse.ArgumentParser(); parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args(); origins = pd.read_parquet(args.out / "01_DERIVED_DATA" / "Fig05_unique_test_origins.parquet"); errors = pd.read_parquet(args.out / "01_DERIVED_DATA" / "Fig05_seed_averaged_sample_errors.parquet"); join_reliability_errors(origins, errors, args.out)
