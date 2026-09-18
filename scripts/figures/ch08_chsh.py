#!/usr/bin/env python3
"""Chapter 8 figure.

FIGURE RECORD
  chsh   Observables sigma(t) = cos t Z + sin t X, a direction at angle t from z in the
         x-z plane of the Bloch sphere. State |Phi+> = (|00> + |11>)/sqrt2, for which
         <sigma(a) x sigma(b)> = cos(a - b).
         Family: A0 at 0, A1 at 2 phi, B0 at phi, B1 at -phi. The chapter's settings are
         phi = pi/4: A0 = Z, A1 = X, B0 = (Z+X)/sqrt2, B1 = (Z-X)/sqrt2.
         Top: the four directions at phi = pi/4.
         Bottom: S(phi) = E00 + E01 + E10 - E11 = 3 cos(phi) - cos(3 phi), phi from 0 to 90
         degrees, with the local bound S = 2 and the quantum maximum 2 sqrt2.

Run without arguments to print the numbers; --write regenerates the SVG.
scripts/check_calculations.py (test_08) recomputes S(phi) from 4x4 matrices.
"""
import math
import sys

from figlib import f, svg, write


def settings(phi):
    return {"A0": 0.0, "A1": 2 * phi, "B0": phi, "B1": -phi}


def correlator(a, b):
    return math.cos(a - b)


def s_value(phi):
    t = settings(phi)
    return (correlator(t["A0"], t["B0"]) + correlator(t["A0"], t["B1"]) + correlator(t["A1"], t["B0"])
            - correlator(t["A1"], t["B1"]))


def crossing():
    """Largest phi in (0, pi/2) with S = 2: cos phi = (sqrt3 - 1)/2."""
    return math.acos((math.sqrt(3) - 1) / 2)


def figure():
    width = 360
    out = [f'<text class="fig-head" x="0" y="16">Measurement directions (x–z plane)</text>']
    cx, cy, r = 180, 132, 88
    out.append(f'<circle class="fig-outline" cx="{cx}" cy="{cy}" r="{r}"/>')
    names = {"A0": ("A₀ = Z", "fig-vector"), "A1": ("A₁ = X", "fig-vector"),
             "B0": ("B₀ = (Z+X)/√2", "fig-vector fig-vector-alt"), "B1": ("B₁ = (Z−X)/√2", "fig-vector fig-vector-alt")}
    for key, t in settings(math.pi / 4).items():
        x, y = cx + r * math.sin(t), cy - r * math.cos(t)
        text, css = names[key]
        out.append(f'<line class="{css}" x1="{cx}" y1="{cy}" x2="{f(x)}" y2="{f(y)}"/>')
        lx, ly = cx + (r + 14) * math.sin(t), cy - (r + 14) * math.cos(t)
        anchor = "start" if math.sin(t) > .2 else ("end" if math.sin(t) < -.2 else "middle")
        cls = "fig-label fig-math" + (" fig-alt-text" if key[0] == "B" else " fig-accent-text")
        out.append(f'<text class="{cls}" x="{f(lx)}" y="{f(ly + 5)}" text-anchor="{anchor}">{text}</text>')

    top, left, pw, ph = 290, 44, 290, 170
    smax = 2 * math.sqrt(2)
    base = top + ph
    out.append(f'<text class="fig-head" x="0" y="{top - 16}">S with A₀ at 0, B₀ at φ, A₁ at 2φ, B₁ at −φ</text>')

    def y_of(s):
        return base - ph * s / 3.0

    out.append(f'<rect class="fig-band" x="{left}" y="{f(y_of(2))}" width="{pw}" height="{f(y_of(0) - y_of(2))}"/>')
    for s, text in ((0, "0"), (1, "1"), (2, "2"), (smax, "2√2")):
        out.append(f'<line class="fig-rule" x1="{left}" y1="{f(y_of(s))}" x2="{left + pw}" y2="{f(y_of(s))}"/>')
        out.append(f'<text class="fig-label fig-soft" x="{left - 8}" y="{f(y_of(s) + 4)}" text-anchor="end">{text}</text>')
    for deg in (0, 45, 90):
        x = left + pw * deg / 90
        out.append(f'<text class="fig-label fig-soft" x="{f(x)}" y="{base + 20}" text-anchor="middle">{deg}°</text>')
    out.append(f'<text class="fig-label fig-soft" x="{left + pw}" y="{base + 40}" text-anchor="end">angle φ between A₀ and B₀</text>')
    pts = [(left + pw * k / 180, y_of(s_value(math.radians(90 * k / 180)))) for k in range(181)]
    out.append('<path class="fig-trace" d="' + " ".join(("M" if i == 0 else "L") + f"{f(x)},{f(y)}" for i, (x, y) in enumerate(pts)) + '"/>')
    x45 = left + pw / 2
    out.append(f'<circle class="fig-dot fig-dot-accent" cx="{f(x45)}" cy="{f(y_of(s_value(math.pi / 4)))}" r="5"/>')
    xc = left + pw * math.degrees(crossing()) / 90
    out.append(f'<line class="fig-line fig-dashed" x1="{f(xc)}" y1="{f(y_of(2))}" x2="{f(xc)}" y2="{base}"/>')
    out.append(f'<text class="fig-label fig-soft" x="{left + 8}" y="{f(y_of(1.1))}">local models: |S| ≤ 2</text>')
    out.append(f'<text class="fig-label fig-soft" x="{f(xc + 5)}" y="{f(y_of(.35))}">{math.degrees(crossing()):.1f}°</text>')
    desc = ("Top: a circle with four arrows. A zero points along z, A one along x, B zero halfway between them at 45 degrees, "
            "and B one at minus 45 degrees. Bottom: S against the angle phi from 0 to 90 degrees. S starts at 2, rises to "
            "2 root 2 at 45 degrees, falls back to 2 at about 68.5 degrees and to 0 at 90 degrees. The region up to 2 is "
            "shaded as the limit for local models.")
    return svg("chsh", width, base + 48, "Settings and the CHSH value", desc, "\n".join(out))


if __name__ == "__main__":
    for deg in (0, 22.5, 45, 60, 68.53, 90):
        print(f"phi = {deg:6.2f} deg   S = {s_value(math.radians(deg)):.4f}")
    print(f"crossing at {math.degrees(crossing()):.2f} deg")
    if "--write" in sys.argv:
        print("wrote", write("08-epr-bell.html", {"chsh": figure()}), "figure")
