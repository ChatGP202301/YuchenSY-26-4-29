# Your next actions

1. Review the Draft PR from `codex/ai-geo-system-v1` into `codex/staging-site-20260817`. Do not merge it into `main`; its purpose is to inspect the isolated control system.
2. Optional free Gemini observation: add repository secret `GEMINI_API_KEY`, repository variable `AI_GEO_FREE_TIER_CONFIRMED=true`, and keep `AI_GEO_MODE=DRY_RUN`. If free-tier eligibility or price cannot be confirmed, leave them unset.
3. Keep `AI_GEO_ENABLED=true` for read-only observation, or set it to `false` for health/status reports only.
4. After the control commit is frozen and independently reviewed, approve a separate dispatcher-only Draft PR to `main` that checks out that exact commit. Do not copy `ai-geo/`, reports or Skill files into the Pages publishing tree.
5. Leave AUTO_L1 disabled. To consider it later, first add branch protection, required review/checks and independently verify repository auto-merge policy; then review a separate minimal-permission PR. Setting `AI_GEO_MODE=AUTO_L1` now is intentionally refused with `REQUIRES_GITHUB_PERMISSION`.
