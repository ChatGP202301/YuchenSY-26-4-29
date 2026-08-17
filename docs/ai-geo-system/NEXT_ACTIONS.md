# Your next actions

1. Create a Gemini API Key in Google AI Studio: <https://aistudio.google.com/apikey>. Keep billing disabled; if the account is not clearly eligible for the free tier, do not run the proof.
2. Accept the free-tier data policy only for the four public product/buyer Prompts. Do not use customer data, PII, private documents, unpublished facts or secrets. Current official terms and pricing must be rechecked at <https://ai.google.dev/gemini-api/docs/pricing> before the run.
3. In the macOS **Keychain Access** app, create a password item with service `yuchen-ai-geo-gemini`, account `ChatGP202301`, and the API Key as its password. Do not paste the Key into Codex chat, a terminal command, GitHub, Markdown or a repository secret for this local proof.
4. Tell Codex only that the Keychain item is ready. The next run must inject it into the single local process without displaying it, keep `AI_GEO_MODE=DRY_RUN`, set `AI_GEO_FREE_TIER_CONFIRMED=true`, execute exactly two EN plus two RU Prompts, and leave results under `/private/tmp`.
5. Review Draft PR #3. Do not merge it into `main` or enable the dispatcher; the remaining scheduler, SSRF and dynamic-report hardening must be completed first.
