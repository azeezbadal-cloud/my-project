"""Automated QA for My Magic Busy Book.

Each check returns (status, name, detail) with status PASS / FAIL / REVIEW.
Automated checks never replace human visual inspection: anything that needs
eyes is reported as NEEDS HUMAN REVIEW.
"""
import os
import re
import subprocess
from collections import Counter
from fontTools.ttLib import TTFont
from pypdf import PdfReader
from PIL import Image, ImageStat

import content as C
from scene import FONTS, FONT_DIR, text_width
from pages import PIECE, SLOT, SIZES

PASS, FAIL, REVIEW = "PASS", "FAIL", "NEEDS HUMAN REVIEW"
SMALL_PARTS_DIAMETER = 1.25  # in (31.7 mm small-parts test cylinder)

_cmaps = {}


def cmap(font):
    if font not in _cmaps:
        _cmaps[font] = TTFont(os.path.join(FONT_DIR, FONTS[font][1])).getBestCmap()
    return _cmaps[font]


def mission_pages(pages):
    return [p for p in pages if p.kind == "mission"]


# ------------------------------------------------------------------ structure
def check_structure(pages, ed):
    out = []
    nums = [p.number for p in pages]
    out.append((PASS if nums == list(range(1, 49)) else FAIL, f"[{ed}] exactly 48 pages, numbered 1-48", f"{len(pages)} pages built"))
    mp = mission_pages(pages)
    titles = [p.mission["title"] for p in mp]
    ok = len(mp) == 36 and len(set(titles)) == 36 and [p.number for p in mp] == list(range(5, 41))
    out.append((PASS if ok else FAIL, f"[{ed}] exactly 36 distinct mission pages on pages 5-40", f"{len(mp)} missions, {len(set(titles))} distinct titles"))
    missing = [m["n"] for m in C.MISSIONS if not (m["title"] and m["instr"] and m["goal"] and m["guide"])]
    out.append((PASS if not missing else FAIL, f"[{ed}] every mission has title, instruction, objective and adult guidance", f"missing: {missing}" if missing else "36/36 complete"))
    sheets = [p for p in pages if p.kind == "pieces"]
    out.append((PASS if [p.number for p in sheets] == [41, 42, 43, 44, 45] else FAIL, f"[{ed}] five cut-out sheets on pages 41-45", str([p.number for p in sheets])))
    return out


# ------------------------------------------------------------------ pieces / slots
def _matching(slots, pieces):
    """Max bipartite matching slots -> distinct pieces."""
    match = {}

    def try_(i, seen):
        for pid in slots[i]["accepts"]:
            if pid in pieces and pid not in seen:
                seen.add(pid)
                if pid not in match or try_(match[pid], seen):
                    match[pid] = i
                    return True
        return False

    return sum(1 for i in range(len(slots)) if try_(i, set())), match


def check_pieces(pages, ed):
    out = []
    inv = [pid for s in C.PIECE_SETS for pid, _, _ in s["items"]]
    dup = [k for k, v in Counter(inv).items() if v > 1]
    out.append((PASS if not dup else FAIL, f"[{ed}] all piece IDs unique", f"{len(inv)} piece IDs; duplicates: {dup or 'none'}"))
    printed = [pc["id"] for p in pages for pc in p.pieces]
    pc_dup = [k for k, v in Counter(printed).items() if v > 1]
    missing_print = sorted(set(inv) - set(printed))
    out.append((PASS if not pc_dup and not missing_print and len(printed) == len(inv) else FAIL,
                f"[{ed}] every inventory piece printed exactly once on the cut-out sheets",
                f"{len(printed)} printed; missing {missing_print or 'none'}; duplicated {pc_dup or 'none'}"))
    used = {pid for m in C.MISSIONS for pid in m["pieces"]}
    orphans = sorted(set(inv) - used)
    unknown = sorted(used - set(inv))
    out.append((PASS if not orphans else FAIL, f"[{ed}] no orphan pieces (every piece used by a mission)", f"orphans: {orphans or 'none'}"))
    out.append((PASS if not unknown else FAIL, f"[{ed}] every required piece ID exists", f"unknown: {unknown or 'none'}"))
    problems, solv = [], []
    for p in mission_pages(pages):
        m = p.mission
        req = set(m["pieces"])
        if not req:
            if p.slots:
                problems.append(f"M{m['n']:02d} is no-cut but has slots")
            if not p.answers:
                problems.append(f"M{m['n']:02d} no-cut mission has no recorded answers")
            continue
        if not p.slots:
            problems.append(f"M{m['n']:02d} has pieces but no board slots")
            continue
        acc = set(x for s in p.slots for x in s["accepts"])
        if acc - req:
            problems.append(f"M{m['n']:02d} slots accept pieces not listed for the mission: {sorted(acc - req)}")
        if req - acc:
            problems.append(f"M{m['n']:02d} pieces with no place on the board: {sorted(req - acc)}")
        n, _ = _matching(p.slots, req)
        if n != len(p.slots):
            problems.append(f"M{m['n']:02d} unsolvable: only {n}/{len(p.slots)} slots can be filled with distinct pieces")
        else:
            solv.append(m["n"])
    out.append((PASS if not problems else FAIL, f"[{ed}] boards <-> pieces mapping complete and every board solvable",
                "; ".join(problems) if problems else f"{len(solv)} piece missions solvable (bipartite matching), {sum(1 for m in C.MISSIONS if not m['pieces'])} no-cut missions with answers"))
    return out


def check_fit(pages, ed):
    out = []
    W, H = SIZES[ed]
    bad, small = [], []
    for p in pages:
        for pc in p.pieces:
            if pc["x"] < 0.4 or pc["y"] < 0.4 or pc["x"] + pc["w"] > W - 0.4 or pc["y"] + pc["h"] > H - 0.4:
                bad.append(f"{pc['id']} p{p.number}")
            if min(pc["w"], pc["h"]) < 1.5:
                small.append(pc["id"])
        ps = p.pieces
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                a, b = ps[i], ps[j]
                gx = max(b["x"] - (a["x"] + a["w"]), a["x"] - (b["x"] + b["w"]))
                gy = max(b["y"] - (a["y"] + a["h"]), a["y"] - (b["y"] + b["h"]))
                if max(gx, gy) < 0.25:
                    bad.append(f"{a['id']}/{b['id']} spacing {max(gx, gy):.2f}in")
    out.append((PASS if not bad else FAIL, f"[{ed}] all cut-out pieces inside the 0.4in safe area with >=0.25in cutting space, no overlapping cut lines",
                "; ".join(bad) if bad else f"piece {PIECE}in square, gap >= 0.25in, all inside safe area"))
    out.append((PASS if not small and PIECE > SMALL_PARTS_DIAMETER else FAIL, f"[{ed}] no detachable piece smaller than 1.5in (small-parts cylinder is 1.25in)",
                f"smallest piece {PIECE}in x {PIECE}in"))
    sb = []
    for p in pages:
        for s in p.slots:
            if s["w"] < PIECE + 0.04 or s["h"] < PIECE + 0.04:
                sb.append(f"p{p.number} slot {s['w']:.2f}x{s['h']:.2f}")
            if s["x"] < 0.4 or s["y"] < 0.4 or s["x"] + s["w"] > W - 0.4 or s["y"] + s["h"] > H - 0.4:
                sb.append(f"p{p.number} slot outside safe area")
    out.append((PASS if not sb else FAIL, f"[{ed}] every board slot is large enough for its card and inside the safe area",
                "; ".join(sb) if sb else f"{sum(len(p.slots) for p in pages)} slots checked (min {min(min(s['w'], s['h']) for p in pages for s in p.slots):.2f}in vs card {PIECE}in)"))
    return out


# ------------------------------------------------------------------ numbers
def check_numbers(pages, ed):
    out, errs = [], []
    by = {p.number: p for p in pages}

    def count(p, gid):
        return sum(1 for e in p.els if e.get("group") == gid)

    for p in pages:
        for gid, n in p.groups.items():
            if count(p, gid) != n:
                errs.append(f"p{p.number} {gid}: drawn {count(p, gid)} != expected {n}")
    # number cards: dots == numeral
    for p in pages:
        for pc in p.pieces:
            if pc["set"] == "NU":
                n = int(pc["id"][2:])
                if count(p, f"card_{pc['id']}") != n:
                    errs.append(f"{pc['id']} dots mismatch")
    # Mission 14 balloons
    p = by[18]
    for i, n in enumerate(C.BALLOON_COUNTS):
        if count(p, f"balloons_{i + 1}") != n:
            errs.append(f"M14 bunch {i + 1}")
        if p.slots[i]["accepts"] != [f"NU{n}"]:
            errs.append(f"M14 slot {i + 1} expects {p.slots[i]['accepts']} for {n} balloons")
    # Mission 16 cupcakes
    p = by[20]
    for i, n in enumerate(C.CUPCAKE_COUNTS):
        if count(p, f"tray_{i + 1}") != n or p.slots[i]["accepts"] != [f"NU{n}"]:
            errs.append(f"M16 tray {i + 1}")
    # Mission 15 monster orders <= cookies available and dots match
    p = by[19]
    if max(C.MONSTER_ORDERS) > len([x for x in C.MISSIONS[14]["pieces"]]):
        errs.append("M15 order larger than cookies available")
    if len(p.slots) < max(C.MONSTER_ORDERS):
        errs.append("M15 plate has fewer spots than largest order")
    # Mission 17 more/less answers consistent with drawn counts
    p = by[21]
    for i, (a, l, r) in enumerate(C.MORE_LESS):
        cl, cr = count(p, f"row{i + 1}_L"), count(p, f"row{i + 1}_R")
        exp = "left" if cl > cr else "right"
        if cl == cr or p.answers[i][1] != exp or (cl, cr) != (l, r):
            errs.append(f"M17 row {i + 1}: drawn {cl} vs {cr}, answer {p.answers[i][1]}")
    # Mission 18 tower helper dots
    p = by[22]
    for n in range(1, 6):
        if count(p, f"helper_{n}") != n:
            errs.append(f"M18 helper {n}")
    # Mission 36 apples -> NU4
    p = by[40]
    ap = count(p, "finale_apples")
    nslot = [s for s in p.slots if any(x.startswith("NU") for x in s["accepts"])]
    if ap != C.FINALE_APPLES or not nslot or nslot[0]["accepts"] != [f"NU{ap}"]:
        errs.append(f"M36 apples {ap} vs slot {nslot[0]['accepts'] if nslot else None}")
    # Mission 13/18 sequence
    p13 = [s["accepts"][0] for s in by[17].slots]
    if p13 != [f"NU{i}" for i in range(1, 11)]:
        errs.append(f"M13 order {p13}")
    ngroups = sum(len(p.groups) for p in pages)
    out.append((PASS if not errs else FAIL, f"[{ed}] number answers match pictured quantities",
                "; ".join(errs) if errs else f"{ngroups} counted groups verified (balloons, cupcakes, cookies orders, card dots, comparison rows, tower helpers, finale apples)"))
    return out


def check_patterns():
    errs = []
    for i, (seq, ans, choices) in enumerate(C.PATTERNS):
        ok = False
        for k in (2, 3):
            unit = seq[:k]
            if all(seq[j] == unit[j % k] for j in range(len(seq))) and len(set(unit)) > 1:
                ok = unit[len(seq) % k] == ans
                break
        if not ok or ans not in choices or len(set(choices)) != 3:
            errs.append(f"pattern {i + 1}")
    fl = Counter(C.FLOWERS)
    if set(fl) != set(C.POTS):
        errs.append("M04 flower colours do not match pot colours")
    for a, nm, food, lab in C.FOODS:
        pass
    if sorted(C.FOOD_ORDER) != list(range(len(C.FOODS))) or sorted(C.FEELING_ORDER) != list(range(len(C.FEELINGS))) or sorted(C.KIND_ORDER) != list(range(len(C.KINDNESS))):
        errs.append("draw-a-line orders are not permutations")
    if any(C.FOOD_ORDER[i] == i for i in range(len(C.FOODS))):
        errs.append("M08: an answer sits directly opposite its animal")
    for (a1, a2, ans, ch) in C.SEQUENCES:
        if ans not in ch:
            errs.append(f"sequence {a1}: answer not offered")
    return [(PASS if not errs else FAIL, "AB / AAB patterns, sequences and matching orders are logically correct",
             "; ".join(errs) if errs else f"{len(C.PATTERNS)} patterns solved programmatically; every answer offered exactly once among 3 choices; line-matching columns are shuffled")]


# ------------------------------------------------------------------ text
def check_text(pages, ed):
    out = []
    W, H = SIZES[ed]
    miss, small, outside, overl = [], [], [], []
    for p in pages:
        texts = [e for e in p.els if e["t"] == "text"]
        for e in texts:
            cm = cmap(e["font"])
            bad = {ch for ch in e["s"] if ch != "\n" and ord(ch) not in cm}
            if bad:
                miss.append(f"p{p.number} '{e['s'][:20]}' {sorted(bad)}")
            if e["size"] < 6:
                small.append(f"p{p.number} {e['size']}pt '{e['s'][:20]}'")
            if p.kind == "mission" and e["s"] == p.mission["instr"] and e["size"] < 12:
                small.append(f"p{p.number} instruction {e['size']}pt")
            if p.kind not in ("cover", "back") and (e["x"] < 0.39 or e["y"] < 0.39 or e["x"] + e["w"] > W - 0.39 or e["y"] + e["h"] > H - 0.39):
                outside.append(f"p{p.number} '{e['s'][:20]}'")
        # overlap between rendered text extents
        boxes = []
        for e in texts:
            lh = e["size"] * e["leading"] / 72
            th = len(e["lines"]) * lh
            top = e["y"] + {"top": 0, "middle": (e["h"] - th) / 2, "bottom": e["h"] - th}[e["valign"]]
            lw = max(text_width(ln, e["font"], e["size"]) for ln in e["lines"])
            left = e["x"] + {"left": 0, "center": (e["w"] - lw) / 2, "right": e["w"] - lw}[e["align"]]
            boxes.append((left, top + lh * 0.12, left + lw, top + th - lh * 0.12, e["s"][:18]))
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if a[0] < b[2] - 0.01 and b[0] < a[2] - 0.01 and a[1] < b[3] - 0.01 and b[1] < a[3] - 0.01:
                    overl.append(f"p{p.number} '{a[4]}' / '{b[4]}'")
    warn = [w for p in pages for w in p.warnings if "overflow" in w]
    out.append((PASS if not miss else FAIL, f"[{ed}] every character exists in its font (no missing glyphs)", "; ".join(miss) if miss else "all text glyphs present in Fredoka / Nunito"))
    out.append((PASS if not warn else FAIL, f"[{ed}] no clipped text (all text fits its box)", "; ".join(warn) if warn else "no overflow after layout"))
    out.append((PASS if not overl else FAIL, f"[{ed}] no overlapping text", "; ".join(overl[:10]) if overl else "pairwise check of rendered text extents"))
    out.append((PASS if not outside else FAIL, f"[{ed}] all interior text inside the 0.4in safe area", "; ".join(outside[:10]) if outside else "ok"))
    sizes = [e["size"] for p in pages for e in p.els if e["t"] == "text"]
    child = [e["size"] for p in mission_pages(pages) for e in p.els if e["t"] == "text" and e["y"] < p.H - 0.9 and e["font"] == "title"]
    out.append((PASS if not small else FAIL, f"[{ed}] no unreadably small text (min 6pt adult notes; mission instructions >= 12pt)",
                ("; ".join(small) if small else f"smallest text {min(sizes):.1f}pt (adult reference table); smallest child-facing heading {(min(child) if child else min(sizes)):.1f}pt")))
    return out


def check_spelling(pages):
    words = Counter()
    for p in pages:
        for e in p.els:
            if e["t"] == "text":
                for w in re.findall(r"[A-Za-z]{2,}", e["s"]):
                    words[w.lower()] += 1
    try:
        from spellchecker import SpellChecker
        spell = SpellChecker(language="en")
        allowed = {"leo", "fredoka", "nunito", "colour", "colours", "favourite", "favourites", "organise", "labelled", "gsm", "laminate", "laminated",
                   "jumper", "cosy", "busy", "dry", "erase", "rd", "sh", "nu", "an", "ic", "rb", "ap", "fm", "oc", "tr", "we", "fa", "rt", "td", "sm",
                   "ho", "ch", "ve", "tm", "ca", "mp", "pg", "boop", "oink", "quack", "cluck", "yum", "letter", "tajawal", "ok", "tidy", "worlds"}
        unk = sorted(w for w in spell.unknown(list(words)) if w not in allowed)
        return [(REVIEW, "spelling and grammar", f"pyspellchecker (en) run on all {len(words)} distinct words in the book: flagged {len(unk)} for review: {', '.join(unk) or 'none'}. Grammar was not machine-checked.")], sorted(words)
    except ImportError:
        pass
    dict_path = "/usr/share/dict/words"
    if not os.path.exists(dict_path):
        return [(REVIEW, "spelling and grammar", f"No dictionary available; {len(words)} distinct words listed in Spelling_Wordlist.txt for human proofreading")], sorted(words)
    known = set(w.strip().lower() for w in open(dict_path))
    unk = sorted(w for w in words if w not in known)
    return [(REVIEW, "spelling and grammar", f"dictionary check: {len(unk)} words not in system dictionary: {', '.join(unk)}")], sorted(words)


# ------------------------------------------------------------------ PDF
def check_pdf(path, ed, pages, render_dir):
    out = []
    r = PdfReader(path)
    W, H = SIZES[ed]
    dims = {(round(float(pg.mediabox.width), 1), round(float(pg.mediabox.height), 1)) for pg in r.pages}
    exp = (round(W * 72, 1), round(H * 72, 1))
    out.append((PASS if len(r.pages) == 48 else FAIL, f"[{ed}] PDF has exactly 48 pages", f"{os.path.basename(path)}: {len(r.pages)} pages"))
    out.append((PASS if dims == {exp} else FAIL, f"[{ed}] PDF page size verified programmatically", f"all pages {sorted(dims)} pt; expected {exp} pt"))
    fonts, unemb = set(), set()
    missing_text = []
    for i, pg in enumerate(r.pages):
        res = pg.get("/Resources") or {}
        for _, f in (res.get("/Font") or {}).items():
            f = f.get_object()
            name = str(f.get("/BaseFont"))
            fonts.add(name.split("+")[-1])
            desc = f.get("/FontDescriptor")
            if desc is None and "/DescendantFonts" in f:
                desc = f["/DescendantFonts"][0].get_object().get("/FontDescriptor")
            if desc is not None:
                d = desc.get_object()
                if not any(k in d for k in ("/FontFile", "/FontFile2", "/FontFile3")):
                    unemb.add(name)
        txt = pg.extract_text() or ""
        p = pages[i]
        key = (p.mission["title"] if p.kind == "mission" else {"pieces": "CUT-OUT SHEET", "cover": "BUSY BOOK", "intro": "", "reference": "GROWN-UP", "certificate": "CERTIFICATE", "back": "LITTLE WORLDS"}[p.kind])
        norm = re.sub(r"\s+", " ", txt).upper()
        if len(txt.strip()) < 15 or (key and key.upper().split(":")[0] not in norm):
            missing_text.append(f"p{i + 1}")
    out.append((PASS if not unemb else FAIL, f"[{ed}] all fonts embedded", f"embedded: {', '.join(sorted(fonts))}"))
    out.append((PASS if not missing_text else FAIL, f"[{ed}] text extraction finds the expected title text on every page", ", ".join(missing_text) if missing_text else "48/48 pages"))
    os.makedirs(render_dir, exist_ok=True)
    subprocess.run(["pdftoppm", "-r", "60", "-png", path, os.path.join(render_dir, "page")], check=True)
    blank, n = [], 0
    for f in sorted(os.listdir(render_dir)):
        if f.endswith(".png"):
            n += 1
            st = ImageStat.Stat(Image.open(os.path.join(render_dir, f)).convert("L"))
            if st.stddev[0] < 8:
                blank.append(f)
    out.append((PASS if n == 48 and not blank else FAIL, f"[{ed}] every page renders (no corrupted or blank pages)", f"{n} pages rasterised with pdftoppm; blank: {blank or 'none'}"))
    return out
