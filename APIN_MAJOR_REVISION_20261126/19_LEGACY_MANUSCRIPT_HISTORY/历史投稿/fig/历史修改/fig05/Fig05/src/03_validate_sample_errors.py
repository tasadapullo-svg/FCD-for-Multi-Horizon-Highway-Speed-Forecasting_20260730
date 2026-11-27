import argparse
from pathlib import Path
from fig05_pipeline import validate_sample_errors

parser = argparse.ArgumentParser(); parser.add_argument("--formal", type=Path, required=True); parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args(); validate_sample_errors(args.formal, args.out)
