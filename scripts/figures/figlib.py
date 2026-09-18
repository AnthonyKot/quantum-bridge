"""Shared helpers for the figure scripts.

Each chapter script computes its numbers, builds one or more inline SVG strings,
and with --write replaces the text between <!-- FIGURE:name --> and
<!-- /FIGURE:name --> in the chapter. Colours and fonts come from CSS classes in
static/style.css, so figures follow the light, dark and print themes.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def f(x):
    """Coordinate formatting: one decimal, no trailing zero noise."""
    return f"{x:.1f}".rstrip("0").rstrip(".")


def svg(name, width, height, title, desc, body):
    return (f'<svg class="fig-svg" viewBox="0 0 {width} {height}" role="img" '
            f'aria-labelledby="fig-{name}-title fig-{name}-desc">\n'
            f'<title id="fig-{name}-title">{title}</title>\n'
            f'<desc id="fig-{name}-desc">{desc}</desc>\n{body}\n</svg>')


def write(chapter, figures):
    """figures: {name: svg string}. Returns the number of figures replaced."""
    path = ROOT / "chapters" / chapter
    text = path.read_text()
    for name, content in figures.items():
        pattern = re.compile(rf"(<!-- FIGURE:{name} -->).*?(<!-- /FIGURE:{name} -->)", re.S)
        if not pattern.search(text):
            raise SystemExit(f"{chapter}: no FIGURE:{name} markers")
        text = pattern.sub(lambda m: m.group(1) + "\n" + content + "\n" + m.group(2), text)
    path.write_text(text)
    return len(figures)
