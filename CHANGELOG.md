# Changelog

Format angelehnt an „Keep a Changelog“. Datumsformat JJJJ-MM-TT.

## [1.1.0] – 2026-11-19
### Geändert
- Veröffentlichung auf GitHub Pages (https://mainframeguru.github.io/zos-cicd-knowledge-hub/) per GitHub Actions.
- `build.py`: Basis-Pfad-Unterstützung (aus `base_url` abgeleitet) für Links, Assets, Feed, Sitemap, Canonical, OG und JSON-LD.
- Neues Skript `scripts/check_site.py` zur Prüfung interner Links der Live-Seite.

## [1.0.0] – 2026-11-19
### Hinzugefügt
- Initiale Website: Überblick, Warum CI/CD (inkl. FAQ), Migrationen (Pfadtabelle, je Quellsystem, automatisierte Migrationsansätze, Stolpersteine, Vorgehensmodell), Produkt-News (24 Einträge, Filter nach Hersteller, Suche), Ressourcen (39 Einträge in 5 Kategorien, Filter + Suche), Impressum- und Datenschutz-Platzhalter.
- Generator `build.py` (JSON → statisches HTML), Atom-Feed, Sitemap, robots.txt, 404, `_headers`.
- SEO: individuelle Titel/Beschreibungen, Canonical, hreflang, OpenGraph/Twitter Cards, OG-Bild, JSON-LD (WebSite, WebPage/Article, CollectionPage, BreadcrumbList, FAQPage, ItemList).
- Teilen-Links ohne Drittanbieter-Skripte, Anker-Links je Eintrag, Zitiervorschlag.
- Dark/Light-Mode, responsives Layout, Skip-Link, Fokus-Stile.
- Schaltbare cookielose Analytics (Cloudflare Web Analytics / GoatCounter).
- Linkprüfung `scripts/check_links.py`.
