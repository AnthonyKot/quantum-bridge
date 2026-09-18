#!/usr/bin/env python3
"""Chapter 3 figure.

FIGURE RECORD
  ensembles   The x-z cross-section of the Bloch ball (y = 0), unit radius.
              A mixture's Bloch vector is the probability-weighted average of its
              members' Bloch vectors, because rho = (I + r.sigma)/2 is linear in r.
              Top panel: |+> (pure, on the surface) against source C, the equal
              mixture of |0> and |1> (centre).
              Bottom panel: two ensembles for each of two density matrices.
                I/2:          1/2 |0>, 1/2 |1>    and   1/2 |+>, 1/2 |->
                diag(3/4,1/4): 3/4 |0>, 1/4 |1>    and   1/2 of each (sqrt3|0> +- |1>)/2
              Bloch vectors are computed from the kets, then averaged.

Run without arguments to print the numbers; --write regenerates the SVG.
scripts/check_calculations.py (test_03) rebuilds each density matrix from projectors.
"""
import math
import sys

from figlib import f, svg, write

S = 1 / math.sqrt(2)
KETS = {
    "|0⟩": (1, 0), "|1⟩": (0, 1), "|+⟩": (S, S), "|−⟩": (S, -S),
    "(√3|0⟩+|1⟩)/2": (math.sqrt(3) / 2, .5), "(√3|0⟩−|1⟩)/2": (math.sqrt(3) / 2, -.5),
}
ENSEMBLES = {
    "source C": [(.5, "|0⟩"), (.5, "|1⟩")],
    "plus-minus coin": [(.5, "|+⟩"), (.5, "|−⟩")],
    "3:1 coin": [(.75, "|0⟩"), (.25, "|1⟩")],
    "tilted pair": [(.5, "(√3|0⟩+|1⟩)/2"), (.5, "(√3|0⟩−|1⟩)/2")],
}


def bloch(ket):
    a, b = map(complex, ket)
    c = a.conjugate() * b
    return (2 * c.real, 2 * c.imag, abs(a) ** 2 - abs(b) ** 2)


def average(ensemble):
    return tuple(sum(w * bloch(KETS[name])[i] for w, name in ensemble) for i in range(3))


def figure():
    width, radius = 360, 118
    out = []

    def disk(cy, title):
        cx = 180
        out.append(f'<text class="fig-head" x="0" y="{cy - radius - 22}">{title}</text>')
        out.append(f'<circle class="fig-outline" cx="{cx}" cy="{cy}" r="{radius}"/>')
        out.append(f'<line class="fig-axis" x1="{cx - radius - 12}" y1="{cy}" x2="{cx + radius + 12}" y2="{cy}"/>')
        out.append(f'<line class="fig-axis" x1="{cx}" y1="{cy + radius + 12}" x2="{cx}" y2="{cy - radius - 12}"/>')
        out.append(f'<text class="fig-label fig-soft fig-italic" x="{cx + radius + 8}" y="{cy + 18}">x</text>')
        out.append(f'<text class="fig-label fig-soft fig-italic" x="{cx - 8}" y="{cy - radius - 4}" text-anchor="end">z</text>')
        return lambda r: (cx + radius * r[0], cy - radius * r[2])

    def point(xy, css, label=None, dx=8, dy=-8, anchor="start", math_font=True):
        out.append(f'<circle class="{css}" cx="{f(xy[0])}" cy="{f(xy[1])}" r="5"/>')
        if label:
            cls = "fig-label fig-math" if math_font else "fig-label"
            out.append(f'<text class="{cls}" x="{f(xy[0] + dx)}" y="{f(xy[1] + dy)}" text-anchor="{anchor}">{label}</text>')

    def chord(proj, a, b, css="fig-line fig-dashed"):
        (x1, y1), (x2, y2) = proj(bloch(KETS[a])), proj(bloch(KETS[b]))
        out.append(f'<line class="{css}" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}"/>')

    top = 170
    proj = disk(top, "A superposition and a mixture")
    chord(proj, "|0⟩", "|1⟩", "fig-chord")
    point(proj(bloch(KETS["|0⟩"])), "fig-dot", "|0⟩", 10, -6)
    point(proj(bloch(KETS["|1⟩"])), "fig-dot", "|1⟩", 10, 16)
    point(proj(bloch(KETS["|+⟩"])), "fig-dot fig-dot-accent", "|+⟩", 4, -12)
    out.append(f'<text class="fig-label fig-soft" x="{f(proj((1, 0, 0))[0] - 14)}" y="{f(top + 32)}" text-anchor="end">source A, pure</text>')
    point(proj(average(ENSEMBLES["source C"])), "fig-dot fig-dot-mixed", "source C", -10, -10, "end", False)

    mid = 520
    proj = disk(mid, "Different mixtures, one matrix")
    chord(proj, "|0⟩", "|1⟩", "fig-chord")
    chord(proj, "|+⟩", "|−⟩", "fig-chord")
    chord(proj, "(√3|0⟩+|1⟩)/2", "(√3|0⟩−|1⟩)/2", "fig-chord fig-chord-alt")
    for name, (dx, dy, anchor) in {"|0⟩": (10, -6, "start"), "|1⟩": (10, 16, "start"), "|+⟩": (4, -10, "start"),
                                   "|−⟩": (-4, -10, "end")}.items():
        point(proj(bloch(KETS[name])), "fig-dot", name, dx, dy, anchor)
    for name, dx, anchor in (("(√3|0⟩+|1⟩)/2", 8, "start"), ("(√3|0⟩−|1⟩)/2", -8, "end")):
        x, y = proj(bloch(KETS[name]))
        out.append(f'<circle class="fig-dot" cx="{f(x)}" cy="{f(y)}" r="5"/>')
    point(proj(average(ENSEMBLES["source C"])), "fig-dot fig-dot-mixed", "I/2", 10, 20, "start")
    point(proj(average(ENSEMBLES["3:1 coin"])), "fig-dot fig-dot-mixed", "diag(¾, ¼)", 10, 18, "start")
    return svg("ensembles", width, mid + radius + 26, "Mixtures inside the Bloch ball", DESC, "\n".join(out))


DESC = ("Two circles, each the x-z slice of the Bloch ball. Top: zero at the top, one at the bottom, plus at the right "
        "edge. Source C, the equal mixture of zero and one, is the midpoint of the vertical line joining them, at the "
        "centre. Bottom: the vertical line from zero to one and the horizontal line from minus to plus cross at the "
        "centre, labelled I over 2. A second horizontal line, at height one half, joins the two tilted states; its "
        "midpoint is on the vertical line at height one half, labelled diag three quarters, one quarter, which is also "
        "three quarters of the way from one to zero.")


if __name__ == "__main__":
    for name, ens in ENSEMBLES.items():
        print(f"{name:16s} r = {tuple(round(v, 4) for v in average(ens))}")
    print("|+> r =", bloch(KETS["|+⟩"]))
    if "--write" in sys.argv:
        print("wrote", write("03-density-matrix.html", {"ensembles": figure()}), "figure")
