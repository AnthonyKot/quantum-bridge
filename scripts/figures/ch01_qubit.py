#!/usr/bin/env python3
"""Chapter 1 figures.

FIGURE RECORD
  sources   Outcome probabilities for three preparations under two measurements.
            Rows: |+>, |->, and an equal classical mixture of |0> and |1>.
            Columns: the {|0>,|1>} measurement and the {|+>,|->} measurement.
            Probabilities are computed from amplitudes (pure states) and by
            averaging the two branches (mixture). No units.
  bloch     Bloch vectors r = (<X>, <Y>, <Z>) in an orthographic projection
            (azimuth 25 degrees, elevation 18 degrees, x axis towards the viewer).
            Plotted: |0>, |1>, |+>, |->, |+i>, and the worked state
            (sqrt3 |0> + i |1>)/2 with r = (0, sqrt3/2, 1/2).

Run without arguments to print the numbers; --write regenerates the SVG.
The numbers are checked independently, through Pauli expectation values, in
scripts/check_calculations.py (test_01).
"""
import math
import sys

from figlib import f, svg, write

S = 1 / math.sqrt(2)
KET0, KET1 = (1, 0), (0, 1)
PLUS, MINUS = (S, S), (S, -S)
PLUS_I = (S, 1j * S)
WORKED = (math.sqrt(3) / 2, 0.5j)


def overlap_probability(basis_state, state):
    amp = sum(b.conjugate() * a for b, a in zip(map(complex, basis_state), map(complex, state)))
    return abs(amp) ** 2


def probabilities(preparation, basis):
    """preparation: list of (weight, state). A pure state is a one-item list."""
    return [sum(w * overlap_probability(b, s) for w, s in preparation) for b in basis]


def source_table():
    sources = [("Source A", "state |+⟩", [(1, PLUS)]),
               ("Source B", "state |−⟩", [(1, MINUS)]),
               ("Source C", "coin flip: |0⟩ or |1⟩", [(.5, KET0), (.5, KET1)])]
    return [(name, note, probabilities(prep, (KET0, KET1)), probabilities(prep, (PLUS, MINUS)))
            for name, note, prep in sources]


def bloch(state):
    a, b = map(complex, state)
    c = a.conjugate() * b
    return (2 * c.real, 2 * c.imag, abs(a) ** 2 - abs(b) ** 2)


def fraction_label(p):
    for value, label in ((0, "0"), (.25, "¼"), (.5, "½"), (.75, "¾"), (1, "1")):
        if abs(p - value) < 1e-9:
            return label
    return f"{p:.2f}"


def figure_sources():
    rows = source_table()
    width, height = 680, 306
    columns = [(190, "Detector reads 0 or 1", ("0", "1"), "fig-bar-plain"),
               (440, "Detector reads + or −", ("+", "−"), "fig-bar")]
    full = 150
    out = []
    for x0, heading, _, _ in columns:
        out.append(f'<text class="fig-head" x="{x0}" y="22">{heading}</text>')
    for i, (name, note, pz, px) in enumerate(rows):
        top = 40 + 88 * i
        out.append(f'<line class="fig-rule" x1="0" y1="{top}" x2="{width}" y2="{top}"/>')
        out.append(f'<text class="fig-label fig-strong" x="4" y="{top + 36}">{name}</text>')
        out.append(f'<text class="fig-label fig-soft fig-math" x="4" y="{top + 56}">{note}</text>')
        for (x0, _, outcomes, css), probs in zip(columns, (pz, px)):
            for j, (symbol, p) in enumerate(zip(outcomes, probs)):
                y = top + 16 + 32 * j
                out.append(f'<text class="fig-label" x="{x0 + 8}" y="{y + 16}" text-anchor="middle">{symbol}</text>')
                out.append(f'<line class="fig-axis" x1="{x0 + 24}" y1="{y - 2}" x2="{x0 + 24}" y2="{y + 24}"/>')
                if p > 1e-9:
                    out.append(f'<rect class="{css}" x="{x0 + 24}" y="{y}" width="{f(full * p)}" height="22"/>')
                out.append(f'<text class="fig-label" x="{f(x0 + 32 + full * p)}" y="{y + 16}">{fraction_label(p)}</text>')
    bottom = 40 + 88 * len(rows)
    out.append(f'<line class="fig-rule" x1="0" y1="{bottom}" x2="{width}" y2="{bottom}"/>')
    desc = ("A grid of outcome probabilities. With the detector that reads 0 or 1, sources A, B and C all give "
            "one half and one half. With the detector that reads plus or minus, source A gives plus with "
            "probability one, source B gives minus with probability one, and source C gives one half and one half.")
    return svg("sources", width, height, "Three sources under two measurements", desc, "\n".join(out))


AZ, EL = math.radians(25), math.radians(18)
RIGHT = (-math.sin(AZ), math.cos(AZ), 0)
UP = (-math.sin(EL) * math.cos(AZ), -math.sin(EL) * math.sin(AZ), math.cos(EL))
TOWARDS = (math.cos(EL) * math.cos(AZ), math.cos(EL) * math.sin(AZ), math.sin(EL))


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def figure_bloch():
    width, height, cx, cy, radius = 680, 400, 330, 200, 150

    def project(r):
        return cx + radius * dot(RIGHT, r), cy - radius * dot(UP, r)

    def path(points, css):
        d = " ".join(("M" if k == 0 else "L") + f"{f(x)},{f(y)}" for k, (x, y) in enumerate(points))
        return f'<path class="{css}" d="{d}"/>'

    out = [f'<circle class="fig-outline" cx="{cx}" cy="{cy}" r="{radius}"/>']
    equator = [(math.cos(t), math.sin(t), 0) for t in (2 * math.pi * k / 180 for k in range(181))]
    front, back, current, is_front = [], [], [], None
    for r in equator:
        side = dot(TOWARDS, r) >= 0
        if side != is_front and current:
            (front if is_front else back).append(current + [r])
            current = []
        is_front = side
        current.append(r)
    (front if is_front else back).append(current)
    out += [path([project(r) for r in seg], "fig-line fig-dashed") for seg in back]
    out += [path([project(r) for r in seg], "fig-line") for seg in front]

    for axis, label, shift in (((1, 0, 0), "x", (-12, 14)), ((0, 1, 0), "y", (8, -8)), ((0, 0, 1), "z", (-4, -10))):
        (x1, y1), (x2, y2) = project(tuple(-1.0 * a for a in axis)), project(tuple(1.22 * a for a in axis))
        out.append(f'<line class="fig-axis" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}"/>')
        out.append(f'<text class="fig-label fig-soft fig-italic" x="{f(x2 + shift[0])}" y="{f(y2 + shift[1])}" text-anchor="middle">{label}</text>')

    rw = bloch(WORKED)
    px, py = project(rw)
    foot = project((0, 0, rw[2]))
    out.append(f'<line class="fig-line fig-dashed" x1="{f(px)}" y1="{f(py)}" x2="{f(foot[0])}" y2="{f(foot[1])}"/>')
    out.append(f'<line class="fig-vector" x1="{cx}" y1="{cy}" x2="{f(px)}" y2="{f(py)}"/>')
    out.append(f'<text class="fig-label fig-soft" x="{f(foot[0] - 8)}" y="{f(foot[1] - 3)}" text-anchor="end"><tspan class="fig-italic">r</tspan><tspan dy="4" font-size="11">z</tspan><tspan dy="-4"> = ½</tspan></text>')

    points = [(bloch(KET0), "|0⟩", (12, -6), "start"), (bloch(KET1), "|1⟩", (12, 16), "start"),
              (bloch(PLUS), "|+⟩  (source A)", (-12, -8), "end"),
              (bloch(MINUS), "|−⟩  (source B)", (-12, -8), "end"),
              (bloch(PLUS_I), "|+i⟩", (12, 16), "start"),
              (rw, "(√3|0⟩ + i|1⟩)/2", (12, -8), "start")]
    for r, label, (dx, dy), anchor in points:
        x, y = project(r)
        # The lower pole is just behind the limb at this elevation; keep it solid so the two poles match.
        css = "fig-dot" if dot(TOWARDS, r) >= -0.32 else "fig-dot fig-dot-back"
        if r is rw:
            css = "fig-dot fig-dot-accent"
        out.append(f'<circle class="{css}" cx="{f(x)}" cy="{f(y)}" r="5"/>')
        out.append(f'<text class="fig-label fig-math" x="{f(x + dx)}" y="{f(y + dy)}" text-anchor="{anchor}">{label}</text>')
    out.append(f'<circle class="fig-dot fig-dot-back" cx="{cx}" cy="{cy}" r="4"/>')
    out.append(f'<text class="fig-label fig-soft" x="{cx - 10}" y="{cy - 6}" text-anchor="end">source C</text>')
    desc = ("A sphere with the z axis vertical. The state zero is at the top and one at the bottom. Plus and minus "
            "are at opposite ends of the x axis, on the equator, and plus i is on the y axis. The worked state is "
            "on the front of the sphere, above the y axis, at height one half. Source C is at the centre.")
    return svg("bloch", width, height, "States on the Bloch sphere", desc, "\n".join(out))


if __name__ == "__main__":
    for name, note, pz, px in source_table():
        print(f"{name:9s} p(0),p(1) = {pz[0]:.3f}, {pz[1]:.3f}   p(+),p(-) = {px[0]:.3f}, {px[1]:.3f}")
    print("worked state r =", tuple(round(v, 4) for v in bloch(WORKED)))
    if "--write" in sys.argv:
        n = write("01-superposition-qubit.html", {"sources": figure_sources(), "bloch": figure_bloch()})
        print(f"wrote {n} figures")
