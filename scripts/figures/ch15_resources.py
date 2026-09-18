#!/usr/bin/env python3
"""Chapter 15 figure.

FIGURE RECORD
  resources  Equally likely messages. For each scenario: what travels, what was shared
             beforehand, what the decoder holds, the Holevo quantity chi of the ensemble the
             decoder holds (bits), and the mutual information achieved by a named measurement.
               1. |0> or |1>, one qubit, nothing shared: chi = 1, Z measurement gives 1.
               2. |0> or |+>, one qubit, nothing shared: chi = h2((1 + 1/sqrt2)/2),
                  Z measurement gives h2(1/4) - 1/2.
               3. I/2 for either message: chi = 0, every measurement 0.
               4. Dense coding, the transmitted qubit alone (four messages): chi = 0.
               5. Dense coding, Bob holding both qubits: chi = 2, Bell measurement gives 2.
             chi = S(average) - average of S(signal), entropies from eigenvalues.

Run without arguments to print the numbers; --write regenerates the SVG.
scripts/check_calculations.py (test_15) recomputes chi from density matrices and the achieved
values from joint outcome distributions.
"""
import math
import sys

from figlib import f, svg, write


def h2(p):
    return 0.0 if p in (0, 1) else -p * math.log2(p) - (1 - p) * math.log2(1 - p)


SCENARIOS = [
    ("|0⟩ or |1⟩", "sends 1 qubit · shares nothing", 1.0, 1.0, "Z"),
    ("|0⟩ or |+⟩", "sends 1 qubit · shares nothing", h2((1 + 1 / math.sqrt(2)) / 2), h2(.25) - .5, "Z"),
    ("I/2 for every message", "sends 1 qubit · shares nothing", 0.0, 0.0, "any"),
    ("dense coding, sent qubit alone", "sends 1 qubit · decoder lacks the ebit", 0.0, 0.0, "any"),
    ("dense coding, Bob holds both", "sends 1 qubit · shares 1 ebit beforehand", 2.0, 2.0, "Bell"),
]


def figure():
    width, left, scale = 360, 24, 125
    out = [f'<text class="fig-label fig-soft" x="{left}" y="16">bits:</text>']
    axis_x = lambda v: left + 40 + scale * v
    for v, t in ((0, "0"), (1, "1"), (2, "2")):
        out.append(f'<text class="fig-label fig-soft" x="{f(axis_x(v))}" y="16" text-anchor="middle">{t}</text>')
    for i, (name, resources, chi, achieved, meas) in enumerate(SCENARIOS):
        y0 = 26 + 86 * i
        out.append(f'<line class="fig-rule" x1="0" y1="{y0}" x2="{width}" y2="{y0}"/>')
        out.append(f'<text class="fig-label fig-strong fig-math" x="0" y="{y0 + 19}">{name}</text>')
        out.append(f'<text class="fig-label fig-soft" x="0" y="{y0 + 37}">{resources}</text>')
        for v in (0, 1, 2):
            out.append(f'<line class="fig-rule" x1="{f(axis_x(v))}" y1="{y0 + 44}" x2="{f(axis_x(v))}" y2="{y0 + 80}"/>')
        out.append(f'<text class="fig-label fig-soft" x="0" y="{y0 + 58}">χ</text>')
        out.append(f'<text class="fig-label fig-soft" x="0" y="{y0 + 76}">{meas}</text>')
        if chi > 1e-9:
            out.append(f'<rect class="fig-bar-outline" x="{f(axis_x(0))}" y="{y0 + 46}" width="{f(scale * chi)}" height="14"/>')
        out.append(f'<text class="fig-label" x="{f(axis_x(chi) + 6)}" y="{y0 + 58}">{chi:.3g}</text>')
        if achieved > 1e-9:
            out.append(f'<rect class="fig-bar" x="{f(axis_x(0))}" y="{y0 + 64}" width="{f(scale * achieved)}" height="14"/>')
        out.append(f'<text class="fig-label" x="{f(axis_x(achieved) + 6)}" y="{y0 + 76}">{achieved:.3g}</text>')
    end = 26 + 86 * len(SCENARIOS)
    out.append(f'<line class="fig-rule" x1="0" y1="{end}" x2="{width}" y2="{end}"/>')
    desc = ("Five rows. Zero or one on one qubit: chi one, Z measurement one bit. Zero or plus: chi 0.601, Z measurement 0.311. "
            "Maximally mixed for every message: zero and zero. Dense coding with only the sent qubit: zero. Dense coding with Bob "
            "holding both qubits after one ebit was shared beforehand: chi two, Bell measurement two.")
    return svg("resources", width, end + 6, "Bits recoverable, with the resources used", desc, "\n".join(out))


if __name__ == "__main__":
    for s in SCENARIOS:
        print(f"{s[0]:32s} chi = {s[2]:.4f}  achieved = {s[3]:.4f} ({s[4]})")
    if "--write" in sys.argv:
        print("wrote", write("15-entropy-holevo.html", {"resources": figure()}), "figure")
