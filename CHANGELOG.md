# Changelog

Format based on “Keep a Changelog”. Date format YYYY-MM-DD.

## [2.2.11] – 2026-11-26
### Changed
- Case studies (HCSC, ANZ, CSE, dwpbank): summaries follow the sources’ wording more closely (e.g. HCSC “without
  production-impacting defects”, CSE “software factory approach”).
- Migrations page, support deadlines table: IBM row lists the IBM announcement as a second source and states IBM Docs’ scope
  (“no additional Validate releases are planned”); Explorer for Endevor row uses the listing’s wording; SCLM row reads
  “Future z/OS release, per IBM” with IBM’s Statement of Direction sentence. The same SCLM sentence is used in the tooling
  table, the SCLM section and the SCLM news entry.
### Removed
- Zowe V2 end-of-support row and news entry: the sentence on a GS UK Forge 2026 session.
- Bridge for Git 2.x news entry: the Java requirement sentence and the link to the 3.0 software requirements (added in 2.2.10).
- SCLM news entry: the closing assessment sentence.
- Bridge for Git 3.0 news entry (Oct 2025): the Java requirement mention; the summary now follows Broadcom’s announcement.

## [2.2.10] – 2026-11-26
### Changed
- Resources, Open Mainframe Project TechXchange 2026 track report: event line now reads “IBM TechXchange 2026 (Atlanta);
  OMP sessions on 26 and 27 Oct 2026”; the sentence on session videos follows the blog’s wording and date.
- Case studies (Nedbank, HCSC, BMC DataStream): the figure in the headline is also given in the summary, attributed in the
  sentence like all other case-study figures.
- Migrations page, support deadlines table: dates that have passed are shown in the source’s own wording and attributed in
  the cell (“GA date per Zowe release schedule”, “Release plan per Marketplace listing”, “Final release per IBM Docs”);
  “(done)” only where the source confirms the release. Cells state only what the linked sources say (Explorer for Endevor,
  Zowe V2 end of support, Bridge for Git wording aligned to the sources).
- News: Zowe security breaking changes and Zowe CLI 8.44.0 entries state only what the sources say; IBM Bob Premium Package
  for Z title uses IBM’s wording (“an evolution of watsonx Code Assistant for Z”); Bridge for Git 2.x entry follows
  Broadcom’s letter and links the 3.0 software requirements.
### Removed
- News, Zowe CLI 8.44.0: the npm tag remark dated 25 Nov 2026.

## [2.2.9] – 2026-11-26
### Added
- Resources (Talk): Open Mainframe Project track report from IBM TechXchange 2026, published 19 Nov 2026
  (`/resources/#res-techxchange-2026-omp-track-report`).
### Changed
- Migrations page, support deadlines table: removed two availability remarks dated 25 Nov 2026 (Zowe 2.18.7 downloads,
  Explorer for Endevor Marketplace version); table date set to 26 Nov 2026.

## [2.2.8] – 2026-11-25
### Changed
- Case studies: figures and outcomes are attributed in the sentence (“According to the case study: …”, “According to the
  service provider’s case study: …”, “According to the reference (in German): …”), the same way for every publisher.
- Undated resources (Atruvia, dwpbank) no longer show a date line, like the other undated case studies.
- Fields a source does not specify are shown uniformly as not set (“n/a” values normalized).
### Removed
- News entry for the IBM Expert Labs dwpbank success story: the source states no publication date, so it cannot be placed in the
  chronological news list. The story remains listed under Resources (`/resources/#res-dwpbank-qgroup`).

## [2.2.7] – 2026-11-25
### Changed
- Case studies and the dwpbank news entry: notes state the publisher and source type only; the added sentence from 2.2.6
  and the earlier verification remarks were removed.
- Atruvia, dwpbank and the dwpbank news entry: only the date added to the site is shown where the source gives no date.
- ANZ case study “From” field, BMC DataStream, a webinar note and a trade-portal note: neutral source-type wording.
- dwpbank case study: deployment statement attributed to the story.
- Overview page (`#numbers`): note under the figures now reads “Each figure is shown with its source and publisher.”
- Migrations tooling table, IBM row: the SCLM-to-Git tool reads SCLM; other legacy SCMs are unloaded to PDS first (per IBM).

## [2.2.6] – 2026-11-25
### Added
- Resources (Whitepaper / Vendor docs): Techstrong PulseMeter report “The Orchestration Challenge in Mainframe Software
  Delivery” (poll of 145, sponsored by BMC; `/resources/#res-techstrong-pulsemeter-mainframe-delivery-2026-11`).
### Changed
- Overview page (`#numbers`) and migrations page (`#pitfall-approvals`): the AI-use figures are now attributed to the
  PulseMeter report (25% deployment automation, 26% security and compliance automation); the DevOps.com article on the
  poll is labeled as sponsored content.
- Resource `#res-devops-com-mainframe-ai-pipeline-2026-11`: the source’s “Sponsored Content” label is stated.
- Case studies: notes harmonized (see 2.2.7).
- Site description and preview image: “linked sources” instead of “verified sources”.

## [2.2.5] – 2026-11-25
### Changed
- Overview and migrations pages: English section anchors (`#what-is-cicd-on-zos`, `#building-blocks`, `#numbers`,
  `#automated-migration`, `#tooling-comparison`, `#approach`); the previous IDs (`#was-ist-cicd-auf-zos`, `#bausteine`,
  `#zahlen`, `#automatisiert`, `#tools-vergleich`, `#vorgehen` and heading IDs) stay as hidden aliases, so existing
  links keep working. Other existing IDs (e.g. `#tabelle`, `#stolpersteine`, `#aktuell`) are unchanged.
- News vendor label “Markt & Studien” renamed to “Market & surveys”; old filter value in shared URLs is mapped.
- Atruvia, dwpbank and the dwpbank news entry: attribution to the IBM Expert Labs success stories, timelines as stated
  in the stories, and an “added” date instead of a publication date where the source states none.
- Q-Wing entry and tooling table: archive targets as stated on the product page and in the success stories.
- Tooling table and resource notes: wording aligned with the editorial policy (factual, attributed descriptions);
  Royal Cyber and CROZ rows corrected.
- Support deadlines: neutral status wording for Explorer for Endevor 2.0.0 and Zowe 2.18.7.
### Removed
- Resource “Mainframe releases are a team sport” (CROZ blog), as the source is no longer available.

## [2.2.4] – 2026-11-25
### Added
- News: Zowe CLI 8.44.0 – REST responses above 64 MiB fail by default, new `--max-response-bytes` option
  (`/news/#news-zowe-cli-8-44-response-limit-2026-11`).
- Resources (Webinar / Talk): Rocket ChangeMan ZMF Virtual User Group, 10 and 15 Dec 2026 – new VS Code extension,
  roadmap and new Git integration (`/resources/#res-rocket-changeman-zmf-user-group-2026-12`).
- Resources (Whitepaper / Vendor docs): PopUp Mainframe “Getting to Git” (`/resources/#res-popup-mainframe-getting-to-git`).
- Migrations page: PopUp Mainframe row in the tooling table (`#tools-vergleich`) and in the service-provider card;
  ChangeMan section notes the announced Git integration; deadlines table row for Explorer for Endevor 2.0.0
  (REST API v1 removal, planned end of Oct 2026, not yet released).
- News page JSON-LD: ItemList entries are now `NewsArticle` items with headline, `datePublished` and source URL.
### Changed
- Migrations page: deadlines table as of 25 Nov 2026; Zowe 2.18.7 still listed without artifacts.
- Resources: CROZ article on DBB 4 / Release Orchestrator flagged as no longer available at its source (HTTP 404)
  (`/resources/#res-croz-dbb4-release-orchestrator`).

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
