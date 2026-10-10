# amz34.github.io

![Project index for always-on AI systems — abstract overview of a linked node map over a server rack](assets/site-overview.jpg)

Personal site and project index for **Aamir Zameer** — AI automation engineer.
Live at **https://amz34.github.io/**

Static, single-file, zero dependencies, no analytics and no third-party fonts.
Served by GitHub Pages from `main` / root.

## What it links to

| Project | What it is |
|---|---|
| [ai-can-run](https://github.com/Amz34/ai-can-run) | Browser-side hardware detection: which open models your machine can run |
| [selfhosted-agent-stack](https://github.com/Amz34/selfhosted-agent-stack) | Run a 24/7 AI agent on free cloud — watchdogs, zram, crash recovery |
| [linkedin-autopilot](https://github.com/Amz34/linkedin-autopilot) | AI drafts, you approve, it publishes |
| [multi-agent-research-pipeline](https://github.com/Amz34/multi-agent-research-pipeline) | Crashproof multi-agent orchestration |
| [hermes-slack-agents](https://github.com/Amz34/hermes-slack-agents) | One gateway, per-client agents |
| [voice-portfolio](https://amz34.github.io/voice-portfolio/) | Talking portfolio — on-device browser voice agent, English and Arabic editions |

## Structure

```
index.html              the whole site (inline CSS, no build step)
assets/og-card.png      1200x630 social preview card
assets/site-overview.jpg 1200x630 section illustration used in this README
assets/                 other site imagery
tools/check_links.py    link guard: fails on a dead visitor-facing link
.github/workflows/      runs that guard on every push and pull request
robots.txt, sitemap.xml discovery for crawlers
.nojekyll               serve files as-is (no Jekyll processing)
```

## Link guard

The page is not built, so a card can rot silently: a repository turns private or
gets renamed and the link starts returning 404 to every visitor. `tools/check_links.py`
reads `index.html` and `README.md`, resolves each `github.com/Amz34/...` link and every
live-demo path **anonymously** — exactly as a visitor would — and confirms that each
referenced asset exists in the tree. It is standard library only.

```bash
python3 tools/check_links.py --selftest   # controls: healthy tree passes, dead link is caught
python3 tools/check_links.py              # the real tree; exit 1 names every dead link
```

The same guard runs in `.github/workflows/link-guard.yml` on every push to `main`,
on pull requests and once a week, so a link that dies later fails the build instead
of quietly staying broken.

## Local preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Editing

One file. Change the copy in `index.html`, commit to `main`, Pages redeploys in
about a minute. Keep it dependency-free so it never rots. Every change goes through
the link guard, so fix a link before it becomes a 404.

## License

MIT — see the license text in [LICENSE](LICENSE).

---

Part of [my always-on agent stack](https://github.com/Amz34) · [Awesome Agent Infrastructure](https://github.com/Amz34/awesome-agent-infrastructure) (135 live-checked building blocks).
