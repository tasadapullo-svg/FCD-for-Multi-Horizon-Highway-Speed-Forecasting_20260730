# Auditable Rolling-Origin Evaluation of Sparse FCD for Multi-Horizon Highway Speed Forecasting

This repository supports a retrospective, six-fold rolling-origin evaluation of sparse commercial floating-car data for multi-horizon highway speed forecasting on the Pan Borneo Highway corridor in Sarawak, Malaysia.

## Scope

The project focuses on data qualification, common-sample evaluation, leakage prevention, temporal stability and reproducibility. It does not claim an independent blind test or universal superiority of a specific model.

## Formal benchmark

- Historical Average
- Seasonal Historical Average
- Persistence
- Ridge Regression
- XGBoost
- GRU

CRG-TCN is not part of this benchmark.

## Evaluation status

```text
Formal runs: 180/180
Failed runs: 0
Rolling-origin folds: 6
Future-window horizons: 1 h, 3 h and 6 h
Common fold-by-horizon manifests: 18
Full-sample leakage assertions: 20/20 passed
Future-information violations: 0
Target-recalculation mismatches: 0
```

## Main descriptive result

XGBoost obtained the lowest fold-averaged MAE at all three future-window horizons, but none of the prespecified fold-level pairwise comparisons remained significant after Holm correction. Seasonal Historical Average remained close and showed lower fold-to-fold variability.

## Interpretation boundary

The final calendar week had been exposed during prior development and is not treated as an independent blind test. All reported results are retrospective rolling-origin evidence for this corridor and observation period.

## Data availability

Commercial raw FCD are not redistributed unless provider permission is confirmed. Public releases should contain code, frozen configurations, data dictionaries, common manifests where permitted, aggregated metrics, audit reports, figures and file hashes.
