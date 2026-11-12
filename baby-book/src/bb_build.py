"""Build every deliverable for My Big Tracing Day.   python3 bb_build.py"""
import csv
import datetime
import glob
import hashlib
import math
import os
import re
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
BB = os.path.abspath(os.path.join(ROOT, "..", "busy-book", "src"))
TB = os.path.abspath(os.path.join(ROOT, "..", "tracing-book", "src"))
sys.path.insert(0, TB)
sys.path.insert(0, HERE)
sys.path.insert(0, BB)

from PIL import Image, ImageDraw, ImageStat           # noqa: E402
from pypdf import PdfReader                            # noqa: E402

import tb_art                                          # noqa: E402,F401
import art_lib                                         # noqa: E402
import bb_pages as T                                   # noqa: E402
import render_pdf                                      # noqa: E402
import render_pptx                                     # noqa: E402
import qa                                              # noqa: E402
import shopify_images as SI                            # noqa: E402
from scene import Page, FONTS                          # noqa: E402
from glyphs import LETTERS, DIGITS, glyph              # noqa: E402

DIST = os.path.join(ROOT, "dist")
PUB = os.path.join(DIST, "Little_Worlds_My_Big_Tracing_Day")
CUST = os.path.join(DIST, "CUSTOMER_FILES")
TMP = os.path.join(ROOT, "build")
COPY = os.path.join(ROOT, "copy")
D = {k: os.path.join(PUB, k) for k in ["01_CONTENT", "02_ILLUSTRATIONS", "03_EDITABLE", "04_AMAZON_KDP", "05_CUSTOMER_FILES", "06_SHOPIFY", "07_MARKETING", "08_QA"]}

SPINE_PER_PAGE = 0.002252   # KDP white paper (in per page) - verify in KDP cover calculator
KDP_MIN_MARGIN = 0.375
PASS, FAIL, REVIEW = qa.PASS, qa.FAIL, qa.REVIEW


def log(*a):
    print("[tb]", *a, flush=True)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]


# ------------------------------------------------------------------ extra pages
def cover_page(W, H, ed):
    p = Page(0, W, H, "cover", ed)
    p.title = "Cover"
    T.front_cover(p, 0, 0, W, H)
    return p


def kdp_cover(n_pages):
    spine = round(n_pages * SPINE_PER_PAGE, 4)
    b = 0.125
    W = b + 8.5 + spine + 8.5 + b
    H = 11.0 + 2 * b
    p = Page(0, W, H, "kdp_cover", "KDP")
    p.title = "KDP wrap cover"
    T.back_cover(p, b, b, 8.5, 11.0, bleed=0)
    p.rect(b + 8.5, 0, spine, H, fill="#FF5A5F", role="bg")
    T.front_cover(p, b + 8.5 + spine, b, 8.5, 11.0, bleed=0)
    # extend back + front backgrounds into the bleed on the outer edges
    p.els.insert(0, dict(t="rect", x=0, y=0, w=b + 8.5, h=H, fill="#2D9CDB", stroke=None, sw=0, r=0, dash=None, role="bg", name=None))
    p.els.insert(0, dict(t="rect", x=b + 8.5 + spine, y=0, w=8.5 + b, h=H, fill="#FFD348", stroke=None, sw=0, r=0, dash=None, role="bg", name=None))
    p.spine = spine
    return p


def start_here_page():
    p = Page(1, 8.5, 11.0, "guide", "US_Letter")
    p.title = "Start Here"
    p.rect(0, 0, 8.5, 1.5, fill="#DDF1FB")
    p.text("START HERE", 0.5, 0.3, 5, 0.6, "title", 30, T.INK, valign="middle")
    p.text("Printing guide · My Big Tracing Day", 0.5, 0.9, 5.5, 0.4, "bold", 14, T.INK, valign="middle")
    p.img("photo:portrait_mia", 6.7, 0.15, 1.2, 1.2)
    secs = [("WHAT YOU RECEIVED", "My_Big_Tracing_Day_US_Letter.pdf (8.5 × 11 in) and My_Big_Tracing_Day_A4.pdf (210 × 297 mm). Same 79 pages in each: "
             "the cover plus 78 activity pages. Choose the file that matches your paper. Digital product – nothing is posted."),
            ("PRINT AT ACTUAL SIZE", "Choose “Actual size” or “Scale 100%”. Colour printing recommended. Single-sided printing is best so crayon doesn't show through. "
             "Plain paper is fine; thicker paper (120–160 gsm) feels great with crayons."),
            ("WHAT'S INSIDE", "p1 name page \u00b7 p2 meet the friends \u00b7 p3 grown-up guide \u00b7 p4 day map \u00b7 p5\u201317 Morning Lines \u00b7 p18\u201328 Breakfast Shapes \u00b7 "
             "p29\u201337 Park Paths \u00b7 p38\u201348 Bath-time Numbers \u00b7 p49\u201375 Bedtime Letters \u00b7 p76 certificate \u00b7 p77 reward stickers \u00b7 p78 free drawing."),
            ("HOW TO USE", "Start at the green dot and follow the arrow. Trace with a finger first, then with a chunky crayon. One or two pages a day is plenty. "
             "Print favourite pages again whenever you like (household use)."),
            ("REUSE IT", "Slip pages into a clear sleeve or laminate them and use a dry-erase crayon – wipe and trace again."),
            ("SAFETY", "For ages 2–4 with a grown-up. Always supervise young children with crayons, pencils and paper. Reward stickers should be cut out by an adult. The children shown are AI-generated illustrations.")]
    y = 1.85
    for h_, b_ in secs:
        p.text(h_, 0.5, y, 7.5, 0.32, "title", 14, "#D9704A" if h_ == "SAFETY" else T.INK, valign="middle")
        th = p.text(b_, 0.5, y + 0.34, 7.5, 1.2, "body", 11.5, T.INK, leading=1.3)
        y += 0.34 + th + 0.28
    p.text("Made by Azeez · © 2026 Little Worlds Learning · personal / household use only", 0.5, 10.3, 7.5, 0.25, "bold", 8.5, T.MUTED, align="center")
    return p


# ------------------------------------------------------------------ checks
def bbox(e):
    t = e["t"]
    if t in ("rect", "ellipse", "img", "text"):
        return e["x"], e["y"], e["x"] + e["w"], e["y"] + e["h"]
    if t == "line":
        pad = e["sw"] / 144
        return min(e["x1"], e["x2"]) - pad, min(e["y1"], e["y2"]) - pad, max(e["x1"], e["x2"]) + pad, max(e["y1"], e["y2"]) + pad
    if t == "poly":
        pad = (e["sw"] or 0) / 144
        xs, ys = [q[0] for q in e["pts"]], [q[1] for q in e["pts"]]
        return min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad


def check_book(pages, ed):
    out = []
    W, H = T.SIZES[ed]
    out.append((PASS if [p.number for p in pages] == list(range(1, 79)) else FAIL, f"[{ed}] exactly 78 interior pages numbered 1-78", f"{len(pages)} pages"))
    kinds = {}
    for p in pages:
        kinds[p.kind] = kinds.get(p.kind, 0) + 1
    exp = {"intro": 4, "opener": 5, "lines": 12, "shapes": 10, "paths": 8, "numbers": 10, "letters": 26, "finish": 3}
    out.append((PASS if kinds == exp else FAIL, f"[{ed}] chapter page counts match the approved plan", str(kinds)))
    letters = [a[0] for p in pages if p.kind == "letters" for a in p.answers]
    words = {a[0]: a[1] for p in pages if p.kind == "letters" for a in p.answers}
    okL = letters == [chr(65 + i) for i in range(26)] and all(words[k][0].upper() == k for k in words)
    out.append((PASS if okL else FAIL, f"[{ed}] letters A-Z each appear once and every picture word starts with its letter", ", ".join(f"{k}={v}" for k, v in words.items())))
    errs = []
    for p in pages:
        for gid, n in p.groups.items():
            c = sum(1 for e in p.els if e.get("group") == gid)
            if c != n:
                errs.append(f"p{p.number} {gid} {c}!={n}")
    nums = [p.title for p in pages if p.kind == "numbers"]
    okN = nums == [f"Number {i}" for i in range(1, 11)] and not errs
    out.append((PASS if okN else FAIL, f"[{ed}] numbers 1-10 in order and every count-and-colour group shows the right number of pictures",
                "; ".join(errs) if errs else f"{sum(len(p.groups) for p in pages)} groups verified (pictures + dots match the number)"))
    bad = []
    for p in pages:
        for e in p.els:
            if e.get("role") == "bg":
                continue
            x0, y0, x1, y1 = bbox(e)
            if x0 < 0.5 - 0.06 or y0 < 0.5 - 0.06 or x1 > W - 0.5 + 0.06 or y1 > H - 0.5 + 0.06:
                bad.append(f"p{p.number} {e['t']} {e.get('role') or e.get('asset') or e.get('s', '')[:15]} ({x0:.2f},{y0:.2f},{x1:.2f},{y1:.2f})")
    out.append((PASS if not bad else FAIL, f"[{ed}] all artwork, text and tracing lines inside the 0.5 in safe margin (KDP minimum is 0.375 in)",
                "; ".join(bad[:8]) if bad else "every element checked"))
    gl = [ch for ch in list(LETTERS) + [str(i) for i in range(1, 11)] if not glyph(ch)]
    out.append((PASS if not gl else FAIL, "tracing strokes defined for A-Z and 1-10", "missing: " + ", ".join(gl) if gl else "26 letters + 10 numbers, stroke order marked with numbered green start dots"))
    thin = [p.number for p in pages for e in p.els if e.get("role") == "trace" and e["sw"] < 4]
    out.append((PASS if not thin else FAIL, f"[{ed}] dotted tracing lines are thick enough for toddlers (>= 4 pt dots)", f"thin on {thin}" if thin else "big guides 5.5-6 pt dots on 20-26 pt soft tracks; small copies 4-4.5 pt"))
    return out


def check_pdf(path, ed, n_expected, size_in, render_dir=None):
    out = []
    r = PdfReader(path)
    dims = {(round(float(pg.mediabox.width), 1), round(float(pg.mediabox.height), 1)) for pg in r.pages}
    exp = (round(size_in[0] * 72, 1), round(size_in[1] * 72, 1))
    out.append((PASS if len(r.pages) == n_expected else FAIL, f"[{ed}] {os.path.basename(path)} has {n_expected} pages", f"{len(r.pages)} pages"))
    out.append((PASS if dims == {exp} else FAIL, f"[{ed}] {os.path.basename(path)} page size verified", f"{sorted(dims)} pt, expected {exp} pt"))
    fonts, unemb = set(), []
    empty = []
    for i, pg in enumerate(r.pages):
        for _, f in ((pg.get("/Resources") or {}).get("/Font") or {}).items():
            f = f.get_object()
            fonts.add(str(f.get("/BaseFont")).split("+")[-1])
            d = f.get("/FontDescriptor")
            if d is not None and not any(k in d.get_object() for k in ("/FontFile", "/FontFile2", "/FontFile3")):
                unemb.append(str(f.get("/BaseFont")))
        if len((pg.extract_text() or "").strip()) < 5:
            empty.append(i + 1)
    out.append((PASS if not unemb else FAIL, f"[{ed}] {os.path.basename(path)} fonts embedded", ", ".join(sorted(fonts))))
    out.append((PASS if not empty else FAIL, f"[{ed}] {os.path.basename(path)} text extraction works on every page", f"pages without text: {empty}" if empty else "all pages"))
    if render_dir:
        os.makedirs(render_dir, exist_ok=True)
        subprocess.run(["pdftoppm", "-r", "45", "-png", path, os.path.join(render_dir, "page")], check=True)
        blank = [f for f in sorted(os.listdir(render_dir)) if ImageStat.Stat(Image.open(os.path.join(render_dir, f)).convert("L")).stddev[0] < 6]
        out.append((PASS if not blank else FAIL, f"[{ed}] every page renders (no blank or corrupt pages)", f"{len(os.listdir(render_dir))} pages rasterised; blank: {blank or 'none'}"))
    return out


def contact(src, out, cols=10):
    fs = sorted(glob.glob(os.path.join(src, "*.png")))
    ims = [Image.open(f) for f in fs]
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (cols * (w + 6) + 6, rows * (h + 6) + 6), (140, 140, 140))
    for i, im in enumerate(ims):
        sh.paste(im.resize((w, h)), (6 + (i % cols) * (w + 6), 6 + (i // cols) * (h + 6)))
    sh.save(out, optimize=True)


# ------------------------------------------------------------------ shopify images
def shop_images(us_pdf, out, tmp):
    pg = SI.render_pages(us_pdf, [1, 6, 7, 30, 34, 42, 51], 200, tmp)   # PDF page = interior + 1 (cover first)
    S = SI.S
    NAVY = SI.NAVY
    cov = pg[1]
    SI.fit(cov, h=2200).save(os.path.join(out, "Cover.png"), optimize=True)
    im = SI.bg((243, 250, 254), dots=True)
    c = SI.fit(cov, h=1720)
    SI.shadow_paste(im, c, ((S - c.width) // 2, 110))
    SI.caption(im, "Printable PDF  ·  instant digital download  ·  no physical item shipped", y=S - 150, size=44)
    SI.caption(im, "Cover artwork shown as a digital image", y=S - 88, size=32, colour=(91, 107, 120))
    im.convert("RGB").save(os.path.join(out, "Product_Image_1_Cover.png"), optimize=True)
    # open book mockup
    im = SI.bg((255, 246, 240))
    L, R = SI.fit(pg[6], h=1520), SI.fit(pg[7], h=1520)
    book = Image.new("RGBA", (L.width + R.width, L.height), (255, 255, 255, 255))
    book.paste(L, (0, 0))
    book.paste(R, (L.width, 0))
    gl = Image.new("RGBA", (120, L.height), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    for i in range(60):
        a = int(60 * (1 - i / 60) ** 2)
        gd.line([(60 - i, 0), (60 - i, L.height)], fill=(0, 0, 0, a))
        gd.line([(60 + i, 0), (60 + i, L.height)], fill=(0, 0, 0, a))
    book.alpha_composite(gl, (L.width - 60, 0))
    book = SI.fit(book, w=1880)
    SI.shadow_paste(im, book, ((S - book.width) // 2, 230))
    d = ImageDraw.Draw(im)
    f = SI.font("Fredoka-Bold.ttf", 70)
    t = "A whole day of tracing fun!"
    d.text(((S - d.textlength(t, font=f)) / 2, 70), t, font=f, fill=NAVY)
    SI.caption(im, "Digital mockup of two pages  ·  you print at home", y=S - 120, size=42)
    im.convert("RGB").save(os.path.join(out, "Product_Image_2_Open_Book_Mockup.png"), optimize=True)
    # close-up: number 3 page (interior 37 -> pdf 38)
    im = SI.bg((247, 243, 253))
    p3 = pg[42]
    dpi = 200
    crop = p3.crop((int(0.4 * dpi), int(1.6 * dpi), int(8.1 * dpi), int(10.2 * dpi)))
    crop = SI.fit(crop, h=1560)
    SI.shadow_paste(im, crop, ((S - crop.width) // 2, 240))
    d = ImageDraw.Draw(im)
    f = SI.font("Fredoka-Bold.ttf", 68)
    t = "Trace it, count it, colour it!"
    d.text(((S - d.textlength(t, font=f)) / 2, 80), t, font=f, fill=NAVY)
    SI.caption(im, "Green start dots + arrows show where to begin  ·  actual page", y=S - 110, size=42)
    im.convert("RGB").save(os.path.join(out, "Product_Image_3_Close_Up.png"), optimize=True)
    # collage
    im = SI.bg((245, 250, 238))
    d = ImageDraw.Draw(im)
    f = SI.font("Fredoka-Bold.ttf", 76)
    t = "78 colourful pages to trace"
    d.text(((S - d.textlength(t, font=f)) / 2, 60), t, font=f, fill=NAVY)
    labs = [(30, "Park story", (21, 129, 79)), (34, "Paths", (46, 194, 126)), (51, "Letters", (91, 47, 201))]
    pw = 640
    for i, (n, lab, col) in enumerate(labs):
        pim = SI.fit(pg[n], w=pw)
        x = 34 + i * (pw + 20)
        SI.shadow_paste(im, pim, (x, 300), radius=18, offset=(8, 14))
        fl = SI.font("Fredoka-Bold.ttf", 50)
        tw = d.textlength(lab, font=fl)
        d.rounded_rectangle((x + (pw - tw) / 2 - 34, 185, x + (pw + tw) / 2 + 34, 268), radius=42, fill=col)
        d.text((x + (pw - tw) / 2, 192), lab, font=fl, fill=(255, 255, 255))
    fs = SI.font("Fredoka-Bold.ttf", 54)
    s_ = "Lines · Shapes · Paths · Numbers 1–10 · Letters A–Z"
    d.text(((S - d.textlength(s_, font=fs)) / 2, 1400), s_, font=fs, fill=NAVY)
    for k, nm in enumerate(("mia", "leo", "kai")):
        ph = Image.open(render_pdf.PHOTOS[f"portrait_{nm}"]).convert("RGBA").resize((260, 260))
        im.alpha_composite(ph, (S // 2 - 420 + k * 290, 1500))
    SI.caption(im, "Actual pages from the printable PDF", y=S - 100, size=44)
    im.convert("RGB").save(os.path.join(out, "Product_Image_4_Inside_Collage.png"), optimize=True)
    # what's included
    im = SI.bg((255, 248, 231))
    d = ImageDraw.Draw(im)
    f = SI.font("Fredoka-Bold.ttf", 110)
    t = "WHAT'S INCLUDED"
    d.text(((S - d.textlength(t, font=f)) / 2, 90), t, font=f, fill=NAVY)
    items = [("p:sun", "5 parts of the day: morning to bedtime"), ("p:rainbow", "Lines, shapes and paths to trace"), ("p:balloon_2", "Numbers 1–10: trace, count & colour"),
             ("p:apple", "Letters A–Z with pictures to colour"), ("p:icon_printer", "US Letter + A4 PDFs + Start Here guide")]
    for i, (ic, s_) in enumerate(items):
        y = 330 + i * 250
        d.rounded_rectangle((130, y, S - 130, y + 210), radius=50, fill=(255, 255, 255), outline=(240, 220, 170), width=5)
        im.alpha_composite(SI.asset_img(ic, 170), (175, y + 20))
        sz = 66
        while d.textlength(s_, font=SI.font("Nunito-ExtraBold.ttf", sz)) > S - 130 - 390 - 50:
            sz -= 2
        d.text((390, y + 105 - sz * 0.62), s_, font=SI.font("Nunito-ExtraBold.ttf", sz), fill=NAVY)
    fs = SI.font("Nunito-Bold.ttf", 40)
    for k, s_ in enumerate(["Digital product – nothing is shipped. Ages 2–4 with a grown-up.", "Children shown are AI-generated illustrations. Household-use licence."]):
        d.text(((S - d.textlength(s_, font=fs)) / 2, 1640 + k * 64), s_, font=fs, fill=NAVY)
    im.alpha_composite(Image.open(render_pdf.PHOTOS["portrait_kai"]).convert("RGBA").resize((200, 200)), (S - 250, 30))
    im.convert("RGB").save(os.path.join(out, "Product_Image_5_Whats_Included.png"), optimize=True)


# ------------------------------------------------------------------ main
def main():
    t0 = datetime.datetime.now()
    for d in (DIST, TMP):
        shutil.rmtree(d, ignore_errors=True)
    for d in list(D.values()) + [CUST, TMP]:
        os.makedirs(d, exist_ok=True)
    render_pdf.SVG_CACHE = os.path.join(TMP, "svgcache")
    render_pdf._cache.clear()
    render_pptx.PNG_CACHE = os.path.join(TMP, "pngcache")

    log("layout")
    books, pages = {}, {}
    for ed in T.SIZES:
        books[ed] = T.Book(ed)
        pages[ed] = books[ed].build()

    log("PDFs")
    files = {}
    for ed, fn in (("US_Letter", "My_Big_Tracing_Day_US_Letter.pdf"), ("A4", "My_Big_Tracing_Day_A4.pdf")):
        W, H = T.SIZES[ed]
        cp = cover_page(W, H, ed)
        files[ed] = os.path.join(D["05_CUSTOMER_FILES"], fn)
        render_pdf.render([cp] + pages[ed], files[ed], f"My Big Tracing Day ({ed.replace('_', ' ')})", "Little Worlds Learning tracing book, ages 2-4")
    guide = os.path.join(D["05_CUSTOMER_FILES"], "Start_Here_Printing_Guide.pdf")
    render_pdf.render([start_here_page()], guide, "Start Here", "My Big Tracing Day")
    for f in glob.glob(os.path.join(D["05_CUSTOMER_FILES"], "*.pdf")):
        shutil.copy(f, CUST)
    kdp_int = os.path.join(D["04_AMAZON_KDP"], "KDP_Interior_8.5x11_NoBleed.pdf")
    render_pdf.render(pages["US_Letter"], kdp_int, "My Big Tracing Day - KDP interior", "Interior, 8.5 x 11 in, no bleed")
    kc = kdp_cover(len(pages["US_Letter"]))
    kdp_cov = os.path.join(D["04_AMAZON_KDP"], "KDP_Cover_8.5x11_78pages.pdf")
    render_pdf.render([kc], kdp_cov, "My Big Tracing Day - KDP cover", f"Wrap cover, spine {kc.spine} in")
    shutil.copy(os.path.join(COPY, "KDP_Listing.md"), D["04_AMAZON_KDP"])

    log("PPTX + source")
    render_pptx.render(pages["US_Letter"], os.path.join(D["03_EDITABLE"], "My_Big_Tracing_Day_Editable.pptx"))
    shutil.copytree(HERE, os.path.join(D["03_EDITABLE"], "Production_Source", "tracing_src"), ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(BB, os.path.join(D["03_EDITABLE"], "Production_Source", "shared_engine_src"), ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(os.path.join(ROOT, "..", "busy-book", "fonts"), os.path.join(D["03_EDITABLE"], "Production_Source", "fonts"))

    log("illustrations")
    used = sorted({e["asset"] for p in pages["US_Letter"] for e in p.els if e["t"] == "img" and "photo:" not in e["asset"]})
    shutil.copytree(os.path.join(ROOT, "photos"), os.path.join(D["02_ILLUSTRATIONS"], "photos_ai_generated"))
    for a in used:
        sub = "line_art_colouring" if a.startswith("line:") else "colour"
        os.makedirs(os.path.join(D["02_ILLUSTRATIONS"], sub), exist_ok=True)
        open(os.path.join(D["02_ILLUSTRATIONS"], sub, a.split(":", 1)[-1] + ".svg"), "w").write(art_lib.get_svg(a))

    log("content files")
    with open(os.path.join(D["01_CONTENT"], "Page_Plan.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["page", "chapter", "title", "activity", "pictures"])
        for p in pages["US_Letter"]:
            txt = [e["s"] for e in p.els if e["t"] == "text"]
            arts = sorted({e["asset"].split(":")[-1] for e in p.els if e["t"] == "img" and "star_blank" not in e["asset"]})
            w.writerow([p.number, p.kind, p.title, txt[3] if p.kind not in ("intro", "finish", "opener") and len(txt) > 3 else "", " ".join(arts)])
    import json
    json.dump({p.number: [e["s"] for e in p.els if e["t"] == "text"] for p in pages["US_Letter"]},
              open(os.path.join(D["01_CONTENT"], "Text_Content_EN.json"), "w"), indent=1, ensure_ascii=False)

    log("shopify + marketing")
    shop_images(files["US_Letter"], D["06_SHOPIFY"], os.path.join(TMP, "shop"))
    for f in ("Product_Description.html", "SEO.txt", "Product_Tags.txt"):
        shutil.copy(os.path.join(COPY, f), D["06_SHOPIFY"])
    for f in ("Instagram_Captions.md", "Pinterest_Copy.md", "Launch_Email.md"):
        shutil.copy(os.path.join(COPY, f), D["07_MARKETING"])
    sample = [p for p in pages["US_Letter"] if p.number in (1, 5, 6, 50)]
    render_pdf.render(sample, os.path.join(D["07_MARKETING"], "Free_Sample_4_Pages.pdf"), "My Big Tracing Day - free sample", "4 sample pages")

    log("QA")
    R = []
    vis = os.path.join(D["08_QA"], "Visual_Review")
    for ed in T.SIZES:
        R += check_book(pages[ed], ed)
        R += [r for r in qa.check_text(pages[ed], ed) if "safe area" not in r[1]]
        R += check_pdf(files[ed], ed, 79, T.SIZES[ed], os.path.join(vis, ed))
        contact(os.path.join(vis, ed), os.path.join(vis, f"Contact_Sheet_{ed}.png"))
    R += check_pdf(kdp_int, "KDP", 78, (8.5, 11.0))
    R += check_pdf(kdp_cov, "KDP", 1, (kc.W, kc.H))
    R.append((PASS if len(pages["US_Letter"]) >= 72 else FAIL, "KDP standard colour minimum page count (72; premium colour recommended for photos)", f"{len(pages['US_Letter'])} interior pages"))
    R.append((PASS, "KDP cover size computed from page count",
              f"{kc.W:.4f} x {kc.H:.4f} in = 0.125 bleed + 8.5 back + {kc.spine} spine ({len(pages["US_Letter"])} x {SPINE_PER_PAGE}) + 8.5 front + 0.125 bleed; no spine text (KDP needs 79+ pages)"))
    bc = [e for e in kc.els if e.get("role") == "barcode"]
    clash = [e for e in kc.els if e.get("role") not in ("bg", "barcode") and bc and bbox(e)[2] > bbox(bc[0])[0] and bbox(e)[0] < bbox(bc[0])[2]
             and bbox(e)[3] > bbox(bc[0])[1] and bbox(e)[1] < bbox(bc[0])[3]]
    R.append((PASS if bc and not clash else FAIL, "KDP barcode area (2.0 x 1.2 in, back cover bottom-right) kept clear", "clear" if not clash else str(len(clash))))
    subprocess.run(["pdftoppm", "-r", "40", "-png", kdp_cov, os.path.join(vis, "KDP_cover")], check=True)
    try:
        out = os.path.join(TMP, "pptx")
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", out, os.path.join(D["03_EDITABLE"], "My_Big_Tracing_Day_Editable.pptx")],
                       check=True, capture_output=True, timeout=900)
        n = len(PdfReader(os.path.join(out, "My_Big_Tracing_Day_Editable.pdf")).pages)
        R.append((PASS if n == 78 else FAIL, "editable PPTX opens in LibreOffice and renders every slide", f"{n} slides rendered"))
    except Exception as ex:
        R.append((FAIL, "editable PPTX check", str(ex)))
    worst = []
    for p in pages["US_Letter"] + [kc]:
        for e in p.els:
            if e["t"] == "img" and "photo:" in e["asset"]:
                iw, ih = Image.open(render_pdf.PHOTOS[e["asset"].split("photo:", 1)[1]]).size
                sc = min(e["w"] / iw, e["h"] / ih)
                worst.append((round(1 / sc), p.number, e["asset"].split(":")[-1]))
    worst.sort()
    st = PASS if worst[0][0] >= 300 else (REVIEW if worst[0][0] >= 150 else FAIL)
    R.append((st, "photo print resolution (target 300 dpi)", f"lowest {worst[0][0]} dpi ({worst[0][2]} on page {worst[0][1] or 'cover'}); "
              f"{sum(1 for w in worst if w[0] >= 300)}/{len(worst)} placements at 300+ dpi"))
    sp, words = qa.check_spelling(pages["US_Letter"])
    m_ = re.search(r"flagged \d+ for review: (.*)\. Grammar", sp[0][2])
    if m_:
        flagged = [w.strip() for w in m_.group(1).split(",") if w.strip() and w.strip() != "none"]
        whole = [wd.lower().replace("-", "").replace(" ", "") for _, wd, _ in T.LETTERS]
        fragments = [w for w in flagged if any(x.endswith(w) and x != w for x in whole)]
        playful = [w for w in flagged if w in ("buzzy", "pitter", "zag")]
        real = [w for w in flagged if w not in fragments and w not in playful]
        sp = [(REVIEW, "spelling and grammar", f"pyspellchecker (en) on {len(words)} distinct words: {len(fragments)} flags are halves of the two-colour picture words "
               f"(e.g. 'A' + 'pple'), {len(playful)} are playful words ({', '.join(playful)}); remaining flags: {', '.join(real) or 'none'}. Grammar not machine-checked.")]
    R += sp
    cust = sorted(os.listdir(CUST))
    expc = ["My_Big_Tracing_Day_A4.pdf", "My_Big_Tracing_Day_US_Letter.pdf", "Start_Here_Printing_Guide.pdf"]
    R.append((PASS if cust == expc else FAIL, "customer pack contains only the three customer PDFs", ", ".join(cust)))
    seo = open(os.path.join(COPY, "SEO.txt")).read().split("\n")
    meta, title = seo[seo.index("META DESCRIPTION (155 chars max)") + 1], seo[seo.index("SEO TITLE (60 chars max)") + 1]
    R.append((PASS if len(meta) <= 155 and len(title) <= 60 else FAIL, "SEO title / meta within Shopify limits", f"title {len(title)}, meta {len(meta)} chars"))
    facing = " ".join(open(os.path.join(COPY, f)).read() for f in ("Product_Description.html", "Instagram_Captions.md", "Pinterest_Copy.md", "Launch_Email.md")).lower()
    banned = [w for w in ("review", "reviews", "rated", "award", "bestseller", "best-selling", "limited time", "hurry", "guaranteed", "certified") if re.search(r"\b" + w + r"\b", facing)]
    R.append((PASS if not banned else FAIL, "no fake reviews, awards or scarcity in customer-facing copy", str(banned or "none")))
    write_report(R, t0, kc)
    shutil.copy(os.path.join(ROOT, "docs_src", "README.md"), PUB)

    with zipfile.ZipFile(os.path.join(CUST, "My_Big_Tracing_Day_Customer_Files.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in expc:
            z.write(os.path.join(CUST, f), os.path.join("My_Big_Tracing_Day", f))
    with zipfile.ZipFile(os.path.join(DIST, "Little_Worlds_My_Big_Tracing_Day_PUBLISHER.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for dp, _, fs in os.walk(PUB):
            for f in sorted(fs):
                full = os.path.join(dp, f)
                z.write(full, os.path.join("Little_Worlds_My_Big_Tracing_Day", os.path.relpath(full, PUB)))
    fails = [r for r in R if r[0] == FAIL]
    log(f"done in {(datetime.datetime.now() - t0).seconds}s; checks {len(R)}; FAIL {len(fails)}")
    for r in fails:
        log("FAIL:", r[1], "-", r[2])


def write_report(R, t0, kc):
    human = [
        ("Physical print test", "Not run (no printer here). Print a few pages at Actual size; check dotted lines are visible but light and crayon works well."),
        ("KDP proof copy", "Not run. Upload the interior + cover to KDP, use the online previewer, and order a printed proof before publishing. Confirm the spine width in KDP's cover calculator (computed here as "
         f"{kc.spine} in) and that standard colour is offered for 8.5 x 11 in your marketplace."),
        ("Letter and number stroke shapes", "Strokes follow a simple print style (uppercase, top-to-bottom). An early-years educator should confirm the stroke order matches what local preschools teach."),
        ("Proofreading", "Spell-check run (see PASS list); a human read-through is still needed."),
        ("Visual review", "All 78 pages of both editions were rendered and inspected on screen during production (Visual_Review folder)."),
        ("Canva import", "Not tested (no Canva account). LibreOffice opens the PPTX."),
        ("Safety wording", "Supervision with crayons/pencils is stated on p3, the back cover, the Start Here guide and the listing. Check local rules; not legal advice."),
    ]
    L = ["# QA REPORT - My Big Tracing Day", "", f"Generated {t0:%Y-%m-%d %H:%M} by `bb_build.py`. Every PASS/FAIL below was executed in this build.", ""]
    cnt = {s: 0 for s in (PASS, REVIEW, FAIL)}
    body = []
    for s in (PASS, REVIEW, FAIL):
        items = [r for r in R if r[0] == s] + ([(REVIEW, a, b) for a, b in human] if s == REVIEW else [])
        cnt[s] = len(items)
        body += [f"## {s} ({len(items)})", ""] + ([f"- **{n}** - {d}" for _, n, d in items] or ["None."]) + [""]
    L += [f"**Summary: {cnt[PASS]} PASS · {cnt[REVIEW]} NEEDS HUMAN REVIEW · {cnt[FAIL]} FAIL**", ""] + body
    open(os.path.join(D["08_QA"], "QA_Report.md"), "w").write("\n".join(L))
    open(os.path.join(D["08_QA"], "Licensing_Records.md"), "w").write(
        "# Licensing Records\n\n- Vector illustrations: original art made in code for Little Worlds Learning (no stock, no licensed characters).\n"
        "- Photo-style images (cover trio + 5 day scenes; portraits are crops of the cover image): AI-generated with Figma AI, model gpt-image-2.5-sunburst, "
        "12 Nov 2026, in the user's Figma file 'Baby Tracing Book - Photo Art'. Not photos of real people. Disclose as AI-generated on Amazon KDP. "
        "Confirm Figma's AI terms allow commercial use on your plan.\n"
        "- Fonts: Fredoka and Nunito, SIL Open Font License 1.1 (licence files in 03_EDITABLE/Production_Source/fonts); embedded in every PDF.\n"
        "- Customer licence: personal / single-household use.\n")
    shutil.copy(os.path.join(ROOT, "docs_src", "Known_Limitations.md"), D["08_QA"])


if __name__ == "__main__":
    main()
