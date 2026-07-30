# Model-input freeze specification

Phase 2A-1 must freeze model-ready inputs, not only metadata.

Required artifacts:

- processed hourly panel with stable `panel_row_id`;
- `feature_columns.json` with ordered names and dtypes;
- `panel_index.parquet` (`panel_row_id`, `node_id`, `timestamp`, `split`);
- per-horizon sample manifests containing history and target row IDs;
- `X_sequence_{split}_H{H}.npz` with shape `[n_samples, history_length, n_features]`;
- `X_tabular_{split}_H{H}.parquet`;
- `y_{split}_H{H}.npy` and `sample_ids_{split}_H{H}.npy`;
- train-fitted imputation/scaler JSON files;
- feature-generation manifest containing code/config/input hashes.

Every manifest records `sample_id`, node, forecast origin, history bounds/row IDs, target bounds/row IDs, target value and observed ratio, split, history length, aggregation threshold, and target definition. Feature order is immutable after freezing.
