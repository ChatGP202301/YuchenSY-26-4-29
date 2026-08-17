from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request

REPO = Path(__file__).resolve().parents[1]
AI_GEO = REPO / "ai-geo"
SRC = AI_GEO / "src"
sys.path[:0] = [str(AI_GEO), str(SRC)]

from adapters import GeminiFreeAdapter, MANUAL_ENGINES, ManualImportAdapter, validate_import_record
from cli import read_records as cli_read_records, sample_budget
from competitor import compare_pages, structural_gaps
from core import load_config, runtime_state, sha256_file
from experiments import classify_result, create_experiment, register_deployment, retest_plan
from features import PROXY_ONLY, audit_features, compare_feature_sets
from git_controller import emergency_revert_plan, simulate_git_action
from guards import classify_risk, content_guard, diff_guard, in_cooling, path_denied, seo_guard
from learning import aggregate_learning
from network import SafeRedirectHandler, robots_text_allows, validate_public_https
from page_analyzer import analyze_html, seo_snapshot
from pipeline import analyze_citations, fixture_citations, live_gemini_citations, run_pipeline
from prompts import INTENTS, discover_prompts
from reporting import citation_metrics, visibility_score
from scheduler import schedule_for
from storage import append_jsonl_idempotent, read_jsonl, rebuild_sqlite


class ConfigTests(unittest.TestCase):
    def test_languages_detect_64_scopes_and_63_records(self):
        config = load_config("languages.yaml")
        self.assertEqual(config["detected_scope_count"], 64)
        self.assertEqual(len(config["records"]), 63)
        self.assertEqual(len({row["language_code"] for row in config["records"]}), 63)

    def test_phase_one_en_ru_only(self):
        config = load_config("languages.yaml")
        enabled = [row["language_code"] for row in config["records"] if row["enabled"]]
        self.assertEqual(enabled, ["en", "ru"])
        deferred = {row["language_code"]: row for row in config["records"] if row["language_code"] in {"es", "fr"}}
        self.assertTrue(all(not row["enabled"] and row["priority"] == 2 for row in deferred.values()))

    def test_zyppy_registry_is_exactly_23_unique_hypotheses(self):
        registry = load_config("citation-factors.json")
        self.assertEqual(len(registry["factors"]), 23)
        self.assertEqual(len({row["factor_id"] for row in registry["factors"]}), 23)
        self.assertEqual(registry["claim_type"], "correlation_hypothesis")
        self.assertEqual(registry["source_material_count_article"], 54)
        self.assertEqual(registry["source_material_count_image"], 55)
        self.assertEqual(registry["image_sha256_status"], "partial_user_supplied")
        self.assertIn("…", registry["image_sha256_partial"])

    def test_author_score_never_changes_risk(self):
        base = {"page":"en/detail.html","files":["en/detail.html"],"operations":[],"change_type":"faq_addition","ownership":"verified","gsc_status":"not_top20","citation_gap_verified":True,"trusted_facts_verified":True,"content_guard":{"passed":True},"seo_guard":{"passed":True},"diff_guard":{"passed":True}}
        first = classify_risk({**base, "author_score": 9.5})
        second = classify_risk({**base, "author_score": 0.0})
        self.assertEqual(first, second)
        self.assertEqual(first["risk"], "L1")

    def test_frozen_controller_hashes_match_manifest(self):
        root = AI_GEO / "vendor" / "frozen-site-quality"
        manifest = json.loads((root / "MANIFEST.json").read_text())
        for name, expected in manifest["files"].items():
            self.assertEqual(sha256_file(root / name), expected)


class PromptAndAdapterTests(unittest.TestCase):
    def test_fixture_discovers_40_localized_prompts(self):
        prompts = discover_prompts(["en", "ru"], 20)
        self.assertEqual(len(prompts), 40)
        self.assertEqual({row["language"] for row in prompts}, {"en", "ru"})
        self.assertEqual({row["intent"] for row in prompts}, set(INTENTS))
        self.assertTrue(any("промышленная установка" in row["prompt_text"] for row in prompts if row["language"] == "ru"))
        self.assertTrue(all({"prompt_id","locale","country","product","intent","channel","created_at"} <= set(row) for row in prompts))

    def test_live_quota_is_hard_capped_20_per_language(self):
        prompts = discover_prompts(["en"], 40)
        selected, quota = sample_budget(prompts, "en", 999)
        self.assertEqual(len(selected), 20)
        self.assertEqual(quota["hard_cap"], 20)

    def test_es_fr_live_quota_is_zero(self):
        prompts = discover_prompts(["es", "fr"], 20)
        self.assertEqual(sample_budget(prompts, "es", 20)[1]["selected"], 0)
        self.assertEqual(sample_budget(prompts, "fr", 20)[1]["selected"], 0)

    def test_gemini_without_key_is_explicitly_skipped(self):
        self.assertEqual(GeminiFreeAdapter(env={}).eligibility(), "SKIPPED_NO_CREDENTIAL")

    def test_gemini_requires_free_tier_confirmation(self):
        self.assertEqual(GeminiFreeAdapter(env={"GEMINI_API_KEY":"secret"}).eligibility(), "SKIPPED_FREE_TIER_UNCONFIRMED")

    def test_consumer_and_paid_surfaces_remain_manual(self):
        self.assertTrue({"chatgpt_web","perplexity_web","deepseek_web","yandex_ai_web","grok_web","copilot_web","yuanbao_web"} <= MANUAL_ENGINES)
        prompt = discover_prompts(["en"], 1)[0]
        self.assertEqual(ManualImportAdapter("grok_web").search(prompt)["status"], "MANUAL_REQUIRED")

    def test_live_sampler_never_calls_adapter_when_ineligible(self):
        rows, statuses = live_gemini_citations(discover_prompts(["en", "ru"], 20), GeminiFreeAdapter(env={}))
        self.assertEqual(rows, [])
        self.assertTrue(all(row["status"] == "SKIPPED_NO_CREDENTIAL" for row in statuses))


class EvidenceStorageTests(unittest.TestCase):
    def raw_record(self, source="manual", evidence=True):
        return {"AI_engine":"chatgpt_web","language":"en","country":"US","prompt_id":"p1","prompt":"question","intent":"supplier","captured_at":"2026-08-17T00:00:00+00:00","source":source,"evidence_url":"https://evidence.example/item" if evidence else None,"citations":[{"url":"https://www.yuchensy.com/en/products.html","position":2}]}

    def test_manual_evidence_without_url_or_screenshot_is_not_verified(self):
        row = validate_import_record(self.raw_record(evidence=False))
        self.assertFalse(row["verified"])
        self.assertEqual(citation_metrics([row], "manual")["eligible"], 0)

    def test_fixture_is_excluded_from_live_denominator(self):
        fixture = validate_import_record(self.raw_record(source="fixture"))
        self.assertEqual(analyze_citations([fixture])["live"]["eligible"], 0)
        self.assertEqual(analyze_citations([fixture])["fixture"]["eligible"], 1)

    def test_non_https_citation_is_denied(self):
        raw = self.raw_record()
        raw["citations"] = [{"url":"http://www.yuchensy.com/en/"}]
        with self.assertRaisesRegex(ValueError, "HTTPS"):
            validate_import_record(raw)

    def test_manual_evidence_reference_must_be_https_and_hash_well_formed(self):
        raw = self.raw_record()
        raw["evidence_url"] = "http://evidence.example/item"
        with self.assertRaisesRegex(ValueError, "evidence_url"):
            validate_import_record(raw)
        raw = self.raw_record(evidence=False)
        raw["screenshot_sha256"] = "short"
        with self.assertRaisesRegex(ValueError, "full SHA-256"):
            validate_import_record(raw)

    def test_jsonl_import_is_idempotent_and_immutable(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.jsonl"
            row = {"schema_version":1,"record_id":"one","value":1}
            self.assertEqual(append_jsonl_idempotent(path, [row], "record_id"), 1)
            self.assertEqual(append_jsonl_idempotent(path, [row], "record_id"), 0)
            with self.assertRaisesRegex(ValueError, "immutable record collision"):
                append_jsonl_idempotent(path, [{**row,"value":2}], "record_id")

    def test_sqlite_is_rebuildable_from_jsonl(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prompt_path = root / "prompts.jsonl"
            append_jsonl_idempotent(prompt_path, discover_prompts(["en"], 2), "prompt_id")
            counts = rebuild_sqlite(root / "db.sqlite3", {"prompts":prompt_path})
            self.assertEqual(counts, {"prompts":2})
            with sqlite3.connect(root / "db.sqlite3") as connection:
                self.assertEqual(connection.execute("SELECT count(*) FROM prompts").fetchone()[0], 2)

    def test_csv_manual_import_parses_citation_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.csv"
            path.write_text('AI_engine,language,country,prompt_id,prompt,intent,captured_at,source,evidence_url,citations_json\nchatgpt_web,en,US,p1,question,supplier,2026-08-17T00:00:00+00:00,manual,https://evidence.example/item,"[{""url"":""https://www.yuchensy.com/en/""}]"\n', encoding="utf-8")
            rows = cli_read_records(path)
            self.assertEqual(rows[0]["citations"][0]["url"], "https://www.yuchensy.com/en/")
            self.assertTrue(validate_import_record(rows[0])["verified"])


class FeatureAndPageTests(unittest.TestCase):
    HTML = """<html lang='en'><head><title>Industrial RO</title><meta name='robots' content='index,follow'><link rel='canonical' href='https://www.yuchensy.com/en/test.html'><script type='application/ld+json'>{\"@context\":\"https://schema.org\",\"@type\":\"Product\"}</script></head><body><main><h1>Industrial reverse osmosis system</h1><p>An industrial reverse osmosis system treats feed water for industrial buyers. Capacity is 2000 LPH and membrane selection depends on TDS.</p><h2>Applications</h2><p>Selection and pretreatment application guidance.</p><h2>FAQ</h2><a href='https://example.org/source'>Source</a></main></body></html>"""

    def test_page_analyzer_reports_extractability_and_schema(self):
        page = analyze_html(self.HTML, "en/test.html")
        self.assertEqual(page["schema_types"], ["Product"])
        self.assertGreater(page["answer_extractability_score"], 0)
        self.assertLessEqual(page["answer_extractability_coverage"], 100)

    def test_feature_audit_emits_23_rows_with_six_no_data_proxies(self):
        rows = audit_features(analyze_html(self.HTML, "en/test.html"), "en/test.html", "en", measured_at="2026-08-17T00:00:00+00:00")
        self.assertEqual(len(rows), 23)
        proxy_rows = [row for row in rows if row["factor_id"] in PROXY_ONLY]
        self.assertEqual(len(proxy_rows), 6)
        self.assertTrue(all(row["status"] == "no-data" and row["value"] is None for row in proxy_rows))

    def test_feature_comparison_refuses_causal_guarantee(self):
        result = compare_feature_sets([{"factor_id":"length","value":10,"status":"observed"}], [{"factor_id":"length","value":100,"status":"observed"}], 0.1, 0.2)
        self.assertFalse(result["causal_guarantee"])
        self.assertEqual(result["interpretation"], "descriptive_association_only")

    def test_competitor_analysis_contains_no_competitor_prose(self):
        ours = analyze_html("<h1>RO</h1>", "en/page.html")
        competitor = analyze_html(self.HTML + "UNIQUE-COMPETITOR-COPY", "https://competitor.example/page")
        result = compare_pages(ours, competitor, "https://competitor.example/page")
        self.assertEqual(result["copyright_policy"], "structure_only_no_competitor_prose")
        self.assertNotIn("UNIQUE-COMPETITOR-COPY", json.dumps(result))

    def test_length_alone_does_not_create_safe_auto_task(self):
        proposal = {"page":"en/detail.html","files":["en/detail.html"],"change_type":"length","ownership":"verified","gsc_status":"not_top20","citation_gap_verified":True,"trusted_facts_verified":True}
        self.assertEqual(classify_risk(proposal)["risk"], "L2")

    def test_low_llms_score_never_authorizes_deletion(self):
        proposal = {"page":"llms.txt","files":["llms.txt"],"operations":["page_delete"],"change_type":"llms_txt","author_score":2.0}
        result = classify_risk(proposal)
        self.assertEqual(result["risk"], "L3")
        self.assertEqual(result["decision"], "DENIED")


class AdversarialGuardTests(unittest.TestCase):
    def safe_proposal(self):
        return {"page":"en/detail.html","files":["en/detail.html"],"operations":[],"change_type":"faq_addition","ownership":"verified","gsc_status":"not_top20","citation_gap_verified":True,"trusted_facts_verified":True,"content_guard":{"passed":True},"seo_guard":{"passed":True},"diff_guard":{"passed":True}}

    def test_protected_workflow_and_seo_paths_are_l3(self):
        for path in [".github/workflows/deploy.yml","CNAME","robots.txt","sitemap.xml","package-lock.json"]:
            with self.subTest(path=path):
                self.assertTrue(path_denied(path))
                self.assertEqual(classify_risk({"files":[path],"operations":[],"change_type":"faq_addition"})["risk"], "L3")

    def test_unknown_ownership_and_gsc_are_never_l1(self):
        proposal = self.safe_proposal()
        proposal.update(ownership="unknown", gsc_status="no-data")
        result = classify_risk(proposal)
        self.assertEqual(result["risk"], "L2")
        self.assertIn("ownership_unknown", result["reasons"])

    def test_verified_low_risk_proposal_can_be_l1_eligible(self):
        self.assertEqual(classify_risk(self.safe_proposal())["decision"], "SAFE_AUTO_ELIGIBLE")

    def test_unverified_certification_and_performance_claims_are_blocked(self):
        result = content_guard("CE certification, 99% removal efficiency, five-year warranty")
        self.assertFalse(result["passed"])
        self.assertGreaterEqual(len(result["violations"]), 3)

    def test_ce_guard_does_not_match_innocent_source_word(self):
        result = content_guard("Add a concise source-backed FAQ about verified selection inputs.")
        self.assertTrue(result["passed"])

    def test_fake_freshness_is_blocked(self):
        result = content_guard("Updated today to improve freshness.")
        self.assertIn("unverified_freshness_claim", result["violations"])

    def test_absolute_explicit_phrasing_is_blocked(self):
        result = content_guard("This system is guaranteed to always remove contaminants.")
        self.assertIn("unsupported_absolute_claim", result["violations"])

    def test_schema_stacking_with_unverified_claim_is_not_l1(self):
        proposal = self.safe_proposal()
        proposal["change_type"] = "schema_factual_addition"
        proposal["content_guard"] = content_guard("NSF approval and FDA certification")
        self.assertEqual(classify_risk(proposal)["risk"], "L2")

    def test_preview_canonical_hreflang_and_robots_drift_are_denied(self):
        base = {"canonical":"https://www.yuchensy.com/en/a","hreflang":[("en","/en/a")],"robots":"index,follow","schema_errors":[],"h1_count":1,"site_counts":{}}
        for key, value in [("canonical","https://evil.example/a"),("hreflang",[]),("robots","noindex")]:
            with self.subTest(key=key):
                result = seo_guard(base, {**base, key:value})
                self.assertFalse(result["passed"])

    def test_site_counts_and_schema_drift_are_denied(self):
        before = {"canonical":"a","hreflang":[],"robots":"index,follow","schema_errors":[],"h1_count":1,"site_counts":{"html_pages":14189,"sitemap_urls":13942,"indexable_pages":13942,"broken_links":0,"not_found":0}}
        after = {**before,"schema_errors":["invalid"],"site_counts":{**before["site_counts"],"sitemap_urls":13941}}
        result = seo_guard(before, after)
        self.assertIn("schema_error", result["violations"])
        self.assertIn("site_sitemap_urls_change", result["violations"])

    def test_diff_limits_include_deletion_ratio(self):
        result = diff_guard([f"en/p{i}.html" for i in range(21)], 480, 20, 6)
        self.assertFalse(result["passed"])
        self.assertTrue({"file_limit","page_limit","deletion_ratio"} <= set(result["violations"]))

    def test_cooling_period_blocks_repeat_change(self):
        now = datetime(2026, 8, 17, tzinfo=timezone.utc)
        self.assertTrue(in_cooling("2026-08-10T00:00:00+00:00", 14, now))
        self.assertFalse(in_cooling("2026-07-01T00:00:00+00:00", 14, now))

    def test_private_and_nonstandard_network_targets_are_blocked(self):
        def resolver(host, port, type=None):
            return [(2, 1, 6, "", ("127.0.0.1", port))]
        with self.assertRaisesRegex(ValueError, "unsafe address"):
            validate_public_https("https://internal.example/", resolver)
        with self.assertRaisesRegex(ValueError, "port 443"):
            validate_public_https("https://example.com:8443/")

    def test_cross_origin_redirect_is_blocked(self):
        def resolver(host, port, type=None):
            return [(2, 1, 6, "", ("8.8.8.8", port))]
        handler = SafeRedirectHandler("example.com", resolver)
        with self.assertRaisesRegex(ValueError, "cross-origin"):
            handler.redirect_request(Request("https://example.com/a"), None, 302, "Found", {}, "https://other.example/b")

    def test_robots_denial_is_enforced(self):
        self.assertFalse(robots_text_allows("User-agent: *\nDisallow: /private", "https://example.com/private/page"))
        self.assertTrue(robots_text_allows("User-agent: *\nDisallow: /private", "https://example.com/public"))


class ExperimentGitAndRunTests(unittest.TestCase):
    def test_retests_require_deployment_commit_and_date(self):
        experiment = create_experiment("en/a.html", "en", ["p1"], "faq_addition", created_at="2026-08-17T00:00:00+00:00")
        self.assertEqual(retest_plan(experiment)[0]["status"], "NOT_SCHEDULED")
        deployed = register_deployment(experiment, "abcdef123456", "2026-08-17T00:00:00+00:00")
        self.assertEqual([row["day"] for row in retest_plan(deployed)], [7, 14, 30])
        self.assertEqual(deployed["cooling_until"], "2026-08-31T00:00:00+00:00")

    def test_small_or_unpaired_experiment_stays_unknown(self):
        self.assertEqual(classify_result([False] * 9, [True] * 9), "UNKNOWN")
        self.assertEqual(classify_result([False] * 10, [True] * 9), "UNKNOWN")

    def test_emergency_revert_requires_ai_ownership_and_severe_regression(self):
        self.assertEqual(emergency_revert_plan("abcdef12", False, True, True)["decision"], "DENIED")
        allowed = emergency_revert_plan("abcdef12", True, True, True)
        self.assertEqual(allowed["decision"], "CREATE_REVERT_PR")
        self.assertFalse(allowed["direct_main_write"])
        self.assertFalse(allowed["auto_merge"])

    def test_emergency_switch_is_health_only_and_auto_l1_downgrades(self):
        disabled = runtime_state({"AI_GEO_ENABLED":"false","AI_GEO_MODE":"DRY_RUN"})
        self.assertFalse(disabled["enabled"])
        auto = runtime_state({"AI_GEO_ENABLED":"true","AI_GEO_MODE":"AUTO_L1"})
        self.assertEqual(auto["mode"], "DRY_RUN")
        self.assertEqual(auto["blocked"], "REQUIRES_GITHUB_PERMISSION")

    def test_git_controller_never_pushes_in_dry_run(self):
        result = simulate_git_action("en", ["en/a.html"], ["p1"], "improve FAQ", 10, 20, {"seo":"PASS"})
        self.assertFalse(result["push_performed"])
        self.assertFalse(result["merged"])
        self.assertFalse(result["deployed"])

    def test_visibility_score_is_no_data_when_incomplete(self):
        result = visibility_score({"citation_frequency":0.5})
        self.assertEqual(result["status"], "no-data")
        self.assertIsNone(result["score"])
        self.assertFalse(result["industry_standard"])

    def test_visibility_weights_produce_bounded_internal_score(self):
        metrics = {"citation_frequency":1,"citation_position":1,"prompt_coverage":1,"language_coverage":1,"commercial_intent_coverage":1,"brand_product_mention":1,"competitor_share_inverse":1}
        self.assertEqual(visibility_score(metrics)["score"], 100)

    def test_learning_never_overrides_risk_policy(self):
        result = aggregate_learning([{"language":"en","page_type":"product","change_type":"faq_addition","result":"WIN"}])
        self.assertEqual(result[0]["success_rate"], 1.0)
        self.assertFalse(result[0]["risk_policy_override"])

    def test_scheduler_has_exact_utc_crons(self):
        self.assertEqual(schedule_for("daily"), "0 2 * * *")
        self.assertEqual(schedule_for("weekly"), "0 3 * * 1")
        self.assertEqual(schedule_for("monthly"), "0 4 1 * *")

    def test_fixture_full_loop_is_idempotent_and_production_safe(self):
        with tempfile.TemporaryDirectory() as directory:
            first = run_pipeline(Path(directory), REPO, fixture=True)
            second = run_pipeline(Path(directory), REPO, fixture=True)
            self.assertEqual(first["prompts"], 40)
            self.assertEqual(first["citations"], 40)
            self.assertEqual(first["feature_observations"], 46)
            self.assertEqual(first["tasks"], 2)
            self.assertEqual(first["experiments"], 2)
            self.assertEqual(first["gemini"], "SKIPPED_NO_CREDENTIAL")
            self.assertTrue(first["metrics"]["fixture_excluded_from_live"])
            self.assertEqual(first["metrics"]["live"]["eligible"], 0)
            self.assertFalse(first["production_modified"])
            self.assertEqual(first["sqlite"], second["sqlite"])
            plans = json.loads((Path(directory) / "data/experiments/retest-plans.json").read_text())["plans"]
            self.assertTrue(all(rows[0]["status"] == "NOT_SCHEDULED" for rows in plans.values()))

    def test_workflow_is_read_only_and_has_no_production_job(self):
        text = (REPO / ".github/workflows/ai-geo-observe.yml").read_text()
        self.assertIn("contents: read", text)
        self.assertNotIn("contents: write", text)
        self.assertNotIn("pull-requests: write", text)
        self.assertNotIn("pages: write", text)
        self.assertIn("AI_GEO_MODE: DRY_RUN", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
