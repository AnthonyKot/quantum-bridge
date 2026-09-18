#!/usr/bin/env python3
"""Chapter 14 figure.

FIGURE RECORD
  syndrome  Three-qubit repetition code, |psi_L> = a|000> + b|111>, qubit 1 leftmost.
            For each error in {I, X1, X2, X3}: the corrupted state (both terms), the
            ancilla readings for the checks Z1Z2 and Z2Z3 (bit q1 xor q2 and q2 xor q3,
            0 meaning eigenvalue +1), and the recovery. The readings are computed from
            each term separately; the figure records that both terms give the same bits,
            so the reading does not depend on a and b.

Run without arguments to print the table; --write regenerates the SVG.
scripts/check_calculations.py (test_14) checks the readings with Z1Z2, Z2Z3 matrices and an
ancilla parity circuit for several (a, b), and that each recovery restores the state.
"""
import sys

from figlib import svg, write

ERRORS = [None, 0, 1, 2]         # which qubit is flipped (None = no error)


def flip(string, k):
    if k is None:
        return string
    return string[:k] + ("1" if string[k] == "0" else "0") + string[k + 1:]


def readings(string):
    q = [int(c) for c in string]
    return q[0] ^ q[1], q[1] ^ q[2]


def rows():
    out = []
    for k in ERRORS:
        terms = (flip("000", k), flip("111", k))
        r = {readings(t) for t in terms}
        assert len(r) == 1
        name = "none" if k is None else f"X{'₁₂₃'[k]}"
        out.append((name, terms, r.pop(), "none" if k is None else f"X{'₁₂₃'[k]}"))
    return out


def figure():
    width = 360
    cols = (0, 62, 216, 294)
    out = [f'<text class="fig-label fig-soft" x="{cols[0]}" y="16">error</text>',
           f'<text class="fig-label fig-soft" x="{cols[1]}" y="16">state after the error</text>',
           f'<text class="fig-label fig-soft" x="{cols[2]}" y="16">readings</text>',
           f'<text class="fig-label fig-soft" x="{cols[3]}" y="16">recovery</text>']
    for i, (name, (t0, t1), (s1, s2), rec) in enumerate(rows()):
        y = 30 + 44 * i
        out.append(f'<line class="fig-rule" x1="0" y1="{y}" x2="{width}" y2="{y}"/>')
        out.append(f'<text class="fig-label fig-strong" x="{cols[0]}" y="{y + 27}">{name}</text>')
        out.append(f'<text class="fig-label fig-math" x="{cols[1]}" y="{y + 28}">α|{t0}⟩ + β|{t1}⟩</text>')
        for j, bit in enumerate((s1, s2)):
            x = cols[2] + 26 * j
            css = "fig-cell fig-cell-on" if bit else "fig-cell"
            out.append(f'<rect class="{css}" x="{x}" y="{y + 9}" width="22" height="26"/>')
            out.append(f'<text class="fig-label fig-strong" x="{x + 11}" y="{y + 27}" text-anchor="middle">{bit}</text>')
        out.append(f'<text class="fig-label" x="{cols[3]}" y="{y + 27}">{rec}</text>')
    end = 30 + 44 * 4
    out.append(f'<line class="fig-rule" x1="0" y1="{end}" x2="{width}" y2="{end}"/>')
    out.append(f'<text class="fig-label fig-soft" x="0" y="{end + 20}">Readings: parity of qubits 1,2 and of qubits 2,3.</text>')
    out.append(f'<text class="fig-label fig-soft" x="0" y="{end + 38}">Both terms give the same bits, whatever α and β are.</text>')
    desc = ("A table with four rows. No error: state alpha 000 plus beta 111, readings 0 0, no recovery. X1: alpha 100 plus beta "
            "011, readings 1 0, recovery X1. X2: alpha 010 plus beta 101, readings 1 1, recovery X2. X3: alpha 001 plus beta 110, "
            "readings 0 1, recovery X3. Both terms of each state give the same readings.")
    return svg("syndrome", width, end + 46, "Syndrome readings and recoveries", desc, "\n".join(out))


if __name__ == "__main__":
    for r in rows():
        print(r)
    if "--write" in sys.argv:
        print("wrote", write("14-error-correction.html", {"syndrome": figure()}), "figure")
