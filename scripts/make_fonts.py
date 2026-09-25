"""One-off: pin the variable Google Fonts to the static styles the SVGs use.

Sources come from github.com/google/fonts (OFL). Output: assets/fonts/*.woff2,
which build.py then subsets per SVG so each image only carries its own glyphs.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

SRC = Path(".fontsrc")
OUT = Path("assets/fonts")

STYLES = {
    "display-800": ("bricolage.ttf", {"wght": 800, "opsz": 96, "wdth": 100}),
    "display-700": ("bricolage.ttf", {"wght": 700, "opsz": 24, "wdth": 100}),
    "serif-italic": ("newsreader-italic.ttf", {"wght": 450, "opsz": 16}),
    "mono-400": ("jbmono.ttf", {"wght": 400}),
    "mono-700": ("jbmono.ttf", {"wght": 700}),
}

for name, (src, axes) in STYLES.items():
    font = instantiateVariableFont(TTFont(SRC / src), axes, updateFontNames=False)
    font.flavor = "woff2"
    font.save(OUT / f"{name}.woff2")
    print(name, (OUT / f"{name}.woff2").stat().st_size // 1024, "KB")
