# GATE-FCD Chinese–English Semantic Audit Report

Sources:

- Meaning source of truth: `GATE-FCD_AJSE_中文正文优化_第六章与结论_20260815.docx`
- English source: `GATE_FCD_AJSE_English_Translation_20260815.docx`
- Audited output: `Humanizer_english.docx`

The Humanizer pass and the semantic audit were carried out as separate stages. The English was first edited for natural academic style under a number/citation lock. The resulting document was then compared independently with the Chinese meaning source of truth.

| Section | CN–EN semantic status | Issues found | Fix applied |
| --- | --- | --- | --- |
| 1 Introduction | PASS_WITH_MINOR_STYLE_DIFFERENCE | Some sentences retained source-language sequencing and repeated transitions. | Restructured sentences without changing the research gap, four questions, four contributions, or framework positioning. |
| 2 Literature Review and Research Gap | PASS_WITH_MINOR_STYLE_DIFFERENCE | Mechanical transitions and dense sentence rhythm. | Improved cohesion while preserving all cited studies, citation numbers, and the stated research gap. |
| 3 Study Area and FCD | PASS_WITH_MINOR_STYLE_DIFFERENCE | No substantive drift. | Clarified that the analyzed quantity is FCD-reported speed and not an independently measured reference. |
| 4 GATE-FCD Methodology | PASS_WITH_MINOR_STYLE_DIFFERENCE | One passage needed a more explicit boundary between the framework and the benchmark models. | Restored the explicit statement that the six models validate the framework and are not evidence for a new model architecture. All processing order, equations, frozen rules, and target definitions were retained. |
| 5 Results | PASS_WITH_MINOR_STYLE_DIFFERENCE | Descriptive and inferential wording required close calibration. | Preserved the descriptive XGBoost ordering, the close SeasonalHA results, the fold-level uncertainty, and the absence of a universal winner. |
| 6 Discussion | PASS_WITH_MINOR_STYLE_DIFFERENCE | Several long sentences and repeated framing phrases. | Improved rhythm while retaining horizon dependence, simple-baseline competitiveness, practical/statistical distinction, engineering implications, and every limitation. |
| 7 Conclusions | PASS_WITH_MINOR_STYLE_DIFFERENCE | The English used worded forms of the frozen statistical count. | Normalized three occurrences of “none of the 15” to `0/15` to match the Chinese source and frozen contract; no result changed. |
| Tables 1–5 | PASS | No content drift. | No table text, value, unit, row meaning, or ranking was modified. |
| Figure captions and notes | PASS_WITH_LIMITATIONS | Captions and notes match the Chinese source, but the supplied source artwork contains internal label conflicts described below. | No image was modified, as required. |
| References | PASS | No change detected. | References and DOI strings remain byte-for-byte identical at paragraph level. |

## Locked meanings confirmed

- GATE-FCD remains an auditable engineering/evidence-construction framework, not a new predictor, imputation method, neural network, or universally superior model.
- The target remains future-window mean FCD-reported speed for H1, H3, and H6.
- Evaluation remains six-fold retrospective rolling-origin evaluation; Fold 6 historical exposure is retained.
- The primary statistical unit remains the rolling-origin fold (`n = 6` paired folds).
- XGBoost has the lowest descriptive fold-macro mean MAE, while SeasonalHA remains close.
- `0/15` prespecified comparisons are statistically significant after Holm adjustment; non-significance is not described as equivalence.
- Horizon- and reliability-conditioned model selection remains the final engineering conclusion.

## Source-artwork limitations

`SOURCE_TEXT_POTENTIAL_INCONSISTENCY`

1. Figure 3 states “fold-training mode median,” whereas the Chinese manuscript, English methods, Equation (5), and frozen protocol specify “fold-training node median.”
2. Figure 3 contains the truncated label “100% assertion passi” in the audit panel.
3. Figure 4(b) displays H6 as `(25/6)` and visually repeats a terminal “6,” whereas the manuscript, table, equation, caption, and frozen protocol specify H6 eligibility as at least `5/6` across future hours 1–6.

These issues pre-existed in the supplied image files and were not introduced or corrected by the Humanizer pass because image modification was prohibited.

`SEMANTIC_AUDIT_STATUS = PASS_WITH_LIMITATIONS`
