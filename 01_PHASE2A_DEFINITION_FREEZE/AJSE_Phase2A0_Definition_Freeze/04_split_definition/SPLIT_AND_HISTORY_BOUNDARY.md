# Split and history-boundary policy

Candidate dates are read from the v2 configuration, not hard-coded:

- Train: 2025-12-08T13:00:00 through 2026-02-07T23:00:00.
- Validation: 2026-02-08T00:00:00 through 2026-02-14T23:00:00.
- Confirmation: 2026-02-15T00:00:00 through 2026-02-21T23:00:00.
- Candidate final test: 2026-02-22T00:00:00 through 2026-02-28T23:00:00.

The v2 point-target pipeline assigns membership by target time and applies a 24-hour maximum-horizon purge to training boundaries. AJSE future-window samples will instead assign by forecast origin and require the full target window to remain inside that split.

Historical observations may causally carry across a boundary because they were available before the new forecast origin. Forward-fill state is not reset. Every fitted statistic and selection decision remains train-only. A strict same-split history count will be produced later only as an audit comparator.

The candidate final test is **CONTAMINATED_TEST**, so this policy cannot authorize a confirmatory final-test run.
