from pathlib import Path
import sys

import pandas as pd
import pyarrow


ROOT = Path(r"E:\20260730_AJSE_FINAL_bak\04_PHASE2A_DATA_RESULTS")
FILES = [
    ROOT / "04_METRICS" / "seed_averaged_sample_errors.parquet",
    ROOT / "05_STATISTICS" / "forecast_origin_metrics.csv",
    ROOT / "04_METRICS" / "fold_level_model_metrics.csv",
]

print("PYTHON", sys.version)
print("PANDAS", pd.__version__)
print("PYARROW", pyarrow.__version__)
for path in FILES:
    frame = pd.read_parquet(path) if path.suffix == ".parquet" else pd.read_csv(path)
    print("\nFILE", path)
    print("ROWS", len(frame))
    print("COLUMNS", list(frame.columns))
    print("DTYPES", frame.dtypes.astype(str).to_dict())
    print("NUNIQUE", frame.nunique(dropna=False).to_dict())
    print("HEAD\n", frame.head(10).to_string(index=False))

manifests = []
manifest_root = ROOT / "01_DATA_PIPELINE" / "folds"
for path in sorted(manifest_root.rglob("sample_manifest_fold*_H*.parquet")):
    frame = pd.read_parquet(path)
    frame = frame.loc[frame["split"].eq("test")].copy()
    if len(frame):
        manifests.append(frame)
origins = pd.concat(manifests, ignore_index=True)
print("\nTEST_MANIFEST_ROWS", len(origins))
print("TEST_MANIFEST_UNIQUE_IDS", origins["sample_id"].nunique())
print("HORIZON_COUNTS", origins.groupby("horizon").size().to_dict())
for horizon, group in origins.groupby("horizon"):
    print("H", horizon)
    for variable in ["history_coverage_ratio", "history_imputation_ratio", "max_gap_24h"]:
        print(variable, group[variable].quantile([0, .25, .5, .75, 1]).to_dict())

nodes = origins[["node_id", "node_order", "latitude", "longitude"]].drop_duplicates()
print("NODE_METADATA_ROWS", len(nodes))
print(nodes.sort_values("node_order").to_string(index=False))
