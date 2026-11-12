"""Shopify product visuals built from the ACTUAL rendered book pages.

Every image that shows pages in a book-like arrangement is captioned as a
digital mockup so it cannot be mistaken for a photo of a manufactured product.
"""
import io
import os
import subprocess
import cairosvg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import art_lib
from scene import FONT_DIR

NAVY = (24, 53, 75)
CREAM = (255, 249, 234)
SKY = (100, 200, 237)
CORAL = (242, 104, 85)
YELLOW = (255, 211, 72)
LIME = (168, 216, 73)
PINK = (247, 182, 210)
S = 2048


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def render_pages(pdf, nums, dpi, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    res = {}
    for n in nums:
        base = os.path.join(out_dir, f"pg{n}_{dpi}")
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", "-f", str(n), "-l", str(n), pdf, base], check=True)
        res[n] = Image.open(base + ".png").convert("RGB")
    return res


def asset_img(name, px):
    png = cairosvg.svg2png(bytestring=art_lib.get_svg(name).encode(), output_width=px)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def shadow_paste(canvas, im, xy, radius=28, offset=(14, 22), alpha=110, rot=0):
    if rot:
        im = im.convert("RGBA").rotate(rot, expand=True, resample=Image.BICUBIC)
    im = im.convert("RGBA")
    sh = Image.new("RGBA", (im.width + radius * 4, im.height + radius * 4), (0, 0, 0, 0))
    mask = im.split()[3].point(lambda a: alpha if a > 0 else 0)
    sh.paste((20, 30, 40, 255), (radius * 2, radius * 2), mask)
    sh = sh.filter(ImageFilter.GaussianBlur(radius))
    canvas.alpha_composite(sh, (xy[0] - radius * 2 + offset[0], xy[1] - radius * 2 + offset[1]))
    canvas.alpha_composite(im, xy)


def bg(colour=CREAM, dots=False):
    im = Image.new("RGBA", (S, S), colour + (255,))
    if dots:
        d = ImageDraw.Draw(im)
        for x, y, r, c in ((120, 140, 70, PINK), (1930, 160, 60, SKY), (110, 1700, 60, LIME), (1940, 1680, 80, YELLOW)):
            d.ellipse((x - r, y - r, x + r, y + r), fill=c + (110,))
    return im


def caption(im, text, y=S - 92, size=40, colour=NAVY):
    d = ImageDraw.Draw(im)
    f = font("Nunito-Bold.ttf", size)
    w = d.textlength(text, font=f)
    d.text(((S - w) / 2, y), text, font=f, fill=colour)


def fit(im, h=None, w=None):
    if h:
        return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)


def build(pdf_us, out_dir, tmp):
    os.makedirs(out_dir, exist_ok=True)
    pg = render_pages(pdf_us, [1, 5, 11, 17, 23, 41], 220, tmp)
    files = {}
    # ---- Cover.png (plain cover render)
    cov = pg[1]
    cover_png = fit(cov, h=2200)
    cover_png.save(os.path.join(out_dir, "Cover.png"), optimize=True)
    files["Cover.png"] = "Front cover rendered directly from the US Letter PDF (1700 x 2200 px)."
    # ---- Image 1: premium cover
    im = bg(dots=True)
    c = fit(cov, h=1720)
    shadow_paste(im, c, ((S - c.width) // 2, 110))
    caption(im, "Printable PDF  ·  instant digital download  ·  no physical item shipped", y=S - 150, size=44)
    caption(im, "Cover artwork shown as a digital image", y=S - 88, size=32, colour=(91, 107, 120))
    im.convert("RGB").save(os.path.join(out_dir, "Product_Image_1_Cover.png"), optimize=True)
    # ---- Image 2: open-book mockup (Rainbow Rescue)
    im = bg((236, 246, 251))
    L, R = fit(pg[5], h=1520), fit(pg[41], h=1520)
    book = Image.new("RGBA", (L.width + R.width, L.height), (255, 255, 255, 255))
    book.paste(L, (0, 0))
    book.paste(R, (L.width, 0))
    g = Image.new("RGBA", (120, L.height), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for i in range(60):
        a = int(70 * (1 - i / 60) ** 2)
        gd.line([(60 - i, 0), (60 - i, L.height)], fill=(0, 0, 0, a))
        gd.line([(60 + i, 0), (60 + i, L.height)], fill=(0, 0, 0, a))
    book.alpha_composite(g, (L.width - 60, 0))
    book = fit(book, w=1880)
    shadow_paste(im, book, ((S - book.width) // 2, 230))
    d = ImageDraw.Draw(im)
    f = font("Fredoka-Bold.ttf", 70)
    t = "Mission 01: Rainbow Rescue"
    d.text(((S - d.textlength(t, font=f)) / 2, 70), t, font=f, fill=NAVY)
    caption(im, "Digital mockup of printed pages (board + cut-out sheet)  ·  you print at home", y=S - 120, size=42)
    im.convert("RGB").save(os.path.join(out_dir, "Product_Image_2_Open_Book_Mockup.png"), optimize=True)
    # ---- Image 3: close-up board + matching pieces
    im = bg((255, 246, 250))
    p5 = pg[5]
    W5, H5 = p5.size
    dpi = 220
    crop = p5.crop((int(0.45 * dpi), int(1.8 * dpi), int(8.05 * dpi), int(5.35 * dpi)))
    crop = fit(crop, w=1280)
    shadow_paste(im, crop, (70, 300))
    p41 = pg[41]
    gx = (8.5 - (4 * 1.55 + 3 * 0.28)) / 2
    gy = 0.5 + 0.88
    order = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1)]
    spots = [(1390, 250, -8), (1650, 430, 6), (1385, 650, 5), (1645, 870, -6), (1395, 1090, -4), (1650, 1300, 8)]
    for (r, cidx), (x, y, rot) in zip(order, spots):
        x0 = gx + cidx * (1.55 + 0.28)
        y0 = gy + r * (1.55 + 0.28)
        card = p41.crop((int(x0 * dpi) - 4, int(y0 * dpi) - 4, int((x0 + 1.55) * dpi) + 4, int((y0 + 1.55) * dpi) + 4))
        card = fit(card, w=300)
        mask = Image.new("L", card.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((3, 3, card.width - 3, card.height - 3), radius=26, fill=255)
        card = card.convert("RGBA")
        card.putalpha(mask)
        shadow_paste(im, card, (x, y), radius=14, offset=(8, 12), alpha=120, rot=rot)
    d = ImageDraw.Draw(im)
    f = font("Fredoka-Bold.ttf", 66)
    t = "Every board has matching cards"
    d.text(((S - d.textlength(t, font=f)) / 2, 80), t, font=f, fill=NAVY)
    f2 = font("Nunito-ExtraBold.ttf", 56)
    lines = ["Colour + symbol on every card", "Large 1.55 in (39 mm) pieces", "Card ID + page number on each piece", "Optional: laminate & add reusable dots"]
    for i, s in enumerate(lines):
        d.ellipse((110, 1060 + i * 110, 150, 1100 + i * 110), fill=CORAL)
        d.text((180, 1044 + i * 110), s, font=f2, fill=NAVY)
    caption(im, "Digital illustration of the printable board and cut-out cards  ·  not a photograph", y=S - 100, size=38)
    im.convert("RGB").save(os.path.join(out_dir, "Product_Image_3_Board_And_Pieces.png"), optimize=True)
    # ---- Image 4: three-panel collage
    im = bg((245, 250, 238))
    d = ImageDraw.Draw(im)
    f = font("Fredoka-Bold.ttf", 76)
    t = "36 missions in 6 little worlds"
    d.text(((S - d.textlength(t, font=f)) / 2, 60), t, font=f, fill=NAVY)
    labels = [(11, "Animal Island", (94, 154, 30)), (17, "Number Town", (31, 134, 179)), (23, "Feelings Forest", (185, 135, 0))]
    pw = 640
    for i, (n, lab, col) in enumerate(labels):
        pim = fit(pg[n], w=pw)
        x = 34 + i * (pw + 20)
        shadow_paste(im, pim, (x, 300), radius=18, offset=(8, 14))
        fl = font("Fredoka-Bold.ttf", 48)
        tw = d.textlength(lab, font=fl)
        d.rounded_rectangle((x + (pw - tw) / 2 - 30, 185, x + (pw + tw) / 2 + 30, 265), radius=40, fill=col)
        d.text((x + (pw - tw) / 2, 193), lab, font=fl, fill=(255, 255, 255))
    skills = [("icon_match", "Match"), ("icon_sort", "Sort"), ("icon_count", "Count"), ("icon_build", "Build"), ("icon_imagine", "Imagine"), ("icon_explore", "Explore")]
    fs_ = font("Fredoka-Bold.ttf", 46)
    for i, (ic, lab) in enumerate(skills):
        cx = int(S * (i + 0.5) / 6)
        d.ellipse((cx - 120, 1290, cx + 120, 1530), fill=(255, 255, 255), outline=(201, 211, 219), width=4)
        im.alpha_composite(asset_img(ic, 170), (cx - 85, 1325))
        d.text((cx - d.textlength(lab, font=fs_) / 2, 1560), lab, font=fs_, fill=NAVY)
    fsub = font("Nunito-Bold.ttf", 46)
    sub = "Colour Kingdom · Animal Island · Number Town · Feelings Forest · Everyday Village · Adventure Land"
    fsub2 = font("Nunito-Bold.ttf", 40)
    d.text(((S - d.textlength(sub, font=fsub2)) / 2, 1720), sub, font=fsub2, fill=NAVY)
    caption(im, "Actual pages from the printable PDF", y=S - 110, size=44)
    im.convert("RGB").save(os.path.join(out_dir, "Product_Image_4_Worlds_Collage.png"), optimize=True)
    # ---- Image 5: what's included
    im = bg(dots=False)
    d = ImageDraw.Draw(im)
    f = font("Fredoka-Bold.ttf", 110)
    t = "WHAT'S INCLUDED"
    d.text(((S - d.textlength(t, font=f)) / 2, 90), t, font=f, fill=NAVY)
    items = [("icon_printer", "48 printable pages"), ("icon_explore", "36 missions in 6 little worlds"), ("icon_scissors", "5 cut-out sheets (97 cards)"),
             ("icon_storage", "US Letter + A4 PDFs, plus a Start Here guide"), ("icon_laminate", "Editable source retained by publisher (not included)")]
    for i, (ic, s) in enumerate(items):
        y = 330 + i * 250
        d.rounded_rectangle((130, y, S - 130, y + 210), radius=50, fill=(255, 255, 255), outline=(233, 221, 182), width=5)
        icon = asset_img(ic, 170)
        im.alpha_composite(icon, (175, y + 20))
        sz = 66
        while d.textlength(s, font=font("Nunito-ExtraBold.ttf", sz)) > S - 130 - 390 - 50:
            sz -= 2
        fi = font("Nunito-ExtraBold.ttf", sz)
        d.text((390, y + 105 - sz * 0.62), s, font=fi, fill=NAVY)
    fs = font("Nunito-Bold.ttf", 40)
    for k, s in enumerate(["Digital product – nothing is shipped. Ages 3–5 with adult supervision.",
                           "Adult cutting required. Scissors, card stock and laminating supplies not included."]):
        d.text(((S - d.textlength(s, font=fs)) / 2, 1640 + k * 64), s, font=fs, fill=NAVY)
    leo = asset_img("leo_cheer", 230)
    im.alpha_composite(leo, (S - 300, 20))
    im.convert("RGB").save(os.path.join(out_dir, "Product_Image_5_Whats_Included.png"), optimize=True)
    return files


def preview_pdf(pdf_us, out_path, tmp):
    nums = [1, 4, 5, 11, 17, 23, 29, 35, 41, 47]
    pg = render_pages(pdf_us, nums, 60, tmp)
    out = []
    for n in nums:
        im = pg[n].convert("RGBA")
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        f = font("Fredoka-Bold.ttf", 46)
        txt = "SAMPLE PREVIEW"
        tw = d.textlength(txt, font=f)
        layer = Image.new("RGBA", (int(tw) + 40, 80), (0, 0, 0, 0))
        ImageDraw.Draw(layer).text((20, 10), txt, font=f, fill=(24, 53, 75, 70))
        layer = layer.rotate(35, expand=True)
        ov.alpha_composite(layer, ((im.width - layer.width) // 2, (im.height - layer.height) // 2))
        out.append(Image.alpha_composite(im, ov).convert("RGB"))
    out[0].save(out_path, save_all=True, append_images=out[1:], resolution=60)
