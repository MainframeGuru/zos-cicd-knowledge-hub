# Changelog

Format based on “Keep a Changelog”. Date format YYYY-MM-DD.

## [2.0.0] – 2026-11-19
### Changed
- **Site language switched to English** (international topic and audience): all pages, product news,
  resources, FAQ, UI strings (filters, buttons, share/cite blocks, 404), date format (e.g. “Nov 19, 2026”),
  Atom feed, sitemap, JSON-LD, Open Graph/Twitter meta, `hreflang="en"`, `<html lang="en">`, `og:locale` `en_US`.
- New site name: **z/OS CI/CD Compass** (formerly “z/OS CI/CD Kompass”); new tagline and description.
- English URL slugs: `/why-cicd/`, `/migrations/`, `/resources/`, `/imprint/` (German legal notice “Impressum”), `/privacy/`.
- Resource type keys renamed to English (`case-study`, `experience`, `talk`, `whitepaper`, `press`) with English labels.
- OG preview image regenerated with the English name.
- `scripts/check_site.py` now also checks internal `#anchor` links and the legacy redirects.
- README, build script comments and messages translated to English.

### Added
- Redirect pages for the former German paths (`/warum-cicd/`, `/migrationen/`, `/ressourcen/`, `/impressum/`,
  `/datenschutz/`): meta refresh + JS redirect preserving query and anchor, `rel=canonical` to the new URL, `noindex`.
- Mapping of old German filter values in shared URLs (e.g. `?type=projektreferenz`) to the new keys.

### Unchanged
- Anchor IDs (`#news-…`, `#res-…`, section IDs) are stable, so deep links keep working.
- No content facts added or removed; translation only.

## [1.1.0] – 2026-11-19
### Changed
- Published on GitHub Pages (https://mainframeguru.github.io/zos-cicd-knowledge-hub/) via GitHub Actions.
- `build.py`: base path support (derived from `base_url`) for links, assets, feed, sitemap, canonical, OG and JSON-LD.
- New script `scripts/check_site.py` for checking internal links on the live site.

## [1.0.0] – 2026-11-19
### Added
- Initial website (in German): overview, why CI/CD (incl. FAQ), migrations (path table, per source system, automated migration approaches, pitfalls, approach model), product news (24 entries, vendor filter, search), resources (39 entries in 5 categories, filter + search), imprint and privacy placeholders.
- Generator `build.py` (JSON → static HTML), Atom feed, sitemap, robots.txt, 404, `_headers`.
- SEO: individual titles/descriptions, canonical, hreflang, Open Graph/Twitter cards, OG image, JSON-LD (WebSite, WebPage/Article, CollectionPage, BreadcrumbList, FAQPage, ItemList).
- Share links without third-party scripts, anchor links per entry, citation suggestion.
- Dark/light mode, responsive layout, skip link, focus styles.
- Switchable cookieless analytics (Cloudflare Web Analytics / GoatCounter).
- Link checker `scripts/check_links.py`.
