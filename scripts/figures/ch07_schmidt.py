#!/usr/bin/env python3
"""Chapter 7 figure.

FIGURE RECORD
  schmidt   Three two-qubit pure states, coefficients C_ij = amplitude of |ij>
            (row i = qubit A, column j = qubit B):
              |+>|1>                          C = [[0, 1/sqrt2], [0, 1/sqrt2]]
              (|00> + |01> + |10>)/sqrt3      C = [[1, 1], [1, 0]]/sqrt3
              (|00> + |11>)/sqrt2             C = [[1, 0], [0, 1]]/sqrt2
            For each: the matrix, det C, and the squared Schmidt coefficients s_k^2,
            which are the eigenvalues of rho_A = C C^dagger (closed form for 2x2).

Run without arguments to print the numbers; --write regenerates the SVG.
scripts/check_calculations.py (test_07) checks the spectra through s1^2 s2^2 = |det C|^2.
"""
import math
import sys

from figlib import f, svg, write

R2, R3 = math.sqrt(2), math.sqrt(3)
STATES = [
    ("|+⟩|1⟩, a product", [[0, 1 / R2], [0, 1 / R2]]),
    ("(|00⟩+|01⟩+|10⟩)/√3", [[1 / R3, 1 / R3], [1 / R3, 0]]),
    ("(|00⟩+|11⟩)/√2, a Bell pair", [[1 / R2, 0], [0, 1 / R2]]),
]
ENTRY = {0: "0", 1 / R2: "1/√2", 1 / R3: "1/√3"}


def det(c):
    return c[0][0] * c[1][1] - c[0][1] * c[1][0]


def schmidt_squares(c):
    rho = [[sum(c[i][k] * c[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
    tr = rho[0][0] + rho[1][1]
    d = rho[0][0] * rho[1][1] - rho[0][1] * rho[1][0]
    disc = math.sqrt(max(tr * tr / 4 - d, 0))
    return tr / 2 + disc, tr / 2 - disc


def entry(v):
    for k, t in ENTRY.items():
        if abs(v - k) < 1e-9:
            return t
    return f"{v:.2f}"


def fraction(v):
    for k, t in ((0, "0"), (.5, "½"), (1, "1"), (1 / 3, "⅓"), (-1 / 3, "−⅓")):
        if abs(v - k) < 1e-9:
            return t
    return f"{v:.3f}"


def figure():
    width = 360
    out = [f'<text class="fig-label fig-soft" x="0" y="16">coefficients C</text>',
           f'<text class="fig-label fig-soft" x="150" y="16">det C</text>',
           f'<text class="fig-label fig-soft" x="222" y="16">Schmidt s²</text>']
    for i, (name, c) in enumerate(STATES):
        y0 = 26 + 132 * i
        out.append(f'<line class="fig-rule" x1="0" y1="{y0}" x2="{width}" y2="{y0}"/>')
        out.append(f'<text class="fig-label fig-strong fig-math" x="0" y="{y0 + 22}">{name}</text>')
        for r in range(2):
            for k in range(2):
                v = c[r][k]
                x, y = 22 + 52 * k, y0 + 36 + 40 * r
                css = "fig-cell fig-cell-on" if abs(v) > 1e-9 else "fig-cell"
                out.append(f'<rect class="{css}" x="{x}" y="{y}" width="50" height="38"/>')
                out.append(f'<text class="fig-label fig-math" x="{x + 25}" y="{y + 24}" text-anchor="middle">{entry(v)}</text>')
        out.append(f'<text class="fig-label fig-strong" x="150" y="{y0 + 80}">{fraction(det(c))}</text>')
        lam = schmidt_squares(c)
        for k, l in enumerate(lam):
            y = y0 + 44 + 34 * k
            out.append(f'<line class="fig-axis" x1="222" y1="{y - 2}" x2="222" y2="{y + 24}"/>')
            if l > 1e-9:
                out.append(f'<rect class="fig-bar" x="222" y="{y}" width="{f(100 * l)}" height="22"/>')
            out.append(f'<text class="fig-label" x="{f(228 + 100 * l)}" y="{y + 16}">{fraction(l)}</text>')
    end = 26 + 132 * 3
    out.append(f'<line class="fig-rule" x1="0" y1="{end}" x2="{width}" y2="{end}"/>')
    desc = ("Three rows. The product state has coefficient matrix with entries zero and one over root two in the right-hand "
            "column only, determinant zero, and Schmidt squares one and zero. The worked state has entries one over root three "
            "except a zero in the bottom right, determinant minus one third, and Schmidt squares 0.873 and 0.127. The Bell pair "
            "has one over root two on the diagonal, determinant one half, and Schmidt squares one half and one half.")
    return svg("schmidt", width, end + 4, "From coefficient matrix to Schmidt coefficients", desc, "\n".join(out))


if __name__ == "__main__":
    for name, c in STATES:
        print(f"{name:30s} det = {det(c):+.4f}  s^2 = {tuple(round(v, 4) for v in schmidt_squares(c))}")
    if "--write" in sys.argv:
        print("wrote", write("07-entanglement-schmidt.html", {"schmidt": figure()}), "figure")
