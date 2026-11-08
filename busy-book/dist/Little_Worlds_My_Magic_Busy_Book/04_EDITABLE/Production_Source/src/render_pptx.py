"""Render Page objects to an editable PowerPoint (Canva-importable).

* Titles, instructions, labels, numbers and notes -> native text boxes
* Boxes, slots, cut lines, dots, paths            -> native shapes / freeforms
* Illustrations                                    -> one transparent PNG per
  artwork, rendered from the SVG master (originals kept in 03_ILLUSTRATIONS)
"""
import hashlib
import os
import cairosvg
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE
from pptx.oxml.ns import qn
from lxml import etree

import art_lib
from scene import FONTS

EMU = 914400
PNG_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build", "pngcache")


def E(v):
    return Emu(int(round(v * EMU)))


def rgb(c):
    c = c.lstrip("#")
    return RGBColor(int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))


def _strip_style(shape):
    st = shape._element.find(qn("p:style"))
    if st is not None:
        shape._element.remove(st)


def _fill_line(shape, e):
    if e.get("fill"):
        shape.fill.solid()
        shape.fill.fore_color.rgb = rgb(e["fill"])
    else:
        shape.fill.background()
    if e.get("stroke"):
        shape.line.color.rgb = rgb(e["stroke"])
        shape.line.width = Pt(e.get("sw", 1))
        if e.get("dash"):
            shape.line.dash_style = MSO_LINE.DASH
    else:
        shape.line.fill.background()


def png_for(asset, inches):
    os.makedirs(PNG_CACHE, exist_ok=True)
    px = int(min(3000, max(300, inches * 300)))
    key = hashlib.md5(f"{asset}|{px}".encode()).hexdigest()[:10]
    fn = os.path.join(PNG_CACHE, f"{asset.replace(':', '__')}_{px}_{key}.png")
    if not os.path.exists(fn):
        svg = art_lib.get_svg(asset)
        w, h = art_lib.get_size(asset)
        if w >= h:
            cairosvg.svg2png(bytestring=svg.encode(), write_to=fn, output_width=px)
        else:
            cairosvg.svg2png(bytestring=svg.encode(), write_to=fn, output_height=px)
    return fn


def render(pages, out_path, notes=None):
    prs = Presentation()
    prs.slide_width = E(pages[0].W)
    prs.slide_height = E(pages[0].H)
    blank = prs.slide_layouts[6]
    # largest use of each asset -> one PNG per asset
    maxsz = {}
    for p in pages:
        for e in p.els:
            if e["t"] == "img":
                maxsz[e["asset"]] = max(maxsz.get(e["asset"], 0), e["w"], e["h"])
    for p in pages:
        s = prs.slides.add_slide(blank)
        for e in p.els:
            t = e["t"]
            if t in ("rect", "ellipse"):
                kind = MSO_SHAPE.OVAL if t == "ellipse" else (MSO_SHAPE.ROUNDED_RECTANGLE if e.get("r") else MSO_SHAPE.RECTANGLE)
                sh = s.shapes.add_shape(kind, E(e["x"]), E(e["y"]), E(e["w"]), E(e["h"]))
                if kind == MSO_SHAPE.ROUNDED_RECTANGLE:
                    sh.adjustments[0] = min(0.5, e["r"] / max(min(e["w"], e["h"]), 1e-6))
                _strip_style(sh)
                _fill_line(sh, e)
                if e.get("role") == "slot":
                    sh.name = "Slot (place piece here)"
                elif e.get("role") == "cut":
                    sh.name = f"Cut line {e.get('name') or ''}".strip()
            elif t == "line":
                sh = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(e["x1"]), E(e["y1"]), E(e["x2"]), E(e["y2"]))
                _strip_style(sh)
                sh.line.color.rgb = rgb(e["stroke"])
                sh.line.width = Pt(e["sw"])
                if e.get("dash"):
                    sh.line.dash_style = MSO_LINE.DASH
            elif t == "poly":
                pts = e["pts"]
                b = s.shapes.build_freeform(E(pts[0][0]), E(pts[0][1]), scale=1.0)
                b.add_line_segments([(E(x), E(y)) for x, y in pts[1:]], close=e["closed"])
                sh = b.convert_to_shape()
                _strip_style(sh)
                _fill_line(sh, dict(e, fill=e["fill"] if e["closed"] else None))
            elif t == "img":
                aw, ah = art_lib.get_size(e["asset"])
                sc = min(e["w"] / aw, e["h"] / ah)
                dw, dh = aw * sc, ah * sc
                ox = (e["w"] - dw) / 2
                oy = {"bottom": e["h"] - dh, "top": 0}.get(e["align"], (e["h"] - dh) / 2)
                pic = s.shapes.add_picture(png_for(e["asset"], maxsz[e["asset"]]), E(e["x"] + ox), E(e["y"] + oy), E(dw), E(dh))
                pic.name = f"Art: {e['asset']}"
                if e.get("rot"):
                    pic.rotation = e["rot"]
            elif t == "text":
                tb = s.shapes.add_textbox(E(e["x"]), E(e["y"]), E(e["w"]), E(e["h"]))
                tb.name = f"Text: {e['s'][:30]}"
                tf = tb.text_frame
                tf.word_wrap = True
                tf.auto_size = None
                tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
                tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[e["valign"]]
                fam, bold = FONTS[e["font"]][2], FONTS[e["font"]][3]
                for i, para in enumerate(e["s"].split("\n")):
                    par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                    par.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}[e["align"]]
                    par.line_spacing = e["leading"] * 0.85
                    r = par.add_run()
                    r.text = para
                    f = r.font
                    f.name = fam
                    f.size = Pt(e["size"])
                    f.bold = bold
                    f.color.rgb = rgb(e["color"])
                    if e.get("outline"):
                        oc, ow = e["outline"]
                        rPr = r._r.get_or_add_rPr()
                        ln = etree.SubElement(rPr, qn("a:ln"), w=str(int(ow * 12700)))
                        sf = etree.SubElement(ln, qn("a:solidFill"))
                        etree.SubElement(sf, qn("a:srgbClr"), val=oc.lstrip("#"))
                        rPr.insert(0, ln)
        if notes and p.number in notes:
            s.notes_slide.notes_text_frame.text = notes[p.number]
    prs.core_properties.title = "My Magic Busy Book - editable master"
    prs.core_properties.author = "Little Worlds Learning"
    prs.save(out_path)
