# Safety and rollout policy

## Environment split

- Use `https://www.yuchensy.com/` only for read-only live citation and HTTP observations.
- Use Git ref `codex/staging-site-20260817` for candidate-page parsing and SEO comparison.
- Do not send AI citation tests to the authenticated, `noindex` Staging URL.

## Risk

- L1: bounded, non-structural, source-backed additions on a verified-owned page. All guards must pass.
- L2: title, H1, large copy, page reordering, templates, protected/high-value pages, already-cited pages, unknown GSC, or unknown ownership. Draft PR only.
- L3: URL, deletion, canonical, hreflang, robots, sitemap architecture, domain, CNAME, workflow security, permissions, bulk changes, or unsupported facts. Report only.

Never let an internal score or an external author score lower risk. A risk result may only remain unchanged or become stricter as evidence becomes uncertain.

## Rollout

Enable English and Russian dry-run experiments first, 3–5 pages each. Keep Spanish and French configured but disabled until the first phase is reviewed. Apply a 14-day page cooling period. Start real 7/14/30-day retests only after an exact production deployment commit and date are registered.

An emergency rollback must revert one exact AI-owned commit on a new branch and open a PR. Never force-push or directly rewrite `main`.
