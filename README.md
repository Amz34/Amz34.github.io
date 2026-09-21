# amz34.github.io

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
| [voice-clone-assistant](https://github.com/Amz34/voice-clone-assistant) | 30-second voice clone assistant |

## Structure

```
index.html              the whole site (inline CSS, no build step)
assets/og-card.png      1200x630 social preview card
robots.txt, sitemap.xml discovery for crawlers
.nojekyll               serve files as-is (no Jekyll processing)
```

## Local preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Editing

One file. Change the copy in `index.html`, commit to `main`, Pages redeploys in
about a minute. Keep it dependency-free so it never rots.

## License

MIT — see the license text in [LICENSE](LICENSE).

---

Part of [my always-on agent stack](https://github.com/Amz34) · [Awesome Agent Infrastructure](https://github.com/Amz34/awesome-agent-infrastructure) (135 live-checked building blocks).
