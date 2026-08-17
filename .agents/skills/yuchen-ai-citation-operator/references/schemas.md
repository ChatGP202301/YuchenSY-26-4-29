# Evidence schema rules

Every record requires `schema_version`, an immutable ID, and an ISO-8601 UTC timestamp.

Prompt records preserve language, locale, country, product, topic, intent, exact prompt text, source, priority, channel, creation time, and last-tested time.

Citation records preserve engine, surface (`api` or `web`), model/interface label, prompt ID and text, language, country, answer SHA-256, citation URL and position, our-domain status and URL, evidence source (`live`, `manual`, or `fixture`), evidence URL or screenshot hash, verification status, and capture time. Do not commit full answers or screenshots.

Feature observations preserve factor ID, page, language, engine, prompt ID, measurement mode, status (`observed`, `proxy`, `no-data`, or `not-applicable`), value, confidence, evidence references, and measurement time.

Experiments preserve page, language, prompt set, baseline citation/SEO evidence, change type, commit, deployment date, 7/14/30-day metrics, result (`WIN`, `NEUTRAL`, `LOSS`, or `UNKNOWN`), and cooling deadline.

Fixture and unverified manual evidence never enter live denominators. Missing external data is `no-data`, not zero.
