# BB housings: keyword, intent and inquiry-path adversarial review
Date: 2026-11-05. Scope: 16 housing pages, collection, 2 accessories. Self-review; no claim of independent human expert review or measured conversion improvement.

## Findings and corrections
1. Collection title/H1 and hero omitted the main BB category despite detail-page changes. Corrected title to 10 & 20 Inch Filter Housings | Big Blue-style BB | Yuchen; H1 now names Big Blue-style (BB) options. First paragraph distinguishes medium-body from BB and blue assemblies from black/clear/blue singles. Does not label medium-body as BB.
2. Collection journey lacked an explicit decision sequence. Added compare → confirm → inquire explanation, retaining search, first-position black cards, independent product pages and prefilled contact form. No fake urgency, prices or certification badges.
3. Prior audit treated keyword occurrence as evidence of correct terminology. Changed to source-supported taxonomy, exclusions and product/intent mapping. No numeric search-volume estimates invented.
4. Black products were merely options. Two independent black singles now lead collection; appropriate existing large-body singles link to same-size black variant. No unsupported black assemblies or medium-body options.
5. Keyword-driven slug changes would unnecessarily migrate 14 live URLs. Preserve their paths and self-canonicals; add exactly two black URLs.
6. Image confidence: 10-inch black image remains a disclosed illustrative derivative, not a camera original. This prevents treating a plausible image as a verified engineering drawing. Actual 10-inch photo is a remaining trust improvement.

## Raw evidence and limits
- Product source screenshots, owner specification confirmations, original black photo. Source fields and URL/keyword allocation: bb-page-keywords.csv; generated products.json.
- Manufacturer terminology: https://www.pentair.com/content/dam/extranet/web/nam/pentek/spec-sheets/310053-pentek-big-blue-spec-sheet.pdf and https://www.pentair.com/en-us/home-water-treatment/filter-housings/big-blue-heavy-duty-series.html . Reference only for language/category observations. Their pressure/temperature/NSF/compatibility claims DO NOT transfer to Yuchen.
- No raw GSC query dataset, customer verbatim inquiry set, verified keyword volumes, production conversion funnel or platform citation sessions acquired. These cannot be presented as completed research.

## Keyword and intent dispositions
| Cluster / candidate | Intended use | Disposition |
|---|---|---|
| water filter housing, 10/20 inch filter housing | category discovery | collection title/H1; applicable detail size/specification |
| Big Blue filter housing, BB filter housing | BB category discovery | Big Blue-style (BB) explicitly explained; large singles/assemblies only, no brand origin assertion |
| 10/20 inch BB-style housing | precise size | corresponding title/H1/meta/schema and quotation identity |
| black filter housing, 10/20 inch black BB housing | colour-specific procurement | two dedicated pages and leading cards; genuine black reference source |
| blue / clear BB-style housing | appearance choice | corresponding pages; clear does not imply material or pressure rating |
| 10 x 4.5 / 20 x 4.5 housing | dimensional selection | supplier size designation, not external dimensions or universal cartridge fit |
| two/three-stage BB housing assembly, wall bracket, support frame | configuration comparison | eight blue assemblies; do not imply included media or removal performance |
| housing brass-insert/plastic-thread ports | connection selection | product-specific choices; no inferred BSP/NPT |
| housing packing quantity, cartridges sold separately | purchasing/inclusions | visible specification and product-specific questions |
| request filter housing quotation | supplier inquiry | top/bottom direct form links, product/selection prefill |
| Big Black, BB10/BB20, jumbo, large diameter, whole-house | adjacent/competitor terminology | research leads, not automatically mandatory copy. Avoid unconfirmed model aliases/branding and unsupported end-use claims; explain size directly |
| Pentair/Pentek manufacturer, competitor SKU, NSF certified, 100 psi, high flow | brand/performance demand | EXCLUDED: not evidence for these products |
| OEM/ODM, MOQ, wholesale price, food-grade, BPA-free | commercial/performance claims | no new unsupported claims; carton quantity not MOQ; quotation for prices |

Coverage means relevant intents have truthful landing sections; it does not mean every permutation of every competitor term is forced into copy. No density target or hidden text. Candidate wording does not establish search demand.

## Customer path and failure analysis
- Entry: H1 identifies general housings AND BB subset; hero says cold water and cartridges excluded. Potential failure: visitor mistakes BB for blue colour or medium-body. Explicit definition corrects this.
- Discovery: black first, named photos and links, search by actual size/colour/mount. Potential failure: filter hides all items. Zero-result count and clear-to-18 are checked.
- Evaluation: one page/product, packing, ports, options, stage/mount differences, related same-size black. Potential failure: wrong interface copied across variants. 10-inch two-stage wall-bracket exception locked by checks.
- Conversion: top/bottom link opens existing contact form and carries actual selected product/options; client adds quantity, destination and contact details. Potential failure: generic product name, stale options or mismatched form. 16 handoffs tested, no messages submitted.
- Delivery: backend unchanged. Form navigation/prefill success does NOT prove inbox delivery, lead quality, sales response or purchase probability. No conversion claim without data.

## SEO/GEO and platform boundary
Unique metadata/H1, self-canonicals, visible body, product-specific JSON-LD without fabricated offers/reviews, crawlable related links and sitemap. These are foundations, not proof of Google index or ChatGPT/Perplexity selection. No special markup promises AI inclusion. Current GSC write/session blockers remain separate. No citation/ranking guarantee.

## Validation and remaining limits
verify-bb.py: deliberately missing black, wrong colour, wrong port must fail; restored source passes; canonical/schema/sitemap/URL preservation and zero-change regeneration checked.
verify-split.cjs: 16 pages x 5 viewport widths, H1/product count, canonical, decoded images, document horizontal overflow; frame/black/unknown/clear search cases.
verify-bb-inquiry.cjs: 16 product-specific form handoffs, selected ports preserved, no actual forms sent.
These tests are not proof of every possible overlap, real iPad/iPhone hardware behaviour, screen-reader usability, subjective attractiveness or conversion lift. Review screenshots and list untested conditions honestly. Publish only with appropriate release authority; this revision is GitHub review first.

## Minimal next experiment (not a promise or standing automation)
After an authorized release and usable analytics access, establish inquiry-click → form arrival → successful submission baseline and review real non-brand queries. Use the existing measurement setup if available, add no tracking authority silently. Judge actual qualified inquiries, not keyword count. No schedule or experiment was executed in this review.

Verification refresh: 80 layout cases and 16 form handoffs rerun after the BB collection headline/hero and three-step guide changes. See split-browser-results.json; no publication performed.

Screenshot-driven finding: initial expanded three-step guide pushed product cards too far below the hero, especially on 375px. Shortened introductory copy and converted the guide to an accessible native details/summary disclosure (not JS-only content). Rebuilt before repeating deterministic/viewport checks. Earlier screenshot files represent the pre-correction layout; recapture for final review.

## Final delivery audit
The earlier compact per-product map has been supplemented by keyword-intent-evidence.csv: each row explicitly records term, procurement intent, product fact, visible landing section, source and unmeasured-demand status. Core terms and actual intent answers are distinguished from literal permutation coverage.
Additional control obstruction checks: verify-controls.cjs passed 80 page/viewport combinations and 330 controls (top/bottom inquiry links and product selectors). Each control is inside horizontal viewport bounds, its centre hit target is the control or descendant, and programmatic focus succeeds. Results: control-check-results.json. This does not test every possible overlap, native select popup, physical device or screen reader.
Final collection screenshots were recaptured after shortening the hero and collapsing the guide: deep-collection-1440.png, deep-collection-768.png, deep-collection-375.png. No actual form messages sent. No merge/publication performed.
