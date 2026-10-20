[← Profile README](Profile-README) · [Home](Home)

# Run locally

> At the end you'll have every README and wiki image rebuilt on your machine and a local preview of both pages.

## Prerequisites

| Tool | Version | Check |
|---|---|---|
| Python | 3.12+ | `python3 --version` |
| Git | any | `git --version` |

No API keys. The only network calls are public: the newsletter feed, the GitHub REST API and GitHub's Markdown renderer for previews.

## Setup

```bash
git clone https://github.com/shubhamcodess/shubhamcodess.git
cd shubhamcodess
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

`requirements.txt` is just `fonttools` and `brotli`: everything is drawn by hand-written Python, and fontTools subsets the fonts into each SVG.

## Build the profile

```bash
.venv/bin/python scripts/build.py          # every static README image, dark and light
.venv/bin/python scripts/make_readme.py    # README.md from those images
.venv/bin/python scripts/update_dynamic.py # today's headlines and the stats card
```

Swap the header logo for one build without editing anything:

```bash
.venv/bin/python scripts/build.py --logo s
```

## Build the wiki

```bash
.venv/bin/python scripts/wiki.py
```

This writes the images to `assets/img/wiki/` and the generated pages (`Home`, `_Sidebar`, `_Footer` and one page per project) to `wiki/`. Hand-written docs like this one are left alone.

## Preview

```bash
mkdir -p .preview
.venv/bin/python scripts/preview.py        # README → .preview/index.html
.venv/bin/python scripts/wiki_preview.py   # wiki  → .preview/wiki/
python3 -m http.server 8000                # then open localhost:8000/.preview/wiki/Home.html
```

Both previews render through GitHub's own Markdown API, so what you see is what GitHub will show. The API allows 60 unauthenticated calls an hour.

## Troubleshooting

<details><summary>Fonts look like Arial or Georgia</summary>

The SVG was opened in a context that blocks `data:` fonts. Open it through the preview server, not straight from disk in an image viewer.

</details>

<details><summary>The wiki on GitHub shows old images</summary>

GitHub caches images through its proxy. `scripts/wiki.py` adds a `?v=` content hash to every image URL, so a rebuild and push gives each changed image a new URL.

</details>
