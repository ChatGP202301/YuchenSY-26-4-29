# Multilingual AI Citation & GEO System v1

Implementation date: 2026-08-17. Status: DRY_RUN hardened; local Gemini proof is credential-blocked; no production change.

## What was created

- Repository Skill: `.agents/skills/yuchen-ai-citation-operator/`.
- Standard-library engine: `ai-geo/` with configuration, Prompt Discovery, adapters, citation evidence, immutable JSONL, rebuildable SQLite, page/competitor analysis, 23-factor observations, guards, experiments, reporting, regression planning, learning and Git simulation.
- Unified commands: `doctor`, `discover-prompts`, `sample`, `import`, `analyze`, `draft-tasks`, `report`, `retest`, `run`, `features audit`, `features explain`, and `features compare`.
- Inactive read-only workflow definition: `.github/workflows/ai-geo-observe.yml` contains daily 02:00, Monday 03:00 and day-one 04:00 UTC schedules, but it exists only on a non-default control branch.
- 61 control-branch adversarial tests and a deterministic fixture loop.

## Languages and prompts

- Detected scopes: 64. Language records: 63.
- Phase 1 enabled: English and Russian.
- Spanish and French remain configured at priority 2 but disabled until Phase 3.
- Other languages are detected/configurable and have zero live budget.
- Fixture discovery produces 20 English plus 20 Russian locally phrased prompts across manufacturer, supplier, price, product, technical, comparison, application, problem, selection, maintenance and FAQ intents.
- Discovery configuration retains EN/RU 40, ES/FR 25; live Gemini hard caps are EN 20, RU 20, ES/FR 0.

## Citation evidence and integrations

- Gemini API runs only when `GEMINI_API_KEY` exists, `AI_GEO_FREE_TIER_CONFIRMED=true`, and the configured budget remains USD 0. Missing credentials return `SKIPPED_NO_CREDENTIAL` without a network call.
- Every Gemini request explicitly enables the Google Search grounding tool. Only `source=curated_local_v1` public Prompts are accepted. Raw answers and plaintext search queries are discarded; only an answer hash, grounding state, query count/hashes and citation metadata are retained.
- The local grounded-proof path selects exactly two English and two Russian Prompts, has a total hard cap of four and writes only to an absolute path under `/private/tmp`. HTTP 403/429 stops the remaining sample without retry, model switch or paid fallback.
- ChatGPT, Google AI web, Perplexity, DeepSeek, Yandex AI, Grok, Copilot and Yuanbao are manual/external-import adapters. The system does not automate consumer web interfaces or use paid fallbacks.
- Every record carries prompt, channel/surface, model/interface, answer hash, citations, positions, timestamps, source type and verification state.
- Manual evidence without a stable evidence URL or screenshot hash is not verified and is excluded from metrics.
- `fixture`, `manual` and `live` denominators are separate. The fixture never contributes to live citation rate.
- A non-fixture run without real competitor evidence now returns `competitor_evidence=no-data` and creates zero competitor gaps, Codex tasks and experiments. Synthetic `example-competitor.test` evidence exists only in the explicit fixture path.

## 23 external hypotheses

The Zyppy list is stored as 23 `correlation_hypothesis` records. The article's 54-source statement and supplied image's 55-source statement are both preserved. The supplied truncated image hash is labelled `partial_user_supplied`; no full hash was invented.

Seventeen factors are direct/hybrid observations. Search Rank, Fan-out Rank, Topic Cluster Ranking, Brand/Entity Trust, Known Source and Domain Authority remain `no-data` without external evidence. Author scores are display-only and cannot affect L1/L2/L3, thresholds, deletion, ranking prediction or internal composite scores. Feature comparison is explicitly descriptive and provides no causal guarantee.

## Page, competitor and internal metrics

- Page Analyzer checks canonical, hreflang, robots, Title, description, H1/H2/H3, links, image alt, Schema and visible text.
- AI Answer Extractability uses 16 configured questions and reports both score and applicable coverage. It is an internal trend metric.
- Public competitor retrieval is HTTPS/443 GET only, same-origin redirects only, fail-closed robots, public-IP validation, 500 ms throttle, 12-second timeout and 512 KiB maximum. Only structure and coverage gaps are retained; competitor prose is not copied.
- Internal AI Visibility weights are 30/15/15/10/10/10/10 for citation frequency, position, Prompt coverage, language coverage, commercial-intent coverage, brand/product mention and inverse competitor share. Missing inputs return `no-data`, not zero. This is not an industry standard.

## L1, L2 and L3 behavior

- L1 eligibility is limited to small FAQ, factual paragraph, internal link, image alt, truthful Schema addition, Meta Description, natural-language or extractability changes. It still requires verified citation gap, verified page ownership, non-protected GSC status, trusted facts, no cooling, safe diff and all guards.
- L2 covers Title, H1, major rewrites/reorganization, keywords, templates/navigation, unknown ownership, unknown GSC, protected/high-value pages, existing AI-cited pages, failed content/SEO/diff evidence or incomplete evidence.
- L3 denies URL/page deletion, canonical/hreflang/robots/sitemap/domain/workflow/permission operations and protected files including `.github/**`, `CNAME`, robots, sitemap, lock files and deployment configuration.
- Unknown means REVIEW_REQUIRED or DENIED, never L1.

## Content and SEO guards

- `trusted-facts.json` starts with only the verified organization name and domain. Certification, approval, warranty, customer, performance, price, export, capacity, experience, test-result and related facts remain UNKNOWN without exact evidence.
- Content Guard blocks unsupported absolute wording, fake freshness, unverified certifications/performance and Schema claim stacking.
- Diff Guard enforces 5 daily pages, 10 weekly pages, 20 files, 500 changed lines and 3% deletion ratio.
- SEO Guard compares canonical, hreflang, robots, Schema errors, H1 count and whole-site HTML/sitemap/indexable/broken/404 counts. Unexpected drift blocks publication.
- A 14-day cooling period prevents repeated page optimization.

## Git, deployment and rollback

- Default runtime is `AI_GEO_MODE=DRY_RUN`. It writes only to a selected artifact/overlay directory, simulates branch/commit/PR metadata and never commits, pushes, merges or deploys pages.
- Current `allow_auto_merge=false` and unverified branch protections force any requested AUTO_L1 back to DRY_RUN with `REQUIRES_GITHUB_PERMISSION`.
- The workflow has only `contents: read`. It has no Pages, write, administration, merge, deployment or revert job.
- A severe technical regression may only produce an `emergency-revert` branch and PR for an exact AI-owned commit. It never writes directly to main and never auto-merges. Traffic, ranking and citation decline remain REVIEW_REQUIRED.
- `AI_GEO_ENABLED=false` changes scheduled runs to health/status reporting only.

## Test and fixture evidence

- Control-branch AI GEO tests: 61/61 pass; no skip/todo. These are the tests reproducible from this public control branch.
- Separate local source-workspace Python baseline: 71/71 pass. Those private/local controller tests are not carried by this public output branch and are external baseline evidence, not remote PR CI.
- Separate local source-workspace Worker baseline: 45/45 pass; no skip/todo. Worker source is likewise absent from the public control branch.
- Fixture loop: 40 prompts, 40 fixture citations, 46 page-factor observations, two competitor gaps, two L2 Codex tasks, two experiments, daily/weekly/monthly reports, SQLite rebuild and undeployed retest plans.
- Repeating the same fixture run produces no duplicate facts and identical table counts.
- Frozen site baseline after implementation: 64 scopes, 14,189 HTML, 13,942 unique sitemap URLs, zero duplicate entries, Critical 0, High 125, macro 98.36 and unchanged fingerprint `a36b469cf0c2d0bf9d8006160c0054686a78aa1ea60378fcdf496dc304961cef`.
- Public page/content files changed by this implementation: zero.

## Validation limitations

- `quick_validate.py` cannot run because the bundled Python lacks PyYAML. No dependency was added. Ruby parsed `openai.yaml`, and tests enforce the same frontmatter/interface/body constraints.
- No Gemini Key was provided. A real four-Prompt proof selection ran locally from `/private/tmp`: two EN plus two RU records were selected and all four returned `SKIPPED_NO_CREDENTIAL` without a network call. This is a credential-gate result, not a citation observation.
- No GSC import was present, so page protection fails closed to L2.
- No production dispatcher is installed. GitHub Actions and the scheduler are configured but inactive: the workflow is on a non-default control branch and has not executed remotely.
- AUTO_L1 is implemented as a gated state but deliberately unavailable under current repository settings.

## Current status

```text
AI GEO SYSTEM STATUS
Repository audit: PASS
Languages detected: 64 scopes / 63 language records
Languages enabled: en, ru
DRY_RUN: ENABLED
AUTO_L1: DISABLED
SEO Guard: PASS
Content Guard: PASS
Risk Guard: PASS
Protected Files Guard: PASS
GitHub Actions: CONFIGURED_INACTIVE
Scheduler: CONFIGURED_INACTIVE
Remote CI: NOT_EXECUTED
Tests: PASS (61 control-branch AI GEO; external baselines 71 Python + 45 Worker)
Production modified: NO
Human actions required: create a free Gemini Key for public Prompts and store it in macOS Keychain; do not enable a dispatcher yet.
```
