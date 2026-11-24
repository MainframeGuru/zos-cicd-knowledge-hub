# Changelog

Format based on “Keep a Changelog”. Date format YYYY-MM-DD.

## [2.2.3] – 2026-11-24
### Added
- News: IBM Z Atlas public preview – system intelligence and change orchestration for z/OS (backfill, 27 Oct 2026;
  `/news/#news-ibm-z-atlas-preview-2026-10`).
- Resources (Press / Article): DevOps.com, “Mainframe AI Is Stuck at the Keyboard. The Pipeline Is Why” (Techstrong
  PulseMeter poll, 145 respondents; `/resources/#res-devops-com-mainframe-ai-pipeline-2026-11`).
- Overview page: context figure on AI use in mainframe delivery (poll via DevOps.com).
- Migrations page: approvals pitfall extended with “approvals and evidence as pipeline outputs”; ISPW/Code Pipeline
  section notes CycloneDX SBOM generation (BMC) and Team Build `sbomz` (Broadcom).
### Changed
- Migrations page: deadlines table as of 24 Nov 2026; Zowe 2.18.7 row states that release artifacts were not yet
  published on the scheduled GA date at the time of the check.

## [2.2.2] – 2026-11-23
### Added
- News: Git for z/OS (zopen community port) with encoding-aware 3-way merges and opt-in transliteration
  (`/news/#news-zopen-git-encoding-2026-11`); Zowe security-driven breaking changes in minor/maintenance releases incl.
  V2 2.18.7 (`/news/#news-zowe-security-breaking-changes-2026-11`); DBB Git Migration Modeler 2.0.0
  (`/news/#news-dbb-git-migration-modeler-2-0-2026-09`); IBM Bob Premium Package for Z self-hosted option
  (`/news/#news-ibm-bob-premium-z-self-hosted-2026-09`).
- Migrations page: stable anchors for each pitfall (`#pitfall-codepages`, `#pitfall-metadata`, `#pitfall-processors`,
  `#pitfall-approvals`, `#pitfall-people`); deep links open the collapsed section automatically.
### Changed
- Migrations page: code page pitfall mentions the Git for z/OS encoding improvements; automated-migration card notes
  DBB Git Migration Modeler 2.0; deadlines table (as of 23 Nov 2026) flags Zowe 2.18.7 as a release with breaking changes.
- Resources: DBB Git Migration Modeler entry updated for version 2.0.0.

## [2.2.1] – 2026-11-21
### Added
- Legal pages published in English and German: Imprint (`/imprint/`), Privacy policy (`/privacy/`),
  Impressum (`/impressum/`) and Datenschutzerklärung (`/datenschutz/`), each with a link to the other language version.
- Footer on every page links all four legal pages; hreflang alternates pair imprint↔impressum and privacy↔datenschutz
  (x-default = English); German pages use `lang="de"` and are listed in the sitemap.
### Changed
- `/impressum/` and `/datenschutz/` are now real German pages instead of redirects to the English pages;
  `scripts/check_site.py` checks them as German pages.
- Placeholder legal texts replaced by the final versions.

## [2.2.0] – 2026-11-20
### Added
- Migrations page: new section “Support deadlines & lifecycle dates” (`/migrations/#deadlines`) with publicly announced
  dates (watsonx Code Assistant for Z Validation Assistant final release, Zowe V2 end of support 30 Mar 2027,
  Endevor Bridge for Git 2.x end of service 30 Jun 2027, SCLM removal intent), linked from the TOC and the overview page.
- News: Rocket Transaction Platform (`/news/#news-rocket-transaction-platform-2026-11`); Zowe V2 end of support and
  remaining V2 maintenance releases (`/news/#news-zowe-v2-eos-2026-10`).
- Resources (Webinar / Talk): GS UK Forge 2026 talk “Orchestrate Mainframe Application Deployments”
  (`/resources/#res-gsuk-2026-orchestrate-deployments`) and the Open Mainframe stream incl. Zowe MCP Server
  (`/resources/#res-gsuk-2026-omp-stream`).
### Changed
- SEO: resources page now emits an `ItemList` in its JSON-LD (one entry per resource anchor), like the news page.

## [2.1.1] – 2026-11-19
### Added
- News: IBM Developer for z/OS EE 18.0 / ADFz 6.0 with DBB 4.0, Wazi Deploy 4.0 and the new Release Orchestrator for Z
  (`/news/#news-ibm-idzee-18-adfz-6-2026-10`); Broadcom Endevor read-only MCP bridge beta (`/news/#news-endevor-mcp-beta-2026-02`).
- BMC October 2026 release entry: link to the BMC AMI Agentics press release (20 Oct 2026).
- Resources: CROZ article on DBB 4 and Release Orchestrator (`/resources/#res-croz-dbb4-release-orchestrator`, labeled Press / Article).
### Changed
- Migrations page, “Application boundaries & repo layout”: note on DBB 4.0 cross-application dependencies; DBB 4.0 added to sources.

## [2.1.0] – 2026-11-19
### Added
- Q Group AG and its Q-Wing tool (Endevor → Git migration with history and archive) on the migrations page:
  Endevor section (Atruvia and dwpbank projects), the “Service provider tools & accelerators” card and a new
  comparison table “Migration tooling at a glance” (`/migrations/#tools-vergleich`) that also covers IBM, Broadcom,
  BMC, Royal Cyber, Living Mainframe and CROZ based on their public information.
- Resources: project references Atruvia (`#res-atruvia-qgroup`) and dwpbank (`#res-dwpbank-qgroup`), vendor pages
  Q-Wing (`#res-qgroup-qwing`) and IDz4VSE (`#res-qgroup-idz4vse`).
- News: IBM Expert Labs success story on the dwpbank migration (`#news-qgroup-dwpbank-success-story-2026-06`).
- Overview page: context figure for the Atruvia migration.

## [2.0.1] – 2026-11-19
### Changed
- Dropped prominent self-labels such as “vendor-neutral” and “independent” from the site tagline,
  meta description, hero eyebrow, footer, Open Graph image, migrations page, imprint, README and
  the GitHub repository description. The site remains factually even-handed (all vendors, sources labeled);
  the words simply no longer appear as a slogan.

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
