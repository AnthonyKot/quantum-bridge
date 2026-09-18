#!/usr/bin/env python3
"""Chapter 6 figure.

FIGURE RECORD
  linearity  Two qubits, basis 00, 01, 10, 11 (first symbol = the input register,
             second = the blank, initially |0>). A copier that works on |0> and |1>
             must send |00> -> |00> and |10> -> |11> (as CNOT does). Rows of real
             amplitudes: the copier's outputs for |0> and |1>; its output for |+>, which
             linearity fixes as (row 1 + row 2)/sqrt2; and |+>|+>, what two copies of
             |+> would be.

Run without arguments to print the numbers; --write regenerates the SVG.
scripts/check_calculations.py (test_06) checks the rows with CNOT and tensor products.
"""
import math
import sys

from figlib import f, svg, write

S = 1 / math.sqrt(2)
LABELS = ["00", "01", "10", "11"]
COPY0 = {"00": 1.0, "01": 0.0, "10": 0.0, "11": 0.0}
COPY1 = {"00": 0.0, "01": 0.0, "10": 0.0, "11": 1.0}


def forced_for_plus():
    """Linearity: U(|+>|0>) = (U|00> + U|10>)/sqrt2."""
    return {k: S * (COPY0[k] + COPY1[k]) for k in LABELS}


def two_copies_of_plus():
    plus = {"0": S, "1": S}
    return {k: plus[k[0]] * plus[k[1]] for k in LABELS}


def rows():
    return [("Input |0⟩: copied, |00⟩", COPY0, "fig-bar-plain"),
            ("Input |1⟩: copied, |11⟩", COPY1, "fig-bar-plain"),
            ("Input |+⟩: what linearity forces", forced_for_plus(), "fig-bar"),
            ("What two copies of |+⟩ would be", two_copies_of_plus(), "fig-bar-alt")]


def label(a):
    for v, t in ((0, "0"), (1, "1"), (S, "1/√2"), (.5, "½")):
        if abs(a - v) < 1e-9:
            return t
    return f"{a:.2f}"


def figure():
    width, unit = 360, 36
    out = []
    for i, (title, state, css) in enumerate(rows()):
        y0 = 104 * i
        out.append(f'<line class="fig-rule" x1="0" y1="{y0 + 2}" x2="{width}" y2="{y0 + 2}"/>')
        out.append(f'<text class="fig-label fig-strong fig-math" x="0" y="{y0 + 22}">{title}</text>')
        base = y0 + 66
        out.append(f'<line class="fig-axis" x1="60" y1="{base}" x2="{width - 10}" y2="{base}"/>')
        for j, k in enumerate(LABELS):
            a = state[k]
            x = 76 + 72 * j
            if abs(a) > 1e-9:
                out.append(f'<rect class="{css}" x="{x}" y="{f(base - unit * a)}" width="34" height="{f(unit * a)}"/>')
                out.append(f'<text class="fig-label" x="{x + 40}" y="{f(base - unit * a / 2 + 4)}">{label(a)}</text>')
            out.append(f'<text class="fig-label fig-math" x="{x + 17}" y="{base + 20}" text-anchor="middle">|{k}⟩</text>')
    end = 104 * 4 + 2
    out.append(f'<line class="fig-rule" x1="0" y1="{end}" x2="{width}" y2="{end}"/>')
    desc = ("Four rows of amplitude bars over 00, 01, 10, 11. Input zero is copied to 00, and input one to 11. For input plus, "
            "linearity forces amplitude one over root two on 00 and on 11 and nothing on 01 or 10. Two copies of plus would "
            "instead have amplitude one half on all four.")
    return svg("linearity", width, end + 4, "What a copier must do to a superposition", desc, "\n".join(out))


if __name__ == "__main__":
    for title, state, _ in rows():
        print(f"{title:34s}", {k: round(v, 4) for k, v in state.items()})
    if "--write" in sys.argv:
        print("wrote", write("06-linearity-no-cloning.html", {"linearity": figure()}), "figure")
