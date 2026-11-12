# Known Limitations – My Magic Busy Book v1.0

Honest list of what this build does **not** do or could not verify.

## Not verified in this environment
1. **No physical print test.** There is no printer here. Both PDFs were rendered to images and inspected on screen; a person must print one copy of each edition at Actual size and check card fit, colour separation and cutting.
2. **No Canva import test.** No Canva account was used. The PPTX was verified by opening it with LibreOffice (48 slides rendered).
3. **Shopify not touched.** Nothing was uploaded or published. Delivery behaviour (multiple files vs ZIP) must be confirmed in your Shopify digital-download app before launch.
4. **Spelling** was checked against a word list where available; a human proofread is still required.

## Editable files
- **Illustrations in the PPTX are PNG pictures** (transparent, rendered at up to 300 dpi from the SVG masters), one picture per artwork so each can be replaced individually. PowerPoint/Canva cannot edit the inside of these drawings; edit the SVG masters in `03_ILLUSTRATIONS` (Illustrator, Inkscape, Figma or Canva's SVG upload) and re-place them.
- **Text, boxes, drop-zones, cut lines, dots and paths are native** PowerPoint text boxes / shapes / freeforms.
- **Expected Canva behaviour (not tested):** Canva's PPTX import generally keeps text boxes and basic shapes editable; dashed outlines, rounded-corner radii, line spacing and freeform paths may be simplified, and fonts may be substituted if not matched. If the 48-slide file is slow, use the five section files in `04_EDITABLE/Sections_for_Canva`.
- Rotated cover cards are pictures with a rotation applied.
- **The true master is the production source** (`04_EDITABLE/Production_Source`): editing `content.py` and re-running `python3 src/build.py` regenerates both PDFs, the PPTX, inventory, manifest, answer key and QA in one step and re-validates everything. Visual edits made only in Canva/PowerPoint will not be validated.
- The A4 PPTX is provided for convenience; Canva edits should start from the US Letter master or the sections.

## Design trade-offs
- Five cut-out sheets hold at most 100 cards at the safe size of 1.55 in. To avoid shrinking pieces, four card sets are shared between boards and 10 missions are no-cut (draw a line / circle the answer). This is documented on each page footer, page 46 and the inventory.
- Memory-game cards are printed single-sided; on thin paper a picture may show through when face-down. Card stock or a plain back sticker solves this.
- Mission 20 (Make a Happy Face) and Mission 35 (Find the Pairs) are open-ended; the "correct placement" is any eye card in the eye box / any mouth card in the mouth box, and any card on any memory spot.
- Mission 22 and Mission 30 accept any order the child can explain; the answer key gives one common order.
- The page 46 reference table uses 6.1–6.6 pt text to fit 36 rows on one page; the full answer key is also provided as `02_CONTENT/Answer_Key.md`.
- Paper pieces are larger than the small-parts test cylinder (1.25 in / 31.7 mm), but paper can tear: the product is labelled not suitable for under-3s and requires adult supervision. This is not a certified toy and no safety certification is claimed.
- No bleed version for professional printing was produced (not requested as a separate edition); interior art stays inside 0.5 in margins.

## Not included on purpose
- No contact details, trademarks, awards, certifications, reviews or ratings were invented.
- Instagram reels are scripts only; no video was produced.
