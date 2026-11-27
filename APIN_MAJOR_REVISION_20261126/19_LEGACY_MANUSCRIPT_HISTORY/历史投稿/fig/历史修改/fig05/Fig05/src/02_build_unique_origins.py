import argparse
from pathlib import Path
from fig05_pipeline import build_unique_origins

parser = argparse.ArgumentParser(); parser.add_argument("--formal", type=Path, required=True); parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args(); build_unique_origins(args.formal, args.out)
