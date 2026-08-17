---
name: yuchen-ai-citation-operator
description: Audit Yuchen Water multilingual AI citations, discover localized buyer prompts, import verifiable AI evidence, compare cited competitors with current pages, measure citation hypotheses, and draft SEO-safe GEO tasks. Use for AI citation monitoring, GEO gap analysis, multilingual prompt research, citation experiments, or post-deployment retesting where production safety and factual provenance are mandatory.
---

# Yuchen AI Citation Operator

Operate the citation system as a control plane. Observe the public production site read-only, evaluate candidate changes from the Staging Git ref, and never treat the protected Staging URL as a real citation target.

## Run the safe workflow

1. Run `python3 ai-geo/cli.py doctor` and stop modification work when any baseline, mode, credential, repository, or protection check is unknown.
2. Run `python3 ai-geo/cli.py discover-prompts` to build localized prompts. Preserve local terminology, units, country, intent, product, and channel; do not translate English prompts mechanically.
3. Run `sample` only for a configured free adapter. Import consumer-web evidence with `import`; never automate consumer webpages or label API evidence as web evidence.
4. Run `analyze` and `features audit`. Keep fixture, unverified manual, and live evidence in separate denominators.
5. Run `draft-tasks`. Require a real citation gap, source-backed page evidence, trusted facts, verified page ownership, and all guards before assigning L1.
6. Run `report`. Do not claim that internal scores, the 23 external hypotheses, or observed changes predict rankings or citations.
7. Register an exact deployment commit and date before running `retest`; otherwise return `NOT_SCHEDULED`.

## Enforce the safety boundary

- Keep `AI_GEO_MODE=DRY_RUN` by default. Generate overlays, proposed patches, diffs, tasks, and reports only.
- Treat missing evidence, missing GSC, unknown ownership, unstable models, or unclear facts as L2/L3, never L1.
- Never change URLs, canonical, hreflang, robots, sitemap, CNAME, workflows, permissions, navigation, build settings, or unverified product facts.
- Never copy competitor prose. Extract only structure, topic coverage, specifications present/missing, FAQ form, schema, and citation evidence.
- Reject paid fallback, secret logging, PII, raw answer storage, fake citations, fake dates, keyword stuffing, doorway pages, hidden text, or unsupported claims.
- Keep scheduled observation read-only. Require separate human approval for any dispatcher workflow, PR merge, deployment, or repository-permission change.

Read [references/policy.md](references/policy.md) for risk and deployment rules. Read [references/schemas.md](references/schemas.md) before creating or importing records.
