# Little Worlds Learning · My Magic Busy Book (Product 03) — Publisher Production Folder

**My Magic Busy Book: 36 Little Missions to Match, Sort, Count & Play!**
48-page printable activity book · ages 3–5 with adult help · US Letter + A4 · v1.0 (November 2026) · suggested price AUD $9.99

## Folder map
| Folder | Contents |
|---|---|
| `01_BRAND` | Brand_Guide.pdf (colours, type, icons, rules, Leo character sheet) · Brand_Colours.json · Typography_Guide.md · Leo_Character_Sheet.svg |
| `02_CONTENT` | Complete_Page_Plan.csv (48 pages) · Activity_Manifest.csv (36 missions) · Piece_Inventory.csv (97 cards + optional reward stars) · Answer_Key.md · Text_Content_EN.json (all page text, for translation) |
| `03_ILLUSTRATIONS` | Every original SVG, grouped by theme; `14_activity_components_cutout_cards` = one SVG per cut-out card; `15_board_hints_silhouettes` = shadow / hint outlines used on boards |
| `04_EDITABLE` | Magic_Busy_Book_Editable.pptx (US Letter master, 48 slides, native text + shapes, adult tips in slide notes) · Magic_Busy_Book_Editable_A4.pptx · `Sections_for_Canva/` (5 smaller PPTX files) · `Production_Source/` (Python source, fonts + licences, copy) — the real master |
| `05_CUSTOMER_FILES` | Magic_Busy_Book_US_Letter.pdf · Magic_Busy_Book_A4.pdf · Start_Here_Printing_Guide.pdf |
| `06_SHOPIFY` | Cover.png · Product_Image_1–5 · Product_Description.html · SEO.txt (title, meta, handle, collections, alt text) · Product_Tags.txt · Preview.pdf (watermarked) |
| `07_MARKETING` | Instagram_Captions.md · Reel_Scripts.md · Pinterest_Copy.md · Facebook_Ad_Concepts.md · Launch_Email.md · Free_Sample_Activity.pdf + notes |
| `08_QA` | QA_Report.md (PASS / NEEDS HUMAN REVIEW / FAIL) · PDF_Validation_Report.md · Activity_Validation_Report.md · Licensing_Records.md · Known_Limitations.md · Spelling_Wordlist.txt · `Visual_Review/` (every page of both editions as PNG, contact sheets, PPTX re-render, cover thumbnails) |

The customer delivery pack is kept **outside** this folder: `dist/CUSTOMER_FILES/` (the three files + an optional labelled ZIP). It contains no editable publisher files.

## Book structure
- p1 cover · p2 "This book belongs to" · p3 grown-up setup guide + safety · p4 Mission Map
- p5–40: 36 missions in six worlds — Colour Kingdom (5–10), Animal Island (11–16), Number Town (17–22), Feelings Forest (23–28), Everyday Village (29–34), Adventure Land (35–40)
- p41–45: five cut-out sheets (97 cards, each 1.55 in / 39 mm square, 0.28 in cutting space)
- p46 grown-up reference & answer key · p47 certificate + six reward stars · p48 back cover

Every mission page has: MISSION number, playful title, child instruction, skill icon with text label, achievement star, and a footer telling the adult exactly which cards (and which sheet) it needs — or that it is a no-cut activity.

## Rebuild / edit
```
pip install reportlab svglib cairosvg python-pptx pypdf pillow fonttools
python3 Production_Source/src/build.py      # (needs poppler-utils; LibreOffice optional for the PPTX check)
```
Edit text in `src/content.py`, layouts in `src/pages.py`, artwork in `src/art_core.py` / `src/art_lib.py`. The build regenerates every file and re-runs QA.

## Shopify delivery recommendation
Attach the three PDFs from `CUSTOMER_FILES` individually (no unzipping needed on phones/tablets) if your digital-download app allows several files per product; otherwise attach `Magic_Busy_Book_Customer_Files.zip`. Do not attach anything from this publisher folder. Nothing has been published automatically.
