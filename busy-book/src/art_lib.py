"""Little Worlds Learning - original illustration library (part 2).

Every function returns a complete SVG document string. ASSETS maps an asset
name to a zero-argument builder so the library can be exported to individual
SVG files (03_ILLUSTRATIONS) and placed into pages by name.
"""
import math
import re
from art_core import *  # noqa: F401,F403
import art_core as C

ASSETS = {}


def asset(name, w=200, h=200, title=None):
    def deco(fn):
        def build():
            return svg_doc(fn(), w, h, title or name.replace("_", " "))
        ASSETS[name] = build
        build.size = (w, h)
        return fn
    return deco


def reg(name, builder):
    ASSETS[name] = builder


def silhouette(svg, fill="#6E7F8C", stroke=None):
    """Turn any asset into a flat silhouette (used for shadow / hint outlines)."""
    stroke = stroke or fill
    svg = re.sub(r'fill="(?!none)[^"]*"', f'fill="{fill}"', svg)
    svg = re.sub(r'stroke="(?!none)[^"]*"', f'stroke="{stroke}"', svg)
    return svg


# ------------------------------------------------------------------ Leo
reg("leo_front", lambda: C.leo_front())
reg("leo_side", lambda: C.leo_side())
reg("leo_three_quarter", lambda: C.leo_three_quarter())
for _p in C.LEO_POSES:
    reg(_p, (lambda n: (lambda: C.leo_pose(n)))(_p))
reg("leo_head", lambda: C.leo_head_only())
reg("leo_head_happy", lambda: C.leo_head_only("happy", "open"))


# ------------------------------------------------------------------ icons (skill system)
@asset("icon_match")
def _():
    return (rect(22, 46, 70, 96, SKY, 14) + star(57, 94, 22, YELLOW, NAVY, 4) +
            rect(108, 46, 70, 96, LIME, 14) + star(143, 94, 22, YELLOW, NAVY, 4) +
            path("M70,162 Q100,186 130,162", "none", NAVY, 6) + path("M120,154 L132,162 L122,174", "none", NAVY, 6))


@asset("icon_sort")
def _():
    return (rect(18, 110, 50, 60, CORAL, 10) + rect(76, 110, 50, 60, YELLOW, 10) + rect(134, 110, 50, 60, SKY, 10) +
            circle(43, 70, 16, CORAL) + star(101, 70, 20, YELLOW, NAVY, 4) +
            poly([(159, 52), (177, 84), (141, 84)], SKY, NAVY, 4) +
            path("M43,90 v12 M101,92 v10 M159,90 v12", "none", NAVY, 4))


@asset("icon_count")
def _():
    return (rect(20, 40, 160, 120, CREAM, 18) +
            "".join(circle(52 + 48 * i, 80, 15, [CORAL, YELLOW, LIME][i]) for i in range(3)) +
            "".join(rect(40 + 48 * i, 112, 24, 30, WHITE, 6, NAVY, 3) for i in range(3)) +
            path("M47,120 v14", "none", NAVY, 4) + path("M93,120 q8,-4 8,4 q0,6 -8,10 h10", "none", NAVY, 3.5) +
            path("M141,120 q8,-4 8,3 q0,3 -5,4 q6,1 5,5 q-2,5 -9,2", "none", NAVY, 3.5))


@asset("icon_build")
def _():
    return (rect(30, 120, 60, 50, CORAL, 8) + rect(96, 120, 60, 50, SKY, 8) + rect(62, 66, 60, 50, LIME, 8) +
            poly([(92, 18), (130, 60), (54, 60)], YELLOW, NAVY, 5) +
            circle(48, 132, 5, WHITE, None, 0) + circle(114, 132, 5, WHITE, None, 0) + circle(80, 78, 5, WHITE, None, 0))


@asset("icon_imagine")
def _():
    return (blob([(70, 86, 34), (110, 70, 38), (146, 92, 30), (100, 108, 32)], WHITE) +
            circle(54, 142, 10, WHITE) + circle(38, 166, 6, WHITE) +
            star(104, 88, 20, YELLOW, NAVY, 4) + heart(140, 92, 11, PINK, NAVY, 3.5) + circle(72, 92, 9, SKY, NAVY, 3.5))


@asset("icon_explore")
def _():
    return (path("M118,118 L170,170", "none", NAVY, 22) + path("M118,118 L170,170", "none", CORAL, 12) +
            circle(86, 86, 50, WATER) + circle(86, 86, 50, "none", NAVY, 10) +
            path("M62,72 q10,-18 30,-18", "none", WHITE, 7))


@asset("icon_scissors")
def _():
    return (circle(52, 140, 22, CORAL) + circle(52, 140, 10, WHITE) + circle(110, 156, 22, CORAL) + circle(110, 156, 10, WHITE) +
            poly([(66, 124), (170, 40), (176, 50), (82, 136)], LGREY, NAVY, 4) +
            poly([(96, 144), (176, 70), (180, 84), (100, 158)], LGREY, NAVY, 4) + circle(86, 136, 5, NAVY, None, 0))


@asset("icon_printer")
def _():
    return (rect(56, 26, 88, 50, WHITE, 6) + rect(24, 70, 152, 70, SKY, 16) + rect(52, 118, 96, 62, WHITE, 6) +
            path("M68,140 h64 M68,158 h44", "none", GREY, 5) + circle(152, 92, 7, LIME, NAVY, 3))


@asset("icon_laminate")
def _():
    return (rect(40, 30, 120, 150, WATER, 16) + rect(56, 46, 88, 118, WHITE, 8) +
            star(100, 98, 26, YELLOW, NAVY, 4) + path("M60,40 L80,30 M140,170 L158,160", "none", WHITE, 6))


@asset("icon_fastener")
def _():
    return (rect(30, 40, 140, 120, CREAM, 16) + circle(100, 100, 32, LGREY) +
            "".join(circle(100 + 18 * math.cos(math.radians(a)), 100 + 18 * math.sin(math.radians(a)), 4, NAVY, None, 0)
                    for a in range(0, 360, 45)) + circle(100, 100, 4, NAVY, None, 0))


@asset("icon_play")
def _():
    return (heart(100, 104, 64, CORAL, NAVY, 6) + star(150, 52, 18, YELLOW, NAVY, 4) + star(46, 56, 12, YELLOW, NAVY, 3))


@asset("icon_storage")
def _():
    return (rect(28, 70, 144, 100, TAN, 10) + poly([(28, 70), (100, 126), (172, 70)], "#E8C08A", NAVY, 5) +
            rect(60, 30, 50, 50, SKY, 8) + rect(96, 40, 46, 46, LIME, 8))


@asset("icon_nocut")
def _():
    return (path("M70,40 L130,160", "none", NAVY, 18) + path("M70,40 L130,160", "none", YELLOW, 10) +
            poly([(124, 150), (138, 178), (140, 146)], CORAL, NAVY, 4) +
            path("M40,170 q20,-26 40,0 t40,0", "none", SKY, 7))


@asset("icon_tap")
def _():
    return (circle(100, 100, 78, "none", "#BFE9F7", 8) + circle(100, 100, 54, "none", SKY, 8) + circle(100, 100, 28, CORAL, NAVY, 6))


@asset("icon_warning")
def _():
    return poly([(100, 22), (182, 168), (18, 168)], YELLOW, NAVY, 8) + rect(92, 70, 16, 54, NAVY, 8, None, 0) + circle(100, 146, 9, NAVY, None, 0)


# ------------------------------------------------------------------ colour drops / clouds / tokens
for _c, (_hex, _sym) in ACT.items():
    def _mk(hexc=_hex, sym=_sym):
        return lambda: svg_doc(path(drop_d(100, 108, 84), hexc, NAVY, 6) + symbol(sym, 100, 128, 30, WHITE, NAVY, 4) +
                               path("M70,90 q4,-24 18,-38", "none", WHITE, 7), 200, 200)
    reg(f"drop_{_c}", _mk())

    def _mkh(hexc=_hex, sym=_sym):
        return lambda: svg_doc(path(drop_d(100, 108, 80), WHITE, hexc, 5).replace("/>", ' stroke-dasharray="12 9"/>') +
                               symbol(sym, 100, 128, 28, "none" if sym == "wave" else WHITE, hexc, 5), 200, 200)
    reg(f"drophint_{_c}", _mkh())

    def _mkc(hexc=_hex, sym=_sym):
        return lambda: svg_doc(blob([(70, 96, 40), (116, 78, 50), (160, 102, 36), (104, 112, 36)], WHITE, 6,
                                    rects=[(40, 96, 150, 46, 23)]) +
                               circle(110, 104, 30, hexc, NAVY, 5) + symbol(sym, 110, 106, 18, WHITE, NAVY, 3.5), 220, 150)
    reg(f"cloud_{_c}", _mkc())

    def _mkt(hexc=_hex, sym=_sym):
        return lambda: svg_doc(circle(100, 100, 84, hexc, NAVY, 7) + symbol(sym, 100, 104, 46, WHITE, NAVY, 5), 200, 200)
    reg(f"token_{_c}", _mkt())


# ------------------------------------------------------------------ shapes
SHAPES = {
    "circle": (CORAL, lambda f, s, sw: circle(100, 100, 74, f, s, sw)),
    "square": (SKY, lambda f, s, sw: rect(30, 30, 140, 140, f, 10, s, sw)),
    "triangle": (LIME, lambda f, s, sw: poly([(100, 24), (180, 166), (20, 166)], f, s, sw)),
    "rectangle": (PINK, lambda f, s, sw: rect(14, 56, 172, 88, f, 10, s, sw)),
    "star": (YELLOW, lambda f, s, sw: star(100, 106, 84, f, s, sw, r=40)),
}
for _n, (_col, _fn) in SHAPES.items():
    reg(f"shape_{_n}", (lambda col=_col, fn=_fn: (lambda: svg_doc(fn(col, NAVY, 7), 200, 200)))())
    reg(f"shapesil_{_n}", (lambda fn=_fn: (lambda: svg_doc(
        fn("#E7ECF0", "#8C9BA7", 6).replace("/>", ' stroke-dasharray="14 10"/>'), 200, 200)))())


# ------------------------------------------------------------------ ice cream
FLAVOURS = {
    "strawberry": ("#F59AC0", "heart"),
    "chocolate": ("#9A6A44", "circle"),
    "mint": ("#8FDCB4", "leaf"),
    "lemon": ("#FFE36E", "star"),
    "blueberry": ("#6FA8E8", "wave"),
    "orange": ("#F9A04B", "diamond"),
}


def scoop(col, sym, cx=100, cy=100, r=72):
    y0 = cy + 34
    bumps = ""
    n = 4
    step = 2 * r / n
    for i in range(n):
        x1 = cx + r - i * step
        bumps += f" Q{x1 - step / 2:.1f},{y0 + 30:.1f} {x1 - step:.1f},{y0:.1f}"
    d = f"M{cx - r:.1f},{y0:.1f} C{cx - r:.1f},{cy - r * 1.45:.1f} {cx + r:.1f},{cy - r * 1.45:.1f} {cx + r:.1f},{y0:.1f}" + bumps + " Z"
    return (path(d, col, NAVY, 6) +
            path(f"M{cx - r * 0.55:.1f},{cy - r * 0.2:.1f} q{r * 0.15:.1f},-{r * 0.38:.1f} {r * 0.5:.1f},-{r * 0.45:.1f}", "none", WHITE, 7) +
            symbol(sym, cx + 8, cy + 6, 24, WHITE, NAVY, 3.5))


for _f, (_col, _sym) in FLAVOURS.items():
    reg(f"scoop_{_f}", (lambda col=_col, sym=_sym: (lambda: svg_doc(scoop(col, sym), 200, 200)))())


@asset("cone", 200, 200)
def _():
    out = poly([(40, 30), (160, 30), (100, 190)], "#F2C27B", NAVY, 6)
    for i in range(1, 5):
        out += line(40 + i * 24, 30, 100 + (i * 24 - 60) * 0.25, 160, "#C8914A", 3)
    out += rect(32, 18, 136, 26, "#F2C27B", 12)
    return out


# ------------------------------------------------------------------ flowers / pots
def flower(cx, cy, col, r=22, stem=True, sym=None):
    out = ""
    if stem:
        out += path(f"M{cx},{cy + 10} L{cx},{cy + 90}", "none", DGREEN, 7)
        out += path(leaf_d(cx + 18, cy + 56, 16), GREEN, NAVY, 4)
    pet = [(cx + r * 1.1 * math.cos(math.radians(a)), cy + r * 1.1 * math.sin(math.radians(a)), r * 0.72) for a in range(0, 360, 60)]
    out += blob(pet, col)
    out += circle(cx, cy, r * 0.6, YELLOW if col != C.ACT["yellow"][0] else "#F7923A", NAVY, 4)
    if sym:
        out += symbol(sym, cx, cy + 1, r * 0.38, WHITE, NAVY, 2.5)
    return out


for _c in ("red", "yellow", "blue", "purple"):
    _hex, _sym = ACT[_c]
    reg(f"flower_{_c}", (lambda h=_hex, s=_sym: (lambda: svg_doc(flower(100, 62, h, 34, True, s), 200, 200)))())

    def _pot(h=_hex, s=_sym):
        return lambda: svg_doc(poly([(36, 70), (164, 70), (146, 186), (54, 186)], h, NAVY, 6) +
                               rect(26, 52, 148, 30, h, 10) + circle(100, 130, 26, WHITE, NAVY, 4) +
                               symbol(s, 100, 132, 15, h if s != "wave" else "none", NAVY, 3) +
                               (symbol(s, 100, 132, 15, "none", h, 3) if s == "wave" else ""), 200, 200)
    reg(f"pot_{_c}", _pot())


@asset("daisy")
def _():
    return flower(100, 64, WHITE, 36, True)


@asset("tulip")
def _():
    return (path("M100,90 L100,186", "none", DGREEN, 7) + path(leaf_d(124, 150, 26), GREEN, NAVY, 4) +
            path("M64,40 L82,58 L100,34 L118,58 L136,40 L136,80 Q100,124 64,80 Z", CORAL, NAVY, 6))


# ------------------------------------------------------------------ robot
@asset("robot_antenna")
def _():
    return (rect(40, 140, 120, 40, LGREY, 12) + line(100, 140, 100, 64, NAVY, 7) + circle(100, 52, 22, CORAL) +
            star(100, 52, 10, YELLOW, NAVY, 2.5) + circle(52, 150, 6, YELLOW, NAVY, 3) + circle(148, 150, 6, YELLOW, NAVY, 3))


@asset("robot_head")
def _():
    return (rect(22, 30, 156, 140, SKY, 26) + rect(8, 76, 18, 46, LIME, 8) + rect(174, 76, 18, 46, LIME, 8) +
            circle(70, 88, 24, WHITE) + eye(72, 90, 10) + circle(130, 88, 24, WHITE) + eye(132, 90, 10) +
            rect(60, 128, 80, 24, WHITE, 12) + path("M80,128 v24 M100,128 v24 M120,128 v24", "none", NAVY, 3))


@asset("robot_body")
def _():
    return (rect(22, 20, 156, 160, LIME, 22) + rect(0, 50, 26, 90, YELLOW, 12) + rect(174, 50, 26, 90, YELLOW, 12) +
            rect(52, 50, 96, 70, WHITE, 12) + heart(100, 88, 22, CORAL, NAVY, 4) +
            circle(64, 148, 10, CORAL) + circle(100, 148, 10, YELLOW) + circle(136, 148, 10, SKY))


@asset("robot_wheels")
def _():
    return (rect(40, 20, 120, 60, LGREY, 14) + circle(60, 130, 44, NAVY) + circle(60, 130, 20, YELLOW, NAVY, 4) +
            circle(140, 130, 44, NAVY) + circle(140, 130, 20, YELLOW, NAVY, 4))


# ------------------------------------------------------------------ animals
@asset("fish")
def _():
    return (poly([(150, 100), (192, 62), (192, 138)], CORAL, NAVY, 6) +
            ellipse(92, 100, 74, 52, "#F7923A") + path("M80,52 Q100,22 128,58", "#F7923A", NAVY, 6) +
            path("M70,62 Q58,100 70,138", "none", NAVY, 4) + path("M104,58 Q92,100 104,142", "none", "#FFB977", 8) +
            eye(46, 88, 8) + path("M22,112 q10,6 18,0", "none", NAVY, 4) + path("M118,124 q14,16 28,4", "#FFD9B0", NAVY, 4))


@asset("cow")
def _():
    out = ""
    for x in (48, 74, 128, 152):
        out += rect(x - 10, 128, 20, 50, WHITE, 8) + rect(x - 10, 166, 20, 14, DGREY, 6)
    out += path("M172,100 q20,10 14,44", "none", NAVY, 5) + circle(186, 148, 6, DGREY, NAVY, 3)
    out += rect(36, 70, 140, 74, WHITE, 34)
    out += path("M120,74 q22,-2 30,14 q-6,22 -28,18 q-14,-14 -2,-32 Z", NAVY, None, 0)
    out += path("M60,110 q16,-8 24,8 q-6,16 -22,12 Z", NAVY, None, 0)
    out += ellipse(160, 158, 14, 9, PINK, NAVY, 3)
    out += path("M30,40 q-14,-12 -10,-24 M70,40 q14,-12 10,-24", "none", "#E9D6A6", 9)
    out += ellipse(50, 68, 40, 36, WHITE) + ellipse(50, 92, 32, 20, PINK)
    out += circle(40, 94, 4, NAVY, None, 0) + circle(60, 94, 4, NAVY, None, 0)
    out += eye(36, 60, 6) + eye(64, 60, 6)
    out += ellipse(10, 54, 14, 8, WHITE) + ellipse(90, 54, 14, 8, WHITE)
    out += path("M44,34 q8,10 16,0 q-4,12 -8,14 q-4,-2 -8,-14 Z", NAVY, None, 0)
    return out


@asset("monkey")
def _():
    return (path("M134,150 C186,150 186,96 160,92 C146,92 146,110 160,112", "none", NAVY, 13) +
            path("M134,150 C186,150 186,96 160,92 C146,92 146,110 160,112", "none", BROWN, 7) +
            ellipse(100, 140, 44, 46, BROWN) + ellipse(100, 148, 28, 32, MUZZLE, None, 0) +
            rect(54, 168, 34, 22, BROWN, 11) + rect(112, 168, 34, 22, BROWN, 11) +
            circle(44, 66, 20, BROWN) + circle(44, 66, 10, MUZZLE, None, 0) +
            circle(156, 66, 20, BROWN) + circle(156, 66, 10, MUZZLE, None, 0) +
            circle(100, 66, 50, BROWN) + path("M62,74 C62,44 92,40 100,58 C108,40 138,44 138,74 C138,104 120,112 100,112 C80,112 62,104 62,74 Z", MUZZLE) +
            eye(84, 70, 7) + eye(116, 70, 7) + ellipse(100, 88, 4, 3, NAVY, None, 0) + smile(100, 96, 14, 9, 4) +
            rect(44, 112, 22, 50, BROWN, 11) + rect(134, 112, 22, 50, BROWN, 11))


@asset("penguin")
def _():
    return (ellipse(76, 182, 22, 10, "#F7923A") + ellipse(124, 182, 22, 10, "#F7923A") +
            path("M52,94 Q30,130 46,150 Q58,140 60,120 Z", NAVY) + path("M148,94 Q170,130 154,150 Q142,140 140,120 Z", NAVY) +
            ellipse(100, 112, 54, 74, NAVY) + ellipse(100, 128, 38, 54, WHITE, None, 0) +
            path("M64,76 C64,52 86,52 100,64 C114,52 136,52 136,76 C136,98 116,104 100,100 C84,104 64,98 64,76 Z", WHITE, None, 0) +
            eye(86, 76, 6) + eye(114, 76, 6) + poly([(88, 90), (112, 90), (100, 106)], "#F7923A", NAVY, 3) +
            circle(76, 94, 5, PINK, None, 0) + circle(124, 94, 5, PINK, None, 0))


@asset("camel")
def _():
    out = ""
    for x in (52, 72, 128, 148):
        out += rect(x - 9, 120, 18, 64, TAN, 8)
    out += path("M30,128 C24,92 50,58 76,80 C88,40 110,40 116,74 C126,40 150,40 160,80 C176,96 172,130 160,134 L40,134 Z", TAN)
    out += path("M164,100 q20,6 22,30", "none", NAVY, 4)
    out += path("M44,110 C30,90 20,70 30,52 C34,40 22,30 14,36", "none", NAVY, 26) + path("M44,110 C30,90 20,70 30,52 C34,40 22,30 14,36", "none", TAN, 16)
    out += ellipse(20, 38, 22, 16, TAN) + eye(18, 32, 5) + circle(6, 44, 3, NAVY, None, 0) + ellipse(30, 22, 6, 9, TAN, NAVY, 3)
    out += rect(84, 60, 48, 22, CORAL, 8) + path("M90,71 h36", "none", YELLOW, 4)
    return out


@asset("frog")
def _():
    return (ellipse(56, 168, 34, 16, GREEN) + ellipse(144, 168, 34, 16, GREEN) +
            ellipse(100, 128, 66, 54, GREEN) + ellipse(100, 140, 40, 34, "#D6F0A8", None, 0) +
            circle(66, 70, 26, GREEN) + circle(134, 70, 26, GREEN) + circle(66, 70, 15, WHITE) + circle(134, 70, 15, WHITE) +
            eye(68, 72, 7) + eye(132, 72, 7) + path("M66,108 Q100,136 134,108", "none", NAVY, 5) +
            circle(52, 112, 7, PINK, None, 0) + circle(148, 112, 7, PINK, None, 0) +
            rect(60, 150, 18, 30, GREEN, 9) + rect(122, 150, 18, 30, GREEN, 9))


@asset("panda")
def _():
    return (ellipse(100, 150, 56, 44, WHITE) + ellipse(62, 176, 22, 16, NAVY) + ellipse(138, 176, 22, 16, NAVY) +
            rect(48, 120, 26, 40, NAVY, 13, None, 0) + rect(126, 120, 26, 40, NAVY, 13, None, 0) +
            circle(56, 44, 20, NAVY) + circle(144, 44, 20, NAVY) + circle(100, 80, 54, WHITE) +
            ellipse(78, 78, 15, 19, NAVY, None, 0) + ellipse(122, 78, 15, 19, NAVY, None, 0) +
            circle(80, 76, 6, WHITE, None, 0) + circle(120, 76, 6, WHITE, None, 0) +
            ellipse(100, 98, 9, 6, NAVY, None, 0) + smile(100, 106, 10, 7, 4) +
            circle(66, 100, 7, PINK, None, 0) + circle(134, 100, 7, PINK, None, 0))


@asset("bee")
def _():
    return (ellipse(80, 54, 30, 38, "#E9F7FD") + ellipse(120, 54, 30, 38, "#E9F7FD") +
            ellipse(100, 120, 62, 50, YELLOW) +
            path("M80,74 Q72,120 80,166", "none", NAVY, 14) + path("M116,72 Q108,120 116,168", "none", NAVY, 14) +
            poly([(160, 116), (186, 120), (160, 128)], NAVY, NAVY, 3) +
            circle(52, 110, 26, YELLOW) + eye(46, 104, 6) + smile(48, 120, 10, 6, 4) + circle(36, 120, 5, PINK, None, 0) +
            path("M44,86 q-8,-20 -20,-24 M58,84 q4,-20 16,-26", "none", NAVY, 4) + circle(24, 62, 5, NAVY, None, 0) + circle(74, 58, 5, NAVY, None, 0))


@asset("squirrel")
def _():
    return (path("M118,170 C190,170 196,90 166,60 C150,44 128,54 140,74 C160,96 150,132 118,140 Z", "#D98A4E") +
            path("M150,70 C166,90 162,120 140,138", "none", "#F0B07A", 8) +
            ellipse(92, 140, 40, 42, "#D98A4E") + ellipse(88, 148, 24, 28, MUZZLE, None, 0) +
            poly([(56, 40), (66, 66), (46, 62)], "#D98A4E", NAVY, 4) + poly([(108, 38), (112, 66), (94, 60)], "#D98A4E", NAVY, 4) +
            circle(80, 80, 38, "#D98A4E") + ellipse(70, 92, 20, 16, MUZZLE, None, 0) +
            eye(66, 74, 6) + eye(94, 74, 6) + circle(66, 90, 4, NAVY, None, 0) + smile(70, 98, 8, 5, 3.5) +
            ellipse(70, 180, 20, 9, "#D98A4E") + ellipse(110, 180, 20, 9, "#D98A4E"))


def rabbit(ears=True):
    out = ""
    if ears:
        out += ellipse(80, 50, 15, 40, WHITE) + ellipse(80, 54, 7, 28, PINK, None, 0)
        out += ellipse(120, 50, 15, 40, WHITE) + ellipse(120, 54, 7, 28, PINK, None, 0)
    out += ellipse(100, 160, 46, 34, WHITE) + circle(146, 168, 12, WHITE)
    out += circle(100, 116, 40, WHITE) + eye(86, 110, 6) + eye(114, 110, 6)
    out += path("M95,124 h10 l-5,6 Z", PINK, NAVY, 3) + path("M92,134 q8,6 16,0", "none", NAVY, 3.5)
    out += circle(76, 128, 6, PINK, None, 0) + circle(124, 128, 6, PINK, None, 0)
    out += ellipse(80, 190, 16, 8, WHITE) + ellipse(120, 190, 16, 8, WHITE)
    return out


@asset("rabbit")
def _():
    return rabbit(True)


@asset("rabbit_noears")
def _():
    return rabbit(False) + path("M64,60 C70,20 90,20 96,74 M104,74 C110,20 130,20 136,60", "none", "#9FB0BD", 4).replace("/>", ' stroke-dasharray="8 7"/>')


@asset("part_rabbit_ears")
def _():
    return (ellipse(76, 100, 22, 74, WHITE, NAVY, 6) + ellipse(76, 106, 10, 52, PINK, None, 0) +
            ellipse(124, 100, 22, 74, WHITE, NAVY, 6) + ellipse(124, 106, 10, 52, PINK, None, 0) +
            rect(50, 160, 100, 22, WHITE, 11))


def fox(tail=True):
    out = ""
    if tail:
        out += path("M140,150 C190,150 196,92 172,70 C176,106 156,124 132,128 Z", "#F7923A")
        out += path("M172,70 C180,84 180,96 176,108 C186,100 188,86 172,70 Z", WHITE, NAVY, 4)
    out += rect(56, 150, 18, 34, "#F7923A", 8) + rect(112, 150, 18, 34, "#F7923A", 8)
    out += ellipse(94, 140, 52, 36, "#F7923A") + ellipse(84, 150, 24, 20, WHITE, None, 0)
    out += poly([(30, 30), (56, 64), (26, 72)], "#F7923A", NAVY, 5) + poly([(98, 26), (96, 66), (70, 54)], "#F7923A", NAVY, 5)
    out += path("M26,70 C26,50 50,42 64,48 C80,42 102,52 100,70 C98,92 76,108 62,118 C48,108 26,92 26,70 Z", "#F7923A")
    out += path("M40,92 C50,104 56,110 62,118 C68,110 76,104 86,92 C76,96 70,96 62,98 C54,96 48,96 40,92 Z", WHITE, None, 0)
    out += eye(48, 74, 5.5) + eye(78, 74, 5.5) + circle(62, 112, 6, NAVY, None, 0)
    return out


@asset("fox")
def _():
    return fox(True)


@asset("fox_notail")
def _():
    return fox(False) + path("M140,150 C190,150 196,92 172,70 C176,106 156,124 132,128", "none", "#9FB0BD", 4).replace("/>", ' stroke-dasharray="8 7"/>')


@asset("part_fox_tail")
def _():
    return (path("M30,160 C120,170 186,100 150,30 C150,96 96,128 30,128 Z", "#F7923A", NAVY, 6) +
            path("M150,30 C164,54 168,78 160,100 C182,84 184,52 150,30 Z", WHITE, NAVY, 5))


def elephant(trunk=True):
    out = ""
    for x in (70, 96, 134, 158):
        out += rect(x - 12, 130, 24, 50, LGREY, 10)
    out += ellipse(118, 112, 66, 50, LGREY) + path("M182,104 q14,6 10,24", "none", NAVY, 4)
    out += ellipse(70, 92, 36, 42, "#C6D0D8") + ellipse(70, 92, 22, 28, PINK, None, 0)
    out += circle(52, 82, 34, LGREY)
    if trunk:
        out += path("M28,92 C14,110 10,140 22,160 C30,166 38,160 34,152 C28,136 34,118 42,104", LGREY, NAVY, 6)
    out += eye(48, 74, 6) + circle(62, 96, 6, PINK, None, 0)
    return out


@asset("elephant")
def _():
    return elephant(True)


@asset("elephant_notrunk")
def _():
    return elephant(False) + path("M28,92 C14,110 10,140 22,160 C30,166 38,160 34,152 C28,136 34,118 42,104", "none", "#9FB0BD", 4).replace("/>", ' stroke-dasharray="8 7"/>')


@asset("part_elephant_trunk")
def _():
    return (path("M120,30 C70,40 50,90 60,150 C66,182 100,178 96,154 C88,110 104,74 140,62 Z", LGREY, NAVY, 6) +
            path("M70,110 q10,-2 18,4 M68,130 q10,-2 18,4", "none", DGREY, 3))


@asset("hen")
def _():
    return (path("M52,172 v18 M44,190 h18 M112,172 v18 M104,190 h18", "none", "#F7923A", 6) +
            path("M150,70 C176,60 186,96 166,112 C186,110 186,134 164,140", WHITE, NAVY, 6) +
            ellipse(96, 124, 66, 52, WHITE) + path("M88,110 q30,-6 48,18 q-30,20 -48,-18 Z", "#F4F0E6", NAVY, 4) +
            circle(56, 70, 34, WHITE) + path("M42,36 q6,-14 14,-2 q6,-14 14,0 q8,-10 12,6 Z", CORAL, NAVY, 4) +
            poly([(22, 70), (6, 78), (22, 86)], "#F7923A", NAVY, 4) + ellipse(30, 96, 7, 10, CORAL, NAVY, 3) + eye(50, 66, 6))


@asset("pig")
def _():
    return (rect(58, 140, 20, 40, PINK, 8) + rect(128, 140, 20, 40, PINK, 8) +
            path("M168,110 q22,-6 14,14 q-8,8 4,14", "none", NAVY, 4) +
            ellipse(110, 120, 66, 46, PINK) + poly([(46, 52), (62, 80), (36, 84)], PINK, NAVY, 5) + poly([(96, 50), (92, 82), (70, 72)], PINK, NAVY, 5) +
            circle(66, 100, 38, PINK) + ellipse(56, 114, 18, 13, "#F49CC0") + circle(50, 114, 3.5, NAVY, None, 0) + circle(62, 114, 3.5, NAVY, None, 0) +
            eye(52, 88, 5.5) + eye(82, 88, 5.5) + circle(90, 108, 6, "#F49CC0", None, 0))


@asset("duck")
def _():
    return (path("M150,96 L186,78 L170,110 Z", YELLOW, NAVY, 5) +
            path("M40,120 C40,84 90,92 112,104 C140,84 176,96 170,122 C166,160 120,170 90,166 C56,164 40,146 40,120 Z", YELLOW) +
            path("M86,124 q26,-10 46,8 q-22,18 -46,-8 Z", "#FFE58C", NAVY, 4) +
            circle(62, 70, 32, YELLOW) + path("M24,74 q-18,0 -18,8 q16,8 30,4 Z", "#F7923A", NAVY, 4) + eye(58, 64, 6) +
            circle(74, 82, 6, PINK, None, 0))


@asset("octopus")
def _():
    out = ""
    for i, x in enumerate((40, 70, 100, 130, 160)):
        out += path(f"M{x},{120} q{-12 if i % 2 else 12},30 0,52 q8,8 14,-2", "none", NAVY, 18)
        out += path(f"M{x},{120} q{-12 if i % 2 else 12},30 0,52 q8,8 14,-2", "none", "#B58BE0", 10)
    out += path("M30,120 C20,40 180,40 170,120 Z", "#B58BE0")
    out += eye(78, 92, 8) + eye(122, 92, 8) + smile(100, 108, 14, 9, 4)
    out += circle(64, 110, 7, PINK, None, 0) + circle(136, 110, 7, PINK, None, 0) + circle(86, 60, 6, "#D4BDF0", None, 0)
    return out


@asset("turtle")
def _():
    return (ellipse(48, 150, 22, 12, "#8FD28E") + ellipse(150, 150, 22, 12, "#8FD28E") +
            ellipse(56, 92, 20, 12, "#8FD28E") + ellipse(144, 92, 20, 12, "#8FD28E") +
            circle(34, 120, 22, "#8FD28E") + eye(28, 114, 5) + smile(28, 126, 6, 4, 3) +
            path("M50,126 C50,70 150,70 170,126 Z", GREEN) + path("M80,92 l22,-6 l20,8 l2,22 l-22,8 l-22,-10 Z", "#7FCF6A", NAVY, 4) +
            rect(46, 120, 128, 14, "#CDEB9E", 7))


@asset("crab")
def _():
    return (path("M40,120 l-22,24 M50,134 l-14,30 M160,120 l22,24 M150,134 l14,30", "none", NAVY, 8) +
            path("M60,100 L40,60 M140,100 L160,60", "none", NAVY, 8) +
            circle(36, 50, 20, CORAL) + poly([(30, 30), (36, 52), (48, 36)], WHITE, NAVY, 3) +
            circle(164, 50, 20, CORAL) + poly([(170, 30), (164, 52), (152, 36)], WHITE, NAVY, 3) +
            ellipse(100, 124, 64, 42, CORAL) +
            line(84, 88, 80, 66, NAVY, 4) + line(116, 88, 120, 66, NAVY, 4) + circle(80, 62, 9, WHITE) + eye(80, 62, 4.5) + circle(120, 62, 9, WHITE) + eye(120, 62, 4.5) +
            smile(100, 128, 14, 9, 4))


@asset("teddy", 200, 300)
def _():
    return (circle(52, 40, 22, BROWN) + circle(52, 40, 11, TAN, None, 0) + circle(148, 40, 22, BROWN) + circle(148, 40, 11, TAN, None, 0) +
            rect(14, 130, 36, 80, BROWN, 18) + rect(150, 130, 36, 80, BROWN, 18) +
            rect(50, 230, 40, 56, BROWN, 18) + rect(110, 230, 40, 56, BROWN, 18) +
            ellipse(100, 186, 62, 72, BROWN) + ellipse(100, 192, 38, 46, TAN, None, 0) +
            circle(100, 80, 56, BROWN) + ellipse(100, 98, 24, 18, TAN) + ellipse(100, 92, 9, 6, NAVY, None, 0) +
            eye(78, 72, 6.5) + eye(122, 72, 6.5) + smile(100, 104, 10, 7, 4) +
            circle(66, 96, 7, PINK, None, 0) + circle(134, 96, 7, PINK, None, 0))



@asset("monster", 260, 220)
def _():
    return (rect(70, 186, 36, 30, LIME, 14) + rect(154, 186, 36, 30, LIME, 14) +
            poly([(70, 40), (60, 6), (94, 30)], YELLOW, NAVY, 5) + poly([(190, 40), (200, 6), (166, 30)], YELLOW, NAVY, 5) +
            rect(30, 24, 200, 176, LIME, 90) +
            circle(96, 74, 26, WHITE) + eye(98, 76, 11) + circle(164, 74, 26, WHITE) + eye(162, 76, 11) +
            path("M70,120 Q130,190 190,120 Z", CORAL, NAVY, 6) + ellipse(130, 150, 22, 9, PINK, None, 0) +
            poly([(96, 122), (108, 122), (102, 134)], WHITE, NAVY, 3) + poly([(152, 122), (164, 122), (158, 134)], WHITE, NAVY, 3) +
            circle(62, 112, 10, PINK, None, 0) + circle(198, 112, 10, PINK, None, 0) +
            circle(40, 150, 8, "#8CC63F", None, 0) + circle(216, 170, 6, "#8CC63F", None, 0))


@asset("cookie")
def _():
    return (circle(100, 100, 76, "#E9B872", NAVY, 7) +
            "".join(ellipse(x, y, 9, 7, DBROWN, None, 0) for x, y in ((70, 70), (120, 64), (138, 110), (90, 120), (60, 128), (112, 150))))


@asset("plate", 300, 120)
def _():
    return ellipse(150, 60, 140, 50, WHITE, NAVY, 6) + ellipse(150, 60, 104, 34, CREAM, NAVY, 3)


@asset("cupcake")
def _():
    return (poly([(48, 104), (152, 104), (138, 184), (62, 184)], SKY, NAVY, 6) +
            path("M70,108 L76,184 M100,108 V184 M130,108 L124,184", "none", "#3FA9E0", 4) +
            blob([(66, 96, 26), (100, 76, 34), (134, 96, 26), (100, 100, 30)], PINK) +
            circle(100, 40, 12, CORAL) + path("M76,90 l6,-4 M112,84 l6,4 M96,64 l2,6 M130,98 l-4,6", "none", WHITE, 5))


@asset("balloon")
def _():
    return (path("M100,150 C94,166 108,176 100,196", "none", NAVY, 3) +
            ellipse(100, 82, 54, 66, CORAL) + poly([(92, 152), (108, 152), (100, 142)], CORAL, NAVY, 4) +
            path("M72,56 q8,-18 24,-22", "none", WHITE, 7))


BALLOON_COLS = [CORAL, SKY, YELLOW, LIME, PINK, "#9B6BD3", "#F7923A", "#3FA9E0", "#6CC04A", "#E8473B"]


def balloon_one(col):
    return (path("M100,150 C94,166 108,176 100,196", "none", NAVY, 3) +
            ellipse(100, 82, 54, 66, col) + poly([(92, 152), (108, 152), (100, 142)], col, NAVY, 4) +
            path("M72,56 q8,-18 24,-22", "none", WHITE, 7))


for _i, _col in enumerate(BALLOON_COLS):
    reg(f"balloon_{_i}", (lambda col=_col: (lambda: svg_doc(balloon_one(col), 200, 200)))())


@asset("apple")
def _():
    return (path("M100,54 C80,34 30,40 30,96 C30,150 70,186 100,170 C130,186 170,150 170,96 C170,40 120,34 100,54 Z", "#E8473B") +
            path("M100,56 Q98,34 110,18", "none", BROWN, 7) + path(leaf_d(126, 34, 16).replace(" Z", " Z"), GREEN, NAVY, 4) +
            path("M54,86 q4,-20 22,-26", "none", WHITE, 7))


@asset("star_item")
def _():
    return star(100, 106, 84, YELLOW, NAVY, 7, r=40) + path("M70,96 l8,-14", "none", WHITE, 6)


@asset("banana")
def _():
    return (path("M40,52 C30,120 90,180 170,150 C176,144 172,138 164,138 C100,148 64,110 58,52 Z", YELLOW, NAVY, 6) +
            path("M36,40 L52,56", "none", BROWN, 10) + path("M70,96 C82,120 110,136 140,140", "none", "#E8B92F", 4))


@asset("bamboo")
def _():
    out = ""
    for x, h in ((64, 160), (110, 176), (146, 140)):
        out += rect(x - 12, 190 - h, 24, h, "#9DD66A", 8)
        for y in range(190 - h + 40, 190, 44):
            out += line(x - 12, y, x + 12, y, NAVY, 4)
    out += path(leaf_d(88, 50, 18), GREEN, NAVY, 4) + path(leaf_d(170, 64, 16), GREEN, NAVY, 4)
    return out


@asset("acorn")
def _():
    return (ellipse(100, 120, 44, 56, "#C98A4B") + path("M48,92 C48,52 152,52 152,92 Z", DBROWN) +
            path("M100,56 q6,-20 16,-24", "none", DBROWN, 7) + path("M76,110 q2,20 14,32", "none", WHITE, 6))


@asset("grass")
def _():
    out = ""
    for i in range(9):
        x = 30 + i * 18
        out += path(f"M{x},{180} Q{x + (8 if i % 2 else -8)},{110} {x + (14 if i % 2 else -10)},{60 + (i % 3) * 20}", "none", NAVY, 12)
        out += path(f"M{x},{180} Q{x + (8 if i % 2 else -8)},{110} {x + (14 if i % 2 else -10)},{60 + (i % 3) * 20}", "none", GREEN, 6)
    return out + rect(20, 170, 160, 18, "#8CC63F", 8)


@asset("carrot")
def _():
    return (path("M90,40 q-24,-30 -40,-20 M100,40 q0,-34 12,-36 M110,40 q24,-28 40,-16", "none", DGREEN, 9) +
            path("M70,44 C70,36 130,36 130,44 C130,90 112,150 100,186 C88,150 70,90 70,44 Z", "#F7923A") +
            path("M80,70 h14 M106,96 h12 M84,120 h14", "none", "#C96A1F", 4))


@asset("bread")
def _():
    return (path("M30,90 C30,50 170,50 170,90 L170,160 C170,170 30,170 30,160 Z", "#E9B872") +
            path("M60,74 l14,20 M94,68 l14,20 M128,72 l14,20", "none", "#B27B3B", 5) +
            path("M30,120 h140", "none", "#D9A55C", 4))


@asset("croissant")
def _():
    return (path("M20,128 C30,80 70,62 100,62 C130,62 170,80 180,128 C160,140 150,120 140,116 C130,140 70,140 60,116 C50,120 40,140 20,128 Z", "#E9A85C") +
            path("M70,72 L76,124 M100,64 V128 M130,72 L124,124", "none", "#B27B3B", 4))


@asset("milk")
def _():
    return (poly([(56, 60), (144, 60), (144, 186), (56, 186)], WHITE, NAVY, 6) + poly([(56, 60), (78, 22), (122, 22), (144, 60)], SKY, NAVY, 6) +
            rect(84, 8, 32, 18, SKY, 4) + rect(56, 96, 88, 52, SKY, 0) + path("M78,122 q10,-14 22,0 q10,14 22,0", "none", WHITE, 5))


@asset("cheese")
def _():
    return (poly([(20, 140), (180, 140), (180, 90), (20, 140)], "#FFE36E", NAVY, 6) +
            poly([(20, 140), (180, 90), (180, 170), (20, 170)], "#FFD348", NAVY, 6) +
            circle(70, 152, 8, "#F2B92E", None, 0) + circle(130, 128, 10, "#F2B92E", None, 0) + circle(150, 156, 7, "#F2B92E", None, 0))


@asset("lettuce")
def _():
    return (path("M18,120 C30,80 50,110 62,80 C76,108 90,72 104,96 C118,70 132,108 146,80 C158,108 172,84 182,120 C170,150 30,150 18,120 Z", "#8CD46A") +
            path("M40,120 q60,-26 120,0", "none", "#5DBB63", 4))


@asset("tomato_slices")
def _():
    out = ""
    for cx in (62, 138):
        out += circle(cx, 100, 46, "#E8473B") + circle(cx, 100, 34, "#F7766A", NAVY, 3)
        for a in range(0, 360, 72):
            out += ellipse(cx + 18 * math.cos(math.radians(a)), 100 + 18 * math.sin(math.radians(a)), 5, 7, "#FFE3A3", None, 0)
    return out


@asset("cheese_slice")
def _():
    return rect(26, 50, 148, 100, "#FFD348", 8) + circle(70, 86, 10, "#F2B92E", None, 0) + circle(126, 118, 12, "#F2B92E", None, 0) + circle(140, 74, 7, "#F2B92E", None, 0)


@asset("bread_slice")
def _():
    return path("M30,100 C10,60 40,30 70,40 C90,20 110,20 130,40 C160,30 190,60 170,100 L170,170 L30,170 Z", "#E9B872") + \
        path("M46,96 C36,70 54,54 74,60 C90,44 110,44 126,60 C146,54 164,70 154,96 L154,156 L46,156 Z", "#FBE3B5", None, 0)


@asset("sandwich", 200, 200)
def _():
    return (rect(30, 140, 140, 30, "#E9B872", 12) + path("M24,132 C40,112 60,140 76,118 C92,140 110,112 126,132 C142,112 160,140 176,124 L176,142 L24,142 Z", "#8CD46A") +
            rect(30, 104, 140, 22, "#FFD348", 6) + rect(36, 80, 128, 20, "#E8473B", 10) +
            path("M30,76 C30,30 170,30 170,76 Z", "#E9B872"))


# ------------------------------------------------------------------ vehicles
@asset("car")
def _():
    return (path("M20,130 L20,104 C20,92 32,86 44,86 L62,86 L82,54 L138,54 L160,86 L170,86 C182,86 186,96 186,108 L186,130 Z", CORAL) +
            poly([(90, 64), (108, 64), (108, 86), (76, 86)], WATER, NAVY, 4) + poly([(118, 64), (134, 64), (148, 86), (118, 86)], WATER, NAVY, 4) +
            circle(58, 134, 22, NAVY) + circle(58, 134, 9, LGREY, None, 0) + circle(150, 134, 22, NAVY) + circle(150, 134, 9, LGREY, None, 0) +
            rect(172, 100, 12, 10, YELLOW, 4, NAVY, 3))


@asset("train")
def _():
    return (rect(100, 40, 70, 90, SKY, 10) + rect(112, 54, 46, 32, WATER, 6, NAVY, 4) + rect(20, 80, 90, 50, CORAL, 10) +
            rect(40, 44, 26, 38, NAVY, 6) + rect(34, 34, 38, 14, CORAL, 6) +
            circle(48, 142, 18, NAVY) + circle(48, 142, 7, YELLOW, None, 0) + circle(98, 142, 18, NAVY) + circle(98, 142, 7, YELLOW, None, 0) +
            circle(146, 142, 18, NAVY) + circle(146, 142, 7, YELLOW, None, 0) + poly([(20, 120), (6, 150), (24, 150)], YELLOW, NAVY, 4) +
            circle(48, 20, 10, WHITE, LGREY, 3) + circle(66, 12, 7, WHITE, LGREY, 3))


@asset("boat")
def _():
    return (path("M100,20 L100,120", "none", NAVY, 6) + poly([(104, 26), (168, 110), (104, 110)], WHITE, NAVY, 6) +
            poly([(96, 40), (96, 110), (46, 110)], YELLOW, NAVY, 6) +
            path("M20,124 L180,124 L156,168 L44,168 Z", CORAL) + circle(70, 146, 7, WHITE, NAVY, 3) + circle(100, 146, 7, WHITE, NAVY, 3) + circle(130, 146, 7, WHITE, NAVY, 3) +
            path("M100,22 l22,8 l-22,8", YELLOW, NAVY, 3))


@asset("plane")
def _():
    return (path("M20,104 C20,88 40,80 60,80 L160,80 C180,80 192,92 192,104 C192,116 180,124 160,124 L60,124 C40,124 20,116 20,104 Z", WHITE) +
            poly([(84, 84), (120, 84), (82, 22), (64, 22)], SKY, NAVY, 5) + poly([(84, 120), (120, 120), (82, 182), (64, 182)], SKY, NAVY, 5) +
            poly([(24, 96), (14, 58), (36, 58), (50, 88)], CORAL, NAVY, 5) +
            "".join(circle(x, 100, 6, WATER, NAVY, 3) for x in (100, 122, 144)) + path("M168,90 q14,2 16,12 h-16 Z", WATER, NAVY, 3))


# ------------------------------------------------------------------ household / routine / clothes
@asset("toothbrush")
def _():
    return g(rect(14, 92, 130, 26, SKY, 13) + rect(132, 86, 56, 38, SKY, 12) + rect(136, 46, 48, 44, WHITE, 6) +
             path("M148,52 v32 M160,52 v32 M172,52 v32", "none", LIME, 6) + circle(40, 105, 6, WHITE, None, 0),
             t="rotate(-18 100 100)")


@asset("pillow")
def _():
    return (path("M24,60 C24,40 40,36 60,44 C90,52 110,52 140,44 C160,36 176,40 176,60 L176,140 C176,160 160,164 140,156 C110,148 90,148 60,156 C40,164 24,160 24,140 Z", "#CFC2F2") +
            star(100, 100, 24, YELLOW, NAVY, 4) + circle(56, 80, 5, WHITE, None, 0) + circle(146, 126, 5, WHITE, None, 0))


@asset("saucepan")
def _():
    return (rect(130, 84, 66, 18, DGREY, 9) + rect(20, 70, 120, 90, LGREY, 16) + rect(14, 64, 132, 18, GREY, 9) +
            path("M50,40 q-8,-14 0,-24 M80,40 q-8,-14 0,-24 M110,40 q-8,-14 0,-24", "none", GREY, 5))


@asset("sunhat")
def _():
    return (ellipse(100, 130, 92, 34, YELLOW) + path("M48,124 C48,60 152,60 152,124 Z", YELLOW) +
            path("M50,112 C80,124 120,124 150,112 L150,124 C120,134 80,134 50,124 Z", CORAL, NAVY, 4) + circle(132, 106, 10, PINK, NAVY, 3))


@asset("rainboots")
def _():
    out = ""
    for x in (24, 104):
        out += path(f"M{x + 6},30 L{x + 50},30 L{x + 50},140 L{x + 72},150 C{x + 76},166 {x + 70},176 {x + 60},176 L{x + 6},176 Z", YELLOW)
        out += rect(x, 24, 56, 18, "#F2B92E", 8) + path(f"M{x + 6},156 h{x + 70 - x - 6}", "none", NAVY, 4)
    return out


@asset("scarf")
def _():
    return (path("M30,60 C70,90 130,90 170,60 L170,92 C130,120 70,120 30,92 Z", CORAL) +
            rect(110, 90, 40, 96, CORAL, 10) + path("M110,120 h40 M110,148 h40", "none", WHITE, 7) +
            path("M114,186 v12 M126,186 v12 M138,186 v12 M148,186 v12", "none", NAVY, 4) +
            path("M60,78 l0,26 M90,86 l0,26", "none", WHITE, 7))


@asset("beanie")
def _():
    return (path("M36,140 C36,60 164,60 164,140 Z", SKY) + rect(28, 128, 144, 34, "#3FA9E0", 14) +
            circle(100, 52, 20, WHITE) + path("M52,140 v18 M76,140 v18 M100,140 v18 M124,140 v18 M148,140 v18", "none", NAVY, 3))


@asset("jumper")
def _():
    return (path("M66,30 L134,30 L186,62 L170,104 L150,94 L150,180 L50,180 L50,94 L30,104 L14,62 Z", LIME) +
            path("M80,30 Q100,52 120,30", "none", NAVY, 5) + path("M50,150 h100", "none", "#7EBF2E", 8) + star(100, 104, 20, YELLOW, NAVY, 4))


@asset("teddy_boots")
def _():
    out = ""
    for x in (20, 108):
        out += path(f"M{x},40 L{x + 52},40 L{x + 52},130 C{x + 74},130 {x + 76},170 {x + 60},170 L{x},170 Z", CORAL)
        out += rect(x - 4, 36, 60, 22, "#F7B6D2", 10)
    return out


@asset("teddy_hat")
def _():
    return (rect(16, 140, 168, 26, NAVY, 13) + rect(44, 50, 112, 100, "#9B6BD3", 14) + rect(44, 112, 112, 22, YELLOW, 0) +
            star(150, 64, 14, YELLOW, NAVY, 3))


@asset("tshirt")
def _():
    return (path("M66,30 L134,30 L180,62 L162,96 L146,86 L146,176 L54,176 L54,86 L38,96 L20,62 Z", SKY) +
            path("M80,30 Q100,50 120,30", "none", NAVY, 5) + heart(100, 112, 18, CORAL, NAVY, 4))


@asset("rt_wake")
def _():
    return (path("M10,170 C40,120 160,120 190,170 Z", "#FFE9A8") + circle(100, 150, 46, YELLOW) +
            "".join(line(100 + 60 * math.cos(math.radians(a)), 150 + 60 * math.sin(math.radians(a)),
                         100 + 80 * math.cos(math.radians(a)), 150 + 80 * math.sin(math.radians(a)), "#F2B92E", 7) for a in range(200, 345, 28)) +
            rect(0, 168, 200, 30, LIME, 0) + circle(150, 70, 30, WHITE) + circle(150, 70, 30, "none", CORAL, 8) +
            line(150, 70, 150, 54, NAVY, 5) + line(150, 70, 162, 76, NAVY, 5) + circle(126, 44, 9, CORAL) + circle(174, 44, 9, CORAL) +
            happy_eye(84, 146, 8) + happy_eye(116, 146, 8) + smile(100, 160, 10, 7, 4))


@asset("rt_wash")
def _():
    return (rect(30, 20, 26, 60, LGREY, 8) + rect(30, 20, 90, 22, LGREY, 10) + path("M110,42 v20", "none", NAVY, 6) +
            path("M110,66 q-8,14 0,20 q8,-6 0,-20 Z", SKY, NAVY, 3) +
            rect(40, 130, 120, 50, PINK, 18) + circle(140, 114, 16, WHITE, SKY, 4) + circle(116, 104, 11, WHITE, SKY, 4) + circle(160, 92, 9, WHITE, SKY, 4) +
            rect(50, 140, 60, 28, WHITE, 10, NAVY, 3))


@asset("rt_brush")
def _():
    return (rect(30, 100, 60, 84, SKY, 12) + rect(36, 92, 48, 18, "#3FA9E0", 6) +
            g(rect(60, 40, 18, 110, LIME, 9) + rect(56, 22, 26, 30, WHITE, 6), t="rotate(-12 69 90)") +
            rect(110, 120, 70, 30, WHITE, 12) + rect(170, 126, 20, 18, CORAL, 4) + path("M110,135 c-16,-4 -18,-24 -4,-28", "none", SKY, 10))


@asset("rt_dress")
def _():
    return (path("M46,20 L94,20 L126,42 L114,66 L102,60 L102,120 L38,120 L38,60 L26,66 L14,42 Z", SKY) + heart(70, 72, 14, CORAL, NAVY, 3) +
            path("M110,110 L180,110 L184,186 L150,186 L146,140 L144,186 L108,186 Z", "#9B6BD3") +
            ellipse(60, 172, 26, 14, CORAL) + path("M40,166 h40", "none", WHITE, 3))


# ------------------------------------------------------------------ faces / emotions
FACE_COL = {"happy": YELLOW, "sad": SKY, "surprised": PINK, "sleepy": "#CFC2F2", "cross": "#F9A04B", "worried": LIME}


def feeling_face(kind):
    col = FACE_COL[kind]
    out = circle(100, 100, 82, col, NAVY, 7)
    if kind == "happy":
        out += happy_eye(70, 86, 12, 6) + happy_eye(130, 86, 12, 6) + path("M60,118 Q100,170 140,118 Z", CORAL, NAVY, 6)
    elif kind == "sad":
        out += eye(70, 88, 9) + eye(130, 88, 9) + path("M68,146 Q100,116 132,146", "none", NAVY, 7) + path(drop_d(146, 112, 12), WHITE, NAVY, 3)
        out += path("M54,66 l26,-8 M146,66 l-26,-8", "none", NAVY, 5)
    elif kind == "surprised":
        out += circle(70, 84, 15, WHITE, NAVY, 5) + eye(70, 86, 6) + circle(130, 84, 15, WHITE, NAVY, 5) + eye(130, 86, 6)
        out += ellipse(100, 138, 16, 20, CORAL, NAVY, 6) + path("M56,58 q14,-12 28,0 M116,58 q14,-12 28,0", "none", NAVY, 5)
    elif kind == "sleepy":
        out += path("M56,90 q14,10 28,0 M116,90 q14,10 28,0", "none", NAVY, 6) + ellipse(100, 134, 10, 8, CORAL, NAVY, 5)
        out += path("M150,40 h18 l-18,18 h18", "none", NAVY, 5)
    elif kind == "cross":
        out += eye(70, 92, 9) + eye(130, 92, 9) + path("M52,64 l32,14 M148,64 l-32,14", "none", NAVY, 7)
        out += path("M70,142 q30,-16 60,0", "none", NAVY, 7)
    elif kind == "worried":
        out += eye(70, 92, 9) + eye(130, 92, 9) + path("M54,72 l28,-12 M146,72 l-28,-12", "none", NAVY, 5)
        out += path("M66,140 q12,-10 22,0 t22,0 t22,0", "none", NAVY, 6)
    if kind not in ("cross",):
        out += circle(48, 116, 9, PINK if col != PINK else CORAL, None, 0) + circle(152, 116, 9, PINK if col != PINK else CORAL, None, 0)
    return out


for _k in FACE_COL:
    reg(f"face_{_k}", (lambda k=_k: (lambda: svg_doc(feeling_face(k), 200, 200)))())


@asset("face_blank", 300, 300)
def _():
    out = ""
    mane = [(150 + 120 * math.cos(math.radians(a)), 160 + 116 * math.sin(math.radians(a)), 36) for a in range(0, 360, 24)]
    out += blob(mane, MANE)
    out += circle(70, 66, 30, GOLD) + circle(70, 66, 15, PINK, None, 0) + circle(230, 66, 30, GOLD) + circle(230, 66, 15, PINK, None, 0)
    out += circle(150, 160, 108, GOLD)
    out += circle(84, 190, 14, PINK, None, 0) + circle(216, 190, 14, PINK, None, 0)
    out += path("M138,170 Q150,164 162,170 Q150,184 138,170 Z", BROWN, NAVY, 4)
    return out


@asset("eyes_round")
def _():
    return circle(56, 100, 34, WHITE, NAVY, 6) + eye(60, 104, 15) + circle(144, 100, 34, WHITE, NAVY, 6) + eye(140, 104, 15)


@asset("eyes_happy")
def _():
    return path("M26,112 Q56,62 86,112", "none", NAVY, 11) + path("M114,112 Q144,62 174,112", "none", NAVY, 11)


@asset("mouth_smile")
def _():
    return path("M26,80 Q100,190 174,80 Z", CORAL, NAVY, 7) + ellipse(100, 126, 32, 12, PINK, None, 0)


@asset("mouth_o")
def _():
    return ellipse(100, 100, 40, 52, CORAL, NAVY, 7) + ellipse(100, 120, 22, 12, PINK, None, 0)


@asset("mouth_wobbly")
def _():
    return path("M24,110 q19,-30 38,0 t38,0 t38,0 t38,0", "none", NAVY, 10)


# ------------------------------------------------------------------ kindness
@asset("k_blocks")
def _():
    return (g(rect(30, 120, 50, 50, CORAL, 8), t="rotate(-14 55 145)") + g(rect(90, 128, 46, 46, SKY, 8), t="rotate(10 113 151)") +
            g(rect(140, 110, 44, 44, YELLOW, 8), t="rotate(24 162 132)") + g(rect(60, 70, 44, 44, LIME, 8), t="rotate(30 82 92)") +
            path("M20,60 q10,-20 24,-10 M160,50 q14,-12 22,4", "none", NAVY, 4))


@asset("k_sad")
def _():
    return feeling_face("sad")


@asset("k_crayon")
def _():
    return (g(rect(60, 40, 40, 120, "#9B6BD3", 6) + poly([(60, 40), (100, 40), (80, 8)], "#E5D6F7", NAVY, 5), t="rotate(20 80 100)") +
            rect(100, 110, 84, 70, WHITE, 8) + path("M114,140 q14,-16 28,0 t28,0", "none", "#9B6BD3", 6))


@asset("k_fall")
def _():
    return (circle(100, 100, 74, MUZZLE) + rect(56, 86, 88, 30, WHITE, 12) + rect(84, 86, 32, 30, "#F4D7B8", 4, NAVY, 3) +
            "".join(circle(x, y, 3, NAVY, None, 0) for x, y in ((92, 96), (108, 96), (92, 106), (108, 106))))


@asset("k_tidy")
def _():
    return (rect(40, 110, 120, 70, TAN, 10) + rect(56, 70, 40, 40, CORAL, 8) + rect(104, 70, 40, 40, SKY, 8) + rect(80, 34, 40, 40, YELLOW, 8) +
            path("M30,140 q-10,-30 10,-40 M170,140 q10,-30 -10,-40", "none", NAVY, 5))


@asset("k_hug")
def _():
    return heart(100, 104, 70, PINK, NAVY, 7) + heart(100, 104, 34, CORAL, NAVY, 5)


@asset("k_share")
def _():
    return (g(rect(46, 40, 30, 110, "#9B6BD3", 6) + poly([(46, 40), (76, 40), (61, 14)], "#E5D6F7", NAVY, 4), t="rotate(-12 61 100)") +
            g(rect(124, 40, 30, 110, LIME, 6) + poly([(124, 40), (154, 40), (139, 14)], "#E6F5C7", NAVY, 4), t="rotate(12 139 100)") +
            heart(100, 170, 18, CORAL, NAVY, 4))


@asset("k_plaster")
def _():
    return (g(rect(20, 76, 160, 48, "#F4D7B8", 24) + rect(74, 76, 52, 48, "#FBE6D2", 4, NAVY, 3) +
              "".join(circle(x, y, 3, NAVY, None, 0) for x, y in ((88, 92), (112, 92), (88, 108), (112, 108))), t="rotate(-24 100 100)") +
            star(160, 40, 16, YELLOW, NAVY, 3))


# ------------------------------------------------------------------ backpack activity
@asset("backpack", 240, 260)
def _():
    return (rect(30, 50, 180, 200, LIME, 34) + path("M70,52 C70,10 170,10 170,52", "none", NAVY, 10) +
            rect(46, 30, 148, 70, YELLOW, 24) + rect(70, 150, 100, 70, "#8CC63F", 16) + circle(120, 92, 8, CORAL, NAVY, 3))


@asset("bottle")
def _():
    return rect(70, 50, 60, 136, SKY, 20) + rect(80, 20, 40, 34, CORAL, 8) + rect(70, 100, 60, 40, WHITE, 0) + path("M84,120 q16,-14 32,0", "none", SKY, 5)


@asset("lunchbox")
def _():
    return (rect(24, 70, 152, 100, CORAL, 18) + path("M74,70 C74,40 126,40 126,70", "none", NAVY, 9) + path("M24,104 H176", "none", NAVY, 5) +
            circle(100, 134, 16, YELLOW, NAVY, 4))


@asset("book")
def _():
    return (path("M100,48 C70,30 40,32 18,40 L18,168 C40,160 70,158 100,176 Z", SKY) +
            path("M100,48 C130,30 160,32 182,40 L182,168 C160,160 130,158 100,176 Z", YELLOW) +
            path("M36,70 q26,-6 48,4 M36,96 q26,-6 48,4 M116,74 q26,-10 48,-4", "none", WHITE, 5) + star(140, 116, 18, CORAL, NAVY, 3))


@asset("bathtub")
def _():
    return (rect(14, 80, 172, 70, WHITE, 26) + rect(8, 70, 184, 24, LGREY, 12) + rect(36, 150, 18, 30, GREY, 6) + rect(146, 150, 18, 30, GREY, 6) +
            circle(70, 60, 18, WHITE, SKY, 4) + circle(100, 44, 12, WHITE, SKY, 4) + circle(128, 60, 15, WHITE, SKY, 4) + path("M170,70 V30 h-20", "none", GREY, 7))


@asset("sofa")
def _():
    return (rect(30, 50, 140, 70, "#9B6BD3", 22) + rect(10, 90, 40, 80, "#8559BD", 18) + rect(150, 90, 40, 80, "#8559BD", 18) +
            rect(40, 110, 120, 50, "#B58BE0", 14) + rect(26, 166, 14, 18, NAVY, 4) + rect(160, 166, 14, 18, NAVY, 4))


@asset("piano")
def _():
    out = rect(20, 40, 160, 120, DBROWN, 12) + rect(32, 90, 136, 50, WHITE, 4, NAVY, 4)
    for i in range(1, 8):
        out += line(32 + 17 * i, 90, 32 + 17 * i, 140, NAVY, 3)
    for i in (1, 2, 4, 5, 6):
        out += rect(26 + 17 * i, 90, 10, 30, NAVY, 2, None, 0)
    return out + rect(30, 160, 14, 26, DBROWN, 4) + rect(156, 160, 14, 26, DBROWN, 4)


# ------------------------------------------------------------------ day / sequences / nature
@asset("sunrise")
def _():
    return (rect(0, 0, 200, 200, "#FFE7D1", 0, None, 0) + circle(100, 150, 50, "#F7923A") + rect(0, 140, 200, 60, LIME, 0) +
            "".join(line(100 + 64 * math.cos(math.radians(a)), 150 + 64 * math.sin(math.radians(a)),
                         100 + 86 * math.cos(math.radians(a)), 150 + 86 * math.sin(math.radians(a)), "#F7923A", 7) for a in range(200, 345, 34)))


@asset("sun")
def _():
    return ("".join(line(100 + 58 * math.cos(math.radians(a)), 100 + 58 * math.sin(math.radians(a)),
                         100 + 84 * math.cos(math.radians(a)), 100 + 84 * math.sin(math.radians(a)), "#F2B92E", 9) for a in range(0, 360, 45)) +
            circle(100, 100, 48, YELLOW) + happy_eye(84, 96, 7) + happy_eye(116, 96, 7) + smile(100, 112, 10, 8, 4) +
            circle(74, 112, 6, CORAL, None, 0) + circle(126, 112, 6, CORAL, None, 0))


@asset("moon")
def _():
    return (path("M120,26 C66,30 40,78 50,116 C62,162 116,184 160,160 C112,160 86,126 92,84 C96,56 110,38 120,26 Z", "#FFE36E") +
            star(150, 60, 14, YELLOW, NAVY, 3) + star(170, 110, 9, YELLOW, NAVY, 3) + path("M70,100 q8,8 16,0", "none", NAVY, 4))


@asset("breakfast")
def _():
    return (ellipse(100, 120, 84, 28, WHITE) + path("M20,110 C24,170 176,170 180,110 Z", SKY) + ellipse(100, 110, 78, 20, "#FFE9C6") +
            circle(70, 108, 8, "#E8473B", None, 0) + circle(98, 104, 8, "#9B6BD3", None, 0) + circle(124, 110, 8, "#E8473B", None, 0) +
            g(rect(130, 40, 14, 70, LGREY, 7), t="rotate(30 137 75)"))


@asset("slide")
def _():
    return (rect(30, 40, 14, 150, CORAL, 6) + rect(80, 40, 14, 150, CORAL, 6) + path("M36,70 h52 M36,100 h52 M36,130 h52", "none", NAVY, 6) +
            path("M90,46 C130,60 150,150 192,170 L182,190 C136,170 116,90 84,70 Z", YELLOW) + rect(20, 186, 176, 10, LIME, 5))


@asset("bedtime")
def _():
    return (rect(20, 100, 160, 60, SKY, 14) + rect(20, 70, 30, 110, "#3FA9E0", 10) + rect(56, 86, 50, 28, WHITE, 12) +
            rect(80, 112, 100, 40, "#CFC2F2", 12) + moon_small(160, 46))


def moon_small(cx, cy):
    return path(f"M{cx + 6},{cy - 26} C{cx - 24},{cy - 22} {cx - 30},{cy + 18} {cx - 4},{cy + 26} C{cx + 14},{cy + 30} {cx + 24},{cy + 20} {cx + 28},{cy + 12} C{cx},{cy + 14} {cx - 10},{cy - 10} {cx + 6},{cy - 26} Z", "#FFE36E", NAVY, 4)


@asset("park_lunch")
def _():
    return ASSETS["sandwich"]().split(">", 1)[1].rsplit("</svg>", 1)[0].split("</title>", 1)[-1]


@asset("seed")
def _():
    return rect(0, 140, 200, 60, "#B98A5E", 0, None, 0) + ellipse(100, 150, 22, 14, DBROWN) + path("M10,140 H190", "none", NAVY, 5)


@asset("sprout")
def _():
    return (rect(0, 140, 200, 60, "#B98A5E", 0, None, 0) + path("M100,140 V80", "none", DGREEN, 7) +
            path(leaf_d(78, 80, 20), GREEN, NAVY, 4).replace("<path", '<path transform="rotate(-60 78 80)"') +
            path(leaf_d(122, 74, 20), GREEN, NAVY, 4).replace("<path", '<path transform="rotate(60 122 74)"') + path("M10,140 H190", "none", NAVY, 5))


@asset("flower_grown")
def _():
    return rect(0, 160, 200, 40, "#B98A5E", 0, None, 0) + flower(100, 56, CORAL, 30, True) + path("M10,160 H190", "none", NAVY, 5)


@asset("egg")
def _():
    return ellipse(100, 108, 54, 70, "#FFF4DA")


@asset("egg_crack")
def _():
    return ellipse(100, 108, 54, 70, "#FFF4DA") + path("M48,96 l18,14 l14,-18 l16,18 l16,-16 l16,16 l20,-14", "none", NAVY, 5)


@asset("chick")
def _():
    return (ellipse(100, 120, 60, 54, YELLOW) + circle(100, 70, 38, YELLOW) + eye(86, 64, 6) + eye(114, 64, 6) +
            poly([(90, 80), (110, 80), (100, 94)], "#F7923A", NAVY, 3) + path("M60,120 q-20,-4 -24,10 q12,6 26,0", YELLOW, NAVY, 4) +
            path("M86,174 v14 M114,174 v14", "none", "#F7923A", 6) + path("M60,150 C60,190 140,190 140,150 L126,162 L114,148 L100,162 L86,148 L74,162 Z", "#FFF4DA", NAVY, 5))


def blocks(n):
    cols = [CORAL, SKY, LIME]
    out = rect(20, 176, 160, 10, LGREY, 5, NAVY, 3)
    for i in range(n):
        out += rect(70, 126 - i * 52, 60, 50, cols[i], 8) + star(100, 151 - i * 52, 10, WHITE, NAVY, 2.5)
    return out


for _n in (1, 2, 3):
    reg(f"blocks_{_n}", (lambda n=_n: (lambda: svg_doc(blocks(n), 200, 200)))())


@asset("sun_high")
def _():
    return rect(0, 0, 200, 200, "#DDF3FB", 0, None, 0) + ASSETS["sun"]().split("</title>", 1)[1].rsplit("</svg>", 1)[0].replace('cy="100', 'cy="80') + rect(0, 170, 200, 30, LIME, 0)


@asset("night")
def _():
    return rect(0, 0, 200, 200, "#2C4E6A", 0, None, 0) + moon_small(100, 90) + star(40, 40, 10, YELLOW, NAVY, 3) + star(160, 50, 12, YELLOW, NAVY, 3) + star(150, 150, 8, YELLOW, NAVY, 3) + rect(0, 176, 200, 24, "#3E9A4B", 0)


@asset("leaf_oak")
def _():
    return (path("M100,20 C120,30 110,50 128,54 C150,52 146,76 132,84 C152,92 150,116 130,118 C146,132 130,156 112,146 C110,164 100,172 100,180 "
                 "C100,172 90,164 88,146 C70,156 54,132 70,118 C50,116 48,92 68,84 C54,76 50,52 72,54 C90,50 80,30 100,20 Z", "#F7923A") +
            path("M100,40 V194", "none", NAVY, 5))


@asset("leaf_green")
def _():
    return path(leaf_d(100, 96, 80), GREEN, NAVY, 6) + path("M100,30 V190 M100,80 l-24,-16 M100,110 l26,-16 M100,140 l-24,-16", "none", NAVY, 4)


@asset("stone_round")
def _():
    return ellipse(100, 120, 80, 54, GREY) + path("M60,104 q12,-14 32,-14", "none", WHITE, 7) + circle(130, 130, 7, DGREY, None, 0)


@asset("stone_flat")
def _():
    return path("M20,140 C20,100 60,80 110,84 C160,88 184,110 180,140 C176,164 30,170 20,140 Z", "#C2B8AE") + path("M60,110 q20,-10 40,-8", "none", WHITE, 7)


@asset("basket", 220, 160)
def _():
    out = path("M30,56 C30,10 190,10 190,56", "none", NAVY, 14) + path("M30,56 C30,10 190,10 190,56", "none", TAN, 7)
    out += path("M14,56 L206,56 L186,150 L34,150 Z", TAN)
    for i in range(1, 6):
        out += line(14 + i * 32, 56, 34 + i * 25, 150, "#B27B3B", 4)
    out += path("M24,90 H196 M30,120 H190", "none", "#B27B3B", 4)
    return out


# ------------------------------------------------------------------ habitats & scenes (wide)
@asset("hab_ocean", 300, 200)
def _():
    return (rect(0, 0, 300, 200, "#7FD3F2", 0, None, 0) + path("M0,30 q25,-14 50,0 t50,0 t50,0 t50,0 t50,0 t50,0 V0 H0 Z", WATER, None, 0) +
            path("M0,170 q75,-24 150,0 t150,0 V200 H0 Z", SAND, None, 0) +
            path("M30,170 C20,140 40,130 30,100 M44,172 C54,146 36,136 48,110", "none", DGREEN, 7) +
            circle(260, 60, 8, WHITE, SKY, 3) + circle(272, 84, 5, WHITE, SKY, 3))


@asset("hab_farm", 300, 200)
def _():
    return (rect(0, 0, 300, 200, "#CFEFFB", 0, None, 0) + path("M0,110 q150,-40 300,0 V200 H0 Z", "#9FD86A", None, 0) +
            rect(200, 50, 80, 70, CORAL, 4) + poly([(196, 54), (240, 20), (284, 54)], "#C94A3C", NAVY, 4) + rect(226, 80, 28, 40, WHITE, 2, NAVY, 3) +
            path("M10,140 H170 M10,166 H170", "none", "#B27B3B", 6) + "".join(rect(14 + 38 * i, 124, 10, 56, "#D9A86C", 3, NAVY, 3) for i in range(5)))


@asset("hab_rainforest", 300, 200)
def _():
    return (rect(0, 0, 300, 200, "#BDE8B0", 0, None, 0) + rect(40, 60, 22, 140, BROWN, 4) + rect(230, 50, 24, 150, BROWN, 4) +
            blob([(52, 56, 44), (104, 46, 36), (32, 80, 28)], DGREEN) + blob([(244, 54, 44), (270, 84, 26), (196, 44, 34)], DGREEN) +
            path("M120,0 C130,40 110,70 130,110 M170,0 C160,30 180,60 166,90", "none", "#5DBB63", 6) +
            path("M0,180 q40,-30 80,0 q40,-30 80,0 q40,-30 80,0 q40,-30 80,0 V200 H0 Z", GREEN, None, 0))


@asset("hab_ice", 300, 200)
def _():
    return (rect(0, 0, 300, 200, "#DDF3FB", 0, None, 0) + poly([(0, 150), (60, 80), (110, 120), (170, 60), (240, 130), (300, 90), (300, 200), (0, 200)], WHITE, "#9CCDE3", 4) +
            rect(0, 168, 300, 32, "#9FD9F0", 0, None, 0) + "".join(star(x, y, 6, WHITE, "#9CCDE3", 2) for x, y in ((40, 30), (130, 24), (230, 34), (280, 20))))


@asset("hab_desert", 300, 200)
def _():
    return (rect(0, 0, 300, 200, "#FFE7B8", 0, None, 0) + circle(250, 44, 26, YELLOW, "#F2B92E", 4) +
            path("M0,140 q80,-60 160,0 q70,-50 140,-10 V200 H0 Z", SAND, "#E5C27A", 4) +
            rect(40, 90, 18, 70, GREEN, 9, DGREEN, 4) + rect(24, 104, 14, 30, GREEN, 7, DGREEN, 3) + rect(60, 96, 14, 30, GREEN, 7, DGREEN, 3))


@asset("hab_pond", 300, 200)
def _():
    return (rect(0, 0, 300, 200, "#CFEFFB", 0, None, 0) + rect(0, 90, 300, 110, "#9FD86A", 0, None, 0) +
            ellipse(150, 150, 130, 40, "#7FD3F2", "#4CB3DA", 4) + ellipse(80, 150, 22, 8, GREEN, DGREEN, 3) + ellipse(220, 156, 20, 7, GREEN, DGREEN, 3) +
            path("M20,120 C20,90 24,70 30,60 M34,124 C36,96 42,80 50,72", "none", DGREEN, 6) + ellipse(30, 58, 6, 14, BROWN, None, 0))


@asset("farm_scene", 420, 300)
def _():
    out = rect(0, 0, 420, 300, "#CFEFFB", 0, None, 0) + circle(370, 44, 26, YELLOW, "#F2B92E", 4)
    out += path("M0,120 q210,-50 420,0 V300 H0 Z", "#9FD86A", None, 0)
    # coop (left)
    out += rect(22, 74, 120, 92, "#F7B6D2", 6) + poly([(14, 78), (82, 30), (150, 78)], CORAL, NAVY, 5) + rect(66, 110, 34, 56, "#C98A4B", 14, NAVY, 4)
    # mud (right top)
    out += path("M250,170 C240,140 300,130 330,140 C380,134 410,160 390,182 C370,200 280,200 250,170 Z", "#A87850", "#7A5434", 4)
    # pond (bottom)
    out += ellipse(150, 252, 120, 36, "#7FD3F2", "#4CB3DA", 4)
    out += path("M10,210 H120 M10,234 H120", "none", "#B27B3B", 5)
    return out


@asset("ocean_scene", 420, 330)
def _():
    out = rect(0, 0, 420, 330, "#7FD3F2", 0, None, 0) + path("M0,30 q30,-14 60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 V0 H0 Z", WATER, None, 0)
    out += path("M0,280 q105,-34 210,0 t210,0 V330 H0 Z", SAND, None, 0)
    out += path("M310,300 C300,240 380,220 410,250 L420,300 Z", "#8C9BA7", NAVY, 4) + path("M330,240 C350,230 380,240 390,256", "none", WHITE, 5)
    for x in (30, 52, 270):
        out += path(f"M{x},300 C{x - 14},260 {x + 14},240 {x},200", "none", DGREEN, 8)
    out += "".join(circle(x, y, r, WHITE, SKY, 3) for x, y, r in ((200, 60, 7), (212, 40, 5), (380, 100, 8), (392, 76, 5)))
    out += g(ASSETS["fish"]().split("</title>", 1)[1].rsplit("</svg>", 1)[0], t="translate(40 60) scale(0.32)")
    out += star(240, 296, 14, CORAL, NAVY, 3)
    return out


@asset("map_scene", 420, 340)
def _():
    out = rect(0, 0, 420, 340, "#7FD3F2", 22)
    out += path("M60,80 C80,30 200,20 260,40 C340,30 400,90 380,170 C400,250 330,320 230,300 C150,330 50,300 50,220 C20,170 30,110 60,80 Z", SAND, "#D9B26A", 6)
    out += path("M80,250 C120,230 140,190 190,180 C240,170 260,120 300,110", "none", CORAL, 6).replace("/>", ' stroke-dasharray="4 14"/>')
    out += path("M300,250 l24,24 M324,250 l-24,24", "none", "#E8473B", 10)
    out += path("M190,60 q20,10 40,0", "none", "#5DBB63", 6) + path("M140,140 C150,120 170,120 176,130", "none", "#7FD3F2", 10)
    out += g(rect(380, 290, 30, 30, WHITE, 15) + path("M395,292 v26 M382,305 h26", "none", NAVY, 3) + poly([(395, 288), (400, 305), (390, 305)], CORAL, NAVY, 2))
    return out


@asset("palm")
def _():
    return (path("M96,190 C90,150 104,100 98,70", "none", NAVY, 24) + path("M96,190 C90,150 104,100 98,70", "none", "#C98A4B", 14) +
            path("M98,70 C70,40 40,46 20,70 C50,60 74,64 98,70 Z", GREEN) + path("M98,70 C126,40 160,46 180,72 C150,60 120,64 98,70 Z", GREEN) +
            path("M98,70 C80,40 90,16 110,10 C100,34 100,52 98,70 Z", GREEN) + circle(92, 80, 9, BROWN) + circle(108, 80, 9, BROWN) +
            ellipse(98, 190, 70, 10, SAND, "#D9B26A", 3))


@asset("bridge")
def _():
    return (rect(0, 130, 200, 70, "#7FD3F2", 0, None, 0) + path("M10,120 Q100,50 190,120", "none", NAVY, 16) + path("M10,120 Q100,50 190,120", "none", "#C98A4B", 9) +
            "".join(line(30 + 28 * i, 104 - (14 if 0 < i < 5 else 0), 30 + 28 * i, 150, "#B27B3B", 6) for i in range(6)) +
            path("M10,120 Q100,90 190,120", "none", NAVY, 5))


@asset("lighthouse")
def _():
    return (poly([(70, 180), (130, 180), (118, 60), (82, 60)], WHITE, NAVY, 6) + poly([(76, 140), (124, 140), (121, 110), (79, 110)], CORAL, NAVY, 4) +
            poly([(80, 84), (120, 84), (119, 72), (81, 72)], CORAL, NAVY, 3) + rect(78, 34, 44, 28, YELLOW, 6) + poly([(72, 36), (100, 12), (128, 36)], CORAL, NAVY, 5) +
            path("M130,44 L186,26 M130,52 L186,70", "none", "#F2B92E", 6) + rect(50, 178, 100, 14, GREY, 6))


@asset("chest")
def _():
    return (rect(30, 90, 140, 90, "#C98A4B", 10) + path("M30,96 C30,40 170,40 170,96 Z", "#B27B3B") +
            rect(30, 90, 140, 14, YELLOW, 4, NAVY, 3) + rect(88, 96, 24, 30, YELLOW, 6, NAVY, 4) + circle(100, 110, 4, NAVY, None, 0) +
            star(60, 58, 9, YELLOW, NAVY, 2.5) + star(144, 62, 7, YELLOW, NAVY, 2.5))


@asset("castle_base", 360, 300)
def _():
    out = rect(0, 270, 360, 30, "#9FD86A", 0, None, 0)
    out += rect(20, 110, 80, 170, "#E3E8EC", 6) + rect(260, 110, 80, 170, "#E3E8EC", 6)
    out += rect(100, 150, 160, 130, "#F1F4F6", 4)
    for x in range(104, 260, 32):
        out += rect(x, 132, 22, 22, "#F1F4F6", 3)
    for y in (180, 220, 250):
        out += path(f"M110,{y} h30 M170,{y} h30 M230,{y} h20 M30,{y - 30} h30 M270,{y - 30} h30", "none", "#B8C3CC", 4)
    out += rect(44, 160, 32, 40, WATER, 16, NAVY, 4) + rect(284, 160, 32, 40, WATER, 16, NAVY, 4)
    return out


@asset("roof_left")
def _():
    return poly([(100, 20), (184, 176), (16, 176)], "#3FA9E0", NAVY, 7) + path("M60,140 h80 M80,100 h40", "none", WHITE, 5)


@asset("roof_right")
def _():
    return poly([(100, 20), (184, 176), (16, 176)], "#9B6BD3", NAVY, 7) + path("M60,140 h80 M80,100 h40", "none", WHITE, 5)


@asset("castle_door")
def _():
    return path("M40,186 L40,90 C40,20 160,20 160,90 L160,186 Z", "#C98A4B", NAVY, 7) + path("M100,40 V186 M40,120 H160", "none", "#9A6A44", 5) + circle(130, 130, 7, YELLOW, NAVY, 3)


@asset("castle_flag")
def _():
    return rect(40, 20, 10, 170, GREY, 4) + path("M50,26 L170,50 L50,92 Z", CORAL, NAVY, 6) + star(92, 58, 14, YELLOW, NAVY, 3) + circle(45, 18, 9, YELLOW)


# rooms
@asset("room_bathroom", 300, 220)
def _():
    return (rect(0, 0, 300, 220, "#DFF4FB", 0, None, 0) + rect(0, 150, 300, 70, "#BDE3F0", 0, None, 0) +
            "".join(rect(10 + 40 * i, 20, 36, 36, "#EAF8FC", 4, "#BFE3EE", 3) for i in range(7)) +
            g(ASSETS["bathtub"]().split("</title>", 1)[1].rsplit("</svg>", 1)[0], t="translate(150 80) scale(0.75)"))


@asset("room_bedroom", 300, 220)
def _():
    return (rect(0, 0, 300, 220, "#F3EDFD", 0, None, 0) + rect(0, 160, 300, 60, "#D9C8F5", 0, None, 0) +
            rect(150, 90, 140, 70, "#CFC2F2", 12) + rect(140, 60, 20, 120, "#9B6BD3", 8) + rect(280, 90, 14, 90, "#9B6BD3", 6) + rect(160, 110, 130, 40, SKY, 10) +
            rect(30, 30, 70, 60, WHITE, 6, NAVY, 4) + moon_small(66, 60))


@asset("room_kitchen", 300, 220)
def _():
    return (rect(0, 0, 300, 220, "#FFF4DA", 0, None, 0) + rect(0, 170, 300, 50, "#F6DFA4", 0, None, 0) +
            rect(170, 80, 110, 100, WHITE, 8) + rect(170, 80, 110, 24, LGREY, 6) + circle(200, 92, 7, NAVY, None, 0) + circle(250, 92, 7, NAVY, None, 0) +
            rect(186, 116, 78, 50, "#3B5266", 8, NAVY, 3) + rect(20, 30, 90, 40, CORAL, 6) + path("M30,50 h70", "none", WHITE, 4))


# vehicle bands
@asset("band_sky", 440, 120)
def _():
    return rect(0, 0, 440, 120, "#CFEFFB", 16) + blob([(330, 60, 22), (360, 48, 28), (390, 62, 20)], WHITE, 4) + circle(40, 34, 18, YELLOW, "#F2B92E", 4)


@asset("band_road", 440, 120)
def _():
    return rect(0, 0, 440, 120, "#9FD86A", 16) + rect(0, 40, 440, 60, "#5E6E7B", 0, NAVY, 4) + path("M10,70 H430", "none", WHITE, 6).replace("/>", ' stroke-dasharray="26 22"/>')


@asset("band_rail", 440, 120)
def _():
    return (rect(0, 0, 440, 120, "#F6DFA4", 16) + "".join(rect(10 + 30 * i, 52, 14, 52, "#9A6A44", 3, NAVY, 3) for i in range(14)) +
            path("M0,62 H440 M0,94 H440", "none", DGREY, 8))


@asset("band_water", 440, 120)
def _():
    return rect(0, 0, 440, 120, "#7FD3F2", 16) + "".join(path(f"M{20 + 70 * i},{60 + (i % 2) * 24} q12,-12 24,0 t24,0", "none", WHITE, 6) for i in range(6))


# weather panels
@asset("weather_sunny", 220, 170)
def _():
    return rect(0, 0, 220, 170, "#FFF1BF", 18, None, 0) + g(ASSETS["sun"]().split("</title>", 1)[1].rsplit("</svg>", 1)[0], t="translate(50 15) scale(0.6)") + rect(0, 140, 220, 30, LIME, 0, None, 0)


@asset("weather_rainy", 220, 170)
def _():
    return (rect(0, 0, 220, 170, "#D7EEF7", 18, None, 0) + blob([(80, 60, 30), (120, 46, 36), (156, 66, 26)], "#C9D3DB", 5, rects=[(60, 60, 120, 30, 15)]) +
            "".join(path(drop_d(x, y, 10), "#3FA9E0", NAVY, 3) for x, y in ((80, 116), (112, 134), (144, 116), (100, 156), (160, 152))))


@asset("weather_cold", 220, 170)
def _():
    def flake(x, y, r):
        return "".join(line(x - r * math.cos(math.radians(a)), y - r * math.sin(math.radians(a)), x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a)), "#3FA9E0", 4) for a in (0, 60, 120))
    return (rect(0, 0, 220, 170, "#EEF7FC", 18, None, 0) + flake(60, 50, 22) + flake(160, 40, 16) + flake(120, 90, 14) + flake(40, 110, 12) +
            path("M0,140 q55,-20 110,0 t110,0 V170 H0 Z", WHITE, "#9CCDE3", 4) + circle(176, 112, 20, WHITE, NAVY, 4) + circle(176, 80, 14, WHITE, NAVY, 4))


# shelves / categories
@asset("shelf", 440, 60)
def _():
    return rect(0, 10, 440, 26, "#C98A4B", 8) + rect(20, 36, 16, 20, "#9A6A44", 4) + rect(404, 36, 16, 20, "#9A6A44", 4)


# number train
@asset("train_engine", 220, 200)
def _():
    return (rect(110, 30, 90, 110, SKY, 12) + rect(124, 46, 62, 40, WATER, 8, NAVY, 4) + rect(16, 80, 104, 60, CORAL, 12) +
            rect(36, 36, 30, 46, NAVY, 6) + rect(28, 26, 46, 16, CORAL, 6) + circle(50, 150, 22, NAVY) + circle(50, 150, 9, YELLOW, None, 0) +
            circle(160, 150, 22, NAVY) + circle(160, 150, 9, YELLOW, None, 0) + poly([(16, 128), (0, 160), (24, 160)], YELLOW, NAVY, 4) +
            circle(52, 12, 10, WHITE, LGREY, 3))


@asset("train_car", 220, 80)
def _():
    return rect(6, 6, 208, 44, YELLOW, 10) + circle(50, 60, 16, NAVY) + circle(50, 60, 6, CORAL, None, 0) + circle(170, 60, 16, NAVY) + circle(170, 60, 6, CORAL, None, 0)


# ------------------------------------------------------------------ worlds (mission map)
@asset("world_colour")
def _():
    out = ""
    for i, c in enumerate(["#E8473B", "#F7923A", "#FFD348", "#6CC04A", "#3FA9E0", "#9B6BD3"]):
        r = 92 - i * 10
        out += path(f"M{100 - r},120 A{r},{r} 0 0 1 {100 + r},120", "none", c, 10)
    out += rect(64, 100, 72, 80, PINK, 6) + rect(54, 80, 26, 100, "#F59AC0", 4) + rect(120, 80, 26, 100, "#F59AC0", 4)
    out += poly([(50, 82), (67, 52), (84, 82)], "#9B6BD3", NAVY, 4) + poly([(116, 82), (133, 52), (150, 82)], "#9B6BD3", NAVY, 4)
    out += path("M88,180 V150 C88,136 112,136 112,150 V180 Z", WHITE, NAVY, 4)
    return out


@asset("world_animal")
def _():
    return (ellipse(100, 150, 96, 40, "#7FD3F2", None, 0) + ellipse(100, 140, 70, 30, SAND, "#D9B26A", 4) +
            ASSETS["palm"]().split("</title>", 1)[1].rsplit("</svg>", 1)[0].replace('<ellipse cx="98.0" cy="190.0"', '<ellipse cx="98.0" cy="999"'))


@asset("world_number")
def _():
    out = ""
    for i, (x, col) in enumerate(((20, CORAL), (80, SKY), (140, LIME))):
        h = 70 + (i % 2) * 30
        out += rect(x, 180 - h, 50, h, col, 6) + rect(x + 13, 190 - h, 24, 24, WHITE, 4, NAVY, 3)
    out += circle(52, 40, 18, YELLOW)
    return out + rect(10, 176, 180, 10, DGREY, 4)


@asset("world_feelings")
def _():
    out = ""
    for x, y, r in ((50, 90, 34), (100, 60, 42), (150, 92, 34)):
        out += rect(x - 7, y + r - 10, 14, 70, BROWN, 4)
    out += blob([(50, 90, 34), (100, 60, 42), (150, 92, 34), (100, 100, 34)], GREEN)
    out += heart(100, 74, 20, PINK, NAVY, 4) + heart(56, 100, 10, CORAL, NAVY, 3) + heart(146, 102, 10, CORAL, NAVY, 3)
    return out + rect(10, 176, 180, 10, "#8CC63F", 4)


@asset("world_everyday")
def _():
    return (rect(24, 96, 70, 80, YELLOW, 6) + poly([(16, 100), (59, 56), (102, 100)], CORAL, NAVY, 5) + rect(48, 130, 22, 46, SKY, 4, NAVY, 3) +
            rect(112, 110, 66, 66, SKY, 6) + poly([(104, 114), (145, 76), (186, 114)], "#9B6BD3", NAVY, 5) + rect(130, 128, 28, 24, WHITE, 4, NAVY, 3) +
            rect(10, 176, 180, 10, "#8CC63F", 4))


@asset("world_adventure")
def _():
    return (poly([(10, 180), (80, 50), (150, 180)], "#8C9BA7", NAVY, 5) + poly([(60, 86), (80, 50), (100, 86), (90, 80), (80, 92), (70, 80)], WHITE, NAVY, 4) +
            poly([(90, 180), (150, 80), (196, 180)], "#A9B4BD", NAVY, 5) + line(80, 50, 80, 14, NAVY, 5) + path("M80,14 L112,24 L80,36 Z", CORAL, NAVY, 4))


# ------------------------------------------------------------------ decor
@asset("cloud_plain", 220, 140)
def _():
    return blob([(70, 86, 36), (114, 66, 46), (156, 90, 32)], WHITE, 5, rects=[(40, 84, 150, 40, 20)])


@asset("rainbow", 300, 160)
def _():
    out = ""
    for i, c in enumerate(["#E8473B", "#F7923A", "#FFD348", "#6CC04A", "#3FA9E0", "#9B6BD3"]):
        r = 140 - i * 14
        out += path(f"M{150 - r},150 A{r},{r} 0 0 1 {150 + r},150", "none", NAVY, 15)
        out += path(f"M{150 - r},150 A{r},{r} 0 0 1 {150 + r},150", "none", c, 11)
    return out


@asset("house_home", 220, 220)
def _():
    return (rect(36, 96, 148, 110, YELLOW, 8) + poly([(20, 104), (110, 24), (200, 104)], CORAL, NAVY, 6) +
            rect(92, 140, 40, 66, SKY, 10) + circle(122, 174, 4, NAVY, None, 0) + rect(50, 120, 32, 30, WHITE, 4, NAVY, 4) + rect(146, 120, 30, 30, WHITE, 4, NAVY, 4) +
            heart(110, 76, 14, PINK, NAVY, 3) + rect(150, 34, 20, 40, BROWN, 3))


@asset("rosette", 200, 260)
def _():
    return (poly([(70, 150), (50, 250), (80, 230), (100, 254), (100, 150)], CORAL, NAVY, 5) +
            poly([(130, 150), (150, 250), (120, 230), (100, 254), (100, 150)], SKY, NAVY, 5) +
            blob([(100 + 64 * math.cos(math.radians(a)), 100 + 64 * math.sin(math.radians(a)), 22) for a in range(0, 360, 30)], YELLOW) +
            circle(100, 100, 52, WHITE) + star(100, 104, 34, YELLOW, NAVY, 5))


@asset("reward_star")
def _():
    return star(100, 106, 90, YELLOW, NAVY, 7, r=46) + happy_eye(84, 102, 7) + happy_eye(116, 102, 7) + smile(100, 118, 9, 7, 4)


@asset("reward_star_blank")
def _():
    return star(100, 106, 90, WHITE, NAVY, 7, r=46)


@asset("sparkle")
def _():
    return star(100, 100, 80, YELLOW, NAVY, 6, r=24)


@asset("hill", 400, 120)
def _():
    return path("M0,120 C80,20 200,20 260,70 C300,40 360,40 400,80 V120 Z", LIME)


@asset("magnifier")
def _():
    return ASSETS["icon_explore"]().split("</title>", 1)[1].rsplit("</svg>", 1)[0]


@asset("fastener_dot", 100, 100)
def _():
    return circle(50, 50, 40, "none", "#8C9BA7", 5).replace("/>", ' stroke-dasharray="7 6"/>') + circle(50, 50, 8, "#8C9BA7", None, 0)


def inner(name):
    s = get_svg(name)
    return s.split("</title>", 1)[1].rsplit("</svg>", 1)[0] if "</title>" in s else s.split(">", 1)[1].rsplit("</svg>", 1)[0]


def card_svg(name):
    w, h = get_size(name)
    sc = 150 / max(w, h)
    body = (rect(6, 6, 188, 188, WHITE, 22, NAVY, 6) +
            g(inner(name), t=f"translate({100 - w * sc / 2:.1f} {100 - h * sc / 2:.1f}) scale({sc:.3f})"))
    return svg_doc(body, 200, 200, "card " + name)


def get_svg(name):
    if name.startswith("card:"):
        return card_svg(name[5:])
    if name.startswith("sil:"):
        return silhouette(get_svg(name[4:]))
    if name.startswith("hint:"):
        return silhouette(get_svg(name[5:]), "#E4EAEE", "#B5C2CC")
    return ASSETS[name]()


def get_size(name):
    s = get_svg(name)
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    return float(m.group(1)), float(m.group(2))
