# Editorial guide — The Bridge

## Current direction

The September 2026 rewrite replaces the old L&L-to-N&C comparison framework.
There is no required “In the course / The step across / The result / Reading”
structure. The user's explicit request was to rebuild the essays from zero with
more explanation, formulas, and less generated-sounding filler. Do not restore
that framework, its “crossing” rhetoric, or its restrictions on useful mathematics.

The audience knows complex numbers and linear algebra but need not know quantum
information. Use the main sequence in index.html; keep existing chapter URLs.
The HTML is the editable source, with no build step.

## Explanations

- Open with a concrete mathematical or operational question.
- Define the system, input, basis, and assumptions before calculating.
- Explain why an equation follows and what its terms predict. More formulas alone
  do not make a better explanation.
- Work an actual instance: track vectors, probabilities, registers, or error branches.
- Check limiting cases, normalisation, and counterexamples to tempting overclaims.
- Include two problems with expandable worked answers; vary the example or an assumption.
- Use topic-specific section headings. No prescribed number of sections.
- Remove commentary about what “the course” missed, artificial paradoxes, grand
  conclusions, and assertions that a chapter is especially important or elegant.
- Distinguish proved calculations from cited theorems. Do not imply universality
  establishes efficient circuits, query bounds establish runtime, or an example
  proves a general optimality claim.

## Conventions

- Column vectors; bras are conjugate transposes. AB means B acts first.
- Tensor basis order 00, 01, 10, 11, leftmost register first.
- X, Y, Z are Pauli matrices; H is Hadamard; use mathcal H for Hamiltonians.
- R_n(theta) = exp(-i theta n.sigma / 2).
- Bell labels: beta_ab = (I tensor X^b Z^a) Phi+.
- Teleportation outcome (a,b) leaves X^b Z^a psi; recovery is Z^a X^b.
- Positive-sign forward QFT, negative-sign inverse; integer basis order explicit.
- All information logarithms base two; distinguish H(X), S(rho), and I(X:Y).
- KaTeX delimiters are dollar/double-dollar. Escape HTML where needed.

## Claims that must retain their qualifications

- POVM effects specify probabilities, not a unique state update.
- Mixed reduced states certify entanglement only when the joint state is pure.
- Interactions do not invariably entangle; CNOT leaves several product inputs product.
- Phi+ has YY correlation -1, so outcomes do not agree in every identical basis.
- No-cloning concerns deterministic exact copying of arbitrary unknown states.
- Measuring a phase-encoded oracle state does not disclose f(x).
- Fourier samples yield partial/approximate period information and require classical
  postprocessing, verification, and sometimes retries.
- Controlled powers may be expensive. Gate universality does not solve that problem.
- Grover's target count, stopping rule, and oracle cost must be specified.
- The channel construction assumes a fixed initially uncorrelated environment.
- Kraus labels need a specified apparatus measurement to denote physical outcomes.
- Noise can reduce system entropy, as full amplitude damping does.
- Error syndromes need not uniquely identify physical errors; degenerate codes matter.
- A message-independent maximally mixed signal carries zero information about the
  message. Dense coding's decoder uses both qubits and pre-shared entanglement.

## Sources

Nielsen & Chuang, 10th Anniversary Edition (2010), is the main reference.
The section pointers were checked against the local PDF's table of contents.
This verifies pointer locations, not every assertion in a chapter. Keep that
boundary explicit in any validation report.

Verify citations before drafting. Do not copy source exposition; write from the
mathematical reasoning after the verification pass. Source titles may be used in
bibliographic references. Prefer chapter/topic references if a section has not
been checked. The local sources directory remains ignored and unpublished.

## Assets and records

- KaTeX is vendored under `static/katex/`; pages must reference it locally, never a CDN.
- `docs/rewrite-review.md` is the change and verification record; `docs/HANDOVER.md`
  is the working checkpoint. Update both when a revision changes what the checks cover.
- `scripts/check_calculations.py` holds eighteen numerical test groups; add a group
  whenever a chapter gains a new worked example.

## Verification

Run ./verify.sh and python3 scripts/check_calculations.py after substantive edits.
For changed math/layout, also open actual pages in a browser and check KaTeX errors,
narrow-screen overflow, keyboard answer toggles, navigation, and printing. Ensure
printed copies include worked answers. Test numerical claims independently of the
formula used in the text where feasible. Tests of examples do not prove theorems.

Before concluding a substantive rewrite, read the book in sequence and check that
terms are introduced before use, internal conventions agree, and references to
later chapters are explicit. Record remaining review limits honestly.
