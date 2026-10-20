"""Render wiki/*.md through GitHub's markdown API into .preview/wiki/, laid out like a wiki.

    .venv/bin/python scripts/wiki_preview.py && python3 -m http.server 8000
    open http://localhost:8000/.preview/wiki/Home.html

Images point at the local build instead of raw.githubusercontent, so unpushed changes show.
"""
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import unquote

from wiki import RAW, ROOT, WIKI

OUT = ROOT / ".preview" / "wiki"


def render(md: str) -> str:
    md = md.replace(RAW, "/assets/img/wiki")
    body = json.dumps({"text": md, "mode": "gfm", "context": "shubhamcodess/shubhamcodess"}).encode()
    req = urllib.request.Request("https://api.github.com/markdown", body,
                                 {"Accept": "application/vnd.github+json", "User-Agent": "wiki-preview"})
    html = urllib.request.urlopen(req).read().decode()
    # wiki links are bare page names; point them at the preview files
    return re.sub(r'href="(?!https?:|#|/)([^"]+)"', lambda m: f'href="{unquote(m.group(1))}.html"', html)


PAGE = """<!doctype html><html><head><meta charset=utf-8><title>{title}</title>
<meta name=viewport content="width=device-width,initial-scale=1">
<link rel=stylesheet href="https://cdn.jsdelivr.net/npm/github-markdown-css@5.8.1/github-markdown.min.css">
<style>body{{margin:0;background:#fff}}@media(prefers-color-scheme:dark){{body{{background:#0d1117}}}}
.wrap{{max-width:1280px;margin:24px auto;padding:0 24px;display:grid;grid-template-columns:minmax(0,1fr) 296px;gap:24px}}
h1.t{{grid-column:1/-1;margin:0;font:400 32px -apple-system,sans-serif;color:#1f2328}}
@media(prefers-color-scheme:dark){{h1.t{{color:#e6edf3}}}}
.box{{border:1px solid #d0d7de;border-radius:6px;padding:16px}}@media(prefers-color-scheme:dark){{.box{{border-color:#30363d}}}}
.foot{{grid-column:1}}@media(max-width:900px){{.wrap{{grid-template-columns:1fr}}}}</style>
</head><body><div class=wrap><h1 class=t>{title}</h1>
<article class="markdown-body">{main}</article>
<aside class="markdown-body box">{side}</aside>
<footer class="markdown-body box foot">{foot}</footer></div></body></html>"""

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    side = render((WIKI / "_Sidebar.md").read_text(encoding="utf-8"))
    foot = render((WIKI / "_Footer.md").read_text(encoding="utf-8"))
    for md in sorted(WIKI.glob("*.md")):
        if md.stem.startswith("_"):
            continue
        title = "Home" if md.stem == "Home" else md.stem.replace("-", " ").replace("   ", " — ")
        html = PAGE.format(title=title, main=render(md.read_text(encoding="utf-8")), side=side, foot=foot)
        (OUT / f"{md.stem}.html").write_text(html, encoding="utf-8")
        print("ok", md.stem)
