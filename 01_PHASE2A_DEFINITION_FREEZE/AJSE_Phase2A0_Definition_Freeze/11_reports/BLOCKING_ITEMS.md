# Blocking items

- **B01 — candidate final week is contaminated**: The candidate week is a subset of the legacy Phase13/15/16 test period and is covered by historical model predictions, feature ablation, robustness/regime analysis, and result interpretation. Resolution: Collect a new independent time period or use retrospective rolling-origin evaluation.
- **B02 — speed_max not approved**: Only a soft 160 km/h audit value exists; no documented physical/provider upper bound was found. Resolution: User/domain approval of a fixed upper-bound rule independent of prediction performance.
- **B03 — provider status whitelist unresolved**: The cleaned input has no provider_status field; valid_* flags and traffic_state are not a documented provider-status whitelist. Resolution: Approve an explicit flag/status policy or declare provider status not applicable with documented rationale.
- **B04 — source project is actively mutating**: 6 v2 Phase6 campaign/trial process entries were active during the audit. Resolution: Wait for Phase6 to finish and take a stable source snapshot before Phase 2A-1.
