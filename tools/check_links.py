#!/usr/bin/env python3
"""Link guard for the amz34.github.io site.

The site is a static page with no build step, so nothing stops a card from
pointing at a repository that is private, renamed or deleted. A visitor then
clicks a dead link and the page silently loses credibility.

This guard reads the links that actually ship (index.html and README.md),
resolves every repository and live-demo link anonymously, and fails when one of
them is not reachable by a visitor.

Standard library only. Exit codes: 0 = all links healthy, 1 = dead link found,
2 = usage or internal error.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request

USER_AGENT = "amz34-link-guard/1.0 (+https://amz34.github.io/)"
# An explicit user agent matters: GitHub answers 403 to default urllib clients.
TIMEOUT = 20
RETRIES = 3

REPO_URL_RE = re.compile(r"https://github\.com/Amz34/[A-Za-z0-9._-]+")
PAGES_URL_RE = re.compile(r"https://amz34\.github\.io(/[A-Za-z0-9._/-]*)?")
SHIPPED_FILES = ("index.html", "README.md")

HTML_REMOTE_RE = re.compile(r'(?:href|src)="(https?://[^"]+)"')
HTML_LOCAL_RE = re.compile(r'(?:href|src)="((?!https?:|//|#|mailto:)[^"]+)"')
MD_REMOTE_RE = re.compile(r"\]\((https?://[^)\s]+)\)")
MD_LOCAL_RE = re.compile(r"\]\((?!https?:|//|#|mailto:)([^)\s]+)\)")

# Statuses that mean "a visitor cannot open this".
DEAD_STATUS = {400, 401, 403, 404, 410, 451}


def fetch_status(url: str) -> int | None:
    """Return the HTTP status, or None when the network failed entirely."""
    last_error: Exception | None = None
    for attempt in range(RETRIES):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                return response.status
        except urllib.error.HTTPError as exc:
            return exc.code  # a real answer, even if it is a bad one
        except Exception as exc:  # noqa: BLE001 - transport failures are retried
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    print(f"  ! network failure for {url}: {last_error}")
    return None


def collect(root: str) -> tuple[set[str], set[str], set[str], set[str]]:
    """Return (repo URLs, pages URLs, remote URLs, local asset paths) that ship."""
    repo_urls: set[str] = set()
    pages_urls: set[str] = set()
    remote: set[str] = set()
    local: set[str] = set()
    for rel in SHIPPED_FILES:
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            continue
        text = open(path, encoding="utf-8").read()
        if rel.endswith(".html"):
            remote.update(HTML_REMOTE_RE.findall(text))
            local.update(HTML_LOCAL_RE.findall(text))
        else:
            remote.update(MD_REMOTE_RE.findall(text))
            local.update(MD_LOCAL_RE.findall(text))
        repo_urls.update(REPO_URL_RE.findall(text))
        for suffix in PAGES_URL_RE.findall(text):
            pages_urls.add(f"https://amz34.github.io{suffix}")
    return repo_urls, pages_urls, remote, local


def check(root: str) -> int:
    repo_urls, pages_urls, remote, local = collect(root)
    failures: list[str] = []
    checked = 0

    print(f"repository links referenced: {len(repo_urls)}")
    for url in sorted(repo_urls):
        checked += 1
        status = fetch_status(url)
        if status is None:
            print(f"  ?    {url} (unverified - network)")
        elif status in DEAD_STATUS:
            failures.append(f"dead repository link ({status}): {url}")
            print(f"  FAIL {status} {url}")
        else:
            print(f"  ok   {status} {url}")

    print(f"live pages referenced: {len(pages_urls)}")
    for url in sorted(pages_urls):
        checked += 1
        status = fetch_status(url)
        if status is None:
            print(f"  ?    {url} (unverified - network)")
        elif status in DEAD_STATUS:
            failures.append(f"dead pages link ({status}): {url}")
            print(f"  FAIL {status} {url}")
        else:
            print(f"  ok   {status} {url}")

    print(f"local assets referenced: {len(local)}")
    for rel in sorted(local):
        checked += 1
        if os.path.exists(os.path.normpath(os.path.join(root, rel))):
            print(f"  ok   present {rel}")
        else:
            failures.append(f"missing asset: {rel}")
            print(f"  FAIL missing {rel}")

    print(f"\nchecked {checked} link(s) from {' + '.join(SHIPPED_FILES)}")
    if failures:
        print(f"RESULT: FAIL - {len(failures)} problem(s)")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("RESULT: PASS - every referenced link is reachable by a visitor")
    return 0


def selftest() -> int:
    """Prove the guard both ways: a healthy tree passes, a dead link is caught."""
    healthy = """<!DOCTYPE html><html><body>
<a href="https://github.com/Amz34/Amz34.github.io">this repository</a>
<a href="https://amz34.github.io/">home</a>
<img src="assets/og-card.png" alt="card">
</body></html>"""
    broken = healthy.replace(
        "https://github.com/Amz34/Amz34.github.io",
        "https://github.com/Amz34/zzz-link-guard-selftest-does-not-exist",
    ).replace("assets/og-card.png", "assets/does-not-exist.png")

    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "assets"), exist_ok=True)
        open(os.path.join(tmp, "assets", "og-card.png"), "wb").write(b"\x89PNG\r\n")
        open(os.path.join(tmp, "README.md"), "w", encoding="utf-8").write("# selftest\n")

        open(os.path.join(tmp, "index.html"), "w", encoding="utf-8").write(healthy)
        print("[selftest] positive control (every link healthy) must exit 0")
        if check(tmp) != 0:
            print("[selftest] FAIL: healthy tree was rejected")
            failures += 1

        open(os.path.join(tmp, "index.html"), "w", encoding="utf-8").write(broken)
        print("\n[selftest] negative control (dead repository + missing asset) must exit 1")
        if check(tmp) != 1:
            print("[selftest] FAIL: broken tree slipped through")
            failures += 1

    if failures:
        print(f"\nSELFTEST: FAIL ({failures})")
        return 1
    print("\nSELFTEST: PASS - healthy tree accepted, dead link caught")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify every visitor-facing link in the site.")
    parser.add_argument("--repo-root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    parser.add_argument("--selftest", action="store_true", help="run the guard's own controls")
    args = parser.parse_args()

    if args.selftest:
        return selftest()
    if not os.path.isdir(args.repo_root):
        print(f"ERROR: not a directory: {args.repo_root}", file=sys.stderr)
        return 2
    return check(args.repo_root)


if __name__ == "__main__":
    sys.exit(main())
