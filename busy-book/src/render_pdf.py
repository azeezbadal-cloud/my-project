"""Render Page objects to a vector PDF with ReportLab (+ svglib for artwork)."""
import os
from reportlab import rl_config
from reportlab.pdfgen import canvas as rl_canvas

rl_config.useA85 = 0   # binary image streams (smaller PDFs)
from reportlab.lib.colors import HexColor
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from reportlab.graphics import shapes as _rl_shapes

_rl_shapes.STATE_DEFAULTS["fontName"] = "Nunito-Regular"   # no unused base-14 font references

import art_lib
from scene import FONTS

_cache = {}
PHOTOS = {}          # name -> raster file path, used by "photo:<name>" assets
SVG_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build", "svgcache")


def svg_path(asset):
    os.makedirs(SVG_CACHE, exist_ok=True)
    fn = os.path.join(SVG_CACHE, asset.replace(":", "__") + ".svg")
    if not os.path.exists(fn):
        with open(fn, "w") as f:
            f.write(art_lib.get_svg(asset))
    return fn


def drawing(asset):
    if asset not in _cache:
        _cache[asset] = svg2rlg(svg_path(asset))
    return _cache[asset]


def _col(c):
    return HexColor(c) if c else None


def _apply_line(c, e):
    if e.get("stroke"):
        c.setStrokeColor(_col(e["stroke"]))
        c.setLineWidth(e.get("sw", 1))
        c.setLineCap(1)
        c.setLineJoin(1)
    if e.get("dash"):
        c.setDash(*e["dash"])
    else:
        c.setDash()


def draw_page(c, p):
    H = p.H * 72

    def X(v):
        return v * 72

    def Y(v):
        return H - v * 72

    for e in p.els:
        t = e["t"]
        c.saveState()
        if t == "rect":
            if e["fill"]:
                c.setFillColor(_col(e["fill"]))
            _apply_line(c, e)
            x, y, w, h = X(e["x"]), Y(e["y"] + e["h"]), X(e["w"]), X(e["h"])
            st, fl = (1 if e["stroke"] else 0), (1 if e["fill"] else 0)
            if e["r"]:
                c.roundRect(x, y, w, h, X(e["r"]), stroke=st, fill=fl)
            else:
                c.rect(x, y, w, h, stroke=st, fill=fl)
        elif t == "ellipse":
            if e["fill"]:
                c.setFillColor(_col(e["fill"]))
            _apply_line(c, e)
            c.ellipse(X(e["x"]), Y(e["y"] + e["h"]), X(e["x"] + e["w"]), Y(e["y"]),
                      stroke=1 if e["stroke"] else 0, fill=1 if e["fill"] else 0)
        elif t == "line":
            _apply_line(c, e)
            c.line(X(e["x1"]), Y(e["y1"]), X(e["x2"]), Y(e["y2"]))
        elif t == "poly":
            if e["fill"]:
                c.setFillColor(_col(e["fill"]))
            _apply_line(c, e)
            path = c.beginPath()
            (x0, y0), rest = e["pts"][0], e["pts"][1:]
            path.moveTo(X(x0), Y(y0))
            for x, y in rest:
                path.lineTo(X(x), Y(y))
            if e["closed"]:
                path.close()
            c.drawPath(path, stroke=1 if e["stroke"] else 0, fill=1 if (e["fill"] and e["closed"]) else 0)
        elif t == "img" and "photo:" in e["asset"]:
            from reportlab.lib.utils import ImageReader
            ir = ImageReader(PHOTOS[e["asset"].split("photo:", 1)[1]])
            iw, ih = ir.getSize()
            bw, bh = X(e["w"]), X(e["h"])
            s_ = min(bw / iw, bh / ih)
            dw, dh = iw * s_, ih * s_
            x0, y0 = X(e["x"]) + (bw - dw) / 2, Y(e["y"] + e["h"]) + (bh - dh) / 2
            if e["rot"]:
                cx, cy = x0 + dw / 2, y0 + dh / 2
                c.translate(cx, cy)
                c.rotate(-e["rot"])
                c.translate(-cx, -cy)
            c.drawImage(ir, x0, y0, dw, dh, mask="auto")
        elif t == "img":
            d = drawing(e["asset"])
            bw, bh = X(e["w"]), X(e["h"])
            s = min(bw / d.width, bh / d.height)
            dw, dh = d.width * s, d.height * s
            if e["align"] == "bottom":
                ox, oy = (bw - dw) / 2, 0
            elif e["align"] == "top":
                ox, oy = (bw - dw) / 2, bh - dh
            else:
                ox, oy = (bw - dw) / 2, (bh - dh) / 2
            x0, y0 = X(e["x"]), Y(e["y"] + e["h"])
            if e["rot"]:
                cx, cy = x0 + bw / 2, y0 + bh / 2
                c.translate(cx, cy)
                c.rotate(-e["rot"])
                c.translate(-cx, -cy)
            c.translate(x0 + ox, y0 + oy)
            c.scale(s, s)
            renderPDF.draw(d, c, 0, 0)
        elif t == "text":
            fname = FONTS[e["font"]][0]
            size = e["size"]
            lh = size * e["leading"]
            th = len(e["lines"]) * lh
            top = X(e["y"])
            if e["valign"] == "middle":
                top += (X(e["h"]) - th) / 2
            elif e["valign"] == "bottom":
                top += X(e["h"]) - th
            for i, ln in enumerate(e["lines"]):
                base = H - (top + i * lh + (lh + size * 0.70) / 2)
                if e["align"] == "center":
                    tx = X(e["x"]) + X(e["w"]) / 2
                elif e["align"] == "right":
                    tx = X(e["x"] + e["w"])
                else:
                    tx = X(e["x"])
                for mode in (("outline",) if e.get("outline") else ()) + ("fill",):
                    to = c.beginText()
                    to.setFont(fname, size)
                    w = c.stringWidth(ln, fname, size)
                    sx = tx - (w / 2 if e["align"] == "center" else (w if e["align"] == "right" else 0))
                    to.setTextOrigin(sx, base)
                    if mode == "outline":
                        oc, ow = e["outline"]
                        c.setStrokeColor(_col(oc))
                        c.setLineWidth(ow)
                        c.setLineJoin(1)
                        to.setTextRenderMode(1)
                    else:
                        c.setFillColor(_col(e["color"]))
                        to.setTextRenderMode(0)
                    to.textLine(ln)
                    c.drawText(to)
        c.restoreState()


def render(pages, out_path, title, subject):
    c = rl_canvas.Canvas(out_path, pageCompression=1, initialFontName="Nunito-Regular", initialFontSize=10)
    c.setTitle(title)
    c.setAuthor("Little Worlds Learning")
    c.setSubject(subject)
    c.setCreator("Little Worlds Learning production pipeline")
    c.setKeywords("busy book, preschool, printable, ages 3-5")
    for p in pages:
        c.setPageSize((p.W * 72, p.H * 72))
        draw_page(c, p)
        c.showPage()
    c.save()
