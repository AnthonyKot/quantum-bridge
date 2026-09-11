# The Bridge

Fifteen chapters on quantum mechanics and quantum information, rebuilt around
calculations rather than a comparison between textbooks. Topics progress from
states and measurements through gates, entanglement, communication, algorithms,
noise, error correction, and entropy.

Readers need complex numbers, linear algebra, and elementary probability. Every
chapter provides prerequisite notes, mathematical explanations, worked examples,
and two problems with expandable worked answers. Larger results used without
proof are labelled and referenced.

## Read locally

```bash
python3 -m http.server 8022 --bind 127.0.0.1
```

Open `http://127.0.0.1:8022/`. Start with `index.html`; `about.html` contains the
notation guide. Chapter URLs remain stable across the rewrite.

## Edit and verify

The published files are plain HTML, CSS, and JavaScript. There is no framework,
content generator, package installation, or build step. Edit chapter HTML directly.
KaTeX and its equation fonts are served from `static/katex/`, preserving the
upstream rendering fixes without a CDN dependency for mathematics. Reading fonts
use Google Fonts with system fallbacks. Light/dark themes and print styles are shared.

```bash
./verify.sh
python3 scripts/check_calculations.py
# Optional browser checks, with Playwright available and the local server running:
node scripts/check_browser.mjs
```

The first command checks structure, navigation, local links and anchors, math
balance, problem/answer presence, and editorial regressions. The second independently
checks the worked finite-dimensional calculations using only Python's standard
library. Neither substitutes for mathematical review of the prose or proves the
cited general theorems.

- `chapters/`: the fifteen chapters, including their answers.
- `static/`: shared reading styles and theme/math bootstrap.
- `scripts/`: content and numerical verification.
- `CONTEXT.md`: current editorial and notation rules.
- `docs/rewrite-review.md`: rewrite scope, corrected claims, and validation record.

Nielsen & Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary
Edition, supplies the main further-reading references. Source PDFs remain local,
ignored by Git, and excluded from the site.
