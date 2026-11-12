# QA REPORT - Leo's Little Lines

Generated 2026-11-12 23:16 by `tb_build.py`. Every PASS/FAIL below was executed in this build.

**Summary: 47 PASS · 8 NEEDS HUMAN REVIEW · 0 FAIL**

## PASS (47)

- **[US_Letter] exactly 72 interior pages numbered 1-72** - 72 pages
- **[US_Letter] chapter page counts match the approved plan** - {'intro': 4, 'lines': 12, 'shapes': 10, 'paths': 8, 'numbers': 10, 'letters': 26, 'finish': 2}
- **[US_Letter] letters A-Z each appear once and every picture word starts with its letter** - A=Apple, B=Bee, C=Car, D=Duck, E=Elephant, F=Fish, G=Gift, H=Hen, I=Ice cream, J=Jumper, K=Kite, L=Lion, M=Monkey, N=Nest, O=Octopus, P=Penguin, Q=Quilt, R=Rabbit, S=Sun, T=Turtle, U=Umbrella, V=Volcano, W=Watermelon, X=Xylophone, Y=Yo-yo, Z=Zebra
- **[US_Letter] numbers 1-10 in order and every count-and-colour group shows the right number of pictures** - 20 groups verified (pictures + dots match the number)
- **[US_Letter] all artwork, text and tracing lines inside the 0.5 in safe margin (KDP minimum is 0.375 in)** - every element checked
- **tracing strokes defined for A-Z and 1-10** - 26 letters + 10 numbers, stroke order marked with numbered green start dots
- **[US_Letter] dotted tracing lines are thick enough for toddlers (>= 4 pt dots)** - big guides 5.5-6 pt dots on 20-26 pt soft tracks; small copies 4-4.5 pt
- **[US_Letter] every character exists in its font (no missing glyphs)** - all text glyphs present in Fredoka / Nunito
- **[US_Letter] no clipped text (all text fits its box)** - no overflow after layout
- **[US_Letter] no overlapping text** - pairwise check of rendered text extents
- **[US_Letter] no unreadably small text (min 6pt adult notes; mission instructions >= 12pt)** - smallest text 8.0pt (adult reference table); smallest child-facing heading 8.0pt
- **[US_Letter] Leos_Little_Lines_US_Letter.pdf has 73 pages** - 73 pages
- **[US_Letter] Leos_Little_Lines_US_Letter.pdf page size verified** - [(612.0, 792.0)] pt, expected (612.0, 792.0) pt
- **[US_Letter] Leos_Little_Lines_US_Letter.pdf fonts embedded** - Fredoka-Bold, Nunito-Bold, Nunito-ExtraBold, Nunito-Regular
- **[US_Letter] Leos_Little_Lines_US_Letter.pdf text extraction works on every page** - all pages
- **[US_Letter] every page renders (no blank or corrupt pages)** - 73 pages rasterised; blank: none
- **[A4] exactly 72 interior pages numbered 1-72** - 72 pages
- **[A4] chapter page counts match the approved plan** - {'intro': 4, 'lines': 12, 'shapes': 10, 'paths': 8, 'numbers': 10, 'letters': 26, 'finish': 2}
- **[A4] letters A-Z each appear once and every picture word starts with its letter** - A=Apple, B=Bee, C=Car, D=Duck, E=Elephant, F=Fish, G=Gift, H=Hen, I=Ice cream, J=Jumper, K=Kite, L=Lion, M=Monkey, N=Nest, O=Octopus, P=Penguin, Q=Quilt, R=Rabbit, S=Sun, T=Turtle, U=Umbrella, V=Volcano, W=Watermelon, X=Xylophone, Y=Yo-yo, Z=Zebra
- **[A4] numbers 1-10 in order and every count-and-colour group shows the right number of pictures** - 20 groups verified (pictures + dots match the number)
- **[A4] all artwork, text and tracing lines inside the 0.5 in safe margin (KDP minimum is 0.375 in)** - every element checked
- **tracing strokes defined for A-Z and 1-10** - 26 letters + 10 numbers, stroke order marked with numbered green start dots
- **[A4] dotted tracing lines are thick enough for toddlers (>= 4 pt dots)** - big guides 5.5-6 pt dots on 20-26 pt soft tracks; small copies 4-4.5 pt
- **[A4] every character exists in its font (no missing glyphs)** - all text glyphs present in Fredoka / Nunito
- **[A4] no clipped text (all text fits its box)** - no overflow after layout
- **[A4] no overlapping text** - pairwise check of rendered text extents
- **[A4] no unreadably small text (min 6pt adult notes; mission instructions >= 12pt)** - smallest text 8.0pt (adult reference table); smallest child-facing heading 8.0pt
- **[A4] Leos_Little_Lines_A4.pdf has 73 pages** - 73 pages
- **[A4] Leos_Little_Lines_A4.pdf page size verified** - [(595.3, 841.9)] pt, expected (595.3, 841.9) pt
- **[A4] Leos_Little_Lines_A4.pdf fonts embedded** - Fredoka-Bold, Nunito-Bold, Nunito-ExtraBold, Nunito-Regular
- **[A4] Leos_Little_Lines_A4.pdf text extraction works on every page** - all pages
- **[A4] every page renders (no blank or corrupt pages)** - 73 pages rasterised; blank: none
- **[KDP] KDP_Interior_8.5x11_NoBleed.pdf has 72 pages** - 72 pages
- **[KDP] KDP_Interior_8.5x11_NoBleed.pdf page size verified** - [(612.0, 792.0)] pt, expected (612.0, 792.0) pt
- **[KDP] KDP_Interior_8.5x11_NoBleed.pdf fonts embedded** - Fredoka-Bold, Nunito-Bold, Nunito-ExtraBold, Nunito-Regular
- **[KDP] KDP_Interior_8.5x11_NoBleed.pdf text extraction works on every page** - all pages
- **[KDP] KDP_Cover_8.5x11_72pages.pdf has 1 pages** - 1 pages
- **[KDP] KDP_Cover_8.5x11_72pages.pdf page size verified** - [(1253.7, 810.0)] pt, expected (1253.7, 810.0) pt
- **[KDP] KDP_Cover_8.5x11_72pages.pdf fonts embedded** - Fredoka-Bold, Nunito-Bold, Nunito-Regular
- **[KDP] KDP_Cover_8.5x11_72pages.pdf text extraction works on every page** - all pages
- **KDP standard colour minimum page count (72)** - 72 interior pages
- **KDP cover size computed from page count** - 17.4121 x 11.2500 in = 0.125 bleed + 8.5 back + 0.1621 spine (72 x 0.002252) + 8.5 front + 0.125 bleed; no spine text (KDP needs 79+ pages)
- **KDP barcode area (2.0 x 1.2 in, back cover bottom-right) kept clear** - clear
- **editable PPTX opens in LibreOffice and renders every slide** - 72 slides rendered
- **customer pack contains only the three customer PDFs** - Leos_Little_Lines_A4.pdf, Leos_Little_Lines_US_Letter.pdf, Start_Here_Printing_Guide.pdf
- **SEO title / meta within Shopify limits** - title 52, meta 134 chars
- **no fake reviews, awards or scarcity in customer-facing copy** - none

## NEEDS HUMAN REVIEW (8)

- **spelling and grammar** - pyspellchecker (en) on 306 distinct words: 21 flags are halves of the two-colour picture words (e.g. 'A' + 'pple'), 3 are playful words (buzzy, pitter, zag); remaining flags: none. Grammar not machine-checked.
- **Physical print test** - Not run (no printer here). Print a few pages at Actual size; check dotted lines are visible but light and crayon works well.
- **KDP proof copy** - Not run. Upload the interior + cover to KDP, use the online previewer, and order a printed proof before publishing. Confirm the spine width in KDP's cover calculator (computed here as 0.1621 in) and that standard colour is offered for 8.5 x 11 in your marketplace.
- **Letter and number stroke shapes** - Strokes follow a simple print style (uppercase, top-to-bottom). An early-years educator should confirm the stroke order matches what local preschools teach.
- **Proofreading** - Spell-check run (see PASS list); a human read-through is still needed.
- **Visual review** - All 72 pages of both editions were rendered and inspected on screen during production (Visual_Review folder).
- **Canva import** - Not tested (no Canva account). LibreOffice opens the PPTX.
- **Safety wording** - Supervision with crayons/pencils is stated on p3, the back cover, the Start Here guide and the listing. Check local rules; not legal advice.

## FAIL (0)

None.
