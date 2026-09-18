#!/usr/bin/env python3
"""Chapter 11 figure.

FIGURE RECORD
  peaks  Probability of each Fourier outcome k (no units).
         Top: exact period. N = 16, r = 4, conditional coset state after measuring the
         output register; outcomes k = 0, 4, 8, 12 with probability 1/4 each.
         Bottom: the chapter's order-finding example, U = multiplication by 2 mod 21,
         order r = 6, control register N = 64 (the chapter's worked samples use
         N = 1024; 64 keeps the bars visible). Starting target |1>, so the phases s/6,
         s = 0..5, are sampled with equal weight:
           p(k) = (1/6) sum_s sin^2(pi N d) / (N^2 sin^2(pi d)),  d = s/6 - k/N,
         taking the limit, p = 1, where d = 0.

Run without arguments to print the numbers; --write regenerates the SVG.
scripts/check_calculations.py (test_11) recomputes both panels by simulating the
two-register circuit directly, without eigenstates.
"""
import math
import sys

from figlib import f, svg, write

EXACT_N, EXACT_R = 16, 4
ORDER_N, ORDER_R, MOD, BASE = 64, 6, 21, 2


def exact_distribution():
    return [1 / EXACT_R if k % (EXACT_N // EXACT_R) == 0 else 0.0 for k in range(EXACT_N)]


def phase_probability(phi, k, n):
    d = phi - k / n
    if abs(math.sin(math.pi * d)) < 1e-12:
        return 1.0
    return math.sin(math.pi * n * d) ** 2 / (n * n * math.sin(math.pi * d) ** 2)


def order_distribution():
    return [sum(phase_probability(s / ORDER_R, k, ORDER_N) for s in range(ORDER_R)) / ORDER_R for k in range(ORDER_N)]


def figure():
    width, left, pw = 360, 34, 316
    out = []

    def plot(top, height, probs, title, ymax, peaks, ticks):
        n = len(probs)
        base = top + height
        out.append(f'<text class="fig-head" x="0" y="{top - 14}">{title}</text>')
        for level in (0, ymax / 2, ymax):
            y = base - height * level / ymax
            out.append(f'<line class="fig-rule" x1="{left}" y1="{f(y)}" x2="{left + pw}" y2="{f(y)}"/>')
            out.append(f'<text class="fig-label fig-soft" x="{left - 6}" y="{f(y + 4)}" text-anchor="end">{level:.3g}</text>')
        step = pw / n
        for k, p in enumerate(probs):
            if p > 1e-6:
                css = "fig-bar" if k in peaks else "fig-bar-plain"
                out.append(f'<rect class="{css}" x="{f(left + k * step + step * .15)}" y="{f(base - height * p / ymax)}" '
                           f'width="{f(step * .7)}" height="{f(height * p / ymax)}"/>')
        for k in ticks:
            x = left + (k + .5) * step
            out.append(f'<text class="fig-label fig-soft" x="{f(x)}" y="{base + 16}" text-anchor="middle">{k}</text>')
        return base

    exact = exact_distribution()
    base = plot(34, 110, exact, "Exact period: N = 16, r = 4", .25, {0, 4, 8, 12}, [0, 4, 8, 12, 15])
    order = order_distribution()
    near = {round(s * ORDER_N / ORDER_R) for s in range(ORDER_R)}
    base2 = plot(base + 70, 150, order, "Order of 2 mod 21 (r = 6), N = 64", .18, near, [0, 11, 21, 32, 43, 53, 63])
    for s in range(1, ORDER_R):
        x = left + (s * ORDER_N / ORDER_R + .5) * pw / ORDER_N
        out.append(f'<line class="fig-line fig-dashed" x1="{f(x)}" y1="{f(base + 80)}" x2="{f(x)}" y2="{f(base2)}"/>')
    out.append(f'<text class="fig-label fig-soft" x="{left + pw}" y="{f(base2 + 36)}" text-anchor="end">outcome k; dashed lines at k = 64s/6</text>')
    desc = ("Two bar charts of outcome probability. Top: for N 16 and period 4, four bars of height one quarter at k 0, 4, 8 "
            "and 12 and nothing elsewhere. Bottom: for the order of 2 modulo 21 with N 64, a tall bar at 0 and at 32, and "
            "clusters of two or three bars around 10.7, 21.3, 42.7 and 53.3, where 64 s over 6 is not an integer, with small "
            "bars spread between the clusters.")
    return svg("peaks", width, base2 + 44, "Fourier outcomes: exact and spread peaks", desc, "\n".join(out))


if __name__ == "__main__":
    ex = exact_distribution()
    print("exact: nonzero at", [k for k, p in enumerate(ex) if p > 0], "sum", sum(ex))
    od = order_distribution()
    print("order: sum", round(sum(od), 6), "max", round(max(od), 4))
    for k in (0, 10, 11, 21, 22, 32, 42, 43, 53, 54):
        print(f"  k={k:2d} p={od[k]:.4f}")
    if "--write" in sys.argv:
        print("wrote", write("11-qft-translations.html", {"peaks": figure()}), "figure")
