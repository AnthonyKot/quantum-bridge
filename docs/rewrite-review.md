# The Bridge: rewrite and review record

> **Note (18 September 2026).** This record describes the 12 September rewrite. The later rework
> (opening questions, figures, optional derivations, closing sections, new title "Quantum Information,
> Explained") and its reviews are recorded in `docs/REWORK-PLAN.md`, which is the current record.


Date: 2026-09-11, updated 2026-09-12 after the depth revision. Scope: the complete
local book, all fifteen chapter bodies, contents, reader's guide, editorial rules,
and shared reading controls.

## Editorial change

The previous fixed textbook-comparison structure has been removed. Chapters now
follow the mathematical question they need to answer. This is a substantive
replacement of their explanations and examples, not a heading-only change.
The subject sequence and existing chapter URLs remain stable.

Each chapter has explicit prerequisites, topic-specific section navigation,
worked calculations, two problems with worked answers, and further reading.
The notation guide specifies register order, matrix order, phases, and entropy
conventions. General theorems used without proof are identified as such.

The revised text is shorter overall: repeated claims about textbooks and the
book's own importance were removed. Explanation is concentrated on mathematical
steps, physical interpretation, assumptions, and counterexamples. Word count and
formula count were not used as substitutes for correctness or learning quality.

## Substantive corrections and additions

| Chapter | Rebuilt explanation / corrected claim |
| --- | --- |
| 01 | Derives measurement interference and Pauli means; distinguishes equal basis probabilities from equivalent states. |
| 02 | Separates POVM effects from state updates; derives measurement operators and an explicit dilation; checks discrimination positivity by eigenvalues. |
| 03 | Derives partial trace from local predictions; contrasts a Bell state with a separable correlated mixture; removes the claim that every interaction entangles. |
| 04 | Tracks matrix order, Bell preparation, reversible oracles, and controlled phases; distinguishes universality from efficient synthesis. |
| 05 | Derives the rotation exponential and pulse probabilities; adds state preparation, detuning, and population-error examples. |
| 06 | Gives linearity and overlap proofs, including an apparatus; identifies exact/deterministic scope and distinguishes encoding from cloning. |
| 07 | Derives Schmidt form from SVD, with correct conjugation; calculates a nontrivial reduced spectrum; separates pure and mixed criteria. |
| 08 | States local-model assumptions, derives CHSH and its quantum bound, and computes a violation; fixes the false all-bases-agree claim for Phi+. |
| 09 | Tracks all three teleportation registers and every correction; proves the unconditioned output is I/2; counts dense coding's shared resource. |
| 10 | Derives phase kickback and final amplitudes; corrects the claim that a computational measurement of a phase-only encoding reveals f(x); states promise and query assumptions. |
| 11 | Calculates Fourier peak probabilities and finite-precision phase estimates; includes failed/divisor-only samples, continued fractions, verification, and controlled-power costs. |
| 12 | Multiplies both reflections, derives the iteration formula, and checks overshoot numerically; distinguishes oracle calls from total runtime. |
| 13 | Derives Kraus form and complete positivity, with a transpose counterexample; calculates damping/dephasing; removes entropy-always-increases rhetoric. |
| 14 | Constructs parity recovery, a coherent-error example, and Shor code checks; explains degeneracy and the Knill–Laflamme criterion instead of claiming syndromes always name unique errors. |
| 15 | Distinguishes entropy from mutual information; calculates two equal-average ensembles with different information, a nonorthogonal example, and both dense-coding Holevo quantities. |

## Verification evidence

- `./verify.sh` passed: chapter count, contents links, previous/next chain, local assets,
  delimiters, HTML nesting, local anchors, answer controls, and editorial scans.
- `scripts/check_calculations.py` passed: eighteen numerical test groups (one per chapter plus
  three added with the depth revision: two-register projection and modular multiplication,
  continued-fraction examples and order checks, Kraus extraction and joint-probability
  mutual information),
  implemented with Python's standard library. Tests include full teleportation
  circuits on multiple complex inputs, all promised two-bit Deutsch–Jozsa truth
  tables, direct Fourier and Grover matrix evolution, channel output matrices,
  and the nine-qubit recovery criterion for every pair of single-site Pauli errors.
- Browser regression passed with no reported issues on all seventeen pages at 1440px and 390px, KaTeX
  rendering from the vendored assets in `static/katex/` (1,419 formulas), absence of page overflow, thirty keyboard-operated answers,
  persisted themes, skip navigation, and print behavior.
- Print review caught omitted collapsed answers. The shared script now opens them
  for printing and restores their previous state afterward. Print colours also
  override the saved dark theme. A generated PDF was checked for solution text.
- Two equations that overflowed the desktop reading column were split into
  separate mathematical steps. Narrow-screen display equations can scroll locally.
- Source section locations were checked against the local Nielsen & Chuang
  10th Anniversary Edition contents; primary-paper links were checked online.
- The chapter sequence was reviewed for notation and prerequisites. Later concepts
  are introduced locally or explicitly deferred, rather than assumed silently.

## Second revision (2026-09-11/12): depth, not breadth

An independent three-reviewer read of the first rewrite, against a reader with one to two
years of a technical degree reading casually, found no factual error in any computed
quantity but rated the text 3/5: reference-card compression, symbols used before
definition (expectation notation, SVD, commutator, mutual information, POVM, GHZ, partial
transpose, asymptotic notation), roughly half of the thirty answers stated rather than
worked, two rhetorical sentences arguing with popular accounts, and one genuine error in
Chapter 11 (the continued-fraction convergent described as "the reduced fraction").

The depth revision answered that review chapter by chapter (see `docs/HANDOVER.md` for
the itemised list): each chapter's load-bearing derivation is now written out, the
listed symbols are defined where first used, all thirty answers show intermediate
working, the rhetorical sentences are removed, and Chapter 11 was rebuilt around the
two-register state, the coset, the modular-multiplication unitary and its eigenphases,
and worked continued-fraction examples. Chapter text grew from about 13,300 to 16,100
words. The upstream commit that vendors KaTeX and restyles the pages was integrated at
file level; all pages now load the local assets.

Checks on the revised files (2026-09-12): `./verify.sh` PASS; eighteen numerical test
groups PASS; browser regression PASS on all seventeen pages at both widths with no
issues; screenshots of the contents page, Chapter 9 and Chapter 15 inspected by eye.

### Independent re-review of the depth revision (2026-09-12)

The same three-reviewer read was repeated on the revised chapters. Result: chapters 6–10
and 11–15 at 4/5 for the target reader, chapters 1–5 at 3.5/5; no computed quantity
wrong anywhere; every one of the thirty answers now shows intermediate steps. Remaining
findings were applied the same day, each verified by re-derivation before insertion:
chapter 3 defines the indexed Pauli symbols at their use; chapter 4 reorders §5 so the
alphabet is defined before it is discussed, displays the telescoping error sum, and ties
"oracle" to the function box; chapter 5 writes the Schrödinger equation, the bare-qubit
Hamiltonian (so "ground state" is correct in context), and defines population, π pulse,
rotating frame and detuning; chapter 6 explains the operator inequality and the
positivity step; chapter 7 gives the coefficient form of the partial trace and repairs a
dangling clause; chapter 8 writes the hidden-variable averaging line and notes the two
meanings of A_x; chapter 9 proves the transpose identity; chapter 10 defines N at first
use; chapter 11 states the convergent-selection rule; chapter 14 defines the code space
and checks Knill–Laflamme on the repetition code; the notation guide gains eleven rows.
Checks after these edits: verify PASS, content PASS, eighteen numerical groups PASS,
browser regression PASS (17 pages, 2 widths, 1,515 formulas, 30 answers, no issues).
Not yet done: a fresh independent read of chapters 4 and 5 after the reorder.

## Limits of this review

The numerical tests check examples and finite-dimensional identities. They do not
prove the cited general theorems or establish that every prose claim is correct.
The quotation scan detects a known phrase list, not every possible textual overlap.
Checking a table of contents verifies a section pointer, not all claims attributed
to that chapter.

No independent subject-matter reviewer or learner study has rated this revision.
A four-star reader rating is the intended quality target, not a measurement that
these technical checks can certify. The implemented evidence is the replacement
text, its reproducible calculations, worked answers, and the verified reading UI.

## Reproduce the browser checks

Serve the root with `python3 -m http.server 8022 --bind 127.0.0.1`.
With Playwright available, run `node scripts/check_browser.mjs`. If it is installed
outside this project, set `PLAYWRIGHT_MODULE` to the absolute path of its
`index.mjs`. `BASE_URL` overrides the server URL; `ARTIFACT_DIR` overrides the
screenshot/PDF directory (default `/tmp/book2-review`). No site build is needed.
