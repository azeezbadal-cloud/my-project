"""My Big Tracing Day - a colourful photo tracing book with Mia, Leo and Kai (ages 2-4).

Built on the Little Worlds tracing engine (tracing-book/src). Changes vs Leo's Little Lines:
saturated colours, photo-realistic AI baby friends instead of the Leo mascot, a day-story
structure with chapter openers, a personalised title page and a reward-sticker page.
78 interior pages.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
for p_ in (os.path.join(ROOT, "..", "tracing-book", "src"), os.path.join(ROOT, "..", "busy-book", "src")):
    p_ = os.path.abspath(p_)
    if p_ not in sys.path:
        sys.path.insert(0, p_)

import tb_art                      # noqa: E402
import tb_pages as T               # noqa: E402
import render_pdf                  # noqa: E402
from scene import Page, text_width  # noqa: E402
from glyphs import pattern_points, catmull, shape_points  # noqa: E402
from art_core import WHITE         # noqa: E402

# ---------------------------------------------------------------- full-strength colours (no pastel)
tb_art.PASTEL_MIX = 0.0
tb_art.OUTLINE = "#18354B"
T.INK = "#1E3346"
T.TRACE = "#5B7083"
T.BAND = "#FFFFFF"
T.BODY = "#FFFFFF"
T.START = "#12A150"

PHOTO_DIR = os.path.join(ROOT, "photos", "derived")
for f in os.listdir(PHOTO_DIR):
    render_pdf.PHOTOS[os.path.splitext(f)[0]] = os.path.join(PHOTO_DIR, f)

TITLE = "My Big Tracing Day"
AUTHOR = "Azeez Khudeeda"
SUBTITLE = "Trace, count & play with Mia, Leo and Kai"
FRIENDS = [("mia", "Mia", "#FFC21A"), ("leo", "Leo", "#2D9CDB"), ("kai", "Kai", "#F2545B")]
FRIEND_LINES = {"mia": "Mia loves sunny yellow and bouncy balls.", "leo": "Leo loves blue skies and big trucks.",
                "kai": "Kai loves red apples and splashy baths."}

CHAPTERS = [
    dict(key="lines", name="Morning Lines", short="MORNING", main="#FF9F1C", deep="#C25E00", tint="#FFF0D6", photo="scene_morning",
         story="Good morning! Mia, Leo and Kai wake up and stretch up high. Let's warm up our hands with lots of lines!", icon="photo:scene_morning_circle"),
    dict(key="shapes", name="Breakfast Shapes", short="BREAKFAST", main="#FF5A5F", deep="#C9303A", tint="#FFE3E4", photo="scene_breakfast",
         story="Breakfast time! Round pancakes, square toast and yummy fruit. Can you find the shapes and trace them?", icon="photo:scene_breakfast_circle"),
    dict(key="paths", name="Park Paths", short="PARK", main="#2EC27E", deep="#15814F", tint="#DDF7EA", photo="scene_park",
         story="Off to the park! The friends walk along winding paths. Help them find the way!", icon="photo:scene_park_circle"),
    dict(key="numbers", name="Bath-time Numbers", short="BATH", main="#2D9CDB", deep="#17679F", tint="#DDF0FB", photo="scene_bath",
         story="Splash! It's bath time. Let's count the ducks and bubbles and trace the numbers 1 to 10!", icon="photo:scene_bath_circle"),
    dict(key="letters", name="Bedtime Letters", short="BEDTIME", main="#8E5CF7", deep="#5B2FC9", tint="#EEE6FE", photo="scene_bedtime",
         story="Night night! The friends snuggle up with a picture book. Let's trace the letters from A to Z!", icon="photo:scene_bedtime_circle"),
]
T.CHAPTERS = CHAPTERS
T.CH = {c["key"]: c for c in CHAPTERS}
T.LINES = [(r[0], r[1], r[2], r[3], ("photo:portrait_kai" if r[4] == "leo_head" else r[4]), r[5]) for r in T.LINES]
SIZES = T.SIZES


class Book(T.Book):
    def __init__(self, edition):
        super().__init__(edition)
        self._seq = 1
        self._count = {}

    # sequential numbering whatever number the base methods ask for
    def new(self, number, kind, title):
        p = super().new(self._seq, kind, title)
        self._seq += 1
        return p

    def friend(self, p):
        return FRIENDS[p.number % 3]

    # ------------------------------------------------------------ colourful header
    def header(self, p, ch, pill, title, instr):
        W, H = self.W, self.H
        if p.kind not in ("numbers", "letters"):
            self._count[p.kind] = self._count.get(p.kind, 0) + 1
            pill = f"{ch['short']} {self._count[p.kind]}"
        p.rect(M_, M_, W - 2 * M_, H - 2 * M_ - 0.35, fill=ch["tint"], r=0.3, role="panel")
        p.rect(M_, M_, W - 2 * M_, 1.0, fill=ch["deep"], r=0.3)
        fk, fname, fcol = self.friend(p)
        p.circle(M_ + 0.55, M_ + 0.5, 0.44, fill=WHITE, stroke=None)
        p.img(f"photo:portrait_{fk}", M_ + 0.15, M_ + 0.1, 0.8, 0.8, role="portrait")
        pw = text_width(pill, "title", 11) + 0.36
        p.rect(M_ + 1.1, M_ + 0.12, pw, 0.3, fill=WHITE, r=0.15)
        p.text(pill, M_ + 1.1, M_ + 0.12, pw, 0.3, "title", 11, ch["deep"], align="center", valign="middle")
        p.text(title, M_ + 1.15 + pw + 0.05, M_ + 0.08, W - 2 * M_ - pw - 2.4, 0.38, "title", 22, WHITE, valign="middle", min_size=15)
        p.text(instr, M_ + 1.12, M_ + 0.55, W - 2 * M_ - 2.2, 0.34, "bold", 13, WHITE, valign="middle", min_size=10)
        p.img("reward_star_blank", W - M_ - 0.9, M_ + 0.08, 0.6, 0.6)
        p.text("I did it!", W - M_ - 1.05, M_ + 0.68, 0.9, 0.24, "xbold", 8.5, WHITE, align="center", valign="middle")
        self.footer(p, ch["main"])

    def footer(self, p, colour):
        y = self.H - M_ - 0.28
        p.text(f"{TITLE}  ·  Little Worlds Learning", M_, y, 4.5, 0.26, "bold", 8, "#5B6B78", valign="middle")
        p.circle(self.W - M_ - 0.17, y + 0.13, 0.17, fill=colour, stroke=None)
        p.text(str(p.number), self.W - M_ - 0.4, y, 0.46, 0.26, "title", 10, WHITE, align="center", valign="middle")

    # ------------------------------------------------------------ chapter opener
    def opener(self, ch, idx):
        p = self.new(0, "opener", ch["name"])
        W, H = self.W, self.H
        p.rect(M_, M_, W - 2 * M_, H - 2 * M_ - 0.35, fill=ch["main"], r=0.35)
        p.rect(M_ + 0.5, M_ + 0.35, 2.4, 0.42, fill=WHITE, r=0.21)
        p.text(f"PART {idx} OF 5", M_ + 0.5, M_ + 0.35, 2.4, 0.42, "title", 14, ch["deep"], align="center", valign="middle")
        p.text(ch["name"], M_, M_ + 0.85, W - 2 * M_, 0.85, "title", 44, WHITE, align="center", valign="middle")
        pw = W - 2 * M_ - 0.8
        ph = pw * 1024 / 1536
        py = M_ + 1.85
        p.rect(M_ + 0.4 - 0.1, py - 0.1, pw + 0.2, ph + 0.2, fill=WHITE, r=0.18)
        p.img("photo:" + ch["photo"], M_ + 0.4, py, pw, ph, role="photo")
        ty = py + ph + 0.35
        p.rect(M_ + 0.4, ty, pw, H - M_ - 0.75 - ty, fill=WHITE, r=0.3)
        p.text(ch["story"], M_ + 0.7, ty + 0.1, pw - 0.6, H - M_ - 0.95 - ty, "title", 22, T.INK, align="center", valign="middle", leading=1.25)
        self.footer(p, WHITE if False else ch["deep"])

    # ------------------------------------------------------------ intro pages
    def title_page(self):
        p = self.new(1, "intro", "Personalised title page")
        W, H = self.W, self.H
        p.rect(M_, M_, W - 2 * M_, H - 2 * M_ - 0.35, fill="#FFD348", r=0.35)
        for i, (x, y, c) in enumerate([(0.9, 0.9, "#FF5A5F"), (W - 1.1, 1.2, "#2D9CDB"), (1.1, H - 2.0, "#2EC27E"), (W - 1.3, H - 2.3, "#8E5CF7"), (W / 2, 0.8, "#FF9F1C")]):
            p.circle(x, y, 0.18, fill=c, stroke=None)
        bw = W - 2 * M_ - 0.8
        p.rect(M_ + 0.4, M_ + 0.45, bw, 1.25, fill=WHITE, r=0.3)
        p.line(M_ + 0.8, M_ + 1.3, M_ + 0.4 + bw - 1.6, M_ + 1.3, stroke=T.TRACE, sw=2.5, dash=(0.1, 8))
        p.text("'s", M_ + 0.4 + bw - 1.55, M_ + 0.75, 1.2, 0.7, "title", 40, T.INK, valign="middle")
        p.text("write your name here", M_ + 0.8, M_ + 1.35, bw - 2.4, 0.25, "bold", 9, "#5B6B78", align="center")
        p.text("Big Tracing Day", M_, M_ + 1.85, W - 2 * M_, 0.95, "title", 52, "#C9303A", align="center", valign="middle")
        pw = W - 2 * M_ - 1.0
        ph = pw * 1024 / 1536
        py = M_ + 3.0
        p.rect(M_ + 0.5 - 0.12, py - 0.12, pw + 0.24, ph + 0.24, fill=WHITE, r=0.2)
        p.img("photo:cover_trio", M_ + 0.5, py, pw, ph, role="photo")
        p.text("with Mia, Leo and Kai", M_, py + ph + 0.3, W - 2 * M_, 0.5, "title", 24, T.INK, align="center", valign="middle")
        p.text("Lines \u00b7 Shapes \u00b7 Paths \u00b7 Numbers \u00b7 Letters", M_, py + ph + 0.85, W - 2 * M_, 0.4, "bold", 15, T.INK, align="center", valign="middle")
        p.text(f"Created by {AUTHOR}  \u00b7  Little Worlds Learning", M_, py + ph + 1.35, W - 2 * M_, 0.35, "title", 14, "#C9303A", align="center", valign="middle")
        self.footer(p, "#FF9F1C")

    def belongs(self):
        p = self.new(2, "intro", "Meet the friends")
        W, H = self.W, self.H
        p.rect(M_, M_, W - 2 * M_, H - 2 * M_ - 0.35, fill="#E8F6FD", r=0.35)
        p.text("Meet your tracing friends!", M_, M_ + 0.3, W - 2 * M_, 0.7, "title", 34, T.INK, align="center", valign="middle")
        ys = T.centers(3, M_ + 1.2, H - M_ - 0.6)
        for i, ((k, name, col), y) in enumerate(zip(FRIENDS, ys)):
            left = i % 2 == 0
            cx = M_ + 1.6 if left else W - M_ - 1.6
            p.circle(cx, y, 1.25, fill=col, stroke=None)
            p.img(f"photo:portrait_{k}", cx - 1.1, y - 1.1, 2.2, 2.2, role="portrait")
            tx = cx + 1.5 if left else M_ + 0.4
            tw = W - M_ - tx - 0.3 if left else cx - 1.5 - tx
            p.rect(tx, y - 0.85, tw, 1.7, fill=WHITE, r=0.3)
            p.text(f"Hi! I'm {name}.", tx + 0.25, y - 0.75, tw - 0.5, 0.65, "title", 28, col if name != "Mia" else "#C98A00", valign="middle")
            p.text(FRIEND_LINES[k], tx + 0.25, y - 0.05, tw - 0.5, 0.75, "bold", 15, T.INK, valign="middle")
        self.footer(p, "#2D9CDB")

    def guide(self):
        super().guide()
        p = self.pages[-1]
        tints = ["#FFF0D6", "#FFE3E4", "#DDF7EA", "#DDF0FB"]
        k = 0
        for e in p.els:
            if e["t"] == "rect" and e.get("fill") in ("#E3F3FC", "#FFE9DF", "#DFF5EA", "#EEE7FA"):
                e["fill"] = tints[k]
                e["role"] = "panel"
                k += 1
        for e in p.els:
            if e["t"] == "text" and "•" in e["s"]:
                e["s"] = e["s"].replace("Leo", "the friends")
                e["lines"] = [ln.replace("Leo", "the friends") for ln in e["lines"]]

    def progress_map(self):
        p = self.new(4, "intro", "My big day map")
        W, H = self.W, self.H
        p.rect(M_, M_, W - 2 * M_, H - 2 * M_ - 0.35, fill="#FFF7DA", r=0.35)
        p.text("My Big Day Map", M_, M_ + 0.1, W - 2 * M_, 0.6, "title", 32, T.INK, align="center", valign="middle")
        p.text("Colour a star when you finish each part of the day!", M_, M_ + 0.7, W - 2 * M_, 0.35, "bold", 14, T.INK, align="center", valign="middle")
        ys = T.centers(5, 1.85, H - M_ - 0.55)
        pts = [(M_ + 1.35 if i % 2 == 0 else W - M_ - 1.35, y) for i, y in enumerate(ys)]
        self.trace(p, catmull(pts, 24), band=30, marker=False)
        for i, (c, (x, y)) in enumerate(zip(CHAPTERS, pts)):
            p.circle(x, y, 0.82, fill=c["main"], stroke=None)
            p.img(c["icon"], x - 0.72, y - 0.72, 1.44, 1.44, role="photo")
            left = i % 2 == 0
            tx = x + 1.05 if left else x - 1.05 - 3.4
            p.text(f"{i + 1}. {c['name']}", tx, y - 0.5, 3.4, 0.45, "title", 19, c["deep"], align="left" if left else "right", valign="middle")
            p.text(f"pages {c['_a']}–{c['_b']}", tx, y - 0.05, 3.4, 0.3, "bold", 12, T.INK, align="left" if left else "right", valign="middle")
            p.img("reward_star_blank", tx + (0 if left else 3.4 - 0.6), y + 0.28, 0.6, 0.6)
        self.footer(p, "#FFC21A")

    # ------------------------------------------------------------ path + letters (replace Leo with the friends)
    def path_page(self, i, n, title, target, ctrl):
        super().path_page(i, n, title, target, ctrl)
        p = self.pages[-1]
        fk = FRIENDS[(i - 1) % 3][0]
        p.title = p.title.replace("Leo", FRIENDS[(i - 1) % 3][1])
        for e in p.els:
            if e["t"] == "img" and e["asset"] == "p:leo_head":
                e["asset"] = f"photo:portrait_{fk}"
        for e in p.els:
            if e["t"] == "text" and ("Help Leo" in e["s"] or e["s"] == title):
                nm = FRIENDS[(i - 1) % 3][1]
                e["s"] = e["s"].replace("Leo", nm)
                e["lines"] = [ln.replace("Leo", nm) for ln in e["lines"]]
        for e in p.els:
            if e.get("role") == "road":
                e["stroke"] = WHITE if e["sw"] < 60 else T.CH["paths"]["main"]

    def letter_page(self, n, L, word, asset):
        super().letter_page(n, L, word, asset)
        p = self.pages[-1]
        fk, fname, _ = self.friend(p)
        for e in p.els:
            if e["t"] == "img" and e["asset"] == "p:leo_happy":
                e.update(asset=f"photo:portrait_{fk}", role="portrait")
            if e["t"] == "text" and e["s"].startswith("Say it with Leo"):
                e["s"] = e["s"].replace("Leo", fname)
                e["lines"] = [ln.replace("Leo", fname) for ln in e["lines"]]
            if e["t"] == "rect" and e.get("fill") == "#FFF8E7":
                e["fill"] = WHITE

    # ------------------------------------------------------------ finish
    def certificate(self):
        p = self.new(0, "finish", "Certificate")
        W, H = self.W, self.H
        p.rect(M_, M_, W - 2 * M_, H - 2 * M_ - 0.35, fill="#FFD348", r=0.35)
        p.rect(M_ + 0.25, M_ + 0.25, W - 2 * M_ - 0.5, H - 2 * M_ - 0.85, fill=WHITE, r=0.3)
        p.text("Hooray!", M_, M_ + 0.45, W - 2 * M_, 0.8, "title", 48, "#C9303A", align="center", valign="middle")
        p.text("SUPER TRACER CERTIFICATE", M_, M_ + 1.25, W - 2 * M_, 0.5, "title", 24, T.INK, align="center", valign="middle")
        pw = W - 2 * M_ - 2.0
        ph = pw * 1024 / 1536
        p.img("photo:cover_trio", M_ + 1.0, M_ + 1.9, pw, ph, role="photo")
        y = M_ + 2.1 + ph
        p.text("This certificate is for", M_, y, W - 2 * M_, 0.4, "bold", 15, T.INK, align="center", valign="middle")
        p.line(M_ + 1.2, y + 1.0, W - M_ - 1.2, y + 1.0, stroke=T.INK, sw=1.6)
        p.text("for a whole Big Tracing Day with Mia, Leo and Kai!", M_ + 0.8, y + 1.15, W - 2 * M_ - 1.6, 0.5, "bold", 14, T.INK, align="center", valign="middle")
        p.line(M_ + 1.2, H - M_ - 1.15, M_ + 3.2, H - M_ - 1.15, stroke=T.INK, sw=1.4)
        p.text("date", M_ + 1.2, H - M_ - 1.1, 2.0, 0.25, "body", 9, "#5B6B78", align="center")
        for x, c in zip(T.centers(5, M_ + 3.5, W - M_ - 0.6), CHAPTERS):
            p.circle(x, H - M_ - 1.3, 0.3, fill=c["main"], stroke=None)
            p.img("reward_star_blank", x - 0.22, H - M_ - 1.52, 0.44, 0.44)
        self.footer(p, "#FFC21A")

    def stickers(self):
        p = self.new(0, "finish", "Reward stickers")
        W, H = self.W, self.H
        p.rect(M_, M_, W - 2 * M_, H - 2 * M_ - 0.35, fill="#EEE6FE", r=0.35)
        p.text("My Reward Stickers", M_, M_ + 0.15, W - 2 * M_, 0.6, "title", 32, T.INK, align="center", valign="middle")
        p.text("Colour them in – or a grown-up can cut them out and stick them on finished pages.", M_ + 0.3, M_ + 0.75, W - 2 * M_ - 0.6, 0.35,
               "bold", 12.5, T.INK, align="center", valign="middle")
        words = ["Super!", "Well done!", "Great job!", "Wow!", "Amazing!", "You did it!", "Brilliant!", "So proud!", "Keep going!", "Star tracer!", "Yay!", "High five!"]
        cols = ["#FF9F1C", "#FF5A5F", "#2EC27E", "#2D9CDB", "#8E5CF7", "#FFC21A"]
        icons = ["star_item", "heart_big", "sun", "balloon_2", "rainbow", "shape_star"]
        xs = T.centers(3, M_ + 0.2, W - M_ - 0.2)
        ys = T.centers(4, M_ + 1.3, H - M_ - 0.6)
        r = min(0.98, (ys[1] - ys[0]) / 2 - 0.08)
        for i, w in enumerate(words):
            x, y = xs[i % 3], ys[i // 3]
            p.circle(x, y, r + 0.08, fill=None, stroke="#5B6B78", sw=1.2, dash=(5, 4), role="cut")
            p.circle(x, y, r, fill=cols[i % 6], stroke=None)
            p.circle(x, y, r - 0.12, fill=WHITE, stroke=None)
            p.img(icons[i % 6], x - 0.42, y - r + 0.2, 0.84, 0.84)
            p.text(w, x - r, y + 0.2, 2 * r, 0.45, "title", 15, cols[i % 6] if cols[i % 6] != "#FFC21A" else "#C98A00", align="center", valign="middle")
        self.footer(p, "#8E5CF7")

    def drawing_page(self):
        super().drawing_page()
        p = self.pages[-1]
        for e in p.els:
            if e["t"] == "img" and e["asset"] == "p:leo_tracing":
                e.update(asset="photo:portrait_leo", y=e["y"] + 0.3, w=1.3, h=1.3, role="portrait")
            if e["t"] == "text" and "draw Leo" in e["s"]:
                e["s"] = e["s"].replace("draw Leo a picture", "draw a picture of your day")
                e["lines"] = [e["s"]]
            if e["t"] == "rect" and e.get("stroke") == "#BFE3F6":
                e["stroke"] = "#FF9F1C"

    # ------------------------------------------------------------ build order (78 pages)
    def build(self):
        self.title_page()
        self.belongs()
        self.guide()
        map_slot = len(self.pages)
        self._seq += 1          # page 4 = day map, drawn last when page ranges are known
        starts = {}
        self.opener(CHAPTERS[0], 1)
        starts["lines"] = self._seq
        for i, row in enumerate(T.LINES):
            self.line_page(*row)
        self.opener(CHAPTERS[1], 2)
        starts["shapes"] = self._seq
        for row in T.SHAPES:
            self.shape_page(*row)
        self.shape_house()
        self.shape_parade()
        self.opener(CHAPTERS[2], 3)
        starts["paths"] = self._seq
        for i, row in enumerate(T.PATHS):
            self.path_page(i + 1, *row)
        self.opener(CHAPTERS[3], 4)
        starts["numbers"] = self._seq
        for i, row in enumerate(T.NUMBERS):
            self.number_page(0, *row)
        self.opener(CHAPTERS[4], 5)
        starts["letters"] = self._seq
        for row in T.LETTERS:
            self.letter_page(0, *row)
        ends = {"lines": starts["shapes"] - 2, "shapes": starts["paths"] - 2, "paths": starts["numbers"] - 2,
                "numbers": starts["letters"] - 2, "letters": self._seq - 1}
        for c in CHAPTERS:
            c["_a"], c["_b"] = starts[c["key"]] - 1, ends[c["key"]]
        self.certificate()
        self.stickers()
        self.drawing_page()
        last = self._seq
        self._seq = 4
        self.progress_map()
        self._seq = last
        tints = {c["tint"] for c in CHAPTERS}
        for p in self.pages:
            for e in p.els:
                if e["t"] == "rect" and e.get("fill") in tints and e.get("role") != "panel":
                    e["fill"] = WHITE
        self.pages.sort(key=lambda q: q.number)
        return self.pages


M_ = T.M
INK, MUTED, BRAND, TAGLINE = T.INK, "#5B6B78", T.BRAND, T.TAGLINE
LETTERS, NUMBERS, LINES, SHAPES, PATHS = T.LETTERS, T.NUMBERS, T.LINES, T.SHAPES, T.PATHS
centers = T.centers


# ---------------------------------------------------------------- covers
def front_cover(p, ox, oy, W, H, bleed=0.0):
    p.rect(ox - bleed, oy - bleed, W + 2 * bleed, H + 2 * bleed, fill="#FFD348", role="bg")
    for x, y, r, c in [(0.6, 0.7, 0.35, "#FF5A5F"), (W - 0.7, 1.0, 0.28, "#2D9CDB"), (0.5, H - 1.4, 0.3, "#2EC27E"), (W - 0.6, H - 1.8, 0.4, "#8E5CF7"),
                       (W * 0.5, 0.45, 0.16, "#FF9F1C"), (0.45, H * 0.5, 0.18, "#FF9F1C")]:
        p.circle(ox + x, oy + y, r, fill=c, stroke=None)
    bw = 3.4
    p.rect(ox + (W - bw) / 2, oy + 0.55, bw, 0.42, fill=WHITE, r=0.21)
    p.text(T.BRAND, ox + (W - bw) / 2, oy + 0.55, bw, 0.42, "title", 13, T.INK, align="center", valign="middle")
    tw = W - 1.1
    p.rect(ox + (W - tw) / 2, oy + 1.15, tw, 2.25, fill=WHITE, r=0.45)
    p.text("My Big", ox, oy + 1.2, W, 0.85, "title", 56, "#C9303A", align="center", valign="middle")
    p.text("Tracing Day", ox, oy + 1.95, W, 1.05, "title", 70, T.INK, align="center", valign="middle", min_size=50)
    p.text(SUBTITLE, ox, oy + 2.95, W, 0.4, "bold", 16, "#17679F", align="center", valign="middle")
    pw = W - 1.3
    ph = pw * 1024 / 1536
    py = oy + 3.75
    p.rect(ox + 0.65 - 0.14, py - 0.14, pw + 0.28, ph + 0.28, fill=WHITE, r=0.22)
    p.img("photo:cover_trio", ox + 0.65, py, pw, ph, role="photo")
    b = Book.__new__(Book)
    b.pages = []
    p.traces = getattr(p, "traces", [])
    T.Book.trace(b, p, pattern_points("wave", ox + 0.9, ox + W - 0.9, py + ph + 0.55, 0.15), band=18)
    bx_, by_, br_ = ox + W - 1.25, py + ph - 0.3, 0.78
    p.circle(bx_, by_, br_, fill="#FF5A5F", stroke=WHITE, sw=4)
    p.text("AGES", bx_ - br_, by_ - 0.5, 2 * br_, 0.34, "title", 16, WHITE, align="center", valign="middle")
    p.text("2–4", bx_ - br_, by_ - 0.18, 2 * br_, 0.6, "title", 34, WHITE, align="center", valign="middle")
    p.rect(ox + 0.5, oy + H - 1.05, W - 1.0, 0.55, fill="#C9303A", r=0.27)
    p.text("Lines · Shapes · Paths · Numbers 1–10 · Letters A–Z", ox + 0.5, oy + H - 1.05, W - 1.0, 0.55, "title", 16, WHITE, align="center", valign="middle")


def back_cover(p, ox, oy, W, H, bleed=0.0, barcode=True):
    p.rect(ox - bleed, oy - bleed, W + 2 * bleed, H + 2 * bleed, fill="#2D9CDB", role="bg")
    p.rect(ox + 0.5, oy + 0.5, W - 1.0, H - 1.0, fill=WHITE, r=0.4, role="bg")
    p.text(TITLE, ox + 0.6, oy + 0.8, W - 1.2, 0.6, "title", 32, T.INK, align="center", valign="middle")
    p.text("A colourful day of first tracing with Mia, Leo and Kai", ox + 0.6, oy + 1.4, W - 1.2, 0.4, "bold", 14, "#C9303A", align="center", valign="middle")
    blurb = ("From wake-up stretches to bedtime stories, little hands trace big, friendly dotted lines all day long. "
             f"78 bright pages build first pre-writing skills one gentle step at a time. Created by {AUTHOR}.")
    p.text(blurb, ox + 0.9, oy + 2.0, W - 1.8, 1.0, "body", 12.5, T.INK, align="center", leading=1.35)
    for i, (k, name, col) in enumerate(FRIENDS):
        x = ox + W * (i + 0.5) / 3
        p.circle(x, oy + 3.85, 0.72, fill=col, stroke=None)
        p.img(f"photo:portrait_{k}", x - 0.62, oy + 3.23, 1.24, 1.24, role="portrait")
        p.text(name, x - 0.8, oy + 4.65, 1.6, 0.4, "title", 17, T.INK, align="center", valign="middle")
    items = ["Morning lines: 12 warm-up pages", "Breakfast shapes: 10 shape pages", "Park paths: 8 follow-the-path pages",
             "Bath-time numbers: 1 to 10 with counting", "Bedtime letters: A to Z with pictures to colour", "Name page, certificate and reward stickers"]
    for i, s in enumerate(items):
        y = oy + 5.25 + i * 0.45
        p.circle(ox + 1.2, y + 0.17, 0.09, fill=CHAPTERS[i % 5]["main"], stroke=None)
        p.text(s, ox + 1.45, y, W - 2.4, 0.36, "bold", 12.5, T.INK, valign="middle")
    p.text("Ages 2–4 with a grown-up. Use crayons or pencils. Adult supervision recommended. Photo illustrations are AI-generated.",
           ox + 0.8, oy + 8.15, W - 1.6, 0.5, "body", 10, T.INK, align="center")
    p.text(f"{T.BRAND}  ·  {T.TAGLINE}", ox + 0.8, oy + H - 1.15, W - 1.6 - (2.3 if barcode else 0), 0.35, "title", 10.5, T.INK, valign="middle")
    if barcode:
        p.rect(ox + W - 0.375 - 2.0, oy + H - 0.375 - 1.2, 2.0, 1.2, fill=WHITE, stroke=None, role="barcode")
