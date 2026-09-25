"""Refresh the parts of the README that change: newsletter headlines and the stats card.

Runs daily from .github/workflows/refresh.yml. Uses only public endpoints;
GITHUB_TOKEN (if set) just raises the REST rate limit.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import urllib.request
from collections import Counter
from pathlib import Path

from svgkit import SVG, measure

USER = "shubhamcodess"
SITE = "https://shubhamcodess.github.io/everything-tech-newsletter/"
README = Path(__file__).resolve().parent.parent / "README.md"
W = 840
LANG_COLORS = ["lime", "cyan", "violet", "pink", "amber", "coral"]


def get(url: str, api: bool = False) -> bytes:
    headers = {"User-Agent": f"{USER}-readme"}
    if api and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return r.read()


def replace_block(text: str, tag: str, body: str) -> str:
    pattern = re.compile(rf"(<!-- {tag}:START -->).*?(<!-- {tag}:END -->)", re.S)
    return pattern.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(2)}", text)


# --------------------------------------------------------------------------- headlines

def short(text: str, limit: int = 150) -> str:
    """First sentence, cut on a word boundary if it's still long."""
    first = re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0]
    if len(first) <= limit:
        return first
    return first[:limit].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"


def headlines(n: int = 3) -> str:
    ed = json.loads(get(SITE + "latest.json"))
    stories = ed["stories"]
    # must-reads first, keeping the editor's order otherwise
    ranked = sorted(range(len(stories)), key=lambda i: (stories[i].get("signal") != "must-read", i))[:n]
    rows = []
    for i in ranked:
        s = stories[i]
        rows.append(f"- **[{s['headline']}]({SITE}#s-{i + 1})** &nbsp;<sub>`{s['topic'].upper()}`</sub>  \n"
                    f"  <sub><i>{short(s['dek'])}</i></sub>")
    date = dt.date.fromisoformat(ed["date"]).strftime("%a %d %b %Y")
    rows.append(f"\n<sub>Edition of {date} · {len(stories)} stories · "
                f"<a href=\"{SITE}\">read the full paper ↗</a></sub>")
    return "\n".join(rows)


# --------------------------------------------------------------------------- stats

def contributions() -> dict:
    html = get(f"https://github.com/users/{USER}/contributions").decode()
    dates = dict(re.findall(r'data-date="([\d-]+)" id="(contribution-day-component-[\d-]+)"', html))
    dates = {v: k for k, v in dates.items()}
    counts = {}
    for cid, tip in re.findall(r'for="(contribution-day-component-[\d-]+)"[^>]*>([^<]*)</tool-tip>', html):
        m = re.match(r"(\d+) contribution", tip)
        counts[dates[cid]] = int(m.group(1)) if m else 0
    days = sorted(counts)
    total = sum(counts.values())
    longest = run = 0
    for d in days:
        run = run + 1 if counts[d] else 0
        longest = max(longest, run)
    current = 0
    for i, d in enumerate(reversed(days)):
        if counts[d]:
            current += 1
        elif i:  # today may still be empty
            break
    month = sum(counts[d] for d in days[-30:])
    return {"total": total, "current": current, "longest": longest, "month": month}


def repos() -> dict:
    data = json.loads(get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner", api=True))
    own = [r for r in data if not r["fork"]]
    langs = Counter()
    for r in own:
        if r["name"] == USER:
            continue
        for lang, size in json.loads(get(r["languages_url"], api=True)).items():
            langs[lang] += size
    return {"repos": len(own), "stars": sum(r["stargazers_count"] for r in own), "langs": langs}


def stats_card(theme: str, c: dict, r: dict) -> None:
    H = 196
    s = SVG(W + 10, H + 10, theme,
            f"{c['total']} contributions in the last year, {c['month']} in the last 30 days, "
            f"longest streak {c['longest']} days, {r['repos']} public repos.")
    s.card(0, 0, W - 2, H)
    s.kicker(26, 36, "LIVE", "GITHUB", "lime", f"UPDATED {dt.date.today():%d %b %Y}".upper())

    figures = [(f"{c['total']:,}", "CONTRIBUTIONS", "PAST 12 MONTHS"),
               (f"{c['month']:,}", "LAST 30 DAYS", f"LONGEST STREAK {c['longest']}"),
               (str(r["repos"]), "PUBLIC REPOS", f"{r['stars']} STARS" if r["stars"] >= 10 else "ORIGINAL, NOT FORKS")]
    for i, (big, label, sub) in enumerate(figures):
        x = 26 + i * 150
        if i:
            s.line(x - 16, 62, x - 16, H - 26, "line", dash="3 4")
        s.text(x, 112, big, "d8", 42, ["lime", "pink", "cyan"][i], tracking=-0.03)
        s.text(x, 140, label, "m7", 11, "ink", tracking=0.08)
        s.text(x, 160, sub, "m4", 10.5, "muted", tracking=0.08)

    # language bar
    x0, x1 = 26 + 3 * 150 + 4, W - 28
    s.line(x0 - 20, 62, x0 - 20, H - 26, "line", dash="3 4")
    s.text(x0, 76, "LANGUAGES · BY BYTES", "m7", 11, "faint", tracking=0.08)
    top = r["langs"].most_common(6)
    total = sum(v for _, v in top) or 1
    x = x0
    bar_w = x1 - x0
    for i, (lang, v) in enumerate(top):
        w = bar_w * v / total
        s.rect(x, 88, max(w - 2, 1), 12, fill=LANG_COLORS[i], rx=0)
        x += w
    for i, (lang, v) in enumerate(top):
        cx, cy = x0 + (i % 2) * (bar_w / 2), 126 + (i // 2) * 22
        s.rect(cx, cy - 8.5, 8, 8, fill=LANG_COLORS[i], rx=0)
        s.text(cx + 14, cy, lang, "m4", 12, "ink", tracking=0.02)
        s.text(cx + 14 + measure(lang, "m4", 12, 0.02) + 8, cy, f"{100 * v / total:.0f}%", "m4", 12, "muted")
    s.save("stats")


if __name__ == "__main__":
    text = README.read_text(encoding="utf-8")
    try:
        text = replace_block(text, "NEWS", headlines())
    except Exception as e:  # keep yesterday's headlines rather than fail the run
        print("headlines skipped:", e)
    README.write_text(text, encoding="utf-8")

    try:
        c, r = contributions(), repos()
    except Exception as e:  # keep the last card rather than fail the run
        print("stats skipped:", e)
    else:
        for theme in ("dark", "light"):
            stats_card(theme, c, r)
        print("refreshed", c, r["repos"], dict(r["langs"].most_common(6)))
