from __future__ import annotations

from pathlib import Path

from core import load_config, utc_now


def citation_metrics(records: list[dict], source: str = "live") -> dict:
    eligible = [row for row in records if row.get("source") == source and row.get("verified")]
    cited = sum(bool(row.get("our_cited")) for row in eligible)
    return {"source":source,"eligible":len(eligible),"our_cited":cited,"citation_rate":round(cited/len(eligible),4) if eligible else None}


def visibility_score(metrics: dict) -> dict:
    required = ["citation_frequency","citation_position","prompt_coverage","language_coverage","commercial_intent_coverage","brand_product_mention","competitor_share_inverse"]
    if any(metrics.get(key) is None for key in required):
        return {"score":None,"status":"no-data","coverage":round(100*sum(metrics.get(k) is not None for k in required)/len(required),2),"industry_standard":False}
    weights = {"citation_frequency":30,"citation_position":15,"prompt_coverage":15,"language_coverage":10,"commercial_intent_coverage":10,"brand_product_mention":10,"competitor_share_inverse":10}
    score = sum(max(0,min(1,float(metrics[key]))) * weight for key, weight in weights.items())
    return {"score":round(score,2),"status":"observed","coverage":100.0,"industry_standard":False}


def write_markdown_report(path: Path, title: str, prompts: list[dict], citations: list[dict], feature_rows: list[dict], tasks: list[dict], experiments: list[dict]) -> None:
    live = citation_metrics(citations, "live")
    manual = citation_metrics(citations, "manual")
    fixture = citation_metrics(citations, "fixture")
    coverage = sum(row.get("status") in {"observed","proxy"} for row in feature_rows)
    competitors = sorted({citation["url"].split("/", 3)[2] for row in citations for citation in row.get("citations", []) if citation["url"].split("/", 3)[2] != row.get("our_domain")})
    risk_counts = {risk:sum(task.get("risk", {}).get("risk") == risk for task in tasks) for risk in ("L1", "L2", "L3")}
    results = {result:sum(row.get("result") == result for row in experiments) for result in ("WIN", "NEUTRAL", "LOSS", "UNKNOWN")}
    registry = load_config("citation-factors.json")
    observations = {}
    for row in feature_rows:
        observations.setdefault(row["factor_id"], set()).add(row.get("status", "no-data"))
    factor_lines = ["| Factor | Author score | Our status | Site effect |", "|---|---:|---|---|"]
    for factor in registry["factors"]:
        statuses = ", ".join(sorted(observations.get(factor["factor_id"], {"not-measured"})))
        factor_lines.append(f"| {factor['name']} | {factor['author_score']} | {statuses} | UNKNOWN |")
    text = f"""# {title}

Generated: `{utc_now()}`

> Internal metrics and the 23 external correlation hypotheses do not predict rankings or AI citations and do not establish causality.

## Summary

- Prompts tested or prepared: {len(prompts)}
- Live eligible observations: {live['eligible']}
- Live citation rate: {live['citation_rate'] if live['citation_rate'] is not None else 'no-data'}
- Verified manual observations: {manual['eligible']} (reported separately)
- Fixture observations: {fixture['eligible']} (excluded from live denominator)
- Our domains cited: {live['our_cited']} live / {manual['our_cited']} manual / {fixture['our_cited']} fixture
- Competitors observed: {', '.join(competitors) if competitors else 'no-data'}
- Citation wins/losses: {results['WIN']} / {results['LOSS']} (paired deployed experiments only)
- Pages analyzed: {len({row.get('page') for row in feature_rows})}
- Pages changed: 0
- Proposed tasks: {len(tasks)} (L1 {risk_counts['L1']}, L2 {risk_counts['L2']}, L3 {risk_counts['L3']})
- Auto merged: 0
- PR created: 0
- Blocked/review changes: {risk_counts['L2'] + risk_counts['L3']}
- SEO errors introduced: 0
- GEO improvements deployed: 0
- Experiments: {len(experiments)}

## 23-factor hypothesis coverage

- Observed/proxy rows: {coverage}/{len(feature_rows)}
- Unmeasured rows: {sum(row.get('status') == 'no-data' for row in feature_rows)}
- Author scores are display-only and never affect risk.

## Author scores and our observed effect

{chr(10).join(factor_lines)}

No deployed paired experiment is present, so every site-effect result is UNKNOWN. Author score and site effect are not treated as causal.

## Unmeasured factors

{', '.join(factor['name'] for factor in registry['factors'] if observations.get(factor['factor_id'], {'no-data'}) <= {'no-data', 'not-measured'}) or 'None'}

## Safety

- Production modified: NO
- Proposed tasks only: {len(tasks)}
- Auto merge: DISABLED unless repository protections are independently verified

## Next recommended actions

- Collect source-backed public production citations or import verifiable manual evidence.
- Review L2 task specifications on Staging; do not apply them to production.
- Register an exact deployment commit/date before scheduling 7/14/30-day retests.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
