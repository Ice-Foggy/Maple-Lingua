"""Build Maple Lingua logo variants 2-5 as SVG with text converted to outlines."""
import math, os, sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONTDIR = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

LEAF = "50,5 57,20 64,16 61,36 74,24 77,31 90,28 85,42 92,46 73,62 76,70 54,67 55,90 45,90 46,67 24,70 27,62 8,46 15,42 10,28 23,31 26,24 39,36 36,16 43,20"
INK, RED, BLUE, GREY, NAVY = "#1B2A41", "#C8332B", "#1F4E9C", "#5A6472", "#1B2A41"

class Font:
    def __init__(self, path):
        self.tt = TTFont(path)
        self.gs = self.tt.getGlyphSet()
        self.upem = self.tt["head"].unitsPerEm
        blob = hb.Blob.from_file_path(path)
        self.hbfont = hb.Font(hb.Face(blob))
        self.order = self.tt.getGlyphOrder()
        os2 = self.tt["OS/2"]
        self.cap = os2.sCapHeight / self.upem
        self.xh = os2.sxHeight / self.upem

    def shape(self, text, size, spacing=0.0):
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {"kern": True, "liga": False})
        k = size / self.upem
        glyphs, x = [], 0.0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            name = self.order[info.codepoint]
            adv = pos.x_advance * k
            glyphs.append((name, x + pos.x_offset * k, adv))
            x += adv + spacing
        width = x - spacing if glyphs else 0
        return glyphs, width, k

    def glyph_d(self, name, transform):
        pen = SVGPathPen(self.gs)
        self.gs[name].draw(TransformPen(pen, transform))
        return pen.getCommands()

    def glyph_bounds(self, name):
        bp = BoundsPen(self.gs); self.gs[name].draw(bp); return bp.bounds

    def text_d(self, text, size, x0, baseline, spacing=0.0, anchor="start"):
        glyphs, width, k = self.shape(text, size, spacing)
        if anchor == "middle": x0 -= width / 2
        parts = [self.glyph_d(n, (k, 0, 0, -k, x0 + gx, baseline)) for n, gx, _ in glyphs]
        return " ".join(p for p in parts if p), width

    def ink_box(self, text, size, spacing=0.0):
        """Ink y-range (in SVG coords, relative to baseline) of a shaped line."""
        glyphs, width, k = self.shape(text, size, spacing)
        top, bot = 0, 0
        for n, _, _ in glyphs:
            b = self.glyph_bounds(n)
            if b: top = max(top, b[3] * k); bot = min(bot, b[1] * k)
        return -top, -bot, width

M500 = Font(f"{FONTDIR}/m500.ttf"); M700 = Font(f"{FONTDIR}/m700.ttf"); M800 = Font(f"{FONTDIR}/m800.ttf")

def leaf(tx, ty, s, fill, extra=""):
    return f'<polygon transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})" fill="{fill}" {extra} points="{LEAF}"/>'

def write(name, w, h, body, title):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.2f} {h:.2f}">'
           f'<title>{title}</title>{body}</svg>\n')
    with open(f"{OUT}/{name}.svg", "w") as f: f.write(svg)

PAD = 32

# ---------- 2 · Split leaf ----------
def split():
    size, sp = 54, 4
    t1 = M800.text_d  # alias
    _, w1, _ = M800.shape("MAPLE", size, sp); _, w2, _ = M800.shape("LINGUA", size, sp)
    wt = max(w1, w2)
    leafsize = 150
    cap = M800.cap * size
    # two caps lines, 56px apart, block centred on the leaf's middle
    lx, ly = PAD, PAD
    cy = ly + leafsize * 0.475
    b1 = cy - 28 + cap / 2 - 0  # line1 baseline
    b1 = cy - (56 + cap) / 2 + cap
    b2 = b1 + 56
    tx = lx + leafsize + 24
    d1, _ = M800.text_d("MAPLE", size, tx, b1, sp); d2, _ = M800.text_d("LINGUA", size, tx, b2, sp)
    lock_w = leafsize + 24 + wt
    # subtitle
    ss, ssp = 15, 3
    parts = [("FRANÇAIS", BLUE), ("|", "#8A93A0"), ("ENGLISH", "#B02A23")]
    widths = [M700.shape(t, ss, ssp)[1] for t, _ in parts]
    sub_w = sum(widths) + 16 * 2
    sub_base = ly + leafsize + 40 + M700.cap * ss
    W = max(lock_w, sub_w) + 2 * PAD
    off = (W - 2 * PAD - lock_w) / 2
    x = (W - sub_w) / 2
    sub = ""
    for (t, c), wdt in zip(parts, widths):
        d, _ = M700.text_d(t, ss, x, sub_base, ssp); sub += f'<path fill="{c}" d="{d}"/>'; x += wdt + 16
    s = leafsize / 100
    lxo = lx + off
    body = (f'<defs><clipPath id="l"><rect x="0" y="0" width="48.6" height="100"/></clipPath>'
            f'<clipPath id="r"><rect x="51.4" y="0" width="48.6" height="100"/></clipPath></defs>'
            f'<g transform="translate({lxo:.2f} {ly:.2f}) scale({s})">'
            f'<polygon clip-path="url(#l)" fill="{BLUE}" points="{LEAF}"/>'
            f'<polygon clip-path="url(#r)" fill="{RED}" points="{LEAF}"/></g>'
            f'<g transform="translate({off:.2f} 0)"><path fill="{INK}" d="{d1}"/><path fill="{INK}" d="{d2}"/></g>{sub}')
    H = sub_base + PAD
    write("maple-lingua-2-dvuyazychnyj-list", W, H, body, "Maple Lingua")

# ---------- 3 · Leaf over the i ----------
def dot():
    size, sp = 76, -2
    text = "maple lıngua"
    glyphs, width, k = M800.shape(text, size, sp)
    asc = 0.8 * size + 20  # room for leaf
    base = PAD + asc
    d, _ = M800.text_d(text, size, PAD, base, sp)
    # locate dotless i (8th glyph: m a p l e ␠ l ı)
    idx = [i for i, ch in enumerate(text)].index(text.index("ı"))
    name, gx, adv = glyphs[idx]
    b = M800.glyph_bounds(name)
    cx = PAD + gx + (b[0] + b[2]) / 2 * k
    ls = 0.40 * size  # leaf box size
    leaf_bottom = base - M800.xh * size - 0.07 * size
    ty = leaf_bottom - 0.90 * ls
    tx = cx - 0.5 * ls
    tag = "Французский и английский для жизни в Канаде"
    ts = 15
    _, tw, _ = M500.shape(tag, ts)
    tb = base + 20 + 0.2 * size + M500.xh * ts + 4
    W = max(width, tw) + 2 * PAD
    td, _ = M500.text_d(tag, ts, W / 2, tb, 0, "middle")
    body = (f'<path fill="{INK}" d="{d}"/>' + leaf(tx, ty, ls / 100, RED) +
            f'<path fill="{GREY}" d="{td}"/>')
    write("maple-lingua-3-list-nad-i", W, tb + PAD, body, "Maple Lingua")
    # version without tagline
    write("maple-lingua-3-list-nad-i-bez-podpisi", W, base + 0.25 * size + PAD,
          f'<path fill="{INK}" d="{d}"/>' + leaf(tx, ty, ls / 100, RED), "Maple Lingua")

# ---------- 4 · Seal ----------
def seal():
    C = 170
    size, sp = 22, 5
    cap = M800.cap * size
    R_top, R_bot = 118, 118 + cap  # caps of both arcs occupy the same ring band
    parts = []

    def arc(text, R, top):
        glyphs, _, k = M800.shape(text, size, 0)
        advs = [a for _, _, a in glyphs]
        total = sum(advs) + sp * (len(advs) - 1)
        s = -total / 2
        for (name, _, adv) in glyphs:
            mid = s + adv / 2
            if top:   # clockwise over the top, glyphs point outward
                phi = 1.5 * math.pi + mid / R; rot = phi + math.pi / 2
            else:     # left-to-right along the bottom, glyphs point inward
                phi = 0.5 * math.pi - mid / R; rot = phi - math.pi / 2
            px, py = C + R * math.cos(phi), C + R * math.sin(phi)
            c, sn = math.cos(rot), math.sin(rot)
            e, f = px - c * adv / 2, py - sn * adv / 2
            g = M800.glyph_d(name, (k * c, k * sn, k * sn, -k * c, e, f))
            if g: parts.append(g)
            s += adv + sp

    arc("MAPLE LINGUA", R_top, True)
    arc("FRANÇAIS • ENGLISH", R_bot, False)
    rm = (R_top + R_top + cap) / 2
    dots = "".join(f'<circle cx="{C + sx * rm:.2f}" cy="{C}" r="3.5" fill="#E5483E"/>' for sx in (-1, 1))
    body = (f'<circle cx="{C}" cy="{C}" r="170" fill="{NAVY}"/>'
            f'<circle cx="{C}" cy="{C}" r="160" fill="none" stroke="#FFFFFF" stroke-width="3"/>'
            f'<circle cx="{C}" cy="{C}" r="98" fill="none" stroke="#FFFFFF" stroke-width="1.5"/>'
            f'<path fill="#FFFFFF" d="{" ".join(parts)}"/>' + dots + leaf(105, 109, 1.3, "#E5483E"))
    write("maple-lingua-4-pechat", 340, 340, body, "Maple Lingua")

# ---------- 5 · Fr + En ----------
def bubbles():
    blue = "M38 10 H132 A28 28 0 0 1 160 38 V92 A28 28 0 0 1 132 120 H62 L30 150 L40 120 H38 A28 28 0 0 1 10 92 V38 A28 28 0 0 1 38 10 Z"
    red = "M148 80 H242 A28 28 0 0 1 270 108 V162 A28 28 0 0 1 242 190 H240 L250 220 L208 190 H148 A28 28 0 0 1 120 162 V108 A28 28 0 0 1 148 80 Z"
    def centred(t, cx, cy):
        top, bot, _ = M800.ink_box(t, 44)
        base = cy - (top + bot) / 2
        d, _ = M800.text_d(t, 44, cx, base, 0, "middle"); return d
    fr, en = centred("Fr", 85, 65), centred("En", 195, 135)
    # wordmark row
    ws, wsp = 44, -1
    _, ww, _ = M800.shape("Maple Lingua", ws, wsp)
    row_w = 30 + 10 + ww
    W = max(280, row_w) + 2 * PAD
    ox = (W - 280) / 2
    cap = M800.cap * ws
    row_top = PAD + 224 + 32
    base = row_top + 2 + cap  # leaf 30px tall, caps ~32px
    rx = (W - row_w) / 2
    wd, _ = M800.text_d("Maple Lingua", ws, rx + 40, base, wsp)
    leaf_ty = base - cap / 2 - 15 * 0.95
    body = (f'<defs><mask id="cut" maskUnits="userSpaceOnUse" x="0" y="0" width="280" height="224">'
            f'<rect x="0" y="0" width="280" height="224" fill="#fff"/>'
            f'<path d="{red}" fill="#000" stroke="#000" stroke-width="12" stroke-linejoin="round"/></mask></defs>'
            f'<g transform="translate({ox:.2f} {PAD})">'
            f'<path d="{blue}" fill="{BLUE}" mask="url(#cut)"/>'
            f'<path d="{fr}" fill="#FFFFFF" mask="url(#cut)"/>'
            f'<path d="{red}" fill="{RED}"/><path d="{en}" fill="#FFFFFF"/></g>'
            + leaf(rx, leaf_ty, 0.30, RED) + f'<path fill="{INK}" d="{wd}"/>')
    write("maple-lingua-5-fr-en", W, base + 0.25 * ws + PAD, body, "Maple Lingua")

split(); dot(); seal(); bubbles()
print("ok")
