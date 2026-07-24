# The Bridge

Essays that carry each topic of a university quantum-mechanics course forward to a concrete result in
**Nielsen & Chuang, *Quantum Computation and Quantum Information***. The "course" end is
**Landau & Lifshitz, *Quantum Mechanics* (Vol. 3)** — the same tradition featured in the sibling
collection, [The Quantum Quartet](https://anthonykot.github.io/quantum-quartet/).

Each essay makes one crossing, in four moves: **In the course → The step across → The result →
Reading**. See [`about.html`](about.html) for the method.

## Reading it

It's a plain static site — open `index.html` in a browser, or serve it:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000/
```

## Stack

- Plain HTML + one shared stylesheet (`static/style.css`) + one small script (`static/theme.js`).
- No build step, no framework, no static-site generator.
- Math via [KaTeX](https://katex.org/) from CDN (`$…$` inline, `$$…$$` display), with SRI hashes pinned.
- Light/dark theme (honours `prefers-color-scheme`, manual toggle persisted in `localStorage`).
- Print-friendly stylesheet.
- `.nojekyll` so GitHub Pages serves the files as-is.

## Structure

```
index.html            landing page + full table of contents
about.html            method & sources
chapters/NN-slug.html one file per essay
static/style.css      shared styles (themes, print)
static/theme.js       theme toggle + KaTeX auto-render
CONTEXT.md            authoring notes: spine, L&L↔N&C map, style guide
```

## Status

Scaffold + full 15-essay map complete. Written in full: essays **01** (qubit & Bloch sphere),
**06** (no-cloning), **09** (teleportation & superdense coding). The other twelve are stubbed on the
contents page.

## A note on sources

No copyrighted text from either book is reproduced. Essays cite section numbers and state results in
original prose and original examples.
