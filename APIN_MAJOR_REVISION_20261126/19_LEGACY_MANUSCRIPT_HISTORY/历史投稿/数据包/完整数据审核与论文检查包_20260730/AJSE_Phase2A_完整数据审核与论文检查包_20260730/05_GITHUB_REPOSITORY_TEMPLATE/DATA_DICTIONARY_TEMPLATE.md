# Data Dictionary Template

| Field | Type | Unit | Source/derived | Definition | Eligibility rule | Public release status |
|---|---|---|---|---|---|---|
| timestamp | datetime | local time | source | Observation timestamp | Must belong to frozen grid | Review |
| node_id | string | — | source/frozen | Fixed virtual monitoring node | Must belong to frozen node list | Anonymize if needed |
| current_speed | float | km/h | source | Platform-reported current speed | Frozen valid range | Aggregated only |
| confidence | float | 0–1 | source | Provider confidence measure | Main threshold frozen in YAML | Aggregated only |
| hourly_speed | float | km/h | derived | Hourly aggregate of valid 15-min slots | Main 2/4 rule | Derived release possible |
| history_valid_count | integer | hours | derived | Valid observations in history window | Protocol-defined | Manifest |
| target_valid_count | integer | hours | derived | Valid future target hours | Horizon-specific | Manifest |
| fold_id | integer | — | derived | Rolling-origin fold identifier | 1–6 | Public |
| sample_id | string | — | derived | Unique common evaluation sample | Must be unique | Public if safe |
