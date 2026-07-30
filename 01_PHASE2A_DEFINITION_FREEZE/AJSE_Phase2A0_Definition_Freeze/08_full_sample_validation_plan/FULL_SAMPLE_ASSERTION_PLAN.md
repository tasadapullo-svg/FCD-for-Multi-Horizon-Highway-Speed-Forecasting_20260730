# Full-sample assertion plan

Status: **PLAN_FROZEN_NOT_EXECUTED**. Phase 2A-0 builds no samples.

Phase 2A-1 must assert over every sample: unique IDs; feature time <= origin; target time > origin; full target inside split; unfilled targets; correct/increasing history indices; one node per sample; train-only scaler/imputation/regime fits; no validation/test fit; no backward fill, centered rolling, or future merge; no history/target overlap; common manifests across models.

A fixed 1,000-sample audit with seed 2026 is additional numerical recomputation only and cannot replace the exhaustive assertions.
