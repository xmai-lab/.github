"""Build the XMAI R4 ("lifted cell") logo set as font-independent SVGs.

Usage: python -I make_logo.py <fonts_dir> <out_dir>
"""

import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

FONTS, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

grotesk = instantiateVariableFont(TTFont(FONTS / "SpaceGrotesk.ttf"), {"wght": 700})
inter = instantiateVariableFont(TTFont(FONTS / "Inter.ttf"), {"wght": 500, "opsz": 14})


def text_path(font, text, x, y, size, anchor="start", tracking=0.0):
    """SVG path data for `text` with baseline at y; anchor 'middle' centres on advance width."""
    cmap, gs = font.getBestCmap(), font.getGlyphSet()
    hmtx, upm = font["hmtx"], font["head"].unitsPerEm
    k = size / upm
    names = [cmap[ord(c)] for c in text]
    width = sum(hmtx[n][0] for n in names) * k + tracking * (len(names) - 1)
    cx = x - width / 2 if anchor == "middle" else x
    pen = SVGPathPen(gs)
    for n in names:
        gs[n].draw(TransformPen(pen, (k, 0, 0, -k, cx, y)))
        cx += hmtx[n][0] * k + tracking
    return pen.getCommands()


def rr(x, y, w, h, radii):
    tl, tr, br, bl = radii
    a = lambda r, ex, ey: f"A{r} {r} 0 0 1 {ex} {ey}" if r else ""
    return (f"M{x + tl} {y} H{x + w - tr} {a(tr, x + w, y + tr)} V{y + h - br} "
            f"{a(br, x + w - br, y + h)} H{x + bl} {a(bl, x, y + h - bl)} V{y + tl} {a(tl, x + tl, y)} Z")


# R4 geometry (same numbers as the approved proposal)
PAD, GAP, OUTER, INNER, LIFT, STROKE, SIZE = 8, 4, 9, 2.5, 5, 3.4, 27
S = (100 - 2 * PAD - GAP) / 2
POS = [(PAD, PAD), (PAD + S + GAP, PAD), (PAD, PAD + S + GAP), (PAD + S + GAP, PAD + S + GAP)]
RADII = [(OUTER, INNER, INNER, INNER), (INNER, OUTER, INNER, INNER),
         (INNER, INNER, INNER, OUTER), (INNER, INNER, OUTER, INNER)]
BASE = S / 2 + SIZE * 0.36

PALETTES = {
    "light": dict(ink="#13283D", paper="#FFFFFF", accent="#0B8F8A", slot="#13283D"),
    "dark": dict(ink="#E8EEF4", paper="#121A22", accent="#3CC4BD", slot="#E8EEF4"),
    "mono-black": dict(ink="#000000", paper="#FFFFFF", accent="#000000", slot="#000000"),
    "mono-white": dict(ink="#FFFFFF", paper="#000000", accent="#FFFFFF", slot="#FFFFFF"),
}


def mark_body(p, knockout=True):
    """Mark elements in the 0..100 box. Letters in closed cells are cut out when knockout=True."""
    out = []
    x, y = POS[0]
    inset = [max(0, r - STROKE / 2) for r in RADII[0]]
    out.append(f'<path d="{rr(x, y, S, S, RADII[0])}" fill="none" stroke="{p["slot"]}" '
               f'stroke-opacity=".28" stroke-width="1.4" stroke-dasharray="2.2 2.2"/>')
    out.append(f'<path d="{rr(x - LIFT + STROKE / 2, y - LIFT + STROKE / 2, S - STROKE, S - STROKE, inset)}" '
               f'fill="none" stroke="{p["accent"]}" stroke-width="{STROKE}"/>')
    out.append(f'<path d="{text_path(grotesk, "X", x + S / 2 - LIFT, y - LIFT + BASE, SIZE, "middle")}" '
               f'fill="{p["accent"]}"/>')
    for (cx, cy), radii, ch in zip(POS[1:], RADII[1:], "MAI"):
        cell, letter = rr(cx, cy, S, S, radii), text_path(grotesk, ch, cx + S / 2, cy + BASE, SIZE, "middle")
        if knockout:   # letter is a hole: the background shows through, works on any ground
            out.append(f'<path d="{cell} {letter}" fill="{p["ink"]}" fill-rule="evenodd"/>')
        else:
            out.append(f'<path d="{cell}" fill="{p["ink"]}"/><path d="{letter}" fill="{p["paper"]}"/>')
    return "\n  ".join(out)


def svg(view, body, bg=None, label="XMAI"):
    rect = f'<rect x="{view[0]}" y="{view[1]}" width="{view[2]}" height="{view[3]}" fill="{bg}"/>\n  ' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(map(str, view))}" role="img" '
            f'aria-label="{label}">\n  <title>{label}</title>\n  {rect}{body}\n</svg>\n')


def wordmark_body(p, sub_color):
    mark = f'<g transform="scale(0.8)">\n  {mark_body(p)}\n  </g>'
    name = f'<path d="{text_path(grotesk, "XMAI", 96, 41, 34, tracking=1.5)}" fill="{p["ink"]}"/>'
    sub = f'<path d="{text_path(inter, "eXplainable Medical AI", 97, 66, 16.5)}" fill="{sub_color}"/>'
    return '<g transform="translate(2 2)">\n  ' + "\n  ".join([mark, name, sub]) + "\n  </g>"


files = {}
for key, p in PALETTES.items():
    files[f"xmai-mark-{key}.svg"] = svg((2, 2, 91, 91), mark_body(p), label="XMAI logo")
# avatar: square with a solid ground (GitHub crops it to a rounded square)
CENTRE = '<g transform="translate(50 50) scale(0.8) translate(-47.5 -47.5)">\n  {}\n  </g>'
files["xmai-avatar.svg"] = svg((0, 0, 100, 100), CENTRE.format(mark_body(PALETTES["light"])), bg="#FFFFFF", label="XMAI logo")
files["xmai-avatar-dark.svg"] = svg((0, 0, 100, 100), CENTRE.format(mark_body(PALETTES["dark"])), bg="#121A22", label="XMAI logo")
subs = {"light": "#5B6876", "dark": "#98A6B4", "mono-black": "#000000", "mono-white": "#FFFFFF"}
for key, p in PALETTES.items():
    files[f"xmai-wordmark-{key}.svg"] = svg((0, 0, 290, 78), wordmark_body(p, subs[key]),
                                           label="XMAI eXplainable Medical AI")

for name, content in files.items():
    (OUT / name).write_text(content)
    print(name, len(content))
