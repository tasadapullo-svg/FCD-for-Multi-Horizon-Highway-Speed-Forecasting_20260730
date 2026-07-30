# AJSE Phase 2A canonical workspace

This directory is restricted to the AJSE Phase 2A task.

## Canonical experimental definition

- Target: `FUTURE_WINDOW_MEAN_SPEED`
- Horizons: `H1`, `H3`, and `H6`
- Sample assignment: by forecast origin, with the complete target window inside the split
- Current verified stage: Phase 2A-0 definition freeze
- Phase 2A-0 status: `BLOCKED`
- Phase 2A-1 completed result set: `NOT FOUND`

## Evidence boundary

The v2.2 P6/P7/P8 direct point-forecast results are not Phase 2A result files and must not be used as the primary AJSE Phase 2A evidence. They were moved, without deletion, to the quarantine directory recorded in `00_MANIFESTS/AJSE_CANONICAL_ROOT_STATUS.json`.

Do not compare v2.2 point-target MAE directly with Phase 2A future-window-mean MAE.

## Directory map

- `00_MANIFESTS`: before/after inventories, SHA-256 hashes, and reorganization actions.
- `01_PHASE2A_DEFINITION_FREEZE`: Phase 2A-0 definitions, policies, and audit reports.
- `02_PHASE2A_RELEASE_PACKAGE`: frozen ZIP, checksum, and terminal summary.
- `03_PHASE2A_BUILD_CODE`: code used to build the Phase 2A-0 package.
- `04_PHASE2A_DATA_RESULTS`: reserved for genuine Phase 2A-1 and later future-window-mean results.

