"""Render every static README image, in dark and light.

    .venv/bin/python scripts/build.py

Content lives in the dicts below; layout lives in the functions. Facts come from
career-os/data/master-experience.md — edit there first, then here.
"""
from __future__ import annotations

from svgkit import SVG, measure, wrap

W = 840
HALF = 410  # two cards per row, 20px gutter

# --------------------------------------------------------------------------- content

# Header logo: "batman" (pulsing bat signal) or "s" (spinning pixel S).
# Swap for one build without editing: .venv/bin/python scripts/build.py --logo s
LOGO = "batman"

NAME = "Shubham Prakash"
TAGLINE = "Building scalable systems with AI integrations at the core."
ROLES = ["SENIOR FULL STACK ENGINEER", "CLOUD NATIVE", "AGENTIC AI"]
TICKER = [
    ("lime", "JAVA 21"), ("cyan", "SPRING BOOT"), ("violet", "MCP SERVERS"), ("pink", "AGENTIC PIPELINES"),
    ("amber", "NEXT.JS 16"), ("coral", "ANGULAR"), ("blue", "KUBERNETES · GKE"), ("mint", "RABBITMQ"),
    ("lime", "POSTGRESQL"), ("cyan", "NEO4J"), ("violet", "SPRING AI"), ("pink", "VERCEL AI SDK"),
    ("amber", "LANGGRAPH"), ("coral", "GITHUB ACTIONS"), ("blue", "HELM"), ("mint", "OLLAMA"),
]

ABOUT = {
    "headline": ["Six years shipping systems people depend on.", "Now building them AI-first."],
    "dek": ("Senior Full Stack Engineer at IBM Consulting. I lead teams, architect Spring Boot "
            "backends and ship Angular and React front ends for enterprise platforms, and I build "
            "the AI layer into them: agentic delivery pipelines, MCP servers and tools where the "
            "model is part of the architecture, not a plugin."),
    "desk": [
        ("lime", "NOW", "Team lead and shadow architect on an order-finance platform"),
        ("cyan", "BUILDING", "MCP tooling, agent pipelines, code-graph intelligence"),
        ("violet", "EXPLORING", "Distributed systems at consumer scale"),
    ],
}

LEAD = {
    "no": "NO.01", "topic": "AI · AUTOMATION", "extra": "PYTHON", "color": "lime",
    "name": "EverythingTech",
    "headline": "A daily tech newspaper with no human editor",
    "dek": ("Python pulls 47 free sources and clusters duplicate coverage. A scheduled Claude Code "
            "routine picks, ranks and writes each story from the full article, and GitHub Pages "
            "serves it. No server, no database, no API key."),
    "stats": [("47", "SOURCES"), ("1", "EDITION A DAY"), ("0", "API KEYS")],
    "stack": "Python · Claude Code routines · GitHub Actions · Pages",
    "cta": "READ TODAY'S EDITION ↗",
}

CARDS = [
    {"no": "NO.02", "topic": "AI INFRA", "extra": "TYPESCRIPT", "color": "cyan", "slug": "mcp-token-optimizer",
     "name": "mcp-token-optimizer",
     "dek": ("A local proxy between your AI agent and its MCP servers that strips the noise from "
             "every tool response. Lossless first, fail-open, zero telemetry."),
     "stat": "UP TO 98% FEWER TOKENS", "stack": "TypeScript · Node · MCP · Ollama · TOON"},
    {"no": "NO.03", "topic": "AGENTS", "extra": "CLAUDE CODE", "color": "violet", "slug": "career-os",
     "name": "career-os",
     "dek": ("A job hunt that runs like a system: Claude Code skills that pull live openings every "
             "morning, tailor each resume and remember every decision."),
     "stat": "22 SKILLS · 11 ATS PLATFORMS", "stack": "Claude Code · Python · Markdown + JSON"},
    {"no": "NO.04", "topic": "LEARNING", "extra": "CLAUDE CODE", "color": "pink", "slug": "lets-dsa",
     "name": "lets-dsa",
     "dek": ("A DSA tutor that refuses to give you the answer. Learn the pattern, derive the "
             "approach, solve it yourself. Five hints, then it stops helping."),
     "stat": "428 PROBLEMS · 20 PATTERNS", "stack": "Claude Code · Python · MCP guardrails"},
    {"no": "NO.05", "topic": "TOOLS", "extra": "JAVASCRIPT", "color": "amber", "slug": "focusify-yt",
     "name": "focusify-yt",
     "dek": ("A Chrome extension that keeps YouTube on your study topic and hides everything else. "
             "Optional local AI, no accounts, no tracking."),
     "stat": "MANIFEST V3 · LOCAL LLM", "stack": "JavaScript · Chrome MV3 · Ollama"},
]

PRIVATE = [
    ("violet", "Cerebro", "Parses Java/Spring repos into a typed code graph and exposes it to AI agents as 41 MCP tools.",
     "Java 21 · Neo4j · Spring AI"),
    ("cyan", "Landskape", "Browser control plane for a GKE fleet, with an embedded AI copilot and its own MCP server.",
     "Next.js 16 · Vercel AI SDK · MCP"),
    ("amber", "Job Orchestrator", "Airflow-style DAG workflow engine: 17 modules, virtual threads, live run monitoring.",
     "Java 21 · RabbitMQ · Quartz"),
    ("lime", "Orbit CI/CD", "Reusable GitHub Actions framework with auto-semver and gated promotions, running across 10+ repos.",
     "GitHub Actions · Helm · GitOps"),
]

ARCHIVE = [
    ("lime", "2020", "Associate System Engineer", "Ran a mission-critical tax engine through two platform migrations."),
    ("cyan", "2021", "Full Stack Developer", "Built the front end of the pilot that launched an open-source migration program."),
    ("violet", "2022", "Tech Lead", "Owned architecture and estimates; made a 10k-row search instant."),
    ("pink", "2023", "Tech Lead", "Set up CI/CD and standards, then shipped the program's first SSO."),
    ("amber", "2024", "Team Lead", "Cut a 20-minute data compile to seconds; delivered a month early."),
    ("coral", "2025", "Senior Dev · Shadow Architect", "Designed the execution framework; batch jobs up to 55% faster."),
]

STACK = [
    ("lime", "LANGUAGES", ["Java 21", "TypeScript", "JavaScript", "Python", "SQL", "Bash"]),
    ("cyan", "BACKEND", ["Spring Boot", "Spring Cloud", "Node.js", "RabbitMQ", "Quartz", "Resilience4j"]),
    ("violet", "FRONTEND", ["Angular", "React 19", "Next.js 16", "Tailwind v4", "shadcn/ui"]),
    ("pink", "AI & AGENTS", ["MCP (client + server)", "Spring AI", "Vercel AI SDK", "LangGraph", "LangChain", "Ollama", "watsonx"]),
    ("amber", "DATA", ["PostgreSQL", "Oracle", "Neo4j", "Liquibase"]),
    ("blue", "CLOUD & OPS", ["GKE", "Kubernetes", "Helm", "Docker", "OpenShift", "Azure AD", "GitHub Actions", "JFrog"]),
    ("coral", "OBSERVABILITY", ["Prometheus", "Grafana", "Loki", "LangSmith"]),
]

CREDS = [
    ("coral", "ANTHROPIC", 5, ["Claude Certified Architect, Professional", "Architect, Foundations",
                              "Developer, Foundations", "Associate, Foundations", "Claude Code Partner"]),
    ("blue", "GOOGLE CLOUD", 3, ["Associate Cloud Engineer", "Generative AI Leader", "Cloud Digital Leader"]),
    ("cyan", "MICROSOFT", 2, ["Azure Developer Associate", "Azure Fundamentals"]),
    ("violet", "GITHUB", 2, ["GitHub Actions", "GitHub Copilot"]),
    ("pink", "IBM · RED HAT", 9, ["Generative & Agentic AI", "watsonx.ai Technical Essentials",
                                 "OpenShift Applications (DO101)", "+ 6 more"]),
]

CULTURE = {
    "headline": "Behind a lens when I'm not behind a terminal.",
    "dek": ("Photography and filmmaking: framing, light, and knowing what to cut in the edit. "
            "It's the same instinct I bring to building products: decide what to leave out."),
}

SECTIONS = {
    "about": ("01 /", "The Lead", "WHO'S WRITING"),
    "work": ("02 /", "Front Page", "SHIPPED IN PUBLIC"),
    "archive": ("03 /", "The Archive", "IBM CONSULTING · 2020 → NOW"),
    "stack": ("04 /", "The Stack", "TOOLS OF THE TRADE"),
    "creds": ("05 /", "Credentials", "21 ACTIVE"),
    "today": ("06 /", "Today in EverythingTech", "UPDATED DAILY"),
    "activity": ("07 /", "On the Wire", "GITHUB ACTIVITY"),
    "culture": ("08 /", "Off the Clock", "CULTURE DESK"),
}

CONNECT = [
    ("linkedin", "cyan", "LINKEDIN"),
    ("email", "lime", "EMAIL"),
    ("newsletter", "pink", "EVERYTHINGTECH"),
    ("blog", "faint", "BLOG · SOON"),
]


# --------------------------------------------------------------------------- pieces

def chip(s: SVG, x: float, y: float, px: float) -> None:
    """The EverythingTech pixel chip, with a blinking core."""
    pins = [(2, 0, 1, 2), (5, 0, 1, 2), (2, 6, 1, 2), (5, 6, 1, 2), (0, 2, 2, 1), (0, 5, 2, 1), (6, 2, 2, 1), (6, 5, 2, 1)]
    s.add('<g shape-rendering="crispEdges">')
    for a, b, w, h in pins:
        s.add(f'<rect x="{x + a * px}" y="{y + b * px}" width="{w * px}" height="{h * px}" fill="{s.c("pink")}"/>')
    s.add(f'<rect x="{x + 2 * px}" y="{y + 2 * px}" width="{4 * px}" height="{4 * px}" fill="{s.c("cyan")}"/>')
    s.add(f'<rect class="core" x="{x + 3 * px}" y="{y + 3 * px}" width="{2 * px}" height="{2 * px}" fill="{s.c("lime")}"/>')
    s.add("</g>")


S_PIXELS = [  # 8x8
    ".######.",
    "##....##",
    "##......",
    ".######.",
    "......##",
    "......##",
    "##....##",
    ".######.",
]

BAT_PIXELS = [  # 27x12, Dark Knight-style silhouette
    "#####.......#.#.......#####",
    ".######....#####....######.",
    "..#######..#####..#######..",
    "...#####################...",
    "...#####################...",
    "....###################....",
    ".....#################.....",
    "........###########........",
    ".........#########.........",
    "...........#####...........",
    "............###............",
    ".............#.............",
]


def _pixels(s: SVG, rows, x, y, px, fill) -> None:
    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            if cell == "#":
                s.add(f'<rect x="{x + c * px}" y="{y + r * px}" width="{px}" height="{px}" fill="{fill(r)}"/>')


def logo_s(s: SVG, x: float, cy: float) -> float:
    """Pixel-art S spinning counterclockwise; rows shade pink → cyan → lime. Returns width."""
    px = 5
    shades = ["pink", "pink", "pink", "cyan", "cyan", "lime", "lime", "lime"]
    s.css.append("@keyframes spin{to{transform:rotate(-360deg)}}"
                 ".spin{transform-box:fill-box;transform-origin:center;animation:spin 6s linear infinite}")
    s.add('<g class="spin" shape-rendering="crispEdges">')
    _pixels(s, S_PIXELS, x, cy - 4 * px, px, lambda r: s.c(shades[r]))
    s.add("</g>")
    return 8 * px


def logo_batman(s: SVG, x: float, cy: float) -> float:
    """Pixel bat with a hard, boxy offset shadow (like the cards), gently pulsing. Returns width."""
    px, cols, rows = 2.6, len(BAT_PIXELS[0]), len(BAT_PIXELS)
    y, off = cy - rows * px / 2 + 3, 3  # +3: the thin tail makes the box look high
    s.css.append("@keyframes beat{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}"
                 ".beat{transform-box:fill-box;transform-origin:center;animation:beat 1.8s ease-in-out infinite}")
    s.add('<g class="beat" shape-rendering="crispEdges">')
    _pixels(s, BAT_PIXELS, x + off, y + off, px, lambda r: "#d99a00")  # gold boxy shadow
    _pixels(s, BAT_PIXELS, x, y, px, lambda r: "#2b303b" if s.theme == "dark" else "#1a1c23")  # charcoal reads on the dark header
    s.add("</g>")
    return cols * px + off


LOGOS = {"s": logo_s, "batman": logo_batman}


def header(theme: str) -> None:
    H = 318
    s = SVG(W, H, theme, f"{NAME}. {TAGLINE}")
    s.css.append("@keyframes blink{50%{opacity:0}}.core{animation:blink 1.6s steps(1) infinite}"
                 ".cursor{animation:blink 1.1s steps(1) infinite}")
    s.rect(0.5, 0.5, W - 1, H - 1, fill="bg", stroke="strong", rx=4)
    s.grain()

    # dateline
    y = 34
    s.text(28, y, "BANGALORE, IN", "m4", 11, "muted", tracking=0.08)
    s.text(W / 2, y, "BUILDING SINCE 2020", "m4", 11, "muted", anchor="middle", tracking=0.08)
    s.text(W - 28, y, "GITHUB.COM/SHUBHAMCODESS", "m4", 11, "muted", anchor="end", tracking=0.08)
    s.line(28, 48, W - 28, 48, "line")

    # nameplate: chip + name + cursor, centred as one group
    size = 78
    name_w = measure(NAME, "d8", size, -0.035)
    cursor_w = measure("_", "d8", size)
    draw = LOGOS[LOGO]
    logo_w = draw(SVG(1, 1, theme, ""), 0, 0)
    x0 = (W - (logo_w + 22 + name_w + cursor_w)) / 2
    draw(s, x0, 116)  # 116 = middle of the name's cap height
    s.text(x0 + logo_w + 22, 144, NAME, "d8", size, "ink", tracking=-0.035)
    s.text(x0 + logo_w + 22 + name_w + 2, 144, "_", "d8", size, "pink", cls="cursor")

    s.text(W / 2, 194, TAGLINE, "si", 22, "ink2", anchor="middle")

    # roles, separated by coloured squares
    gap, sq = 14, 7
    parts = [measure(r, "m7", 11.5, 0.12) for r in ROLES]
    total = sum(parts) + (len(ROLES) - 1) * (gap * 2 + sq)
    x = (W - total) / 2
    for i, (r, w) in enumerate(zip(ROLES, parts)):
        s.text(x, 232, r, "m7", 11.5, "ink2", tracking=0.12)
        x += w
        if i < len(ROLES) - 1:
            s.rect(x + gap, 232 - 8.5, sq, sq, fill=["lime", "cyan"][i], rx=0)
            x += gap * 2 + sq

    # ticker band
    ty = 262
    s.rect(1, ty, W - 2, 34, fill="bg2")
    s.line(1, ty, W - 1, ty, "line")
    s.line(1, ty + 34, W - 1, ty + 34, "line")
    seq, x = [], 0.0
    for color, label in TICKER:
        seq.append((x, color, label))
        x += 8 + 10 + measure(label, "m4", 12, 0.06) + 26
    seq_w = x
    s.css.append(f"@keyframes tick{{to{{transform:translateX(-{seq_w:.1f}px)}}}}"
                 f".tick{{animation:tick {seq_w / 38:.1f}s linear infinite}}")
    s.defs.append(f'<clipPath id="band"><rect x="1" y="{ty}" width="{W - 2}" height="34"/></clipPath>')
    s.add(f'<g clip-path="url(#band)"><g class="tick">')
    for rep in (0, seq_w, 2 * seq_w):
        for x, color, label in seq:
            s.rect(20 + rep + x, ty + 13, 8, 8, fill=color, rx=0)
            s.text(20 + rep + x + 18, ty + 21.5, label, "m4", 12, "ink2", tracking=0.06)
    s.add("</g></g>")
    s.save("header")


def section(key: str, theme: str) -> None:
    no, title, note = SECTIONS[key]
    s = SVG(W, 70, theme, title)
    s.line(0, 10, W, 10, "strong", sw=3)
    s.line(0, 15, W, 15, "strong", sw=1)
    s.text(0, 52, no, "m7", 12, "pink", tracking=0.08)
    s.text(measure(no, "m7", 12, 0.08) + 14, 53, title, "d7", 28, "ink", tracking=-0.02)
    s.text(W, 52, note, "m4", 11, "muted", anchor="end", tracking=0.08)
    s.save(f"section-{key}")


def about(theme: str) -> None:
    left_w = 540
    head = [r for h in ABOUT["headline"] for r in wrap(h, "d7", 25, left_w, -0.02)]
    dek = wrap(ABOUT["dek"], "si", 16.5, left_w)
    x_desk = 26 + left_w + 30
    desk = [wrap(text, "si", 14.5, W - x_desk - 30) for *_, text in ABOUT["desk"]]
    H = max(96 + len(head) * 32 + len(dek) * 25 + 20, 94 + sum(22 + len(r) * 20 + 18 for r in desk) + 4)
    s = SVG(W + 10, H + 10, theme, " ".join(ABOUT["headline"]) + " " + ABOUT["dek"])
    s.card(0, 0, W - 2, H, accent="lime")
    s.kicker(26, 38, "NO.00", "PROFILE", "lime", "6 YRS · IBM CONSULTING")
    y = s.lines(26, 82, head, 32, style="d7", size=25, fill="ink", tracking=-0.02)
    s.lines(26, y + 38, dek, 25, style="si", size=16.5, fill="ink2")

    # "on the desk" column
    x = x_desk
    s.line(x - 16, 60, x - 16, H - 24, "line", dash="3 4")
    s.text(x, 82 - 18, "ON THE DESK", "m7", 11, "faint", tracking=0.1)
    y = 82 + 12
    for (color, label, _), rows in zip(ABOUT["desk"], desk):
        s.rect(x, y - 8.5, 8, 8, fill=color, rx=0)
        s.text(x + 14, y, label, "m7", 11, color, tracking=0.08)
        s.lines(x, y + 22, rows, 20, style="si", size=14.5, fill="ink")
        y += 22 + len(rows) * 20 + 18
    s.save("about")


def lead_card(theme: str) -> None:
    c = LEAD
    text_w = 520
    head = wrap(c["headline"], "d7", 27, text_w, -0.02)
    dek = wrap(c["dek"], "si", 16, text_w)
    H = 70 + 34 + len(head) * 32 + 14 + len(dek) * 24 + 70
    s = SVG(W + 10, H + 10, theme, f"{c['name']}: {c['headline']}. {c['dek']}")
    s.card(0, 0, W - 2, H, accent=c["color"])
    s.kicker(26, 38, c["no"], c["topic"], c["color"], c["extra"])
    s.stamp(W - 90, 33, "LIVE DAILY", "pink")
    s.text(26, 84, c["name"], "m7", 13, c["color"], tracking=0.04)
    y = s.lines(26, 84 + 34, head, 32, style="d7", size=27, fill="ink", tracking=-0.02)
    s.lines(26, y + 34, dek, 24, style="si", size=16, fill="ink2")

    # stat column
    x = 26 + text_w + 40
    s.line(x - 20, 64, x - 20, H - 70, "line", dash="3 4")
    y = 100
    for big, small in c["stats"]:
        s.text(x, y, big, "d8", 34, c["color"], tracking=-0.02)
        s.text(x + measure(big, "d8", 34, -0.02) + 12, y - 4, small, "m7", 11, "muted", tracking=0.08)
        y += 52

    # byline
    s.line(26, H - 44, W - 28, H - 44, "line", dash="3 3")
    s.text(26, H - 20, c["stack"], "m4", 11.5, "muted", tracking=0.04)
    s.text(W - 28, H - 20, c["cta"], "m7", 11.5, c["color"], anchor="end", tracking=0.08)
    s.save("card-everythingtech")


def small_cards(theme: str) -> None:
    inner = HALF - 52
    # rows of two share a height
    for pair in (CARDS[0:2], CARDS[2:4]):
        deks = [wrap(c["dek"], "si", 15, inner) for c in pair]
        H = 84 + 20 + max(len(d) for d in deks) * 22 + 94
        for c, dek in zip(pair, deks):
            s = SVG(HALF + 10, H + 10, theme, f"{c['name']}: {c['dek']}")
            s.card(0, 0, HALF - 2, H, accent=c["color"])
            s.kicker(24, 36, c["no"], c["topic"], c["color"], c["extra"])
            s.text(24, 76, c["name"], "d7", 23, "ink", tracking=-0.02)
            s.lines(24, 76 + 30, dek, 22, style="si", size=15, fill="ink2")
            s.text(24, H - 64, c["stat"], "m7", 11.5, c["color"], tracking=0.08)
            s.line(24, H - 46, HALF - 26, H - 46, "line", dash="3 3")
            s.text(24, H - 22, c["stack"], "m4", 11, "muted", tracking=0.03)
            s.text(HALF - 26, H - 22, "↗", "m7", 13, c["color"], anchor="end")
            s.save(f"card-{c['slug']}")


def private_desk(theme: str) -> None:
    cols = len(PRIVATE)
    colw = (W - 52 - (cols - 1) * 24) / cols
    descs = [wrap(d, "si", 14, colw) for _, _, d, _ in PRIVATE]
    stacks = [wrap(st, "m4", 10.5, colw, 0.03) for *_, st in PRIVATE]
    H = 92 + max(len(d) for d in descs) * 20 + 22 + max(len(t) for t in stacks) * 15 + 26
    s = SVG(W + 10, H + 10, theme, "From the private desk: " + "; ".join(f"{n}: {d}" for _, n, d, _ in PRIVATE))
    s.card(0, 0, W - 2, H)
    s.text(26, 36, "FROM THE PRIVATE DESK", "m7", 11, "faint", tracking=0.1)
    s.text(26 + measure("FROM THE PRIVATE DESK", "m7", 11, 0.1) + 12, 36,
           "SOLO BUILDS · SOURCE NOT PUBLIC", "m4", 11, "muted", tracking=0.08)
    s.stamp(W - 84, 31, "PRIVATE", "violet", rot=3)
    for i, ((color, name, _, _), desc, stack) in enumerate(zip(PRIVATE, descs, stacks)):
        x = 26 + i * (colw + 24)
        if i:
            s.line(x - 12, 60, x - 12, H - 20, "line", dash="3 4")
        s.rect(x, 80, 9, 9, fill=color, rx=0)
        s.text(x + 17, 89, name, "d7", 18, "ink", tracking=-0.01)
        y = s.lines(x, 114, desc, 20, style="si", size=14, fill="ink2")
        s.lines(x, y + 26, stack, 15, style="m4", size=10.5, fill=color, tracking=0.03)
    s.save("card-private")


def archive(theme: str) -> None:
    n = len(ARCHIVE)
    colw = (W - 52) / n
    roles = [wrap(r, "d7", 15, colw - 14) for _, _, r, _ in ARCHIVE]
    notes = [wrap(t, "si", 13, colw - 14) for *_, t in ARCHIVE]
    rh = max(len(r) for r in roles) * 19
    H = 138 + rh + 8 + max(len(t) for t in notes) * 18 + 24
    s = SVG(W + 10, H + 10, theme, "Career timeline at IBM Consulting, 2020 to now. "
            + " ".join(f"{y}: {r}, {t}" for _, y, r, t in ARCHIVE))
    s.css.append("@keyframes pulse{0%{r:6;opacity:.9}100%{r:18;opacity:0}}.pulse{animation:pulse 1.8s ease-out infinite}")
    s.card(0, 0, W - 2, H)
    s.kicker(26, 36, "IBM CONSULTING", "OCT 2020 — PRESENT", "cyan", "ENTERPRISE PLATFORMS · GLOBAL RETAIL")
    track = 96
    s.line(26, track, W - 28, track, "strong", sw=2)
    for i, ((color, year, _, _), role, note) in enumerate(zip(ARCHIVE, roles, notes)):
        x = 26 + i * colw
        s.text(x, track - 16, year, "m7", 13, color, tracking=0.06)
        if i == n - 1:
            s.add(f'<circle class="pulse" cx="{x + 5}" cy="{track}" r="6" fill="{s.c(color)}"/>')
            # "NOW" badge pinned to the card's right edge, clear of the year
            bw = measure("NOW", "m7", 10, 0.12) + 14
            bx = W - 28 - bw
            s.rect(bx, track - 29, bw, 18, fill="none", stroke="pink", sw=1.5, rx=2)
            s.text(bx + bw / 2, track - 16.5, "NOW", "m7", 10, "pink", anchor="middle", tracking=0.12, cls="blink")
        s.rect(x, track - 5, 10, 10, fill=color, rx=0)
        s.lines(x, 132, role, 19, style="d7", size=15, fill="ink", tracking=-0.01)
        s.lines(x, 132 + rh + 8, note, 18, style="si", size=13, fill="ink2")
    s.css.append("@keyframes bl{50%{opacity:0}}.blink{animation:bl 1.1s steps(1) infinite}")
    s.save("archive")


def stack(theme: str) -> None:
    label_w, x0, right = 150, 26, W - 28
    chip_h, gap, row_gap = 28, 8, 10
    # lay out first to find the height
    rows, y = [], 34
    for color, label, items in STACK:
        x, first_y = x0 + label_w, y
        placed = []
        for it in items:
            w = measure(it, "m4", 12, 0.02) + 34
            if x + w > right:
                x, y = x0 + label_w, y + chip_h + gap
            placed.append((x, y, w, it))
            x += w + gap
        rows.append((color, label, first_y, placed))
        y += chip_h + row_gap + 8
    H = y + 12
    s = SVG(W + 10, H + 10, theme, "Tech stack. " + " ".join(f"{l}: {', '.join(i)}." for _, l, i in STACK))
    s.card(0, 0, W - 2, H)
    for i, (color, label, fy, placed) in enumerate(rows):
        if i:
            s.line(x0, fy - 9, right, fy - 9, "line", dash="2 4")
        s.rect(x0, fy + 10, 8, 8, fill=color, rx=0)
        s.text(x0 + 16, fy + 18.5, label, "m7", 11, color, tracking=0.08)
        for x, y, w, it in placed:
            s.rect(x, y, w, chip_h, fill="surface", stroke="line", rx=3)
            s.rect(x + 11, y + 11, 6, 6, fill=color, rx=0)
            s.text(x + 24, y + 18.5, it, "m4", 12, "ink", tracking=0.02)
    s.save("stack")


def creds(theme: str) -> None:
    n = len(CREDS)
    colw = (W - 52 - (n - 1) * 18) / n
    wrapped = [[wrap(it, "si", 13.5, colw) for it in items] for *_, items in CREDS]
    H = 118 + max(sum(len(w) * 18 + 8 for w in col) for col in wrapped) + 16
    s = SVG(W + 10, H + 10, theme, "21 active credentials. " + " ".join(f"{iss}: {', '.join(i)}." for _, iss, _, i in CREDS))
    s.card(0, 0, W - 2, H)
    for i, ((color, issuer, count, _), col) in enumerate(zip(CREDS, wrapped)):
        x = 26 + i * (colw + 18)
        if i:
            s.line(x - 9, 26, x - 9, H - 20, "line", dash="3 4")
        s.text(x, 44, issuer, "m7", 11, color, tracking=0.08)
        s.text(x, 90, f"×{count}", "d8", 38, "ink", tracking=-0.02)
        y = 124
        for rows in col:
            s.lines(x, y, rows, 18, style="si", size=13.5, fill="ink2")
            y += len(rows) * 18 + 8
    s.save("creds")


def viewfinder(s: SVG, x: float, y: float, w: float, h: float) -> None:
    s.css.append("@keyframes rec{50%{opacity:.15}}.rec{animation:rec 1.2s steps(1) infinite}"
                 "@keyframes focus{0%,100%{transform:scale(1)}45%{transform:scale(1.35)}55%{transform:scale(.92)}}"
                 f".focus{{transform-origin:{x + w / 2}px {y + h / 2}px;animation:focus 3.2s ease-in-out infinite}}")
    s.rect(x, y, w, h, fill="surface", stroke="line", rx=6)
    for f in (1 / 3, 2 / 3):
        s.line(x + w * f, y + 8, x + w * f, y + h - 8, "line", dash="2 4")
        s.line(x + 8, y + h * f, x + w - 8, y + h * f, "line", dash="2 4")
    L, m = 18, 12
    for cx, cy, dx, dy in ((x + m, y + m, 1, 1), (x + w - m, y + m, -1, 1), (x + m, y + h - m, 1, -1), (x + w - m, y + h - m, -1, -1)):
        s.add(f'<path d="M{cx} {cy + dy * L}V{cy}H{cx + dx * L}" fill="none" stroke="{s.c("ink2")}" stroke-width="2"/>')
    fx, fy, fs = x + w / 2, y + h / 2, 22
    s.add(f'<g class="focus"><rect x="{fx - fs}" y="{fy - fs * .7}" width="{fs * 2}" height="{fs * 1.4}" fill="none" '
          f'stroke="{s.c("lime")}" stroke-width="1.6"/></g>')
    s.add(f'<circle class="rec" cx="{x + 26}" cy="{y + 30}" r="5" fill="{s.c("pink")}"/>')
    s.text(x + 36, y + 34, "REC", "m7", 10.5, "pink", tracking=0.1)
    s.text(x + w - 22, y + 34, "4K · 24", "m4", 10.5, "ink2", anchor="end", tracking=0.06)
    s.text(x + w / 2, y + h - 18, "ISO 400   f/1.8   1/50", "m4", 10.5, "ink2", anchor="middle", tracking=0.06)


def culture(theme: str) -> None:
    text_w = 470
    head = wrap(CULTURE["headline"], "d7", 26, text_w, -0.02)
    dek = wrap(CULTURE["dek"], "si", 16, text_w)
    H = max(64 + 18 + len(head) * 31 + 14 + len(dek) * 24 + 24, 210)
    s = SVG(W + 10, H + 10, theme, f"Off the clock: photography and filmmaking. {CULTURE['dek']}")
    s.card(0, 0, W - 2, H, accent="pink")
    s.kicker(26, 38, "NO.∞", "CULTURE", "pink", "PHOTOGRAPHY · FILMMAKING")
    y = s.lines(26, 82, head, 31, style="d7", size=26, fill="ink", tracking=-0.02)
    s.lines(26, y + 32, dek, 24, style="si", size=16, fill="ink2")
    viewfinder(s, W - 28 - 260, (H - 160) / 2, 260, 160)
    s.save("culture")


ICONS = {
    "linkedin": lambda s, x, y, c: s.add(
        f'<rect x="{x}" y="{y}" width="18" height="18" rx="2" fill="{c}"/>'
        f'<rect x="{x + 3.5}" y="{y + 7.5}" width="2.6" height="7.5" fill="{s.c("bg")}"/>'
        f'<circle cx="{x + 4.8}" cy="{y + 4.6}" r="1.6" fill="{s.c("bg")}"/>'
        f'<path d="M{x + 8} {y + 7.5}h2.5v1.2c.5-.9 1.5-1.4 2.7-1.4 2 0 2.9 1.2 2.9 3.4V15h-2.6v-3.8c0-1-.4-1.6-1.3-1.6'
        f'-.9 0-1.6.6-1.6 1.7V15H{x + 8}z" fill="{s.c("bg")}"/>'),
    "email": lambda s, x, y, c: s.add(
        f'<rect x="{x}" y="{y + 2}" width="18" height="14" rx="1.5" fill="none" stroke="{c}" stroke-width="2"/>'
        f'<path d="M{x + 1} {y + 3.5}l8 6.5 8-6.5" fill="none" stroke="{c}" stroke-width="2"/>'),
    "newsletter": lambda s, x, y, c: chip(s, x, y, 2.25),
    "blog": lambda s, x, y, c: s.add(
        f'<path d="M{x + 2} {y + 16}l2-6 9-9 4 4-9 9z" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>'
        f'<path d="M{x + 11} {y + 3}l4 4" stroke="{c}" stroke-width="2"/>'),
}


def connect(theme: str) -> None:
    bw, bh = 196, 44
    for key, color, label in CONNECT:
        s = SVG(bw + 8, bh + 8, theme, label.title())
        soon = key == "blog"
        s.rect(5, 5, bw - 2, bh, fill="shadow" if not soon else "none", rx=3)
        if not soon:
            s.rect(2.5, 2.5, bw - 2, bh, fill=color, rx=3)
        s.rect(0.5, 0.5, bw - 2, bh, fill="bg", stroke="strong" if not soon else "faint", sw=1.2, rx=3,
               extra='stroke-dasharray="4 3"' if soon else "")
        ICONS[key](s, 16, bh / 2 - 8.5, s.c(color))
        s.text(46, bh / 2 + 5, label, "m7", 12.5, "ink" if not soon else "muted", tracking=0.08)
        if not soon:
            s.text(bw - 18, bh / 2 + 5, "↗", "m7", 13, color, anchor="end")
        s.save(f"btn-{key}")


def footer(theme: str) -> None:
    s = SVG(W, 96, theme, "Let's build something. Say hi on LinkedIn or email prakashshubham36@gmail.com")
    s.line(0, 10, W, 10, "strong", sw=1)
    s.text(W / 2, 54, "Let's build something.", "d7", 24, "ink", anchor="middle", tracking=-0.01)
    s.text(W / 2, 82, "SAY HI ON LINKEDIN ↗ · PRAKASHSHUBHAM36@GMAIL.COM", "m4", 10.5, "muted", anchor="middle", tracking=0.08)
    s.save("footer")


if __name__ == "__main__":
    import sys
    if "--logo" in sys.argv:
        LOGO = sys.argv[sys.argv.index("--logo") + 1]
    for theme in ("dark", "light"):
        header(theme)
        for key in SECTIONS:
            section(key, theme)
        about(theme)
        lead_card(theme)
        small_cards(theme)
        private_desk(theme)
        archive(theme)
        stack(theme)
        creds(theme)
        culture(theme)
        connect(theme)
        footer(theme)
    print("built")
