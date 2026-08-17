# Operating the AI Citation Skill

Run commands from the repository root with Python 3. The default is DRY_RUN.

## Health and deterministic fixture

```sh
python3 ai-geo/cli.py doctor
python3 ai-geo/cli.py run --fixture --site-root . --output /tmp/yuchen-ai-geo-fixture
```

The fixture creates 40 EN/RU prompts and exercises import, feature measurement, gap analysis, task drafting, reporting, SQLite rebuild and undeployed retest plans. It never contributes to live metrics.

## Discover and sample prompts

```sh
python3 ai-geo/cli.py discover-prompts --languages en ru --per-language 20 --output /tmp/prompts.jsonl
python3 ai-geo/cli.py sample --prompts /tmp/prompts.jsonl --language en --engine gemini_api --limit 20 --output /tmp/gemini-status.json
```

Without a Key the second command returns `SKIPPED_NO_CREDENTIAL`. A Key is only used when `AI_GEO_FREE_TIER_CONFIRMED=true` and budget is zero.

## Import human or external evidence

Provide CSV, JSON or JSONL with the required prompt/platform/time fields, citations and either `evidence_url` or `screenshot_sha256` for a verified manual record. CSV stores its citations array in a `citations_json` column:

```sh
python3 ai-geo/cli.py import --input /tmp/manual-results.jsonl --output /tmp/citations.jsonl
python3 ai-geo/cli.py analyze --citations /tmp/citations.jsonl --output /tmp/citation-summary.json
```

Do not import raw answers, credentials or PII. Store only answer hashes and evidence references.

## Explain, audit and compare the 23 hypotheses

```sh
python3 ai-geo/cli.py features explain query_answer_match
python3 ai-geo/cli.py features audit --site-root . --page en/products.html --language en --output /tmp/features.jsonl
python3 ai-geo/cli.py features compare --before /tmp/before.jsonl --after /tmp/after.jsonl --citation-before 0.10 --citation-after 0.15
```

The comparison is descriptive and never claims causality.

## Experiments and retests

```sh
python3 ai-geo/cli.py retest --experiment /tmp/experiments.jsonl --output /tmp/retests.json
```

The result remains `NOT_SCHEDULED` until an experiment has both an exact deployment commit and deployment date. Only then are days 7, 14 and 30 scheduled.

## Stop and AUTO_L1 behavior

```sh
AI_GEO_ENABLED=false python3 ai-geo/cli.py run --site-root . --output /tmp/health-only
AI_GEO_MODE=AUTO_L1 python3 ai-geo/cli.py doctor
```

The first is health-only. The second currently returns `REQUIRES_GITHUB_PERMISSION` and downgrades to DRY_RUN. Do not change the repository policy file to bypass external protection checks.
