"""Page builders for My Magic Busy Book (48 pages).

Every layout is computed from the page's content box so the US Letter and A4
editions are each laid out properly (no stretching).  Piece cards and slots
keep the same physical size in both editions so pieces always fit the boards.
"""
import math
from scene import Page, text_width
import content as C
from art_core import (NAVY, YELLOW, SKY, LIME, CORAL, PINK, CREAM, WHITE, ACT, GREY, DGREY, LGREY)

M = 0.5            # page margin (home-printer safe area >= 0.4in)
PIECE = 1.55       # cut-out card size (in)
SLOT = 1.65        # board drop-zone size (in)
GAP = 0.28         # cutting space between cards
HINT = "#8C9BA7"
MUTED = "#5B6B78"

SIZES = {"US_Letter": (8.5, 11.0), "A4": (8.2677, 11.6929)}


# =============================================================== helpers
def centers(n, a, b):
    return [a + (b - a) * (i + 0.5) / n for i in range(n)]


def two(n):
    return f"{n:02d}"


class Book:
    def __init__(self, edition):
        self.ed = edition
        self.W, self.H = SIZES[edition]
        self.sheet_of = {}       # piece id -> sheet page
        self.sheets = self.allocate()
        self.pages = []

    # ------------------------------------------------ piece allocation (first-fit, sets never split)
    def allocate(self):
        cap = 20
        sheets = [[] for _ in range(5)]
        for s in C.PIECE_SETS:
            n = len(s["items"])
            for sh in sheets:
                if sum(len(x["items"]) for x in sh) + n <= cap:
                    sh.append(s)
                    break
            else:
                raise RuntimeError(f"Pieces do not fit on 5 sheets: {s['code']}")
        for i, sh in enumerate(sheets):
            for s in sh:
                for pid, _, _ in s["items"]:
                    self.sheet_of[pid] = 41 + i
        return sheets

    def set_pages(self, code):
        return sorted({m["page"] for m in C.MISSIONS for pid in m["pieces"] if pid.startswith(code) and pid[len(code):].isdigit()})

    # ------------------------------------------------ geometry
    def new(self, number, kind):
        p = Page(number, self.W, self.H, kind, self.ed)
        p.X0, p.X1 = M, self.W - M
        p.CW = p.X1 - p.X0
        p.Y0, p.Y1 = 1.85, self.H - 0.9
        p.CH = p.Y1 - p.Y0
        self.pages.append(p)
        return p

    # ------------------------------------------------ shared furniture
    def footer(self, p, centre_text=None, icon=None, colour=SKY):
        y = self.H - M - 0.3
        p.circle(self.W - M - 0.17, y + 0.15, 0.17, fill=colour, stroke=NAVY, sw=1.2)
        p.text(str(p.number), self.W - M - 0.4, y + 0.02, 0.46, 0.26, "title", 10, NAVY, align="center", valign="middle")
        if centre_text:
            x = M
            if icon:
                p.img(icon, x, y + 0.01, 0.26, 0.26)
                x += 0.34
            p.text(centre_text, x, y + 0.02, self.W - M - 0.5 - x, 0.26, "bold", 8.5, NAVY, valign="middle", min_size=7)
        else:
            p.text("MY MAGIC BUSY BOOK  \u00b7  Little Worlds Learning", M, y + 0.02, 4.0, 0.26, "bold", 7.5, MUTED, valign="middle")

    def pieces_note(self, m):
        if not m["pieces"]:
            return "No cutting needed – use a finger, crayon or dry-erase pen", "icon_nocut"
        groups = {}
        for pid in m["pieces"]:
            code = pid.rstrip("0123456789")
            groups.setdefault((self.sheet_of[pid], code), []).append(pid)
        parts = []
        for (sheet, code), lst in sorted(groups.items()):
            nums = sorted(int(x[len(code):]) for x in lst)
            if len(nums) > 2 and nums == list(range(nums[0], nums[-1] + 1)):
                lab = f"{code}{nums[0]}–{code}{nums[-1]}"
            else:
                lab = ", ".join(f"{code}{n}" for n in nums)
            parts.append(f"{lab} (p{sheet})")
        return "Cut-out pieces: " + "  ·  ".join(parts), "icon_scissors"

    def mission_frame(self, m, header_h=1.2):
        p = self.new(m["page"], "mission")
        ch = C.CHAPTER[m["ch"]]
        p.mission, p.chapter = m, ch
        p.title = f"Mission {two(m['n'])} - {m['title']}"
        W = self.W
        p.rect(M, M, W - 2 * M, header_h, fill=ch["tint"], stroke=ch["colour"], sw=1.5, r=0.22)
        p.rect(M + 0.2, M + 0.14, 1.32, 0.32, fill=ch["deep"], r=0.16)
        p.text(f"MISSION {two(m['n'])}", M + 0.2, M + 0.14, 1.32, 0.32, "title", 13, WHITE, align="center", valign="middle")
        p.text(ch["name"].upper(), M + 1.62, M + 0.14, 3.0, 0.32, "xbold", 9.5, ch["deep"], valign="middle")
        p.text(m["title"], M + 0.2, M + 0.46, W - 2 * M - 1.55, 0.46, "title", 26, NAVY, valign="middle", min_size=17)
        sk_label, sk_icon = C.SKILLS[m["skill"]]
        pw = 0.38 + text_width(sk_label, "xbold", 9) + 0.12
        p.rect(M + 0.2, M + 0.9, pw, 0.26, fill=WHITE, stroke=ch["deep"], sw=1.2, r=0.13)
        p.img(sk_icon, M + 0.25, M + 0.915, 0.23, 0.23)
        p.text(sk_label, M + 0.52, M + 0.9, pw - 0.3, 0.26, "xbold", 9, NAVY, valign="middle")
        p.text(m["instr"], M + 0.3 + pw, M + 0.86, W - 2 * M - pw - 1.6, 0.32, "bold", 14.5, NAVY, valign="middle", min_size=11)
        # achievement star
        p.img("reward_star_blank", W - M - 1.05, M + 0.1, 0.78, 0.78)
        p.text("I did it!", W - M - 1.2, M + 0.86, 1.08, 0.24, "xbold", 9, ch["deep"], align="center", valign="middle")
        note, icon = self.pieces_note(m)
        self.footer(p, note, icon, ch["colour"])
        p.Y0 = M + header_h + 0.15
        p.CH = p.Y1 - p.Y0
        return p, ch

    def slot(self, p, cx, cy, accepts, target, hint=None, w=SLOT, h=SLOT, fill=WHITE, hint_scale=0.74, dot=True):
        x, y = cx - w / 2, cy - h / 2
        p.rect(x, y, w, h, fill=fill, stroke=HINT, sw=1.7, r=0.14, dash=(5, 3.5), role="slot")
        if hint:
            hs = min(w, h) * hint_scale
            p.img(hint, cx - hs / 2, cy - hs / 2, hs, hs, role="hint")
        if dot:
            p.img("fastener_dot", x + w - 0.27, y + 0.07, 0.2, 0.2, role="fastener")
        p.add_slot(x, y, w, h, accepts if isinstance(accepts, list) else [accepts], target, p.mission["n"])

    def leo_say(self, p, pose, x, y, h, text, bubble_w=2.0, side="right", size=12.5):
        lw = h * 0.8
        lx = x if side == "right" else x + bubble_w + 0.1
        p.img(pose, lx, y, lw, h, role="leo")
        bx = x + lw + 0.05 if side == "right" else x
        by = y + 0.05
        bh = 0.62
        p.rect(bx, by, bubble_w, bh, fill=WHITE, stroke=NAVY, sw=1.4, r=0.2)
        tx = bx + 0.06 if side == "right" else bx + bubble_w - 0.06
        p.poly([(tx, by + 0.38), (tx - 0.16 if side == "right" else tx + 0.16, by + 0.52), (tx, by + 0.5)], fill=WHITE, stroke=NAVY, sw=1.4)
        p.rect(tx - 0.02 if side == "right" else tx - 0.03, by + 0.39, 0.05, 0.1, fill=WHITE)
        p.text(text, bx + 0.08, by, bubble_w - 0.16, bh, "title", size, NAVY, align="center", valign="middle")

    def arrow(self, p, x, y, w=0.28, colour=NAVY):
        p.line(x, y, x + w - 0.1, y, stroke=colour, sw=3)
        p.poly([(x + w - 0.13, y - 0.1), (x + w, y), (x + w - 0.13, y + 0.1)], fill=colour, stroke=colour, sw=1)

    def dot(self, p, x, y):
        p.circle(x, y, 0.075, fill=WHITE, stroke=NAVY, sw=1.8, role="dot")

    def boxed_img(self, p, asset, x, y, w, h, fill=WHITE, stroke="#C9D3DB", label=None, lsize=11):
        p.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.2, r=0.14)
        ih = h - (0.3 if label else 0.12)
        p.img(asset, x + 0.08, y + 0.06, w - 0.16, ih - 0.04)
        if label:
            p.text(label, x, y + h - 0.3, w, 0.28, "xbold", lsize, NAVY, align="center", valign="middle")

    def group_grid(self, p, gid, asset, n, x, y, w, h, per_row=3, size=None):
        rows = math.ceil(n / per_row)
        size = size or min(w / per_row, h / rows) * 0.9
        k = 0
        for r in range(rows):
            cnt = min(per_row, n - k)
            cy = y + h * (r + 0.5) / rows
            for cx in centers(cnt, x + (w - w * cnt / per_row) / 2, x + (w + w * cnt / per_row) / 2):
                p.img(asset, cx - size / 2, cy - size / 2, size, size, group=gid)
                k += 1
        p.add_group(gid, n)

    # =============================================================== build all
    def build(self):
        self.cover()
        self.belongs()
        self.setup_guide()
        self.mission_map()
        for m in C.MISSIONS:
            getattr(self, f"m{two(m['n'])}")(m)
        for i in range(5):
            self.piece_sheet(i)
        self.reference()
        self.certificate()
        self.back_cover()
        self.pages.sort(key=lambda q: q.number)
        return self.pages

    # =============================================================== pages 1-4
    def cover(self):
        p = self.new(1, "cover")
        p.title = "Cover"
        W, H = self.W, self.H
        p.rect(0, 0, W, H, fill=SKY)
        p.img("cloud_plain", 0.3, 2.2, 1.9, 1.2)
        p.img("cloud_plain", W - 2.2, 3.4, 1.7, 1.08)
        p.img("hill", -0.4, H - 3.0, W * 0.75, 2.4, align="bottom")
        p.img("hill", W * 0.3, H - 2.6, W * 0.8, 2.2, align="bottom")
        p.rect(0, H - 1.0, W, 1.0, fill="#8CC63F")
        # brand pill
        bw = 3.3
        p.rect((W - bw) / 2, 0.5, bw, 0.42, fill=WHITE, stroke=NAVY, sw=1.6, r=0.21)
        p.text(C.PRODUCT["brand"], (W - bw) / 2, 0.5, bw, 0.42, "title", 14, NAVY, align="center", valign="middle")
        # title panel
        tw, ty = W - 1.3, 1.08
        p.rect((W - tw) / 2, ty, tw, 2.35, fill=WHITE, stroke=NAVY, sw=3, r=0.4)
        p.text("MY MAGIC", (W - tw) / 2, ty + 0.12, tw, 0.95, "title", 60, CORAL, align="center", valign="middle")
        p.text("BUSY BOOK", (W - tw) / 2, ty + 0.98, tw, 1.15, "title", 74, NAVY, align="center", valign="middle")
        # subtitle ribbon
        sw_ = W - 1.6
        p.rect((W - sw_) / 2, ty + 2.2, sw_, 0.5, fill=NAVY, r=0.25)
        p.text(C.PRODUCT["subtitle"], (W - sw_) / 2, ty + 2.2, sw_, 0.5, "xbold", 15.5, WHITE, align="center", valign="middle")
        # ages badge
        bx_, by_, br_ = W - 1.35, ty + 3.75, 0.78
        p.circle(bx_, by_, br_, fill=YELLOW, stroke=NAVY, sw=3)
        p.circle(bx_, by_, br_ - 0.1, fill=None, stroke=WHITE, sw=2, dash=(4, 4))
        p.text("AGES", bx_ - br_, by_ - 0.52, 2 * br_, 0.36, "title", 17, NAVY, align="center", valign="middle")
        p.text("3–5", bx_ - br_, by_ - 0.2, 2 * br_, 0.62, "title", 36, NAVY, align="center", valign="middle")
        # Leo + activity cards
        cy = ty + 3.1
        p.img("leo_cheer", W / 2 - 1.55, cy + 0.3, 3.1, 3.9)
        cards = [("card:fish", 0.55, cy + 0.6, -10), ("card:cow", 1.45, cy + 1.75, 8), ("card:apple", 0.5, cy + 3.0, 6),
                 ("card:banana", 1.55, cy + 4.05, -8), ("card:sunhat", W - 2.25, cy + 2.15, 10), ("card:rainboots", W - 1.55, cy + 3.25, -6)]
        for a, x, y, r in cards:
            p.img(a, x, y, 1.15, 1.15, rot=r)
        p.img("shape_star", W / 2 + 1.5, cy + 0.25, 0.75, 0.75, rot=12)
        p.img("shape_triangle", W / 2 - 2.3, cy + 0.35, 0.62, 0.62, rot=-10)
        p.img("shape_circle", W / 2 + 1.75, cy + 1.3, 0.5, 0.5)
        p.img("shape_square", W / 2 - 2.0, cy + 2.6, 0.48, 0.48, rot=14)
        # number train
        ty2 = H - 2.05
        p.img("train_engine", 0.9, ty2 - 0.05, 1.25, 1.14, align="bottom")
        for i in range(3):
            x = 2.15 + i * 1.1
            p.img("train_car", x, ty2 + 0.72, 1.05, 0.38, align="bottom")
            p.rect(x + 0.18, ty2 + 0.08, 0.7, 0.66, fill=WHITE, stroke=NAVY, sw=1.6, r=0.1)
            p.text(str(i + 1), x + 0.18, ty2 + 0.08, 0.7, 0.66, "title", 28, [CORAL, "#1F86B3", "#5E9A1E"][i], align="center", valign="middle")
        p.line(0.7, ty2 + 1.13, 5.6, ty2 + 1.13, stroke=NAVY, sw=3)
        p.img("cupcake", W - 2.4, ty2 + 0.05, 0.9, 0.9)
        p.img("scoop_strawberry", W - 1.45, ty2 - 0.1, 0.62, 0.62)
        p.img("cone", W - 1.45, ty2 + 0.4, 0.62, 0.66)
        p.text(C.PRODUCT["tagline"], 0.5, H - 0.72, W - 1.0, 0.36, "title", 14, NAVY, align="center", valign="middle")

    def belongs(self):
        p = self.new(2, "intro")
        p.title = "This Book Belongs To"
        W, H = self.W, self.H
        p.rect(M, M, W - 2 * M, H - 2 * M - 0.4, fill=CREAM, stroke=YELLOW, sw=3, r=0.4)
        for x, y, s in ((0.9, 0.9, 0.5), (W - 1.5, 1.1, 0.6), (1.2, 4.6, 0.4), (W - 1.4, 5.0, 0.45), (W - 1.9, 8.4, 0.5), (1.0, 8.7, 0.55)):
            p.img("sparkle", x, y, s, s)
        p.text("THIS BOOK", M, 1.0, W - 2 * M, 0.7, "title", 40, CORAL, align="center", valign="middle")
        p.text("BELONGS TO", M, 1.65, W - 2 * M, 0.7, "title", 40, NAVY, align="center", valign="middle")
        bw = W - 2.2
        p.rect((W - bw) / 2, 2.6, bw, 1.15, fill=WHITE, stroke=NAVY, sw=2.4, r=0.3)
        p.line((W - bw) / 2 + 0.4, 3.45, (W + bw) / 2 - 0.4, 3.45, stroke="#B5C2CC", sw=2, dash=(6, 5))
        p.text("my name", (W - bw) / 2, 3.5, bw, 0.22, "bold", 9, MUTED, align="center")
        p.img("leo_wave", W / 2 - 1.9, 4.1, 3.8, 4.75)
        bh = 1.25
        by = H - M - 0.4 - bh - 0.35
        p.rect(1.0, by, W - 2.0, bh, fill=WHITE, stroke=SKY, sw=2.5, r=0.3)
        p.text("Welcome, little explorer!\nAre you ready for 36 fun missions?", 1.1, by, W - 2.2, bh, "title", 21, NAVY,
               align="center", valign="middle")
        self.footer(p, None, None, YELLOW)

    def setup_guide(self):
        p = self.new(3, "intro")
        p.title = "Parent Setup Guide"
        W, H = self.W, self.H
        p.text("GROWN-UP SETUP GUIDE", M, M, W - 2 * M, 0.5, "title", 26, NAVY, valign="middle")
        p.text("About 30–45 minutes to prepare. You only need to do it once – the pieces can be reused again and again.",
               M, M + 0.5, W - 2 * M, 0.3, "body", 10.5, NAVY)
        steps = [
            ("icon_printer", "PRINT", "Print at Actual size / 100% on plain paper. Card stock (160–220 gsm) lasts longer."),
            ("icon_scissors", "CUT", "An adult cuts out the cards on pages 41–45 along the solid lines. Round off sharp corners."),
            ("icon_laminate", "LAMINATE (optional)", "Laminate boards and cards, then trim leaving a small sealed edge around each card."),
            ("icon_fastener", "FASTEN (optional)", "Add reusable adhesive or hook-and-loop dots: one on each card back, one on each dotted-circle spot on the boards."),
            ("icon_play", "PLAY TOGETHER", "Read the mission aloud, show the cards and let your child try. Helping is part of the fun!"),
            ("icon_storage", "STORE SAFELY", "After play, collect every piece into a labelled envelope or zip bag and store out of reach."),
        ]
        cw = (W - 2 * M - 0.2) / 2
        chh = 1.08
        for i, (icon, head, body) in enumerate(steps):
            x = M + (i % 2) * (cw + 0.2)
            y = 1.38 + (i // 2) * (chh + 0.14)
            p.rect(x, y, cw, chh, fill=CREAM, stroke="#E9DDB6", sw=1.2, r=0.18)
            p.circle(x + 0.32, y + 0.32, 0.22, fill=CORAL, stroke=NAVY, sw=1.2)
            p.text(str(i + 1), x + 0.1, y + 0.1, 0.44, 0.44, "title", 15, WHITE, align="center", valign="middle")
            p.img(icon, x + 0.12, y + 0.56, 0.42, 0.42)
            p.text(head, x + 0.66, y + 0.1, cw - 0.75, 0.3, "title", 13, NAVY, valign="middle")
            p.text(body, x + 0.66, y + 0.42, cw - 0.75, 0.62, "body", 9.5, NAVY)
        # diagram
        dy = 1.38 + 3 * (chh + 0.14) + 0.05
        p.text("HOW THE PIECES WORK", M, dy, W - 2 * M, 0.32, "title", 15, NAVY, valign="middle")
        dy += 0.4
        bx = M + 0.1
        # sample piece card
        self.piece_card(p, bx + 1.25, dy + 0.15, "RD1", record=False)
        notes = [(dy + 0.25, "Cut along the solid line", bx + 1.25),
                 (dy + 1.4, "Piece ID + page it belongs to", bx + 1.4)]
        for yy, s, tx in notes:
            p.text(s, bx - 0.1, yy - 0.15, 1.25, 0.42, "bold", 8.5, NAVY, align="right", valign="middle")
            p.line(bx + 1.17, yy + 0.06, tx + 0.08, yy + 0.06, stroke=CORAL, sw=1.4)
        p.img("icon_scissors", bx, dy + 1.83, 0.26, 0.26)
        p.text("Solid line = cut line", bx + 0.32, dy + 1.85, 2.6, 0.24, "xbold", 9, NAVY)
        # sample slot
        sx = M + 4.0
        p.rect(sx, dy + 0.1, SLOT, SLOT, fill=WHITE, stroke=HINT, sw=1.7, r=0.14, dash=(5, 3.5))
        p.img("drophint_red", sx + 0.21, dy + 0.31, 1.22, 1.22)
        p.img("fastener_dot", sx + SLOT - 0.27, dy + 0.17, 0.2, 0.2)
        p.text("Dashed box = place a card here", sx + SLOT + 0.12, dy + 0.35, W - M - sx - SLOT - 0.15, 0.5, "bold", 8.5, NAVY)
        p.img("fastener_dot", sx + SLOT + 0.12, dy + 0.93, 0.24, 0.24)
        p.text("= optional fastener spot", sx + SLOT + 0.42, dy + 0.9, W - M - sx - SLOT - 0.45, 0.5, "bold", 8.5, NAVY)
        p.text("No folds or glue are needed anywhere in this book.", sx, dy + 1.85, W - M - sx, 0.24, "xbold", 9, NAVY)
        # safety
        sy = dy + 2.25
        sh = H - M - 0.42 - sy
        p.rect(M, sy, W - 2 * M, sh, fill="#FFF6D6", stroke=CORAL, sw=2.2, r=0.2)
        p.img("icon_warning", M + 0.15, sy + 0.15, 0.6, 0.6)
        p.text("SAFETY FIRST – ADULT SUPERVISION REQUIRED", M + 0.9, sy + 0.12, W - 2 * M - 1.0, 0.32, "title", 13, CORAL, valign="middle")
        safety = ("WARNING: Contains detachable paper pieces. Not suitable for children under 3 years. "
                  "An adult must print, cut and prepare all pieces, and supervise play at all times. "
                  "Paper can tear into small bits: check pieces before each use and throw away any torn, wet or chewed pieces. "
                  "Keep pieces away from children who put objects in their mouths. Use only flat fasteners (reusable adhesive or "
                  "hook-and-loop dots) – never pins, staples, magnets, beads or cords. Store pieces out of reach after play. "
                  "This is a printable learning activity, not a certified toy.")
        p.text(safety, M + 0.9, sy + 0.46, W - 2 * M - 1.05, sh - 0.52, "body", 10.5, NAVY, leading=1.28)
        self.footer(p, None, None, CORAL)

    def mission_map(self):
        p = self.new(4, "intro")
        p.title = "My Little Mission Map"
        W, H = self.W, self.H
        p.text("MY LITTLE MISSION MAP", M, M, W - 2 * M, 0.55, "title", 30, NAVY, align="center", valign="middle")
        p.text("Finish a world, then colour its star!", M, M + 0.55, W - 2 * M, 0.32, "bold", 14, NAVY, align="center", valign="middle")
        top, bot = 1.55, H - M - 0.55
        rows = centers(3, top, bot)
        cols = [M + (W - 2 * M) * 0.27, M + (W - 2 * M) * 0.73]
        pts = []
        for i, ch in enumerate(C.CHAPTERS):
            r, c = i // 2, (i % 2 if (i // 2) % 2 == 0 else 1 - i % 2)
            pts.append((cols[c], rows[r]))
        path = [pts[0]] + [q for q in pts[1:]]
        p.poly(path, fill=None, stroke="#E9DDB6", sw=26, closed=False)
        p.poly(path, fill=None, stroke=WHITE, sw=4, closed=False, dash=(10, 8))
        rr = min(1.05, (bot - top) / 6 - 0.1)
        for i, (ch, (x, y)) in enumerate(zip(C.CHAPTERS, pts)):
            p.circle(x, y - 0.25, rr, fill=ch["tint"], stroke=ch["colour"], sw=4)
            p.img(ch["world"], x - rr * 0.72, y - 0.25 - rr * 0.72, rr * 1.44, rr * 1.44)
            p.rect(x - 1.45, y + rr - 0.3, 2.9, 0.42, fill=ch["deep"], r=0.21)
            p.text(f"{ch['num']}  {ch['name'].upper()}", x - 1.45, y + rr - 0.3, 2.9, 0.42, "title", 14, WHITE, align="center", valign="middle")
            a, b = ch["pages"]
            p.text(f"Missions {(a - 4):02d}–{(b - 4):02d}  ·  pages {a}–{b}", x - 1.45, y + rr + 0.13, 2.9, 0.24, "bold", 9, NAVY, align="center", valign="middle")
            sx = x + rr * 0.55 if i % 2 == 0 else x - rr * 0.55 - 0.72
            p.img("reward_star_blank", sx, y - 0.25 - rr - 0.05, 0.72, 0.72)
        p.img("leo_side", M, M - 0.05, 0.85, 1.06)
        p.img("leo_head_happy", W - M - 0.95, M, 0.95, 0.85)
        self.footer(p, "Six worlds  ·  36 missions  ·  one big adventure!", "sparkle", LIME)

    # =============================================================== Colour Kingdom
    def m01(self, m):
        p, ch = self.mission_frame(m)
        cols = centers(3, p.X0, p.X1)
        avail = p.CH - 1.35
        rows = [p.Y0 + avail * (i + 0.5) / 2 for i in range(2)]
        order = ["red", "orange", "yellow", "green", "blue", "purple"]
        cell_h = 3.35
        for i, col in enumerate(order):
            cx, cyc = cols[i % 3], rows[i // 3]
            top = cyc - cell_h / 2
            p.img(f"cloud_{col}", cx - 1.05, top, 2.1, 1.25)
            p.text(col, cx - 1.0, top + 1.25, 2.0, 0.34, "title", 16, NAVY, align="center", valign="middle")
            self.slot(p, cx, top + 1.62 + SLOT / 2, f"RD{i + 1}", f"{col} cloud", hint=f"drophint_{col}")
        by = p.Y1 - 1.25
        p.img("rainbow", p.X0 + p.CW / 2 - 1.2, by + 0.05, 2.4, 1.15, align="bottom")
        self.leo_say(p, "leo_wave", p.X0, by - 0.05, 1.3, "Can you help me?", 1.9)
        p.text("Look for the matching symbol too!", p.X1 - 2.3, by + 0.3, 2.3, 0.6, "bold", 11, MUTED, align="right")

    def m02(self, m):
        p, ch = self.mission_frame(m)
        names = ["circle", "square", "triangle", "rectangle", "star"]
        board_h = p.CH - 1.55
        p.rect(p.X0, p.Y0, p.CW, board_h, fill=ch["tint"], r=0.3)
        rows = centers(2, p.Y0, p.Y0 + board_h)
        pos = [(c, rows[0]) for c in centers(3, p.X0, p.X1)] + [(c, rows[1]) for c in centers(2, p.X0 + 0.8, p.X1 - 0.8)]
        order = [2, 0, 4, 1, 3]   # shuffled board order
        for (cx, cy), k in zip(pos, order):
            nm = names[k]
            self.slot(p, cx, cy - 0.15, f"SH{k + 1}", f"{nm} outline", hint=f"shapesil_{nm}", hint_scale=0.8)
            p.text(nm, cx - 1.0, cy - 0.15 + SLOT / 2 + 0.05, 2.0, 0.34, "title", 15, NAVY, align="center", valign="middle")
        self.leo_say(p, "leo_point", p.X0 + 0.1, p.Y1 - 1.4, 1.4, "Let's find it!", 1.8)
        p.img("magnifier", p.X1 - 1.4, p.Y1 - 1.35, 1.2, 1.2)
        p.text("Count the corners!", p.X1 - 3.6, p.Y1 - 0.95, 2.1, 0.4, "bold", 11, MUTED, align="right", valign="middle")

    def m03(self, m):
        p, ch = self.mission_frame(m)
        # awning
        n = 12
        sw_ = p.CW / n
        for i in range(n):
            p.rect(p.X0 + i * sw_, p.Y0, sw_, 0.34, fill=PINK if i % 2 == 0 else WHITE, stroke=None)
        p.rect(p.X0, p.Y0, p.CW, 0.34, fill=None, stroke=NAVY, sw=1.5, r=0.06)
        orders = [("IC1", "IC2", "strawberry", "chocolate"), ("IC3", "IC4", "mint", "lemon"), ("IC5", "IC6", "blueberry", "orange")]
        cols = centers(3, p.X0, p.X1)
        top = p.Y0 + 0.5
        for i, ((b, t, fb, ft), cx) in enumerate(zip(orders, cols)):
            # ticket
            tw, th = 1.85, 1.45
            p.rect(cx - tw / 2, top, tw, th, fill=WHITE, stroke=NAVY, sw=1.4, r=0.12)
            p.text(f"ORDER {i + 1}", cx - tw / 2, top + 0.04, tw, 0.28, "title", 12, ch["deep"], align="center", valign="middle")
            p.img(f"scoop_{ft}", cx - 0.32, top + 0.3, 0.64, 0.5)
            p.img(f"scoop_{fb}", cx - 0.32, top + 0.62, 0.64, 0.5)
            p.img("cone", cx - 0.25, top + 0.98, 0.5, 0.42, align="top")
            sy = top + th + 0.25
            self.slot(p, cx, sy + SLOT / 2, t, f"order {i + 1} top scoop ({ft})", hint="hint:" + f"scoop_{ft}", hint_scale=0.0)
            self.slot(p, cx, sy + SLOT * 1.5 + 0.04, b, f"order {i + 1} bottom scoop ({fb})", hint=None)
            p.text("2", cx - SLOT / 2 + 0.08, sy + 0.05, 0.3, 0.3, "title", 12, HINT)
            p.text("1", cx - SLOT / 2 + 0.08, sy + SLOT + 0.09, 0.3, 0.3, "title", 12, HINT)
            p.img("cone", cx - 0.75, sy + 2 * SLOT + 0.08, 1.5, 1.45, align="top")
        p.text("Then invent your own ice cream!", p.X0, p.Y1 - 0.42, p.CW, 0.38, "title", 15, ch["deep"], align="center", valign="middle")

    def m04(self, m):
        p, ch = self.mission_frame(m)
        fx = centers(6, p.X0, p.X1)
        fy = p.Y0 + 0.1
        for i, (x, col) in enumerate(zip(fx, C.FLOWERS)):
            p.img(f"flower_{col}", x - 0.6, fy, 1.2, 1.55)
            self.dot(p, x, fy + 1.75)
        px = centers(3, p.X0, p.X1)
        py = p.Y1 - 2.35
        p.rect(p.X0, p.Y1 - 0.45, p.CW, 0.4, fill="#C9E89A", r=0.12)
        for x, col in zip(px, C.POTS):
            self.dot(p, x, py - 0.2)
            p.img(f"pot_{col}", x - 0.95, py, 1.9, 1.9)
            p.text(col, x - 0.9, p.Y1 - 0.45, 1.8, 0.4, "title", 15, NAVY, align="center", valign="middle")
        for i, col in enumerate(C.FLOWERS):
            p.answers.append((f"flower {i + 1} ({col})", f"{col} pot"))
        p.text("Draw a line, then say the colour!", p.X0, (fy + 1.9 + py - 0.3) / 2 - 0.2, p.CW, 0.4, "bold", 12, HINT, align="center", valign="middle")

    def m05(self, m):
        p, ch = self.mission_frame(m)
        n = len(C.PATTERNS)
        rh = min(1.25, (p.CH - 0.1) / n - 0.1)
        ys = centers(n, p.Y0, p.Y1)
        tok = min(0.62, rh * 0.62)
        for i, ((seq, ans, choices), cy) in enumerate(zip(C.PATTERNS, ys)):
            p.rect(p.X0, cy - rh / 2, p.CW, rh, fill=ch["tint"], r=0.18)
            x = p.X0 + 0.15
            for col in seq:
                p.img(f"token_{col}", x, cy - tok / 2, tok, tok)
                x += tok + 0.07
            p.rect(x + 0.02, cy - 0.4, 0.8, 0.8, fill=WHITE, stroke=HINT, sw=1.6, r=0.12, dash=(4, 3))
            p.text("?", x + 0.02, cy - 0.4, 0.8, 0.8, "title", 26, HINT, align="center", valign="middle")
            x += 1.0
            p.line(x, cy - rh / 2 + 0.12, x, cy + rh / 2 - 0.12, stroke=WHITE, sw=3)
            cxs = centers(3, x + 0.1, p.X1 - 0.1)
            for cx, col in zip(cxs, choices):
                p.circle(cx, cy, tok * 0.62, fill=WHITE, stroke=None)
                p.img(f"token_{col}", cx - tok * 0.45, cy - tok * 0.45, tok * 0.9, tok * 0.9)
            p.answers.append((f"pattern {i + 1}: " + ", ".join(seq), ans))

    def m06(self, m):
        p, ch = self.mission_frame(m)
        parts = [("RB1", "robot_antenna", "antenna"), ("RB2", "robot_head", "head"), ("RB3", "robot_body", "body"), ("RB4", "robot_wheels", "wheels")]
        cx = p.X0 + p.CW * 0.42
        total = 4 * SLOT
        top = p.Y0 + (p.CH - total) / 2
        for i, (pid, a, lab) in enumerate(parts):
            cy = top + SLOT * i + SLOT / 2
            self.slot(p, cx, cy, pid, f"robot {lab}", hint="hint:" + a, hint_scale=0.82)
            p.rect(p.X0, cy - 0.2, 1.45, 0.4, fill=ch["tint"], stroke=ch["colour"], sw=1.2, r=0.2)
            p.text(f"{i + 1}  {lab}", p.X0, cy - 0.2, 1.45, 0.4, "title", 13, NAVY, align="center", valign="middle")
            p.line(p.X0 + 1.5, cy, cx - SLOT / 2 - 0.08, cy, stroke=HINT, sw=1.2, dash=(2, 3))
        rx = cx + SLOT / 2 + 0.3
        self.leo_say(p, "leo_cheer", rx, p.Y0 + 0.4, 1.9, "Beep boop!", p.X1 - rx - 1.6)
        bw = p.X1 - rx
        p.rect(rx, p.Y1 - 2.4, bw, 2.1, fill=CREAM, stroke=YELLOW, sw=1.6, r=0.2)
        p.text("SILLY ROBOT TIME!", rx + 0.15, p.Y1 - 2.3, bw - 0.3, 0.36, "title", 13, CORAL, valign="middle")
        p.text("Now mix it up! Put the wheels on top or the head at the bottom. What does your robot do?",
               rx + 0.15, p.Y1 - 1.9, bw - 0.3, 1.5, "bold", 11, NAVY)

    # =============================================================== Animal Island
    def m07(self, m):
        p, ch = self.mission_frame(m)
        habs = [("hab_ocean", "OCEAN", "AN1", "fish"), ("hab_farm", "FARM FIELD", "AN2", "cow"), ("hab_rainforest", "RAINFOREST", "AN3", "monkey"),
                ("hab_ice", "ICY LAND", "AN4", "penguin"), ("hab_desert", "DESERT", "AN5", "camel"), ("hab_pond", "POND", "AN6", "frog")]
        order = [0, 3, 2, 5, 4, 1]
        pw = (p.CW - 0.25) / 2
        ph = min((p.CH - 0.3) / 3, pw / 1.5)
        ys = centers(3, p.Y0, p.Y1)
        for k, idx in enumerate(order):
            a, lab, pid, an = habs[idx]
            x = p.X0 + (k % 2) * (pw + 0.25)
            y = ys[k // 2] - ph / 2
            p.img(a, x, y, pw, ph)
            p.rect(x, y, pw, ph, fill=None, stroke=NAVY, sw=1.8, r=0.12)
            tw = text_width(lab, "title", 11) + 0.3
            p.rect(x + 0.1, y + 0.1, tw, 0.32, fill=WHITE, stroke=NAVY, sw=1.2, r=0.16)
            p.text(lab, x + 0.1, y + 0.1, tw, 0.32, "title", 11, NAVY, align="center", valign="middle")
            self.slot(p, x + pw - SLOT / 2 - 0.12, y + ph / 2, pid, f"{lab.lower()} ({an})", hint=None)

    def m08(self, m):
        p, ch = self.mission_frame(m)
        n = len(C.FOODS)
        ys = centers(n, p.Y0, p.Y1)
        bh = min(1.18, p.CH / n - 0.12)
        for i, y in enumerate(ys):
            a, name, _, _ = C.FOODS[i]
            p.rect(p.X0, y - bh / 2, 2.55, bh, fill=ch["tint"], r=0.16)
            p.img(a, p.X0 + 0.08, y - bh / 2 + 0.05, bh - 0.1, bh - 0.1)
            p.text(name, p.X0 + bh + 0.05, y - 0.2, 2.55 - bh - 0.1, 0.4, "title", 15, NAVY, valign="middle")
            self.dot(p, p.X0 + 2.72, y)
            fa, _, food, flab = C.FOODS[C.FOOD_ORDER[i]]
            fx = p.X1 - 2.45
            p.rect(fx, y - bh / 2, 2.45, bh, fill=CREAM, r=0.16)
            p.img(food, p.X1 - bh - 0.03, y - bh / 2 + 0.05, bh - 0.1, bh - 0.1)
            p.text(flab, fx + 0.25, y - 0.2, 2.45 - bh - 0.3, 0.4, "title", 15, NAVY, valign="middle")
            self.dot(p, fx - 0.17, y)
        for a, name, food, flab in C.FOODS:
            p.answers.append((name, flab))

    def m09(self, m):
        p, ch = self.mission_frame(m)
        board_h = p.CH - 1.55
        p.rect(p.X0, p.Y0, p.CW, board_h, fill="#F1F4F6", r=0.3)
        order = [("AN5", "camel"), ("AN1", "fish"), ("AN6", "frog"), ("AN2", "cow"), ("AN4", "penguin"), ("AN3", "monkey")]
        cols = centers(3, p.X0, p.X1)
        rows = centers(2, p.Y0, p.Y0 + board_h)
        for k, (pid, an) in enumerate(order):
            self.slot(p, cols[k % 3], rows[k // 2 if False else k // 3], pid, f"{an} shadow", hint="sil:" + an, hint_scale=0.82)
        self.leo_say(p, "leo_surprised", p.X0 + 0.1, p.Y1 - 1.4, 1.4, "Who's hiding?", 1.9)
        p.text("Look at the ears, tails and feet!", p.X1 - 3.4, p.Y1 - 0.95, 3.4, 0.4, "bold", 11.5, MUTED, align="right", valign="middle")

    def m10(self, m):
        p, ch = self.mission_frame(m)
        rows = [("rabbit_noears", "AP1", "rabbit", "ears"), ("fox_notail", "AP2", "fox", "tail"), ("elephant_notrunk", "AP3", "elephant", "trunk")]
        ys = centers(3, p.Y0, p.Y1)
        rh = min(2.45, p.CH / 3 - 0.15)
        for (a, pid, an, part), y in zip(rows, ys):
            p.rect(p.X0, y - rh / 2, p.CW, rh, fill=ch["tint"], r=0.25)
            p.img(a, p.X0 + 0.2, y - rh / 2 + 0.08, rh - 0.16, rh - 0.16)
            p.text(f"The {an} is missing its...", p.X0 + rh + 0.2, y - 0.55, 2.4, 0.5, "title", 15, NAVY, valign="middle")
            p.text("?", p.X0 + rh + 0.2, y - 0.05, 2.4, 0.6, "title", 30, ch["deep"], valign="middle")
            p.img("icon_match", p.X1 - SLOT - 1.0, y - 0.32, 0.64, 0.64)
            self.slot(p, p.X1 - SLOT / 2 - 0.2, y, pid, f"{an}'s missing {part}", hint=None)
            p.answers.append((an, part))

    def m11(self, m):
        p, ch = self.mission_frame(m)
        sw_, sh_ = p.CW, p.CW * 300 / 420
        sy = p.Y0
        p.img("farm_scene", p.X0, sy, sw_, sh_)
        p.rect(p.X0, sy, sw_, sh_, fill=None, stroke=NAVY, sw=1.8, r=0.12)
        k = sw_ / 420
        spots = [("FM1", "hen", "hen house", 82, 116), ("FM2", "pig", "mud puddle", 322, 162), ("FM3", "duck", "pond", 236, 236)]
        for pid, an, place, ux, uy in spots:
            self.slot(p, p.X0 + ux * k, sy + uy * k, pid, f"{place} ({an})", hint="hint:" + an, hint_scale=0.78)
        by = sy + sh_ + 0.25
        bh = p.Y1 - by
        sounds = [("hen", "Cluck, cluck!"), ("pig", "Oink, oink!"), ("duck", "Quack, quack!")]
        for cx, (a, s) in zip(centers(3, p.X0, p.X1), sounds):
            w = p.CW / 3 - 0.2
            p.rect(cx - w / 2, by, w, min(bh, 1.5), fill=CREAM, stroke=YELLOW, sw=1.4, r=0.2)
            ih = min(bh, 1.5) - 0.2
            p.img(a, cx - w / 2 + 0.1, by + 0.1, ih, ih)
            p.text(s, cx - w / 2 + ih + 0.12, by, w - ih - 0.2, min(bh, 1.5), "title", 13, NAVY, valign="middle")

    def m12(self, m):
        p, ch = self.mission_frame(m)
        sw_, sh_ = p.CW, p.CW * 330 / 420
        sy = p.Y0
        p.img("ocean_scene", p.X0, sy, sw_, sh_)
        p.rect(p.X0, sy, sw_, sh_, fill=None, stroke=NAVY, sw=1.8, r=0.12)
        k = sw_ / 420
        spots = [("OC1", "octopus", "by the rocks", 330, 190), ("OC2", "turtle", "swimming in the sea", 200, 116), ("OC3", "crab", "on the sand", 108, 272)]
        for pid, an, place, ux, uy in spots:
            self.slot(p, p.X0 + ux * k, sy + uy * k, pid, f"{an} ({place})", hint="hint:" + an, hint_scale=0.8)
        by = sy + sh_ + 0.2
        p.rect(p.X0, by, p.CW, min(1.25, p.Y1 - by), fill=CREAM, stroke=SKY, sw=1.4, r=0.2)
        p.img("magnifier", p.X0 + 0.15, by + 0.12, 0.9, 0.9)
        p.text("I spy a little fish and a starfish. Can you find them? Where is the turtle swimming to?",
               p.X0 + 1.2, by + 0.05, p.CW - 1.35, min(1.25, p.Y1 - by) - 0.1, "bold", 12.5, NAVY, valign="middle")

    # =============================================================== Number Town
    def m13(self, m):
        p, ch = self.mission_frame(m)
        pitch = SLOT + 0.13
        rows = [[None, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10]]
        rh = 2.35
        ys = centers(3, p.Y0, p.Y1)
        for r, (row, cy) in enumerate(zip(rows, ys)):
            top = cy - rh / 2
            x = p.X0 + (p.CW - 4 * pitch) / 2
            for j, num in enumerate(row):
                cx = x + j * pitch + pitch / 2
                if num is None:
                    p.img("train_engine", cx - 0.95, top + 0.35, 1.9, 1.75, align="bottom")
                    continue
                p.img("train_car", cx - pitch / 2 + 0.02, top + SLOT + 0.02, pitch - 0.04, 0.6, align="top")
                self.slot(p, cx, top + SLOT / 2 + 0.05, f"NU{num}", f"train carriage {num}", hint=None)
                p.text(str(num), cx - 0.3, top + SLOT + 0.06, 0.6, 0.22, "title", 9, NAVY, align="center", valign="middle")
            p.line(p.X0 + 0.1, top + SLOT + 0.68, p.X1 - 0.1, top + SLOT + 0.68, stroke=DGREY, sw=2.5)
            p.line(p.X0 + 0.1, top + SLOT + 0.78, p.X1 - 0.1, top + SLOT + 0.78, stroke=DGREY, sw=2.5)
        cx = p.X0 + (p.CW - 4 * pitch) / 2 + 3 * pitch + pitch / 2
        self.leo_say(p, "leo_happy", cx - pitch / 2 + 0.05, ys[2] - rh / 2 - 0.05, 1.45, "All aboard!", pitch - 1.0, size=10.5)

    def m14(self, m):
        p, ch = self.mission_frame(m)
        cols = centers(3, p.X0, p.X1)
        rows = centers(2, p.Y0, p.Y1)
        cell_h = 3.85
        for i, n in enumerate(C.BALLOON_COUNTS):
            cx, cy = cols[i % 3], rows[i // 3]
            top = cy - cell_h / 2
            w = p.CW / 3 - 0.15
            p.rect(cx - w / 2, top, w, 2.05, fill=ch["tint"], r=0.2)
            per = 3
            size = min(0.68, (w - 0.2) / per)
            rows_n = math.ceil(n / per)
            k = 0
            for r in range(rows_n):
                cnt = min(per, n - k)
                yy = top + 0.12 + r * (size + 0.05) + (2.05 - 0.24 - rows_n * (size + 0.05)) / 2
                for xx in centers(cnt, cx - size * cnt / 2, cx + size * cnt / 2):
                    p.img(f"balloon_{(i * 3 + k) % 10}", xx - size / 2, yy, size, size, group=f"balloons_{i + 1}")
                    k += 1
            p.add_group(f"balloons_{i + 1}", n)
            self.slot(p, cx, top + 2.05 + 0.15 + SLOT / 2, f"NU{n}", f"bunch {i + 1} ({n} balloons)", hint=None)

    def m15(self, m):
        p, ch = self.mission_frame(m)
        mw = min(3.4, p.CW * 0.48)
        p.img("monster", p.X0, p.Y0 + 0.05, mw, mw * 220 / 260)
        ox = p.X0 + mw + 0.2
        p.text("The monster says:", ox, p.Y0, p.X1 - ox, 0.36, "title", 14, NAVY, valign="middle")
        ow = (p.X1 - ox - 0.2) / 3
        for j, n in enumerate(C.MONSTER_ORDERS):
            x = ox + j * (ow + 0.1)
            y = p.Y0 + 0.45
            p.rect(x, y, ow, 2.1, fill=WHITE, stroke=ch["colour"], sw=2, r=0.18)
            p.text(f"Feed me", x, y + 0.08, ow, 0.3, "title", 11, NAVY, align="center", valign="middle")
            p.text(str(n), x, y + 0.36, ow, 0.8, "title", 44, ch["deep"], align="center", valign="middle")
            dots = n
            dx = centers(min(dots, 3), x + 0.15, x + ow - 0.15)
            for d in range(dots):
                rr_ = d // 3
                xs = centers(min(3, dots - rr_ * 3), x + 0.15, x + ow - 0.15)
                p.circle(xs[d % 3], y + 1.38 + rr_ * 0.34, 0.12, fill=CORAL, stroke=NAVY, sw=1, group=f"order_{n}")
            p.add_group(f"order_{n}", n)
        py = p.Y0 + mw * 220 / 260 + 0.25
        ph = p.Y1 - py - 0.35
        p.img("plate", p.X0, py, p.CW, ph)
        p.text("Put the cookies on the plate. Count them. Yum!", p.X0, p.Y1 - 0.35, p.CW, 0.33, "title", 13, ch["deep"], align="center", valign="middle")
        top_row = centers(3, p.X0 + 0.6, p.X1 - 0.6)
        bottom_row = centers(2, p.X0 + 1.5, p.X1 - 1.5)
        cy = py + ph / 2
        allc = [f"TR{i}" for i in range(1, 6)]
        for x in top_row:
            self.slot(p, x, cy - SLOT / 2 - 0.04, allc, "plate (any cookie)", hint="hint:cookie", hint_scale=0.6)
        for x in bottom_row:
            self.slot(p, x, cy + SLOT / 2 + 0.04, allc, "plate (any cookie)", hint="hint:cookie", hint_scale=0.6)

    def m16(self, m):
        p, ch = self.mission_frame(m)
        n = len(C.CUPCAKE_COUNTS)
        ys = centers(n, p.Y0, p.Y1)
        cs = 0.56
        tw = 5 * cs + 0.5
        for i, (cnt, y) in enumerate(zip(C.CUPCAKE_COUNTS, ys)):
            tx = p.X0 + 0.1
            p.rect(tx, y - 0.78, tw, 1.56, fill=CREAM, stroke="#C98A4B", sw=2.4, r=0.16)
            for k in range(cnt):
                r, c = k // 5, k % 5
                p.img("cupcake", tx + 0.25 + c * cs, y - 0.7 + r * 0.72, cs, cs * 1.25, group=f"tray_{i + 1}")
            p.add_group(f"tray_{i + 1}", cnt)
            p.text("=", tx + tw + 0.1, y - 0.4, 0.6, 0.8, "title", 36, ch["deep"], align="center", valign="middle")
            self.slot(p, p.X1 - SLOT / 2 - 0.4, y, f"NU{cnt}", f"tray {i + 1} ({cnt} cupcakes)", hint=None)

    def m17(self, m):
        p, ch = self.mission_frame(m)
        n = len(C.MORE_LESS)
        ys = centers(n, p.Y0, p.Y1)
        bh = min(1.75, p.CH / n - 0.18)
        bw = (p.CW - 0.75) / 2
        for i, ((a, l, r), y) in enumerate(zip(C.MORE_LESS, ys)):
            for side, cnt in ((0, l), (1, r)):
                x = p.X0 + side * (bw + 0.75)
                p.rect(x, y - bh / 2, bw, bh, fill=WHITE, stroke=ch["colour"], sw=2.2, r=0.2)
                self.group_grid(p, f"row{i + 1}_{'LR'[side]}", a, cnt, x + 0.1, y - bh / 2 + 0.08, bw - 0.2, bh - 0.16, per_row=3, size=min(0.62, (bh - 0.2) / 2))
            p.text("or", p.X0 + bw, y - 0.3, 0.75, 0.6, "title", 18, ch["deep"], align="center", valign="middle")
            p.answers.append((f"row {i + 1} ({a}: {l} vs {r})", "left" if l > r else "right"))

    def m18(self, m):
        p, ch = self.mission_frame(m)
        sh = 1.6
        base_y = p.Y1 - 0.05
        cxs = [p.X0 + p.CW * 0.32, p.X0 + p.CW * 0.68]
        p.rect(p.X0, base_y, p.CW, 0.12, fill=DGREY, r=0.05)
        for t, cx in enumerate(cxs):
            for k in range(5):
                num = t * 5 + k + 1
                cy = base_y - sh * k - sh / 2
                self.slot(p, cx, cy, f"NU{num}", f"tower {t + 1}, level {k + 1}", hint=None, h=sh, dot=True)
                if t == 0:
                    xs = centers(min(num, 3), cx - 0.5, cx + 0.5)
                    for d in range(num):
                        row_ = d // 3
                        xs = centers(min(3, num - row_ * 3), cx - 0.45, cx + 0.45)
                        p.circle(xs[d % 3], cy - 0.25 + row_ * 0.3, 0.09, fill=LGREY, stroke=HINT, sw=1, group=f"helper_{num}")
                    p.add_group(f"helper_{num}", num)
        lw = cxs[0] - SLOT / 2 - p.X0 - 0.12
        p.text("EASIER\ntower\n1 to 5", p.X0, base_y - 4.8, lw, 1.3, "title", 15, ch["deep"], align="center", valign="middle")
        p.text("Start with 1 at the bottom!", p.X0, base_y - 3.1, lw, 1.1, "bold", 10.5, NAVY, align="center", valign="middle")
        p.text("CHALLENGE\ntower\n6 to 10", cxs[1] + SLOT / 2 + 0.1, base_y - 4.8, p.X1 - cxs[1] - SLOT / 2 - 0.1, 1.3, "title", 15, CORAL, align="center", valign="middle")

    # =============================================================== Feelings Forest
    def m19(self, m):
        p, ch = self.mission_frame(m)
        self.leo_say(p, "leo_think", p.X0 + p.CW / 2 - 1.95, p.Y0, 1.95, "What should I wear?", 2.3)
        cols = centers(3, p.X0, p.X1)
        top = p.Y0 + 2.25
        panels = [("weather_sunny", "SUNNY", "WE1", "sun hat"), ("weather_rainy", "RAINY", "WE2", "rain boots"), ("weather_cold", "COLD", "WE3", "warm scarf")]
        pw = p.CW / 3 - 0.2
        for cx, (a, lab, pid, item) in zip(cols, panels):
            ph = pw * 170 / 220
            p.img(a, cx - pw / 2, top, pw, ph)
            p.rect(cx - pw / 2, top, pw, ph, fill=None, stroke=NAVY, sw=1.6, r=0.16)
            p.text(lab, cx - pw / 2, top + ph + 0.05, pw, 0.4, "title", 17, NAVY, align="center", valign="middle")
            self.slot(p, cx, top + ph + 0.6 + SLOT / 2, pid, f"{lab.lower()} weather ({item})", hint=None)
        p.text("What is the weather like today?", p.X0, p.Y1 - 0.45, p.CW, 0.4, "title", 14, ch["deep"], align="center", valign="middle")

    def m20(self, m):
        p, ch = self.mission_frame(m)
        fw = min(p.CW - 0.4, p.CH - 1.7, 5.6)
        fx = p.X0 + (p.CW - fw) / 2
        fy = p.Y0
        p.img("face_blank", fx, fy, fw, fw)
        k = fw / 300
        self.slot(p, fx + 150 * k, fy + 116 * k, ["FA1", "FA2"], "eyes (any eye card)", hint=None, fill=WHITE)
        self.slot(p, fx + 150 * k, fy + 228 * k, ["FA3", "FA4", "FA5"], "mouth (any mouth card)", hint=None, fill=WHITE)
        p.text("eyes", fx + 150 * k + SLOT / 2 + 0.1, fy + 116 * k - 0.18, 1.0, 0.36, "title", 13, NAVY, valign="middle")
        p.text("mouth", fx + 150 * k + SLOT / 2 + 0.1, fy + 228 * k - 0.18, 1.0, 0.36, "title", 13, NAVY, valign="middle")
        iy = fy + fw + 0.12
        ih = p.Y1 - iy
        p.rect(p.X0, iy, p.CW, ih, fill=ch["tint"], r=0.2)
        p.text("Ideas to try:", p.X0 + 0.15, iy, 1.5, ih, "title", 13, NAVY, valign="middle")
        for cx, (a, lab) in zip(centers(3, p.X0 + 1.6, p.X1), [("face_happy", "happy"), ("face_surprised", "surprised"), ("face_sleepy", "sleepy")]):
            s = min(ih - 0.15, 1.0)
            p.img(a, cx - s - 0.05, iy + (ih - s) / 2, s, s)
            p.text(lab, cx + 0.02, iy, min(1.1, p.X1 - cx - 0.06), ih, "title", 12.5, NAVY, valign="middle")

    def m21(self, m):
        p, ch = self.mission_frame(m)
        n = len(C.FEELINGS)
        ys = centers(n, p.Y0, p.Y1)
        bh = min(1.18, p.CH / n - 0.12)
        for i, y in enumerate(ys):
            a, _ = C.FEELINGS[i]
            p.img(f"face_{a}", p.X0 + 0.4, y - bh / 2, bh, bh)
            self.dot(p, p.X0 + 0.55 + bh, y)
            _, word = C.FEELINGS[C.FEELING_ORDER[i]]
            ww = 2.4
            p.rect(p.X1 - ww, y - 0.33, ww, 0.66, fill=ch["tint"], stroke=ch["colour"], sw=1.8, r=0.33)
            p.text(word, p.X1 - ww, y - 0.33, ww, 0.66, "title", 20, NAVY, align="center", valign="middle")
            self.dot(p, p.X1 - ww - 0.18, y)
        for a, word in C.FEELINGS:
            p.answers.append((f"{a} face", word))

    def m22(self, m):
        p, ch = self.mission_frame(m)
        labels = ["First", "Next", "Then", "Last"]
        cols = centers(2, p.X0, p.X1)
        avail = p.CH - 1.2
        rows = [p.Y0 + avail * (i + 0.5) / 2 for i in range(2)]
        pos = [(cols[0], rows[0]), (cols[1], rows[0]), (cols[0], rows[1]), (cols[1], rows[1])]
        for i, (cx, cy) in enumerate(pos):
            p.circle(cx - SLOT / 2 - 0.35, cy - SLOT / 2 + 0.1, 0.32, fill=ch["colour"], stroke=NAVY, sw=1.6)
            p.text(str(i + 1), cx - SLOT / 2 - 0.67, cy - SLOT / 2 - 0.22, 0.64, 0.64, "title", 22, NAVY, align="center", valign="middle")
            self.slot(p, cx, cy, f"RT{i + 1}", f"step {i + 1} ({labels[i].lower()})", hint=None)
            p.text(labels[i], cx - 1.0, cy + SLOT / 2 + 0.06, 2.0, 0.36, "title", 15, NAVY, align="center", valign="middle")
        for (y, x1, x2) in ((rows[0], cols[0] + SLOT / 2 + 0.15, cols[1] - SLOT / 2 - 0.75), (rows[1], cols[0] + SLOT / 2 + 0.15, cols[1] - SLOT / 2 - 0.75)):
            p.line(x1, y, x2, y, stroke=ch["deep"], sw=3)
            p.poly([(x2, y - 0.12), (x2 + 0.2, y), (x2, y + 0.12)], fill=ch["deep"], stroke=ch["deep"], sw=1)
        p.poly([(cols[1], rows[0] + SLOT / 2 + 0.48), (cols[1], (rows[0] + rows[1]) / 2 + 0.1), (cols[0], (rows[0] + rows[1]) / 2 + 0.1),
                (cols[0], rows[1] - SLOT / 2 - 0.12)], fill=None, stroke=ch["deep"], sw=3, closed=False, dash=(6, 5))
        by = p.Y1 - 0.95
        p.rect(p.X0, by, p.CW, 0.9, fill=CREAM, stroke=YELLOW, sw=1.4, r=0.2)
        p.img("rt_wake", p.X0 + 0.12, by + 0.08, 0.74, 0.74)
        p.text("Every family's morning is different. What do YOU do first?", p.X0 + 1.0, by, p.CW - 1.1, 0.9, "title", 13, NAVY, valign="middle")

    def m23(self, m):
        p, ch = self.mission_frame(m)
        th = min(p.CH - 0.25, 6.9)
        k = th / 300
        tw = 200 * k
        tx = p.X0 + 1.25
        ty = p.Y0 + 0.25 + (p.CH - 0.25 - th) / 2
        p.img("teddy", tx, ty, tw, th)
        spots = [("TD1", "hat", 100, 26), ("TD2", "jumper", 100, 182), ("TD3", "boots", 100, 262)]
        for pid, lab, ux, uy in spots:
            cy = max(p.Y0 + SLOT / 2, ty + uy * k)
            sx = tx + ux * k
            self.slot(p, sx, cy, pid, f"teddy's {lab}", hint=None)
            p.rect(p.X0, cy - 0.22, 1.05, 0.44, fill=ch["tint"], stroke=ch["colour"], sw=1.4, r=0.22)
            p.text(lab, p.X0, cy - 0.22, 1.05, 0.44, "title", 14, NAVY, align="center", valign="middle")
        rx = tx + tw + 0.2
        rw = p.X1 - rx
        p.img("leo_happy", rx, p.Y0 + 0.3, rw, min(rw * 1.25, 2.2))
        p.rect(rx, p.Y1 - 3.0, rw, 2.9, fill=CREAM, stroke=YELLOW, sw=1.4, r=0.2)
        p.text("Hat on the head, jumper on the body, boots on the feet. Cosy!", rx + 0.1, p.Y1 - 2.95, rw - 0.2, 2.8, "title", 13, NAVY, align="center", valign="middle")

    def m24(self, m):
        p, ch = self.mission_frame(m)
        n = len(C.KINDNESS)
        top, bot = p.Y0, p.Y1 - 1.5
        ys = centers(n, top, bot)
        bh = min(1.85, (bot - top) / n - 0.2)
        bw = 3.05
        for i, y in enumerate(ys):
            a, cap, _, _ = C.KINDNESS[i]
            p.rect(p.X0, y - bh / 2, bw, bh, fill=WHITE, stroke=ch["colour"], sw=2, r=0.2)
            p.img(a, p.X0 + 0.1, y - bh / 2 + 0.1, bh - 0.2, bh - 0.2)
            p.text(cap, p.X0 + bh, y - bh / 2, bw - bh - 0.1, bh, "bold", 11.5, NAVY, valign="middle")
            self.dot(p, p.X0 + bw + 0.17, y)
            _, _, ka, kcap = C.KINDNESS[C.KIND_ORDER[i]]
            x = p.X1 - bw
            p.rect(x, y - bh / 2, bw, bh, fill=ch["tint"], stroke=ch["colour"], sw=2, r=0.2)
            p.img(ka, p.X1 - bh + 0.1, y - bh / 2 + 0.1, bh - 0.2, bh - 0.2)
            p.text(kcap, x + 0.12, y - bh / 2, bw - bh - 0.1, bh, "title", 13, NAVY, valign="middle")
            self.dot(p, x - 0.17, y)
        for a, cap, ka, kcap in C.KINDNESS:
            p.answers.append((cap, kcap))
        gy = p.Y1 - 1.35
        for i, x in enumerate(centers(7, p.X0, p.X1 - 2.6)):
            p.img(["flower_red", "daisy", "flower_yellow", "tulip", "flower_blue", "daisy", "flower_purple"][i], x - 0.4, gy, 0.8, 1.25)
        self.leo_say(p, "leo_proud", p.X1 - 2.55, gy - 0.1, 1.4, "Kind hearts grow!", 1.4, size=10.5)

    # =============================================================== Everyday Village
    def m25(self, m):
        p, ch = self.mission_frame(m)
        secs = [("FRUIT & VEG", ["apple", "carrot"], ["SM1", "SM2"]), ("BAKERY", ["bread", "croissant"], ["SM3", "SM4"]), ("DAIRY", ["milk", "cheese"], ["SM5", "SM6"])]
        ys = centers(3, p.Y0, p.Y1)
        for (lab, icons, acc), y in zip(secs, ys):
            lw = 2.2
            p.rect(p.X0, y - 1.05, lw, 2.1, fill=ch["tint"], stroke=ch["colour"], sw=1.8, r=0.2)
            p.text(lab, p.X0, y - 0.95, lw, 0.4, "title", 15, NAVY, align="center", valign="middle")
            for j, ic in enumerate(icons):
                p.img(ic, p.X0 + 0.25 + j * 0.9, y - 0.45, 0.8, 0.8)
            sx = centers(2, p.X0 + lw + 0.2, p.X1)
            p.img("shelf", p.X0 + lw + 0.2, y + SLOT / 2 - 0.05, p.X1 - p.X0 - lw - 0.2, 0.32, align="top")
            for x in sx:
                self.slot(p, x, y - 0.12, acc, f"{lab.lower()} shelf", hint=None)
            p.answers.append((lab, " & ".join(icons)))

    def m26(self, m):
        p, ch = self.mission_frame(m)
        bh = 2.2
        p.img("backpack", p.X0 + p.CW / 2 - 1.0, p.Y0, 2.0, bh)
        p.img("leo_side", p.X0 + p.CW / 2 + 1.2, p.Y0 + 0.2, 1.6, 2.0)
        p.text("Ready for preschool!", p.X0, p.Y0 + 0.7, p.CW / 2 - 1.15, 0.8, "title", 15, ch["deep"], align="center", valign="middle")
        top = p.Y0 + bh + 0.25
        cols = centers(4, p.X0, p.X1)
        rows = centers(2, top, p.Y1)
        bw = p.CW / 4 - 0.18
        bhh = min(2.6, (p.Y1 - top) / 2 - 0.2)
        for i, (a, lab, ok) in enumerate(C.BACKPACK):
            cx, cy = cols[i % 4], rows[i // 4]
            self.boxed_img(p, a, cx - bw / 2, cy - bhh / 2, bw, bhh, label=lab, lsize=12)
            p.answers.append((lab, "take it" if ok else "leave it at home"))

    def m27(self, m):
        p, ch = self.mission_frame(m)
        rooms = [("room_bathroom", "BATHROOM", "HO1", "toothbrush"), ("room_bedroom", "BEDROOM", "HO2", "pillow"), ("room_kitchen", "KITCHEN", "HO3", "saucepan")]
        order = [1, 2, 0]
        ys = centers(3, p.Y0, p.Y1)
        rh = min(2.45, p.CH / 3 - 0.15)
        rw = rh * 300 / 220
        for k, y in zip(order, ys):
            a, lab, pid, thing = rooms[k]
            p.img(a, p.X0, y - rh / 2, rw, rh)
            p.rect(p.X0, y - rh / 2, rw, rh, fill=None, stroke=NAVY, sw=1.6, r=0.1)
            tw = text_width(lab, "title", 12) + 0.3
            p.rect(p.X0 + 0.1, y - rh / 2 + 0.1, tw, 0.34, fill=WHITE, stroke=NAVY, sw=1.2, r=0.17)
            p.text(lab, p.X0 + 0.1, y - rh / 2 + 0.1, tw, 0.34, "title", 12, NAVY, align="center", valign="middle")
            p.line(p.X0 + rw + 0.15, y, p.X1 - SLOT - 0.45, y, stroke=HINT, sw=2, dash=(4, 4))
            self.slot(p, p.X1 - SLOT / 2 - 0.2, y, pid, f"{lab.lower()} ({thing})", hint=None)

    def m28(self, m):
        p, ch = self.mission_frame(m)
        rw = 2.6
        p.rect(p.X0, p.Y0, rw, p.CH, fill=CREAM, stroke=CORAL, sw=2, r=0.25)
        p.text("RECIPE", p.X0, p.Y0 + 0.1, rw, 0.45, "title", 18, CORAL, align="center", valign="middle")
        steps = [("bread_slice", "bread"), ("lettuce", "lettuce"), ("cheese_slice", "cheese"), ("tomato_slices", "tomato"), ("bread_slice", "bread")]
        sy = centers(5, p.Y0 + 0.6, p.Y1 - 0.1)
        for i, ((a, lab), y) in enumerate(zip(steps, sy)):
            p.circle(p.X0 + 0.35, y, 0.22, fill=ch["colour"], stroke=NAVY, sw=1.2)
            p.text(str(i + 1), p.X0 + 0.13, y - 0.22, 0.44, 0.44, "title", 14, WHITE, align="center", valign="middle")
            p.img(a, p.X0 + 0.68, y - 0.42, 0.84, 0.84)
            p.text(lab, p.X0 + 1.55, y - 0.2, rw - 1.6, 0.4, "title", 13, NAVY, valign="middle")
        cx = p.X0 + rw + (p.CW - rw) / 2
        stack_h = 0.95 + 3 * SLOT + 0.95
        top = p.Y0 + (p.CH - stack_h) / 2
        p.img("bread_slice", cx - 1.2, top, 2.4, 0.95, role="printed")
        p.text("5", cx + 1.25, top + 0.25, 0.4, 0.4, "title", 15, ch["deep"], valign="middle")
        fills = [("CH3", "tomato", "4"), ("CH2", "cheese", "3"), ("CH1", "lettuce", "2")]
        for j, (pid, lab, num) in enumerate(fills):
            cy = top + 0.95 + SLOT * j + SLOT / 2
            self.slot(p, cx, cy, pid, f"sandwich step {num} ({lab})", hint=None)
            p.circle(cx + SLOT / 2 + 0.35, cy, 0.22, fill=ch["colour"], stroke=NAVY, sw=1.2)
            p.text(num, cx + SLOT / 2 + 0.13, cy - 0.22, 0.44, 0.44, "title", 14, WHITE, align="center", valign="middle")
        p.img("bread_slice", cx - 1.2, top + 0.95 + 3 * SLOT, 2.4, 0.95)
        p.text("1", cx + 1.25, top + 0.95 + 3 * SLOT + 0.3, 0.4, 0.4, "title", 15, ch["deep"], valign="middle")

    def m29(self, m):
        p, ch = self.mission_frame(m)
        bands = [("band_sky", "SKY", "VE1", "plane"), ("band_road", "ROAD", "VE2", "car"), ("band_rail", "RAILWAY", "VE3", "train"), ("band_water", "WATER", "VE4", "boat")]
        bh = min((p.CH - 0.36) / 4, p.CW * 120 / 440)
        ys = centers(4, p.Y0, p.Y1)
        for (a, lab, pid, v), y in zip(bands, ys):
            p.img(a, p.X0, y - bh / 2, p.CW, bh)
            p.rect(p.X0, y - bh / 2, p.CW, bh, fill=None, stroke=NAVY, sw=1.6, r=0.2)
            tw = text_width(lab, "title", 13) + 0.34
            p.rect(p.X0 + 0.15, y - bh / 2 + 0.12, tw, 0.36, fill=WHITE, stroke=NAVY, sw=1.2, r=0.18)
            p.text(lab, p.X0 + 0.15, y - bh / 2 + 0.12, tw, 0.36, "title", 13, NAVY, align="center", valign="middle")
            self.slot(p, p.X0 + p.CW * 0.62, y, pid, f"{lab.lower()} ({v})", hint=None)

    def m30(self, m):
        p, ch = self.mission_frame(m)
        times = [("sunrise", "MORNING"), ("sun_high", "DAYTIME"), ("night", "EVENING")]
        tx = centers(3, p.X0, p.X1)
        for x, (a, lab) in zip(tx, times):
            p.img(a, x - 0.85, p.Y0 + 0.05, 1.7, 1.7)
            p.rect(x - 0.85, p.Y0 + 0.05, 1.7, 1.7, fill=None, stroke=NAVY, sw=1.6, r=0.14)
            p.text(lab, x - 1.1, p.Y0 + 1.8, 2.2, 0.4, "title", 16, NAVY, align="center", valign="middle")
            self.dot(p, x, p.Y0 + 2.35)
        ax = centers(len(C.DAY), p.X0, p.X1)
        ay = p.Y1 - 2.15
        bw = p.CW / len(C.DAY) - 0.12
        for x, (a, lab, when) in zip(ax, C.DAY):
            self.dot(p, x, ay - 0.2)
            self.boxed_img(p, a, x - bw / 2, ay, bw, 1.6, label=lab, lsize=10)
            p.answers.append((lab, when))
        p.text("Every day is different – any answer you can explain is right!", p.X0, p.Y1 - 0.45, p.CW, 0.4, "title", 13, ch["deep"], align="center", valign="middle")

    # =============================================================== Adventure Land
    def m31(self, m):
        p, ch = self.mission_frame(m)
        sw_ = p.CW
        sh_ = sw_ * 340 / 420
        p.img("map_scene", p.X0, p.Y0, sw_, sh_)
        k = sw_ / 420
        spots = [("TM1", "palm", "palm tree", 150, 104), ("TM2", "bridge", "bridge (start)", 112, 238), ("TM3", "lighthouse", "lighthouse", 318, 156)]
        for pid, a, lab, ux, uy in spots:
            self.slot(p, p.X0 + ux * k, p.Y0 + uy * k, pid, lab, hint="hint:" + a, hint_scale=0.8)
        by = p.Y0 + sh_ + 0.15
        bh = p.Y1 - by
        p.img("chest", p.X1 - min(bh, 1.4), by, min(bh, 1.4), min(bh, 1.4))
        self.leo_say(p, "leo_point", p.X0, by, min(bh, 1.45), "X marks the spot!", 2.0)
        p.text("Follow the dots from the bridge to the treasure!", p.X0 + 3.3, by, p.CW - 3.3 - min(bh, 1.4) - 0.1, min(bh, 1.4), "bold", 11.5, NAVY, valign="middle")

    def m32(self, m):
        p, ch = self.mission_frame(m)
        cw_ = min(p.CW, (p.CH - 0.6) * 360 / 300)
        chh = cw_ * 300 / 360
        cx0 = p.X0 + (p.CW - cw_) / 2
        cy0 = p.Y0
        p.img("castle_base", cx0, cy0, cw_, chh)
        k = cw_ / 360
        spots = [("CA1", "roof_left", "left tower roof", 60, 58), ("CA2", "roof_right", "right tower roof", 300, 58),
                 ("CA4", "castle_flag", "flag on the wall", 180, 80), ("CA3", "castle_door", "castle door", 180, 216)]
        for pid, a, lab, ux, uy in spots:
            self.slot(p, cx0 + ux * k, cy0 + uy * k, pid, lab, hint="hint:" + a, hint_scale=0.78)
        p.text("triangle  ·  triangle  ·  arch door  ·  flag", p.X0, p.Y1 - 0.5, p.CW, 0.45, "title", 14, ch["deep"], align="center", valign="middle")

    def m33(self, m):
        p, ch = self.mission_frame(m)
        n = len(C.SEQUENCES)
        ys = centers(n, p.Y0, p.Y1)
        rh = min(1.75, p.CH / n - 0.15)
        s = min(1.05, rh - 0.3)
        for i, ((a1, a2, ans, choices), y) in enumerate(zip(C.SEQUENCES, ys)):
            p.rect(p.X0, y - rh / 2, p.CW, rh, fill=ch["tint"], r=0.2)
            x = p.X0 + 0.12
            for a in (a1, a2):
                self.boxed_img(p, a, x, y - s / 2, s, s)
                x += s + 0.05
                self.arrow(p, x + 0.02, y, 0.26)
                x += 0.3
            p.rect(x, y - s / 2, s, s, fill=WHITE, stroke=HINT, sw=1.6, r=0.14, dash=(4, 3))
            p.text("?", x, y - s / 2, s, s, "title", 30, HINT, align="center", valign="middle")
            x += s + 0.18
            p.line(x, y - rh / 2 + 0.15, x, y + rh / 2 - 0.15, stroke=WHITE, sw=3)
            cs = min(0.95, s - 0.05)
            for cx, a in zip(centers(3, x + 0.08, p.X1 - 0.08), choices):
                self.boxed_img(p, a, cx - cs / 2, y - cs / 2, cs, cs)
            p.answers.append((f"row {i + 1}: {a1}, then {a2}", ans))

    def m34(self, m):
        p, ch = self.mission_frame(m)
        fx = centers(6, p.X0, p.X1)
        fy = p.Y0 + 0.1
        for x, (a, kind) in zip(fx, C.NATURE):
            p.rect(x - 0.56, fy, 1.12, 1.2, fill=WHITE, stroke="#C9D3DB", sw=1.2, r=0.14)
            p.img(a, x - 0.48, fy + 0.08, 0.96, 1.04)
            self.dot(p, x, fy + 1.4)
        bx = centers(3, p.X0, p.X1)
        by = p.Y1 - 2.3
        for x, kind in zip(bx, C.BASKETS):
            self.dot(p, x, by - 0.2)
            p.img("basket", x - 1.0, by, 2.0, 1.45)
            p.text(kind.upper(), x - 1.1, by + 1.5, 2.2, 0.4, "title", 15, NAVY, align="center", valign="middle")
            icon = {"leaves": "leaf_green", "flowers": "daisy", "stones": "stone_round"}[kind]
            p.img(icon, x - 0.32, by + 0.45, 0.64, 0.64)
        for a, kind in C.NATURE:
            p.answers.append((a.replace("_", " "), f"{kind} basket"))
        p.text("Draw a line from each treasure to its basket.", p.X0, (fy + 1.5 + by) / 2 - 0.4, p.CW, 0.4, "bold", 12, HINT, align="center", valign="middle")

    def m35(self, m):
        p, ch = self.mission_frame(m)
        g_ = 0.18
        gw = 4 * SLOT + 3 * g_
        x0 = p.X0 + (p.CW - gw) / 2
        p.rect(x0 - 0.2, p.Y0, gw + 0.4, 2 * SLOT + g_ + 0.75, fill=ch["tint"], r=0.25)
        p.text("Card spots: lay your cards here face-down", x0, p.Y0 + 0.05, gw, 0.36, "title", 13, NAVY, align="center", valign="middle")
        allm = [f"MP{i}" for i in range(1, 9)]
        for r in range(2):
            for c in range(4):
                self.slot(p, x0 + c * (SLOT + g_) + SLOT / 2, p.Y0 + 0.5 + r * (SLOT + g_) + SLOT / 2, allm, "memory card spot (any card)", hint="icon_play", hint_scale=0.35)
        hy = p.Y0 + 2 * SLOT + g_ + 0.95
        p.text("HOW TO PLAY", p.X0, hy, p.CW, 0.4, "title", 17, ch["deep"], valign="middle")
        steps = ["Mix up the 8 cards and lay them face-down on the card spots.",
                 "Take turns to turn over two cards.",
                 "Same picture? Keep the pair! Different? Turn them back over.",
                 "Keep going until every pair is found. Everyone is a winner!"]
        sy = hy + 0.5
        sh = min(0.62, (p.Y1 - sy - 1.0) / 4)
        for i, s in enumerate(steps):
            y = sy + i * (sh + 0.08)
            p.circle(p.X0 + 0.25, y + sh / 2, 0.2, fill=ch["colour"], stroke=NAVY, sw=1.2)
            p.text(str(i + 1), p.X0 + 0.05, y + sh / 2 - 0.2, 0.4, 0.4, "title", 13, WHITE, align="center", valign="middle")
            p.text(s, p.X0 + 0.6, y, p.CW - 0.6, sh, "bold", 12, NAVY, valign="middle")
        ex = p.Y1 - 0.95
        for cx, a in zip(centers(4, p.X0, p.X1 - 2.0), ["sun", "boat", "apple", "tulip"]):
            p.img(a, cx - 0.4, ex + 0.05, 0.8, 0.8)
        p.text("4 pairs to find", p.X1 - 2.0, ex, 2.0, 0.9, "title", 14, NAVY, align="center", valign="middle")

    def m36(self, m):
        p, ch = self.mission_frame(m)
        X0, X1, Y0, Y1 = p.X0, p.X1, p.Y0, p.Y1
        stops_y = centers(4, Y0 + 0.2, Y1 - 1.6)
        lx, rx = X0 + p.CW * 0.3, X0 + p.CW * 0.7
        stops = [
            (rx, stops_y[0], "STOP 1 · COLOUR", "Find the BLUE drop", "RD5", "drophint_blue", None),
            (lx, stops_y[1], "STOP 2 · SHAPE", "Find the STAR", "SH5", "shapesil_star", None),
            (rx, stops_y[2], "STOP 3 · COUNT", "How many apples?", "NU4", None, "apples"),
            (lx, stops_y[3], "STOP 4 · PICTURE", "Who lives on the ice?", "AN4", None, "hab_ice"),
        ]
        home = (X1 - 1.15, Y1 - 0.85)
        start = (X0 + 0.75, Y0 + 0.6)
        pts = [start] + [(x, y) for x, y, *_ in stops] + [home]
        p.poly(pts, fill=None, stroke="#F6DFA4", sw=30, closed=False)
        p.poly(pts, fill=None, stroke=CORAL, sw=3, closed=False, dash=(8, 7))
        p.img("leo_side", X0, Y0, 1.3, 1.6)
        p.text("START", X0, Y0 + 1.55, 1.3, 0.3, "title", 12, ch["deep"], align="center", valign="middle")
        for (x, y, head, ask, pid, hint, extra) in stops:
            side = -1 if x > X0 + p.CW / 2 else 1
            tx = x + side * (SLOT / 2 + 0.15) - (2.4 if side < 0 else 0)
            p.rect(tx, y - 0.62, 2.4, 0.38, fill=ch["deep"], r=0.19)
            p.text(head, tx, y - 0.62, 2.4, 0.38, "title", 11.5, WHITE, align="center", valign="middle")
            p.text(ask, tx, y - 0.2, 2.4, 0.4, "title", 13, NAVY, align="center", valign="middle")
            if extra == "apples":
                self.group_grid(p, "finale_apples", "apple", C.FINALE_APPLES, tx + 0.2, y + 0.22, 2.0, 0.55, per_row=4, size=0.48)
            elif extra:
                p.img(extra, tx + 0.55, y + 0.22, 1.3, 0.85)
            self.slot(p, x, y, pid, f"{head.title()} ({ask})", hint=hint, hint_scale=0.74)
        p.img("house_home", home[0] - 0.95, home[1] - 1.3, 1.9, 1.9)
        p.img("sparkle", home[0] - 1.45, home[1] - 1.25, 0.45, 0.45)
        p.img("sparkle", home[0] + 0.8, home[1] - 1.45, 0.38, 0.38)
        p.rect(X0 + 0.1, Y1 - 0.55, 3.9, 0.5, fill=YELLOW, stroke=NAVY, sw=1.6, r=0.25)
        p.text("HOME! Mission complete!", X0 + 0.1, Y1 - 0.55, 3.9, 0.5, "title", 15, NAVY, align="center", valign="middle")

    # =============================================================== piece sheets
    def piece_card(self, p, x, y, pid, record=True):
        s, asset, label = C.PIECE_INDEX[pid]
        ch = next(c for c in C.CHAPTERS if c["colour"] == s["tab"])
        p.rect(x, y, PIECE, PIECE, fill=WHITE, stroke=NAVY, sw=1.4, r=0.12, role="cut", name=pid)
        p.rect(x + 0.07, y + PIECE - 0.31, PIECE - 0.14, 0.24, fill=ch["tint"], r=0.08)
        pages = self.set_pages(s["code"])
        p.text(pid, x + 0.12, y + PIECE - 0.31, 0.6, 0.24, "xbold", 8.5, NAVY, valign="middle")
        ptxt = (f"p{pages[0]}–{pages[-2]}, {pages[-1]}" if len(pages) > 3 else "p" + ", ".join(str(q) for q in pages))
        p.text(ptxt, x + 0.55, y + PIECE - 0.31, PIECE - 0.67, 0.24, "bold", 7, NAVY,
               align="right", valign="middle", min_size=6)
        if asset is None:  # number card
            n = int(pid[2:])
            p.text(str(n), x, y + 0.04, PIECE, 0.78, "title", 46, ch["deep"], align="center", valign="middle")
            rows_ = 1 if n <= 5 else 2
            for d in range(n):
                r_ = d // 5
                cnt = min(5, n - r_ * 5)
                xs = centers(cnt, x + 0.3, x + PIECE - 0.3)
                p.circle(xs[d % 5], y + 0.92 + r_ * 0.2 + (0.1 if rows_ == 1 else 0), 0.075, fill=CORAL, stroke=NAVY, sw=0.8, group=f"card_{pid}")
            if record:
                p.add_group(f"card_{pid}", n)
        else:
            p.img(asset, x + 0.16, y + 0.1, PIECE - 0.32, PIECE - 0.46)
        if record:
            p.pieces.append(dict(id=pid, x=x, y=y, w=PIECE, h=PIECE, label=label, set=s["code"]))

    def piece_sheet(self, i):
        num = 41 + i
        p = self.new(num, "pieces")
        p.title = f"Cut-out Sheet {i + 1} of 5"
        W, H = self.W, self.H
        sets = self.sheets[i]
        p.img("icon_scissors", M, M, 0.42, 0.42)
        p.text(f"CUT-OUT SHEET {i + 1} OF 5", M + 0.5, M - 0.02, 3.6, 0.46, "title", 18, NAVY, valign="middle")
        p.text("Grown-ups: cut along the solid lines", W - M - 3.3, M - 0.02, 3.3, 0.46, "xbold", 10, CORAL, align="right", valign="middle")
        legend = "   ·   ".join(f"{s['code']} = {s['name']} (p{', p'.join(str(q) for q in self.set_pages(s['code']))})" for s in sets)
        p.text(legend, M, M + 0.46, W - 2 * M, 0.34, "bold", 7.8, NAVY, leading=1.15)
        ids_ = [pid for s in sets for pid, _, _ in s["items"]]
        gw = 4 * PIECE + 3 * GAP
        gx = (W - gw) / 2
        gy = M + 0.88
        for k, pid in enumerate(ids_):
            r, c = divmod(k, 4)
            self.piece_card(p, gx + c * (PIECE + GAP), gy + r * (PIECE + GAP), pid)
        p.text(f"Store these {len(ids_)} pieces in an envelope labelled “Sheet {i + 1}”.  Throw away any torn or damaged pieces.",
               M, H - M - 0.3, W - 2 * M - 0.5, 0.26, "bold", 8, MUTED, valign="middle")
        p.circle(W - M - 0.17, H - M - 0.15, 0.17, fill=LGREY, stroke=NAVY, sw=1.2)
        p.text(str(num), W - M - 0.4, H - M - 0.28, 0.46, 0.26, "title", 10, NAVY, align="center", valign="middle")

    # =============================================================== pages 46-48
    def reference(self):
        p = self.new(46, "reference")
        p.title = "Adult Reference"
        W, H = self.W, self.H
        p.text("GROWN-UP REFERENCE & ANSWER KEY", M, M, W - 2 * M, 0.42, "title", 20, NAVY, valign="middle")
        p.text("Answers are suggestions – praise effort and thinking, and accept any choice your child can sensibly explain.",
               M, M + 0.42, W - 2 * M, 0.24, "body", 8.5, NAVY)
        rows = [(f"{m['n']:02d}", str(m["page"]), m["title"].title().replace("'S", "'s"), self.pieces_short(m), C.ANSWER_SHORT[m["n"]]) for m in C.MISSIONS]
        colw = (W - 2 * M - 0.2) / 2
        ty = M + 0.72
        rh = 0.3
        for half in range(2):
            x = M + half * (colw + 0.2)
            p.rect(x, ty, colw, 0.24, fill=NAVY, r=0.05)
            heads = [("#", 0.22), ("Pg", 0.24), ("Mission", 1.0), ("Pieces", 0.74), ("Answer / tip", colw - 2.24)]
            xx = x + 0.04
            for hname, w in heads:
                p.text(hname, xx, ty, w, 0.24, "xbold", 7, WHITE, valign="middle")
                xx += w
            for j, row in enumerate(rows[half * 18:(half + 1) * 18]):
                y = ty + 0.25 + j * rh
                if j % 2 == 0:
                    p.rect(x, y, colw, rh, fill="#F1F4F6")
                xx = x + 0.04
                for (hname, w), val in zip(heads, row):
                    p.text(val, xx, y, w - 0.03, rh, "bold" if hname in ("#", "Mission") else "body", 6.6, NAVY, valign="middle", min_size=6.0, leading=1.1)
                    xx += w
        y = ty + 0.25 + 18 * rh + 0.15
        boxes = [
            ("AT EVERY STAGE", [
                "Just starting (about 3): offer 2–3 pieces at a time, point and name together, and help place them.",
                "Growing (about 4): try a whole board, count aloud, take turns and talk about choices.",
                "Confident (about 5): invent new patterns, explain answers, try the 6–10 tower and play memory with all pairs.",
                "Every child develops at their own pace – repeat favourites, skip ahead or come back later."]),
            ("STORAGE", [
                "Keep each cut-out sheet's pieces in its own labelled envelope or zip bag (Sheet 1–5).",
                "Shared pieces (RD, SH, AN, NU) are used on several pages – return them to their envelope after play.",
                "Store the book flat in a folder; keep pieces out of reach of younger children."]),
            ("PRINTING TIPS", [
                "Print at Actual size / 100% (not 'fit to page') so the cards fit the boards.",
                "Use the US Letter PDF for Letter paper and the A4 PDF for A4 paper.",
                "Card stock (160–220 gsm) is sturdier. Print only the pages you need; reprint pieces any time for household use."]),
        ]
        bw = (W - 2 * M - 0.3) / 3
        bh = H - M - 0.45 - y
        for k, (head, items) in enumerate(boxes):
            x = M + k * (bw + 0.15)
            p.rect(x, y, bw, bh, fill=CREAM, stroke="#E9DDB6", sw=1.2, r=0.15)
            p.text(head, x + 0.1, y + 0.06, bw - 0.2, 0.28, "title", 11, CORAL, valign="middle")
            p.text("\n".join("• " + s for s in items), x + 0.1, y + 0.38, bw - 0.2, bh - 0.45, "body", 7.8, NAVY, leading=1.2, min_size=6.5)
        self.footer(p, "Full answer key and piece inventory: provided with the publisher files", None, LGREY)

    def pieces_short(self, m):
        if not m["pieces"]:
            return "no-cut"
        groups = {}
        for pid in m["pieces"]:
            code = pid.rstrip("0123456789")
            groups.setdefault(code, []).append(int(pid[len(code):]))
        out = []
        for code, nums in groups.items():
            nums.sort()
            lab = f"{code}{nums[0]}–{nums[-1]}" if len(nums) > 2 and nums == list(range(nums[0], nums[-1] + 1)) else ",".join(f"{code}{n}" for n in nums)
            out.append(f"{lab} p{self.sheet_of[code + str(nums[0])]}")
        return "; ".join(out)

    def certificate(self):
        p = self.new(47, "certificate")
        p.title = "Certificate and Reward Stars"
        W, H = self.W, self.H
        ch_h = H * 0.56
        p.rect(M, M, W - 2 * M, ch_h, fill=CREAM, stroke=YELLOW, sw=5, r=0.35)
        p.rect(M + 0.15, M + 0.15, W - 2 * M - 0.3, ch_h - 0.3, fill=None, stroke=CORAL, sw=1.5, r=0.28, dash=(3, 4))
        p.img("rosette", M + 0.35, M + 0.3, 1.0, 1.3)
        p.img("leo_cheer", W - M - 1.4, M + 0.25, 1.1, 1.38)
        p.text("CERTIFICATE OF", M + 1.45, M + 0.45, W - 2 * M - 2.9, 0.45, "title", 20, NAVY, align="center", valign="middle")
        p.text("GREAT EXPLORING", M + 1.45, M + 0.88, W - 2 * M - 2.9, 0.75, "title", 34, CORAL, align="center", valign="middle", min_size=24)
        p.text("This certificate is proudly given to", M, M + 1.75, W - 2 * M, 0.35, "bold", 13, NAVY, align="center", valign="middle")
        lw = W - 3.2
        p.line((W - lw) / 2, M + 2.75, (W + lw) / 2, M + 2.75, stroke=NAVY, sw=1.6)
        p.text("child's name", M, M + 2.8, W - 2 * M, 0.25, "body", 9, MUTED, align="center")
        p.text("for completing all 36 missions in", M, M + 3.15, W - 2 * M, 0.3, "bold", 12.5, NAVY, align="center", valign="middle")
        p.text("MY MAGIC BUSY BOOK!", M, M + 3.45, W - 2 * M, 0.45, "title", 22, NAVY, align="center", valign="middle")
        p.line(M + 1.0, M + ch_h - 0.65, M + 3.2, M + ch_h - 0.65, stroke=NAVY, sw=1.4)
        p.text("date", M + 1.0, M + ch_h - 0.6, 2.2, 0.25, "body", 9, MUTED, align="center")
        p.line(W - M - 3.2, M + ch_h - 0.65, W - M - 1.0, M + ch_h - 0.65, stroke=NAVY, sw=1.4)
        p.text("signed (grown-up)", W - M - 3.2, M + ch_h - 0.6, 2.2, 0.25, "body", 9, MUTED, align="center")
        # stars
        sy = M + ch_h + 0.15
        p.text("MY SIX REWARD STARS", M, sy, W - 2 * M, 0.38, "title", 16, NAVY, align="center", valign="middle")
        p.text("Colour a star for each world you finish – or cut them out and stick them on your Mission Map (page 4).",
               M, sy + 0.36, W - 2 * M, 0.28, "body", 9.5, NAVY, align="center", valign="middle")
        cols = centers(3, M, W - M)
        avail = H - M - 0.45 - (sy + 0.75)
        rows = [sy + 0.75 + avail * (k + 0.5) / 2 for k in range(2)]
        ss = min(1.65, avail / 2 - 0.35)
        for i, chp in enumerate(C.CHAPTERS):
            cx, cy = cols[i % 3], rows[i // 3]
            p.img("reward_star_blank", cx - ss / 2, cy - ss / 2 - 0.15, ss, ss, role="reward")
            p.text(str(chp["num"]), cx - 0.4, cy - 0.35, 0.8, 0.5, "title", 22, chp["deep"], align="center", valign="middle")
            p.text(chp["name"], cx - 1.2, cy + ss / 2 - 0.12, 2.4, 0.3, "title", 11.5, NAVY, align="center", valign="middle")
        self.footer(p, "Reward stars are optional – colour them in, or an adult can cut them out", None, YELLOW)

    def back_cover(self):
        p = self.new(48, "back")
        p.title = "Back Cover"
        W, H = self.W, self.H
        p.rect(0, 0, W, H, fill=NAVY)
        p.rect(M, M, W - 2 * M, H - 2 * M, fill=CREAM, r=0.4)
        p.text(C.PRODUCT["brand"], M, M + 0.3, W - 2 * M, 0.45, "title", 22, NAVY, align="center", valign="middle")
        p.text(C.PRODUCT["tagline"], M, M + 0.75, W - 2 * M, 0.35, "bold", 13, CORAL, align="center", valign="middle")
        p.img("leo_wave", W / 2 - 1.2, M + 1.2, 2.4, 3.0)
        p.text("Thank you for exploring with Leo!", M, M + 4.25, W - 2 * M, 0.42, "title", 18, NAVY, align="center", valign="middle")
        desc = ("My Magic Busy Book is a 48-page printable activity book for ages 3–5 with adult help. Six little worlds hold "
                "36 missions to match, sort, count, build and imagine. Five cut-out sheets supply reusable paper pieces that are "
                f"shared across the boards, and {C.NO_CUT_COUNT} missions need no cutting at all.")
        p.text(desc, M + 0.6, M + 4.75, W - 2 * M - 1.2, 1.0, "body", 10.5, NAVY, align="center", leading=1.25)
        y = M + 5.85
        bw = (W - 2 * M - 0.9) / 3
        blocks = [
            ("PRINTING", "Print at Actual size / 100% on US Letter or A4 paper. Card stock and lamination are optional."),
            ("SAFETY", "Not suitable for children under 3. Contains detachable paper pieces. An adult must prepare all pieces and supervise play."),
            ("LICENCE", "For personal / single-household use only. You may print copies for your own household. Do not resell, share or redistribute the files."),
        ]
        for k, (head, body) in enumerate(blocks):
            x = M + 0.3 + k * (bw + 0.15)
            p.rect(x, y, bw, 2.2, fill=WHITE, stroke="#E9DDB6", sw=1.2, r=0.18)
            p.text(head, x + 0.1, y + 0.1, bw - 0.2, 0.3, "title", 12, CORAL, align="center", valign="middle")
            p.text(body, x + 0.12, y + 0.45, bw - 0.24, 1.7, "body", 9, NAVY, align="center", leading=1.22)
        p.text("© 2026 Little Worlds Learning. All illustrations, characters (including Leo the Little Explorer) and text are original "
               "works of Little Worlds Learning. Fonts: Fredoka and Nunito (SIL Open Font License 1.1).",
               M + 0.4, H - M - 1.3, W - 2 * M - 0.8, 0.5, "body", 8, MUTED, align="center")
        p.text(f"Digital download · 48 pages · {C.PRODUCT['version']}", M, H - M - 0.7, W - 2 * M, 0.3, "xbold", 9.5, NAVY, align="center", valign="middle")
        p.text("Edition: " + ("US Letter (8.5 × 11 in)" if self.ed == "US_Letter" else "A4 (210 × 297 mm)"), M, H - M - 0.42, W - 2 * M, 0.26,
               "bold", 8.5, MUTED, align="center", valign="middle")
