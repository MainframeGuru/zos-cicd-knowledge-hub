#!/usr/bin/env python3
"""Statischer Site-Generator für den z/OS CI/CD Kompass.

Liest data/*.json und src/content/*.html und schreibt die fertige Website nach public/.
Keine Abhängigkeiten außer Python 3.8+. Aufruf:  python3 build.py
"""
import json, html, os, re, shutil, datetime
from pathlib import Path
from urllib.parse import quote, urlparse

ROOT = Path(__file__).parent
OUT = ROOT / "public"
SITE = json.loads((ROOT / "data/site.json").read_text(encoding="utf-8"))
NEWS = sorted(json.loads((ROOT / "data/news.json").read_text(encoding="utf-8")), key=lambda n: n["date"], reverse=True)
RES = json.loads((ROOT / "data/resources.json").read_text(encoding="utf-8"))
BASE = SITE["base_url"].rstrip("/")
# Pfad-Präfix aus base_url ableiten: "https://user.github.io/repo" -> "/repo", eigene Domain -> "".
# Alle root-absoluten Links (href="/…", src="/…") im erzeugten HTML werden damit automatisch präfixiert.
BASE_PATH = urlparse(BASE).path.rstrip("/")


def with_base(markup):
    """Präfixiert root-absolute interne Links/Assets mit BASE_PATH (lässt //cdn… und https://… unberührt)."""
    if not BASE_PATH:
        return markup
    return re.sub(r'((?:href|src|action)=")/(?!/)', lambda m: m.group(1) + BASE_PATH + "/", markup)
E = html.escape
MONTHS = ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni", "Juli", "Aug.", "Sep.", "Okt.", "Nov.", "Dez."]

RES_TYPES = [  # Reihenfolge = Filter-Reihenfolge. Neue Typen hier ergänzen.
    ("projektreferenz", "Projektreferenz / Case Study", "Öffentlich dokumentiertes Projekt mit benannter oder anonymisierter Organisation, veröffentlicht von Anwender, Hersteller oder Dienstleister."),
    ("erfahrungsbericht", "Erfahrungsbericht", "Anwender berichten in Interview, Blog oder Gespräch – weniger formal als eine Case Study."),
    ("vortrag", "Webinar / Vortrag / Präsentation", "Konferenzvortrag, Webinar, Panel, Demo oder Foliensatz (SHARE, GSE, TechXchange, Open Mainframe Summit …)."),
    ("whitepaper", "Whitepaper / Hersteller-Doku", "Dokumentation, Leitfäden, Produktseiten und Marketing von Herstellern oder Dienstleistern."),
    ("presse", "Presse / Fachartikel", "Berichte und Gastbeiträge in Fach- und Publikumsmedien sowie Pressemitteilungen."),
]
TYPE_LABEL = {k: v for k, v, _ in RES_TYPES}

FAQ = [
    ("Ist Git auf z/OS überhaupt verfügbar?", "Ja. Ein Git-Client für z/OS UNIX System Services wird u. a. über IBM Open Enterprise Foundation for z/OS bzw. die zopen Community bereitgestellt. Alternativ arbeiten Entwickler lokal (VS Code, Eclipse) und Builds laufen per SSH/Zowe auf z/OS."),
    ("Muss ich für CI/CD auf IBM DBB umsteigen?", "Nein. DBB ist eine verbreitete Option für abhängigkeitsbasierte Builds. Alternativen sind Broadcom Team Build, BMC AMI DevX Code Pipeline oder bestehende JCL-Builds, die von der Pipeline gestartet und überwacht werden."),
    ("Kann ich meinen Library Manager behalten?", "Ja. Endevor (Bridge for Git), ChangeMan ZMF und BMC Code Pipeline bieten Git-Integrationen für eine Koexistenz. Ob das dauerhaft oder als Übergang sinnvoll ist, wird in der Fachwelt unterschiedlich bewertet."),
    ("Wie lange dauert eine Migration?", "Öffentliche Beispiele reichen von wenigen Monaten für Pilotumfänge bis zu mehrjährigen Programmen. ANZ meldet ca. 40 Anwendungen in 8 Monaten. Entscheidend sind Volumen, Anzahl Prozessorvarianten, Testabdeckung und Schulungsaufwand."),
    ("Welche CI-Server funktionieren mit z/OS?", "Jenkins, GitLab CI (inkl. nativem z/OS-Runner), GitHub Actions und Azure DevOps sind öffentlich dokumentiert – meist mit Agent/Runner, der per SSH oder Zowe auf z/OS zugreift. IBM stellt Pipeline-Templates auf GitHub bereit."),
    ("Was passiert mit SCLM?", "IBM beabsichtigt laut aktualisiertem Statement of Direction (Okt. 2026), SCLM aus einem zukünftigen z/OS-Release zu entfernen. Ursprünglich war z/OS 3.2 als letztes Release genannt."),
]

PAGES = [
    # slug, Navigationslabel, Titel, Beschreibung, Content-Datei, in Navigation, Seitentyp
    ("", "Überblick", "CI/CD auf z/OS – Git, Pipelines & Migrationen verständlich erklärt", SITE["description"], "index.html", True, "WebPage"),
    ("warum-cicd", "Warum CI/CD", "Warum CI/CD auf dem Mainframe? Gründe, Nutzen, Risiken", "Fachkräfte, Git als Standard, Geschwindigkeit, Tests, Compliance und Kosten: die wichtigsten Gründe für CI/CD auf IBM z/OS – mit öffentlich belegten Beispielen und FAQ.", "warum-cicd.html", True, "Article"),
    ("migrationen", "Migrationen", "Migrationspfade: Endevor, ChangeMan ZMF, ISPW, SCLM → Git & CI/CD", "Neutraler Vergleich der Migrationspfade von Endevor, ChangeMan ZMF, ISPW/Code Pipeline, SCLM, Panvalet und Librarian zu Git, DBB und CI/CD – inklusive automatisierter Migrationsansätze.", "migrationen.html", True, "Article"),
    ("news", "Produkt-News", "Produkt-News CI/CD auf z/OS: IBM, Broadcom, BMC, Rocket, Zowe", "Datierte Produktneuheiten rund um Mainframe-DevOps: IBM DBB, Wazi Deploy, Endevor Bridge for Git, BMC AMI DevX, Zowe, Galasa, Rocket und mehr – filterbar nach Hersteller.", None, True, "CollectionPage"),
    ("ressourcen", "Ressourcen", "Case Studies, Vorträge & Artikel zu Mainframe-CI/CD", "Kuratierte, klar gekennzeichnete Quellen: Projektreferenzen, Erfahrungsberichte, Vorträge/Webinare, Whitepaper und Presseartikel zu Git und CI/CD auf z/OS.", None, True, "CollectionPage"),
    ("impressum", "Impressum", "Impressum", "Impressum und Haftungsausschluss des z/OS CI/CD Kompass.", "impressum.html", False, "WebPage"),
    ("datenschutz", "Datenschutz", "Datenschutz", "Datenschutzhinweise: keine Cookies, keine Drittanbieter-Skripte, optionale cookielose Reichweitenmessung.", "datenschutz.html", False, "WebPage"),
]


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
    return f"{int(parts[2])}. {MONTHS[m-1]} {y}"


def analytics_snippet():
    a = SITE.get("analytics", {})
    p = a.get("provider", "none")
    if p == "cloudflare" and "HIER" not in a.get("cloudflare_token", "HIER"):
        tok = json.dumps({"token": a["cloudflare_token"]})
        return f"<script defer src=\"https://static.cloudflareinsights.com/beacon.min.js\" data-cf-beacon='{tok}'></script>"
    if p == "goatcounter" and "HIER" not in a.get("goatcounter_code", "HIER"):
        return f'<script data-goatcounter="https://{E(a["goatcounter_code"])}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
    return "<!-- Analytics deaktiviert (data/site.json → analytics.provider) -->"


def analytics_text():
    p = SITE.get("analytics", {}).get("provider", "none")
    if p == "cloudflare":
        return ("Wir nutzen Cloudflare Web Analytics. Es werden keine Cookies gesetzt und keine personenbezogenen Profile gebildet; "
                "gemessen werden aggregierte Seitenaufrufe, Referrer, Land und Gerätetyp. Anbieter: Cloudflare, Inc. [Rechtsgrundlage/Drittlandtransfer ergänzen].")
    if p == "goatcounter":
        return ("Wir nutzen GoatCounter (goatcounter.com), eine cookielose, datensparsame Open-Source-Statistik. "
                "Gemessen werden aggregierte Seitenaufrufe, Referrer, Browser, Bildschirmgröße und Land; IP-Adressen werden nicht gespeichert. [Rechtsgrundlage ergänzen].")
    return "Derzeit findet keine Reichweitenmessung statt. Falls aktiviert, wird ausschließlich ein cookieloses Verfahren (Cloudflare Web Analytics oder GoatCounter) eingesetzt; dieser Abschnitt wird dann aktualisiert."


LOGO = '<svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#0b7a75"/><path d="M8 11h16M8 16h10M8 21h16" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><circle cx="23" cy="16" r="2.6" fill="#7ee2d9"/></svg>'


def share_block(page_url, title):
    u, t = quote(page_url, safe=""), quote(title, safe="")
    return f'''<aside class="share" aria-label="Seite teilen">
  <span class="muted small">Teilen:</span>
  <a href="https://www.linkedin.com/sharing/share-offsite/?url={u}" rel="noopener" target="_blank">LinkedIn</a>
  <a href="https://x.com/intent/post?url={u}&amp;text={t}" rel="noopener" target="_blank">X</a>
  <a href="https://mastodonshare.com/?url={u}&amp;text={t}" rel="noopener" target="_blank">Mastodon</a>
  <a href="mailto:?subject={t}&amp;body={u}">E-Mail</a>
  <a href="{E(page_url)}" data-copy="url">Link kopieren</a>
</aside>'''


def cite_block(page_url, title):
    today = SITE["last_updated"]
    txt = f'{SITE["name"]}: „{title}“. Stand {fmt_date(today)}. Online: {page_url} (abgerufen am TT.MM.JJJJ).'
    return f'''<details class="cite-box"><summary>Zitieren</summary>
<p class="small muted">Vorschlag für eine Quellenangabe (Abrufdatum anpassen). Einzelne Einträge haben eigene Anker-Links (¶).</p>
<div class="cite">{E(txt)}</div>
<p><button class="chip" type="button" data-copy="{E(txt)}">Zitat kopieren</button></p></details>'''


def json_ld(page):
    slug, _, title, desc, _, _, ptype = page
    graph = [
        {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": SITE["name"], "description": SITE["description"], "inLanguage": "de"},
        {"@type": ptype, "@id": url(slug) + "#page", "url": url(slug), "name": title, "description": desc, "inLanguage": "de",
         "isPartOf": {"@id": BASE + "/#website"}, "dateModified": SITE["last_updated"],
         "image": BASE + "/assets/og-image.png"},
    ]
    if ptype == "Article":
        graph[1].update({"headline": title, "author": {"@type": "Organization", "name": SITE["name"]}, "datePublished": "2026-11-19"})
    if slug:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Überblick", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": page[1], "item": url(slug)}]})
    if slug == "warum-cicd":
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]})
    if slug == "news":
        graph.append({"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": url("news") + "#news-" + n["id"], "name": n["title"]} for i, n in enumerate(NEWS)]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def layout(page, body):
    slug, nav_label, title, desc, _, _, _ = page
    full_title = f"{title} | {SITE['name']}" if slug else f"{SITE['name']} – {title}"
    page_url = url(slug)
    cur = ' aria-current="page"'
    nav = "".join(
        '<li><a href="/' + (p[0] + "/" if p[0] else "") + '"' + (cur if p[0] == slug else "") + '>' + E(p[1]) + '</a></li>'
        for p in PAGES if p[5])
    tw = f'<meta name="twitter:site" content="{E(SITE["twitter_handle"])}">' if SITE.get("twitter_handle") else ""
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full_title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{page_url}">
<link rel="alternate" hreflang="de" href="{page_url}">
<link rel="alternate" hreflang="x-default" href="{page_url}">
<link rel="alternate" type="application/atom+xml" title="{E(SITE['name'])} – Produkt-News" href="/feed.xml">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0b7a75">
<meta property="og:type" content="{"article" if page[6] == "Article" else "website"}">
<meta property="og:site_name" content="{E(SITE['name'])}">
<meta property="og:locale" content="{SITE['locale']}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{page_url}">
<meta property="og:image" content="{BASE}/assets/og-image.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(SITE['name'])}: CI/CD auf z/OS">
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
<a class="skip" href="#main">Zum Inhalt springen</a>
<header class="site"><div class="wrap nav">
  <a class="brand" href="/">{LOGO}<span>{E(SITE['name'])}</span></a>
  <button class="icon-btn menu-btn" id="menu-toggle" aria-controls="menu" aria-expanded="false" aria-label="Menü">☰</button>
  <nav aria-label="Hauptnavigation"><ul id="menu">{nav}</ul></nav>
  <button class="icon-btn" id="theme-toggle" type="button" aria-label="Farbschema wechseln" hidden>◐</button>
</div></header>
<main id="main">
{body}
<div class="wrap">{share_block(page_url, title)}{cite_block(page_url, title)}</div>
</main>
<footer class="site"><div class="wrap cols">
  <div><b>{E(SITE['name'])}</b><br>{E(SITE['tagline'])}.<br>Herstellerneutral · keine Cookies · keine Tracker von Drittanbietern.</div>
  <div>Zuletzt aktualisiert: <time datetime="{SITE['last_updated']}">{fmt_date(SITE['last_updated'])}</time><br>
  <a href="/feed.xml">Atom-Feed</a> · <a href="/sitemap.xml">Sitemap</a><br>
  <a href="/impressum/">Impressum</a> · <a href="/datenschutz/">Datenschutz</a></div>
  <div class="small">Marken gehören ihren Inhabern. Angaben ohne Gewähr; Quellen sind jeweils verlinkt.</div>
</div></footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="/assets/app.js" defer></script>
</body>
</html>
'''


def news_card(n, heading="h3"):
    extra = "".join(f' · <a href="{E(l["url"])}" rel="noopener">{E(l["label"])}</a>' for l in n.get("extra_links", []))
    tags = "".join(f'<span class="tag">{E(t)}</span>' for t in n.get("tags", []))
    aid = "news-" + n["id"]
    return f'''<li><article class="card" id="{aid}" data-vendor="{E(n['vendor'])}">
  <div class="meta"><time datetime="{n['date'][:7] if n.get('date_precision') == 'month' else n['date']}">{fmt_date(n['date'], n.get('date_precision'))}</time><span class="badge v">{E(n['vendor'])}</span><span>{E(n['product'])}</span></div>
  <{heading}>{E(n['title'])}<a class="anchor" href="/news/#{aid}" aria-label="Link zu diesem Eintrag" title="Link zu diesem Eintrag">¶</a></{heading}>
  <p>{E(n['summary'])}</p>
  <p class="small">Quelle: <a href="{E(n['url'])}" rel="noopener">{E(n['source'])}</a>{extra}</p>
  <div class="tags">{tags}</div>
</article></li>'''


def page_news():
    vendors = []
    for n in NEWS:
        if n["vendor"] not in vendors:
            vendors.append(n["vendor"])
    chips = '<button class="chip" type="button" data-value="alle" aria-pressed="true">Alle</button>' + "".join(
        f'<button class="chip" type="button" data-value="{E(v)}" aria-pressed="false">{E(v)} ({sum(1 for n in NEWS if n["vendor"] == v)})</button>' for v in vendors)
    items = "\n".join(news_card(n, "h2") for n in NEWS)
    return f'''<div class="wrap">
<header class="page-head"><span class="eyebrow">Produkt-News</span><h1>Produkt-News: CI/CD und DevOps auf z/OS</h1>
<p class="lead">Datierte Neuheiten von Herstellern und Open-Source-Projekten – jeweils mit Primärquelle. Neueste zuerst. <a href="/feed.xml">Als Atom-Feed abonnieren</a>.</p></header>
<div data-filter-root="vendor">
  <div class="filters" role="group" aria-label="Nach Hersteller filtern" hidden>{chips}</div>
  <p><input class="search" type="search" placeholder="In News suchen …" aria-label="In News suchen" hidden> <span class="count" aria-live="polite">{len(NEWS)} Einträge</span></p>
  <ol class="timeline" data-filter-list>
{items}
  </ol>
</div>
<p class="muted small">Datumsangaben mit Monatsgenauigkeit stammen aus Fix-Listen oder Release-Übersichten ohne Tagesdatum.</p>
</div>'''


def res_card(r):
    extra = "".join(f' · <a href="{E(l["url"])}" rel="noopener">{E(l["label"])}</a>' for l in r.get("extra_links", []))
    rows = []
    for k, lbl in (("org", "Organisation"), ("from", "Von"), ("to", "Nach / Werkzeuge"), ("event", "Veranstaltung"), ("format", "Format")):
        v = r.get(k)
        if v and v not in ("—", "k. A."):
            rows.append(f"<b>{lbl}:</b> {E(v)}")
    aid = "res-" + r["id"]
    date = f'<time datetime="{E(r["date"])}">{fmt_date(r["date"])}</time>' if r.get("date") else ""
    return f'''<li><article class="card" id="{aid}" data-type="{r['type']}">
  <div class="meta"><span class="badge t-{r['type']}">{E(TYPE_LABEL[r['type']])}</span>{date}<span>{E(r['publisher'])}</span></div>
  <h3>{E(r['title'])}<a class="anchor" href="/ressourcen/#{aid}" aria-label="Link zu diesem Eintrag" title="Link zu diesem Eintrag">¶</a></h3>
  <p>{E(r['summary'])}</p>
  <p class="small">{" · ".join(rows)}</p>
  <p class="small"><a href="{E(r['url'])}" rel="noopener">Zur Quelle →</a>{extra}</p>
  <p class="small muted">{E(r.get('note', ''))}</p>
</article></li>'''


def page_resources():
    chips = '<button class="chip" type="button" data-value="alle" aria-pressed="true">Alle</button>' + "".join(
        f'<button class="chip" type="button" data-value="{k}" aria-pressed="false">{E(v)} ({sum(1 for r in RES if r["type"] == k)})</button>' for k, v, _ in RES_TYPES)
    legend = "".join(f'<div class="card"><span class="badge t-{k}">{E(v)}</span><p class="small">{E(d)}</p></div>' for k, v, d in RES_TYPES)
    order = {k: i for i, (k, _, _) in enumerate(RES_TYPES)}
    items = "\n".join(res_card(r) for r in sorted(RES, key=lambda r: (order[r["type"]], -int((r.get("date") or "0")[:4]))))
    return f'''<div class="wrap">
<header class="page-head"><span class="eyebrow">Ressourcen</span><h1>Case Studies, Erfahrungsberichte, Vorträge &amp; Artikel</h1>
<p class="lead">Jede Quelle ist eindeutig gekennzeichnet. Wichtig: Eine <b>Projektreferenz</b> dokumentiert ein konkretes Vorhaben; ein <b>Vortrag/Webinar</b> ist nicht automatisch eine Referenz; <b>Whitepaper</b> und Herstellerseiten sind Marketing bzw. Dokumentation.</p></header>
<h2 class="small muted" style="margin-top:1rem">Kennzeichnung</h2>
<div class="grid">{legend}</div>
<div data-filter-root="type" style="margin-top:2rem">
  <div class="filters" role="group" aria-label="Nach Quellentyp filtern" hidden>{chips}</div>
  <p><input class="search" type="search" placeholder="Suchen (z. B. Endevor, GitLab, Bank) …" aria-label="Ressourcen durchsuchen" hidden> <span class="count" aria-live="polite">{len(RES)} Einträge</span></p>
  <ul class="grid" style="list-style:none;padding:0" data-filter-list>
{items}
  </ul>
</div>
<div class="info small">Fehlt eine öffentliche Quelle? Hinweise sind willkommen (siehe <a href="/impressum/">Impressum</a>). Aufgenommen werden nur Einträge mit öffentlich erreichbarer URL.</div>
</div>'''


def faq_html():
    return "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQ)


def atom_feed():
    upd = SITE["last_updated"] + "T00:00:00Z"
    entries = []
    for n in NEWS:
        link = url("news") + "#news-" + n["id"]
        entries.append(f'''<entry><title>{E(n['title'])}</title><link href="{link}"/><id>{link}</id>
<updated>{n['date']}T00:00:00Z</updated><category term="{E(n['vendor'])}"/>
<summary>{E(n['summary'])} Quelle: {E(n['url'])}</summary></entry>''')
    return f'''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="de">
<title>{E(SITE['name'])} – Produkt-News</title>
<subtitle>{E(SITE['tagline'])}</subtitle>
<link href="{BASE}/feed.xml" rel="self"/><link href="{url('news')}"/>
<id>{BASE}/feed.xml</id><updated>{upd}</updated><author><name>{E(SITE['name'])}</name></author>
{"".join(entries)}
</feed>
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
        elif slug == "ressourcen":
            body = page_resources()
        else:
            body = (ROOT / "src/content" / src).read_text(encoding="utf-8")
            body = body.replace("{{LATEST_NEWS}}", latest).replace("{{FAQ}}", faq_html()).replace("{{ANALYTICS_TEXT}}", E(analytics_text()))
        d = OUT / slug if slug else OUT
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(with_base(layout(page, body)), encoding="utf-8")
    # 404
    p404 = ("404", "", "Seite nicht gefunden", "Diese Seite existiert nicht (mehr).", None, False, "WebPage")
    (OUT / "404.html").write_text(with_base(layout(p404, '<div class="wrap"><h1>Seite nicht gefunden</h1><p>Zurück zum <a href="/">Überblick</a>.</p></div>')).replace('content="index,follow', 'content="noindex,follow'), encoding="utf-8")
    (OUT / "feed.xml").write_text(atom_feed(), encoding="utf-8")
    sm = "".join(f"<url><loc>{url(p[0])}</loc><lastmod>{SITE['last_updated']}</lastmod><changefreq>{'weekly' if p[0] in ('', 'news', 'ressourcen') else 'monthly'}</changefreq></url>" for p in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    (OUT / "_headers").write_text("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: interest-cohort=()\n/assets/*\n  Cache-Control: public, max-age=86400\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    # Sicherheitsnetz: verbotene Begriffe dürfen nie veröffentlicht werden
    # Liste liegt lokal in scripts/banned-terms.txt (per .gitignore NICHT im Repository).
    bf = ROOT / "scripts/banned-terms.txt"
    banned = [b.strip().lower() for b in bf.read_text(encoding="utf-8").splitlines() if b.strip() and not b.startswith("#")] if bf.exists() else []
    # In CI (GitHub Actions) kommt die Liste aus dem Repository-Secret BANNED_TERMS (eine Zeile oder Komma je Begriff).
    banned += [b.strip().lower() for b in re.split(r"[\n,]", os.environ.get("BANNED_TERMS", "")) if b.strip()]
    if not banned:
        print("Hinweis: keine Schutzliste gefunden (scripts/banned-terms.txt / BANNED_TERMS) – Prüfung übersprungen.")
    for f in OUT.rglob("*"):
        if f.is_file() and f.suffix in (".html", ".xml", ".txt", ".js", ".css"):
            low = f.read_text(encoding="utf-8").lower()
            for b in banned:
                if b in low:
                    raise SystemExit(f"ABBRUCH: verbotener Begriff '{b}' in {f}")
    print(f"OK: {len(PAGES)} Seiten, {len(NEWS)} News, {len(RES)} Ressourcen → {OUT}")


if __name__ == "__main__":
    main()
