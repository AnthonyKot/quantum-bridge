#!/usr/bin/env python3
"""Chapter 13 figure.

FIGURE RECORD
  channel  Bloch vectors in the x-z plane (all states here have r_y = 0).
           Top: one amplitude-damping interaction, gamma = 3/4, input |+>.
             Kraus K0 = diag(1, sqrt(1-gamma)) (no emission), K1 = sqrt(gamma)|0><1| (emission).
             Recorded outcome j: probability p_j = |K_j psi|^2, conditional state K_j psi / sqrt(p_j).
             Ignored outcome: the channel output sum_j K_j rho K_j^dag, whose Bloch vector is the
             p_j-weighted average of the two conditional Bloch vectors.
           Bottom: image of the whole Bloch ball (drawn as its x-z slice) under
             dephasing, p = 1/4: (x, z) -> ((1-2p) x, z);
             amplitude damping, gamma = 3/4: (x, z) -> (sqrt(1-gamma) x, (1-gamma) z + gamma);
             full damping, gamma = 1: every state -> (0, 1).

Run without arguments to print the numbers; --write regenerates the SVG.
scripts/check_calculations.py (test_13) recomputes the top panel from a joint unitary with an
environment qubit, and the bottom panel from Kraus operators on points of the circle.
"""
import math
import sys

from figlib import f, svg, write

GAMMA, P_DEPHASE = 0.75, 0.25
S2 = 1 / math.sqrt(2)
INPUT = (S2, S2)


def kraus(gamma):
    return [((1, 0), (0, math.sqrt(1 - gamma))), ((0, math.sqrt(gamma)), (0, 0))]


def apply(m, v):
    return tuple(sum(m[i][j] * v[j] for j in range(2)) for i in range(2))


def bloch(v):
    a, b = v
    return (2 * a * b, a * a - b * b)          # (r_x, r_z) for real amplitudes


def branches(gamma=GAMMA, psi=INPUT):
    out = []
    for name, k in zip(("no emission", "emission"), kraus(gamma)):
        w = apply(k, psi)
        p = w[0] ** 2 + w[1] ** 2
        cond = (w[0] / math.sqrt(p), w[1] / math.sqrt(p))
        out.append((name, p, cond, bloch(cond)))
    return out


def ignored(gamma=GAMMA):
    b = branches(gamma)
    return tuple(sum(p * r[i] for _, p, _, r in b) for i in range(2))


def dephase_map(x, z, p=P_DEPHASE):
    return (1 - 2 * p) * x, z


def damp_map(x, z, gamma=GAMMA):
    return math.sqrt(1 - gamma) * x, (1 - gamma) * z + gamma


def figure():
    width, radius, cx = 360, 112, 180
    out = []

    def disk(cy, title):
        out.append(f'<text class="fig-head" x="0" y="{cy - radius - 20}">{title}</text>')
        out.append(f'<circle class="fig-outline" cx="{cx}" cy="{cy}" r="{radius}"/>')
        out.append(f'<line class="fig-axis" x1="{cx - radius - 10}" y1="{cy}" x2="{cx + radius + 10}" y2="{cy}"/>')
        out.append(f'<line class="fig-axis" x1="{cx}" y1="{cy + radius + 10}" x2="{cx}" y2="{cy - radius - 10}"/>')
        return lambda x, z: (cx + radius * x, cy - radius * z)

    def dot(xy, css, text=None, dx=8, dy=-8, anchor="start", cls="fig-label"):
        out.append(f'<circle class="{css}" cx="{f(xy[0])}" cy="{f(xy[1])}" r="5"/>')
        if text:
            out.append(f'<text class="{cls}" x="{f(xy[0] + dx)}" y="{f(xy[1] + dy)}" text-anchor="{anchor}">{text}</text>')

    top = 158
    P = disk(top, "One interaction, three descriptions")
    b = branches()
    (_, p0, _, r0), (_, p1, _, r1) = b
    a0, a1, avg = P(*r0), P(*r1), P(*ignored())
    out.append(f'<line class="fig-chord" x1="{f(a0[0])}" y1="{f(a0[1])}" x2="{f(a1[0])}" y2="{f(a1[1])}"/>')
    start = P(*bloch(INPUT))
    out.append(f'<line class="fig-line fig-dashed" x1="{f(start[0])}" y1="{f(start[1])}" x2="{f(avg[0])}" y2="{f(avg[1])}"/>')
    dot(start, "fig-dot", "start |+⟩", 8, 18, "end", "fig-label fig-math")
    dot(a1, "fig-dot fig-dot-alt", "emission, p = 3/8", 10, -4, "start", "fig-label fig-alt-text")
    dot(a0, "fig-dot fig-dot-alt", "no emission", 10, -4, "start", "fig-label fig-alt-text")
    out.append(f'<text class="fig-label fig-alt-text" x="{f(a0[0] + 10)}" y="{f(a0[1] + 12)}">p = 5/8</text>')
    dot(avg, "fig-dot fig-dot-mixed", "outcome ignored", -10, 4, "end")

    mid = top + radius * 2 + 86
    P = disk(mid, "What each channel does to the whole ball")
    steps = [2 * math.pi * k / 120 for k in range(121)]

    def curve(points, css):
        d = " ".join(("M" if i == 0 else "L") + "{},{}".format(*map(f, P(*pt))) for i, pt in enumerate(points))
        out.append(f'<path class="{css}" d="{d}"/>')

    curve([dephase_map(math.sin(t), math.cos(t)) for t in steps], "fig-image fig-image-alt")
    curve([damp_map(math.sin(t), math.cos(t)) for t in steps], "fig-image")
    dot(P(0, 1), "fig-dot fig-dot-accent", "full damping → |0⟩", 10, -6, "start", "fig-label")
    x, y = P(*dephase_map(-1, 0))
    out.append(f'<text class="fig-label fig-alt-text" x="{f(x - 6)}" y="{f(y + 44)}" text-anchor="end">dephasing</text>')
    out.append(f'<text class="fig-label fig-alt-text" x="{f(x - 6)}" y="{f(y + 60)}" text-anchor="end">p = ¼</text>')
    x, y = P(*damp_map(1, 0))
    out.append(f'<text class="fig-label fig-accent-text" x="{f(x + 10)}" y="{f(y + 4)}">damping, γ = ¾</text>')
    desc = ("Top: a circle, the x-z slice of the Bloch ball. The input plus sits at the right edge. Two recorded outcomes lie on "
            "the circle: emission at the top, the state zero, with probability three eighths, and no emission at x 0.8, z 0.6, "
            "with probability five eighths. A segment joins them, and the ignored-outcome state lies on it inside the circle, at "
            "x one half, z three quarters. Bottom: the unit circle; dephasing squeezes it into a tall ellipse of half width; "
            "damping shrinks it into a small ellipse centred at z three quarters touching the top; full damping sends every state "
            "to the top point.")
    return svg("channel", width, mid + radius + 24, "Recorded, ignored, and the channel on the whole ball", desc, "\n".join(out))


if __name__ == "__main__":
    for name, p, cond, r in branches():
        print(f"{name:12s} p = {p:.4f}  state = {tuple(round(c, 4) for c in cond)}  r(x,z) = {tuple(round(v, 4) for v in r)}")
    print("ignored-outcome r(x,z) =", tuple(round(v, 4) for v in ignored()))
    if "--write" in sys.argv:
        print("wrote", write("13-open-systems-channels.html", {"channel": figure()}), "figure")
