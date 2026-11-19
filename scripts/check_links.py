#!/usr/bin/env python3
"""Checks all external links in public/ (HTTP status). Usage: python3 scripts/check_links.py"""
import re, glob, subprocess, concurrent.futures as cf, html
urls = set()
for f in glob.glob("public/**/*.html", recursive=True):
    for u in re.findall(r'href="(https?://[^"]+)"', open(f, encoding="utf-8").read()):
        u = html.unescape(u)
        if not any(s in u for s in ("sharing/share-offsite", "x.com/intent", "mastodonshare.com", "pages.dev", "github.io")):
            urls.add(u)
def check(u):
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-L", "--max-time", "25", "-A",
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36", u], capture_output=True, text=True)
    return r.stdout, u
with cf.ThreadPoolExecutor(12) as ex:
    res = sorted(ex.map(check, urls))
bad = [r for r in res if r[0] != "200"]
for c, u in bad: print(c, u)
print(f"{len(urls)} links checked, {len(bad)} not 200 (403/999 = usually bot protection, check manually)")
