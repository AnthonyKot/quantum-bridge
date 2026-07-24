# CONTEXT — authoring notes for *The Bridge*

Internal guide for keeping the essays consistent. Not published as a reader-facing page.

## Premise

Quantum computing added no new physics. It reinterpreted the standard postulates of a QM course as
statements about *information*. Each essay makes exactly one such crossing explicit, landing on a
named object in Nielsen & Chuang (N&C).

**Course side = L&L + Sakurai.** Landau & Lifshitz Vol. 3 (L&L) is the anchor (continuity with The
Quantum Quartet), but it is the most austere text in the canon — no two-level tensor products, no
information, no Bell. Sakurai, *Modern Quantum Mechanics*, is the secondary mirror, cited wherever it
maps a result more cleanly (Stern–Gerlach/two-state systems, EPR, Bell). **Name the gap explicitly:**
where L&L (or both texts) never reaches the information-theoretic idea, the essay says so plainly
rather than papering over it — that honesty is a feature of the book, not a defect.

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
- **Pointer discipline (credibility is the whole game):** only cite a § you can verify against an
  actual copy in the working dir. When unverified, cite at chapter/topic granularity. Sakurai's
  numbering varies by edition — cite it by chapter and topic, never a bare § number.
- **Verified L&L §** (Vol. 3, Ch I–IX): §2 superposition, §3–4 operators, §7 wavefunction &
  measurement, §8 Hamiltonian/time-dependent equation, §14 density matrix, Ch VIII Spin, Ch IX
  Identity of particles. **Do not reuse** the earlier wrong pointers: §5 is the *continuous spectrum*
  (not composite systems); §11 is *Matrices* (not superposition). Re-verify all others when the
  source PDFs land in `sources/` (git-ignored).

## Spine (L&L → N&C map)

Course-side column lists L&L pointers first, Sakurai (chapter/topic) where it mirrors more cleanly.

| # | Slug | Course side (L&L / Sakurai) | Result side (N&C) | Status |
|---|------|-------------------|-------------------|--------|
| 01 | superposition-qubit | §2 superposition; Sakurai two-state systems | §1.2, §2.1–2.2 qubit, Bloch sphere, tensor product | **written** |
| 02 | observables-measurement | §3, §7 operators & measurement | §2.2.3–2.2.6 projective measurement, POVMs | stub |
| 03 | density-matrix | §14 density matrix | §2.4 mixed states, partial trace | stub |
| 04 | unitary-gates | §8 Schrödinger equation | Ch 4 gates, circuits, universality | stub |
| 05 | spin-single-qubit | Ch VIII spin | §2.1.3, §4.2 single-qubit gates, Pauli group | stub |
| 06 | linearity-no-cloning | linearity of QM | §1.3.5, Box 12.1 no-cloning theorem | **written** |
| 07 | composite-entanglement | Ch IX symmetrization → singlet; Sakurai coupled spins (**gap:** L&L has no entanglement-as-resource — name it) | §2.5 entanglement, Bell states, Schmidt | stub |
| 08 | epr-bell | Sakurai EPR & Bell (**gap:** L&L has neither) | §2.6 Bell / CHSH inequalities | stub |
| 09 | teleportation-superdense | §7 measurement; Sakurai EPR (**gap:** entanglement-as-resource is the book's step) | §1.3.7, §2.3 teleportation, superdense coding | **written** |
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
