#!/usr/bin/env python3
"""Chapter 2 figures.

FIGURE RECORD
  apparatus   Input (sqrt3|0> + i|1>)/2, the chapter's running example. Two apparatuses:
              M_0 = |0><0|, M_1 = |1><1| (ideal), and N_m = X M_m, that is
              N_0 = |1><0|, N_1 = |0><1|. For each branch: probability
              p(m) = |M_m psi|^2, normalised conditional state M_m psi / sqrt(p(m))
              (named up to a global phase), and the certain outcome of an immediate
              second reading by the same apparatus.
  unambiguous Inputs |0> and |+>. Effects E_0 = c|-><-| ("says |0>"), E_+ = c|1><1|
              ("says |+>"), E_? = I - E_0 - E_+, with c = 2 - sqrt2. Bars: <v|E|v>.

Both figures are narrow (360 units) so that on a phone each outcome, its probability
and its state are visible together without sideways scrolling.

Run without arguments to print the numbers; --write regenerates the SVG.
scripts/check_calculations.py (test_02) checks them with matrix products.
"""
import math
import sys

from figlib import f, svg, write

S = 1 / math.sqrt(2)
EXAMPLE = (math.sqrt(3) / 2, 0.5j)
EXAMPLE_LABEL = "(√3|0⟩ + i|1⟩)/2"
BASIS = {"|0⟩": (1, 0), "|1⟩": (0, 1)}
M = {0: ((1, 0), (0, 0)), 1: ((0, 0), (0, 1))}
XGATE = ((0, 1), (1, 0))
C = 2 - math.sqrt(2)


def matmul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


N = {m: matmul(XGATE, M[m]) for m in (0, 1)}
APPARATUS = {"M": M, "N": N}


def apply(matrix, v):
    return tuple(sum(complex(matrix[i][j]) * complex(v[j]) for j in range(2)) for i in range(2))


def norm2(v):
    return sum(abs(a) ** 2 for a in v)


def name_of(v):
    """Name a normalised vector as a basis ket, ignoring a global phase."""
    for name, k in BASIS.items():
        if abs(abs(sum(complex(a).conjugate() * b for a, b in zip(k, v))) - 1) < 1e-9:
            return name
    raise ValueError(v)


def branches(apparatus, state=EXAMPLE):
    ops = APPARATUS[apparatus]
    rows = []
    for m in (0, 1):
        out = apply(ops[m], state)
        p = norm2(out)
        after = tuple(a / math.sqrt(p) for a in out)
        again = [n for n in (0, 1) if abs(norm2(apply(ops[n], after)) - 1) < 1e-9]
        rows.append({"reading": m, "p": p, "state": after, "name": name_of(after), "again": again[0]})
    return rows


def overlap2(a, b):
    return abs(sum(complex(x).conjugate() * complex(y) for x, y in zip(a, b))) ** 2


def unambiguous_rows():
    one, minus = (0, 1), (S, -S)
    rows = []
    for name, v in (("Input |0⟩", (1, 0)), ("Input |+⟩", (S, S))):
        says_zero, says_plus = C * overlap2(minus, v), C * overlap2(one, v)
        rows.append((name, [says_zero, says_plus, 1 - says_zero - says_plus]))
    return rows


def frac(p):
    for value, text in ((0, "0"), (.25, "¼"), (.75, "¾"), (1, "1")):
        if abs(p - value) < 1e-9:
            return text
    return f"{p:.3f}"


def figure_apparatus():
    width, height = 360, 372
    out = [f'<text class="fig-label fig-soft" x="0" y="18">Prepared state</text>',
           f'<text class="fig-label fig-math" x="108" y="19">{EXAMPLE_LABEL}</text>']
    specs = (("M", "Apparatus M", "M₀ = |0⟩⟨0|,  M₁ = |1⟩⟨1|"),
             ("N", "Apparatus N", "N₀ = |1⟩⟨0|,  N₁ = |0⟩⟨1|"))
    for i, (key, title, ops) in enumerate(specs):
        top = 36 + 168 * i
        out.append(f'<line class="fig-rule" x1="0" y1="{top}" x2="{width}" y2="{top}"/>')
        out.append(f'<text class="fig-label fig-strong" x="0" y="{top + 22}">{title}</text>')
        out.append(f'<text class="fig-label fig-math fig-soft" x="112" y="{top + 23}">{ops}</text>')
        out.append(f'<text class="fig-label fig-soft" x="98" y="{top + 50}" text-anchor="middle">reads</text>')
        out.append(f'<text class="fig-label fig-soft" x="178" y="{top + 50}">state left</text>')
        out.append(f'<text class="fig-label fig-soft" x="264" y="{top + 50}">reads again</text>')
        root = (14, top + 104)
        out.append(f'<circle class="fig-dot" cx="{root[0]}" cy="{root[1]}" r="4"/>')
        for b in branches(key):
            y = top + 78 + 54 * b["reading"]
            out.append(f'<line class="fig-line fig-branch" x1="{root[0]}" y1="{root[1]}" x2="{86}" y2="{y}"/>')
            mx, my = (root[0] + 86) / 2, (root[1] + y) / 2
            dy = -8 if b["reading"] == 0 else 17
            out.append(f'<text class="fig-label fig-strong" x="{f(mx - 4)}" y="{f(my + dy)}" text-anchor="middle">{frac(b["p"])}</text>')
            out.append(f'<circle class="fig-node" cx="98" cy="{y}" r="12"/>')
            out.append(f'<text class="fig-label fig-strong" x="98" y="{y + 5}" text-anchor="middle">{b["reading"]}</text>')
            changed = b["name"] != f'|{b["reading"]}⟩'
            accent = " fig-accent-text" if changed else ""
            out.append(f'<text class="fig-label fig-soft" x="{126}" y="{y + 5}">→</text>')
            out.append(f'<text class="fig-label fig-math{accent}" x="178" y="{y + 6}">{b["name"]}</text>')
            out.append(f'<text class="fig-label fig-soft" x="{226}" y="{y + 5}">→</text>')
            out.append(f'<text class="fig-label{accent}" x="264" y="{y + 5}">{b["again"]}, certainly</text>')
    out.append(f'<line class="fig-rule" x1="0" y1="{36 + 336}" x2="{width}" y2="{36 + 336}"/>')
    desc = ("Two branching diagrams for the same prepared state. Apparatus M reads 0 with probability three quarters and "
            "leaves the state 0, or reads 1 with probability one quarter and leaves the state 1; reading again repeats the "
            "first answer. Apparatus N has the same two probabilities but leaves the state 1 after reading 0 and the state 0 "
            "after reading 1, so reading again gives the opposite answer.")
    return svg("apparatus", width, height + 2, "Same probabilities, different states left behind", desc, "\n".join(out))


def figure_unambiguous():
    width = 360
    labels = ("says “it was |0⟩”", "says “it was |+⟩”", "says “don’t know”")
    out = []
    y = 0
    for i, (name, probs) in enumerate(unambiguous_rows()):
        out.append(f'<line class="fig-rule" x1="0" y1="{y + 4}" x2="{width}" y2="{y + 4}"/>')
        out.append(f'<text class="fig-label fig-strong fig-math" x="0" y="{y + 26}">{name}</text>')
        for j, p in enumerate(probs):
            ry = y + 42 + 30 * j
            correct = j == i
            out.append(f'<text class="fig-label fig-math" x="0" y="{ry + 15}">{labels[j]}</text>')
            out.append(f'<line class="fig-axis" x1="150" y1="{ry - 2}" x2="150" y2="{ry + 22}"/>')
            if p > 1e-9:
                css = "fig-bar" if correct else "fig-bar-plain"
                out.append(f'<rect class="{css}" x="150" y="{ry}" width="{f(170 * p)}" height="20"/>')
            out.append(f'<text class="fig-label" x="{f(156 + 170 * p)}" y="{ry + 15}">{frac(p)}</text>')
        y += 140
    out.append(f'<line class="fig-rule" x1="0" y1="{y + 4}" x2="{width}" y2="{y + 4}"/>')
    desc = ("Outcome probabilities for the three-outcome measurement. Input zero: says zero with probability 0.293, says plus "
            "with probability zero, don't know with probability 0.707. Input plus: says zero with probability zero, says plus "
            "with probability 0.293, don't know with probability 0.707. A wrong identification never occurs.")
    return svg("unambiguous", width, y + 8, "A measurement that is never wrong", desc, "\n".join(out))


if __name__ == "__main__":
    for key in APPARATUS:
        rows = branches(key)
        print(f"Apparatus {key}: total probability {sum(r['p'] for r in rows):.3f}")
        for r in rows:
            print(f"  reads {r['reading']} with p = {r['p']:.3f}, leaves {r['name']} (norm {norm2(r['state']):.3f}), "
                  f"reads {r['again']} again")
    for name, probs in unambiguous_rows():
        print(name, [round(q, 4) for q in probs], "sum", round(sum(probs), 6))
    if "--write" in sys.argv:
        n = write("02-observables-measurement.html",
                  {"apparatus": figure_apparatus(), "unambiguous": figure_unambiguous()})
        print(f"wrote {n} figures")
