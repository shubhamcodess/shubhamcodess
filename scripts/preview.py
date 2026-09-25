"""Render README.md through GitHub's markdown API into .preview/index.html."""
import json, urllib.request
from pathlib import Path
body = json.dumps({"text": Path("README.md").read_text(), "mode": "gfm", "context": "shubhamcodess/shubhamcodess"}).encode()
req = urllib.request.Request("https://api.github.com/markdown", body, {"Accept": "application/vnd.github+json", "User-Agent": "preview"})
html = urllib.request.urlopen(req).read().decode()
Path(".preview/index.html").write_text(f"""<!doctype html><html><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<link rel=stylesheet href="https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown.min.css">
<style>body{{margin:0;background:#fff}}@media(prefers-color-scheme:dark){{body{{background:#0d1117}}}}
.markdown-body{{box-sizing:border-box;max-width:880px;margin:24px auto;padding:24px;border:1px solid #30363d;border-radius:6px}}</style>
</head><body><article class=markdown-body>{html}</article></body></html>""")
print("ok")
