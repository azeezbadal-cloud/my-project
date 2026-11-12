"""Renderer-neutral page model.

Units: inches, origin top-left.  A Page holds drawing elements (rendered to PDF
and PPTX) plus machine-checkable metadata: activity slots, count groups and
answer records used by the validators.
"""
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "..", "fonts")

# key -> (reportlab name, file, pptx family, pptx bold)
FONTS = {
    "title": ("Fredoka-Bold", "Fredoka-Bold.ttf", "Fredoka", True),
    "semi": ("Fredoka-SemiBold", "Fredoka-SemiBold.ttf", "Fredoka SemiBold", False),
    "bold": ("Nunito-Bold", "Nunito-Bold.ttf", "Nunito", True),
    "xbold": ("Nunito-ExtraBold", "Nunito-ExtraBold.ttf", "Nunito ExtraBold", False),
    "body": ("Nunito-Regular", "Nunito-Regular.ttf", "Nunito", False),
}
_registered = False


def register_fonts():
    global _registered
    if _registered:
        return
    for key, (rl, f, _, _) in FONTS.items():
        pdfmetrics.registerFont(TTFont(rl, os.path.join(FONT_DIR, f)))
    _registered = True


register_fonts()


def text_width(s, font, size):
    return pdfmetrics.stringWidth(s, FONTS[font][0], size) / 72.0


def wrap(text, font, size, width):
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for w in words:
            t = (cur + " " + w).strip()
            if text_width(t, font, size) <= width or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


class Page:
    def __init__(self, number, W, H, kind, edition):
        self.number = number
        self.W, self.H = W, H
        self.kind = kind
        self.edition = edition
        self.els = []
        self.slots = []          # activity drop zones
        self.groups = {}         # count-group id -> expected count
        self.answers = []        # no-cut answers (for answer key / validation)
        self.pieces = []         # pieces printed on this page (piece sheets)
        self.warnings = []
        self.title = ""
        self.notes = ""

    # -------------------------------------------------- primitives
    def rect(self, x, y, w, h, fill=None, stroke=None, sw=1.0, r=0.0, dash=None, role=None, name=None):
        self.els.append(dict(t="rect", x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, sw=sw, r=r, dash=dash, role=role, name=name))

    def ellipse(self, x, y, w, h, fill=None, stroke=None, sw=1.0, dash=None, group=None, role=None):
        self.els.append(dict(t="ellipse", x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, sw=sw, dash=dash, group=group, role=role))

    def circle(self, cx, cy, r, **kw):
        self.ellipse(cx - r, cy - r, 2 * r, 2 * r, **kw)

    def line(self, x1, y1, x2, y2, stroke="#18354B", sw=1.0, dash=None, role=None):
        self.els.append(dict(t="line", x1=x1, y1=y1, x2=x2, y2=y2, stroke=stroke, sw=sw, dash=dash, role=role))

    def poly(self, pts, fill=None, stroke=None, sw=1.0, closed=True, dash=None, role=None):
        self.els.append(dict(t="poly", pts=pts, fill=fill, stroke=stroke, sw=sw, closed=closed, dash=dash, role=role))

    def img(self, asset, x, y, w, h, align="center", rot=0, group=None, role=None, name=None):
        self.els.append(dict(t="img", asset=asset, x=x, y=y, w=w, h=h, align=align, rot=rot, group=group, role=role, name=name))

    def text(self, s, x, y, w, h, font="bold", size=12, color="#18354B", align="left", valign="top",
             leading=1.18, min_size=None, outline=None, role=None, name=None):
        min_size = min_size or max(6.5, size * 0.6)
        sz = size
        while True:
            lines = wrap(s, font, sz, w - 0.02)
            th = len(lines) * sz * leading / 72.0
            if th <= h + 1e-6 or sz <= min_size:
                break
            sz -= 0.5
        if th > h + 0.01:
            self.warnings.append(f"text overflow on p{self.number}: '{s[:40]}' needs {th:.2f}in > {h:.2f}in")
        if sz < size:
            self.warnings.append(f"text shrunk p{self.number}: '{s[:30]}' {size}->{sz}pt")
        self.els.append(dict(t="text", s=s, lines=lines, x=x, y=y, w=w, h=h, font=font, size=sz, color=color,
                             align=align, valign=valign, leading=leading, outline=outline, role=role, name=name))
        return th

    # -------------------------------------------------- metadata
    def add_slot(self, x, y, w, h, accepts, target, mission):
        self.slots.append(dict(x=x, y=y, w=w, h=h, accepts=accepts, target=target, mission=mission))

    def add_group(self, gid, n):
        self.groups[gid] = n
