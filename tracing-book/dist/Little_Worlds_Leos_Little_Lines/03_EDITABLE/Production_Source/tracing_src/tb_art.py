"""Leo's Little Lines - pastel art layer + new original illustrations.

Re-uses the Little Worlds Learning illustration library (busy-book/src) and adds:
  * "p:<asset>"    -> pastel version (fills blended toward white, softer outline)
  * "line:<asset>" -> colouring-page line art (white fills, soft navy outline)
  * new assets needed for the tracing book (registered into art_lib.ASSETS)
"""
import os
import re
import sys

BB = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "busy-book", "src"))
if BB not in sys.path:
    sys.path.insert(0, BB)

import art_lib                       # noqa: E402
from art_core import (circle, ellipse, rect, path, poly, line, g, blob, star, heart, drop_d, leaf_d,  # noqa: E402
                      eye, happy_eye, smile, svg_doc, NAVY, YELLOW, SKY, LIME, CORAL, PINK, WHITE, GREEN,
                      DGREEN, BROWN, TAN, GREY, LGREY, DGREY, SAND, WATER)

OUTLINE = "#44596B"     # softened navy for pastel art
PASTEL_MIX = 0.38       # share of white blended into every fill


def _blend(hexc, k):
    h = hexc.lstrip("#")
    if len(h) != 6:
        return hexc
    r, gg, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    r, gg, b = (round(c + (255 - c) * k) for c in (r, gg, b))
    return f"#{r:02X}{gg:02X}{b:02X}"


def pastelize(svg):
    def fill(m):
        c = m.group(1)
        if c.upper() in ("#FFFFFF", "NONE"):
            return m.group(0)
        if c.upper() == "#18354B":
            return f'fill="{OUTLINE}"'
        return f'fill="{_blend(c, PASTEL_MIX)}"'

    def stroke(m):
        c = m.group(1)
        if c.upper() == "#18354B":
            return f'stroke="{OUTLINE}"'
        if c.upper() in ("#FFFFFF", "NONE"):
            return m.group(0)
        return f'stroke="{_blend(c, PASTEL_MIX * 0.6)}"'

    svg = re.sub(r'fill="(#[0-9A-Fa-f]{6}|none)"', fill, svg)
    return re.sub(r'stroke="(#[0-9A-Fa-f]{6}|none)"', stroke, svg)


def lineart(svg):
    svg = re.sub(r'fill="(#[0-9A-Fa-f]{6})"', lambda m: 'fill="#FFFFFF"' if m.group(1).upper() != "#18354B" else f'fill="{OUTLINE}"', svg)
    return re.sub(r'stroke="(#[0-9A-Fa-f]{6})"', lambda m: f'stroke="{OUTLINE}"' if m.group(1).upper() != "#FFFFFF" else 'stroke="#FFFFFF"', svg)


_orig_get_svg = art_lib.get_svg


def get_svg(name):
    if name.startswith("p:"):
        return pastelize(_orig_get_svg(name[2:]) if not name[2:].startswith(("p:", "line:")) else get_svg(name[2:]))
    if name.startswith("line:"):
        return lineart(_orig_get_svg(name[5:]))
    return _orig_get_svg(name)


art_lib.get_svg = get_svg


def _reg(name, w=200, h=200):
    def deco(fn):
        art_lib.ASSETS[name] = lambda: svg_doc(fn(), w, h, name.replace("_", " "))
        return fn
    return deco


# ----------------------------------------------------------------- new artwork
@_reg("ball")
def _():
    return (circle(100, 100, 76, CORAL) + path("M30,80 Q100,60 170,80", "none", WHITE, 12) +
            path("M30,124 Q100,144 170,124", "none", YELLOW, 12) + circle(100, 100, 76, "none", NAVY, 6))


@_reg("rocket")
def _():
    return (poly([(70, 130), (40, 176), (78, 160)], CORAL, NAVY, 5) + poly([(130, 130), (160, 176), (122, 160)], CORAL, NAVY, 5) +
            path("M100,14 C140,40 140,120 128,160 L72,160 C60,120 60,40 100,14 Z", WHITE) + circle(100, 80, 18, SKY, NAVY, 5) +
            path("M80,160 L100,196 L120,160 Z", YELLOW, NAVY, 4) + path("M78,44 Q100,32 122,44", "none", CORAL, 8))


@_reg("puddle", 200, 120)
def _():
    return ellipse(100, 70, 90, 34, WATER) + ellipse(70, 62, 20, 6, WHITE, None, 0) + ellipse(140, 80, 14, 5, WHITE, None, 0)


@_reg("snail_body", 240, 200)
def _():
    return (path("M20,170 C20,150 60,148 120,150 L210,150 C226,150 232,170 214,176 L40,180 C28,180 20,178 20,170 Z", "#F7B6D2") +
            path("M196,152 L206,104 M214,154 L230,110", "none", NAVY, 5) + circle(206, 100, 7, NAVY, None, 0) + circle(230, 106, 7, NAVY, None, 0) +
            circle(110, 96, 64, "#FFE3A3") + eye(212, 140, 4) + smile(214, 156, 6, 4, 3))


@_reg("lilypad", 200, 120)
def _():
    return path("M100,60 L190,48 C190,96 150,112 100,112 C40,112 10,90 10,60 C10,26 60,10 100,10 Z", GREEN, NAVY, 5) + path("M100,60 L60,30", "none", DGREEN, 4)


@_reg("gift")
def _():
    return (rect(30, 70, 140, 110, PINK, 8) + rect(22, 50, 156, 34, CORAL, 8) + rect(88, 50, 24, 130, YELLOW, 2, NAVY, 4) +
            path("M100,50 C70,10 40,30 70,50 M100,50 C130,10 160,30 130,50", "none", NAVY, 6))


@_reg("party_hat")
def _():
    return (poly([(100, 22), (164, 178), (36, 178)], SKY, NAVY, 6) + path("M66,108 L134,108 M50,146 L150,146", "none", YELLOW, 10) +
            circle(100, 22, 16, CORAL) + ellipse(100, 180, 70, 12, CORAL))


@_reg("door")
def _():
    return rect(48, 14, 104, 176, "#9B6BD3", 8) + rect(64, 34, 72, 56, "#B58BE0", 6, NAVY, 4) + rect(64, 110, 72, 60, "#B58BE0", 6, NAVY, 4) + circle(132, 104, 7, YELLOW, NAVY, 3)


@_reg("heart_big")
def _():
    return heart(100, 104, 82, CORAL, NAVY, 7) + path("M58,70 q8,-14 24,-14", "none", WHITE, 7)


@_reg("kite")
def _():
    return (poly([(100, 14), (160, 84), (100, 150), (40, 84)], CORAL, NAVY, 6) + path("M100,14 L100,150 M40,84 L160,84", "none", NAVY, 4) +
            path("M100,150 C90,166 116,174 104,190", "none", NAVY, 4) + poly([(92, 166), (110, 172), (96, 180)], YELLOW, NAVY, 3))


@_reg("nest", 220, 180)
def _():
    return (ellipse(110, 70, 30, 38, "#DDF3FB") + ellipse(80, 78, 26, 34, "#DDF3FB") + ellipse(140, 80, 26, 34, "#DDF3FB") +
            path("M20,90 C30,160 190,160 200,90 Z", TAN) + path("M30,104 Q110,124 190,104 M40,124 Q110,142 180,124", "none", BROWN, 5))


@_reg("quilt")
def _():
    out = ""
    cols = [PINK, YELLOW, SKY, LIME]
    for r in range(4):
        for c in range(4):
            out += rect(20 + c * 40, 20 + r * 40, 40, 40, cols[(r + c) % 4], 0, NAVY, 3)
    return out + rect(20, 20, 160, 160, "none", 8, NAVY, 6) + heart(100, 100, 14, CORAL, NAVY, 3)


@_reg("umbrella")
def _():
    return (path("M20,100 C20,30 180,30 180,100 Q160,86 140,100 Q120,86 100,100 Q80,86 60,100 Q40,86 20,100 Z", "#9B6BD3") +
            path("M100,100 L100,170 Q100,190 82,186", "none", NAVY, 7) + path("M100,40 L100,100", "none", NAVY, 3) + circle(100, 30, 6, YELLOW, NAVY, 3))


@_reg("volcano")
def _():
    return (poly([(10, 186), (80, 60), (120, 60), (190, 186)], "#B98A5E", NAVY, 6) + path("M80,60 Q100,74 120,60", "#F7923A", NAVY, 4) +
            path("M86,60 C70,30 92,20 100,8 C108,24 130,30 114,60 Z", CORAL, NAVY, 4) + path("M88,70 L80,110 L96,96 L92,130", "none", "#F7923A", 7))


@_reg("watermelon")
def _():
    return (path("M14,70 A86,86 0 0 0 186,70 Z", "#6CC04A") + path("M28,70 A72,72 0 0 0 172,70 Z", "#F59AC0", NAVY, 4) +
            "".join(ellipse(x, y, 4, 7, NAVY, None, 0) for x, y in ((70, 96), (100, 112), (130, 96), (86, 124), (116, 124))))


@_reg("xylophone")
def _():
    cols = [CORAL, "#F7923A", YELLOW, LIME, SKY, "#9B6BD3"]
    out = rect(18, 60, 164, 14, BROWN, 6) + rect(18, 150, 164, 14, BROWN, 6)
    for i, c in enumerate(cols):
        h = 112 - i * 9
        out += rect(26 + i * 26, 112 - h / 2, 22, h, c, 6)
    return out + path("M150,20 L120,70", "none", NAVY, 6) + circle(150, 20, 10, CORAL)


@_reg("yoyo")
def _():
    return (path("M100,10 L100,70", "none", NAVY, 4) + circle(100, 120, 60, SKY) + circle(100, 120, 38, "#3FA9E0") +
            circle(100, 120, 12, YELLOW, NAVY, 4) + path("M60,92 q14,-16 34,-18", "none", WHITE, 6))


@_reg("zebra")
def _():
    return (path("M60,40 L52,8 L80,32 M120,32 L148,8 L140,40", WHITE, NAVY, 5) +
            path("M50,60 C50,20 150,20 150,60 L150,140 C150,170 130,190 100,190 C70,190 50,170 50,140 Z", WHITE) +
            path("M60,70 h24 M60,96 h22 M118,70 h22 M120,96 h20 M86,40 l6,20 M114,40 l-6,20", "none", NAVY, 8) +
            ellipse(100, 160, 38, 26, LGREY) + circle(86, 160, 4, NAVY, None, 0) + circle(114, 160, 4, NAVY, None, 0) +
            eye(78, 118, 6) + eye(122, 118, 6) + path("M88,22 C96,6 104,6 112,22", "none", NAVY, 10))


@_reg("icecream")
def _():
    return (poly([(64, 100), (136, 100), (100, 194)], "#F2C27B", NAVY, 6) + path("M76,124 L124,124 M84,148 L116,148", "none", "#C8914A", 4) +
            circle(100, 70, 40, "#F59AC0") + circle(100, 32, 16, CORAL) + path("M78,62 q8,-14 22,-16", "none", WHITE, 6))


@_reg("lion_face")
def _():
    return art_lib.inner("leo_head")


@_reg("cloud_puff", 220, 140)
def _():
    return blob([(70, 86, 36), (114, 66, 46), (156, 90, 32)], WHITE, 5, rects=[(40, 84, 150, 40, 20)])


@_reg("leo_tracing", 200, 250)
def _():
    # Leo with a big chunky crayon
    body = art_lib.inner("leo_happy")
    crayon = g(rect(150, 100, 22, 90, CORAL, 6) + poly([(150, 100), (172, 100), (161, 76)], "#F7B6D2", NAVY, 4), t="rotate(25 161 140)")
    return body + crayon
