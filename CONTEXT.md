# CONTEXT — authoring notes for *The Bridge*

Internal guide for keeping the essays consistent. Not published as a reader-facing page.

## Premise

Quantum computing added no new physics. It reinterpreted the standard postulates of a QM course as
statements about *information*. Each essay makes exactly one such crossing explicit, starting from
Landau & Lifshitz Vol. 3 (L&L) and landing on a named object in Nielsen & Chuang (N&C).

## The four-move template (every chapter)

Use these exact section headings (`<section class="move">` with an `<h2>` carrying a numbered pill):

1. **In the course** — the L&L framing, with § numbers. Course-side accent colour (`--course`).
2. **The step across** — the single reinterpretation. This is the heart; keep it to one idea.
3. **The result** — the N&C statement + a short *original* worked example. Result accent (`--result`).
4. **Reading** — pointers to L&L § and N&C §. No reproduced text.

Header, footer, and prev/next nav are copied verbatim between chapters (adjust titles/links only).

## Style guide

- Reader: has had / is taking a first serious QM course. Knows Hilbert spaces, Hermitian operators,
  Dirac notation. Assumes **no** prior quantum computing.
- Tone: scholarly but plain; short sentences; motivate every equation. Match The Quantum Quartet.
- Math: KaTeX, `$…$` / `$$…$$`. Prefer explicit small examples (single qubit, Bell pair) over generality.
- British/neutral spelling, en-dashes for ranges, `&` only in nav/titles.
- Never reproduce L&L or N&C prose. Cite sections; invent your own examples.

## Spine (L&L → N&C map)

| # | Slug | Course side (L&L) | Result side (N&C) | Status |
|---|------|-------------------|-------------------|--------|
| 01 | superposition-qubit | §2, §11 superposition principle | §1.2, §2.1–2.2 qubit, Bloch sphere, tensor product | **written** |
| 02 | observables-measurement | §3, §7 operators & measurement | §2.2.3–2.2.6 projective measurement, POVMs | stub |
| 03 | density-matrix | §14 density matrix | §2.4 mixed states, partial trace | stub |
| 04 | unitary-gates | §8 Schrödinger equation | Ch 4 gates, circuits, universality | stub |
| 05 | spin-single-qubit | Ch VIII spin | §2.1.3, §4.2 single-qubit gates, Pauli group | stub |
| 06 | linearity-no-cloning | linearity of QM | §1.3.5, Box 12.1 no-cloning theorem | **written** |
| 07 | composite-entanglement | Ch IX identity of particles | §2.5 entanglement, Bell states, Schmidt | stub |
| 08 | epr-bell | EPR & hidden variables | §2.6 Bell / CHSH inequalities | stub |
| 09 | teleportation-superdense | distinguishability & measurement | §1.3.7, §2.3 teleportation, superdense coding | **written** |
| 10 | interference-deutsch | superposition & interference | §1.4.3–1.4.4 Deutsch, Deutsch–Jozsa | stub |
| 11 | fourier-shor | Fourier methods | Ch 5 QFT, phase estimation, Shor | stub |
| 12 | amplitude-grover | amplitudes & probability | Ch 6 Grover search | stub |
| 13 | open-systems-channels | decoherence, reduced dynamics | Ch 8 quantum operations (Kraus) | stub |
| 14 | error-correction | redundancy & symmetry | Ch 10 quantum error correction | stub |
| 15 | entropy-holevo | von Neumann entropy | Ch 11–12 quantum entropy, Holevo | stub |

## Adding a stub → full essay

1. Copy an existing chapter file; rename to `chapters/NN-slug.html`.
2. Fix `<title>`, the `<h1>`, the four moves, and the prev/next links at the bottom.
3. On `index.html`, change that row's `<span class="stub">…</span>` to an `<a href="chapters/NN-slug.html">…</a>`
   and drop its `<span class="soon">soon</span>` badge.
4. Keep the KaTeX SRI hashes identical to the other pages.
