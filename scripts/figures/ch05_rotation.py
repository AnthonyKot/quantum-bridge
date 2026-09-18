#!/usr/bin/env python3
"""Chapter 5 figure.

FIGURE RECORD
  pulse   Input |0>, Bloch vector (0, 0, 1). Drive in the rotating frame,
          H_eff = hbar (Omega X + Delta Z) / 2, constant for time t.
          The Bloch vector rotates by angle omega t about the axis (Omega, 0, Delta)/omega,
          omega = sqrt(Omega^2 + Delta^2), right-handed (R_n(theta) = exp(-i theta n.sigma/2)).
          Two drives: resonant, Delta = 0; detuned, Delta = Omega.
          Top: both paths on the Bloch sphere (projection as in Chapter 1), with the
          resonant pi/2 and pi pulses marked and the detuned path's lowest point marked.
          Bottom: p(1) = (1 - r_z)/2 against Omega t from 0 to 2 pi.
          Paths come from the rotation formula (Rodrigues); the test recomputes them from
          the 2x2 matrix exponential acting on |0>.

Run without arguments to print the numbers; --write regenerates the SVG.
"""
import math
import sys

from figlib import f, svg, write

AZ, EL = math.radians(25), math.radians(18)
RIGHT = (-math.sin(AZ), math.cos(AZ), 0)
UP = (-math.sin(EL) * math.cos(AZ), -math.sin(EL) * math.sin(AZ), math.cos(EL))
TOWARDS = (math.cos(EL) * math.cos(AZ), math.cos(EL) * math.sin(AZ), math.sin(EL))


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def bloch_after(omega_t, detuning_ratio):
    """Bloch vector of |0> after the drive, with Delta = detuning_ratio * Omega and Omega t = omega_t."""
    w = math.sqrt(1 + detuning_ratio ** 2)
    n = (1 / w, 0, detuning_ratio / w)
    r0 = (0, 0, 1)
    angle = w * omega_t
    par = dot(n, r0)
    c, s = math.cos(angle), math.sin(angle)
    nx = cross(n, r0)
    return tuple(n[i] * par + c * (r0[i] - n[i] * par) + s * nx[i] for i in range(3))


def p1(omega_t, detuning_ratio):
    return (1 - bloch_after(omega_t, detuning_ratio)[2]) / 2


def figure():
    width, cx, cy, radius = 360, 180, 160, 118
    out = []

    def project(r):
        return cx + radius * dot(RIGHT, r), cy - radius * dot(UP, r)

    def path(points, css):
        d = " ".join(("M" if k == 0 else "L") + f"{f(x)},{f(y)}" for k, (x, y) in enumerate(points))
        return f'<path class="{css}" d="{d}"/>'

    out.append(f'<text class="fig-head" x="0" y="18">The Bloch vector during the pulse</text>')
    out.append(f'<circle class="fig-outline" cx="{cx}" cy="{cy}" r="{radius}"/>')
    eq = [(math.cos(t), math.sin(t), 0) for t in (2 * math.pi * k / 120 for k in range(121))]
    out.append(path([project(r) for r in eq if dot(TOWARDS, r) < 0], "fig-line fig-dashed"))
    out.append(path([project(r) for r in eq], "fig-line fig-faint"))
    for axis, label, (dx, dy) in (((1, 0, 0), "x", (-10, 14)), ((0, 1, 0), "y", (10, 4)), ((0, 0, 1), "z", (10, -2))):
        (x1, y1), (x2, y2) = project(tuple(-a for a in axis)), project(tuple(1.18 * a for a in axis))
        out.append(f'<line class="fig-axis" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}"/>')
        out.append(f'<text class="fig-label fig-soft fig-italic" x="{f(x2 + dx)}" y="{f(y2 + dy)}" text-anchor="middle">{label}</text>')
    steps = 90
    res = [project(bloch_after(math.pi * k / steps, 0)) for k in range(steps + 1)]
    det = [project(bloch_after(2 * math.pi / math.sqrt(2) * k / (2 * steps), 1)) for k in range(2 * steps + 1)]
    out.append(path(res, "fig-trace"))
    out.append(path(det, "fig-trace fig-trace-alt"))
    for (x, y), text, dx, dy, anchor, css in (
            (project((0, 0, 1)), "start |0⟩", -10, -6, "end", "fig-dot"),
            (project(bloch_after(math.pi / 2, 0)), "π/2 pulse", -10, -8, "end", "fig-dot fig-dot-accent"),
            (project(bloch_after(math.pi, 0)), "π pulse: |1⟩", 10, 16, "start", "fig-dot fig-dot-accent"),
            (project(bloch_after(math.pi / math.sqrt(2), 1)), "detuned: stops here", 10, 18, "start", "fig-dot fig-dot-alt")):
        out.append(f'<circle class="{css}" cx="{f(x)}" cy="{f(y)}" r="5"/>')
        cls = "fig-label fig-math" if "|" in text or "π" in text else "fig-label"
        out.append(f'<text class="{cls}" x="{f(x + dx)}" y="{f(y + dy)}" text-anchor="{anchor}">{text}</text>')

    # p(1) against Omega t.
    top, left, plot_w, plot_h = 330, 44, 296, 150
    base = top + plot_h
    out.append(f'<text class="fig-head" x="0" y="{top - 16}">Probability of reading 1 after the pulse</text>')
    for level, text in ((0, "0"), (.5, "½"), (1, "1")):
        y = base - plot_h * level
        out.append(f'<line class="fig-rule" x1="{left}" y1="{f(y)}" x2="{left + plot_w}" y2="{f(y)}"/>')
        out.append(f'<text class="fig-label fig-soft" x="{left - 8}" y="{f(y + 4)}" text-anchor="end">{text}</text>')
    for k, text in enumerate(("0", "π/2", "π", "3π/2", "2π")):
        x = left + plot_w * k / 4
        out.append(f'<line class="fig-axis" x1="{f(x)}" y1="{base}" x2="{f(x)}" y2="{base + 5}"/>')
        out.append(f'<text class="fig-label fig-soft fig-math" x="{f(x)}" y="{base + 22}" text-anchor="middle">{text}</text>')
    out.append(f'<text class="fig-label fig-soft" x="{left + plot_w}" y="{base + 42}" text-anchor="end">pulse area Ωt</text>')

    def curve(ratio):
        return [(left + plot_w * k / 200, base - plot_h * p1(2 * math.pi * k / 200, ratio)) for k in range(201)]

    out.append(path(curve(0), "fig-trace"))
    out.append(path(curve(1), "fig-trace fig-trace-alt"))
    for (x, y), css in (((left + plot_w / 4, base - plot_h * p1(math.pi / 2, 0)), "fig-dot fig-dot-accent"),
                        ((left + plot_w / 2, base - plot_h * p1(math.pi, 0)), "fig-dot fig-dot-accent"),
                        ((left + plot_w * (math.pi / math.sqrt(2)) / (2 * math.pi), base - plot_h * p1(math.pi / math.sqrt(2), 1)),
                         "fig-dot fig-dot-alt")):
        out.append(f'<circle class="{css}" cx="{f(x)}" cy="{f(y)}" r="4.5"/>')
    out.append(f'<text class="fig-label fig-accent-text" x="{left + 6}" y="{top + 14}">resonant, Δ = 0</text>')
    out.append(f'<text class="fig-label fig-alt-text" x="{f(left + plot_w * .30)}" y="{f(base - plot_h * .5 - 10)}" text-anchor="middle">detuned, Δ = Ω</text>')
    desc = ("Top: a sphere with z up. Starting at zero on top, the resonant path runs down the side of the sphere through the "
            "minus y point, marked pi over 2 pulse, to one at the bottom, marked pi pulse. The detuned path is a smaller circle "
            "that leaves the top and reaches only the equator, at the plus x point. Bottom: probability of reading one against "
            "pulse area from zero to two pi. The resonant curve rises from zero to one at pi and falls back to zero at two pi. "
            "The detuned curve peaks at one half, near pulse area 2.2, and oscillates faster.")
    return svg("pulse", width, base + 50, "A pulse moves the Bloch vector and sets the outcome probability", desc, "\n".join(out))


if __name__ == "__main__":
    for label, t, ratio in (("pi/2 pulse", math.pi / 2, 0), ("pi pulse", math.pi, 0),
                            ("detuned, Omega t = pi/sqrt2", math.pi / math.sqrt(2), 1)):
        r = bloch_after(t, ratio)
        print(f"{label:28s} r = {tuple(round(v, 4) for v in r)}  p(1) = {p1(t, ratio):.4f}")
    if "--write" in sys.argv:
        print("wrote", write("05-spin-single-qubit.html", {"pulse": figure()}), "figure")
