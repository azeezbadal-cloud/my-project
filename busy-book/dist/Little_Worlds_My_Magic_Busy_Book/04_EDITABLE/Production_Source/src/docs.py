"""Supporting publisher + customer documents (all generated from content.py)."""
import csv
import json
import os

import art_lib
import art_core as A
import content as C
from scene import Page, text_width
from pages import Book, PIECE, SLOT, M, centers
from art_core import NAVY, YELLOW, SKY, LIME, CORAL, PINK, CREAM, WHITE

MUTED = "#5B6B78"


def _page(n, W=8.5, H=11.0, kind="doc"):
    p = Page(n, W, H, kind, "US_Letter")
    return p


def _foot(p, label):
    p.text(f"{label}  ·  Little Worlds Learning  ·  {C.PRODUCT['version']}", M, p.H - 0.75, p.W - 2 * M - 0.5, 0.26, "bold", 8, MUTED, valign="middle")
    p.text(str(p.number), p.W - M - 0.4, p.H - 0.75, 0.4, 0.26, "title", 10, NAVY, align="right", valign="middle")


# ======================================================================= brand guide
def brand_guide_pages():
    ps = []
    # 1 - identity
    p = _page(1)
    p.rect(0, 0, 8.5, 3.6, fill=SKY)
    p.text("LITTLE WORLDS LEARNING", M, 0.6, 7.5, 0.7, "title", 34, NAVY, align="center", valign="middle")
    p.text("Brand Guide  ·  Product 03: My Magic Busy Book", M, 1.3, 7.5, 0.4, "bold", 15, NAVY, align="center", valign="middle")
    p.text(C.PRODUCT["tagline"], M, 1.75, 7.5, 0.4, "title", 18, WHITE, align="center", valign="middle")
    p.img("leo_wave", 3.25, 2.15, 2.0, 2.5)
    y = 4.9
    p.text("BRAND COLOURS", M, y, 7.5, 0.4, "title", 16, NAVY)
    y += 0.5
    for i, (name, hx) in enumerate(C.BRAND_COLOURS.items()):
        x = M + (i % 4) * 1.9
        yy = y + (i // 4) * 1.35
        p.rect(x, yy, 1.75, 0.8, fill=hx, stroke=NAVY if hx in ("#FFFFFF", "#FFF9EA") else None, sw=1, r=0.12)
        p.text(name, x, yy + 0.84, 1.75, 0.22, "xbold", 9, NAVY)
        p.text(hx, x, yy + 1.04, 1.75, 0.2, "body", 8.5, NAVY)
    y += 2.85
    p.text("SUPPORTING COLOURS (activity colours, Leo, chapter 6)", M, y, 7.5, 0.3, "title", 12, NAVY)
    y += 0.4
    for i, (name, hx) in enumerate(C.SUPPORT_COLOURS.items()):
        x = M + (i % 5) * 1.5
        yy = y + (i // 5) * 0.95
        p.rect(x, yy, 0.5, 0.5, fill=hx, r=0.08)
        p.text(f"{name}\n{hx}", x + 0.56, yy - 0.02, 0.92, 0.6, "body", 7, NAVY, leading=1.1)
    _foot(p, "Brand Guide")
    ps.append(p)
    # 2 - typography + icon system + design rules
    p = _page(2)
    p.text("TYPOGRAPHY", M, M, 7.5, 0.45, "title", 20, NAVY)
    rows = [("title", 30, "Fredoka Bold – covers & activity titles"), ("bold", 16, "Nunito Bold – instructions and numbers"),
            ("body", 12, "Nunito Regular – parent notes and guidance"), ("xbold", 10, "Nunito ExtraBold – small labels, piece IDs")]
    y = 1.05
    for f, s, lab in rows:
        p.text("Match, sort, count & play!", M, y, 4.6, 0.55, f, s, NAVY, valign="middle")
        p.text(lab, M + 4.7, y, 2.8, 0.55, "body", 9, MUTED, valign="middle")
        y += 0.62
    p.text("Arabic extensions: Tajawal Bold (SIL OFL 1.1) is bundled for future Arabic and bilingual editions.", M, y, 7.5, 0.3, "body", 9.5, NAVY)
    y += 0.55
    p.text("SKILL ICONS (always shown with a text label – never colour alone)", M, y, 7.5, 0.35, "title", 13, NAVY)
    y += 0.45
    for i, (k, (lab, ic)) in enumerate(C.SKILLS.items()):
        x = M + i * 1.25
        p.img(ic, x + 0.15, y, 0.9, 0.9)
        p.text(lab, x, y + 0.95, 1.2, 0.3, "xbold", 10, NAVY, align="center")
    y += 1.5
    p.text("COLOUR + SYMBOL PAIRS (colour-blind friendly)", M, y, 7.5, 0.35, "title", 13, NAVY)
    y += 0.45
    for i, c in enumerate(A.ACT):
        x = M + i * 1.25
        p.img(f"token_{c}", x + 0.25, y, 0.7, 0.7)
        p.text(f"{c} = {A.ACT[c][1]}", x, y + 0.75, 1.2, 0.3, "bold", 9, NAVY, align="center")
    y += 1.3
    p.text("ILLUSTRATION & LAYOUT RULES", M, y, 7.5, 0.35, "title", 13, NAVY)
    rules = ["All artwork is original vector art drawn from primitive shapes (03_ILLUSTRATIONS, SVG).",
             "Outline: Dark Navy #18354B, 5 units on a 200-unit art grid, round caps and joins. Flat fills, no gradients or filters.",
             "Corner radius 10–18 art units; page panels 0.14–0.4 in radius. Faces: simple oval eyes with one highlight.",
             "Page grid: 0.5 in margins (home-printer safe area), mission header 1.2 in, footer 0.3 in.",
             "Cut-out cards are always 1.55 in square; board drop zones 1.65 in. Never shrink pieces to fit – redesign the board instead.",
             "Line language: SOLID navy = cut line · DASHED grey = place a card here · small dotted circle = optional fastener spot.",
             "Interior pages stay white and uncluttered; full-colour backgrounds only on the cover and back cover."]
    p.text("\n".join("• " + r for r in rules), M, y + 0.42, 7.5, 3.0, "body", 10, NAVY, leading=1.3)
    _foot(p, "Brand Guide")
    ps.append(p)
    # 3 - Leo character sheet
    p = _page(3)
    p.text("LEO THE LITTLE EXPLORER – CHARACTER SHEET", M, M, 7.5, 0.45, "title", 18, NAVY)
    p.text("Golden lion cub · rounded ears · big simple eyes · sky-blue explorer vest · coral shoes · lime & yellow backpack. Original character – not based on any licensed character.",
           M, M + 0.45, 7.5, 0.45, "body", 9.5, NAVY)
    for i, (a, lab) in enumerate([("leo_front", "FRONT"), ("leo_side", "SIDE"), ("leo_three_quarter", "THREE-QUARTER")]):
        x = M + 0.2 + i * 2.5
        p.img(a, x, 1.5, 2.1, 2.6)
        p.text(lab, x, 4.15, 2.1, 0.3, "title", 12, NAVY, align="center")
    p.text("EXPRESSIONS & POSES", M, 4.65, 7.5, 0.35, "title", 13, NAVY)
    poses = list(A.LEO_POSES.items())
    for i, (a, v) in enumerate(poses):
        x = M + (i % 4) * 1.9
        y = 5.1 + (i // 4) * 2.45
        p.img(a, x + 0.25, y, 1.4, 1.75)
        p.text(f"“{v[5]}”", x, y + 1.78, 1.9, 0.3, "bold", 9, NAVY, align="center")
        p.text(a.replace("leo_", ""), x, y + 2.05, 1.9, 0.22, "body", 8, MUTED, align="center")
    p.text("Use: Leo introduces missions and celebrates. Keep Leo at or below 1.6 in tall on activity boards so he never crowds the activity space.",
           M + 5.75, 7.75, 1.75, 2.0, "body", 9.5, NAVY)
    _foot(p, "Brand Guide")
    ps.append(p)
    return ps


def character_sheet_svg():
    parts = []
    W, H = 1600, 1250

    def inner(name):
        s = art_lib.get_svg(name)
        return s.split("</title>", 1)[1].rsplit("</svg>", 1)[0]

    parts.append(f'<rect width="{W}" height="{H}" fill="#FFF9EA"/>')
    parts.append('<text x="60" y="80" font-family="Fredoka, sans-serif" font-weight="700" font-size="48" fill="#18354B">Leo the Little Explorer – Character Sheet</text>')
    parts.append('<text x="60" y="120" font-family="Nunito, sans-serif" font-size="22" fill="#18354B">Little Worlds Learning original mascot · outline #18354B · fur #F4B940 · mane #E98A2E · vest #64C8ED · shoes #F26855</text>')
    for i, (a, lab) in enumerate([("leo_front", "Front"), ("leo_side", "Side"), ("leo_three_quarter", "Three-quarter")]):
        x = 80 + i * 480
        parts.append(f'<g transform="translate({x} 150) scale(1.6)">{inner(a)}</g>')
        parts.append(f'<text x="{x + 160}" y="580" text-anchor="middle" font-family="Fredoka, sans-serif" font-weight="700" font-size="30" fill="#18354B">{lab}</text>')
    for i, (a, v) in enumerate(A.LEO_POSES.items()):
        x = 40 + i * 222
        parts.append(f'<g transform="translate({x} 640) scale(1.05)">{inner(a)}</g>')
        parts.append(f'<text x="{x + 105}" y="940" text-anchor="middle" font-family="Nunito, sans-serif" font-weight="700" font-size="19" fill="#18354B">{v[5]}</text>')
        parts.append(f'<text x="{x + 105}" y="968" text-anchor="middle" font-family="Nunito, sans-serif" font-size="16" fill="#5B6B78">{a.replace("leo_", "")}</text>')
    parts.append('<text x="60" y="1060" font-family="Nunito, sans-serif" font-size="22" fill="#18354B">Rules: keep proportions (head ≈ half of height), always wear the vest, coral shoes and backpack; simple oval eyes with one highlight;</text>')
    parts.append('<text x="60" y="1095" font-family="Nunito, sans-serif" font-size="22" fill="#18354B">never add fingers or realistic anatomy; never crowd activity space (max 1.6 in tall on boards).</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">' + "".join(parts) + "</svg>"


# ======================================================================= printing guide (customer)
def printing_guide_pages(book):
    ps = []
    p = _page(1)
    p.rect(0, 0, 8.5, 1.6, fill=SKY)
    p.text("START HERE", M, 0.35, 5.5, 0.6, "title", 32, NAVY, valign="middle")
    p.text("Printing & set-up guide for My Magic Busy Book", M, 0.95, 5.8, 0.4, "bold", 14, NAVY, valign="middle")
    p.img("leo_wave", 6.6, 0.15, 1.3, 1.6)
    y = 1.9
    secs = [
        ("WHAT YOU RECEIVED", "Two complete 48-page PDFs – Magic_Busy_Book_US_Letter.pdf (8.5 × 11 in) and Magic_Busy_Book_A4.pdf (210 × 297 mm) – plus this guide. "
         "Both PDFs have the same content. Choose the one that matches your paper. This is a digital product: nothing will be posted to you."),
        ("1. PRINT AT ACTUAL SIZE", "In the print dialog choose “Actual size” or “Scale 100%”. Turn OFF “Fit to page” / “Shrink oversized pages”. "
         "If pages are scaled, the cut-out cards may not fit the boxes on the boards. Print single-sided. Plain 80–100 gsm paper works; card stock (160–220 gsm) is sturdier for the cut-out sheets."),
        ("2. WHICH PAGES ARE WHICH", "Pages 1–4: cover, name page, grown-up setup guide and Mission Map.  Pages 5–40: 36 activity boards (6 worlds × 6 missions).  "
         "Pages 41–45: five cut-out sheets.  Page 46: grown-up reference & answer key.  Page 47: certificate and reward stars.  Page 48: back cover."),
        ("3. ASSEMBLE (ADULT JOB)", "An adult cuts out the 97 cards on pages 41–45 along the solid lines – each card is 1.55 in (39 mm) square. Round off any sharp corners. "
         f"{C.NO_CUT_COUNT} missions need no cutting at all – use a finger, a crayon or a dry-erase pen if laminated. Optional: laminate boards and cards, then add reusable adhesive putty or hook-and-loop dots to the dotted-circle spots."),
        ("4. ORGANISE THE PIECES", "Each card shows a piece ID (e.g. RD1) and the page(s) it is used on. Keep each sheet's cards in its own labelled envelope or zip bag (Sheet 1–5). "
         "Some cards are shared: rainbow drops (RD), shapes (SH), animals (AN) and number cards (NU) are used on more than one page. The footer of every board lists the pieces it needs."),
        ("5. SAFETY & SUPERVISION", "Not suitable for children under 3 years. Contains detachable paper pieces. An adult must prepare all pieces and supervise play at all times. "
         "Check pieces before each use; throw away torn, wet or chewed pieces. Never use pins, staples, magnets, beads or cords as fasteners. Store pieces out of reach after play. This is a printable learning activity, not a certified toy."),
        ("6. STORE & REUSE", "Keep the printed pages flat in a folder or binder with the piece envelopes in a pocket. Laminated pages can be wiped clean. "
         "You may reprint pages and pieces as often as you like for use in your own household."),
    ]
    for head, body in secs:
        p.text(head, M, y, 7.5, 0.32, "title", 13.5, CORAL if head.startswith("5") else NAVY, valign="middle")
        h = p.text(body, M, y + 0.34, 7.5, 1.0, "body", 10.2, NAVY, leading=1.28)
        y += 0.34 + h + 0.2
    _foot(p, "Start Here")
    ps.append(p)
    # page 2: mission index
    p = _page(2)
    p.text("MISSION INDEX & PIECE FINDER", M, M, 7.5, 0.45, "title", 18, NAVY, valign="middle")
    p.text("Board page → cut-out pieces needed (and which sheet they are on)".replace("→", "/"), M, M + 0.45, 7.5, 0.28, "body", 10, NAVY)
    y0 = 1.35
    colw = 3.7
    for i, m in enumerate(C.MISSIONS):
        col, row = divmod(i, 18)
        x = M + col * (colw + 0.1)
        y = y0 + row * 0.47
        ch = C.CHAPTER[m["ch"]]
        p.rect(x, y, colw, 0.42, fill=ch["tint"], r=0.08)
        p.text(f"p{m['page']}", x + 0.06, y, 0.4, 0.42, "xbold", 9, NAVY, valign="middle")
        p.text(f"{m['n']:02d} {m['title'].title()}", x + 0.45, y + 0.02, colw - 0.5, 0.2, "bold", 8.5, NAVY, valign="middle")
        p.text(book.pieces_note(m)[0].replace("Cut-out pieces: ", "Pieces: "), x + 0.45, y + 0.21, colw - 0.5, 0.19, "body", 7.5, NAVY, valign="middle", min_size=6.2)
    _foot(p, "Start Here")
    ps.append(p)
    return ps


# ======================================================================= free sample
def free_sample_pages():
    b = Book("US_Letter")
    pages = b.build()
    board = pages[4]
    board.number = 1
    sp = Page(2, b.W, b.H, "pieces", "US_Letter")
    sp.text("FREE SAMPLE – CUT-OUT PIECES FOR RAINBOW RESCUE", M, M, b.W - 2 * M, 0.45, "title", 16, NAVY, valign="middle")
    sp.text("Grown-ups: print at Actual size, then cut along the solid lines. Adult supervision required – not suitable for children under 3.",
            M, M + 0.45, b.W - 2 * M, 0.3, "bold", 9.5, CORAL)
    gx = (b.W - (3 * PIECE + 2 * 0.4)) / 2
    for k in range(6):
        r, c = divmod(k, 3)
        b.piece_card(sp, gx + c * (PIECE + 0.4), 1.5 + r * (PIECE + 0.4), f"RD{k + 1}", record=True)
    sp.rect(M, 5.6, b.W - 2 * M, 3.6, fill=CREAM, stroke=YELLOW, sw=2, r=0.3)
    sp.img("leo_cheer", M + 0.3, 5.85, 2.1, 2.6)
    sp.text("Enjoyed this mission?", M + 2.7, 5.9, 4.5, 0.5, "title", 20, NAVY, valign="middle")
    sp.text("This is Mission 01 from My Magic Busy Book by Little Worlds Learning: 48 printable pages with 36 little missions "
            "to match, sort, count and play, five cut-out sheets, a grown-up guide, answer key and certificate. Ages 3–5 with adult help.",
            M + 2.7, 6.45, 4.5, 2.0, "body", 11, NAVY, leading=1.3)
    sp.text("Free sample for personal / household use. © 2026 Little Worlds Learning.", M, b.H - 0.8, b.W - 2 * M, 0.26, "bold", 8, MUTED, align="center")
    return [board, sp]


# ======================================================================= CSV / data files
def write_content_files(out_dir, book_us, pages_us, book_a4, pages_a4):
    os.makedirs(out_dir, exist_ok=True)
    by = {p.number: p for p in pages_us}
    # Complete page plan
    with open(os.path.join(out_dir, "Complete_Page_Plan.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["page_number", "section", "page_type", "title", "mission_number", "child_instruction", "skill", "cut_out_pieces"])
        for p in pages_us:
            if p.kind == "mission":
                m = p.mission
                w.writerow([p.number, C.CHAPTER[m["ch"]]["name"], "activity board" + (" (no-cut)" if not m["pieces"] else ""), m["title"],
                            f"{m['n']:02d}", m["instr"], C.SKILLS[m["skill"]][0], " ".join(m["pieces"]) or "none"])
            else:
                sec = {"cover": "Introduction", "intro": "Introduction", "pieces": "Piece sheets", "reference": "Adult reference", "certificate": "Reward", "back": "Back cover"}[p.kind]
                extra = " ".join(pc["id"] for pc in p.pieces)
                w.writerow([p.number, sec, p.kind, p.title, "", "", "", extra])
    # Activity manifest
    with open(os.path.join(out_dir, "Activity_Manifest.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["page_number", "mission_number", "mission_name", "chapter", "learning_goal", "difficulty", "requires_cutouts", "piece_sheet",
                    "piece_ids", "correct_placements", "adult_guidance", "works_with_finger_or_pencil", "works_with_paper_cutouts",
                    "works_with_reusable_fasteners", "validation_status"])
        for m in C.MISSIONS:
            p = by[m["page"]]
            sheets = sorted({book_us.sheet_of[x] for x in m["pieces"]})
            if m["pieces"]:
                pl = " | ".join(f"{'/'.join(s['accepts'])} -> {s['target']}" for s in p.slots)
            else:
                pl = " | ".join(f"{a} -> {b}" for a, b in p.answers)
            w.writerow([m["page"], f"{m['n']:02d}", m["title"], C.CHAPTER[m["ch"]]["name"], m["goal"], m["diff"], "yes" if m["pieces"] else "no",
                        " ".join(f"p{s}" for s in sheets) or "none (no-cut)", " ".join(m["pieces"]) or "none", pl, m["guide"],
                        m["modes"][0], m["modes"][1], m["modes"][2], "VALIDATED (automated) / visual check required"])
    # Piece inventory
    with open(os.path.join(out_dir, "Piece_Inventory.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["piece_id", "set_code", "set_name", "description", "artwork_svg", "sheet_page_us_letter", "sheet_page_a4", "position_us_in_xy",
                    "size_in", "used_on_pages", "used_by_missions", "board_targets"])
        tg = {}
        for p in pages_us:
            for s in p.slots:
                for pid in s["accepts"]:
                    tg.setdefault(pid, []).append(f"p{p.number}: {s['target']}")
        pos = {pc["id"]: (p.number, pc) for p in pages_us for pc in p.pieces}
        for s in C.PIECE_SETS:
            for pid, asset, label in s["items"]:
                pg, pc = pos[pid]
                ms = [m for m in C.MISSIONS if pid in m["pieces"]]
                w.writerow([pid, s["code"], s["name"], label, (asset + ".svg") if asset else "native text + dots", pg, book_a4.sheet_of[pid],
                            f"{pc['x']:.2f},{pc['y']:.2f}", f"{PIECE} x {PIECE}", " ".join(str(m["page"]) for m in ms),
                            " ".join(f"M{m['n']:02d}" for m in ms), " ; ".join(tg.get(pid, []))])
        w.writerow(["ST1-ST6", "ST", "Reward stars (optional)", "colour-in or cut-out chapter stars", "reward_star_blank.svg", 47, 47, "", "1.65 star",
                    "4", "chapter rewards", "p4 Mission Map milestone stars (optional)"])
    # Answer key
    L = ["# My Magic Busy Book – Answer Key", "", "Answers are suggestions. Praise effort, and accept any choice a child can sensibly explain. "
         "Page numbers are identical in the US Letter and A4 editions.", ""]
    for m in C.MISSIONS:
        p = by[m["page"]]
        L.append(f"## Mission {m['n']:02d} – {m['title'].title()} (page {m['page']})")
        L.append(f"*{C.CHAPTER[m['ch']]['name']} · {C.SKILLS[m['skill']][0].title()} · {m['diff']}*  ")
        L.append(f"Goal: {m['goal']}  ")
        if m["pieces"]:
            L.append(f"Pieces: {book_us.pieces_note(m)[0].replace('Cut-out pieces: ', '')}")
            L.append("")
            L.append("| Board spot | Correct piece(s) |")
            L.append("|---|---|")
            for s in p.slots:
                L.append(f"| {s['target']} | {', '.join(f'{x} ({C.PIECE_INDEX[x][2]})' for x in s['accepts'])} |")
        else:
            L.append("No-cut activity.")
            L.append("")
            L.append("| Item | Answer |")
            L.append("|---|---|")
            for a, b in p.answers:
                L.append(f"| {a} | {b} |")
        L.append("")
        L.append(f"Grown-up tip: {m['guide']}")
        L.append("")
    open(os.path.join(out_dir, "Answer_Key.md"), "w").write("\n".join(L))
    # Text content (translation source)
    txt = {"product": C.PRODUCT, "chapters": [{k: c[k] for k in ("num", "name")} for c in C.CHAPTERS],
           "missions": [{k: m[k] for k in ("n", "page", "title", "instr", "goal", "diff", "guide")} | {"leo_line": m["leo"][1] if m["leo"] else None}
                        for m in C.MISSIONS],
           "pages": {p.number: [e["s"] for e in p.els if e["t"] == "text"] for p in pages_us}}
    json.dump(txt, open(os.path.join(out_dir, "Text_Content_EN.json"), "w"), indent=1, ensure_ascii=False)
