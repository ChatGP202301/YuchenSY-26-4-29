from __future__ import annotations

from core import load_config, stable_id, utc_now

PROXY_ONLY = {"search_rank", "fan_out_rank", "topic_cluster_ranking", "brand_entity_trust", "known_source", "domain_authority"}


def _observed(factor_id: str, page: dict) -> tuple[str, object, str]:
    checks = page.get("answer_extractability_checks", {})
    mapping = {
        "url_accessibility": bool(page.get("canonical")),
        "preview_control": page.get("robots", "") or "no-data",
        "query_answer_match": checks.get("what_product"),
        "intent_format_match": bool(page.get("h2") or checks.get("faq")),
        "answer_near_top": len(page.get("opening_text", "")) >= 120,
        "ai_ready_structure": bool(page.get("h2") and (page.get("links") or page.get("schema_types"))),
        "factually_specific": any(checks.get(key) for key in ("capacity","feed_water","tds","flow_rate","membrane","power")),
        "explicit_phrasing": bool(page.get("h1")) and len(page.get("opening_text", "")) >= 80,
        "cites_sources": any(str(link).startswith("https://") for link in page.get("links", [])),
        "self_contained_passages": len(page.get("opening_text", "")) >= 180,
        "content_visibility": page.get("word_count", 0) >= 150,
        "freshness": "no-data",
        "length": page.get("word_count", 0),
        "language": bool(page.get("h1")),
        "entity_consistency": bool(set(page.get("schema_types", [])) & {"Organization","Manufacturer","Product","Service"}),
        "structured_data": bool(page.get("schema_types")) and not page.get("schema_errors"),
        "llms_txt": "report-at-site-level",
    }
    value = mapping.get(factor_id, "no-data")
    if value == "no-data": return "no-data", None, "low"
    return "observed", value, "high" if isinstance(value, bool) else "medium"


def audit_features(page: dict, page_ref: str, language: str, engine: str = "page_audit", prompt_id: str | None = None, measured_at: str | None = None) -> list[dict]:
    registry = load_config("citation-factors.json")
    measured_at = measured_at or utc_now()
    rows = []
    for factor in registry["factors"]:
        factor_id = factor["factor_id"]
        if factor_id in PROXY_ONLY:
            status, value, confidence = "no-data", None, "low"
        else:
            status, value, confidence = _observed(factor_id, page)
        identity = {"factor":factor_id,"page":page_ref,"engine":engine,"prompt":prompt_id,"measured":measured_at}
        rows.append({
            "schema_version":1, "observation_id":stable_id("feature", identity), "factor_id":factor_id, "page":page_ref, "language":language,
            "engine":engine, "prompt_id":prompt_id, "measurement_mode":factor["measurement_mode"], "status":status, "value":value,
            "confidence":confidence, "evidence_refs":[page_ref], "measured_at":measured_at, "author_score":factor["author_score"],
            "claim_type":registry["claim_type"], "causal_claim":False,
        })
    return rows


def explain_factor(factor_id: str) -> dict:
    registry = load_config("citation-factors.json")
    factor = next((row for row in registry["factors"] if row["factor_id"] == factor_id), None)
    if not factor: raise KeyError(factor_id)
    return {**factor, "source_url":registry["source_url"], "claim_type":registry["claim_type"], "safety":registry["author_score_policy"]}


def compare_feature_sets(before: list[dict], after: list[dict], citation_before: float | None, citation_after: float | None) -> dict:
    before_map = {row["factor_id"]:row for row in before}
    after_map = {row["factor_id"]:row for row in after}
    changes = []
    for factor_id in sorted(set(before_map) | set(after_map)):
        old, new = before_map.get(factor_id, {}), after_map.get(factor_id, {})
        if old.get("value") != new.get("value") or old.get("status") != new.get("status"):
            changes.append({"factor_id":factor_id,"before":old.get("value"),"after":new.get("value"),"before_status":old.get("status"),"after_status":new.get("status")})
    return {"feature_changes":changes, "citation_rate_before":citation_before, "citation_rate_after":citation_after, "causal_guarantee":False, "interpretation":"descriptive_association_only"}
