# GATE-FCD AJSE English Final QA Report

## Three-pass verification

1. **Humanizer pass:** Academic-English editing under number and citation locks; 46 initial narrative paragraphs refined.
2. **Independent content pass:** Paragraph-by-paragraph Chinese–English meaning audit, numerical audit, statistical-claim audit, terminology audit, and figure/table/reference audit. Semantic fixes were applied only to the English document.
3. **Final integrity pass:** Reopened and reparsed the final DOCX; rechecked structure, values, citations, tables, media, references, high-risk phrases, and Chinese characters; rendered the document with Microsoft Word and visually inspected all 38 pages.

## Required QA questions

| # | Question | Answer |
| ---: | --- | --- |
| 1 | Are the Chinese and English meanings consistent? | Yes for the manuscript text; source-artwork limitations are listed below. |
| 2 | Did the English add new research meaning? | No. |
| 3 | Was the experimental logic changed? | No. |
| 4 | Was any numerical result changed? | No. Three worded forms of “none of 15” were normalized to `0/15` without changing the result. |
| 5 | Was the model ranking changed? | No. |
| 6 | Was the meaning of statistical significance changed? | No. |
| 7 | Was independent/blind-test language used incorrectly? | No. The retrospective evaluation and Fold 6 exposure are explicit. |
| 8 | Is FCD-reported speed used correctly? | Yes. It is not presented as independent ground truth. |
| 9 | Are all limitations retained? | Yes. |
| 10 | Is GATE-FCD still positioned as an engineering framework? | Yes. It is not presented as a new predictor, imputation algorithm, or neural-network architecture. |
| 11 | Are Figure/Table references consistent? | Textual numbering, captions, notes, and tables are consistent; the supplied Figure 3 and Figure 4 artwork contains the source-level issues below. |
| 12 | Are the references unchanged? | Yes; all reference paragraphs and DOI strings are identical. |
| 13 | Is any Chinese text left in the English DOCX? | No; Unicode CJK count = 0. |
| 14 | Is obvious machine translation still present? | No material machine-translation pattern was found in the final review. |
| 15 | Is obvious AI filler still present? | No prohibited AI-style filler or high-risk phrase remained in the final scan. |

## Structural and visual integrity

- Paragraphs: 202 in the Chinese source, original English, and final English.
- Tables: 5 in all three documents; final dimensions are 12×2, 11×5, 7×4, 12×2, and 7×4.
- Inline shapes/objects: 17 in all three documents.
- Sections: 1 in all three documents.
- Final rendering: 38 pages; every page was visually inspected. No clipping, overlap, broken image, missing table, or truncated equation was found.
- The narrow columns in Table 2 retain the source layout and cause some line wrapping, but no text is missing or clipped.
- Figures 1, 2, 4, 6, and 7 match the supplied PNG files byte-for-byte. The embedded Figure 3 and Figure 5 are inherited size/export variants of the supplied PNGs; visual comparison confirmed the same scientific content, and the embedded media are unchanged from the original English DOCX.

## Source-level issues not altered

`SOURCE_TEXT_POTENTIAL_INCONSISTENCY`

1. **Figure 3, causal-history box:** “fold-training mode median” conflicts with “fold-training node median” in the Chinese source, Equation (5), Table 2, and the English methods.
2. **Figure 3, audit box:** the artwork contains the truncated wording “100% assertion passi.”
3. **Figure 4(b), H6 target row:** the artwork displays `(25/6)` and repeats a terminal “6.” This conflicts with the frozen H6 eligibility rule of at least `5/6` over future hours 1–6, which is stated correctly in the Chinese source, English manuscript, tables, equations, caption, and note.

The supplied figures were not changed. Because Figure 4 contains a frozen-rule conflict, the figure/table/reference audit cannot be marked PASS until the source artwork is corrected by the author.

## Final status

```text
========================================
GATE-FCD AJSE ENGLISH FINALIZATION
========================================

HUMANIZER_SKILL = FOUND

SOURCE_CN = GATE-FCD_AJSE_中文正文优化_第六章与结论_20260815.docx
SOURCE_EN = GATE_FCD_AJSE_English_Translation_20260815.docx

SEMANTIC_AUDIT_STATUS = PASS_WITH_LIMITATIONS
NUMERICAL_CONSISTENCY = PASS
STATISTICAL_CLAIM_AUDIT = PASS
TERMINOLOGY_AUDIT = PASS
FIGURE_TABLE_REFERENCE_AUDIT = FAIL
CHINESE_CHARACTER_SCAN = PASS
REFERENCES_INTEGRITY = PASS

AJSE_ENGLISH_FINAL_QA = PASS_WITH_LIMITATIONS

OUTPUT:
Humanizer_english.docx
02_CN_EN_SEMANTIC_AUDIT_REPORT.md
03_NUMERICAL_CONSISTENCY_AUDIT.md
04_STATISTICAL_CLAIM_AUDIT.md
05_HUMANIZER_CHANGELOG.md
06_FINAL_QA_REPORT.md

NEXT_STAGE_ALLOWED = NO
```
