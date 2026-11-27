# GATE-FCD Chinese–English Semantic Audit Report

Sources:

- Meaning source of truth: `GATE-FCD_AJSE_中文正文优化_第六章与结论_20260815.docx`
- English source: `Humanizer_english.docx`
- Audited output: `Humanizer_english_AJSE_FINAL.docx`

The Humanizer editing stage and the semantic/data audit were kept separate. Sentence splitting was performed under numeric and citation locks. The final text was then checked independently against the Chinese meaning source and the frozen English scientific contract.

| Section | Final status | Verified boundary |
| --- | --- | --- |
| Abstract | PASS | Ten-sentence summary uses only evidence already present in the manuscript. |
| 1 Introduction | PASS | Research problem, corridor context, four questions, and four contributions remain unchanged. |
| 2 Literature Review | PASS | Cited studies and the stated research gap remain unchanged; only sentence structure was simplified. |
| 3 Study Area and FCD | PASS | FCD-reported speed remains provider-derived and is not presented as independent ground truth. |
| 4 Methodology | PASS | Complete-grid reconstruction, eligibility gating, causal processing, common manifests, and audit order remain unchanged. |
| 5 Results | PASS | Descriptive ranking, uncertainty, fold dependence, reliability boundaries, and all values remain unchanged. |
| 6 Discussion | PASS | Horizon dependence, simple-baseline competitiveness, practical/statistical distinction, and limitations remain unchanged. |
| 7 Conclusions | PASS | The conclusion remains horizon- and reliability-conditioned and does not claim a universal winner. |
| Tables 1–5 | PASS | Table structure and cell text are identical to the source English DOCX. |
| References | PASS | All reference paragraphs and DOI strings are identical to the source English DOCX. |
| Embedded media | PASS | All 17 embedded media files have unchanged SHA-256 hashes. |

## Locked meanings confirmed

- GATE-FCD remains an auditable engineering and evidence-construction framework, not a new predictor, imputation algorithm, or neural-network architecture.
- The target remains future-window mean FCD-reported speed for H1, H3, and H6.
- Evaluation remains six-fold retrospective rolling-origin evaluation; Fold 6 historical exposure remains explicit.
- The primary inferential unit remains the rolling-origin fold (`n = 6`).
- XGBoost has the lowest descriptive fold-macro mean MAE, while SeasonalHA remains close.
- `0/15` comparisons are significant after Holm adjustment; non-significance is not treated as equivalence.
- Model choice remains conditioned on forecast horizon and data reliability.

## Source-artwork limitations

The supplied figures were intentionally left unchanged.

1. Figure 3 states “fold-training mode median,” while the manuscript and Equation (5) specify “fold-training node median.”
2. Figure 3 contains the truncated label “100% assertion passi.”
3. Figure 4(b) displays H6 as `(25/6)` and repeats a final “6,” while the frozen manuscript rule is at least `5/6` across future hours 1–6.

`SEMANTIC_AUDIT_STATUS = PASS_WITH_SOURCE_ARTWORK_LIMITATIONS`

