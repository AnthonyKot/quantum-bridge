#!/usr/bin/env python3
"""Chapter 10 figure.

FIGURE RECORD
  kickback  Two input bits, basis order 00, 01, 10, 11 (first bit leftmost).
            Three functions: constant f = 0; balanced f = x1 xor x2 (the chapter's
            worked example); balanced f = x1.
            Left panel: data-register amplitudes after H x H and one oracle call with a
            |-> target, (-1)^f(x) / 2. Right panel: amplitudes after the final H x H,
            a_z = (1/4) sum_x (-1)^(f(x) + x.z), the chapter's formula.

Run without arguments to print the numbers; --write regenerates the SVG.
scripts/check_calculations.py (test_10) recomputes both panels with 4x4 matrices.
"""
import sys

from figlib import f, svg, write

LABELS = ["00", "01", "10", "11"]
FUNCTIONS = [
    ("constant, f = 0", lambda x1, x2: 0),
    ("balanced, f = x₁ ⊕ x₂", lambda x1, x2: x1 ^ x2),
    ("balanced, f = x₁", lambda x1, x2: x1),
]


def bits(label):
    return int(label[0]), int(label[1])


def after_oracle(fn):
    return {k: (-1) ** fn(*bits(k)) / 2 for k in LABELS}


def after_hadamards(fn):
    out = {}
    for z in LABELS:
        z1, z2 = bits(z)
        out[z] = sum((-1) ** (fn(*bits(x)) + (bits(x)[0] * z1 + bits(x)[1] * z2)) for x in LABELS) / 4
    return out


def label(a):
    for v, t in ((0, ""), (1, "1"), (-1, "−1"), (.5, "½"), (-.5, "−½")):
        if abs(a - v) < 1e-9:
            return t
    return f"{a:.2f}"


def panel(out, x0, base, state, css, unit):
    out.append(f'<line class="fig-axis" x1="{x0 - 4}" y1="{base}" x2="{x0 + 150}" y2="{base}"/>')
    for j, k in enumerate(LABELS):
        a, x = state[k], x0 + 38 * j
        if abs(a) > 1e-9:
            top, h = (base - unit * a, unit * a) if a > 0 else (base, -unit * a)
            out.append(f'<rect class="{css}" x="{x}" y="{f(top)}" width="26" height="{f(h)}"/>')
            ty = base - unit * a - 5 if a > 0 else base - unit * a + 14
            out.append(f'<text class="fig-label" x="{x + 13}" y="{f(ty)}" text-anchor="middle">{label(a)}</text>')
        out.append(f'<text class="fig-label fig-soft" x="{x + 13}" y="{f(base + 58)}" text-anchor="middle">{k}</text>')


def figure():
    width, unit = 360, 38
    out = [f'<text class="fig-head" x="8" y="16">After the oracle</text>',
           f'<text class="fig-head" x="200" y="16">After the last H⊗H</text>']
    for i, (name, fn) in enumerate(FUNCTIONS):
        y0 = 26 + 142 * i
        out.append(f'<line class="fig-rule" x1="0" y1="{y0}" x2="{width}" y2="{y0}"/>')
        out.append(f'<text class="fig-label fig-strong fig-math" x="0" y="{y0 + 20}">{name}</text>')
        base = y0 + 72
        panel(out, 12, base, after_oracle(fn), "fig-bar-plain", unit)
        panel(out, 204, base, after_hadamards(fn), "fig-bar", unit)
    end = 26 + 142 * 3
    out.append(f'<line class="fig-rule" x1="0" y1="{end}" x2="{width}" y2="{end}"/>')
    desc = ("Three rows, each with two small bar charts over 00, 01, 10, 11. After the oracle every amplitude is plus or minus "
            "one half: all positive for the constant function; plus, minus, minus, plus for x1 xor x2; plus, plus, minus, minus "
            "for f equals x1. After the final Hadamards all the amplitude is on one string: 00 for the constant function, 11 for "
            "x1 xor x2, and 10 for f equals x1.")
    return svg("kickback", width, end + 4, "Signs after the oracle, and where the final Hadamards send them", desc, "\n".join(out))


if __name__ == "__main__":
    for name, fn in FUNCTIONS:
        print(f"{name:26s}", [after_oracle(fn)[k] for k in LABELS], "->", [after_hadamards(fn)[k] for k in LABELS])
    if "--write" in sys.argv:
        print("wrote", write("10-interference-deutsch.html", {"kickback": figure()}), "figure")
