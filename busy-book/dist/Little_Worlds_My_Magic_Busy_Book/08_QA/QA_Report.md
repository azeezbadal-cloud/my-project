# QA REPORT - My Magic Busy Book

Generated 2026-11-08 04:37 by the automated production pipeline (`src/build.py`, `src/qa.py`). Version 1.0 · November 2026.

Every check below was actually executed in this build unless it says *Not run*. Automated checks do not replace human visual inspection.

**Summary: 52 PASS · 10 NEEDS HUMAN REVIEW · 0 FAIL**

## PASS (52)

- **[US_Letter] exactly 48 pages, numbered 1-48** - 48 pages built
- **[US_Letter] exactly 36 distinct mission pages on pages 5-40** - 36 missions, 36 distinct titles
- **[US_Letter] every mission has title, instruction, objective and adult guidance** - 36/36 complete
- **[US_Letter] five cut-out sheets on pages 41-45** - [41, 42, 43, 44, 45]
- **[US_Letter] all piece IDs unique** - 97 piece IDs; duplicates: none
- **[US_Letter] every inventory piece printed exactly once on the cut-out sheets** - 97 printed; missing none; duplicated none
- **[US_Letter] no orphan pieces (every piece used by a mission)** - orphans: none
- **[US_Letter] every required piece ID exists** - unknown: none
- **[US_Letter] boards <-> pieces mapping complete and every board solvable** - 26 piece missions solvable (bipartite matching), 10 no-cut missions with answers
- **[US_Letter] all cut-out pieces inside the 0.4in safe area with >=0.25in cutting space, no overlapping cut lines** - piece 1.55in square, gap >= 0.25in, all inside safe area
- **[US_Letter] no detachable piece smaller than 1.5in (small-parts cylinder is 1.25in)** - smallest piece 1.55in x 1.55in
- **[US_Letter] every board slot is large enough for its card and inside the safe area** - 124 slots checked (min 1.60in vs card 1.55in)
- **[US_Letter] number answers match pictured quantities** - 37 counted groups verified (balloons, cupcakes, cookies orders, card dots, comparison rows, tower helpers, finale apples)
- **[US_Letter] every character exists in its font (no missing glyphs)** - all text glyphs present in Fredoka / Nunito
- **[US_Letter] no clipped text (all text fits its box)** - no overflow after layout
- **[US_Letter] no overlapping text** - pairwise check of rendered text extents
- **[US_Letter] all interior text inside the 0.4in safe area** - ok
- **[US_Letter] no unreadably small text (min 6pt adult notes; mission instructions >= 12pt)** - smallest text 6.1pt (adult reference table); smallest child-facing heading 9.0pt
- **[US_Letter] PDF has exactly 48 pages** - Magic_Busy_Book_US_Letter.pdf: 48 pages
- **[US_Letter] PDF page size verified programmatically** - all pages [(612.0, 792.0)] pt; expected (612.0, 792.0) pt
- **[US_Letter] all fonts embedded** - embedded: Fredoka-Bold, Nunito-Bold, Nunito-ExtraBold, Nunito-Regular
- **[US_Letter] text extraction finds the expected title text on every page** - 48/48 pages
- **[US_Letter] every page renders (no corrupted or blank pages)** - 48 pages rasterised with pdftoppm; blank: none
- **[A4] exactly 48 pages, numbered 1-48** - 48 pages built
- **[A4] exactly 36 distinct mission pages on pages 5-40** - 36 missions, 36 distinct titles
- **[A4] every mission has title, instruction, objective and adult guidance** - 36/36 complete
- **[A4] five cut-out sheets on pages 41-45** - [41, 42, 43, 44, 45]
- **[A4] all piece IDs unique** - 97 piece IDs; duplicates: none
- **[A4] every inventory piece printed exactly once on the cut-out sheets** - 97 printed; missing none; duplicated none
- **[A4] no orphan pieces (every piece used by a mission)** - orphans: none
- **[A4] every required piece ID exists** - unknown: none
- **[A4] boards <-> pieces mapping complete and every board solvable** - 26 piece missions solvable (bipartite matching), 10 no-cut missions with answers
- **[A4] all cut-out pieces inside the 0.4in safe area with >=0.25in cutting space, no overlapping cut lines** - piece 1.55in square, gap >= 0.25in, all inside safe area
- **[A4] no detachable piece smaller than 1.5in (small-parts cylinder is 1.25in)** - smallest piece 1.55in x 1.55in
- **[A4] every board slot is large enough for its card and inside the safe area** - 124 slots checked (min 1.60in vs card 1.55in)
- **[A4] number answers match pictured quantities** - 37 counted groups verified (balloons, cupcakes, cookies orders, card dots, comparison rows, tower helpers, finale apples)
- **[A4] every character exists in its font (no missing glyphs)** - all text glyphs present in Fredoka / Nunito
- **[A4] no clipped text (all text fits its box)** - no overflow after layout
- **[A4] no overlapping text** - pairwise check of rendered text extents
- **[A4] all interior text inside the 0.4in safe area** - ok
- **[A4] no unreadably small text (min 6pt adult notes; mission instructions >= 12pt)** - smallest text 6.1pt (adult reference table); smallest child-facing heading 9.0pt
- **[A4] PDF has exactly 48 pages** - Magic_Busy_Book_A4.pdf: 48 pages
- **[A4] PDF page size verified programmatically** - all pages [(595.3, 841.9)] pt; expected (595.3, 841.9) pt
- **[A4] all fonts embedded** - embedded: Fredoka-Bold, Nunito-Bold, Nunito-ExtraBold, Nunito-Regular
- **[A4] text extraction finds the expected title text on every page** - 48/48 pages
- **[A4] every page renders (no corrupted or blank pages)** - 48 pages rasterised with pdftoppm; blank: none
- **AB / AAB patterns, sequences and matching orders are logically correct** - 6 patterns solved programmatically; every answer offered exactly once among 3 choices; line-matching columns are shuffled
- **US Letter and A4 editions have identical page order, boards, slots and piece-sheet allocation** - page numbers, answers and piece IDs identical in both editions
- **editable PPTX opens and renders 48 slides (LibreOffice)** - 48 slides; 1034 native text boxes, 978 native shapes/lines/freeforms, 768 separately replaceable artwork pictures; LibreOffice re-renders 48 pages
- **customer download pack contains exactly the three customer files (no editable publisher files)** - Magic_Busy_Book_A4.pdf, Magic_Busy_Book_US_Letter.pdf, Start_Here_Printing_Guide.pdf
- **SEO title and meta description within Shopify length limits** - title 54 chars, meta 143 chars
- **no fake reviews, ratings, awards or artificial scarcity in sales copy** - scan of customer-facing copy (description, captions, pins, email, tags, ad text): none found

## NEEDS HUMAN REVIEW (10)

- **Mascot consistency** - Leo was drawn from one parametric definition (same head, vest, shoes, backpack, colours) in every pose; contact sheets inspected on screen. Confirm on a physical print.
- **Overall visual quality / illustration style** - All 48 pages of both editions rendered and inspected at 50-60 dpi during production (see Visual_Review). A designer should review at 100% zoom and on paper.
- **Spelling and grammar** - pyspellchecker (en) run on all 653 distinct words in the book: flagged 2 for review: pdf, sil. Grammar was not machine-checked. Text was written in Australian/British English (colour, favourite). Human proofread required.
- **Cover readable at Shopify thumbnail size** - Cover_thumbnail_160px.png and _300px.png generated; title is ~70 pt on an 11 in cover (about 17 px tall letters at 160 px wide). Inspected on screen: title readable. Confirm in the Shopify theme.
- **Physical print test** - Not run - no printer in this environment. Print one copy of each edition at Actual size and check that the 1.55 in cards fit the 1.65 in boxes, colours are distinguishable and nothing is clipped by the printer.
- **Canva import of the PPTX** - Not testable here (no Canva account in this build). LibreOffice opens the PPTX and renders all 48 slides. See Known_Limitations.md for expected Canva behaviour.
- **Educational accuracy (animals, foods, habitats)** - Reviewed in production: see Activity_Validation_Report.md section 'Accuracy notes'. A second reviewer (early-childhood educator) should confirm.
- **Emotions, routines and stereotypes** - Feelings are shown on non-human round faces; adult notes state faces can mean different things; routines and day activities accept any explained answer; no gendered roles appear. Human sensitivity review recommended.
- **Safety wording** - Under-3 warning, adult preparation and supervision appear on p3, p41-45 footers, p48, the printing guide and the Shopify description. Check against the rules of the country you sell in (e.g. ACCC guidance in Australia); this is not legal advice.
- **Font licences** - Fredoka, Nunito and Tajawal are SIL Open Font License 1.1 (licence texts included). OFL permits embedding in PDFs and commercial use; confirm the fonts used inside Canva are licensed via Canva for your account.

## FAIL (0)

None.

## Part L checklist cross-reference

- 1 Exactly 48 pages: structure + PDF page count (both editions)
- 2 Exactly 36 distinct missions: structure
- 3 Five cut-out sheets contain every required piece: pieces
- 4 Cut-out references correct: pieces mapping + footer notes generated from the same data
- 5 Correct counting/matching answers: number answers + patterns
- 6 Consistent mascot: NEEDS HUMAN REVIEW
- 7 Consistent typography and colours: single font/colour system in code; brand guide
- 8 Spelling and grammar: NEEDS HUMAN REVIEW
- 9 No clipped text or illustrations: text overflow check + visual review
- 10 No unreadably small instructions: text size check
- 11 No overlapping cut lines: piece spacing check
- 12 No duplicated or missing pieces: pieces
- 13 No fonts failing to render: glyph coverage + font embedding
- 14 No corrupted or blank pages: PDF raster check
- 15 Both editions verified: all checks run for US Letter and A4
- 16 Cover readable at thumbnail size: NEEDS HUMAN REVIEW (thumbnails provided)
- 17 Original illustrations / licences: Licensing_Records.md
- 18 No fake photos or reviews: copy scan + mockup captions
- 19 Adult supervision info: NEEDS HUMAN REVIEW of wording; present on p3, p48, sheets, guide, listing
- 20 Customer pack correct: customer pack check