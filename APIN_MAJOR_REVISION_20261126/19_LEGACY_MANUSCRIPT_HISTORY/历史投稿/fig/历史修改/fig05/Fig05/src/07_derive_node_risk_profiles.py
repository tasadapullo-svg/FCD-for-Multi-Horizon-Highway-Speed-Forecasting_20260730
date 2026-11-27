import argparse
from pathlib import Path
import pandas as pd
from fig05_pipeline import derive_node_risk

parser = argparse.ArgumentParser(); parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args(); joined = pd.read_parquet(args.out / "01_DERIVED_DATA" / "Fig05_joined_sample_errors.parquet"); node_fold = pd.read_csv(args.out / "04_FIG05B" / "Fig05b_node_fold_horizon_metrics.csv"); node_fold["has_data"] = node_fold["has_data"].astype(str).str.lower().eq("true"); nodes = pd.read_csv(args.out / "01_DERIVED_DATA" / "verified_node_sequence_derived.csv"); derive_node_risk(joined, node_fold, nodes, args.out)
