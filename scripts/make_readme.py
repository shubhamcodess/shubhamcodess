"""Write README.md from the built images. Keeps the current NEWS block if present.

Every <picture> is emitted on one line: GitHub's markdown parser splits a
multi-line <a><picture> apart, which drops the dark-mode <source>.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LI = "https://www.linkedin.com/in/shubham-prakash-dev/"
SITE = "https://shubhamcodess.github.io/everything-tech-newsletter/"
GH = "https://github.com/shubhamcodess"
RAW = "https://raw.githubusercontent.com/shubhamcodess/shubhamcodess/output"


def pic(name, alt, width="100%", dark=None, light=None):
    d = dark or f"assets/img/{name}-dark.svg"
    l = light or f"assets/img/{name}-light.svg"
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{d}">'
            f'<img alt="{alt}" src="{l}" width="{width}"></picture>')


def a(href, inner):
    return f'<a href="{href}">{inner}</a>' if href else inner


def block(*items):
    return "<p>" + "\n".join(items) + "</p>"


def section(key, title):
    return block(pic(f"section-{key}", title))


CARDS = [
    ("mcp-token-optimizer", "mcp-token-optimizer: a local proxy that strips noise from MCP tool responses"),
    ("career-os", "career-os: a job hunt that runs like a system, built on Claude Code skills"),
    ("lets-dsa", "lets-dsa: a DSA tutor that refuses to give you the answer"),
    ("focusify-yt", "focusify-yt: a Chrome extension that keeps YouTube on your study topic"),
]
BUTTONS = [
    ("linkedin", LI, "LinkedIn"),
    ("email", "mailto:prakashshubham36@gmail.com", "Email"),
    ("newsletter", SITE, "EverythingTech"),
    ("blog", None, "Blog, coming soon"),
]


def pair(x, y):
    return block(*(a(f"{GH}/{slug}", pic(f"card-{slug}", alt, "49%")) for slug, alt in (x, y)))


README = f"""<div align="center">

{block(pic("header", "Shubham Prakash. Building scalable systems with AI integrations at the core. Senior Full Stack Engineer, cloud native, AI-led engineering."))}

{block(*(a(h, pic(f"btn-{k}", alt, "190")) for k, h, alt in BUTTONS))}

</div>

{section("about", "The Lead")}

{block(a(LI, pic("about", "Six years shipping systems people depend on. Now building them AI-first. Senior Full Stack Engineer at IBM Consulting: I lead teams, architect Spring Boot backends and ship Angular and React front ends, and build the AI layer into them.")))}

{section("work", "Front Page")}

{block(a(SITE, pic("card-everythingtech", "EverythingTech: a daily tech newspaper with no human editor, written by a Claude Code routine from 47 sources")))}

{pair(CARDS[0], CARDS[1])}

{pair(CARDS[2], CARDS[3])}

{block(pic("card-private", "From the private desk: Cerebro, Landskape, Job Orchestrator and Orbit CI/CD"))}

{section("archive", "The Archive")}

{block(a(LI, pic("archive", "Career timeline at IBM Consulting from 2020 to now")))}

{section("stack", "The Stack")}

{block(pic("stack", "Tech stack: Java, TypeScript, Spring Boot, Angular, Next.js, MCP, Spring AI, Kubernetes and more"))}

{section("creds", "Credentials")}

{block(a(LI + "details/certifications/", pic("creds", "21 active credentials from Anthropic, Google Cloud, Microsoft, GitHub, IBM and Red Hat")))}

{section("today", "Today in EverythingTech")}

<!-- NEWS:START -->
<!-- NEWS:END -->

{section("activity", "On the Wire")}

{block(pic("stats", "GitHub activity: contributions, streaks and top languages"))}

{block(pic("snake", "Contribution graph being eaten by a snake", dark=f"{RAW}/snake-dark.svg", light=f"{RAW}/snake-light.svg"))}

{section("culture", "Off the Clock")}

{block(pic("culture", "Off the clock: photography and filmmaking"))}

{block(a(LI, pic("footer", "Let's build something. Say hi on LinkedIn or email prakashshubham36@gmail.com")))}
"""

if __name__ == "__main__":
    path = ROOT / "README.md"
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    news = re.search(r"<!-- NEWS:START -->.*?<!-- NEWS:END -->", old, re.S)
    text = README.replace("<!-- NEWS:START -->\n<!-- NEWS:END -->", news.group(0)) if news else README
    path.write_text(text, encoding="utf-8")
    print("README.md written")
