# Logic, Method, Results, and Contribution Review

## Overall assessment

The revised manuscript now presents a closed evidence chain:

`incomplete API returns → complete-grid reconstruction → eligibility gating → causal histories and targets → common manifests → retrospective rolling-origin evaluation → uncertainty and audit evidence → horizon- and reliability-conditioned engineering decision`

## Logic and contribution revisions

- The Introduction now states exactly four research questions. Model complexity is evaluated inside the third question instead of appearing as an unintended fifth question.
- The contribution is defined as an auditable evidence-construction protocol, not a new neural-network architecture or imputation algorithm.
- The opening two Discussion paragraphs were merged because they repeated the same comparison with earlier FCD studies.
- The revised Discussion first positions the upstream eligibility contribution, then interprets horizon-dependent model performance, statistical uncertainty, engineering selection, and limitations.
- Two remaining sentences above 30 words were split in the Study Area and Methodology sections without changing their technical meaning.

## Protected scientific content

The following content was preserved and rechecked:

- complete-grid reconstruction and record eligibility;
- 2-of-4 hourly aggregation;
- 24-h strictly causal history;
- H1, H3, and H6 future-window targets, including the H6 at-least-5-of-6 rule;
- common sample manifests;
- six-fold retrospective rolling-origin evaluation;
- 180/180 formal runs and 20/20 leakage assertions;
- XGBoost and SeasonalHA comparison;
- 0/15 Holm-adjusted significant comparisons;
- FCD-reported speed semantics;
- retrospective rather than prospective evidence level;
- limitations concerning one corridor, 51 nodes, approximately three months, discrete spatial coverage, and no independent reference speed.

## Result emphasis

The revised manuscript keeps the main result explicit but cautious. XGBoost has the lowest descriptive fold-macro MAE at H1, H3, and H6, but the differences from SeasonalHA are small and unstable across folds and reliability strata. All paired intervals cross zero, and no prespecified comparison is significant after Holm correction. The engineering conclusion is therefore horizon- and reliability-conditioned model selection, not a universal winner claim.

## Final narrative word count

| Section | Words |
|---|---:|
| Introduction | 864 |
| Literature Review and Research Gap | 948 |
| Study Area and FCD | 431 |
| GATE-FCD Methodology | 2,547 |
| Results | 1,362 |
| Discussion | 1,666 |
| Conclusions | 436 |
| Data and Code Availability | 46 |
| **Total narrative** | **8,300** |

The target range of approximately 8,300–8,500 words is met without reducing method reproducibility, results, statistical boundaries, or limitations.
