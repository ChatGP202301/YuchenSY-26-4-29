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
