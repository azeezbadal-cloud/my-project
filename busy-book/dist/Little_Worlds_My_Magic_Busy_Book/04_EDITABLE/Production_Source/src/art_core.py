"""Little Worlds Learning - original vector illustration core.

All artwork is drawn from primitive shapes in code (no stock, no AI images).
Design-system rules applied to every asset:
  * outline colour  : Dark Navy #18354B
  * outline weight  : 5 units on a 200-unit art grid (round caps / joins)
  * corner radius   : 10-18 units on rectangles
  * flat brand fills, no gradients, no filters (prints cleanly at home)
"""
import math

# ---------------------------------------------------------------- palette
NAVY = "#18354B"
YELLOW = "#FFD348"
SKY = "#64C8ED"
LIME = "#A8D849"
CORAL = "#F26855"
PINK = "#F7B6D2"
CREAM = "#FFF9EA"
WHITE = "#FFFFFF"

# supporting naturals (documented in Brand_Guide)
GOLD = "#F4B940"      # Leo fur
MANE = "#E98A2E"      # Leo mane
MUZZLE = "#FFEBC2"
BROWN = "#9A6A44"
DBROWN = "#6E4A30"
TAN = "#D9A86C"
GREY = "#A9B4BD"
LGREY = "#E3E8EC"
DGREY = "#6B7A86"
GREEN = "#5DBB63"     # leaf / grass
DGREEN = "#3E9A4B"
WATER = "#BFE9F7"
SAND = "#F6DFA4"

# six activity colours (each paired with a symbol so colour is never the only cue)
ACT = {
    "red":    ("#E8473B", "heart"),
    "orange": ("#F7923A", "circle"),
    "yellow": ("#FFD348", "star"),
    "green":  ("#6CC04A", "leaf"),
    "blue":   ("#3FA9E0", "wave"),
    "purple": ("#9B6BD3", "diamond"),
}

SW = 5


def _a(**kw):
    out = []
    for k, v in kw.items():
        if v is None:
            continue
        k = k.rstrip("_").replace("_", "-")
        out.append(f'{k}="{v}"')
    return " ".join(out)


def _st(f, s, sw):
    if sw and s:
        return _a(fill=f, stroke=s, stroke_width=sw, stroke_linejoin="round", stroke_linecap="round")
    return _a(fill=f)


def circle(cx, cy, r, f=WHITE, s=NAVY, sw=SW):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" {_st(f, s, sw)}/>'


def ellipse(cx, cy, rx, ry, f=WHITE, s=NAVY, sw=SW):
    return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" {_st(f, s, sw)}/>'


def rect(x, y, w, h, f=WHITE, rx=0, s=NAVY, sw=SW):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" ry="{rx:.1f}" {_st(f, s, sw)}/>'


def path(d, f="none", s=NAVY, sw=SW):
    return f'<path d="{d}" {_st(f, s, sw)}/>'


def poly(pts, f=WHITE, s=NAVY, sw=SW):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{p}" {_st(f, s, sw)}/>'


def line(x1, y1, x2, y2, s=NAVY, sw=SW):
    return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", "none", s, sw)


def g(*items, t=None):
    tr = f' transform="{t}"' if t else ""
    return f"<g{tr}>" + "".join(items) + "</g>"


def blob(circles, f, sw=SW, s=NAVY, rects=()):
    """Union of circles (and rects) with a single clean outer outline."""
    out = []
    for cx, cy, r in circles:
        out.append(circle(cx, cy, r + sw / 2, s, None, 0))
    for x, y, w, h, rx in rects:
        out.append(rect(x - sw / 2, y - sw / 2, w + sw, h + sw, s, rx + sw / 2, None, 0))
    for cx, cy, r in circles:
        out.append(circle(cx, cy, r - sw / 2, f, None, 0))
    for x, y, w, h, rx in rects:
        out.append(rect(x + sw / 2, y + sw / 2, w - sw, h - sw, f, max(rx - sw / 2, 0), None, 0))
    return "".join(out)


def star_pts(cx, cy, R, r=None, n=5, rot=-90):
    r = r if r is not None else R * 0.48
    pts = []
    for i in range(n * 2):
        ang = math.radians(rot + i * 180 / n)
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def star(cx, cy, R, f=YELLOW, s=NAVY, sw=SW, r=None):
    return poly(star_pts(cx, cy, R, r), f, s, sw)


def heart_d(cx, cy, s):
    return (f"M{cx:.1f},{cy + s * 0.42:.1f} "
            f"C{cx - s * 1.05:.1f},{cy - s * 0.2:.1f} {cx - s * 0.5:.1f},{cy - s * 0.95:.1f} {cx:.1f},{cy - s * 0.38:.1f} "
            f"C{cx + s * 0.5:.1f},{cy - s * 0.95:.1f} {cx + s * 1.05:.1f},{cy - s * 0.2:.1f} {cx:.1f},{cy + s * 0.42:.1f} Z")


def heart(cx, cy, s, f=CORAL, st=NAVY, sw=SW):
    return path(heart_d(cx, cy, s), f, st, sw)


def drop_d(cx, cy, s):
    return (f"M{cx:.1f},{cy - s:.1f} "
            f"C{cx + s * 0.25:.1f},{cy - s * 0.55:.1f} {cx + s * 0.68:.1f},{cy - s * 0.1:.1f} {cx + s * 0.68:.1f},{cy + s * 0.3:.1f} "
            f"C{cx + s * 0.68:.1f},{cy + s * 0.72:.1f} {cx + s * 0.35:.1f},{cy + s * 0.98:.1f} {cx:.1f},{cy + s * 0.98:.1f} "
            f"C{cx - s * 0.35:.1f},{cy + s * 0.98:.1f} {cx - s * 0.68:.1f},{cy + s * 0.72:.1f} {cx - s * 0.68:.1f},{cy + s * 0.3:.1f} "
            f"C{cx - s * 0.68:.1f},{cy - s * 0.1:.1f} {cx - s * 0.25:.1f},{cy - s * 0.55:.1f} {cx:.1f},{cy - s:.1f} Z")


def leaf_d(cx, cy, s, ang=0):
    # pointed oval leaf, axis vertical before rotation
    return (f"M{cx:.1f},{cy - s:.1f} C{cx + s * 0.75:.1f},{cy - s * 0.5:.1f} {cx + s * 0.75:.1f},{cy + s * 0.5:.1f} {cx:.1f},{cy + s:.1f} "
            f"C{cx - s * 0.75:.1f},{cy + s * 0.5:.1f} {cx - s * 0.75:.1f},{cy - s * 0.5:.1f} {cx:.1f},{cy - s:.1f} Z")


def eye(cx, cy, r=8, ry=None, hl=True):
    ry = ry or r * 1.25
    out = ellipse(cx, cy, r, ry, NAVY, None, 0)
    if hl:
        out += circle(cx + r * 0.3, cy - ry * 0.35, r * 0.38, WHITE, None, 0)
    return out


def happy_eye(cx, cy, w=10, sw=SW):
    return path(f"M{cx - w:.1f},{cy + 3:.1f} Q{cx:.1f},{cy - w:.1f} {cx + w:.1f},{cy + 3:.1f}", "none", NAVY, sw)


def smile(cx, cy, w=14, depth=10, sw=SW):
    return path(f"M{cx - w:.1f},{cy:.1f} Q{cx:.1f},{cy + depth:.1f} {cx + w:.1f},{cy:.1f}", "none", NAVY, sw)


def symbol(kind, cx, cy, s, f=WHITE, st=NAVY, sw=3):
    """Shape cue paired with each activity colour (colour-blind friendly)."""
    if kind == "heart":
        return heart(cx, cy, s, f, st, sw)
    if kind == "circle":
        return circle(cx, cy, s * 0.62, f, st, sw)
    if kind == "star":
        return star(cx, cy, s * 0.85, f, st, sw)
    if kind == "leaf":
        return path(leaf_d(cx, cy, s * 0.85), f, st, sw) + line(cx, cy - s * 0.6, cx, cy + s * 0.7, st, sw * 0.7)
    if kind == "wave":
        return path(f"M{cx - s:.1f},{cy:.1f} q{s / 2:.1f},{-s * 0.6:.1f} {s:.1f},0 q{s / 2:.1f},{s * 0.6:.1f} {s:.1f},0",
                    "none", f if f != "none" else st, sw * 1.8)
    if kind == "diamond":
        return poly([(cx, cy - s * 0.85), (cx + s * 0.6, cy), (cx, cy + s * 0.85), (cx - s * 0.6, cy)], f, st, sw)
    raise ValueError(kind)


def svg_doc(body, w=200, h=200, title=None):
    t = f"<title>{title}</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f"{t}{body}</svg>")


# ====================================================================== LEO
# Leo the Little Explorer - original Little Worlds Learning mascot.

def _leo_head(cx, cy, eyes="open", mouth="smile", brows=None, look=0, scale=1.0):
    s = scale
    out = []
    # mane (scalloped)
    mane = []
    for i in range(14):
        a = math.radians(i * 360 / 14)
        mane.append((cx + 52 * s * math.cos(a), cy + 50 * s * math.sin(a), 17 * s))
    out.append(blob(mane, MANE))
    # ears
    for ex in (-38, 38):
        out.append(circle(cx + ex * s + look * 0.3, cy - 40 * s, 15 * s, GOLD))
        out.append(circle(cx + ex * s + look * 0.3, cy - 40 * s, 7 * s, PINK, None, 0))
    # face
    out.append(circle(cx, cy, 46 * s, GOLD))
    # hair tuft
    out.append(path(f"M{cx - 10 * s + look * 0.3:.1f},{cy - 44 * s:.1f} q8,-16 14,-4 q6,-12 12,2", MANE, NAVY, SW * 0.9))
    fx = cx + look
    # cheeks
    out.append(circle(fx - 29 * s, cy + 12 * s, 7 * s, PINK, None, 0))
    out.append(circle(fx + 29 * s, cy + 12 * s, 7 * s, PINK, None, 0))
    # muzzle
    out.append(ellipse(fx, cy + 16 * s, 24 * s, 17 * s, MUZZLE))
    # eyes
    ey = cy - 6 * s
    for dx in (-17, 17):
        x = fx + dx * s
        if eyes == "happy":
            out.append(happy_eye(x, ey, 8 * s))
        elif eyes == "wide":
            out.append(ellipse(x, ey, 10 * s, 12 * s, WHITE, NAVY, 3))
            out.append(eye(x + 1, ey + 1, 5.5 * s))
        elif eyes == "wink" and dx > 0:
            out.append(happy_eye(x, ey, 8 * s))
        elif eyes == "sleepy":
            out.append(path(f"M{x - 8 * s:.1f},{ey:.1f} Q{x:.1f},{ey + 7 * s:.1f} {x + 8 * s:.1f},{ey:.1f}", "none", NAVY, SW))
        else:
            out.append(eye(x, ey, 7.5 * s))
    # brows
    if brows == "raised":
        for dx in (-17, 17):
            out.append(path(f"M{fx + (dx - 8) * s:.1f},{ey - 19 * s:.1f} q{8 * s:.1f},{-7 * s:.1f} {16 * s:.1f},0", "none", NAVY, 3.5))
    elif brows == "curious":
        out.append(path(f"M{fx - 25 * s:.1f},{ey - 15 * s:.1f} q{8 * s:.1f},{-3 * s:.1f} {16 * s:.1f},{1 * s:.1f}", "none", NAVY, 3.5))
        out.append(path(f"M{fx + 9 * s:.1f},{ey - 19 * s:.1f} q{8 * s:.1f},{-8 * s:.1f} {16 * s:.1f},{-1 * s:.1f}", "none", NAVY, 3.5))
    # nose
    ny = cy + 8 * s
    out.append(path(f"M{fx - 8 * s:.1f},{ny:.1f} Q{fx:.1f},{ny - 4 * s:.1f} {fx + 8 * s:.1f},{ny:.1f} Q{fx:.1f},{ny + 10 * s:.1f} {fx - 8 * s:.1f},{ny:.1f} Z", BROWN, NAVY, 3))
    my = cy + 19 * s
    if mouth == "smile":
        out.append(path(f"M{fx - 12 * s:.1f},{my:.1f} Q{fx - 6 * s:.1f},{my + 7 * s:.1f} {fx:.1f},{my:.1f} Q{fx + 6 * s:.1f},{my + 7 * s:.1f} {fx + 12 * s:.1f},{my:.1f}", "none", NAVY, 3.5))
    elif mouth == "open":
        out.append(path(f"M{fx - 13 * s:.1f},{my - 1:.1f} Q{fx:.1f},{my + 24 * s:.1f} {fx + 13 * s:.1f},{my - 1:.1f} Z", CORAL, NAVY, 3.5))
        out.append(ellipse(fx, my + 8 * s, 6 * s, 3.5 * s, PINK, None, 0))
    elif mouth == "o":
        out.append(ellipse(fx, my + 4 * s, 6 * s, 7.5 * s, CORAL, NAVY, 3.5))
    elif mouth == "hmm":
        out.append(path(f"M{fx - 8 * s:.1f},{my + 3:.1f} q{8 * s:.1f},{-4 * s:.1f} {16 * s:.1f},{2 * s:.1f}", "none", NAVY, 3.5))
    return "".join(out)


def _arm(sx, sy, ang, side, paw=True, length=44):
    """Arm drawn hanging down from shoulder (sx,sy), rotated by ang degrees outward."""
    a = ang if side == "L" else -ang
    body = rect(sx - 10, sy - 6, 20, length, GOLD, 10) + (circle(sx, sy + length - 4, 12, GOLD) if paw else "")
    return g(body, t=f"rotate({a:.1f} {sx:.1f} {sy:.1f})")


def leo_front(eyes="open", mouth="smile", brows=None, arms=(18, 18), look=0, backpack=True):
    """Leo, front view. Canvas 200 x 250."""
    out = []
    cx = 100
    # tail (behind)
    out.append(path("M136,206 C168,214 184,200 182,184", "none", NAVY, 13))
    out.append(path("M136,206 C168,214 184,200 182,184", "none", GOLD, 7))
    out.append(path("M182,186 C170,182 172,166 184,160 C182,170 194,174 190,186 Z", MANE, NAVY, 4))
    # backpack peeking behind shoulders
    if backpack:
        out.append(rect(52, 132, 96, 64, LIME, 16))
        out.append(rect(60, 124, 80, 22, YELLOW, 10))
    # legs + shoes
    for lx in (80, 120):
        out.append(rect(lx - 13, 196, 26, 30, GOLD, 10))
        out.append(ellipse(lx + (-4 if lx < 100 else 4), 230, 20, 12, CORAL))
        out.append(path(f"M{lx - 12 + (-4 if lx < 100 else 4)},{226} h24", "none", WHITE, 3))
    # left arm (viewer's left) behind body
    lshoulder = (68, 146)
    rshoulder = (132, 146)
    late = []
    for sh, spec, side in ((lshoulder, arms[0], "L"), (rshoulder, arms[1], "R")):
        ang, ln = spec if isinstance(spec, tuple) else (spec, 44)
        (late if abs(ang) > 90 else out).append(_arm(*sh, ang, side, length=ln))
    # body
    out.append(ellipse(cx, 172, 40, 40, GOLD))
    out.append(ellipse(cx, 180, 24, 26, MUZZLE, None, 0))
    # vest panels
    out.append(path("M62,160 C62,140 76,134 90,134 L90,205 C76,206 64,198 62,186 Z", SKY))
    out.append(path("M138,160 C138,140 124,134 110,134 L110,205 C124,206 136,198 138,186 Z", SKY))
    out.append(rect(70, 168, 14, 12, WHITE, 4, NAVY, 3))    # pocket
    out.append(rect(116, 168, 14, 12, WHITE, 4, NAVY, 3))
    out.append(circle(104, 150, 3.5, YELLOW, NAVY, 2))
    # straps
    out.append(path("M84,136 L84,150", "none", CORAL, 6))
    out.append(path("M116,136 L116,150", "none", CORAL, 6))
    # head
    out.append(_leo_head(cx, 82, eyes, mouth, brows, look))
    out.extend(late)
    return svg_doc("".join(out), 200, 250, "Leo the Little Explorer")


def leo_side():
    """Leo walking, side view facing right. Canvas 200 x 250."""
    out = []
    # tail
    out.append(path("M64,200 C32,208 16,194 18,178", "none", NAVY, 13))
    out.append(path("M64,200 C32,208 16,194 18,178", "none", GOLD, 7))
    out.append(path("M18,180 C30,176 28,160 16,154 C18,164 6,168 10,180 Z", MANE, NAVY, 4))
    # back leg
    out.append(g(rect(84, 194, 24, 32, TAN, 10), t="rotate(12 96 196)"))
    out.append(ellipse(96, 230, 20, 11, CORAL))
    # backpack (on back = left side)
    out.append(rect(50, 130, 40, 66, LIME, 14))
    out.append(rect(46, 124, 40, 24, YELLOW, 10))
    out.append(rect(56, 160, 26, 18, WHITE, 6, NAVY, 3))
    # body
    out.append(ellipse(108, 172, 34, 40, GOLD))
    out.append(path("M86,142 C100,134 128,136 136,150 L138,190 C128,206 100,208 88,198 Z", SKY))
    out.append(path("M118,140 L118,206", "none", NAVY, 3))
    out.append(rect(122, 168, 12, 12, WHITE, 4, NAVY, 3))
    out.append(path("M92,138 L86,172", "none", CORAL, 7))
    # front leg
    out.append(g(rect(110, 194, 24, 32, GOLD, 10), t="rotate(-14 122 196)"))
    out.append(ellipse(132, 230, 21, 11, CORAL))
    # arm (swinging)
    out.append(_arm(108, 150, -25, "L", length=42))
    # head (profile)
    cx, cy = 112, 82
    mane = []
    for i in range(13):
        a = math.radians(i * 360 / 13)
        mane.append((cx - 8 + 48 * math.cos(a), cy + 48 * math.sin(a), 17))
    out.append(blob(mane, MANE))
    out.append(circle(cx - 12, cy - 40, 15, GOLD))
    out.append(circle(cx - 12, cy - 40, 7, PINK, None, 0))
    out.append(circle(cx, cy, 44, GOLD))
    out.append(path(f"M{cx - 6},{cy - 42} q8,-16 14,-4 q6,-12 12,2", MANE, NAVY, 4.5))
    out.append(ellipse(cx + 34, cy + 14, 24, 18, MUZZLE))
    out.append(path(f"M{cx + 50},{cy + 2} q8,2 7,10 q-6,4 -11,-2 Z", BROWN, NAVY, 3))
    out.append(path(f"M{cx + 34},{cy + 24} q8,6 18,0", "none", NAVY, 3.5))
    out.append(eye(cx + 20, cy - 8, 7.5))
    out.append(circle(cx + 6, cy + 12, 7, PINK, None, 0))
    return svg_doc("".join(out), 200, 250, "Leo side view")


def leo_three_quarter():
    """Leo three-quarter view (turned to viewer's right). Canvas 200 x 250."""
    out = []
    out.append(path("M130,206 C162,214 178,200 176,184", "none", NAVY, 13))
    out.append(path("M130,206 C162,214 178,200 176,184", "none", GOLD, 7))
    out.append(path("M176,186 C164,182 166,166 178,160 C176,170 188,174 184,186 Z", MANE, NAVY, 4))
    # backpack visible on viewer's left
    out.append(rect(44, 132, 44, 64, LIME, 14))
    out.append(rect(42, 126, 44, 22, YELLOW, 10))
    for lx, dx in ((84, -3), (118, 5)):
        out.append(rect(lx - 13, 196, 26, 30, GOLD, 10))
        out.append(ellipse(lx + dx, 230, 20, 12, CORAL))
    out.append(_arm(70, 146, 14, "L"))
    out.append(ellipse(104, 172, 36, 40, GOLD))
    out.append(ellipse(112, 180, 20, 26, MUZZLE, None, 0))
    out.append(path("M70,160 C70,142 80,134 96,134 L96,206 C82,206 72,198 70,186 Z", SKY))
    out.append(path("M136,160 C136,142 128,136 120,134 L120,205 C128,204 136,196 138,186 Z", SKY))
    out.append(rect(76, 168, 14, 12, WHITE, 4, NAVY, 3))
    out.append(path("M88,136 L88,152", "none", CORAL, 6))
    out.append(_arm(136, 146, 20, "R"))
    out.append(_leo_head(104, 82, "open", "smile", None, look=10))
    return svg_doc("".join(out), 200, 250, "Leo three-quarter view")


LEO_POSES = {
    # name: (eyes, mouth, brows, arms, look, phrase)
    "leo_happy":     ("open", "smile", None, (18, 18), 0, "Hello, explorer!"),
    "leo_wave":      ("happy", "open", None, (18, (128, 46)), 0, "Can you help me?"),
    "leo_point":     ("open", "smile", "raised", (18, 95), 4, "Let's find it!"),
    "leo_think":     ("open", "hmm", "curious", (18, (-141, 30)), -4, "Hmm... what goes here?"),
    "leo_cheer":     ("happy", "open", None, ((128, 46), (128, 46)), 0, "Mission complete!"),
    "leo_surprised": ("wide", "o", "raised", (60, 60), 0, "Wow!"),
    "leo_proud":     ("wink", "smile", None, (35, 35), 0, "Great exploring!"),
}


def leo_pose(name):
    e, m, b, arms, look, _ = LEO_POSES[name]
    return leo_front(e, m, b, arms, look)


def leo_head_only(eyes="open", mouth="smile"):
    body = _leo_head(100, 104, eyes, mouth, None)
    return svg_doc(body, 200, 180, "Leo head")
