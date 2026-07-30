# Phase 2A-1 formal definition freeze

- Definition freeze commit: `14f0a7547147051c583753a3e44cce9c967ca23e`
- Frozen configuration SHA-256: `b6206a3618ef5af931915223f71ebed567eb17649039c354f94a9261fd1334c1`
- Target: future-window mean speed at H1/H3/H6.
- History: strict causal contiguous 24 hours; no longer lag or weekly branch.
- Validation: six expanding rolling-origin folds, half-open boundaries.
- Purge: a sample is eligible only if the complete future target window is inside its assigned split; no additional embargo.
- H6 primary target coverage: at least five of six future hourly observations; no target imputation.
- Models: HA, SeasonalHA, Persistence, Ridge, XGBoost, GRU.
- Stochastic seeds: 42, 2026, 3407.
- The GRU is the sole lightweight sequence model in the AJSE benchmark.
- CRG-TCN is excluded to preserve the boundary from the separate model paper.
- Test results may not alter any definition above.
- The last week is retrospective; an independent blind-test claim is prohibited.

The data-pipeline resume commit changes only checkpoint recovery behavior. It does not change the frozen configuration or model/data definition.
