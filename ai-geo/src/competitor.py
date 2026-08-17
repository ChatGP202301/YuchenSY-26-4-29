from __future__ import annotations

from core import stable_id, utc_now
from network import safe_get
from page_analyzer import analyze_html


def structural_gaps(ours: dict, competitor: dict) -> list[dict]:
    gaps = []
    comparisons = [
        ("faq", bool(ours.get("answer_extractability_checks", {}).get("faq")), bool(competitor.get("answer_extractability_checks", {}).get("faq"))),
        ("technical_specifications", ours.get("answer_extractability_score", 0) >= 50, competitor.get("answer_extractability_score", 0) >= 50),
        ("tables_or_structured_sections", bool(ours.get("h2")), bool(competitor.get("h2"))),
        ("entity_schema", bool(set(ours.get("schema_types", [])) & {"Organization","Product","Service"}), bool(set(competitor.get("schema_types", [])) & {"Organization","Product","Service"})),
        ("answer_near_top", len(ours.get("opening_text", "")) >= 120, len(competitor.get("opening_text", "")) >= 120),
    ]
    for name, has_ours, has_competitor in comparisons:
        if has_competitor and not has_ours:
            gaps.append({"gap":name, "evidence":"competitor_structure_present_our_structure_absent", "copy_competitor_text":False})
    return gaps


def compare_pages(our_page: dict, competitor_page: dict, source_url: str, captured_at: str | None = None) -> dict:
    gaps = structural_gaps(our_page, competitor_page)
    captured = captured_at or f"{utc_now()[:10]}T00:00:00+00:00"
    structural_identity = {
        "url": source_url,
        "captured_day": captured[:10],
        "our": {"h2": our_page.get("h2", []), "schema": our_page.get("schema_types", []), "checks": our_page.get("answer_extractability_checks", {})},
        "competitor": {"h2": competitor_page.get("h2", []), "schema": competitor_page.get("schema_types", []), "checks": competitor_page.get("answer_extractability_checks", {})},
    }
    return {
        "schema_version":1, "snapshot_id":stable_id("competitor", structural_identity), "captured_at":captured, "source_url":source_url,
        "WHY_COMPETITOR_WAS_CITED":[item["gap"] for item in gaps] or ["UNKNOWN"], "OUR_PAGE_GAPS":gaps,
        "RECOMMENDED_ACTIONS":[f"Review a source-backed {item['gap']} addition" for item in gaps] or ["Collect more evidence"],
        "RISK_LEVEL":"L2", "copyright_policy":"structure_only_no_competitor_prose",
    }


def analyze_competitor_url(url: str, our_page: dict) -> dict:
    response = safe_get(url)
    competitor = analyze_html(response["text"], response["url"])
    return compare_pages(our_page, competitor, response["url"])
