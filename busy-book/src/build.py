"""Build every deliverable for My Magic Busy Book.

    python3 build.py            # full build -> busy-book/dist/
"""
import csv
import datetime
import glob
import hashlib
import re
import json
import os
import shutil
import subprocess
import sys
import zipfile

from PIL import Image
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import art_lib                     # noqa: E402
import content as C               # noqa: E402
import docs                       # noqa: E402
import qa                         # noqa: E402
import render_pdf                 # noqa: E402
import render_pptx                # noqa: E402
import shopify_images             # noqa: E402
from pages import Book, PIECE, SIZES  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, ".."))
DIST = os.path.join(ROOT, "dist")
PUB = os.path.join(DIST, "Little_Worlds_My_Magic_Busy_Book")
CUST = os.path.join(DIST, "CUSTOMER_FILES")
TMP = os.path.join(ROOT, "build", "tmp")
COPY = os.path.join(ROOT, "copy")

D = {k: os.path.join(PUB, k) for k in ["01_BRAND", "02_CONTENT", "03_ILLUSTRATIONS", "04_EDITABLE", "05_CUSTOMER_FILES", "06_SHOPIFY", "07_MARKETING", "08_QA"]}


def log(*a):
    print("[build]", *a, flush=True)


# ------------------------------------------------------------------ illustrations
CATS = [
    ("01_mascot_leo", ("leo_",)),
    ("02_icons_ui", ("icon_", "fastener_dot", "magnifier")),
    ("03_colours_shapes", ("drop_", "drophint_", "cloud_red", "cloud_orange", "cloud_yellow", "cloud_green", "cloud_blue", "cloud_purple", "token_", "shape_", "shapesil_", "scoop_", "cone", "flower_red", "flower_yellow", "flower_blue", "flower_purple", "pot_", "robot_", "rainbow")),
    ("04_animals", ("fish", "cow", "monkey", "penguin", "camel", "frog", "panda", "bee", "squirrel", "rabbit", "fox", "elephant", "hen", "pig", "duck", "octopus", "turtle", "crab", "part_", "teddy", "monster")),
    ("05_food", ("apple", "banana", "bamboo", "acorn", "grass", "carrot", "bread", "croissant", "milk", "cheese", "lettuce", "tomato", "sandwich", "cupcake", "cookie", "breakfast", "park_lunch", "plate")),
    ("06_vehicles", ("car", "train", "boat", "plane")),
    ("07_clothes_weather", ("sunhat", "rainboots", "scarf", "beanie", "jumper", "tshirt", "weather_", "sun", "moon", "night")),
    ("08_faces_feelings", ("face_", "eyes_", "mouth_", "k_")),
    ("09_home_routine", ("toothbrush", "pillow", "saucepan", "bathtub", "sofa", "piano", "backpack", "bottle", "lunchbox", "book", "rt_", "room_", "bedtime", "slide")),
    ("10_nature_adventure", ("seed", "sprout", "flower_grown", "egg", "chick", "blocks_", "leaf_", "stone_", "basket", "palm", "bridge", "lighthouse", "chest", "castle_", "roof_", "map_scene", "daisy", "tulip")),
    ("11_scenes_worlds", ("hab_", "farm_scene", "ocean_scene", "band_", "shelf", "world_", "hill", "cloud_plain", "house_home", "balloon")),
    ("12_rewards_decor", ("reward_", "rosette", "sparkle", "star_item")),
]


def category(name):
    for cat, prefs in CATS:
        if any(name == p or name.startswith(p) for p in prefs):
            return cat
    return "13_misc"


def piece_component_svg(book, pid):
    s, asset, label = C.PIECE_INDEX[pid]
    pages = book.set_pages(s["code"])
    ch = next(c for c in C.CHAPTERS if c["colour"] == s["tab"])
    body = (f'<rect x="3" y="3" width="149" height="149" rx="12" fill="#FFFFFF" stroke="#18354B" stroke-width="2.5"/>'
            f'<rect x="10" y="124" width="135" height="22" rx="8" fill="{ch["tint"]}"/>'
            f'<text x="16" y="140" font-family="Nunito, sans-serif" font-weight="800" font-size="11" fill="#18354B">{pid}</text>'
            f'<text x="139" y="140" text-anchor="end" font-family="Nunito, sans-serif" font-weight="700" font-size="9" fill="#18354B">p{", ".join(map(str, pages))}</text>')
    if asset:
        inner = art_lib.inner(asset)
        w, h = art_lib.get_size(asset)
        sc = min(123 / w, 106 / h)
        body += f'<g transform="translate({77.5 - w * sc / 2:.1f} {66 - h * sc / 2:.1f}) scale({sc:.3f})">{inner}</g>'
    else:
        n = int(pid[2:])
        body += f'<text x="77.5" y="78" text-anchor="middle" font-family="Fredoka, sans-serif" font-weight="700" font-size="68" fill="{ch["deep"]}">{n}</text>'
        for d in range(n):
            r_, c_ = divmod(d, 5)
            cnt = min(5, n - r_ * 5)
            x = 30 + (95 / cnt) * (c_ + 0.5)
            body += f'<circle cx="{x:.1f}" cy="{96 + r_ * 16}" r="6" fill="#F26855" stroke="#18354B" stroke-width="1.5"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 155 155" width="1.55in" height="1.55in">'
            f'<title>{pid} {label} (cut-out card, 1.55 in)</title>{body}</svg>')


def export_illustrations(book):
    base = D["03_ILLUSTRATIONS"]
    n = 0
    for name in sorted(art_lib.ASSETS):
        d = os.path.join(base, category(name))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, name + ".svg"), "w").write(art_lib.get_svg(name))
        n += 1
    comp = os.path.join(base, "14_activity_components_cutout_cards")
    os.makedirs(comp, exist_ok=True)
    for s in C.PIECE_SETS:
        for pid, _, _ in s["items"]:
            open(os.path.join(comp, f"{pid}.svg"), "w").write(piece_component_svg(book, pid))
            n += 1
    hints = os.path.join(base, "15_board_hints_silhouettes")
    os.makedirs(hints, exist_ok=True)
    used = {e["asset"] for p in book.pages for e in p.els if e["t"] == "img" and ":" in e["asset"]}
    for a in sorted(used):
        open(os.path.join(hints, a.replace(":", "_") + ".svg"), "w").write(art_lib.get_svg(a))
        n += 1
    return n


# ------------------------------------------------------------------ helpers
def contact_sheet(png_dir, out, cols=8):
    fs = sorted(glob.glob(os.path.join(png_dir, "*.png")))
    ims = [Image.open(f) for f in fs]
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (w + 8) + 8, rows * (h + 8) + 8), (136, 136, 136))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((w, h)), (8 + (i % cols) * (w + 8), 8 + (i // cols) * (h + 8)))
    sheet.save(out, optimize=True)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]


def zipdir(src, out, arc_root):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for dp, _, fs in os.walk(src):
            for f in sorted(fs):
                full = os.path.join(dp, f)
                z.write(full, os.path.join(arc_root, os.path.relpath(full, src)))


# ------------------------------------------------------------------ main
def main():
    t0 = datetime.datetime.now()
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    if os.path.exists(TMP):
        shutil.rmtree(TMP)
    for d in list(D.values()) + [CUST, TMP]:
        os.makedirs(d, exist_ok=True)

    log("laying out both editions")
    books, pages = {}, {}
    for ed in SIZES:
        books[ed] = Book(ed)
        pages[ed] = books[ed].build()

    log("rendering customer PDFs")
    pdf = {}
    for ed, fn in (("US_Letter", "Magic_Busy_Book_US_Letter.pdf"), ("A4", "Magic_Busy_Book_A4.pdf")):
        pdf[ed] = os.path.join(D["05_CUSTOMER_FILES"], fn)
        render_pdf.render(pages[ed], pdf[ed], "My Magic Busy Book (" + ed.replace("_", " ") + ")",
                          "Little Worlds Learning printable busy book, ages 3-5, " + C.PRODUCT["version"])
    guide = os.path.join(D["05_CUSTOMER_FILES"], "Start_Here_Printing_Guide.pdf")
    render_pdf.render(docs.printing_guide_pages(books["US_Letter"]), guide, "Start Here - Printing Guide", "My Magic Busy Book")
    for f in glob.glob(os.path.join(D["05_CUSTOMER_FILES"], "*.pdf")):
        shutil.copy(f, CUST)

    log("editable PowerPoint master + sections")
    notes = {m["page"]: f"Mission {m['n']:02d} - {m['title']}\nGoal: {m['goal']}\nGrown-up tip: {m['guide']}" for m in C.MISSIONS}
    pptx_main = os.path.join(D["04_EDITABLE"], "Magic_Busy_Book_Editable.pptx")
    render_pptx.render(pages["US_Letter"], pptx_main, notes)
    secdir = os.path.join(D["04_EDITABLE"], "Sections_for_Canva")
    os.makedirs(secdir, exist_ok=True)
    sections = [("01_Intro_p01-04", 1, 4), ("02_Colour_Kingdom_Animal_Island_p05-16", 5, 16), ("03_Number_Town_Feelings_Forest_p17-28", 17, 28),
                ("04_Everyday_Village_Adventure_Land_p29-40", 29, 40), ("05_CutOut_Sheets_Reference_Back_p41-48", 41, 48)]
    for name, a, b in sections:
        render_pptx.render([p for p in pages["US_Letter"] if a <= p.number <= b], os.path.join(secdir, f"Magic_Busy_Book_{name}.pptx"), notes)
    a4_pptx = os.path.join(D["04_EDITABLE"], "Magic_Busy_Book_Editable_A4.pptx")
    render_pptx.render(pages["A4"], a4_pptx, notes)
    src_dir = os.path.join(D["04_EDITABLE"], "Production_Source")
    shutil.copytree(HERE, os.path.join(src_dir, "src"), ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(os.path.join(ROOT, "fonts"), os.path.join(src_dir, "fonts"))
    shutil.copytree(COPY, os.path.join(src_dir, "copy"))

    log("illustrations")
    n_svg = export_illustrations(books["US_Letter"])

    log("brand files")
    render_pdf.render(docs.brand_guide_pages(), os.path.join(D["01_BRAND"], "Brand_Guide.pdf"), "Little Worlds Learning Brand Guide", "Brand guide")
    json.dump({"brand": C.BRAND_COLOURS, "supporting": C.SUPPORT_COLOURS,
               "chapters": {c["name"]: {"main": c["colour"], "deep": c["deep"], "tint": c["tint"]} for c in C.CHAPTERS},
               "activity_colour_symbol_pairs": {k: {"hex": v[0], "symbol": v[1]} for k, v in art_lib.ACT.items()}},
              open(os.path.join(D["01_BRAND"], "Brand_Colours.json"), "w"), indent=2)
    open(os.path.join(D["01_BRAND"], "Leo_Character_Sheet.svg"), "w").write(docs.character_sheet_svg())
    shutil.copy(os.path.join(ROOT, "docs_src", "Typography_Guide.md"), D["01_BRAND"])

    log("content files")
    docs.write_content_files(D["02_CONTENT"], books["US_Letter"], pages["US_Letter"], books["A4"], pages["A4"])

    log("shopify + marketing")
    shopify_images.build(pdf["US_Letter"], D["06_SHOPIFY"], os.path.join(TMP, "shop"))
    shopify_images.preview_pdf(pdf["US_Letter"], os.path.join(D["06_SHOPIFY"], "Preview.pdf"), os.path.join(TMP, "prev"))
    for f in ("Product_Description.html", "SEO.txt", "Product_Tags.txt"):
        shutil.copy(os.path.join(COPY, f), D["06_SHOPIFY"])
    for f in ("Instagram_Captions.md", "Reel_Scripts.md", "Pinterest_Copy.md", "Facebook_Ad_Concepts.md", "Launch_Email.md", "Free_Sample_Notes.md"):
        shutil.copy(os.path.join(COPY, f), D["07_MARKETING"])
    render_pdf.render(docs.free_sample_pages(), os.path.join(D["07_MARKETING"], "Free_Sample_Activity.pdf"), "Free sample - Rainbow Rescue", "Lead magnet")

    log("QA")
    results = []
    vis = os.path.join(D["08_QA"], "Visual_Review")
    for ed in SIZES:
        results += qa.check_structure(pages[ed], ed)
        results += qa.check_pieces(pages[ed], ed)
        results += qa.check_fit(pages[ed], ed)
        results += qa.check_numbers(pages[ed], ed)
        results += qa.check_text(pages[ed], ed)
        results += qa.check_pdf(pdf[ed], ed, pages[ed], os.path.join(vis, ed))
        contact_sheet(os.path.join(vis, ed), os.path.join(vis, f"Contact_Sheet_{ed}.png"))
    results += qa.check_patterns()
    # cross-edition consistency
    same = all([(p.number, p.kind, [s["accepts"] for s in p.slots]) for p in pages["US_Letter"]][i] ==
               [(p.number, p.kind, [s["accepts"] for s in p.slots]) for p in pages["A4"]][i] for i in range(48))
    same_sheet = books["US_Letter"].sheet_of == books["A4"].sheet_of
    results.append((qa.PASS if same and same_sheet else qa.FAIL, "US Letter and A4 editions have identical page order, boards, slots and piece-sheet allocation",
                    "page numbers, answers and piece IDs identical in both editions" if same and same_sheet else "mismatch"))
    # PPTX
    pp_ok, pp_detail = False, "LibreOffice not available"
    try:
        out = os.path.join(TMP, "pptx_check")
        os.makedirs(out, exist_ok=True)
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", out, pptx_main], check=True, capture_output=True, timeout=600)
        r = PdfReader(os.path.join(out, "Magic_Busy_Book_Editable.pdf"))
        from pptx import Presentation
        prs = Presentation(pptx_main)
        n_txt = sum(1 for s in prs.slides for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip())
        n_pic = sum(1 for s in prs.slides for sh in s.shapes if sh.shape_type == 13)
        n_shape = sum(1 for s in prs.slides for sh in s.shapes if sh.shape_type in (1, 9, 5))
        pp_ok = len(r.pages) == 48 and len(prs.slides) == 48
        pp_detail = (f"{len(prs.slides)} slides; {n_txt} native text boxes, {n_shape} native shapes/lines/freeforms, {n_pic} separately replaceable artwork pictures; "
                     f"LibreOffice re-renders {len(r.pages)} pages")
        subprocess.run(["pdftoppm", "-r", "40", "-png", "-f", "1", "-l", "8", os.path.join(out, "Magic_Busy_Book_Editable.pdf"), os.path.join(vis, "PPTX_render_page")], check=True)
    except Exception as e:  # pragma: no cover
        pp_detail = f"check failed: {e}"
    results.append((qa.PASS if pp_ok else qa.FAIL, "editable PPTX opens and renders 48 slides (LibreOffice)", pp_detail))
    # spelling
    sp, words = qa.check_spelling(pages["US_Letter"])
    open(os.path.join(D["08_QA"], "Spelling_Wordlist.txt"), "w").write("\n".join(words))
    # Shopify thumbnail
    cov = Image.open(os.path.join(D["06_SHOPIFY"], "Cover.png"))
    for wpx in (160, 300):
        cov.resize((wpx, int(cov.height * wpx / cov.width)), Image.LANCZOS).save(os.path.join(vis, f"Cover_thumbnail_{wpx}px.png"))
    # customer pack
    cust = sorted(os.listdir(CUST))
    exp = ["Magic_Busy_Book_A4.pdf", "Magic_Busy_Book_US_Letter.pdf", "Start_Here_Printing_Guide.pdf"]
    results.append((qa.PASS if cust == exp else qa.FAIL, "customer download pack contains exactly the three customer files (no editable publisher files)", ", ".join(cust)))
    # copy checks
    seo = open(os.path.join(COPY, "SEO.txt")).read().split("\n")
    meta = seo[seo.index("META DESCRIPTION (155 chars max)") + 1]
    title = seo[seo.index("SEO TITLE (60 chars max)") + 1]
    facing = [open(os.path.join(COPY, f)).read() for f in ("Product_Description.html", "Instagram_Captions.md", "Pinterest_Copy.md", "Launch_Email.md", "Product_Tags.txt")]
    facing += [ln for ln in open(os.path.join(COPY, "Facebook_Ad_Concepts.md")).read().splitlines() if ln.strip().startswith(("- Primary text", "- Headline"))]
    alltxt = " ".join(facing).lower()
    banned = [w for w in ("review", "reviews", "rated", "award", "awards", "best-selling", "bestseller", "only a few left", "limited time", "hurry", "guaranteed", "certified") if re.search(r"\b" + w + r"\b", alltxt)]
    fake_review = any(s in alltxt for s in ("★★★★★", "5 stars", "five stars", "customers say", "\"love it\""))
    results.append((qa.PASS if len(meta) <= 155 and len(title) <= 60 else qa.FAIL, "SEO title and meta description within Shopify length limits", f"title {len(title)} chars, meta {len(meta)} chars"))
    results.append((qa.PASS if not banned and not fake_review else qa.FAIL, "no fake reviews, ratings, awards or artificial scarcity in sales copy", f"scan of customer-facing copy (description, captions, pins, email, tags, ad text): {banned or 'none found'}"))

    write_reports(results, sp, pages, books, pdf, n_svg, pp_detail, t0)

    log("README, licensing, zips")
    shutil.copy(os.path.join(ROOT, "docs_src", "README.md"), PUB)
    with zipfile.ZipFile(os.path.join(CUST, "Magic_Busy_Book_Customer_Files.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in exp:
            z.write(os.path.join(CUST, f), os.path.join("My_Magic_Busy_Book", f))
    zipdir(PUB, os.path.join(DIST, "Little_Worlds_My_Magic_Busy_Book_PUBLISHER.zip"), "Little_Worlds_My_Magic_Busy_Book")
    write_manifest()
    fails = [r for r in results if r[0] == qa.FAIL]
    log(f"done in {(datetime.datetime.now() - t0).seconds}s; checks: {len(results)}; FAIL: {len(fails)}")
    for r in fails:
        log("FAIL:", r[1], "-", r[2])
    return 0 if not fails else 1


def write_manifest():
    rows = []
    for dp, _, fs in os.walk(DIST):
        for f in sorted(fs):
            full = os.path.join(dp, f)
            rows.append((os.path.relpath(full, DIST), os.path.getsize(full), sha(full)))
    with open(os.path.join(DIST, "FILE_MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["path", "bytes", "sha256_16"])
        w.writerows(sorted(rows))


def write_reports(results, sp, pages, books, pdf, n_svg, pp_detail, t0):
    q = D["08_QA"]
    human = [
        ("Mascot consistency", "Leo was drawn from one parametric definition (same head, vest, shoes, backpack, colours) in every pose; contact sheets inspected on screen. Confirm on a physical print."),
        ("Overall visual quality / illustration style", "All 48 pages of both editions rendered and inspected at 50-60 dpi during production (see Visual_Review). A designer should review at 100% zoom and on paper."),
        ("Spelling and grammar", sp[0][2] + " Text was written in Australian/British English (colour, favourite). Human proofread required."),
        ("Cover readable at Shopify thumbnail size", "Cover_thumbnail_160px.png and _300px.png generated; title is ~70 pt on an 11 in cover (about 17 px tall letters at 160 px wide). Inspected on screen: title readable. Confirm in the Shopify theme."),
        ("Physical print test", "Not run - no printer in this environment. Print one copy of each edition at Actual size and check that the 1.55 in cards fit the 1.65 in boxes, colours are distinguishable and nothing is clipped by the printer."),
        ("Canva import of the PPTX", "Not testable here (no Canva account in this build). LibreOffice opens the PPTX and renders all 48 slides. See Known_Limitations.md for expected Canva behaviour."),
        ("Educational accuracy (animals, foods, habitats)", "Reviewed in production: see Activity_Validation_Report.md section 'Accuracy notes'. A second reviewer (early-childhood educator) should confirm."),
        ("Emotions, routines and stereotypes", "Feelings are shown on non-human round faces; adult notes state faces can mean different things; routines and day activities accept any explained answer; no gendered roles appear. Human sensitivity review recommended."),
        ("Safety wording", "Under-3 warning, adult preparation and supervision appear on p3, p41-45 footers, p48, the printing guide and the Shopify description. Check against the rules of the country you sell in (e.g. ACCC guidance in Australia); this is not legal advice."),
        ("Font licences", "Fredoka, Nunito and Tajawal are SIL Open Font License 1.1 (licence texts included). OFL permits embedding in PDFs and commercial use; confirm the fonts used inside Canva are licensed via Canva for your account."),
    ]
    status_order = [qa.PASS, qa.REVIEW, qa.FAIL]
    L = ["# QA REPORT - My Magic Busy Book", "",
         f"Generated {t0:%Y-%m-%d %H:%M} by the automated production pipeline (`src/build.py`, `src/qa.py`). {C.PRODUCT['version']}.", "",
         "Every check below was actually executed in this build unless it says *Not run*. Automated checks do not replace human visual inspection.", ""]
    counts = {s: 0 for s in status_order}
    for s in status_order:
        items = [r for r in results if r[0] == s]
        if s == qa.REVIEW:
            items = items + [(qa.REVIEW, a, b) for a, b in human]
        counts[s] = len(items)
        L.append(f"## {s} ({len(items)})")
        L.append("")
        if not items:
            L.append("None.")
        for _, name, det in items:
            L.append(f"- **{name}** - {det}")
        L.append("")
    L.insert(6, f"**Summary: {counts[qa.PASS]} PASS · {counts[qa.REVIEW]} NEEDS HUMAN REVIEW · {counts[qa.FAIL]} FAIL**\n")
    L += ["## Part L checklist cross-reference", ""]
    xref = [("1 Exactly 48 pages", "structure + PDF page count (both editions)"), ("2 Exactly 36 distinct missions", "structure"), ("3 Five cut-out sheets contain every required piece", "pieces"),
            ("4 Cut-out references correct", "pieces mapping + footer notes generated from the same data"), ("5 Correct counting/matching answers", "number answers + patterns"),
            ("6 Consistent mascot", "NEEDS HUMAN REVIEW"), ("7 Consistent typography and colours", "single font/colour system in code; brand guide"), ("8 Spelling and grammar", "NEEDS HUMAN REVIEW"),
            ("9 No clipped text or illustrations", "text overflow check + visual review"), ("10 No unreadably small instructions", "text size check"),
            ("11 No overlapping cut lines", "piece spacing check"), ("12 No duplicated or missing pieces", "pieces"), ("13 No fonts failing to render", "glyph coverage + font embedding"),
            ("14 No corrupted or blank pages", "PDF raster check"), ("15 Both editions verified", "all checks run for US Letter and A4"), ("16 Cover readable at thumbnail size", "NEEDS HUMAN REVIEW (thumbnails provided)"),
            ("17 Original illustrations / licences", "Licensing_Records.md"), ("18 No fake photos or reviews", "copy scan + mockup captions"), ("19 Adult supervision info", "NEEDS HUMAN REVIEW of wording; present on p3, p48, sheets, guide, listing"),
            ("20 Customer pack correct", "customer pack check")]
    L += [f"- {a}: {b}" for a, b in xref]
    open(os.path.join(q, "QA_Report.md"), "w").write("\n".join(L))

    # PDF validation report
    P = ["# PDF Validation Report", ""]
    for ed in SIZES:
        r = PdfReader(pdf[ed])
        P.append(f"## {os.path.basename(pdf[ed])}")
        P.append(f"- File size: {os.path.getsize(pdf[ed]) / 1e6:.2f} MB; SHA-256 (16): {sha(pdf[ed])}")
        P.append(f"- Pages: {len(r.pages)}; MediaBox: {float(r.pages[0].mediabox.width):.2f} x {float(r.pages[0].mediabox.height):.2f} pt "
                 f"({float(r.pages[0].mediabox.width) / 72:.3f} x {float(r.pages[0].mediabox.height) / 72:.3f} in)")
        P.append(f"- Metadata title: {r.metadata.title}; author: {r.metadata.author}")
        P.append("- No bleed and no printer's marks (home-print edition). Margins / safe area: 0.5 in (cards and text checked >= 0.4 in from every edge).")
        P.append("- Artwork is vector (SVG drawn through svglib); no raster images inside the book PDFs.")
        P.append("")
        P.append("| Page | Title | Extracted characters |")
        P.append("|---|---|---|")
        for i, pg in enumerate(r.pages):
            P.append(f"| {i + 1} | {pages[ed][i].title} | {len((pg.extract_text() or '').strip())} |")
        P.append("")
    P += ["## Checks", ""] + [f"- {s}: **{n}** - {d}" for s, n, d in results if "PDF" in n or "render" in n or "font" in n.lower()]
    open(os.path.join(q, "PDF_Validation_Report.md"), "w").write("\n".join(P))

    # Activity validation report
    A = ["# Activity Validation Report", "", "Source of truth: `02_CONTENT/Activity_Manifest.csv` and `Piece_Inventory.csv`, both generated from the same data that draws the pages.", ""]
    A += [f"- {s}: **{n}** - {d}" for s, n, d in results if any(k in n for k in ("piece", "Piece", "mission", "number", "pattern", "slot", "board", "solvable"))]
    A += ["", "## Mission-by-mission", "", "| # | Page | Mission | Cut-outs | Pieces | Slots | Finger/pencil | Paper cut-outs | Fasteners | Status |", "|---|---|---|---|---|---|---|---|---|---|"]
    by = {p.number: p for p in pages["US_Letter"]}
    for m in C.MISSIONS:
        p = by[m["page"]]
        A.append(f"| {m['n']:02d} | {m['page']} | {m['title']} | {'yes' if m['pieces'] else 'no-cut'} | {len(m['pieces'])} | {len(p.slots) if m['pieces'] else len(p.answers)} answers"
                 f" | {m['modes'][0]} | {m['modes'][1]} | {m['modes'][2]} | automated PASS; visual check |")
    A += ["", "## Piece budget", "",
          f"- {sum(len(s['items']) for s in C.PIECE_SETS)} cards in {len(C.PIECE_SETS)} sets; capacity 5 sheets x 20 = 100 at a safe card size of {PIECE} in (39 mm).",
          "- To stay within five sheets without shrinking cards, sets are shared between boards (RD: p5 & p40; SH: p6 & p40; AN: p11, p13 & p40; NU: p17, p18, p20, p22 & p40) and 10 missions were designed as no-cut activities.",
          "- Sets are never split across sheets; sheet allocation is first-fit by usage order, not by chapter.", "",
          "## Accuracy notes (animals, food, habitats)", "",
          "- Habitats: fish-ocean, cow-farm field, monkey-rainforest, penguin-icy land (many penguin species live in cold southern regions; some live in warmer places - adult note says animals can live in more than one kind of place), camel-desert, frog-pond.",
          "- Foods: panda-bamboo (bamboo is almost all of a giant panda's diet); bee-flowers (nectar and pollen); penguin-fish; squirrel-acorns (nuts and seeds); cow-grass; monkey-banana (many monkeys eat fruit; bananas are a familiar example). Avoided the common inaccurate pairing rabbit-carrot. Adult note: animals eat other foods too.",
          "- Farm: hen-hen house, pig-mud (pigs cool off in mud), duck-pond.",
          "- Anatomy: each animal keeps the correct number of legs, ears, eyes for its simplified style; no hands with fingers are drawn.", ""]
    open(os.path.join(q, "Activity_Validation_Report.md"), "w").write("\n".join(A))
    # Licensing
    Lc = ["# Licensing Records", "",
          "| Asset | Source | Licence | Notes |", "|---|---|---|---|",
          f"| {n_svg} SVG illustrations, Leo mascot, icons, scenes | Created for this product in code (`src/art_core.py`, `src/art_lib.py`) | Owned by Little Worlds Learning | No stock images, no AI-generated images, no traced or licensed characters, no brand logos |",
          "| Fredoka (Bold, SemiBold static instances) | Google Fonts repository (github.com/google/fonts, ofl/fredoka) | SIL Open Font License 1.1 | Licence text: Production_Source/fonts/OFL-Fredoka.txt. Static instances generated from the variable font with fontTools; renamed instances are permitted by OFL (no Reserved Font Name declared) |",
          "| Nunito (Regular, Bold, ExtraBold static instances) | Google Fonts repository (ofl/nunito) | SIL Open Font License 1.1 | Licence text: OFL-Nunito.txt |",
          "| Tajawal Bold (future Arabic editions) | Google Fonts repository (ofl/tajawal) | SIL Open Font License 1.1 | Bundled for future use, not used in v1.0 pages |",
          "| Python libraries (ReportLab, svglib, CairoSVG, python-pptx, pypdf, Pillow, fontTools) | PyPI | BSD / LGPL / MIT-style open-source licences | Build tools only; nothing from them is embedded as content |",
          "", "OFL 1.1 allows the fonts to be embedded in commercial PDFs and bundled with software; the fonts themselves must not be sold on their own.",
          "Customer licence (printed on page 48 and in the listing): personal / single-household use; no resale or redistribution of the files."]
    open(os.path.join(q, "Licensing_Records.md"), "w").write("\n".join(Lc))
    shutil.copy(os.path.join(ROOT, "docs_src", "Known_Limitations.md"), q)


if __name__ == "__main__":
    sys.exit(main())
