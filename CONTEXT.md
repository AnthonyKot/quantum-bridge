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
- **Verified L&L §** (OCR'd the Contents of `sources/landau-lifshitz-vol3-qm.pdf`, a scan): §2 The
  principle of superposition (p6), §3–4 operators, §7 The wave function and measurements (p21), §8 The
  Hamiltonian operator (p25), §14 The density matrix (p38), Ch VIII Spin = §54–60 (Spin §54, Spinors §55,
  partial polarisation §59), Ch IX Identity of particles = §61–65 (indistinguishability §61, exchange
  interaction §62 — where two-spin singlet/triplet live). **Confirmed wrong, never reuse:** §5 =
  *continuous spectrum*, §11 = *Matrices*, and note §17 (not §8) is "Schrödinger's equation" proper.
- **Verified N&C §** (10th Anniversary Ed. 2010, `sources/nielsen-chuang-full.pdf`): §1.2 qubit/Bloch,
  §1.3.5 *“Qubit copying circuit?”* (no-cloning), §1.3.7 teleportation, §2.2.3/2.2.5/2.2.6
  measurement/projective/POVM, §2.2.8 composite systems, §2.3 superdense coding, §2.4 density operator,
  §2.5 Schmidt, §2.6 *EPR and the Bell inequality*, §12.1 distinguishing states/accessible info,
  §1.4.3–1.4.4 Deutsch(–Jozsa); chapters 4/5/6/8/10/11/12 confirmed for the stubs. There is **no** "Box
  12.1" — don't cite it.
- **Verified Sakurai §** (3rd ed., Napolitano, `sources/sakurai-napolitano-3e.pdf`): §3.10 *Spin
  Correlation Measurements and Bell's Inequality* (EPR/Bell, essay 08), §3.10.1 spin-singlet
  correlations. Cite topic-first, `(§3.10)` parenthetical.

## Sourcing discipline — TWO PASSES (hard rule)

The source PDFs and generation want **opposite** access to the same file. With a book's sentence sitting
in the context window, the path of least resistance is to reproduce it — which is exactly how essay 02
first shipped three verbatim N&C quotes and essay 08 a verbatim EPR sentence. So separate the passes:

- **Verification pass — sources OPEN.** Confirm § numbers, titles, and values against the PDFs. Pin every
  pointer you'll need.
- **Writing pass — sources CLOSED.** Do NOT read the PDFs while drafting. State every fact (theorem,
  definition, result) in your own words, from understanding. A theorem's *content* is free to state; its
  author's *sentence* is not.
- Order: verify first, close the files, then write.

**No-reproduction line is held absolutely** (the footer promises it — do not weaken the footer instead).
Allowed: section/chapter TITLES as bibliographic citations (e.g. §2.6 *EPR and the Bell inequality*), and
standard field terminology (*element of reality*, *spooky action*). Not allowed: any sentence or phrase of
source *exposition*, quoted or lightly reworded.

**Verification checklist — quotation scan (STANDING step, run on every essay):** after writing, `grep`
the essay for ASCII `\"`, read every `<blockquote>` by eye, and eyeball each hit. Multibyte trap: a
bracket-class regex like `[“"]` is unreliable on curly quotes in this locale — never trust one regex;
read the blockquotes. This is permanent, not cleanup: the verbatim EPR criterion in essay 08 was found
only by the sweep, not by suspicion.

## Spine (L&L → N&C map)

Course-side column lists L&L pointers first, Sakurai (chapter/topic) where it mirrors more cleanly.

| # | Slug | Course side (L&L / Sakurai) | Result side (N&C) | Status |
|---|------|-------------------|-------------------|--------|
| 01 | superposition-qubit | §2 superposition; Sakurai two-state systems | §1.2, §2.1–2.2 qubit, Bloch sphere, tensor product | **written** |
| 02 | observables-measurement | §7 projective measurement (**gap:** no course does POVMs — that gap IS the essay) | §2.2.5 projective, §2.2.6 POVM, Box 2.3/2.5 (Naimark) | **written** |
| 03 | density-matrix | §14 density matrix (**no manufactured gap:** L&L already frames ρ as a subsystem's state; N&C changes the *use*, not the object) | §2.4 density operator, §2.4.3 reduced density operator/partial trace | **written** |
| 04 | unitary-gates | **CROSSING REWRITTEN** (old "unitary → gates" duplicates 05's two-level rotations). Real non-overlapping content = **universality**: a finite gate set densely generates the whole unitary group — a question with **no course-side counterpart** (physics never asks which Hamiltonians suffice to reach every other). Gap-shaped essay. | Ch 4 §4.5 universal quantum gates (§4.5.2 single-qubit+CNOT, §4.5.3 discrete sets) | stub — rewrite crossing before writing (like 11) |
| 05 | spin-single-qubit | Ch VIII spin → Bloch rotations (**owns the two-level rotations; keep disjoint from 04's universality**) | §2.1.3 Pauli matrices, §4.2 single qubit operations | stub |
| 06 | linearity-no-cloning | linearity of QM | §1.3.5, Box 12.1 no-cloning theorem | **written** |
| 07 | entanglement-schmidt | **crossing = failure of separation of variables** (course: ψ(x₁,x₂) won't factor = nuisance; N&C: same non-product state = defining resource — obstacle→asset, cleanest thesis instance). Schmidt = essay 03 backwards (singular values of coeff matrix; λ_i² = reduced-density eigenvalues; rank 1 ⟺ product). **Caution not crossing:** identical-particle antisymmetry (L&L Ch IX §61–63) looks entangled but isn't a resource (not separately addressable); symmetrization = constraint on legal states, entanglement = property of a state you have. | §2.5 Schmidt & purifications; §2.2.8 composite systems | **written** |
| 08 | epr-bell | Sakurai §3.10 EPR & Bell's inequality (**gap:** L&L/Feynman have neither) | §2.6 EPR and the Bell inequality | **written** |
| 09 | teleportation-superdense | §7 measurement; Sakurai EPR (**gap:** entanglement-as-resource is the book's step) | §1.3.7, §2.3 teleportation, superdense coding | **written** |
| 10 | interference-deutsch | superposition & interference | §1.4.3–1.4.4 Deutsch, Deutsch–Jozsa | stub |
| 11 | fourier-shor | **CROSSING REWRITTEN** (old "Fourier on ℤ_N" was borrowed from harmonic analysis, not in any course). New: momentum eigenstates = eigenstates of the *translation operator*; the QM Fourier transform is the change of basis that diagonalizes translations; the QFT is the same for translations on the cyclic group ℤ_N; period-finding reads off that eigenvalue. L&L has the translation operator + momentum as its generator. | Ch 5 §5.1 QFT, §5.2 phase estimation, §5.3 factoring | stub — **SPLIT**: period-finding (11) vs number theory/factoring (11b) |
| 12 | amplitude-grover | amplitudes & probability | Ch 6 Grover search | stub |
| 13 | open-systems-channels | decoherence, reduced dynamics | Ch 8 quantum operations (Kraus) | stub |
| 14 | error-correction | **crossing = the CSCO** (L&L §3–4: complete set of commuting observables — verified; code space = their joint eigenspace, syndrome = measuring that CSCO; hydrogen labelled by {H,L²,L_z}). Move 2: syndrome = which *error* not which *state* (subspace not ray → callback 02/03); continuous a·I+b·X+c·Y+d·Z collapses to one Pauli, "digital because you looked". History stated as "widely argued", not documented consensus. Ends at 9-qubit + discretization (no stabilizer/CSS/threshold). | Ch 10 §10.1.1 bit-flip, §10.1.2 phase-flip, §10.2 Shor 9-qubit | **written** |
| 15 | entropy-holevo | von Neumann entropy (§14 density matrix; needs 02 POVMs) | Ch 11 §11.3 von Neumann entropy, §12.1.1 Holevo | stub |

### Sequencing notes (write order, by dependency)

- **02 is the highest-dependency node** — 03, 13, 15 are all written in the vocabulary of POVMs (Kraus
  operators ≈ a POVM with post-measurement states kept). Writing 02 unblocks a third of the series.
  *(done)*
- **14 is self-contained** — good for momentum/story. Bit-flip, phase-flip, and the 9-qubit code need
  only Pauli errors, so it does **not** wait on 13. The "digital because you looked" syndrome argument
  is the Move 2 step across, not a footnote.
- **11 is blocked on itself** until the crossing is rewritten (translation operator, above) **and split**
  into period-finding vs number-theory. The N&C side (QFT circuit, §5.1/§5.3) is the safest material in
  the book; the risk was always the course side. Don't write until reframed.

## Adding a stub → full essay

1. Copy an existing chapter file; rename to `chapters/NN-slug.html`.
2. Fix `<title>`, the `<h1>`, the four moves, and the prev/next links at the bottom.
3. On `index.html`, change that row's `<span class="stub">…</span>` to an `<a href="chapters/NN-slug.html">…</a>`
   and drop its `<span class="soon">soon</span>` badge.
4. Keep the KaTeX SRI hashes identical to the other pages.
