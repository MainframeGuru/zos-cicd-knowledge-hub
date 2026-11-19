#!/usr/bin/env python3
"""Crawlt die (live oder lokal laufende) Website und prüft alle internen Links/Assets auf HTTP 200.
Aufruf: python3 scripts/check_site.py https://mainframeguru.github.io/zos-cicd-knowledge-hub/
"""
import re, sys, html, urllib.request, urllib.error
from urllib.parse import urljoin, urldefrag, urlparse

start = sys.argv[1] if len(sys.argv) > 1 else "https://mainframeguru.github.io/zos-cicd-knowledge-hub/"
if not start.endswith("/"):
    start += "/"
host, prefix = urlparse(start).netloc, urlparse(start).path
extra = ["feed.xml", "sitemap.xml", "robots.txt", "assets/og-image.png", "assets/style.css", "assets/app.js", "assets/favicon.svg"]
todo, seen, bad = [start] + [start + e for e in extra], set(), []

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
        for link in re.findall(r'(?:href|src)="([^"]+)"|<loc>([^<]+)</loc>', text):
            link = html.unescape(link[0] or link[1])
            absu = urldefrag(urljoin(u, link))[0]
            p = urlparse(absu)
            if p.netloc == host and p.scheme in ("http", "https"):
                if not p.path.startswith(prefix):
                    bad.append(("AUSSERHALB", absu + "  (gefunden in " + u + ")")); continue
                todo.append(absu)
print(f"\n{len(seen)} interne URLs geprüft, {len(bad)} Probleme")
for b in bad:
    print("  ", *b)
sys.exit(1 if bad else 0)
