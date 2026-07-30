# Pan Borneo SIRAF One-Week Traffic Forecasting

This repository is organized as a reproducible SCI-style experiment pipeline for sparse TomTom floating car data on the Pan Borneo Highway, Sarawak.

Current completed stage:

- Phase 1: project audit and data inventory.
- Phase 2: leakage-free forecasting window construction.
- Phase 3: baseline models for speed prediction.
- Phase 4: deep learning smoke test.
- Phase 5: controlled deep learning training.

Phase 3 uses mean speed over the future target window as the prediction target, not terminal speed at the last horizon step. The main baseline horizons are 1h, 3h, 6h, 12h, and 24h; 168h remains excluded from the main baseline experiment.

Phase 5 shows that TCN and LSTM improve over SeasonalHistoricalAverage at 1h, 3h, and 6h, but not at 12h and 24h. The current interpretation is that deep models provide useful short- and medium-horizon correction, while strong periodic baselines remain competitive for longer aggregated mean-speed horizons.

Run Phase 1:

```powershell
py scripts/phase1_data_audit.py --config configs/phase1_data_audit.yaml
```

Phase 1 writes tables to `outputs/tables`, logs to `outputs/logs`, and the audit report to `reports/phase1_data_audit_report.md`.
