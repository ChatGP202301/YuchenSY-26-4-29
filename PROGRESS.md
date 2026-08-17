# PROGRESS

1. Restored true Git history/remote and based the isolated control branch on Staging `ed62f00d`.
2. Recorded production `a383110a` and kept production/Staging release commits unchanged.
3. Added the repository Skill, standard-library engine, 63-language config and 23 correlation hypotheses.
4. Added Prompt, evidence, competitor/page, task, experiment, retest, reporting and learning loops.
5. Enforced DRY_RUN, zero budget, manual-only consumer surfaces and fail-closed L1 ownership/GSC gates.
6. Added read-only schedules and no deployment/merge/revert permissions.
7. RED found path/evidence/idempotency defects; GREEN fixed them; new tests 51/51.
8. Baselines pass: original Python 71/71, Worker 45/45, combined Python 122/122.
9. Site baseline unchanged: 64 / 14,189 / 13,942 / Critical 0 / fingerprint `a36b469c…61cef`.

## Gemini grounded proof hardening — 2026-08-17

1. Goal: make one bounded Gemini API proof capable of testing two EN and two RU public prompts with explicit Google Search grounding.
2. Order: freeze repository refs and tests; add RED safety tests; implement grounding and four-call sampling; isolate live from fixture; correct reports; rerun all gates.
3. Scope is limited to the task whitelist; public site files, workflow, production and Staging remain read-only.
4. Maximum risk: treating synthetic competitor evidence or ungrounded model output as a live citation observation.
5. Secrets must remain process-only; no API key or raw answer may enter Git, logs, reports or stored results.
6. Initial refs verified: tree `588a62ccf1855c43459f99205925618aecdce9bc`, production `a383110a874971b977586942fa8511375543e713`, Staging `ed62f00d38996a92a18d822a50d00aa3b09b182b`.
7. Initial reproducible control-branch tests pass 51/51; the separately held local Worker baseline passes 45/45 with the bundled Node runtime.
8. RED evidence: 61 tests ran with two failures and seven errors, exposing missing grounding, unsafe HTTP failure handling, public-input enforcement gaps, missing four-Prompt/output guards and live fixture contamination.
9. GREEN evidence: 61/61 pass; the fixture loop remains unchanged, while non-fixture runs with no real competitor evidence create zero gaps, tasks and experiments.
10. Local proof selected exactly two EN plus two RU public Prompts and returned four `SKIPPED_NO_CREDENTIAL` states without making a network call; output stayed under `/private/tmp`.
11. Implementation Report now distinguishes configured/inactive workflows, not-executed remote CI and external source-workspace baselines.
