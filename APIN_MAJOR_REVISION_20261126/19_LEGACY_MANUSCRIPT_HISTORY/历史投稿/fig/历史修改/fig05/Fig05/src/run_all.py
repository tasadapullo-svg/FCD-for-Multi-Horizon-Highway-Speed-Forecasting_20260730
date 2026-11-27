from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path

import pandas as pd

from fig05_pipeline import build_workbook_payload, output_hashes, package_results, run_core


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--formal", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--node", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    started = datetime.now()
    state = run_core(args.formal, args.out)
    subprocess.run([str(Path(__import__("sys").executable)), str(args.out / "src" / "11_plot_figure5.py"), "--out", str(args.out)], check=True)
    output_hashes(args.out)
    audit = pd.read_csv(args.out / "06_AUDIT" / "Fig05_audit.csv")
    payload = build_workbook_payload(args.out, audit)
    subprocess.run([str(args.node), str(args.out / "src" / "build_workbook.mjs"), str(payload), str(args.out / "07_PACKAGE" / "Fig05_complete_data.xlsx"), str(args.out / "tmp" / "workbook_previews")], check=True)
    state["figure_status"] = "READY_WITH_LIMITATIONS"
    state["final_zip"] = str(args.out / "Fig05_COMPLETE_RESULT_PACKAGE.zip")
    state["model_retraining"] = "NO"
    state["legacy_results_used"] = "NO"
    state["formal_results_modified"] = "NO"
    state["stop_gate_failure"] = "NO_CORE_STOP_GATE_FAILURE; DOCUMENTED_LIMITATIONS_PRESENT"
    final_status = f"""# FINAL STATUS

- FIG05_DATA_AUDIT_STATUS: {state['data_audit_status']}
- FIG05_FIGURE_STATUS: {state['figure_status']}
- MODEL_RETRAINING: NO
- LEGACY_RESULTS_USED: NO
- FORMAL_RESULTS_MODIFIED: NO
- Core stop-gate failure: NO
- Limitations: missing external node-distance audit package; stable-high-risk minimum n not frozen; max-gap and hours-since-observation quartiles blocked by tied cutpoints; Python 3.10 unavailable.
"""
    (args.out / "FINAL_STATUS.md").write_text(final_status, encoding="utf-8")
    log = {
        "started": started.isoformat(), "finished": datetime.now().isoformat(), **state,
    }
    (args.out / "execution_log.txt").write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    zip_path = package_results(args.out)
    print(f"FIG05_INPUT_HASH_STATUS = PASS")
    print(f"FIG05_UNIQUE_ORIGINS = {state['unique_origins']}")
    print(f"FIG05_MODEL_SAMPLE_ROWS = {state['model_sample_rows']}")
    print(f"FIG05_JOINED_ROWS = {state['joined_rows']}")
    print(f"FIG05_MAE_REPRODUCTION_MAX_MISMATCH = {state['mae_max_mismatch']:.17g}")
    print(f"FIG05_RELIABILITY_BIN_STATUS = {state['bin_status']['status']}")
    print(f"FIG05_NODE_FOLD_ROWS = {state['node_fold_rows']}")
    print(f"FIG05_NODE_RISK_ROWS = {state['node_risk_rows']}")
    print(f"FIG05_FEB17_SENSITIVITY_STATUS = {state['feb17_sensitivity_status']}")
    print(f"FIG05_STABLE_HIGH_RISK_THRESHOLD_STATUS = {state['stable_high_risk_threshold_status']}")
    print(f"FIG05_DATA_AUDIT_STATUS = {state['data_audit_status']}")
    print(f"FIG05_FIGURE_STATUS = {state['figure_status']}")
    print(f"FIG05_FINAL_ZIP = {zip_path}")
    print("MODEL_RETRAINING = NO")
    print("LEGACY_RESULTS_USED = NO")
    print("FORMAL_RESULTS_MODIFIED = NO")


if __name__ == "__main__":
    main()
