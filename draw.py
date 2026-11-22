#!/usr/bin/env python3
"""Draw the front page of 21 November 2026 world news as one 1024x1024 PNG.

Original artwork drawn in code with Pillow. No photos, no downloads, no
network. Deterministic: same input always produces the same PNG bytes.
Run: python3 draw.py  ->  writes entry.png next to this script.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 231)
INK = (26, 26, 26)
RED = (176, 42, 30)
BLUE = (31, 78, 121)
GREY = (90, 86, 78)
LIGHT = (233, 226, 210)
SKY = (186, 214, 232)
SAND = (214, 178, 120)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def panel(draw, x, y, w, h, kicker, headline, body, head_size=30,
          body_size=19, art=None, head_lines=2):
    """A bordered news panel. art(d, x, y, w, h) draws the illustration."""
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    pad = 14
    cx = x + pad
    cy = y + 10
    draw.text((cx, cy), kicker, font=F_SANS_B(15), fill=RED)
    cy += 24
    hl = wrap(draw, headline, F_SERIF_B(head_size), w - 2 * pad)
    cy = text_block(draw, cx, cy, hl[:head_lines], F_SERIF_B(head_size),
                    leading=head_size + 6)
    cy += 4
    if art is not None:
        art_h = 76 if h > 200 else 64
        art(draw, x + pad, cy, w - 2 * pad, art_h)
        cy += art_h + 8
    bl = wrap(draw, body, F_SANS(body_size), w - 2 * pad)
    # Cap the body so it never spills past the panel's bottom edge.
    max_lines = max(1, (y + h - pad - cy) // (body_size + 6))
    if len(bl) > max_lines:
        bl = bl[:max_lines]
        bl[-1] = bl[-1].rstrip(".,") + "…"
    text_block(draw, cx, cy, bl, F_SANS(body_size),
               leading=body_size + 6)
    return y + h


# ---- illustrations (simple original pictograms, drawn in code) ----

def art_mexico(d, x, y, w, h):
    # Desert dusk: sky, sun, mountains, road, helicopter, handcuffs.
    d.rectangle([x, y, x + w, y + h], fill=(246, 214, 150))
    d.ellipse([x + w - 78, y + 8, x + w - 18, y + 68], fill=(232, 120, 40))
    d.polygon([(x, y + h), (x + w * 0.30, y + h * 0.42),
               (x + w * 0.55, y + h), ], fill=(150, 96, 52))
    d.polygon([(x + w * 0.42, y + h), (x + w * 0.72, y + h * 0.30),
               (x + w, y + h)], fill=(120, 74, 40))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(96, 62, 34))
    # helicopter silhouette
    hx, hy = x + 24, y + 14
    d.ellipse([hx, hy, hx + 46, hy + 16], fill=INK)
    d.line([(hx - 26, hy + 6), (hx + 72, hy + 6)], fill=INK, width=4)
    d.line([(hx + 46, hy + 8), (hx + 66, hy + 26)], fill=INK, width=4)
    d.line([(hx + 23, hy + 16), (hx + 23, hy + 30)], fill=INK, width=4)
    d.line([(hx + 14, hy + 30), (hx + 32, hy + 30)], fill=INK, width=4)
    # handcuffs
    cx0, cy0 = x + w - 108, y + h - 46
    d.ellipse([cx0, cy0, cx0 + 30, cy0 + 30], outline=INK, width=5)
    d.ellipse([cx0 + 46, cy0, cx0 + 76, cy0 + 30], outline=INK, width=5)
    d.line([(cx0 + 30, cy0 + 15), (cx0 + 46, cy0 + 15)], fill=INK, width=5)


def art_kryvyi(d, x, y, w, h):
    # City skyline at night with an orange blast starburst.
    d.rectangle([x, y, x + w, y + h], fill=(38, 44, 66))
    for i, (bx, bw, bh) in enumerate([(0, 34, 52), (40, 26, 70), (72, 40, 44),
                                      (118, 30, 62), (154, 36, 48)]):
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(16, 18, 28))
        for wy in range(y + h - bh + 8, y + h - 6, 14):
            d.rectangle([x + bx + 6, wy, x + bx + 12, wy + 7], fill=(240, 200, 90))
    cx, cy = x + w - 58, y + 40
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 14, 42
        a = math.radians(ang)
        d.line([(cx, cy), (cx + r2 * math.cos(a), cy + r2 * math.sin(a))],
               fill=(255, 150, 40), width=6)
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 190, 60))
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 240, 180))


def art_cop(d, x, y, w, h):
    # Globe with a thermometer climbing past the top.
    cx, cy, r = x + 62, y + h // 2 + 4, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(140, 190, 220),
              outline=BLUE, width=3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=3)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=BLUE, width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=2)
    d.ellipse([cx - 26, cy - 18, cx - 2, cy + 6], fill=(90, 170, 90))
    d.ellipse([cx + 4, cy + 8, cx + 30, cy + 30], fill=(90, 170, 90))
    # thermometer
    tx = x + w - 52
    d.rectangle([tx, y + 6, tx + 16, y + h - 18], outline=RED, width=3)
    d.rectangle([tx + 3, y + h - 34, tx + 13, y + h - 21], fill=RED)
    d.ellipse([tx - 6, y + h - 26, tx + 22, y + h + 2], fill=RED)
    d.line([(tx + 8, y + h - 22), (tx + 8, y + 12)], fill=RED, width=7)
    d.text((x + 118, y + 8), "COP31", font=F_SANS_B(22), fill=BLUE)
    d.text((x + 118, y + 36), "ANTALYA", font=F_SANS_B(22), fill=BLUE)
    d.text((x + 118, y + 66), "OVERTIME", font=F_SANS_B(20), fill=RED)


def art_markets(d, x, y, w, h):
    # Falling red chart line with arrow.
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.line([(x + 6, y + h - 22), (x + w - 6, y + h - 22)], fill=GREY, width=2)
    pts = [(x + 10, y + 14), (x + w * 0.30, y + 26), (x + w * 0.48, y + 22),
           (x + w * 0.66, y + 52), (x + w * 0.84, y + 66),
           (x + w - 12, y + h - 26)]
    d.line(pts, fill=RED, width=5, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 16, ey - 2), (ex - 4, ey - 16)], fill=RED)
    d.text((x + 10, y + h - 20), "-3.7%", font=F_SANS_B(20), fill=RED)


def art_poland(d, x, y, w, h):
    # Shield with a map pin and a missile streak across the sky.
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    d.line([(x + 8, y + 18), (x + w - 40, y + 34)], fill=INK, width=3)
    d.polygon([(x + w - 40, y + 34), (x + w - 58, y + 28),
               (x + w - 58, y + 40)], fill=INK)
    d.polygon([(x + 30, y + 22), (x + 78, y + 22), (x + 54, y + h - 8)],
              fill=(31, 78, 121))
    d.ellipse([x + 40, y + 26, x + 68, y + 54], fill=(255, 255, 255))
    d.ellipse([x + 48, y + 34, x + 60, y + 46], fill=RED)
    d.text((x + 92, y + 30), "WARSAW", font=F_SANS_B(22), fill=INK)
    d.text((x + 92, y + 58), "NATO", font=F_SANS_B(22), fill=RED)


def art_mercury(d, x, y, w, h):
    # Cratered Mercury with a small probe flying past.
    d.rectangle([x, y, x + w, y + h], fill=(16, 18, 30))
    for sx, sy in [(14, 12), (60, 30), (120, 8), (180, 26), (230, 14),
                   (40, 66), (200, 70)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    cx, cy, r = x + 70, y + h // 2, 36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 160, 148))
    for ox, oy, orr in [(-12, -8, 7), (10, 6, 9), (-2, 16, 5), (16, -16, 4)]:
        d.ellipse([cx + ox - orr, cy + oy - orr, cx + ox + orr, cy + oy + orr],
                  fill=(130, 122, 110))
    # probe: body + panels + dish
    px, py = x + w - 84, y + 18
    d.rectangle([px, py, px + 26, py + 12], fill=(220, 220, 220))
    d.rectangle([px - 16, py + 2, px, py + 10], fill=(90, 140, 200))
    d.rectangle([px + 26, py + 2, px + 42, py + 10], fill=(90, 140, 200))
    d.arc([px + 8, py + 10, px + 30, py + 30], 0, 180, fill=(220, 220, 220),
          width=3)
    d.text((x + 118, y + h - 26), "8 YEARS IN FLIGHT", font=F_SANS_B(13),
           fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28
    X0, X1 = M, W - M

    # --- masthead ---
    rule(d, X0, X1, 14, width=3)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=F_SERIF_B(62))
    d.text(((W - tw) / 2, 22), title, font=F_SERIF_B(62), fill=INK)
    rule(d, X0, X1, 104, width=2)
    date = "SATURDAY, 21 NOVEMBER 2026"
    dw = d.textlength(date, font=F_SANS_B(38))
    d.text(((W - dw) / 2, 112), date, font=F_SANS_B(38), fill=RED)
    tag = "One day's world news — in one picture"
    tgw = d.textlength(tag, font=F_SERIF(20))
    d.text(((W - tgw) / 2, 158), tag, font=F_SERIF(20), fill=GREY)
    rule(d, X0, X1, 188, width=3)
    rule(d, X0, X1, 192, width=1)

    # --- lead story: Mexico captures El Chapo Isidro ---
    ly, lh = 202, 200
    d.rectangle([X0, ly, X1, ly + lh], outline=INK, width=2)
    d.text((X0 + 14, ly + 10), "LEAD  •  MEXICO", font=F_SANS_B(16), fill=RED)
    head = "Mexico captures 'El Chapo Isidro'"
    hl = wrap(d, head, F_SERIF_B(40), 560)
    text_block(d, X0 + 14, ly + 36, hl, F_SERIF_B(40), leading=46)
    body = ("Mexican forces seized Fausto Isidro Meza Flores — one of the "
            "FBI's 10 most wanted — in Guasave, Sinaloa, with US help.")
    bl = wrap(d, body, F_SANS(18), 560)
    text_block(d, X0 + 14, ly + 36 + len(hl) * 46 + 8, bl, F_SANS(18),
               leading=24)
    art_mexico(d, X0 + 600, ly + 12, X1 - X0 - 614, lh - 24)

    # --- row 2: two stories ---
    ry, rh = 414, 254
    w2 = (X1 - X0 - 12) // 2
    panel(d, X0, ry, w2, rh, "WAR  •  UKRAINE",
          "Missile hits Zelenskyy's hometown",
          "Russian missiles hit Kryvyi Rih, killing 2 — a boy of 7 and a "
          "woman of 20 — and wounding 60.",
          head_size=27, body_size=16, art=art_kryvyi)
    panel(d, X0 + w2 + 12, ry, w2, rh, "CLIMATE  •  TURKEY",
          "COP31 talks run into overtime",
          "The Antalya summit passed its deadline with no deal — and "
          "fossil fuels are still missing from the draft.",
          head_size=27, body_size=16, art=art_cop)

    # --- row 3: three stories (text only, no art: keeps them legible) ---
    ry3, rh3 = 680, 192
    w3 = (X1 - X0 - 24) // 3
    panel(d, X0, ry3, w3, rh3, "MARKETS",
          "AI sell-off sinks stocks",
          "The S&P 500 fell 3.7% and Japan's Nikkei 5.06% as the AI "
          "rally unravelled.",
          head_size=23, body_size=17, art=None)
    panel(d, X0 + w3 + 12, ry3, w3, rh3, "EUROPE  •  NATO",
          "Missile lands in Poland",
          "NATO chief Rutte flew to Warsaw after a Russian missile "
          "crashed on Polish soil.",
          head_size=23, body_size=17, art=None)
    panel(d, X0 + 2 * (w3 + 12), ry3, w3, rh3, "SPACE",
          "Probe reaches Mercury",
          "Europe and Japan's BepiColombo entered orbit around Mercury "
          "after an eight-year journey.",
          head_size=23, body_size=17, art=None)

    # --- footer: also today ---
    fy = 884
    rule(d, X0, X1, fy, width=3)
    d.text((X0, fy + 8), "ALSO TODAY", font=F_SANS_B(16), fill=RED)
    items = [
        ("NIGERIA", "At least 24 dead as a boat carrying mourners to a "
         "funeral capsizes."),
        ("HEALTH", "Mosquitoes carrying a bacterium cut dengue cases by "
         "69% in Brazil."),
        ("SPORT", "Las Vegas Grand Prix under the lights tonight; UFC in "
         "Doha, Qatar."),
    ]
    col_w = (X1 - X0) // 3
    for i, (kick, txt) in enumerate(items):
        cx = X0 + i * col_w
        d.text((cx, fy + 34), kick, font=F_SANS_B(15), fill=BLUE)
        bl = wrap(d, txt, F_SANS(16), col_w - 16)
        text_block(d, cx, fy + 56, bl[:3], F_SANS(16), leading=21)
    rule(d, X0, X1, H - 16, width=2)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
