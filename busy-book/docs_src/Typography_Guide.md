# Typography Guide – Little Worlds Learning · My Magic Busy Book

| Role | Font | Size in the book | Where |
|---|---|---|---|
| Cover title | Fredoka Bold | 57–74 pt | Cover |
| Mission titles | Fredoka Bold | 24.5–26 pt (auto-fit, minimum 17 pt) | Header of every mission page |
| Mission pill, labels on boards | Fredoka Bold | 11–20 pt | "MISSION 01", colour words, shape names, feeling words |
| Child instruction | Nunito Bold | 14.5 pt (minimum 11 pt) | Header of every mission page – written to be read aloud by an adult |
| Numbers on number cards | Fredoka Bold | 46 pt + matching dots | Cut-out sheet 3 |
| Parent notes / guides | Nunito Regular | 9–10.5 pt | Pages 3, 46, 48, printing guide |
| Piece IDs, small labels | Nunito ExtraBold / Bold | 7–9 pt | Cut-out cards (adult-facing) |
| Adult reference table | Nunito Regular / Bold | 6.1–6.6 pt | Page 46 only (detailed answer key also in 02_CONTENT/Answer_Key.md) |

## Licences
Fredoka, Nunito and Tajawal: SIL Open Font License 1.1 (licence files in `04_EDITABLE/Production_Source/fonts`). Free for commercial use and PDF embedding. Fonts are embedded (subset) in every PDF.

## Static instances
Google Fonts ships Fredoka and Nunito as variable fonts. The production pipeline creates static instances (Fredoka Bold 700, Fredoka SemiBold 600, Nunito Regular 400, Bold 700, ExtraBold 800) with fontTools and names them correctly so PowerPoint, LibreOffice and Canva match them.

## Fonts in the editable PPTX / Canva
Text boxes request **Fredoka** (bold) and **Nunito** (regular, bold) and **Nunito ExtraBold**. Install the fonts from `Production_Source/fonts` before editing in PowerPoint. In Canva, Fredoka and Nunito are available in the font library; if an imported text box shows a substitute font, select it and choose Fredoka / Nunito.

## Glyph rule
Fredoka and Nunito do not contain arrows (→), scissors (✂), stars (★) or hearts (♥). Use drawn shapes or icons instead. The QA pipeline checks every character against the font it uses.

## Future languages
- **Arabic / bilingual:** use Tajawal Bold for headings and Noto Sans Arabic or Tajawal for body text; mirror layouts right-to-left (mission pill and star swap sides). All child-facing strings live in `02_CONTENT/Text_Content_EN.json` and `src/content.py` for translation.
- **German:** expect ~30 % longer strings. Every text box in the layout engine auto-shrinks to a minimum size and the QA run reports any overflow, so translated builds can be verified the same way.
