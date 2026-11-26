#!/usr/bin/env python3
"""Static site generator for the z/OS CI/CD Compass.

Reads data/*.json and src/content/*.html and writes the finished website to public/.
No dependencies other than Python 3.8+. Usage:  python3 build.py
"""
import json, html, os, re, shutil, datetime
from pathlib import Path
from urllib.parse import quote, urlparse

ROOT = Path(__file__).parent
OUT = ROOT / "public"
SITE = json.loads((ROOT / "data/site.json").read_text(encoding="utf-8"))
NEWS = sorted(json.loads((ROOT / "data/news.json").read_text(encoding="utf-8")), key=lambda n: n.get("sort_date") or n["date"] or n.get("date_added"), reverse=True)  # sort_date: keeps list position for entries whose source states no date
RES = json.loads((ROOT / "data/resources.json").read_text(encoding="utf-8"))
BASE = SITE["base_url"].rstrip("/")
LANG = SITE.get("language", "en")
# Derive the path prefix from base_url: "https://user.github.io/repo" -> "/repo", custom domain -> "".
# All root-absolute links (href="/…", src="/…") in the generated HTML are prefixed automatically.
BASE_PATH = urlparse(BASE).path.rstrip("/")


def with_base(markup):
    """Prefix root-absolute internal links/assets with BASE_PATH (leaves //cdn… and https://… untouched)."""
    if not BASE_PATH:
        return markup
    return re.sub(r'((?:href|src|action)=")/(?!/)', lambda m: m.group(1) + BASE_PATH + "/", markup)
E = html.escape
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

RES_TYPES = [  # Order = filter order. Add new types here.
    ("case-study", "Project reference / Case study", "Publicly documented project with a named or anonymized organization, published by the user, vendor or service provider."),
    ("experience", "Experience report", "Users report in an interview, blog or conversation – less formal than a case study."),
    ("talk", "Webinar / Talk / Presentation", "Conference talk, webinar, panel, demo or slide deck (SHARE, GSE, TechXchange, Open Mainframe Summit …)."),
    ("whitepaper", "Whitepaper / Vendor docs", "Documentation, guides, product pages and marketing from vendors or service providers."),
    ("press", "Press / Article", "Reports and guest articles in trade and general media, as well as press releases."),
]
TYPE_LABEL = {k: v for k, v, _ in RES_TYPES}

FAQ = [
    ("Is Git actually available on z/OS?", "Yes. A Git client for z/OS UNIX System Services is provided, among others, through IBM Open Enterprise Foundation for z/OS and the zopen Community. Alternatively, developers work locally (VS Code, Eclipse) and builds run on z/OS via SSH/Zowe."),
    ("Do I have to switch to IBM DBB for CI/CD?", "No. DBB is one option for dependency-based builds. Alternatives include Broadcom Team Build, BMC AMI DevX Code Pipeline, or existing JCL builds that are started and monitored by the pipeline."),
    ("Can I keep my library manager?", "Yes. Endevor (Bridge for Git), ChangeMan ZMF and BMC Code Pipeline offer Git integrations for coexistence. IBM argues that Git should be the authoritative source rather than being permanently synchronized with a legacy library manager (see Why CI/CD?)."),
    ("How long does a migration take?", "ANZ reports around 40 applications in 8 months; according to the IBM Expert Labs success story, dwpbank’s complete transformation was delivered in 11 months. The key factors are volume, the number of processor variants, test coverage and training effort."),
    ("Which CI servers work with z/OS?", "Jenkins, GitLab CI (including a native z/OS runner), GitHub Actions and Azure DevOps are publicly documented – usually with an agent/runner that accesses z/OS via SSH or Zowe. IBM provides pipeline templates on GitHub."),
    ("What happens to SCLM?", "In an update of 27 Oct 2026 in the IBM Community thread “Infrastructure Management Deprecations”, IBM states that it intends to remove SCLM from a future release of z/OS. According to a LinkedIn post by Marna Walle (IBM), IBM had earlier planned to remove SCLM in the release after z/OS 3.2."),
]

PAGES = [
    # slug, nav label, title, description, content file, in navigation, page type
    ("", "Overview", "CI/CD on z/OS – Git, pipelines & migrations explained", SITE["description"], "index.html", True, "WebPage"),
    ("why-cicd", "Why CI/CD", "Why CI/CD on the mainframe? Reasons, benefits, risks", "Skills, Git as the standard, speed, testing, compliance and cost: the main reasons for CI/CD on IBM z/OS – with publicly documented examples and an FAQ.", "why-cicd.html", True, "Article"),
    ("migrations", "Migrations", "Migration paths: Endevor, ChangeMan ZMF, ISPW, SCLM → Git & CI/CD", "Migration paths from Endevor, ChangeMan ZMF, ISPW/Code Pipeline, SCLM, Panvalet and Librarian to Git, DBB and CI/CD – including automated migration approaches.", "migrations.html", True, "Article"),
    ("news", "Product news", "Product news on CI/CD for z/OS: IBM, Broadcom, BMC, Rocket, Zowe", "Dated product announcements around mainframe DevOps: IBM DBB, Wazi Deploy, Endevor Bridge for Git, BMC AMI DevX, Zowe, Galasa, Rocket and more – filterable by vendor.", None, True, "CollectionPage"),
    ("resources", "Resources", "Case studies, talks & articles on mainframe CI/CD", "Curated, clearly labeled sources: project references, experience reports, talks/webinars, whitepapers and press articles on Git and CI/CD on z/OS.", None, True, "CollectionPage"),
    ("imprint", "Imprint", "Imprint", "Imprint (legal notice) of the z/OS CI/CD Compass: operator, contact, person responsible for content and editorial policy.", "imprint.html", False, "WebPage"),
    ("privacy", "Privacy", "Privacy policy", "Privacy policy of the z/OS CI/CD Compass: hosting on GitHub Pages, no cookies, no analytics, browser functions and your rights.", "privacy.html", False, "WebPage"),
    ("impressum", "Impressum", "Impressum", "Impressum des z/OS CI/CD Compass: Anbieter, Kontakt, inhaltlich Verantwortlicher und redaktionelle Grundsätze.", "impressum.html", False, "WebPage"),
    ("datenschutz", "Datenschutz", "Datenschutzerklärung", "Datenschutzerklärung des z/OS CI/CD Compass: Hosting bei GitHub Pages, keine Cookies, keine Reichweitenmessung, Browser-Funktionen und Ihre Rechte.", "datenschutz.html", False, "WebPage"),
]

# German-language pages (all other pages use SITE["language"]) and EN<->DE translation pairs for hreflang.
PAGE_LANG = {"impressum": ("de", "de_DE"), "datenschutz": ("de", "de_DE")}
TRANSLATIONS = {"imprint": "impressum", "privacy": "datenschutz"}  # en slug -> de slug


def page_lang(slug):
    return PAGE_LANG.get(slug, (LANG, SITE["locale"]))


def hreflang_links(slug):
    pairs = {**TRANSLATIONS, **{v: k for k, v in TRANSLATIONS.items()}}
    if slug not in pairs:
        return f'<link rel="alternate" hreflang="{LANG}" href="{url(slug)}">\n<link rel="alternate" hreflang="x-default" href="{url(slug)}">'
    en, de = (slug, pairs[slug]) if slug in TRANSLATIONS else (pairs[slug], slug)
    return (f'<link rel="alternate" hreflang="en" href="{url(en)}">\n<link rel="alternate" hreflang="de" href="{url(de)}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{url(en)}">')

# Former German URL paths (v1) -> new English slugs. Redirect pages keep existing links working.
REDIRECTS = {
    "warum-cicd": "why-cicd",
    "migrationen": "migrations",
    "ressourcen": "resources",
}


def url(slug):
    return f"{BASE}/{slug}/" if slug else f"{BASE}/"


def fmt_date(d, precision=None):
    if not d:
        return ""
    parts = d.split("-")
    if len(parts) == 1:
        return parts[0]
    y, m = int(parts[0]), int(parts[1])
    if len(parts) == 2 or precision == "month":
        return f"{MONTHS[m-1]} {y}"
    return f"{MONTHS[m-1]} {int(parts[2])}, {y}"


def _configured(value):
    return bool(value) and "_HERE" not in value


def analytics_snippet():
    a = SITE.get("analytics", {})
    p = a.get("provider", "none")
    if p == "cloudflare" and _configured(a.get("cloudflare_token", "")):
        tok = json.dumps({"token": a["cloudflare_token"]})
        return f"<script defer src=\"https://static.cloudflareinsights.com/beacon.min.js\" data-cf-beacon='{tok}'></script>"
    if p == "goatcounter" and _configured(a.get("goatcounter_code", "")):
        return f'<script data-goatcounter="https://{E(a["goatcounter_code"])}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
    return "<!-- Analytics disabled (data/site.json → analytics.provider) -->"


def analytics_text():
    p = SITE.get("analytics", {}).get("provider", "none")
    if p == "cloudflare":
        return ("We use Cloudflare Web Analytics. No cookies are set and no personal profiles are created; "
                "aggregated page views, referrers, country and device type are measured. Provider: Cloudflare, Inc. [Add legal basis/third-country transfer].")
    if p == "goatcounter":
        return ("We use GoatCounter (goatcounter.com), a cookieless, privacy-friendly open-source analytics service. "
                "Aggregated page views, referrers, browser, screen size and country are measured; IP addresses are not stored. [Add legal basis].")
    return "No audience measurement currently takes place. If enabled, only a cookieless method (Cloudflare Web Analytics or GoatCounter) will be used; this section will then be updated."


LOGO = '<svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#0b7a75"/><path d="M8 11h16M8 16h10M8 21h16" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><circle cx="23" cy="16" r="2.6" fill="#7ee2d9"/></svg>'


def share_block(page_url, title):
    u, t = quote(page_url, safe=""), quote(title, safe="")
    return f'''<aside class="share" aria-label="Share this page">
  <span class="muted small">Share:</span>
  <a href="https://www.linkedin.com/sharing/share-offsite/?url={u}" rel="noopener" target="_blank">LinkedIn</a>
  <a href="https://x.com/intent/post?url={u}&amp;text={t}" rel="noopener" target="_blank">X</a>
  <a href="https://mastodonshare.com/?url={u}&amp;text={t}" rel="noopener" target="_blank">Mastodon</a>
  <a href="mailto:?subject={t}&amp;body={u}">Email</a>
  <a href="{E(page_url)}" data-copy="url">Copy link</a>
</aside>'''


def cite_block(page_url, title):
    today = SITE["last_updated"]
    txt = f'{SITE["name"]}: “{title}”. Last updated {fmt_date(today)}. Available at: {page_url} (accessed YYYY-MM-DD).'
    return f'''<details class="cite-box"><summary>Cite</summary>
<p class="small muted">Suggested citation (adjust the access date). Individual entries have their own anchor links (¶).</p>
<div class="cite">{E(txt)}</div>
<p><button class="chip" type="button" data-copy="{E(txt)}">Copy citation</button></p></details>'''


def json_ld(page):
    slug, _, title, desc, _, _, ptype = page
    graph = [
        {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": SITE["name"], "description": SITE["description"], "inLanguage": LANG},
        {"@type": ptype, "@id": url(slug) + "#page", "url": url(slug), "name": title, "description": desc, "inLanguage": page_lang(slug)[0],
         "isPartOf": {"@id": BASE + "/#website"}, "dateModified": SITE["last_updated"],
         "image": BASE + "/assets/og-image.png"},
    ]
    if ptype == "Article":
        graph[1].update({"headline": title, "author": {"@type": "Organization", "name": SITE["name"]}, "datePublished": "2026-11-19"})
    if slug:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Overview", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": page[1], "item": url(slug)}]})
    if slug == "why-cicd":
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]})
    if slug == "news":
        graph.append({"@type": "ItemList", "name": "Product news: CI/CD and DevOps on z/OS", "itemListOrder": "https://schema.org/ItemListOrderDescending", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": {
                "@type": "NewsArticle", "@id": url("news") + "#news-" + n["id"], "url": url("news") + "#news-" + n["id"],
                "headline": n["title"], "datePublished": n["date"] or n.get("date_added"), "inLanguage": LANG,
                "about": n["product"], "isBasedOn": n["url"]}} for i, n in enumerate(NEWS)]})
    if slug == "resources":
        graph.append({"@type": "ItemList", "name": "Case studies, experience reports, talks and articles", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": url("resources") + "#res-" + r["id"], "name": r["title"]} for i, r in enumerate(RES)]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def layout(page, body):
    slug, nav_label, title, desc, _, _, _ = page
    full_title = f"{title} | {SITE['name']}" if slug else f"{SITE['name']} – {title}"
    page_url = url(slug)
    cur = ' aria-current="page"'
    nav = "".join(
        '<li><a href="/' + (p[0] + "/" if p[0] else "") + '"' + (cur if p[0] == slug else "") + '>' + E(p[1]) + '</a></li>'
        for p in PAGES if p[5])
    plang, plocale = page_lang(slug)
    tw = f'<meta name="twitter:site" content="{E(SITE["twitter_handle"])}">' if SITE.get("twitter_handle") else ""
    return f'''<!doctype html>
<html lang="{plang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full_title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{page_url}">
{hreflang_links(slug)}
<link rel="alternate" type="application/atom+xml" title="{E(SITE['name'])} – Product news" href="/feed.xml">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0b7a75">
<meta property="og:type" content="{"article" if page[6] == "Article" else "website"}">
<meta property="og:site_name" content="{E(SITE['name'])}">
<meta property="og:locale" content="{plocale}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{page_url}">
<meta property="og:image" content="{BASE}/assets/og-image.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(SITE['name'])}: CI/CD on z/OS">
<meta name="twitter:card" content="summary_large_image">{tw}
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{BASE}/assets/og-image.png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/style.css">
<script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<script type="application/ld+json">{json_ld(page)}</script>
{analytics_snippet()}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap nav">
  <a class="brand" href="/">{LOGO}<span>{E(SITE['name'])}</span></a>
  <button class="icon-btn menu-btn" id="menu-toggle" aria-controls="menu" aria-expanded="false" aria-label="Menu">☰</button>
  <nav aria-label="Main navigation"><ul id="menu">{nav}</ul></nav>
  <button class="icon-btn" id="theme-toggle" type="button" aria-label="Toggle color scheme" hidden>◐</button>
</div></header>
<main id="main">
{body}
<div class="wrap">{share_block(page_url, title)}{cite_block(page_url, title)}</div>
</main>
<footer class="site"><div class="wrap cols">
  <div><b>{E(SITE['name'])}</b><br>{E(SITE['tagline'])}.<br>No cookies · no third-party trackers.</div>
  <div>Last updated: <time datetime="{SITE['last_updated']}">{fmt_date(SITE['last_updated'])}</time><br>
  <a href="/feed.xml">Atom feed</a> · <a href="/sitemap.xml">Sitemap</a><br>
  <a href="/imprint/">Imprint</a> · <a href="/privacy/">Privacy</a> · <a href="/impressum/" hreflang="de" lang="de">Impressum (DE)</a> · <a href="/datenschutz/" hreflang="de" lang="de">Datenschutz (DE)</a></div>
  <div class="small">Trademarks belong to their respective owners. Information provided without warranty; sources are linked in each case.</div>
</div></footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="/assets/app.js" defer></script>
</body>
</html>
'''


def added_meta(x):
    # Entries with "date_added": show the MainframeGuru publication date; the source date only if the source gives one.
    d = x["date_added"]
    src = f' · Source date: {E(x["source_date"])}' if x.get("source_date") else ""
    return f'<span>Added to MainframeGuru: <time datetime="{d}">{fmt_date(d)}</time>{src}</span>'


def news_card(n, heading="h3"):
    extra = "".join(f' · <a href="{E(l["url"])}" rel="noopener">{E(l["label"])}</a>' for l in n.get("extra_links", []))
    tags = "".join(f'<span class="tag">{E(t)}</span>' for t in n.get("tags", []))
    aid = "news-" + n["id"]
    when = added_meta(n) if n.get("date_added") else f'<time datetime="{n["date"][:7] if n.get("date_precision") == "month" else n["date"]}">{fmt_date(n["date"], n.get("date_precision"))}</time>'
    return f'''<li><article class="card" id="{aid}" data-vendor="{E(n['vendor'])}">
  <div class="meta">{when}<span class="badge v">{E(n['vendor'])}</span><span>{E(n['product'])}</span></div>
  <{heading}>{E(n['title'])}<a class="anchor" href="/news/#{aid}" aria-label="Link to this entry" title="Link to this entry">¶</a></{heading}>
  <p>{E(n['summary'])}</p>
  <p class="small">Source: <a href="{E(n['url'])}" rel="noopener">{E(n['source'])}</a>{extra}</p>
  <div class="tags">{tags}</div>
</article></li>'''


def page_news():
    vendors = []
    for n in NEWS:
        if n["vendor"] not in vendors:
            vendors.append(n["vendor"])
    chips = '<button class="chip" type="button" data-value="all" aria-pressed="true">All</button>' + "".join(
        f'<button class="chip" type="button" data-value="{E(v)}" aria-pressed="false">{E(v)} ({sum(1 for n in NEWS if n["vendor"] == v)})</button>' for v in vendors)
    items = "\n".join(news_card(n, "h2") for n in NEWS)
    return f'''<div class="wrap">
<header class="page-head"><span class="eyebrow">Product news</span><h1>Product news: CI/CD and DevOps on z/OS</h1>
<p class="lead">Dated announcements from vendors and open-source projects – each with its primary source. Newest first. <a href="/feed.xml">Subscribe via Atom feed</a>.</p></header>
<div data-filter-root="vendor">
  <div class="filters" role="group" aria-label="Filter by vendor" hidden>{chips}</div>
  <p><input class="search" type="search" placeholder="Search news …" aria-label="Search news" hidden> <span class="count" aria-live="polite">{len(NEWS)} entries</span></p>
  <ol class="timeline" data-filter-list>
{items}
  </ol>
</div>
<p class="muted small">Dates with month precision come from fix lists or release overviews without a specific day.</p>
</div>'''


def res_card(r):
    extra = "".join(f' · <a href="{E(l["url"])}" rel="noopener">{E(l["label"])}</a>' for l in r.get("extra_links", []))
    rows = []
    for k, lbl in (("org", "Organization"), ("from", "From"), ("to", "To / tools"), ("event", "Event"), ("format", "Format")):
        v = r.get(k)
        if v and v not in ("—", "n/a"):
            rows.append(f"<b>{lbl}:</b> {E(v)}")
    aid = "res-" + r["id"]
    date = added_meta(r) if r.get("date_added") else f'<time datetime="{E(r["date"])}">{fmt_date(r["date"])}</time>' if r.get("date") else ""
    return f'''<li><article class="card" id="{aid}" data-type="{r['type']}">
  <div class="meta"><span class="badge t-{r['type']}">{E(TYPE_LABEL[r['type']])}</span>{date}<span>{E(r['publisher'])}</span></div>
  <h3>{E(r['title'])}<a class="anchor" href="/resources/#{aid}" aria-label="Link to this entry" title="Link to this entry">¶</a></h3>
  <p>{E(r['summary'])}</p>
  <p class="small">{" · ".join(rows)}</p>
  <p class="small"><a href="{E(r['url'])}" rel="noopener">Go to source →</a>{extra}</p>
  <p class="small muted">{E(r.get('note', ''))}</p>
</article></li>'''


def page_resources():
    chips = '<button class="chip" type="button" data-value="all" aria-pressed="true">All</button>' + "".join(
        f'<button class="chip" type="button" data-value="{k}" aria-pressed="false">{E(v)} ({sum(1 for r in RES if r["type"] == k)})</button>' for k, v, _ in RES_TYPES)
    legend = "".join(f'<div class="card"><span class="badge t-{k}">{E(v)}</span><p class="small">{E(d)}</p></div>' for k, v, d in RES_TYPES)
    order = {k: i for i, (k, _, _) in enumerate(RES_TYPES)}
    items = "\n".join(res_card(r) for r in sorted(RES, key=lambda r: (order[r["type"]], -int((r.get("date_added") or r.get("date") or "0")[:4]))))
    return f'''<div class="wrap">
<header class="page-head"><span class="eyebrow">Resources</span><h1>Case studies, experience reports, talks &amp; articles</h1>
<p class="lead">Every source is clearly labeled. Important: a <b>project reference</b> documents a concrete undertaking; a <b>talk/webinar</b> is not automatically a reference; <b>whitepapers</b> and vendor pages are marketing or documentation.</p></header>
<h2 class="small muted" style="margin-top:1rem">Labels</h2>
<div class="grid">{legend}</div>
<div data-filter-root="type" style="margin-top:2rem">
  <div class="filters" role="group" aria-label="Filter by source type" hidden>{chips}</div>
  <p><input class="search" type="search" placeholder="Search (e.g. Endevor, GitLab, bank) …" aria-label="Search resources" hidden> <span class="count" aria-live="polite">{len(RES)} entries</span></p>
  <ul class="grid" style="list-style:none;padding:0" data-filter-list>
{items}
  </ul>
</div>
<div class="info small">Missing a public source? Suggestions are welcome (see <a href="/imprint/">Imprint</a>). Only entries with a publicly accessible URL are included.</div>
</div>'''


def faq_html():
    return "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQ)


def atom_feed():
    upd = SITE["last_updated"] + "T00:00:00Z"
    entries = []
    for n in NEWS:
        link = url("news") + "#news-" + n["id"]
        entries.append(f'''<entry><title>{E(n['title'])}</title><link href="{link}"/><id>{link}</id>
<updated>{n.get('date_added') or n['date']}T00:00:00Z</updated><category term="{E(n['vendor'])}"/>
<summary>{E(n['summary'])} Source: {E(n['url'])}</summary></entry>''')
    return f'''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="{LANG}">
<title>{E(SITE['name'])} – Product news</title>
<subtitle>{E(SITE['tagline'])}</subtitle>
<link href="{BASE}/feed.xml" rel="self"/><link href="{url('news')}"/>
<id>{BASE}/feed.xml</id><updated>{upd}</updated><author><name>{E(SITE['name'])}</name></author>
{"".join(entries)}
</feed>
'''


def redirect_page(old, new):
    target = url(new)
    t = json.dumps(target)
    return f'''<!doctype html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<title>Moved to {E(target)}</title>
<link rel="canonical" href="{target}">
<meta name="robots" content="noindex,follow">
<meta http-equiv="refresh" content="0; url={target}">
<script>location.replace({t}+location.search+location.hash)</script>
</head>
<body>
<p>This page has moved (former path <code>/{old}/</code>). New address: <a href="{target}">{E(target)}</a></p>
</body>
</html>
'''


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    for f in (ROOT / "assets").iterdir():
        if f.is_file():
            shutil.copy(f, OUT / "assets" / f.name)
    latest = '<ol class="timeline">' + "".join(news_card(n) for n in NEWS[:4]) + "</ol>"
    for page in PAGES:
        slug, _, _, _, src, _, _ = page
        if slug == "news":
            body = page_news()
        elif slug == "resources":
            body = page_resources()
        else:
            body = (ROOT / "src/content" / src).read_text(encoding="utf-8")
            body = body.replace("{{LATEST_NEWS}}", latest).replace("{{FAQ}}", faq_html()).replace("{{ANALYTICS_TEXT}}", E(analytics_text()))
        d = OUT / slug if slug else OUT
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(with_base(layout(page, body)), encoding="utf-8")
    # Redirects from the former German paths (absolute URLs, so no with_base needed)
    slugs = {p[0] for p in PAGES}
    for old, new in REDIRECTS.items():
        assert new in slugs and old not in slugs, (old, new)
        (OUT / old).mkdir(parents=True, exist_ok=True)
        (OUT / old / "index.html").write_text(redirect_page(old, new), encoding="utf-8")
    # 404
    p404 = ("404", "", "Page not found", "This page does not exist (anymore).", None, False, "WebPage")
    (OUT / "404.html").write_text(with_base(layout(p404, '<div class="wrap"><h1>Page not found</h1><p>Back to the <a href="/">overview</a>.</p></div>')).replace('content="index,follow', 'content="noindex,follow'), encoding="utf-8")
    (OUT / "feed.xml").write_text(atom_feed(), encoding="utf-8")
    sm = "".join(f"<url><loc>{url(p[0])}</loc><lastmod>{SITE['last_updated']}</lastmod><changefreq>{'weekly' if p[0] in ('', 'news', 'resources') else 'monthly'}</changefreq></url>" for p in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    (OUT / "_headers").write_text("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: interest-cohort=()\n/assets/*\n  Cache-Control: public, max-age=86400\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    # Safety net: banned terms must never be published.
    # The list lives locally in scripts/banned-terms.txt (excluded from the repository via .gitignore).
    bf = ROOT / "scripts/banned-terms.txt"
    banned = [b.strip().lower() for b in bf.read_text(encoding="utf-8").splitlines() if b.strip() and not b.startswith("#")] if bf.exists() else []
    # In CI (GitHub Actions) the list comes from the repository secret BANNED_TERMS (one term per line or comma-separated).
    banned += [b.strip().lower() for b in re.split(r"[\n,]", os.environ.get("BANNED_TERMS", "")) if b.strip()]
    if not banned:
        print("Note: no banned-terms list found (scripts/banned-terms.txt / BANNED_TERMS) – check skipped.")
    for f in OUT.rglob("*"):
        if f.is_file() and f.suffix in (".html", ".xml", ".txt", ".js", ".css"):
            low = f.read_text(encoding="utf-8").lower()
            for b in banned:
                if b in low:
                    raise SystemExit(f"ABORT: banned term '{b}' found in {f}")
    print(f"OK: {len(PAGES)} pages, {len(REDIRECTS)} redirects, {len(NEWS)} news, {len(RES)} resources → {OUT}")


if __name__ == "__main__":
    main()
