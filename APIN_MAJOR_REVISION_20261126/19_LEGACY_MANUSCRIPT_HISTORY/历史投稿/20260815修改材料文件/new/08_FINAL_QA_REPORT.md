# GATE-FCD AJSE Final QA Report

## Three completed checks

1. **Scientific consistency check:** The final text was aligned with the 202-paragraph source body. Numeric and citation-token mismatches were `0`; all locked data, model, target, and statistical meanings were confirmed.
2. **Language and AJSE check:** The Abstract was verified in Microsoft Word at 150 words and 10 sentences. The full text was checked for grammar, long sentences, AI-style phrasing, captions, keywords, and the data/code statement.
3. **File and visual check:** The final DOCX was reopened, parsed, exported with Microsoft Word, and rendered to 39 pages. Every page was inspected for clipping, overlap, broken images, truncated equations, broken tables, and hyperlink layout.

## Final integrity results

| Check | Result |
| --- | --- |
| Final paragraphs | 207 = 202 source + 3 front-matter + 2 data/code paragraphs |
| Tables | 5; content identical to source |
| Inline shapes | 17; unchanged |
| Embedded media | 17; all hashes unchanged |
| References | Exact paragraph-level match |
| Numeric/citation mismatches | 0 |
| Chinese characters | 0 |
| Figure captions | 7 in AJSE `Fig.` style |
| Active repository hyperlink | 1; target verified |
| Sentences over 30 words before References | 0 |
| High-risk statistical phrases | 0 |
| Targeted AI-style phrases | 0 |
| Rendered pages | 39; visually checked |

## Source-level limitations retained

The final manuscript is ready for author review, but the supplied figure artwork still contains three pre-existing issues:

1. Figure 3: “fold-training mode median” should be checked against the manuscript’s “fold-training node median.”
2. Figure 3: “100% assertion passi” is visibly truncated.
3. Figure 4(b): `(25/6)` and the repeated terminal “6” conflict with the manuscript’s frozen H6 rule of at least `5/6`.

These are image-source issues. The manuscript text, equations, tables, captions, and notes retain the correct frozen rules.

## Final status

```text
ABSTRACT_COMPLIANCE = PASS
SEMANTIC_AUDIT = PASS_WITH_SOURCE_ARTWORK_LIMITATIONS
NUMERICAL_CONSISTENCY = PASS
STATISTICAL_CLAIM_AUDIT = PASS
SENTENCE_AND_WORD_AUDIT = PASS
DATA_AND_CODE_AVAILABILITY = PASS
REFERENCES_INTEGRITY = PASS
TABLE_INTEGRITY = PASS
MEDIA_INTEGRITY = PASS
VISUAL_QA = PASS

AJSE_FINAL_QA = PASS_WITH_SOURCE_ARTWORK_LIMITATIONS
```

