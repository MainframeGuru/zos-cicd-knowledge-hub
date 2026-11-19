#!/usr/bin/env python3
"""Crawls the (live or locally served) website and checks that all internal links/assets return HTTP 200
and that all internal #anchors exist on the target page. Also checks the legacy (v1, German) redirect paths.
Usage: python3 scripts/check_site.py https://mainframeguru.github.io/zos-cicd-knowledge-hub/
"""
import re, sys, html, urllib.request, urllib.error
from urllib.parse import urljoin, urldefrag, urlparse

start = sys.argv[1] if len(sys.argv) > 1 else "https://mainframeguru.github.io/zos-cicd-knowledge-hub/"
if not start.endswith("/"):
    start += "/"
host, prefix = urlparse(start).netloc, urlparse(start).path
extra = ["feed.xml", "sitemap.xml", "robots.txt", "assets/og-image.png", "assets/style.css", "assets/app.js", "assets/favicon.svg"]
# Former German paths -> new English slugs (must stay in sync with REDIRECTS in build.py)
legacy = {"warum-cicd": "why-cicd", "migrationen": "migrations", "ressourcen": "resources", "impressum": "imprint", "datenschutz": "privacy"}
todo, seen, bad = [start] + [start + e for e in extra] + [start + n + "/" for n in legacy.values()], set(), []
ids, anchors = {}, []  # page -> set of ids; (page, fragment, found_in)


def fetch(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "zos-cicd-sitecheck"}), timeout=30) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read()
    except urllib.error.HTTPError as e:
        return e.code, "", b""


while todo:
    u = todo.pop()
    if u in seen:
        continue
    seen.add(u)
    code, ctype, body = fetch(u)
    print(code, u)
    if code != 200:
        bad.append((code, u)); continue
    if "html" in ctype or "xml" in ctype:
        text = body.decode("utf-8", "replace")
        if "html" in ctype:
            ids[u] = set(re.findall(r'\sid="([^"]+)"', text))
        for link in re.findall(r'(?:href|src)="([^"]+)"|<loc>([^<]+)</loc>|<link href="([^"]+)"', text):
            link = html.unescape(link[0] or link[1] or link[2])
            absu, frag = urldefrag(urljoin(u, link))
            p = urlparse(absu)
            if p.netloc == host and p.scheme in ("http", "https"):
                if not p.path.startswith(prefix):
                    bad.append(("OUTSIDE-BASE", absu + "  (found in " + u + ")")); continue
                if frag:
                    anchors.append((absu, frag, u))
                todo.append(absu)

for page, frag, src in anchors:
    if page in ids and frag not in ids[page]:
        bad.append(("MISSING-ANCHOR", f"{page}#{frag}  (found in {src})"))

# Legacy redirect pages: must return 200, point (canonical + meta refresh) to the new URL
for old, new in legacy.items():
    code, _, body = fetch(start + old + "/")
    text = body.decode("utf-8", "replace")
    target = start + new + "/"
    tpath = re.escape(prefix + new + "/")  # compare by path so the check also works against a local server
    ok = (code == 200 and re.search(r'rel="canonical" href="https?://[^"/]+' + tpath + '"', text) is not None
          and re.search(r'url=https?://[^"/]+' + tpath + '"', text) is not None)
    print(("OK " if ok else "BAD"), "redirect", start + old + "/", "->", target)
    if not ok:
        bad.append(("REDIRECT", start + old + "/"))

print(f"\n{len(seen)} internal URLs checked, {len(anchors)} anchor links checked, {len(bad)} problems")
for b in bad:
    print("  ", *b)
sys.exit(1 if bad else 0)
