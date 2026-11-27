import argparse
from pathlib import Path
from fig05_pipeline import audit_inputs

parser = argparse.ArgumentParser(); parser.add_argument("--formal", type=Path, required=True); parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args(); audit_inputs(args.formal, args.out)
