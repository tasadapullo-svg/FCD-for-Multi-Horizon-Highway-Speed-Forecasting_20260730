# Phase 2A-0 executive summary

## Decision

**PHASE2A0_STATUS = BLOCKED**

Experimental definitions were frozen as a draft, but Phase 2A-1 is not authorized.

## Frozen draft

- Task: future-window mean speed, H=1/3/6.
- H=6 primary completeness: 5/6; descriptive sensitivity: 6/6.
- Primary history: 24h; secondary development histories: 72h and 168h.
- Primary hourly aggregation: 2/4; descriptive thresholds: 1/4, 3/4, 4/4.
- Time grid: Asia/Kuala_Lumpur, floor-15min/floor-hour, complete hours only.
- History boundary: causal carry-over; all fit statistics remain train-only.

## Why blocked

1. Candidate final week is `CONTAMINATED_TEST`: it overlaps legacy evaluated/test predictions and downstream analyses.
2. Speed maximum has no approved physical/provider rule.
3. Provider status whitelist cannot be derived because the field is absent.
4. The v2 source tree was actively receiving Phase6 output during this audit; a stable snapshot is required before later work.

The source Git commit is `70fd08cb47895be22e6c9425df37ea4b0fb23cca`; the source worktree is dirty: True. No source file was changed by this audit. No model was trained and no final-week performance was inspected or computed.
