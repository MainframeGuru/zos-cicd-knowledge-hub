# z/OS CI/CD Compass

An English-language knowledge site about CI/CD, Git and DevOps on IBM z/OS.
Static, no framework, no cookies, no third-party scripts.

Live: https://mainframeguru.github.io/zos-cicd-knowledge-hub/

## Structure

```
data/site.json        Name, base URL (incl. path), last-updated date, language/locale, analytics switch (SINGLE config point)
data/news.json        Product news (one line = one entry; newest are sorted first automatically)
data/resources.json   Case studies, experience reports, talks, whitepapers, press
src/content/*.html    Editorial pages (overview, why CI/CD, migrations, imprint, privacy)
assets/               CSS, JS, favicon, OG preview image (og-image.png, 1200x630)
build.py              Generator: produces public/ (HTML, feed.xml, sitemap.xml, robots.txt, 404.html, _headers, legacy redirects)
scripts/check_links.py  Checks all external links in the build
scripts/check_site.py   Crawls the live site and checks all internal links/assets, #anchors and legacy redirects
.github/workflows/pages.yml  Build + deployment to GitHub Pages on every push to main
scripts/og-template.html  Template for the OG image (regeneration see below)
```

All content is rendered to plain HTML at build time (fully crawlable, works without JS).
JavaScript only adds filters, search, the dark-mode toggle and “Copy link”.

## Pages and URLs

| Page | Path | Source |
|---|---|---|
| Overview | `/` | `src/content/index.html` |
| Why CI/CD | `/why-cicd/` | `src/content/why-cicd.html` (+ FAQ in `build.py`) |
| Migrations | `/migrations/` | `src/content/migrations.html` |
| Product news | `/news/` | `data/news.json` |
| Resources | `/resources/` | `data/resources.json` |
| Imprint | `/imprint/` | `src/content/imprint.html` – this is the German legal notice (“Impressum”, § 5 DDG) |
| Privacy | `/privacy/` | `src/content/privacy.html` |

**Legacy redirects:** v1 of the site was in German. The former paths `/warum-cicd/`, `/migrationen/`, `/ressourcen/`,
`/impressum/` and `/datenschutz/` are generated as small redirect pages (meta refresh + JS redirect that keeps
`?query` and `#anchor`, `rel=canonical` to the new URL, `noindex`). They are configured in `build.py` → `REDIRECTS`
and are not listed in the sitemap. Anchor IDs (`#news-…`, `#res-…` and section IDs) were kept unchanged.

## Live site & deployment

Every push to `main` builds the site via GitHub Actions (`python3 build.py`) and publishes `public/` to GitHub Pages.
`public/` is not committed.

**Base path:** `build.py` derives the path from `data/site.json` → `base_url` (here `/zos-cicd-knowledge-hub`) and
prefixes all internal links automatically. For a custom domain, `"base_url": "https://www.example.org"`
(without path) plus a custom domain in the Pages settings is enough.

## Build and preview locally

```bash
python3 build.py
mkdir -p /tmp/srv && ln -sfn "$PWD/public" /tmp/srv/zos-cicd-knowledge-hub
python3 -m http.server 8000 -d /tmp/srv   # → http://localhost:8000/zos-cicd-knowledge-hub/
python3 scripts/check_site.py http://localhost:8000/zos-cicd-knowledge-hub/   # internal links, anchors, redirects
python3 scripts/check_links.py           # external links (403 = usually bot protection, check manually)
```

## Adding product news

Add an object to `data/news.json`:

```json
{"id":"vendor-product-2026-12", "date":"2026-12-01", "vendor":"IBM", "product":"IBM DBB",
 "title":"…", "summary":"2–3 factual sentences, no marketing.", "tags":["Build"],
 "url":"https://primary-source…", "source":"IBM Documentation",
 "extra_links":[{"label":"Secondary source","url":"https://…"}]}
```

- `id` is permanent (anchor link `news/#news-<id>`); never change it afterwards.
- Set `date_precision: "month"` if only the month is known.
- `vendor`: a new value automatically creates a new filter chip.

## Adding a resource

In `data/resources.json`:

```json
{"id":"short-unique", "type":"case-study", "date":"2026-12", "title":"…",
 "org":"Organization or 'anonymized'", "publisher":"Who published it?",
 "from":"Source system", "to":"Target tools", "summary":"…", "url":"https://…",
 "note":"Note on the source, e.g. 'Published by the vendor'",
 "format":"Webinar|Conference talk|Slides|Demo video (talks only)", "event":"SHARE 2026 (optional)"}
```

Allowed `type` values (defined in `build.py` → `RES_TYPES`, extensible there):

| type | Label | When |
|---|---|---|
| `case-study` | Project reference / Case study | concrete, publicly documented project |
| `experience` | Experience report | user interview, blog, conversation |
| `talk` | Webinar / Talk / Presentation | conference, webinar, panel, demo, slides |
| `whitepaper` | Whitepaper / Vendor docs | docs, guides, product pages, marketing |
| `press` | Press / Article | media reports, guest articles, press releases |

Editorial rules: only entries with a real, verified URL; no invented customers or figures;
label vendor sources as such; keep `last_updated` in `data/site.json` current.
Old German filter values in shared URLs (e.g. `?type=projektreferenz`) are mapped to the new keys in `assets/app.js`.

## Enabling analytics

Set `data/site.json` → `analytics.provider` to `"cloudflare"` or `"goatcounter"` and enter the token/code.
Without a valid token no script is included. The privacy page adapts its text automatically.

## Regenerating the OG image

```bash
google-chrome --headless=new --no-sandbox --hide-scrollbars --window-size=1200,630 \
  --screenshot=assets/og-image.png file://$PWD/scripts/og-template.html
```

## Banned-terms list (optional, local)

If `scripts/banned-terms.txt` exists (one term per line), `build.py` aborts as soon as one of these terms
appears in the generated site. The file is excluded from the repository via `.gitignore`.
In GitHub Actions the same list can optionally be stored as the repository secret `BANNED_TERMS`.
