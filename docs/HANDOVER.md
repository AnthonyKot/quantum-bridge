# Book2 handover — 12 September 2026

## Objective and authorisation

The user asked to replace the book's rigid textbook-comparison framework, improve
its explanations, and publish. A subsequent review identified excessive
compression, undefined notation, abbreviated answers, and problems in Chapters
11 and 12. The agreed direction is deeper existing chapters, not more chapters.
The user has explicitly authorised publication; no further editorial approval is
required. The latest request is for this handover checkpoint.

Repository: `/home/diablo/book2`
Remote: `https://github.com/AnthonyKot/quantum-bridge.git`
Live site: `https://anthonykot.github.io/quantum-bridge/`
GitHub Pages: existing legacy deployment from `master`, repository root.

**Update 2026-09-12 (later session): browser regression re-run and passed on the revised files; independent re-review obtained (4/5, 4/5, 3.5/5) and its findings applied; docs updated. Commit and publication steps below were then executed; see git log.**

**State at the time of the original checkpoint: extensive local changes, not committed or published.**
Local `master` HEAD is `60f2dc3`; fetched `origin/master` is `9a14bbb`.
Do not reset or discard the working tree: it contains both the first rewrite and
the subsequent depth revision.

## Completed

### First rewrite (already present before this latest pass)

- Replaced all fifteen chapter bodies and removed the four-move comparison template.
- Added prerequisites, chapter section navigation, a notation guide, and thirty
  problems with expandable answers.
- Corrected claims about entanglement, measurement, Fourier sampling, channels,
  error correction, and information.
- Rebuilt contents/about pages and editorial instructions; retained chapter URLs.
- Added structural, numerical, and browser verification scripts.
- Added keyboard access and print handling that opens answers and restores them.

### Depth revision responding to the supplied review

All fifteen chapters have now received substantive expansions:

1. Defines expectation notation and derives its probability-weighted meaning;
   expands the interference cross term.
2. Explains the domains and action of the apparatus construction, then derives
   measurement-operator completeness.
3. Derives the partial trace by expanding local measurement probabilities.
4. Defines commutators; explains exact versus approximate gate construction,
   countability, and density with examples.
5. Replaces unexplained Levi-Civita notation with explicit Pauli anticommutation
   and the even/odd exponential-series derivation.
6. Derives factorised product overlaps and explains why copying contradicts
   unitarity; defines rays.
7. Defines and constructs the SVD through eigenvectors of C†C, before using it to
   obtain Schmidt form; explains its physical role and the kernel.
8. Explains the shared hidden-variable assignment behind CHSH, recalls the
   commutator, and removes the reviewed rhetorical sentences.
9. Writes all eight teleportation terms and groups them by Alice's prefixes;
   replaces “No-cloning is respected” with an explanation of where the state remains.
10. Derives the n-qubit Hadamard identity from the one-qubit rule and tensor products.
11. Substantially rebuilt: two-register evaluation, measurement projection and
    normalisation, coset definition, geometric sums, finite-precision phase
    estimation, the modular-multiplication unitary and its eigenphases, continued
    fractions, candidate verification, and resource costs.
12. Derives the diffusion matrix from the outer product, fixes “their product is”
    before individual matrices, and defines asymptotic O/Theta notation.
13. Derives Kraus operators from the joint output and partial trace; defines
    partial transpose before the example.
14. Defines syndrome and GHZ; derives syndrome signs from commutation and
    anticommutation on the entire code subspace.
15. Defines conditional entropy and mutual information using a joint-probability
    table and Bayes' rule; reintroduces POVM locally.

All thirty answers were expanded or rewritten to include intermediate working.
Chapter 11's second exercise now uses actual measured fractions and modular checks.

Important Chapter 11 correction: the unknown phase fraction in lowest terms occurs
among the convergents of the measured k/N. It is not obtained by reducing k/N.
Examples include 85/256 → convergent 1/3 and modular multiplication by 2 modulo 21
with samples 341/1024 and 171/1024. N ≥ 2r² is explained as a sufficient register-size
margin for a sufficiently close sample, not a necessary hypothesis of Legendre's
approximation theorem or a guarantee of every measurement outcome.

### Upstream changes preserved in the working tree

Fetched remote commit `9a14bbb`, which vendors KaTeX, fixes rendering readiness,
and changes typography/themes/equation styling. Its mathematical content is still
the old book.

- Copied its `static/katex/` assets into the working tree.
- Switched all seventeen HTML pages from CDN KaTeX URLs to those local assets.
- Combined its stylesheet with local navigation, solution, accessibility, and
  print styles; removed obsolete comparison-template styling.
- Combined its rendering bootstrap with the local beforeprint/afterprint behavior.
- Updated README for local math assets. Google reading fonts retain system fallbacks.

**This integration is currently at file level only. Git ancestry is not merged.**

## Verification already completed on the latest files

- `./verify.sh` passed after the depth rewrite and upstream file integration.
- All eighteen numerical test groups passed (standard-library Python).
- `scripts/check_content.py` passed for all seventeen HTML pages and thirty answers.
- `git diff --check` passed at the handover checkpoint.
- New numerical checks verify the two-register projection, the actual modular
  multiplication permutation and eigenstates, continued-fraction examples and
  order checks, extracted Kraus operators, and mutual information computed directly
  from joint probabilities.
- Continued-fraction theorem checked against primary academic notes:
  `https://crypto.stanford.edu/pbc/notes/contfrac/converge.html`.
- GitHub Pages configuration was checked through `gh api`.

The earlier rewrite passed desktop/mobile browser and print checks, but **the
latest depth revision and integrated upstream styles have not yet had their final
browser review**. Do not report the earlier browser result as validation of these
latest files. The localhost server is currently not running: port 8022 refused
connection at the last check.

## Remaining work, in order

1. Read the revised book in order, focusing on the newly expanded hinges and all
   answers. Check that definitions precede use and paragraphs connect the reasoning.
   Numerical tests do not establish pedagogical quality. Inspect especially the
   reordered SVD section, Chapter 11, and newly added long displays.
2. Start the local server and run the browser regression. Inspect screenshots at
   desktop and phone widths, math rendering, long equation scrolling, keyboard
   solutions, and print. Check the combined upstream styles and dark-theme print.
3. Update `docs/rewrite-review.md` and `CONTEXT.md` to reflect this second revision,
   its explicit acceptance criteria, current asset setup, and actual final results.
   The existing review report primarily describes the first rewrite and includes
   stale references to fifteen test groups and CDN loading.
4. Re-run required checks after any fixes. Review the staged diff; exclude `sources/`
   and temporary files. Sources remain ignored; temporary editing scripts live in
   `/tmp` and are not required to build or edit the site.
5. Commit the current coherent work, then reconcile `origin/master` with a normal
   merge (or another history-preserving workflow). Inspect conflicts and retain
   both the new content and upstream rendering changes. Do not force-push or
   replace the remote history. Re-fetch if necessary to detect newer remote work.
6. Run checks on the final merged tree and push `master` to origin. Publication is
   already authorised.
7. Confirm the Pages build succeeds for the pushed commit and smoke-test the live
   site, including the corrected Chapter 11 and local KaTeX assets. Report the live
   URL and results, distinguishing deployment from merely pushing a commit.

## Commands and environment

From `/home/diablo/book2`:

```bash
./verify.sh
python3 -m http.server 8022 --bind 127.0.0.1
```

In a separate session, with the server running:

```bash
PLAYWRIGHT_MODULE=/home/diablo/book11/node_modules/playwright/index.mjs node scripts/check_browser.mjs
```

Browser test options: `BASE_URL` (default `http://127.0.0.1:8022`) and
`ARTIFACT_DIR` (default `/tmp/book2-review`). Existing browser artifacts in that
folder belong to the previous rewrite until replaced. Playwright and Chromium are
already installed; no new frontend framework or site build is needed.

GitHub checks:

```bash
gh api repos/AnthonyKot/quantum-bridge/pages
gh api repos/AnthonyKot/quantum-bridge/pages/builds/latest
```

Sandbox network calls failed on GitHub and were successfully retried with tool
escalation. Chromium likewise previously required execution outside the sandbox.
Use the normal escalation mechanism when needed; no manual credential handling.

Useful files:
- `scripts/check_calculations.py`: eighteen numerical test groups.
- `scripts/check_content.py`: HTML, destinations, and chapter structure.
- `scripts/check_browser.mjs`: browser/keyboard/print regression.
- `verify.sh`: combined verification entry point.
- `docs/rewrite-review.md`: older review record, pending update.
- `/tmp/book2-depth.py`: one-shot depth-edit script, already applied. **Do not rerun**:
  its replacement anchors assume the earlier files.
- `/tmp/book2-integrate.py`: one-shot upstream file integration, already applied.
  **Do not rerun**: it asserts the vendor files do not yet exist.

The four-star target is a reader-quality goal, not a rating that technical tests
can certify. No independent review of this latest expansion has yet been obtained.
