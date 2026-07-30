# Time-grid audit

Timezone is frozen to Asia/Kuala_Lumpur (UTC+08:00). Source timestamps are local wall-clock values and are floored to 15 minutes; hours are half-open `[hour_start, hour_start+1h)` bins.

- First raw timestamp: 2025-12-08 13:15:00.
- First complete confirmatory hour: 2025-12-08 14:00:00.
- Last raw timestamp: 2026-02-28 23:45:00.
- Last complete hour: 2026-02-28 23:00:00.
- The partial 13:00 start hour contains 126 raw records and is excluded from the confirmatory panel.
- Legacy 15-min denominator: 403,665; new complete-bin denominator: 403,512.
- Legacy hourly denominator: 100,980; new complete-hour denominator: 100,878.
- Boundary exclusion removes 153 theoretical node×15-min slots and 102 node×hour rows.

Actual missing observations do not change these theoretical denominators.
