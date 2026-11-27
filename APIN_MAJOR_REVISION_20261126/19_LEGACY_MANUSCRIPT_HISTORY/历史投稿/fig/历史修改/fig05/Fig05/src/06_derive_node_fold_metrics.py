import argparse
from pathlib import Path
import pandas as pd
from fig05_pipeline import derive_node_fold

parser = argparse.ArgumentParser(); parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args(); joined = pd.read_parquet(args.out / "01_DERIVED_DATA" / "Fig05_joined_sample_errors.parquet"); nodes = pd.read_csv(args.out / "01_DERIVED_DATA" / "verified_node_sequence_derived.csv"); derive_node_fold(joined, nodes, args.out)
