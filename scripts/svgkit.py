"""Tiny SVG toolkit for the profile README.

Every image is a self-contained SVG: the fonts it needs are subset to the exact
glyphs it uses and embedded as woff2 data URIs, because GitHub serves README
images through a proxy that blocks external font requests.
"""
from __future__ import annotations

import base64
import io
from functools import lru_cache
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
OUT = ROOT / "assets" / "img"

# Colour tokens lifted from EverythingTech (docs/assets/app.css).
THEMES = {
    "dark": {
        "bg": "#16181f", "bg2": "#1a1d25", "surface": "#1e222b", "surface2": "#252a35",
        "ink": "#ebe7de", "ink2": "#c6c2b8", "muted": "#9097a6", "faint": "#656c7c",
        "line": "#323847", "strong": "#454d61", "shadow": "#0a0b0f",
        "lime": "#bef264", "cyan": "#5eead4", "violet": "#a78bfa", "pink": "#ff6ec7",
        "amber": "#fbbf24", "coral": "#ff8a65", "blue": "#7aa2ff", "mint": "#6ee7b7",
        "grain": 0.05,
    },
    "light": {
        "bg": "#f2eee4", "bg2": "#ebe5d8", "surface": "#faf7f0", "surface2": "#f4efe4",
        "ink": "#1a1c23", "ink2": "#3a3d47", "muted": "#62656f", "faint": "#8f8f97",
        "line": "#d8cfbd", "strong": "#1c1e26", "shadow": "#1c1e26",
        "lime": "#4f7d00", "cyan": "#0e8f83", "violet": "#6645cf", "pink": "#c8237f",
        "amber": "#a55f00", "coral": "#c24620", "blue": "#2856c4", "mint": "#12815f",
        "grain": 0.035,
    },
}

# style key -> (font file, css family, weight, italic)
STYLES = {
    "d8": ("display-800", "SPDisplay", 800, False),
    "d7": ("display-700", "SPDisplay7", 700, False),
    "si": ("serif-italic", "SPSerif", 450, True),
    "m4": ("mono-400", "SPMono", 400, False),
    "m7": ("mono-700", "SPMono7", 700, False),
}
FALLBACK = {
    "d8": "'Helvetica Neue',Arial,sans-serif", "d7": "'Helvetica Neue',Arial,sans-serif",
    "si": "Georgia,serif", "m4": "ui-monospace,Menlo,monospace", "m7": "ui-monospace,Menlo,monospace",
}


@lru_cache(maxsize=None)
def _font(style: str) -> TTFont:
    return TTFont(FONTS / f"{STYLES[style][0]}.woff2")


def measure(text: str, style: str, size: float, tracking: float = 0.0) -> float:
    """Advance width in px (no kerning; close enough for layout)."""
    f = _font(style)
    cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    units = sum(hmtx[cmap.get(ord(c), cmap.get(ord("?")))][0] for c in text)
    return units * size / upm + tracking * size * len(text)


def wrap(text: str, style: str, size: float, width: float, tracking: float = 0.0) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and measure(trial, style, size, tracking) > width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def _font_face(style: str, chars: set[str]) -> str:
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga"]
    opts.name_IDs = []
    opts.notdef_outline = True
    sub = subset.Subsetter(opts)
    sub.populate(text="".join(sorted(chars)) + " ")
    f = TTFont(FONTS / f"{STYLES[style][0]}.woff2")
    sub.subset(f)
    buf = io.BytesIO()
    f.flavor = "woff2"
    f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    _, fam, weight, italic = STYLES[style]
    return (f"@font-face{{font-family:{fam};src:url(data:font/woff2;base64,{b64}) format('woff2');"
            f"font-weight:{weight};font-style:{'italic' if italic else 'normal'}}}")


class SVG:
    def __init__(self, w: float, h: float, theme: str, title: str):
        self.w, self.h, self.theme, self.title = w, h, theme, title
        self.t = THEMES[theme]
        self.body: list[str] = []
        self.css: list[str] = []
        self.defs: list[str] = []
        self.chars: dict[str, set[str]] = {}

    def c(self, token: str) -> str:
        return self.t.get(token, token)

    # --- primitives -------------------------------------------------------
    def add(self, raw: str) -> None:
        self.body.append(raw)

    def rect(self, x, y, w, h, fill="none", stroke=None, sw=1, rx=3, extra="") -> None:
        s = f' stroke="{self.c(stroke)}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{self.c(fill)}"{s} {extra}/>')

    def line(self, x1, y1, x2, y2, stroke="line", sw=1, dash=None, extra="") -> None:
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{self.c(stroke)}" stroke-width="{sw}"{d} {extra}/>')

    def text(self, x, y, s: str, style="m4", size=12, fill="ink", anchor="start",
             tracking=0.0, cls="", extra="") -> None:
        self.chars.setdefault(style, set()).update(s)
        ls = f' letter-spacing="{tracking * size:.2f}"' if tracking else ""
        classes = f"{style} {cls}".strip()
        self.add(f'<text x="{x}" y="{y}" class="{classes}" font-size="{size}" '
                 f'fill="{self.c(fill)}" text-anchor="{anchor}"{ls} {extra}>{escape(s)}</text>')

    def lines(self, x, y, rows: list[str], lh: float, **kw) -> float:
        for i, r in enumerate(rows):
            self.text(x, y + i * lh, r, **kw)
        return y + (len(rows) - 1) * lh

    def card(self, x, y, w, h, accent=None, fill="bg") -> None:
        """Newsletter story box: hard offset shadow, optional accent shadow."""
        if accent:
            self.rect(x + 8, y + 8, w, h, fill="shadow", rx=3)
            self.rect(x + 3, y + 3, w, h, fill=accent, rx=3)
        else:
            self.rect(x + 5, y + 5, w, h, fill="shadow", rx=3)
        self.rect(x, y, w, h, fill=fill, stroke="strong", sw=1.2, rx=3)

    def kicker(self, x, y, no: str, topic: str, color: str, extra: str = "") -> float:
        """`NO.01  ■ TOPIC  extra` in mono caps. Returns x after the topic."""
        self.text(x, y, no, "m7", 11, "faint", tracking=0.07)
        x2 = x + measure(no, "m7", 11, 0.07) + 12
        self.rect(x2, y - 8.5, 8, 8, fill=color, rx=0)
        self.text(x2 + 14, y, topic, "m7", 11, color, tracking=0.07)
        x3 = x2 + 14 + measure(topic, "m7", 11, 0.07) + 12
        if extra:
            self.text(x3, y, extra, "m4", 11, "muted", tracking=0.07)
        return x3

    def stamp(self, cx, cy, label: str, color="pink", rot=-3) -> None:
        w = measure(label, "m7", 10.5, 0.12) + 16
        self.add(f'<g transform="rotate({rot} {cx} {cy})">')
        self.rect(cx - w / 2, cy - 11, w, 20, fill="none", stroke=color, sw=2, rx=1)
        self.text(cx, cy + 3.5, label, "m7", 10.5, color, anchor="middle", tracking=0.12)
        self.add("</g>")

    def grain(self) -> None:
        self.defs.append(
            '<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>'
            '<feColorMatrix values="0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 1 0"/></filter>')
        self.add(f'<rect width="100%" height="100%" filter="url(#grain)" opacity="{self.t["grain"]}"/>')

    # --- output -----------------------------------------------------------
    def render(self) -> str:
        faces = [_font_face(st, ch) for st, ch in self.chars.items() if ch]
        classes = [f".{k}{{font-family:{STYLES[k][1]},{FALLBACK[k]};font-weight:{STYLES[k][2]};"
                   f"font-style:{'italic' if STYLES[k][3] else 'normal'}}}" for k in self.chars]
        style = "".join(faces + classes + self.css)
        defs = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{escape(self.title)}">'
                f"<title>{escape(self.title)}</title><style>{style}</style>{defs}{''.join(self.body)}</svg>")

    def save(self, name: str) -> Path:
        OUT.mkdir(parents=True, exist_ok=True)
        p = OUT / f"{name}-{self.theme}.svg"
        p.write_text(self.render(), encoding="utf-8")
        return p
