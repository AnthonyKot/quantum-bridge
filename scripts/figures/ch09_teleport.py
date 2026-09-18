#!/usr/bin/env python3
"""Chapter 9 figure.

FIGURE RECORD
  teleport  Three registers in the chapter's order Q, A, B (Q first, the unknown input;
            A and B share |Phi+>). Alice holds Q and A, Bob holds B.
            STEPS is the drawn circuit, in time order; the test executes it:
              CNOT Q -> A, H on Q, measure Q (bit a), measure A (bit b),
              send a and b to Bob, then X^b on B, then Z^a on B.
            Bob's state is annotated at three times: before the bits arrive
            (I/2 on average), after measurement (X^b Z^a |psi>), after correction (|psi>).

--write regenerates the SVG. scripts/check_calculations.py (test_09) runs STEPS with
8x8 matrices on several inputs and checks every branch.
"""
import sys

from figlib import svg, write

REGISTERS = ["Q", "A", "B"]
OWNER = {"Q": "Alice", "A": "Alice", "B": "Bob"}
STEPS = [
    ("cnot", "Q", "A"),
    ("h", "Q"),
    ("measure", "Q", "a"),
    ("measure", "A", "b"),
    ("x_if", "B", "b"),
    ("z_if", "B", "a"),
]


def figure():
    width = 360
    ys = {"Q": 64, "A": 124, "B": 214}
    out = [f'<rect class="fig-zone" x="0" y="34" width="{width}" height="118" rx="6"/>',
           f'<rect class="fig-zone fig-zone-alt" x="0" y="176" width="{width}" height="96" rx="6"/>',
           f'<text class="fig-label fig-strong" x="8" y="{34 + 16}">Alice</text>',
           f'<text class="fig-label fig-strong" x="8" y="{176 + 16}">Bob</text>',
           f'<text class="fig-label fig-soft" x="0" y="18">time →</text>']
    starts = {"Q": "|ψ⟩", "A": "", "B": ""}
    for reg, y in ys.items():
        out.append(f'<text class="fig-label fig-strong" x="10" y="{y + 5}">{reg}</text>')
        if starts[reg]:
            out.append(f'<text class="fig-label fig-math" x="30" y="{y + 5}">{starts[reg]}</text>')
    # Shared Bell pair on A and B.
    out.append(f'<path class="fig-bell" d="M44,{ys["A"]} C28,{ys["A"] + 30} 28,{ys["B"] - 30} 44,{ys["B"]}"/>')
    out.append(f'<text class="fig-label fig-soft fig-math" x="46" y="{(ys["A"] + ys["B"]) / 2 + 5}">Φ⁺ shared</text>')
    x_measure = 196
    for reg in ("Q", "A"):
        out.append(f'<line class="fig-wire" x1="48" y1="{ys[reg]}" x2="{x_measure}" y2="{ys[reg]}"/>')
    out.append(f'<line class="fig-wire" x1="48" y1="{ys["B"]}" x2="{width - 44}" y2="{ys["B"]}"/>')
    x = {"cnot": 88, "h": 136}
    for step in STEPS:
        kind = step[0]
        if kind == "cnot":
            c, t = ys[step[1]], ys[step[2]]
            out.append(f'<line class="fig-wire" x1="{x[kind]}" y1="{c}" x2="{x[kind]}" y2="{t + 11}"/>')
            out.append(f'<circle class="fig-control" cx="{x[kind]}" cy="{c}" r="5"/>')
            out.append(f'<circle class="fig-target" cx="{x[kind]}" cy="{t}" r="11"/>')
            out.append(f'<line class="fig-wire" x1="{x[kind] - 11}" y1="{t}" x2="{x[kind] + 11}" y2="{t}"/>')
        elif kind == "h":
            y = ys[step[1]]
            out.append(f'<rect class="fig-gate" x="{x[kind] - 14}" y="{y - 14}" width="28" height="28" rx="3"/>')
            out.append(f'<text class="fig-label fig-strong" x="{x[kind]}" y="{y + 5}" text-anchor="middle">H</text>')
        elif kind == "measure":
            y, bit = ys[step[1]], step[2]
            out.append(f'<rect class="fig-gate" x="{x_measure - 16}" y="{y - 14}" width="32" height="28" rx="3"/>')
            out.append(f'<path class="fig-line" d="M{x_measure - 10},{y + 7} A11,11 0 0 1 {x_measure + 10},{y + 7}"/>')
            out.append(f'<line class="fig-line" x1="{x_measure}" y1="{y + 7}" x2="{x_measure + 8}" y2="{y - 7}"/>')
            xb = 244 if bit == "b" else 292
            out.append(f'<line class="fig-classical" x1="{x_measure + 16}" y1="{y - 2}" x2="{xb + 1.5}" y2="{y - 2}"/>')
            out.append(f'<line class="fig-classical" x1="{x_measure + 16}" y1="{y + 2}" x2="{xb - 1.5}" y2="{y + 2}"/>')
            out.append(f'<line class="fig-classical" x1="{xb - 1.5}" y1="{y + 2}" x2="{xb - 1.5}" y2="{ys["B"] - 14}"/>')
            out.append(f'<line class="fig-classical" x1="{xb + 1.5}" y1="{y - 2}" x2="{xb + 1.5}" y2="{ys["B"] - 14}"/>')
            out.append(f'<text class="fig-label fig-strong" x="{x_measure + 24}" y="{y - 8}">{bit}</text>')
        elif kind in ("x_if", "z_if"):
            xg, g, bit = (244, "X", "b") if kind == "x_if" else (292, "Z", "a")
            y = ys["B"]
            out.append(f'<rect class="fig-gate" x="{xg - 16}" y="{y - 14}" width="32" height="28" rx="3"/>')
            out.append(f'<text class="fig-label fig-strong" x="{xg}" y="{y + 5}" text-anchor="middle">{g}<tspan dy="-6" font-size="12">{bit}</tspan></text>')
    out.append(f'<text class="fig-label fig-math" x="{width - 38}" y="{ys["B"] + 5}">|ψ⟩</text>')
    out.append(f'<text class="fig-label fig-soft" x="{width}" y="18" text-anchor="end">double lines: classical bits</text>')
    notes = [(52, 30, "start", "unconditioned, until the bits arrive: I/2"),
             (52, 50, "start", "conditioned on Alice’s outcome (a, b): XᵇZᵃ|ψ⟩"),
             (width - 4, 30, "end", "")]
    for xn, dy, anchor, text in notes:
        if text:
            out.append(f'<text class="fig-label fig-soft fig-math" x="{xn}" y="{ys["B"] + dy}" text-anchor="{anchor}">{text}</text>')
    desc = ("A circuit with three wires. Alice holds Q, which carries the unknown state psi, and A; Bob holds B. A and B start as a "
            "shared Bell pair. Alice applies a controlled-NOT from Q to A, then H to Q, then measures Q to get bit a and A to get "
            "bit b. Double lines carry the two bits to Bob, who applies X if b is one and then Z if a is one. Bob's wire ends in "
            "psi. Bob's unconditioned state is I over 2 until the bits arrive; conditioned on Alice's outcome a, b it is X to the b, Z to the a, psi.")
    return svg("teleport", width, ys["B"] + 60, "Teleportation, register by register", desc, "\n".join(out))


if __name__ == "__main__":
    for s in STEPS:
        print(s)
    if "--write" in sys.argv:
        print("wrote", write("09-teleportation-superdense.html", {"teleport": figure()}), "figure")
