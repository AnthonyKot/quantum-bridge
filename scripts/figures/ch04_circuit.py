#!/usr/bin/env python3
"""Chapter 4 figure.

FIGURE RECORD
  circuit   Two qubits, input |00>. Qubit 1 is the top wire and the FIRST symbol of
            each basis label; basis order 00, 01, 10, 11 (leftmost register first).
            Circuit: H on qubit 1, then CNOT with qubit 1 as control and qubit 2 as
            target. As a matrix product the output is CNOT (H x I) |00>.
            Rows of amplitude bars (real amplitudes, so signs are shown):
              after the input, after H, after CNOT;
              and, for comparison, the other gate order (CNOT first, then H).
            Amplitudes are computed by applying the gates' basis rules:
            H|0> = (|0>+|1>)/sqrt2, H|1> = (|0>-|1>)/sqrt2 on qubit 1;
            CNOT |a,b> = |a, b xor a>.

Run without arguments to print the numbers; --write regenerates the SVG.
scripts/check_calculations.py (test_04) checks the rows with 4x4 matrices.
"""
import math
import sys

from figlib import f, svg, write

S = 1 / math.sqrt(2)
LABELS = ["00", "01", "10", "11"]


def h_on_first(state):
    """Apply H to qubit 1 by the basis rule, term by term."""
    out = {k: 0.0 for k in LABELS}
    for label, amp in state.items():
        a, b = label
        if a == "0":
            out["0" + b] += S * amp
            out["1" + b] += S * amp
        else:
            out["0" + b] += S * amp
            out["1" + b] -= S * amp
    return out


def cnot(state):
    out = {k: 0.0 for k in LABELS}
    for label, amp in state.items():
        a, b = int(label[0]), int(label[1])
        out[f"{a}{b ^ a}"] += amp
    return out


START = {"00": 1.0, "01": 0.0, "10": 0.0, "11": 0.0}


def rows():
    after_h = h_on_first(START)
    return [("Input |00⟩", START), ("After H on qubit 1", after_h), ("After CNOT", cnot(after_h)),
            ("Other order: CNOT, then H", h_on_first(cnot(START)))]


def label(a):
    for v, t in ((0, "0"), (1, "1"), (S, "1/√2"), (-S, "−1/√2")):
        if abs(a - v) < 1e-9:
            return t
    return f"{a:.2f}"


def figure():
    width = 360
    out = []
    # Circuit diagram.
    y1, y2 = 34, 84
    out.append(f'<text class="fig-label fig-soft" x="0" y="{y1 + 5}">qubit 1</text>')
    out.append(f'<text class="fig-label fig-soft" x="0" y="{y2 + 5}">qubit 2</text>')
    out.append(f'<text class="fig-label fig-math" x="64" y="{y1 + 5}">|0⟩</text>')
    out.append(f'<text class="fig-label fig-math" x="64" y="{y2 + 5}">|0⟩</text>')
    for y in (y1, y2):
        out.append(f'<line class="fig-wire" x1="92" y1="{y}" x2="{width - 8}" y2="{y}"/>')
    out.append(f'<rect class="fig-gate" x="138" y="{y1 - 16}" width="32" height="32" rx="3"/>')
    out.append(f'<text class="fig-label fig-strong" x="154" y="{y1 + 5}" text-anchor="middle">H</text>')
    cx = 236
    out.append(f'<line class="fig-wire" x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2 + 12}"/>')
    out.append(f'<circle class="fig-control" cx="{cx}" cy="{y1}" r="5"/>')
    out.append(f'<circle class="fig-target" cx="{cx}" cy="{y2}" r="12"/>')
    out.append(f'<line class="fig-wire" x1="{cx - 12}" y1="{y2}" x2="{cx + 12}" y2="{y2}"/>')
    for x, n in ((116, "①"), (196, "②"), (292, "③")):
        out.append(f'<line class="fig-line fig-dashed" x1="{x}" y1="{y1 - 22}" x2="{x}" y2="{y2 + 20}"/>')
        out.append(f'<text class="fig-label fig-soft" x="{x}" y="{y2 + 36}" text-anchor="middle">{n}</text>')
    # Amplitude rows.
    top, unit = y2 + 56, 36
    marks = ("①", "②", "③", "")
    for i, (title, state) in enumerate(rows()):
        y0 = top + 104 * i
        out.append(f'<line class="fig-rule" x1="0" y1="{y0}" x2="{width}" y2="{y0}"/>')
        out.append(f'<text class="fig-label fig-strong fig-math" x="0" y="{y0 + 20}">{(marks[i] + "  ") if marks[i] else ""}{title}</text>')
        base = y0 + 64
        out.append(f'<line class="fig-axis" x1="60" y1="{base}" x2="{width - 10}" y2="{base}"/>')
        for j, k in enumerate(LABELS):
            a = state[k]
            x = 76 + 72 * j
            if abs(a) > 1e-9:
                top_y, h = (base - unit * a, unit * a) if a > 0 else (base, -unit * a)
                css = "fig-bar-plain" if i == 3 else "fig-bar"
                out.append(f'<rect class="{css}" x="{x}" y="{f(top_y)}" width="34" height="{f(h)}"/>')
                out.append(f'<text class="fig-label" x="{x + 40}" y="{f(base - unit * a / 2 + 4)}">{label(a)}</text>')
            out.append(f'<text class="fig-label fig-math" x="{x + 17}" y="{base + 20}" text-anchor="middle">|{k}⟩</text>')
    end = top + 104 * 4
    out.append(f'<line class="fig-rule" x1="0" y1="{end}" x2="{width}" y2="{end}"/>')
    desc = ("A circuit with two wires, qubit 1 on top. A Hadamard gate on qubit 1 is followed by a controlled-NOT with qubit 1 "
            "as control and qubit 2 as target. Below, amplitude bars over the basis 00, 01, 10, 11. At the input only 00 has "
            "amplitude one. After H, 00 and 10 each have one over root two. After CNOT, 00 and 11 each have one over root two. "
            "In the other gate order, CNOT first then H, the result is 00 and 10 with one over root two each, a product state.")
    return svg("circuit", width, end + 6, "A two-gate circuit, amplitude by amplitude", desc, "\n".join(out))


if __name__ == "__main__":
    for title, state in rows():
        print(f"{title:28s}", {k: round(v, 4) for k, v in state.items()}, "norm", round(sum(v * v for v in state.values()), 6))
    if "--write" in sys.argv:
        print("wrote", write("04-unitary-gates.html", {"circuit": figure()}), "figure")
