#!/usr/bin/env python3
"""Chapter 12 figures.

FIGURE RECORD
  amplitudes  N = 4, marked item w = 2 (binary 10, leftmost register first).
              Three panels of the four real amplitudes: start, after the oracle,
              after diffusion. Computed by the mean-reflection rule a -> 2*mean - a.
              The dashed line in the middle panel is the amplitude mean, 1/4.
  rotation    N = 8, one marked item. Left: the state after k = 0..3 iterations in
              the plane spanned by |r> (horizontal) and |w> (vertical), at angle
              (2k+1)*theta from |r>, sin(theta) = 1/sqrt(8). The dashed vector is
              the state after the first oracle call, at angle -theta.
              Right: success probability p_k = sin^2((2k+1) theta), k = 0..6.

Run without arguments to print the numbers; --write regenerates the SVG.
scripts/check_calculations.py (test_12) checks these numbers against a direct
matrix simulation of G = D O_w.
"""
import math
import sys

from figlib import f, svg, write

N_SMALL, W_SMALL = 4, 2
N_PLANE = 8
K_VECTORS = 4
K_BARS = 7


def oracle(amplitudes, w):
    return [-a if x == w else a for x, a in enumerate(amplitudes)]


def diffusion(amplitudes):
    mean = sum(amplitudes) / len(amplitudes)
    return [2 * mean - a for a in amplitudes]


def small_panels():
    start = [1 / math.sqrt(N_SMALL)] * N_SMALL
    after_oracle = oracle(start, W_SMALL)
    return [("1. Start", start), ("2. After the oracle", after_oracle),
            ("3. After diffusion", diffusion(after_oracle))]


def theta(n):
    return math.asin(1 / math.sqrt(n))


def angle(k, n):
    return (2 * k + 1) * theta(n)


def success(k, n):
    return math.sin(angle(k, n)) ** 2


def stopping_count(n):
    return round(math.pi / (4 * theta(n)) - .5)


def label_probability(p):
    """Two decimals, except that a value just short of one is not printed as 1.00."""
    return f"{p:.4f}" if .995 <= p < 1 - 1e-9 else f"{math.floor(p * 100 + .5) / 100:.2f}"


def label(value):
    for v, text in ((0, "0"), (.25, "¼"), (.5, "½"), (-.5, "−½"), (1, "1")):
        if abs(value - v) < 1e-9:
            return text
    return f"{value:.2f}"


def figure_amplitudes():
    width, height, base, unit = 680, 268, 140, 80
    out = []
    for i, (title, amps) in enumerate(small_panels()):
        x0 = 20 + 225 * i
        out.append(f'<text class="fig-head" x="{x0}" y="22">{title}</text>')
        out.append(f'<line class="fig-axis" x1="{x0}" y1="{base}" x2="{x0 + 190}" y2="{base}"/>')
        if i == 1:
            mean = sum(amps) / len(amps)
            y = base - unit * mean
            out.append(f'<line class="fig-line fig-dashed" x1="{x0}" y1="{f(y)}" x2="{x0 + 190}" y2="{f(y)}"/>')
            out.append(f'<text class="fig-label fig-soft" x="{x0 + 12 + 44 * W_SMALL + 15}" y="{f(y - 7)}" text-anchor="middle">mean {label(mean)}</text>')
        for x, a in enumerate(amps):
            bx = x0 + 12 + 44 * x
            css = "fig-bar" if x == W_SMALL else "fig-bar-plain"
            top, h = (base - unit * a, unit * a) if a >= 0 else (base, -unit * a)
            if abs(a) > 1e-9:
                out.append(f'<rect class="{css}" x="{bx}" y="{f(top)}" width="30" height="{f(h)}"/>')
            ty = base - unit * a - 7 if a >= 0 else base - unit * a + 17
            out.append(f'<text class="fig-label" x="{bx + 15}" y="{f(ty)}" text-anchor="middle">{label(a)}</text>')
            out.append(f'<text class="fig-label{" fig-strong" if x == W_SMALL else ""}" x="{bx + 15}" y="224" text-anchor="middle">{x}</text>')
            out.append(f'<text class="fig-label fig-soft" x="{bx + 15}" y="242" text-anchor="middle">{x:02b}</text>')
    out.append(f'<text class="fig-label fig-soft" x="{width - 4}" y="263" text-anchor="end">candidate x (decimal, binary); the marked item is 2</text>')
    desc = ("Three bar charts of four amplitudes. At the start all four are one half. After the oracle the marked "
            "amplitude, item 2, is minus one half and the mean of the four is one quarter. After diffusion the marked "
            "amplitude is one and the other three are zero.")
    return svg("amplitudes", width, height, "One Grover iteration with four candidates", desc, "\n".join(out))


def figure_rotation():
    width, height = 680, 345
    ox, oy, radius = 165, 255, 140
    n = N_PLANE
    out = [f'<text class="fig-head" x="20" y="22">The state in the plane of |r⟩ and |w⟩, N = 8</text>',
           f'<text class="fig-head" x="425" y="22">Success probability after k iterations</text>']

    def tip(a, r=radius):
        return ox + r * math.cos(a), oy - r * math.sin(a)

    arc = " ".join(("M" if j == 0 else "L") + "{},{}".format(*map(f, tip(math.radians(d))))
                   for j, d in enumerate(range(-21, 181, 3)))
    out.append(f'<path class="fig-line" d="{arc}"/>')
    out.append(f'<line class="fig-axis" x1="{ox - radius - 10}" y1="{oy}" x2="{ox + radius + 22}" y2="{oy}"/>')
    out.append(f'<line class="fig-axis" x1="{ox}" y1="{oy + 70}" x2="{ox}" y2="{oy - radius - 22}"/>')
    out.append(f'<text class="fig-label fig-math" x="{ox + radius + 8}" y="{oy - 8}">|r⟩</text>')
    out.append(f'<text class="fig-label fig-math" x="{ox + 8}" y="{oy - radius - 12}">|w⟩</text>')

    x, y = tip(-theta(n))
    out.append(f'<line class="fig-line fig-dashed" x1="{ox}" y1="{oy}" x2="{f(x)}" y2="{f(y)}"/>')
    out.append(f'<text class="fig-label fig-soft" x="{f(x + 4)}" y="{f(y + 18)}" text-anchor="end">after the first oracle call</text>')

    best = stopping_count(n)
    for k in range(K_VECTORS):
        a = angle(k, n)
        x, y = tip(a)
        css = "fig-vector" if k == best else "fig-vector fig-vector-plain"
        out.append(f'<line class="{css}" x1="{ox}" y1="{oy}" x2="{f(x)}" y2="{f(y)}"/>')
        out.append(f'<circle class="fig-dot{" fig-dot-accent" if k == best else ""}" cx="{f(x)}" cy="{f(y)}" r="4.5"/>')
        lx, ly = tip(a, radius + 20)
        anchor = "start" if math.cos(a) > .3 else ("end" if math.cos(a) < -.3 else "middle")
        text = "k = 0 (start)" if k == 0 else f"k = {k}"
        out.append(f'<text class="fig-label" x="{f(lx)}" y="{f(ly + 4)}" text-anchor="{anchor}">{text}</text>')
    mx, my = tip(theta(n) / 2, 62)
    out.append(f'<text class="fig-label fig-soft fig-italic" x="{f(mx)}" y="{f(my + 4)}">θ</text>')
    mx, my = tip(2 * theta(n), 70)
    out.append(f'<text class="fig-label fig-soft fig-italic" x="{f(mx)}" y="{f(my)}">2θ</text>')

    bx0, base, scale, step = 440, 285, 210, 33
    out.append(f'<line class="fig-axis" x1="{bx0 - 8}" y1="{base}" x2="{bx0 + step * K_BARS}" y2="{base}"/>')
    for level in (0, .5, 1):
        yy = base - scale * level
        out.append(f'<line class="fig-rule" x1="{bx0 - 8}" y1="{f(yy)}" x2="{bx0 + step * K_BARS}" y2="{f(yy)}"/>')
        out.append(f'<text class="fig-label fig-soft" x="{bx0 - 12}" y="{f(yy + 4)}" text-anchor="end">{label(level)}</text>')
    for k in range(K_BARS):
        p = success(k, n)
        css = "fig-bar" if k == best else "fig-bar-plain"
        out.append(f'<rect class="{css}" x="{bx0 + step * k}" y="{f(base - scale * p)}" width="24" height="{f(scale * p)}"/>')
        out.append(f'<text class="fig-label" x="{bx0 + step * k + 12}" y="{f(base - scale * p - 6)}" text-anchor="middle">{label_probability(p)}</text>')
        out.append(f'<text class="fig-label" x="{bx0 + step * k + 12}" y="{base + 18}" text-anchor="middle">{k}</text>')
    out.append(f'<text class="fig-label fig-soft" x="{bx0 + step * K_BARS / 2}" y="{base + 38}" text-anchor="middle">iterations k</text>')
    desc = ("Left: a half circle with the unmarked direction horizontal and the marked direction vertical. The start "
            "state is 20.7 degrees above horizontal. Each iteration adds 41.4 degrees: 62.1, 103.5, then 144.9 degrees. "
            "The state after two iterations is closest to vertical. Right: success probabilities 0.13, 0.78, 0.95, "
            "0.33, 0.01, 0.55 and 0.9998 for zero to six iterations, rising, falling and rising again.")
    return svg("rotation", width, height, "Grover iterations as a rotation, and the overshoot", desc, "\n".join(out))


if __name__ == "__main__":
    for title, amps in small_panels():
        print(f"{title:22s}", [round(a, 3) for a in amps], "mean", round(sum(amps) / len(amps), 3))
    print(f"N=8: theta = {math.degrees(theta(N_PLANE)):.2f} deg, stop at k = {stopping_count(N_PLANE)}")
    for k in range(K_BARS):
        print(f"  k={k}: angle {math.degrees(angle(k, N_PLANE)):6.1f} deg   p = {success(k, N_PLANE):.4f}")
    if "--write" in sys.argv:
        n = write("12-grover-search.html", {"amplitudes": figure_amplitudes(), "rotation": figure_rotation()})
        print(f"wrote {n} figures")
