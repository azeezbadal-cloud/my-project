# Little Worlds Learning · Leo's Little Lines — My First Tracing Book (ages 2–4)

72 activity pages in a soft pastel style · Leo the Little Explorer · v1.0 (November 2026)
Sell as a printable PDF on Shopify (AUD $7.99 suggested) and as a paperback on Amazon KDP (US$9.99–11.99 suggested).

## Book structure (interior pages)
| Pages | Part |
|---|---|
| 1–4 | Title page · This book belongs to · Grown-up guide · My Tracing Journey (progress map) |
| 5–16 | Warm-up lines (straight, rain, slants, waves, zig-zags, hops, rainbow arches, bubbles, loops, snail swirls, line parade) |
| 17–26 | Shapes (circle, square, triangle, rectangle, oval, star, heart, diamond, shape house, shape parade) |
| 27–34 | Paths (eight winding roads for Leo) |
| 35–44 | Numbers 1–10: trace + count & colour |
| 45–70 | Letters A–Z: trace + colour a picture (A Apple … Z Zebra) |
| 71–72 | Certificate · My best drawing |

## Folder map
| Folder | Contents |
|---|---|
| `01_CONTENT` | Page_Plan.csv · Text_Content_EN.json (all text, for translation) |
| `02_ILLUSTRATIONS` | Every artwork used, as SVG: `pastel/` and `line_art_colouring/` |
| `03_EDITABLE` | Leos_Little_Lines_Editable.pptx (72 slides, native text/shapes/dotted lines) · Production_Source (code + fonts) |
| `04_AMAZON_KDP` | KDP_Interior_8.5x11_NoBleed.pdf (72 pages) · KDP_Cover_8.5x11_72pages.pdf (wrap cover) · KDP_Listing.md (title, description, keywords, categories, settings) |
| `05_CUSTOMER_FILES` | Leos_Little_Lines_US_Letter.pdf · Leos_Little_Lines_A4.pdf (cover + 72 pages each) · Start_Here_Printing_Guide.pdf |
| `06_SHOPIFY` | Cover.png · 5 product images · description, SEO, tags |
| `07_MARKETING` | Instagram, Pinterest, launch email · Free_Sample_3_Pages.pdf |
| `08_QA` | QA_Report.md · Visual_Review (every page of both editions, KDP cover render) · licensing · known limitations |

Customer delivery files are also in `dist/CUSTOMER_FILES/` (plus a labelled ZIP). Never give customers the publisher folder.

## Publishing on Amazon KDP (short)
1. kdp.amazon.com → Create → Paperback.
2. Details: copy from `KDP_Listing.md`.
3. Content: ISBN (free KDP ISBN is fine) · Ink & paper: Standard colour, white · Trim 8.5 × 11 in · No bleed · Matte cover.
4. Upload `KDP_Interior_8.5x11_NoBleed.pdf` and `KDP_Cover_8.5x11_72pages.pdf` (upload your own cover PDF).
5. Launch the Previewer, fix anything it flags, order a proof copy, then set price and publish.

## Rebuild
`python3 Production_Source/tracing_src/tb_build.py` (needs the shared engine folder next to it, ReportLab, svglib, CairoSVG, python-pptx, pypdf, Pillow, poppler-utils).
