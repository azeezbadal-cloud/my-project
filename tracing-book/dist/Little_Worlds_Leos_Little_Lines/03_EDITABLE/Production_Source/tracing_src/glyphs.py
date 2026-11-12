"""Tracing paths: uppercase letters, digits, shapes and line patterns.

Glyph strokes live in a 100 x 100 box (x right, y down), drawn in a simple
print-style handwriting order (top to bottom, left to right). Each stroke is a
list of points; stroke order = list order.
"""
import math


def arc(cx, cy, rx, ry, a0, a1, n=None):
    n = n or max(8, int(abs(a1 - a0) / 6))
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def L(*pts):
    return list(pts)


LETTERS = {
    "A": [L((50, 0), (12, 100)), L((50, 0), (88, 100)), L((27, 62), (73, 62))],
    "B": [L((18, 0), (18, 100)), L((18, 0), (52, 0)) + arc(52, 24, 26, 24, -90, 90) + L((18, 48)),
          L((18, 48), (56, 48)) + arc(56, 74, 30, 26, -90, 90) + L((18, 100))],
    "C": [arc(54, 50, 42, 50, -40, -320)],
    "D": [L((18, 0), (18, 100)), L((18, 0), (40, 0)) + arc(40, 50, 44, 50, -90, 90) + L((18, 100))],
    "E": [L((82, 0), (18, 0), (18, 100), (82, 100)), L((18, 50), (68, 50))],
    "F": [L((82, 0), (18, 0), (18, 100)), L((18, 50), (68, 50))],
    "G": [arc(52, 50, 42, 50, -40, -360), L((94, 52), (60, 52))],
    "H": [L((16, 0), (16, 100)), L((84, 0), (84, 100)), L((16, 50), (84, 50))],
    "I": [L((50, 0), (50, 100)), L((26, 0), (74, 0)), L((26, 100), (74, 100))],
    "J": [L((30, 0), (84, 0)), L((66, 0), (66, 70)) + arc(42, 70, 24, 30, 0, 170)],
    "K": [L((18, 0), (18, 100)), L((84, 0), (18, 58)), L((38, 40), (86, 100))],
    "L": [L((20, 0), (20, 100), (82, 100))],
    "M": [L((10, 100), (10, 0), (50, 62), (90, 0), (90, 100))],
    "N": [L((16, 100), (16, 0), (84, 100), (84, 0))],
    "O": [arc(50, 50, 42, 50, -90, -450)],
    "P": [L((18, 0), (18, 100)), L((18, 0), (54, 0)) + arc(54, 26, 28, 26, -90, 90) + L((18, 52))],
    "Q": [arc(50, 50, 42, 50, -90, -450), L((60, 70), (92, 104))],
    "R": [L((18, 0), (18, 100)), L((18, 0), (54, 0)) + arc(54, 26, 28, 26, -90, 90) + L((18, 52)), L((46, 52), (86, 100))],
    "S": [arc(50, 26, 34, 25, -15, -270) + arc(50, 75, 36, 25, -90, 165)[1:]],
    "T": [L((10, 0), (90, 0)), L((50, 0), (50, 100))],
    "U": [L((16, 0), (16, 62)) + arc(50, 62, 34, 38, 180, 0) + L((84, 0))],
    "V": [L((10, 0), (50, 100), (90, 0))],
    "W": [L((4, 0), (27, 100), (50, 32), (73, 100), (96, 0))],
    "X": [L((14, 0), (86, 100)), L((86, 0), (14, 100))],
    "Y": [L((12, 0), (50, 50), (50, 100)), L((88, 0), (50, 50))],
    "Z": [L((16, 0), (84, 0), (16, 100), (84, 100))],
}

DIGITS = {
    "0": [arc(50, 50, 38, 50, -90, -450)],
    "1": [L((30, 20), (55, 0), (55, 100))],
    "2": [arc(50, 28, 32, 28, -165, 35) + L((15, 100), (86, 100))],
    "3": [arc(48, 26, 32, 25, -160, 90)[:-1] + arc(48, 75, 36, 25, -90, 160)],
    "4": [L((64, 0), (12, 66), (90, 66)), L((64, 22), (64, 100))],
    "5": [L((80, 0), (26, 0), (23, 46)) + arc(48, 70, 36, 30, -130, 150)],
    "6": [L((70, 2), (24, 58)) + arc(50, 70, 30, 30, 180, -180)],
    "7": [L((14, 0), (86, 0), (40, 100))],
    "8": [arc(50, 25, 26, 25, 90, -270), arc(50, 74, 32, 26, -90, 270)],
    "9": [arc(50, 30, 30, 30, 0, -360), L((80, 30), (76, 100))],
}


def glyph(ch):
    if ch in LETTERS:
        return LETTERS[ch]
    if ch == "10":
        one = [[(x * 0.5 - 4, y) for x, y in s] for s in DIGITS["1"]]
        zero = [[(48 + x * 0.55, y) for x, y in s] for s in DIGITS["0"]]
        return one + zero
    return DIGITS[ch]


# ----------------------------------------------------------------- shapes (unit box -1..1, start point first)
def shape_points(kind):
    if kind == "circle":
        return arc(0, 0, 1, 1, -90, 270, 64)
    if kind == "oval":
        return arc(0, 0, 0.72, 1, -90, 270, 64)
    if kind == "square":
        return [(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)]
    if kind == "rectangle":
        return [(-1, -0.6), (1, -0.6), (1, 0.6), (-1, 0.6), (-1, -0.6)]
    if kind == "triangle":
        return [(0, -1), (1, 0.85), (-1, 0.85), (0, -1)]
    if kind == "diamond":
        return [(0, -1), (0.75, 0), (0, 1), (-0.75, 0), (0, -1)]
    if kind == "star":
        pts = []
        for i in range(11):
            a = math.radians(-90 + i * 36)
            r = 1 if i % 2 == 0 else 0.45
            pts.append((r * math.cos(a), r * math.sin(a) + 0.08))
        return pts
    if kind == "heart":
        pts = []
        for i in range(73):
            t = math.radians(i * 5)
            x = 16 * math.sin(t) ** 3
            y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            pts.append((x / 17, (y + 2) / 17))
        return pts[0:1] + pts[1:]
    raise ValueError(kind)


# ----------------------------------------------------------------- line patterns: f(t) -> offset in [-1, 1]
def pattern(kind, t):
    if kind == "straight":
        return 0.0
    if kind == "wave":
        return 0.8 * math.sin(2 * math.pi * 2 * t)
    if kind == "zigzag":
        k = (t * 4) % 1
        return 0.8 * (4 * abs(k - 0.5) - 1)
    if kind == "bumps":
        return 0.8 - 1.6 * abs(math.sin(math.pi * 3 * t))
    if kind == "diag_down":
        return -0.8 + 1.6 * t
    if kind == "diag_up":
        return 0.8 - 1.6 * t
    raise ValueError(kind)


def pattern_points(kind, x0, x1, y, amp, n=120):
    if kind == "loops":
        loops, r = 4, amp
        out = []
        for i in range(n * 2 + 1):
            u = i / (n * 2)
            out.append((x0 + (x1 - x0) * u - r * 0.9 * math.sin(2 * math.pi * loops * u), y - r * math.cos(2 * math.pi * loops * u) + r * 0.0))
        return out
    return [(x0 + (x1 - x0) * i / n, y + amp * pattern(kind, i / n)) for i in range(n + 1)]


def spiral_points(cx, cy, r, turns=2.5, n=160):
    return [(cx + r * (i / n) * math.cos(2 * math.pi * turns * i / n), cy + r * (i / n) * math.sin(2 * math.pi * turns * i / n)) for i in range(n + 1)]


def catmull(pts, n=18):
    out = []
    p = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(pts[-1])
    return out


def path_length(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
