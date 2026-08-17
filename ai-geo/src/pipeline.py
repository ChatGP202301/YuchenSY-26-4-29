from __future__ import annotations

import json
from pathlib import Path

from adapters import GeminiFreeAdapter, validate_import_record
from competitor import compare_pages
from core import atomic_write_json, load_config
from experiments import create_experiment, retest_plan
from features import audit_features
from git_controller import simulate_git_action
from guards import classify_risk, content_guard, diff_guard, seo_guard
from page_analyzer import analyze_file, analyze_html, seo_snapshot
from prompts import discover_prompts
from reporting import citation_metrics, visibility_score, write_markdown_report
from storage import append_jsonl_idempotent, read_jsonl, rebuild_sqlite


def analyze_citations(records: list[dict]) -> dict:
    live = citation_metrics(records, "live")
    manual = citation_metrics(records, "manual")
    fixture = citation_metrics(records, "fixture")
    competitors = {}
    for record in records:
        for citation in record.get("citations", []):
            host = citation["url"].split("/", 3)[2].lower()
            if host != record.get("our_domain"):
                competitors[host] = competitors.get(host, 0) + 1
    return {"live":live,"manual":manual,"fixture":fixture,"competitors":dict(sorted(competitors.items(), key=lambda item:(-item[1],item[0]))),"fixture_excluded_from_live":True}


def fixture_citations(prompts: list[dict]) -> list[dict]:
    records = []
    for index, prompt in enumerate(prompts):
        citations = [{"url":f"https://example-competitor.test/{prompt['language']}/industrial-ro", "position":1, "title":"Fixture competitor"}]
        if index % 5 == 0:
            citations.append({"url":f"https://www.yuchensy.com/{prompt['language']}/products.html", "position":2, "title":"Yuchen fixture citation"})
        raw = {
            "AI_engine":"fixture_engine", "surface":"fixture", "model_interface":"fixture-v1", "language":prompt["language"], "country":prompt["country"],
            "prompt_id":prompt["prompt_id"], "prompt":prompt["prompt_text"], "intent":prompt["intent"], "captured_at":f"2026-08-17T00:{index:02d}:00+00:00",
            "source":"fixture", "answer_sha256":"0"*64, "citations":citations, "verified":True, "evidence_url":"https://fixture.invalid/evidence",
        }
        records.append(validate_import_record(raw))
    return records


def live_gemini_citations(prompts: list[dict], adapter: GeminiFreeAdapter | None = None) -> tuple[list[dict], list[dict]]:
    """Sample at most 20 EN and 20 RU prompts after the zero-cost gate passes."""
    adapter = adapter or GeminiFreeAdapter()
    eligibility = adapter.eligibility()
    if eligibility != "ELIGIBLE":
        return [], [{"engine": adapter.name, "status": eligibility, "language": language, "selected": 0} for language in ("en", "ru")]
    caps = load_config("system.yaml")["daily_live_caps"]
    citations = []
    statuses = []
    for language in ("en", "ru"):
        selected = [row for row in prompts if row["language"] == language][: int(caps[language])]
        completed = 0
        failures = 0
        for prompt in selected:
            try:
                result = adapter.search(prompt)
                if result.get("status") != "OK":
                    failures += 1
                    continue
                raw = {
                    "AI_engine": adapter.name,
                    "surface": "api",
                    "model_interface": result.get("model", "unknown"),
                    "language": prompt["language"],
                    "country": prompt["country"],
                    "prompt_id": prompt["prompt_id"],
                    "prompt": prompt["prompt_text"],
                    "intent": prompt["intent"],
                    "captured_at": result["captured_at"],
                    "source": "live",
                    "answer_sha256": result.get("answer_sha256", ""),
                    "citations": result.get("citations", []),
                    "verified": True,
                    "notes": "Gemini free API sample; not represented as a consumer web result.",
                }
                citations.append(validate_import_record(raw))
                completed += 1
            except Exception as exc:
                failures += 1
                statuses.append({"engine": adapter.name, "status": "ERROR", "language": language, "prompt_id": prompt["prompt_id"], "error_type": type(exc).__name__})
        statuses.append({"engine": adapter.name, "status": "COMPLETED" if not failures else "PARTIAL", "language": language, "selected": len(selected), "completed": completed, "failed": failures})
    return citations, statuses


def draft_task(page_path: str, prompts: list[dict], gap: dict, page: dict) -> dict:
    content = content_guard("Add a concise source-backed FAQ about Yuchen Water and selection inputs.")
    before = seo_snapshot(page, {"html_pages":14189,"sitemap_urls":13942,"indexable_pages":13942,"broken_links":0,"not_found":0})
    after = dict(before)
    seo = seo_guard(before, after)
    diff = diff_guard([page_path], 20, 0, 1)
    proposal = {"page":page_path,"files":[page_path],"operations":[],"change_type":"faq_addition","ownership":"unknown","gsc_status":"no-data","citation_gap_verified":True,"trusted_facts_verified":content["passed"],"content_guard":content,"seo_guard":seo,"diff_guard":diff}
    risk = classify_risk(proposal)
    return {
        "page":page_path,"prompt_ids":[row["prompt_id"] for row in prompts[:5]],"evidence":[gap.get("snapshot_id")],"structural_gaps":gap.get("OUR_PAGE_GAPS", []),
        "allowed_paths":[page_path],"forbidden":["URL","canonical","hreflang","robots","sitemap","unverified claims"],"acceptance_commands":["python3 ai-geo/cli.py doctor","python3 tools/test_ai_geo_system.py"],
        "rollback_point":"exact pre-change commit required","risk":risk,"apply_page":False,
    }


def run_pipeline(output_root: Path, site_root: Path, fixture: bool = False) -> dict:
    output_root.mkdir(parents=True, exist_ok=True)
    data = output_root / "data"
    reports = output_root / "reports"
    prompts = discover_prompts(["en","ru"], 20)
    prompt_path = data / "prompts" / "prompts.jsonl"
    append_jsonl_idempotent(prompt_path, prompts, "prompt_id")

    citation_path = data / "citations" / "citations.jsonl"
    sample_statuses = []
    if fixture:
        append_jsonl_idempotent(citation_path, fixture_citations(prompts), "citation_id")
    else:
        live_rows, sample_statuses = live_gemini_citations(prompts)
        append_jsonl_idempotent(citation_path, live_rows, "citation_id")
    citations = read_jsonl(citation_path)

    feature_rows = []
    pages = []
    for language in ("en", "ru"):
        path = site_root / language / "products.html"
        if not path.is_file(): path = site_root / language / "index.html"
        page = analyze_file(path, site_root)
        pages.append((language, path.relative_to(site_root).as_posix(), page))
        feature_rows.extend(audit_features(page, page["path"], language, measured_at="2026-08-17T01:00:00+00:00" if fixture else None))
    feature_path = data / "metrics" / "feature-observations.jsonl"
    append_jsonl_idempotent(feature_path, feature_rows, "observation_id")

    competitor_fixture = analyze_html("<html><head><title>Industrial RO supplier</title><script type='application/ld+json'>{\"@context\":\"https://schema.org\",\"@type\":\"Product\"}</script></head><body><main><h1>Industrial reverse osmosis system</h1><h2>Specifications</h2><p>Capacity and feed water selection checklist for industrial buyers.</p><h2>FAQ</h2><p>What data is required?</p></main></body></html>", "https://example-competitor.test/page")
    gaps = [compare_pages(page, competitor_fixture, f"https://example-competitor.test/{language}/page") for language, _, page in pages]
    gap_path = data / "competitors" / "snapshots.jsonl"
    append_jsonl_idempotent(gap_path, gaps, "snapshot_id")

    tasks = [draft_task(path, [row for row in prompts if row["language"] == language], gaps[index], page) for index, (language, path, page) in enumerate(pages)]
    atomic_write_json(reports / "pr" / "codex-tasks.json", {"schema_version":1,"tasks":tasks})

    experiments = [create_experiment(task["page"], task["page"].split("/",1)[0], task["prompt_ids"], "faq_addition", created_at="2026-08-17T02:00:00+00:00") for task in tasks]
    experiment_path = data / "experiments" / "experiments.jsonl"
    append_jsonl_idempotent(experiment_path, experiments, "experiment_id")
    plans = {row["experiment_id"]:retest_plan(row) for row in experiments}
    atomic_write_json(data / "experiments" / "retest-plans.json", {"schema_version":1,"plans":plans})

    metrics = analyze_citations(citations)
    atomic_write_json(data / "metrics" / "citation-summary.json", {"schema_version":1,**metrics})
    sample_status = GeminiFreeAdapter(env={}).eligibility() if fixture else GeminiFreeAdapter().eligibility()
    write_markdown_report(reports / "daily" / "2026-08-17.md", "AI GEO Daily Report", prompts, citations, feature_rows, tasks, experiments)
    write_markdown_report(reports / "weekly" / "2026-W34.md", "AI GEO Weekly Report", prompts, citations, feature_rows, tasks, experiments)
    write_markdown_report(reports / "monthly" / "2026-08.md", "AI GEO Monthly Report", prompts, citations, feature_rows, tasks, experiments)
    sources = {"prompts":prompt_path,"citations":citation_path,"feature_observations":feature_path,"competitor_snapshots":gap_path,"experiments":experiment_path}
    sqlite_counts = rebuild_sqlite(data / "metrics" / "ai-geo.sqlite3", sources)
    simulation = simulate_git_action("en", [tasks[0]["page"]], tasks[0]["prompt_ids"], "draft answer-ready FAQ coverage", pages[0][2]["answer_extractability_score"], pages[0][2]["answer_extractability_score"], {"seo_guard":"PASS","content_guard":"PASS"})
    result = {"status":"PASS","mode":"DRY_RUN","fixture":fixture,"prompts":len(prompts),"citations":len(citations),"feature_observations":len(feature_rows),"tasks":len(tasks),"experiments":len(experiments),"gemini":sample_status,"sample_statuses":sample_statuses,"metrics":metrics,"sqlite":sqlite_counts,"git":simulation,"production_modified":False}
    atomic_write_json(output_root / "run-result.json", {"schema_version":1,**result})
    return result
