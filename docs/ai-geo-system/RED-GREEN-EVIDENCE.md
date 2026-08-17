# Adversarial RED to GREEN evidence

The first full AI GEO test run intentionally exercised real guard behavior rather than replacing guards with mocks.

## Observed RED

Command:

```sh
python3 -m unittest tools/test_ai_geo_system.py -v
```

Result: 48 tests executed, one failure.

```text
FAIL: test_protected_workflow_and_seo_paths_are_l3
path='.github/workflows/deploy.yml'
AssertionError: False is not true
```

Root cause: path normalization used `lstrip("./")`, which removed the meaningful leading dot from `.github` and prevented the denylist pattern from matching.

## GREEN repair

Path normalization now removes only explicit `./` prefixes and preserves `.github`. The same command then returned:

```text
Ran 48 tests
OK
```

The suite also performs adverse inputs for all ten required classes: protected paths, forged claims, unverified evidence, fixture/live separation, paid/manual adapters and quota limits, SSRF/redirect/robots, cooling, duplicate import, and SEO drift. Additional reverse checks cover fake freshness, absolute wording, Schema stacking, length-driven expansion, low LLMs.txt score, diff limits, emergency revert ownership and the emergency switch.

## Import-evidence RED to GREEN

The CSV adapter test next exposed that a manual record with a valid evidence URL was still defaulting to unverified. Validation was repaired so manual evidence defaults to verified only when an evidence URL or screenshot hash exists, while an explicit false remains false and string booleans are parsed safely. The inverse test still proves a record without either evidence reference is excluded.

## Gemini grounded proof RED — 2026-08-17

After adding ten network-boundary and live/fixture isolation tests, the unmodified implementation produced a genuine RED result:

```text
Ran 61 tests
FAILED (failures=2, errors=7)
```

The failures proved that the request omitted the required `google_search` tool, HTTP 403/429 escaped instead of stopping safely, non-public Prompt sources reached the network, the four-Prompt proof/output guards did not exist, and a non-fixture pipeline created two synthetic competitor tasks and experiments. The full terminal output was retained in the execution conversation; no assertion, threshold or existing test was weakened.

## Gemini grounded proof GREEN

The adapter now sends `tools: [{"google_search": {}}]`, discards the answer and plaintext search queries after hashing, denies non-public Prompt sources before network access and returns terminal structured states for 403/429. The CLI selects two EN plus two RU Prompts, caps the proof at four and confines its output to `/private/tmp`. The live pipeline emits `no-data` and zero tasks/experiments when it has no real competitor evidence.

```text
Ran 61 tests in 0.079s
OK
```

The actual credential-gate proof then selected four records and returned four `SKIPPED_NO_CREDENTIAL` states. No Gemini request was made and this result is not counted as live citation evidence.
