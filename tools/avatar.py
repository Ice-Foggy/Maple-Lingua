import sys
fontdir, out = sys.argv[1], sys.argv[2]
sys.argv = ["x", fontdir, out + "/_tmp"]
sys.path.insert(0, sys.argv[0] if False else __import__("os").path.dirname(__file__))
import build_logos as B
N = 1024
def leaf_split(tx, ty, s):
    return (f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s})">'
            f'<polygon clip-path="url(#l)" fill="{B.BLUE}" points="{B.LEAF}"/>'
            f'<polygon clip-path="url(#r)" fill="{B.RED}" points="{B.LEAF}"/></g>')
defs = ('<defs><clipPath id="l"><rect x="0" y="0" width="48.6" height="100"/></clipPath>'
        '<clipPath id="r"><rect x="51.4" y="0" width="48.6" height="100"/></clipPath></defs>')
def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{N}" height="{N}" viewBox="0 0 {N} {N}">'
            f'{defs}<rect width="{N}" height="{N}" fill="#FFFFFF"/>{body}</svg>\n')
# A: leaf only (leaf ink spans y 5..90, x 8..92 in its 100 box)
s = 6.8; cx, cy = 50, 47.5
open(f"{out}/avatar-2-list.svg", "w").write(svg(leaf_split(N/2 - cx*s, N/2 - cy*s, s)))
# B: leaf + wordmark
s = 4.8; size, sp = 96, 6
_, w, _ = B.M800.shape("MAPLE LINGUA", size, sp)
if w > 760: size = size * 760 / w; sp = sp * 760 / w; _, w, _ = B.M800.shape("MAPLE LINGUA", size, sp)
cap = B.M800.cap * size; gap = 44
block = 85 * s + gap + cap
top = (N - block) / 2
leafpart = leaf_split(N/2 - cx*s, top - 5*s, s)
d, _ = B.M800.text_d("MAPLE LINGUA", size, N/2, top + 85*s + gap + cap, sp, "middle")
open(f"{out}/avatar-2-list-s-nazvaniem.svg", "w").write(svg(leafpart + f'<path fill="{B.INK}" d="{d}"/>'))
print("ok")
