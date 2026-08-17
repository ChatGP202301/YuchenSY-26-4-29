# Repository audit

Audit date: 2026-08-17. The audit was read-only. Production and Staging were not changed.

## Repository identity and release topology

- GitHub repository: `ChatGP202301/YuchenSY-26-4-29` (public).
- Production source: `main@a383110a874971b977586942fa8511375543e713`.
- Full-site Staging source: `codex/staging-site-20260817@ed62f00d38996a92a18d822a50d00aa3b09b182b`.
- Control branch base: the exact Staging commit above. AI GEO implementation is isolated on `codex/ai-geo-system-v1`.
- Deployment model: GitHub Pages serves static files from the repository root. `CNAME` binds production to `www.yuchensy.com`.
- The GitHub repository is a public-output repository. Local generators, the SEO controller and Worker source are not all present on the remote output branch. Merging the control plane into `main` would expose internal files through Pages, so it is not allowed.
- No pre-existing GitHub Actions workflow was present on either recorded release commit. Repository auto-merge is disabled and branch protection has not been independently verified.

## Site inventory

The frozen local scanner found:

- 64 scopes: the root plus 62 active language directories and one legacy `sr-me` scope.
- 14,189 static HTML files.
- 13,942 unique sitemap URLs, 13,942 entries and zero duplicates.
- Static assets include images, CSS, JavaScript and fonts. There is no runtime template engine in the public output tree.
- Root and language directories contain home, product/category, product-detail, about/brand, contact/lead, blog/news and catalog/download-oriented pages.
- `robots.txt`, `llms.txt`, root sitemap indexes and language sitemaps are public release files.

## Existing SEO and content signals

- Pages contain self-canonical links and multilingual `hreflang` sets.
- The site uses Title, Meta Description and H1 in generated static HTML.
- JSON-LD includes page-dependent organization, product, service, breadcrumb and related types.
- The frozen controller checks sitemap membership, canonical and hreflang integrity, language leakage, duplicate content, page structure and GEO/AEO signals.
- Local GSC assets and read-only adapters exist outside the public output branch. No GSC evidence was loaded into this baseline, so protected-page decisions default to L2.
- Local evidence uses JSON, CSV and SQLite in existing tools. The new control plane uses immutable JSONL as fact source and rebuildable SQLite for queries.

## Frozen acceptance baseline

`site_quality_control.scan_site(Path('.'))` returned:

| Measure | Result |
|---|---:|
| Scopes | 64 |
| HTML pages | 14,189 |
| Unique sitemap URLs | 13,942 |
| Duplicate sitemap entries | 0 |
| Critical failures | 0 |
| High failures | 125 |
| Macro score | 98.36 |
| Audit fingerprint | `a36b469cf0c2d0bf9d8006160c0054686a78aa1ea60378fcdf496dc304961cef` |

The score is a local quality indicator, not a ranking or citation prediction. The controller, regression helper and accepted contract are frozen under `ai-geo/vendor/frozen-site-quality/` with SHA-256 values in `MANIFEST.json`.

## Dual-environment operating rule

- `https://www.yuchensy.com/` is the only target for real public HTTP, indexability and AI citation observation. It is read-only.
- The protected/noindex Staging preview is not an AI citation target. It is used for local page structure analysis, proposed overlays, before/after SEO guards and human preview.
- Candidate content is never applied by this system. It produces task specifications and proposed-patch metadata only.
- A one-off Russian homepage timeout remains an unverified network observation, not a 404 or modification trigger.

## Safety conclusion

The safest architecture is a control branch that reads public production evidence and analyzes the frozen Staging tree. Unknown page ownership, missing GSC evidence, existing citation, high-value signals or any protected technical change prevent L1. Production publication remains a separate, human-approved release operation.
