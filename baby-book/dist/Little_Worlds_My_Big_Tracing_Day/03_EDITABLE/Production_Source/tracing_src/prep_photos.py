"""Derive book-ready photo assets from the AI-generated originals (originals are kept untouched)."""
import os
from PIL import Image, ImageDraw, ImageFilter

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "photos")
OUT = os.path.join(SRC, "derived")
os.makedirs(OUT, exist_ok=True)


def circle(im, box, size, name):
    c = im.crop(box).resize((size, size), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(m).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
    c.putalpha(m.resize((size, size), Image.LANCZOS))
    c.save(os.path.join(OUT, name + ".png"), optimize=True)


trio = Image.open(os.path.join(SRC, "trio_v1.png")).convert("RGB")
# soften the AI-made wall sign (top right) so no stray text appears in the book
box = (1230, 0, 1536, 250)
big = trio.filter(ImageFilter.GaussianBlur(16))
mask = Image.new("L", trio.size, 0)
ImageDraw.Draw(mask).rounded_rectangle(box, radius=70, fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(30))
trio = Image.composite(big, trio, mask)
trio.save(os.path.join(OUT, "cover_trio.jpg"), quality=92)
circle(trio, (77, 27, 587, 537), 620, "portrait_mia")
circle(trio, (532, 27, 1042, 537), 620, "portrait_leo")
circle(trio, (982, 62, 1482, 562), 620, "portrait_kai")
for s in ("morning", "breakfast", "park", "bath", "bedtime"):
    im = Image.open(os.path.join(SRC, f"scene_{s}.png")).convert("RGB")
    im.save(os.path.join(OUT, f"scene_{s}.jpg"), quality=92)
    w, h = im.size
    circle(im, ((w - h) // 2, 0, (w + h) // 2, h), 460, f"scene_{s}_circle")
print(sorted(os.listdir(OUT)))
