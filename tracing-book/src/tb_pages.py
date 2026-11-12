"""Leo's Little Lines - My First Tracing Book (ages 2-4). 72 interior pages."""
import math
import tb_art  # noqa: F401  (registers pastel/line-art prefixes + new art)
from scene import Page, text_width
from glyphs import glyph, shape_points, pattern_points, spiral_points, catmull, arc
from art_core import WHITE

TITLE = "Leo's Little Lines"
SUBTITLE = "My First Tracing Book"
AGES = "AGES 2–4"
BRAND = "LITTLE WORLDS LEARNING"
TAGLINE = "Big Curiosity. Little Adventures."
VERSION = "Version 1.0 · November 2026"

INK = "#2F4A5E"        # text
MUTED = "#6B7D8C"
TRACE = "#7F93A3"      # dotted guide
BAND = "#EEF2F6"       # soft track under dots
BODY = "#EDF1F5"       # glyph body
START = "#3FA87A"      # start dot + arrow
M = 0.5
SIZES = {"US_Letter": (8.5, 11.0), "A4": (8.2677, 11.6929)}

CHAPTERS = [
    dict(key="lines", name="Warm-up Lines", short="LINES", tint="#E3F3FC", main="#BFE3F6", deep="#3E8DBF", pages=(5, 16), icon="p:rainbow"),
    dict(key="shapes", name="Shapes", short="SHAPES", tint="#FFE9DF", main="#FFCDB8", deep="#D9704A", pages=(17, 26), icon="p:shape_star"),
    dict(key="paths", name="Paths", short="PATHS", tint="#DFF5EA", main="#BDE9D3", deep="#2F9468", pages=(27, 34), icon="p:house_home"),
    dict(key="numbers", name="Numbers 1–10", short="NUMBERS", tint="#EEE7FA", main="#D8CAF2", deep="#7D5DBF", pages=(35, 44), icon="p:balloon_2"),
    dict(key="letters", name="Letters A–Z", short="LETTERS", tint="#FDE7EF", main="#F8C9DA", deep="#C94B7C", pages=(45, 70), icon="p:apple"),
]
CH = {c["key"]: c for c in CHAPTERS}

LINES = [
    (5, "straight", "Buzzy bees", "Trace from each bee to its flower.", "bee", ["flower_red", "flower_yellow", "flower_blue", "flower_purple"]),
    (6, "rain", "Pitter-patter rain", "Trace the rain down to the puddle.", "cloud_puff", ["puddle"]),
    (7, "diag_down", "Roll the ball", "Trace each ball down to the basket.", "ball", ["basket"]),
    (8, "diag_up", "Rockets go up!", "Trace each rocket up to the star.", "rocket", ["star_item"]),
    (9, "wave", "Swimming fish", "Trace the waves from the fish to the turtle.", "fish", ["turtle"]),
    (10, "zigzag", "Zig-zag car", "Trace the zig-zag road to the house.", "car", ["house_home"]),
    (11, "bumps", "Hop, hop, bunny!", "Trace the hops to the carrot.", "rabbit", ["carrot"]),
    (12, "rainbow", "Rainbow arches", "Trace every arch of the rainbow.", None, None),
    (13, "bubbles", "Round bubbles", "Trace round and round each bubble.", None, None),
    (14, "loops", "Loop-the-loop!", "Trace the loops from the plane to the cloud.", "plane", ["cloud_puff"]),
    (15, "spiral", "Snail swirls", "Trace the swirl on each snail's shell.", None, None),
    (16, "mixed", "Leo's line parade", "Trace every kind of line!", "leo_head", ["star_item"]),
]
SHAPES = [
    (17, "circle", "Circle", "sun", "round like the sun"),
    (18, "square", "Square", "gift", "like a present"),
    (19, "triangle", "Triangle", "party_hat", "like a party hat"),
    (20, "rectangle", "Rectangle", "door", "like a door"),
    (21, "oval", "Oval", "egg", "like an egg"),
    (22, "star", "Star", "star_item", "like a star in the sky"),
    (23, "heart", "Heart", "heart_big", "like a big hug"),
    (24, "diamond", "Diamond", "kite", "like a kite"),
]
PATHS = [
    (27, "Leo walks home", "house_home", [(0.0, 0.5), (1.0, 0.5)]),
    (28, "To the apple", "apple", [(0.0, 0.15), (0.45, 0.2), (0.55, 0.8), (1.0, 0.85)]),
    (29, "Down to the boat", "boat", [(0.0, 0.05), (0.8, 0.12), (0.88, 0.45), (0.12, 0.55), (0.18, 0.88), (1.0, 0.92)]),
    (30, "Zig-zag to the castle", "world_colour", [(0.0, 0.05), (0.92, 0.25), (0.08, 0.5), (0.92, 0.72), (0.15, 0.95)]),
    (31, "Round to the moon", "moon", [(0.05, 0.02), (0.05, 0.85), (0.5, 0.98), (0.95, 0.85), (0.95, 0.05)]),
    (32, "Wiggly snail trail", "snail_body", [(0.0, 0.92), (0.2, 0.45), (0.4, 0.92), (0.6, 0.45), (0.8, 0.92), (1.0, 0.4)]),
    (33, "Balloon ride", "balloon_2", [(0.0, 0.95), (0.45, 0.85), (0.62, 0.45), (0.4, 0.22), (0.22, 0.45), (0.55, 0.62), (1.0, 0.05)]),
    (34, "Home time!", "house_home", [(0.0, 0.02), (0.55, 0.05), (0.95, 0.2), (0.85, 0.45), (0.15, 0.45), (0.05, 0.7), (0.5, 0.95), (1.0, 0.9)]),
]
NUMBERS = [(1, "one", "sun", "sun"), (2, "two", "fish", "fish"), (3, "three", "balloon_2", "balloons"), (4, "four", "duck", "ducks"),
           (5, "five", "star_item", "stars"), (6, "six", "cupcake", "cupcakes"), (7, "seven", "apple", "apples"), (8, "eight", "daisy", "flowers"),
           (9, "nine", "ball", "balls"), (10, "ten", "leaf_green", "leaves")]
LETTERS = [("A", "Apple", "apple"), ("B", "Bee", "bee"), ("C", "Car", "car"), ("D", "Duck", "duck"), ("E", "Elephant", "elephant"),
           ("F", "Fish", "fish"), ("G", "Gift", "gift"), ("H", "Hen", "hen"), ("I", "Ice cream", "icecream"), ("J", "Jumper", "jumper"),
           ("K", "Kite", "kite"), ("L", "Lion", "lion_face"), ("M", "Monkey", "monkey"), ("N", "Nest", "nest"), ("O", "Octopus", "octopus"),
           ("P", "Penguin", "penguin"), ("Q", "Quilt", "quilt"), ("R", "Rabbit", "rabbit"), ("S", "Sun", "sun"), ("T", "Turtle", "turtle"),
           ("U", "Umbrella", "umbrella"), ("V", "Volcano", "volcano"), ("W", "Watermelon", "watermelon"), ("X", "Xylophone", "xylophone"),
           ("Y", "Yo-yo", "yoyo"), ("Z", "Zebra", "zebra")]


def centers(n, a, b):
    return [a + (b - a) * (i + 0.5) / n for i in range(n)]


class Book:
    def __init__(self, edition):
        self.ed = edition
        self.W, self.H = SIZES[edition]
        self.pages = []

    # ------------------------------------------------------------ frame
    def new(self, n, kind, title):
        p = Page(n, self.W, self.H, kind, self.ed)
        p.title = title
        p.X0, p.X1 = M, self.W - M
        p.CW = p.X1 - p.X0
        p.Y0, p.Y1 = 1.68, self.H - 0.95
        p.CH = p.Y1 - p.Y0
        p.traces = []
        self.pages.append(p)
        return p

    def footer(self, p, colour):
        y = self.H - M - 0.28
        p.text(f"{TITLE}  ·  Little Worlds Learning", M, y, 4.5, 0.26, "bold", 8, MUTED, valign="middle")
        p.circle(self.W - M - 0.17, y + 0.13, 0.17, fill=colour, stroke=None)
        p.text(str(p.number), self.W - M - 0.4, y, 0.46, 0.26, "title", 10, INK, align="center", valign="middle")

    def header(self, p, ch, pill, title, instr):
        W = self.W
        p.rect(M, M, W - 2 * M, 1.0, fill=ch["tint"], r=0.25)
        pw = text_width(pill, "title", 11) + 0.4
        p.rect(M + 0.2, M + 0.12, pw, 0.3, fill=ch["deep"], r=0.15)
        p.text(pill, M + 0.2, M + 0.12, pw, 0.3, "title", 11, WHITE, align="center", valign="middle")
        p.text(title, M + 0.25 + pw + 0.05, M + 0.08, W - 2 * M - pw - 1.6, 0.38, "title", 22, INK, valign="middle", min_size=15)
        p.text(instr, M + 0.22, M + 0.55, W - 2 * M - 1.4, 0.34, "bold", 13, INK, valign="middle", min_size=10)
        p.img("p:reward_star_blank", W - M - 0.9, M + 0.08, 0.6, 0.6)
        p.text("I did it!", W - M - 1.05, M + 0.68, 0.9, 0.24, "xbold", 8.5, ch["deep"], align="center", valign="middle")
        self.footer(p, ch["main"])

    # ------------------------------------------------------------ tracing primitives
    def trace(self, p, pts, dot=5.5, gap=9.5, band=20, marker=True, number=None):
        if band:
            p.poly(pts, fill=None, stroke=BAND, sw=band, closed=False, role="band")
        p.poly(pts, fill=None, stroke=TRACE, sw=dot, closed=False, dash=(0.1, gap), role="trace")
        p.traces.append(pts)
        if marker:
            self.start_marker(p, pts, 0.09 if number is None else 0.12, number)

    def start_marker(self, p, pts, r, number=None):
        x0, y0 = pts[0]
        d, k = 0, 1
        while k < len(pts) - 1 and d < 0.32:
            d += math.dist(pts[k - 1], pts[k])
            k += 1
        dx, dy = pts[k][0] - x0, pts[k][1] - y0
        ln = math.hypot(dx, dy) or 1
        ux, uy = dx / ln, dy / ln
        ax, ay = x0 + ux * (r + 0.16), y0 + uy * (r + 0.16)
        s = 0.085
        p.poly([(ax + ux * s, ay + uy * s), (ax - ux * s * 0.6 - uy * s * 0.8, ay - uy * s * 0.6 + ux * s * 0.8),
                (ax - ux * s * 0.6 + uy * s * 0.8, ay - uy * s * 0.6 - ux * s * 0.8)], fill=START, stroke=START, sw=1, role="arrow")
        p.circle(x0, y0, r, fill=START, stroke=WHITE, sw=1.5, role="start")
        if number is not None:
            p.text(str(number), x0 - r, y0 - r, 2 * r, 2 * r, "title", 9, WHITE, align="center", valign="middle")

    def draw_glyph(self, p, ch, x, y, size, big=True):
        strokes = glyph(ch)
        k = size / 100.0
        sp = [[(x + px * k, y + py * k) for px, py in s] for s in strokes]
        for s in sp:
            p.poly(s, fill=None, stroke=BODY, sw=size * 72 * 0.15, closed=False, role="body")
        for i, s in enumerate(sp):
            self.trace(p, s, dot=6 if big else 4, gap=10.5 if big else 7, band=0, marker=False)
        placed = []
        r = 0.12 if big else 0.06
        for i, s in enumerate(sp):
            pts = s
            if any(math.dist(s[0], q) < 2.4 * r for q in placed):
                want, d, k = 3.0 * r, 0.0, 1
                while k < len(s) and d + math.dist(s[k - 1], s[k]) < want:
                    d += math.dist(s[k - 1], s[k])
                    k += 1
                if k < len(s):
                    seg = math.dist(s[k - 1], s[k]) or 1
                    f = (want - d) / seg
                    q = (s[k - 1][0] + (s[k][0] - s[k - 1][0]) * f, s[k - 1][1] + (s[k][1] - s[k - 1][1]) * f)
                    pts = [q] + s[k:]
            placed.append(pts[0])
            self.start_marker(p, pts, r, (i + 1) if big else None)
        p.glyphs = getattr(p, "glyphs", []) + [(ch, x, y, size)]

    def shape(self, p, kind, cx, cy, r, big=True):
        pts = [(cx + px * r, cy + py * r) for px, py in shape_points(kind)]
        self.trace(p, pts, dot=6 if big else 4.5, gap=10 if big else 7.5, band=26 if big else 14)

    # ------------------------------------------------------------ build
    def build(self):
        self.title_page()
        self.belongs()
        self.guide()
        self.progress_map()
        for row in LINES:
            self.line_page(*row)
        for row in SHAPES:
            self.shape_page(*row)
        self.shape_house()
        self.shape_parade()
        for i, row in enumerate(PATHS):
            self.path_page(i + 1, *row)
        for i, row in enumerate(NUMBERS):
            self.number_page(35 + i, *row)
        for i, row in enumerate(LETTERS):
            self.letter_page(45 + i, *row)
        self.certificate()
        self.drawing_page()
        self.pages.sort(key=lambda q: q.number)
        return self.pages

    # ------------------------------------------------------------ intro
    def title_page(self):
        p = self.new(1, "intro", "Title page")
        W, H = self.W, self.H
        p.rect(M, M, W - 2 * M, H - 2 * M - 0.4, fill="#F3FAFE", r=0.4)
        p.text(BRAND, M, M + 0.35, W - 2 * M, 0.35, "title", 13, MUTED, align="center", valign="middle")
        p.text("Leo's", M, M + 0.8, W - 2 * M, 0.9, "title", 54, "#E8906B", align="center", valign="middle")
        p.text("Little Lines", M, M + 1.6, W - 2 * M, 1.05, "title", 66, INK, align="center", valign="middle")
        p.text(SUBTITLE, M, M + 2.65, W - 2 * M, 0.45, "bold", 20, INK, align="center", valign="middle")
        pts = pattern_points("wave", M + 0.9, W - M - 0.9, M + 3.4, 0.18)
        self.trace(p, pts, band=18)
        p.img("p:leo_tracing", W / 2 - 1.7, M + 3.75, 3.4, 4.25)
        p.text("Lines · Shapes · Paths · Numbers · Letters", M, H - M - 1.6, W - 2 * M, 0.4, "title", 15, "#3E8DBF", align="center", valign="middle")
        p.text(f"{AGES}  ·  {TAGLINE}", M, H - M - 1.15, W - 2 * M, 0.3, "bold", 11, MUTED, align="center", valign="middle")
        self.footer(p, "#FFE3A3")

    def belongs(self):
        p = self.new(2, "intro", "This book belongs to")
        W, H = self.W, self.H
        p.rect(M, M, W - 2 * M, H - 2 * M - 0.4, fill="#FFF8E7", r=0.4)
        p.text("This book belongs to", M, M + 0.6, W - 2 * M, 0.7, "title", 34, INK, align="center", valign="middle")
        bw = W - 2.4
        p.rect((W - bw) / 2, M + 1.55, bw, 1.15, fill=WHITE, stroke="#F2D58A", sw=3, r=0.3)
        p.line((W - bw) / 2 + 0.4, M + 2.4, (W + bw) / 2 - 0.4, M + 2.4, stroke=TRACE, sw=2.5, dash=(0.1, 8))
        p.text("Draw yourself here!", M, M + 3.0, W - 2 * M, 0.4, "title", 16, "#E8906B", align="center", valign="middle")
        fw = W - 3.0
        p.rect((W - fw) / 2, M + 3.5, fw, 4.2, fill=WHITE, stroke="#F2D58A", sw=3, r=0.3, dash=(6, 5))
        p.img("p:leo_wave", W - M - 1.9, H - M - 2.75, 1.7, 2.1)
        p.text("Hi! I'm Leo.\nLet's draw lines together!", M + 0.3, H - M - 2.2, W - 2 * M - 2.4, 1.0, "title", 18, INK, valign="middle")
        self.footer(p, "#FFE3A3")

    def guide(self):
        p = self.new(3, "intro", "Grown-up guide")
        W, H = self.W, self.H
        p.text("FOR GROWN-UPS", M, M, W - 2 * M, 0.5, "title", 24, INK, valign="middle")
        p.text("Little hands are just getting ready to write. This book builds the first skills step by step: big lines, shapes, paths, "
               "then numbers and letters when your child is ready.", M, M + 0.5, W - 2 * M, 0.55, "body", 11, INK, leading=1.25)
        boxes = [
            ("HOW TO USE", ["Start at the green dot and follow the arrow.", "Trace with a finger first, then with a crayon.",
                            "One or two pages a day is plenty – stop while it's still fun.", "Go back to favourite pages any time."]),
            ("HOLDING THE CRAYON", ["Chunky crayons are easiest for little hands.", "A whole-hand grip is normal at 2; a finger grip comes later.",
                                    "Let your child choose either hand.", "Sit at a table with feet supported if you can."]),
            ("CHEER THE EFFORT", ["Wobbly lines are perfect – they are learning!", "Praise trying: “You followed the dots all the way!”",
                                  "Colour the star at the top of each page together.", "Name the pictures and talk about them."]),
            ("PRINTING & SAFETY", ["Use crayons or pencils – markers can bleed through the paper.", "Printing at home? Print at Actual size; single-sided is best.",
                                   "Always supervise young children with crayons and pencils.", "Lamination plus a dry-erase crayon makes pages reusable."]),
        ]
        bw = (W - 2 * M - 0.25) / 2
        bh = (H - M - 0.6 - (M + 1.2)) / 2 - 0.12
        tints = ["#E3F3FC", "#FFE9DF", "#DFF5EA", "#EEE7FA"]
        for i, (head, items) in enumerate(boxes):
            x = M + (i % 2) * (bw + 0.25)
            y = M + 1.2 + (i // 2) * (bh + 0.25)
            p.rect(x, y, bw, bh, fill=tints[i], r=0.25)
            p.text(head, x + 0.2, y + 0.15, bw - 0.4, 0.36, "title", 14, INK, valign="middle")
            p.text("\n".join("•  " + s for s in items), x + 0.2, y + 0.6, bw - 0.4, bh - 0.7, "body", 13, INK, leading=1.45)
        self.footer(p, "#FFE3A3")

    def progress_map(self):
        p = self.new(4, "intro", "My tracing journey")
        W, H = self.W, self.H
        p.text("My Tracing Journey", M, M, W - 2 * M, 0.6, "title", 30, INK, align="center", valign="middle")
        p.text("Colour a star when you finish each part!", M, M + 0.6, W - 2 * M, 0.35, "bold", 13, INK, align="center", valign="middle")
        ys = centers(5, 1.7, H - M - 0.6)
        pts = [(M + 1.3 if i % 2 == 0 else W - M - 1.3, y) for i, y in enumerate(ys)]
        self.trace(p, catmull(pts, 24), band=28, marker=False)
        for i, (c, (x, y)) in enumerate(zip(CHAPTERS, pts)):
            p.circle(x, y, 0.72, fill=c["tint"], stroke=c["main"], sw=4)
            p.img(c["icon"], x - 0.5, y - 0.5, 1.0, 1.0)
            tx = x + 0.95 if i % 2 == 0 else x - 0.95 - 3.4
            p.text(f"{i + 1}. {c['name']}", tx, y - 0.45, 3.4, 0.42, "title", 17, c["deep"], align="left" if i % 2 == 0 else "right", valign="middle")
            a, b = c["pages"]
            p.text(f"pages {a}–{b}", tx, y - 0.03, 3.4, 0.3, "bold", 11, INK, align="left" if i % 2 == 0 else "right", valign="middle")
            p.img("p:reward_star_blank", tx + (0 if i % 2 == 0 else 3.4 - 0.55), y + 0.28, 0.55, 0.55)
        self.footer(p, "#FFE3A3")

    # ------------------------------------------------------------ lines chapter
    def line_page(self, n, kind, title, instr, start, ends):
        c = CH["lines"]
        p = self.new(n, "lines", title)
        self.header(p, c, f"LINES {n - 4}", title, instr)
        X0, X1, Y0, Y1, CWd, CHd = p.X0, p.X1, p.Y0, p.Y1, p.CW, p.CH
        if kind in ("straight", "diag_down", "diag_up", "wave", "zigzag", "bumps", "loops", "mixed"):
            rows = 4
            rh = CHd / rows
            s = min(1.1, rh * 0.62)
            kinds = ["straight", "wave", "zigzag", "bumps"] if kind == "mixed" else [kind] * rows
            for i, y in enumerate(centers(rows, Y0, Y1)):
                end = ends[i % len(ends)]
                p.img("p:" + start, X0, y - s / 2, s, s)
                p.img("p:" + end, X1 - s, y - s / 2, s, s)
                k = kinds[i]
                amp = rh * (0.2 if k == "loops" else 0.28)
                if k == "diag_down":
                    pts = [(X0 + s + 0.2, y - amp), (X1 - s - 0.2, y + amp)]
                elif k == "diag_up":
                    pts = [(X0 + s + 0.2, y + amp), (X1 - s - 0.2, y - amp)]
                else:
                    pts = pattern_points(k, X0 + s + 0.25, X1 - s - 0.25, y, amp)
                self.trace(p, pts)
        elif kind == "rain":
            cols = centers(4, X0, X1)
            p.img("p:cloud_puff", X0 + 0.2, Y0, CWd - 0.4, 1.3)
            p.img("p:puddle", X0, Y1 - 1.0, CWd, 1.0)
            for x in cols:
                self.trace(p, [(x, Y0 + 1.5), (x, Y1 - 1.15)])
        elif kind == "rainbow":
            cx, by = X0 + CWd / 2, Y1 - 0.9
            rmax = min(CWd / 2 - 0.3, CHd - 1.3)
            for r in [rmax - i * 0.6 for i in range(5)]:
                self.trace(p, arc(cx, by, r, r, 180, 360, 80))
            p.img("p:cloud_puff", X0, by - 0.25, 1.5, 0.95)
            p.img("p:cloud_puff", X1 - 1.5, by - 0.25, 1.5, 0.95)
        elif kind == "bubbles":
            spots = [(0.18, 0.18, 0.75), (0.62, 0.14, 0.55), (0.88, 0.35, 0.45), (0.38, 0.5, 1.0), (0.82, 0.72, 0.8), (0.14, 0.78, 0.6), (0.55, 0.88, 0.4)]
            for fx, fy, fr in spots:
                cx, cy = X0 + fx * CWd, Y0 + fy * (CHd - 0.3)
                self.trace(p, arc(cx, cy, fr, fr, -90, 270, 72))
            p.img("p:duck", X1 - 1.3, Y1 - 1.2, 1.3, 1.2)
        elif kind == "spiral":
            for i, (cx, cy) in enumerate([(cx, cy) for cy in centers(2, Y0, Y1) for cx in centers(2, X0, X1)]):
                w = CWd / 2 - 0.2
                h = w * 200 / 240
                x0, y0 = cx - w / 2, cy - h / 2
                p.img("p:snail_body", x0, y0, w, h)
                sc = w / 240
                self.trace(p, spiral_points(x0 + 110 * sc, y0 + 96 * sc, 54 * sc, 2.25), band=12, dot=5, gap=8.5)

    # ------------------------------------------------------------ shapes chapter
    def shape_page(self, n, kind, name, pic, like):
        c = CH["shapes"]
        p = self.new(n, "shapes", name)
        self.header(p, c, f"SHAPES {n - 16}", name, f"Trace the {name.lower()}. Start at the green dot!")
        r = min(p.CW * 0.27, p.CH * 0.27)
        cx, cy = p.X0 + p.CW * 0.38, p.Y0 + r + 0.35
        self.shape(p, kind, cx, cy, r)
        bx = p.X1 - 2.0
        p.rect(bx, p.Y0 + 0.2, 2.0, 2.35, fill=c["tint"], r=0.25)
        p.img("p:" + pic, bx + 0.25, p.Y0 + 0.3, 1.5, 1.5)
        p.text(like, bx + 0.05, p.Y0 + 1.85, 1.9, 0.6, "title", 12.5, INK, align="center", valign="middle")
        ry = p.Y1 - 1.0
        p.text("Now trace these little ones!", p.X0, ry - 1.15, p.CW, 0.35, "title", 14, c["deep"], align="center", valign="middle")
        for x in centers(3, p.X0, p.X1):
            self.shape(p, kind, x, ry, 0.62, big=False)

    def shape_house(self):
        c = CH["shapes"]
        p = self.new(25, "shapes", "Shape house")
        self.header(p, c, "SHAPES 9", "Shape house", "Trace the shapes to build a house.")
        X0, Y0, CWd, CHd = p.X0, p.Y0, p.CW, p.CH
        cx = X0 + CWd * 0.45
        s = min(CWd * 0.26, CHd * 0.26)
        body_top = Y0 + CHd * 0.42
        self.trace(p, [(cx - s, body_top), (cx + s, body_top), (cx + s, body_top + 2 * s * 0.95), (cx - s, body_top + 2 * s * 0.95), (cx - s, body_top)])
        self.trace(p, [(cx, body_top - s * 1.3), (cx + s * 1.25, body_top - 0.08), (cx - s * 1.25, body_top - 0.08), (cx, body_top - s * 1.3)])
        dw, dh = s * 0.32, s * 0.62
        dtop = body_top + 2 * s * 0.95 - 2 * dh - 0.05
        self.trace(p, [(cx - dw, dtop), (cx + dw, dtop), (cx + dw, dtop + 2 * dh), (cx - dw, dtop + 2 * dh), (cx - dw, dtop)], band=12)
        self.trace(p, arc(cx - s * 0.55, body_top + s * 0.45, s * 0.24, s * 0.24, -90, 270, 48), band=12)
        self.trace(p, arc(cx + s * 0.55, body_top + s * 0.45, s * 0.24, s * 0.24, -90, 270, 48), band=12)
        self.trace(p, arc(p.X1 - 1.0, Y0 + 0.9, 0.62, 0.62, -90, 270, 60))
        p.rect(X0, p.Y1 - 0.35, CWd, 0.3, fill="#DFF5EA", r=0.15)
        p.text("square · triangle · rectangle · circles", X0, Y0 + 0.1, CWd * 0.7, 0.4, "title", 14, c["deep"], valign="middle")

    def shape_parade(self):
        c = CH["shapes"]
        p = self.new(26, "shapes", "Shape parade")
        self.header(p, c, "SHAPES 10", "Shape parade", "Trace all the shapes. Can you name them?")
        kinds = ["circle", "square", "triangle", "star", "heart", "diamond"]
        rr = min(p.CW / 6 - 0.15, p.CH / 4 - 0.45)
        for i, k in enumerate(kinds):
            cx = centers(3, p.X0, p.X1)[i % 3]
            cy = centers(2, p.Y0, p.Y1)[i // 3] - 0.2
            self.shape(p, k, cx, cy, rr, big=False)
            p.text(k, cx - 1.0, cy + rr + 0.2, 2.0, 0.35, "title", 14, INK, align="center", valign="middle")

    # ------------------------------------------------------------ paths chapter
    def path_page(self, i, n, title, target, ctrl):
        c = CH["paths"]
        p = self.new(n, "paths", title)
        self.header(p, c, f"PATHS {i}", title, "Help Leo follow the path. Stay on the road!")
        X0, Y0, CWd, CHd = p.X0 + 0.65, p.Y0 + 0.65, p.CW - 1.3, p.CH - 1.3
        pts = catmull([(X0 + u * CWd, Y0 + v * CHd) for u, v in ctrl], 28)
        p.poly(pts, fill=None, stroke=c["main"], sw=62, closed=False, role="road")
        p.poly(pts, fill=None, stroke=c["tint"], sw=50, closed=False, role="road")
        self.trace(p, pts, band=0)
        sx, sy = pts[0]
        ex, ey = pts[-1]
        p.img("p:leo_head", sx - 0.55, sy - 0.55 - 0.55, 1.1, 1.0)
        p.img("p:" + target, ex - 0.65, ey - 0.65 - 0.5, 1.3, 1.3)
        p.answers.append(("path length (in)", round(sum(math.dist(pts[k], pts[k + 1]) for k in range(len(pts) - 1)), 1)))

    # ------------------------------------------------------------ numbers chapter
    def number_page(self, n, num, word, asset, plural):
        c = CH["numbers"]
        p = self.new(n, "numbers", f"Number {num}")
        self.header(p, c, f"NUMBER {num}", f"{num}  ·  {word}", f"Trace the {num}. Then count and colour {num} {plural}.")
        big = min(3.3, p.CH * 0.4)
        bx = p.X0 + 0.3
        self.draw_glyph(p, str(num), bx, p.Y0 + 0.2, big)
        rx = bx + big + 0.4
        p.text(word, rx, p.Y0 + 0.4, p.X1 - rx, 0.9, "title", 44, c["deep"], align="center", valign="middle")
        dots_y = p.Y0 + 1.55
        per = 5
        for d in range(num):
            r_, k = divmod(d, per)
            cnt = min(per, num - r_ * per)
            xs = centers(cnt, rx + 0.2, p.X1 - 0.2)
            p.circle(xs[k], dots_y + r_ * 0.55, 0.2, fill=c["main"], stroke=c["deep"], sw=1.5, group=f"dots_{num}")
        p.add_group(f"dots_{num}", num)
        sy = p.Y0 + big + 0.5
        p.text("Trace again:", p.X0, sy, 1.6, 0.4, "title", 13, c["deep"], valign="middle")
        ssz = 1.1
        for x in centers(3, p.X0 + 1.7, p.X1):
            self.draw_glyph(p, str(num), x - ssz / 2, sy - 0.15, ssz, big=False)
        py = sy + ssz + 0.15
        ph = p.Y1 - py
        p.rect(p.X0, py, p.CW, ph, fill=c["tint"], r=0.25)
        p.text(f"Count and colour {num} {plural}!", p.X0, py + 0.08, p.CW, 0.4, "title", 15, INK, align="center", valign="middle")
        per_row = 5
        rows = 1 if num <= 5 else 2
        size = min(1.05, (ph - 0.65) / rows - 0.08, p.CW / per_row - 0.15)
        k = 0
        for r_ in range(rows):
            cnt = min(per_row, num - r_ * per_row)
            yy = py + 0.55 + r_ * (size + 0.08) + ((ph - 0.6) - rows * (size + 0.08)) / 2
            for x in centers(cnt, p.X0 + (p.CW - p.CW * cnt / per_row) / 2, p.X0 + (p.CW + p.CW * cnt / per_row) / 2):
                p.img("line:" + asset, x - size / 2, yy, size, size, group=f"count_{num}")
                k += 1
        p.add_group(f"count_{num}", num)

    # ------------------------------------------------------------ letters chapter
    def letter_page(self, n, L, word, asset):
        c = CH["letters"]
        p = self.new(n, "letters", f"Letter {L}")
        self.header(p, c, f"LETTER {L}", f"{L} is for {word}", f"Trace the big {L}. Then colour the {word.lower()}!")
        big = min(3.4, p.CH * 0.42)
        bx = p.X0 + 0.25
        self.draw_glyph(p, L, bx, p.Y0 + 0.2, big)
        rx = bx + big + 0.35
        rw = p.X1 - rx
        pic = min(rw - 0.2, big - 0.6)
        p.rect(rx, p.Y0 + 0.1, rw, big + 0.2, fill=c["tint"], r=0.25)
        p.img("line:" + asset, rx + (rw - pic) / 2, p.Y0 + 0.2, pic, pic)
        fs = 30
        w1 = text_width(word[0], "title", fs)
        w2 = text_width(word[1:], "title", fs)
        tx = rx + (rw - w1 - w2) / 2
        ty = p.Y0 + 0.25 + pic
        p.text(word[0], tx, ty, w1 + 0.02, 0.55, "title", fs, c["deep"], valign="middle")
        p.text(word[1:], tx + w1, ty, w2 + 0.05, 0.55, "title", fs, INK, valign="middle")
        sy = p.Y0 + big + 0.55
        p.text("Trace again:", p.X0, sy, 1.6, 0.4, "title", 13, c["deep"], valign="middle")
        ssz = 1.1
        for x in centers(4, p.X0 + 1.6, p.X1):
            self.draw_glyph(p, L, x - ssz / 2, sy - 0.1, ssz, big=False)
        ty2 = sy + ssz + 0.35
        p.rect(p.X0, ty2, p.CW, p.Y1 - ty2, fill="#FFF8E7", r=0.25)
        lh = min(1.9, p.Y1 - ty2 - 0.2)
        p.img("p:leo_happy", p.X0 + 0.15, ty2 + 0.1, lh * 0.8, lh)
        p.text(f"Say it with Leo:\n“{L} is for {word}!”", p.X0 + lh * 0.8 + 0.35, ty2 + 0.1, p.CW - lh * 0.8 - 0.5, (p.Y1 - ty2) * 0.62,
               "title", 22, INK, valign="middle", min_size=14)
        p.text(f"What else starts with {L}?", p.X0 + lh * 0.8 + 0.35, ty2 + (p.Y1 - ty2) * 0.62, p.CW - lh * 0.8 - 0.5, (p.Y1 - ty2) * 0.3,
               "bold", 14, c["deep"], valign="middle")
        p.answers.append((L, word))

    # ------------------------------------------------------------ finish
    def certificate(self):
        p = self.new(71, "finish", "Certificate")
        W, H = self.W, self.H
        p.rect(M, M, W - 2 * M, H - 2 * M - 0.4, fill="#FFF8E7", stroke="#F2D58A", sw=5, r=0.4)
        p.rect(M + 0.18, M + 0.18, W - 2 * M - 0.36, H - 2 * M - 0.76, fill=None, stroke="#F8C9DA", sw=2, r=0.32, dash=(0.1, 8))
        p.text("Hooray!", M, M + 0.6, W - 2 * M, 0.8, "title", 46, "#E8906B", align="center", valign="middle")
        p.text("SUPER TRACER CERTIFICATE", M, M + 1.4, W - 2 * M, 0.5, "title", 24, INK, align="center", valign="middle")
        p.img("p:leo_cheer", W / 2 - 1.3, M + 2.05, 2.6, 3.25)
        p.text("This certificate is for", M, M + 5.45, W - 2 * M, 0.4, "bold", 14, INK, align="center", valign="middle")
        p.line(M + 1.4, M + 6.45, W - M - 1.4, M + 6.45, stroke=INK, sw=1.6)
        p.text("for tracing lines, shapes, paths, numbers and letters with Leo!", M + 0.8, M + 6.65, W - 2 * M - 1.6, 0.6, "bold", 13, INK, align="center", valign="middle")
        p.line(M + 1.4, H - M - 1.45, M + 3.4, H - M - 1.45, stroke=INK, sw=1.4)
        p.text("date", M + 1.4, H - M - 1.4, 2.0, 0.25, "body", 9, MUTED, align="center")
        for i, x in enumerate(centers(5, M + 3.6, W - M - 0.8)):
            p.img("p:reward_star_blank", x - 0.3, H - M - 1.9, 0.6, 0.6)
        p.text("one star for each part!", M + 3.6, H - M - 1.25, W - 2 * M - 4.4, 0.25, "body", 9, MUTED, align="center")
        self.footer(p, "#FFE3A3")

    def drawing_page(self):
        p = self.new(72, "finish", "My best drawing")
        W, H = self.W, self.H
        p.text("My Best Drawing", M, M, W - 2 * M, 0.6, "title", 30, INK, align="center", valign="middle")
        p.text("Use your lines and shapes to draw Leo a picture!", M, M + 0.6, W - 2 * M, 0.35, "bold", 13, INK, align="center", valign="middle")
        p.rect(M, M + 1.15, W - 2 * M, H - 2 * M - 1.65, fill=WHITE, stroke="#BFE3F6", sw=4, r=0.35)
        p.img("p:leo_tracing", W - M - 1.45, H - M - 2.25, 1.3, 1.65)
        self.footer(p, "#FFE3A3")


# ---------------------------------------------------------------- covers
def front_cover(p, ox, oy, W, H, bleed=0.0):
    """Draw the front cover in the trim box (ox, oy, W, H); background bleeds by `bleed`."""
    p.rect(ox - bleed, oy - bleed, W + 2 * bleed, H + 2 * bleed, fill="#DDF1FB", role="bg")
    p.img("p:hill", ox - 0.4, oy + H - 2.6, W * 0.75, 2.4, align="bottom")
    p.img("p:hill", ox + W * 0.3, oy + H - 2.3, W * 0.8, 2.1, align="bottom")
    p.rect(ox - bleed, oy + H - 0.9, W + 2 * bleed, 0.9 + bleed, fill="#CDEBB0", role="bg")
    p.img("p:cloud_puff", ox + 0.4, oy + 3.6, 1.7, 1.08)
    p.img("p:cloud_puff", ox + W - 2.0, oy + 4.6, 1.5, 0.95)
    bw = 3.4
    p.rect(ox + (W - bw) / 2, oy + 0.55, bw, 0.42, fill=WHITE, r=0.21)
    p.text(BRAND, ox + (W - bw) / 2, oy + 0.55, bw, 0.42, "title", 13, INK, align="center", valign="middle")
    tw = W - 1.3
    p.rect(ox + (W - tw) / 2, oy + 1.15, tw, 2.25, fill=WHITE, r=0.45)
    p.text("Leo's", ox, oy + 1.2, W, 0.85, "title", 54, "#E8906B", align="center", valign="middle")
    p.text("Little Lines", ox, oy + 1.95, W, 1.1, "title", 70, INK, align="center", valign="middle", min_size=50)
    p.text(SUBTITLE, ox, oy + 2.95, W, 0.4, "bold", 18, "#3E8DBF", align="center", valign="middle")
    # dotted demo lines
    b = Book.__new__(Book)
    b.pages = []
    p.traces = getattr(p, "traces", [])
    Book.trace(b, p, pattern_points("wave", ox + 0.8, ox + W - 0.8, oy + 3.85, 0.16), band=18)
    Book.trace(b, p, [(ox + 0.95 + 0.65 * math.cos(math.radians(a)), oy + 5.5 + 0.65 * math.sin(math.radians(a))) for a in range(-90, 271, 5)], band=16)
    Book.trace(b, p, [(ox + W - 1.6 + 0.62 * x, oy + 6.2 + 0.62 * y) for x, y in shape_points("star")], band=16)
    p.img("p:leo_tracing", ox + W / 2 - 1.75, oy + 4.15, 3.5, 4.4)
    bx_, by_, br_ = ox + W - 1.35, oy + H - 2.6, 0.75
    p.circle(bx_, by_, br_, fill="#FFF1B8", stroke="#F2C94C", sw=3)
    p.text("AGES", bx_ - br_, by_ - 0.5, 2 * br_, 0.34, "title", 16, INK, align="center", valign="middle")
    p.text("2–4", bx_ - br_, by_ - 0.18, 2 * br_, 0.6, "title", 34, INK, align="center", valign="middle")
    p.text("Lines · Shapes · Paths · Numbers · Letters", ox + 0.4, oy + H - 0.8, W - 0.8, 0.45, "title", 16, INK, align="center", valign="middle")


def back_cover(p, ox, oy, W, H, bleed=0.0, barcode=True):
    p.rect(ox - bleed, oy - bleed, W + 2 * bleed, H + 2 * bleed, fill="#FFF3E9", role="bg")
    p.text(TITLE, ox + 0.6, oy + 0.7, W - 1.2, 0.6, "title", 30, INK, align="center", valign="middle")
    p.text("My first tracing book with Leo the Little Explorer", ox + 0.6, oy + 1.3, W - 1.2, 0.4, "bold", 14, "#E8906B", align="center", valign="middle")
    blurb = ("Big, friendly dotted lines help little hands get ready to write. Leo leads the way through 72 pastel pages: "
             "warm-up lines, shapes, paths to follow, numbers 1 to 10 and letters A to Z – with pictures to colour along the way.")
    p.text(blurb, ox + 0.7, oy + 1.95, W - 1.4, 1.3, "body", 12.5, INK, align="center", leading=1.35)
    items = ["12 warm-up line pages", "10 shape pages", "8 follow-the-path pages", "10 number pages with counting", "26 letter pages with pictures to colour",
             "Grown-up tips and a certificate"]
    for i, s in enumerate(items):
        y = oy + 3.55 + i * 0.5
        p.circle(ox + 1.25, y + 0.17, 0.09, fill=START, stroke=None)
        p.text(s, ox + 1.5, y, W - 2.5, 0.36, "bold", 13, INK, valign="middle")
    p.img("p:leo_wave", ox + W - 2.4, oy + 3.6, 1.8, 2.25)
    p.text("For ages 2–4 with a grown-up. Use crayons or pencils. Adult supervision recommended.", ox + 0.7, oy + 6.75, W - 1.4, 0.5, "body", 10.5, INK, align="center")
    p.text(f"{BRAND}  ·  {TAGLINE}", ox + 0.7, oy + H - 1.0, W - 1.4 - (2.4 if barcode else 0), 0.35, "title", 11, INK, align="center" if not barcode else "left", valign="middle")
    if barcode:
        p.rect(ox + W - 0.375 - 2.0, oy + H - 0.375 - 1.2, 2.0, 1.2, fill=WHITE, role="barcode")
