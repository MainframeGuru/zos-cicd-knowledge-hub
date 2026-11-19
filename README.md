# z/OS CI/CD Kompass

Herstellerneutrale, deutschsprachige Wissensseite zu CI/CD, Git und DevOps auf IBM z/OS.
Statisch, ohne Framework, ohne Cookies, ohne Drittanbieter-Skripte.

## Struktur

```
data/site.json        Name, Basis-URL (inkl. Pfad), Stand-Datum, Analytics-Schalter (EINZIGE Konfigurationsstelle)
data/news.json        Produkt-News (eine Zeile = ein Eintrag, neueste werden automatisch zuerst sortiert)
data/resources.json   Case Studies, Erfahrungsberichte, Vorträge, Whitepaper, Presse
src/content/*.html    Redaktionelle Seiten (Überblick, Warum CI/CD, Migrationen, Impressum, Datenschutz)
assets/               CSS, JS, Favicon, OG-Vorschaubild (og-image.png, 1200x630)
build.py              Generator: erzeugt public/ (HTML, feed.xml, sitemap.xml, robots.txt, 404.html, _headers)
scripts/check_links.py  Prüft alle externen Links im Build
scripts/check_site.py   Crawlt die Live-Seite und prüft alle internen Links/Assets
.github/workflows/pages.yml  Build + Deployment auf GitHub Pages bei jedem Push auf main
scripts/og-template.html  Vorlage für das OG-Bild (Neu-Erzeugung siehe unten)
```

Alle Inhalte werden zur Build-Zeit als fertiges HTML gerendert (voll crawlbar, funktioniert ohne JS).
JavaScript ergänzt nur Filter, Suche, Dark-Mode-Umschalter und „Link kopieren“.

## Live-Seite & Deployment

Live: https://mainframeguru.github.io/zos-cicd-knowledge-hub/

Jeder Push auf `main` baut die Seite per GitHub Actions (`python3 build.py`) und veröffentlicht `public/` auf GitHub Pages.
`public/` wird nicht eingecheckt.

**Basis-Pfad:** `build.py` leitet aus `data/site.json` → `base_url` den Pfad ab (hier `/zos-cicd-knowledge-hub`) und
präfixiert alle internen Links automatisch. Für eine eigene Domain genügt `"base_url": "https://www.example.org"`
(ohne Pfad) plus Custom Domain in den Pages-Einstellungen.

## Lokal bauen und ansehen

```bash
python3 build.py
mkdir -p /tmp/srv && ln -sfn "$PWD/public" /tmp/srv/zos-cicd-knowledge-hub
python3 -m http.server 8000 -d /tmp/srv   # → http://localhost:8000/zos-cicd-knowledge-hub/
python3 scripts/check_site.py http://localhost:8000/zos-cicd-knowledge-hub/   # interne Links
python3 scripts/check_links.py           # Linkprüfung (403 = meist Bot-Schutz, manuell prüfen)
```

## Neue Produkt-News hinzufügen

In `data/news.json` ein Objekt ergänzen:

```json
{"id":"hersteller-produkt-2026-12", "date":"2026-12-01", "vendor":"IBM", "product":"IBM DBB",
 "title":"…", "summary":"2–3 sachliche Sätze, keine Werbung.", "tags":["Build"],
 "url":"https://primärquelle…", "source":"IBM Documentation",
 "extra_links":[{"label":"Zweitquelle","url":"https://…"}]}
```

- `id` ist dauerhaft (Anker-Link `news/#news-<id>`), nie nachträglich ändern.
- `date_precision: "month"` setzen, wenn nur der Monat bekannt ist.
- `vendor`: neuer Wert erzeugt automatisch einen neuen Filter-Chip.

## Neue Ressource hinzufügen

In `data/resources.json`:

```json
{"id":"kurz-eindeutig", "type":"projektreferenz", "date":"2026-12", "title":"…",
 "org":"Organisation oder 'anonymisiert'", "publisher":"Wer hat es veröffentlicht?",
 "from":"Quellsystem", "to":"Zielwerkzeuge", "summary":"…", "url":"https://…",
 "note":"Hinweis zur Quelle, z. B. 'Vom Hersteller veröffentlicht'",
 "format":"Webinar|Konferenzvortrag|Folien|Demo-Video (nur bei Vorträgen)", "event":"SHARE 2026 (optional)"}
```

Zulässige `type`-Werte (definiert in `build.py` → `RES_TYPES`, dort erweiterbar):

| type | Label | Wann |
|---|---|---|
| `projektreferenz` | Projektreferenz / Case Study | konkretes, öffentlich dokumentiertes Projekt |
| `erfahrungsbericht` | Erfahrungsbericht | Anwender-Interview, -Blog, -Gespräch |
| `vortrag` | Webinar / Vortrag / Präsentation | Konferenz, Webinar, Panel, Demo, Folien |
| `whitepaper` | Whitepaper / Hersteller-Doku | Doku, Leitfaden, Produktseite, Marketing |
| `presse` | Presse / Fachartikel | Medienberichte, Gastbeiträge, Pressemitteilungen |

Redaktionsregeln: nur Einträge mit echter, geprüfter URL; keine erfundenen Kunden/Zahlen;
Herstellerquellen als solche kennzeichnen; Stand-Datum in `data/site.json` → `last_updated` pflegen.

## Analytics aktivieren

`data/site.json` → `analytics.provider` auf `"cloudflare"` oder `"goatcounter"` setzen und Token/Code
eintragen. Ohne gültigen Token wird kein Skript eingebunden. Die Datenschutzseite passt ihren Text automatisch an.

## OG-Bild neu erzeugen

```bash
google-chrome --headless=new --no-sandbox --hide-scrollbars --window-size=1200,630 \
  --screenshot=assets/og-image.png file://$PWD/scripts/og-template.html
```

## Schutzliste (optional, lokal)

Liegt `scripts/banned-terms.txt` vor (eine Zeile pro Begriff), bricht `build.py` ab, sobald einer dieser
Begriffe in der generierten Seite auftaucht. Die Datei ist per `.gitignore` vom Repository ausgeschlossen.
In GitHub Actions kann dieselbe Liste optional als Repository-Secret `BANNED_TERMS` hinterlegt werden.
