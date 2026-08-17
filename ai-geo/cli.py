#!/usr/bin/env python3
"""Standard-library CLI for the isolated AI GEO control plane."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from adapters import GeminiFreeAdapter, ManualImportAdapter, validate_import_record
from core import atomic_write_json, load_config, runtime_state
from experiments import retest_plan
from features import audit_features, compare_feature_sets, explain_factor
from page_analyzer import analyze_file
from pipeline import analyze_citations, draft_task, run_pipeline
from prompts import discover_prompts
from reporting import write_markdown_report
from storage import append_jsonl_idempotent, read_jsonl


def emit(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def read_records(path: Path) -> list[dict]:
    if path.suffix.lower() == ".jsonl":
        return read_jsonl(path)
    if path.suffix.lower() == ".csv":
        records = []
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                value = dict(row)
                for field in ("citations", "citations_json"):
                    if value.get(field):
                        value["citations"] = json.loads(value.pop(field))
                        break
                records.append(value)
        return records
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, dict) and isinstance(value.get("records"), list):
        return value["records"]
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return [value]
    raise ValueError("input must be a JSON object/list or JSONL records")


def configured_language(code: str) -> dict:
    config = load_config("languages.yaml")
    row = next((item for item in config["records"] if item["language_code"] == code), None)
    if row is None:
        raise ValueError(f"unknown language: {code}")
    return row


def command_doctor(_: argparse.Namespace) -> int:
    languages = load_config("languages.yaml")
    factors = load_config("citation-factors.json")
    state = runtime_state()
    result = {
        "status": "BLOCKED" if state.get("blocked") else ("PASS" if state["mode"] == "DRY_RUN" else "READY"),
        "languages_detected": languages["detected_scope_count"],
        "language_records": len(languages["records"]),
        "languages_enabled": [row["language_code"] for row in languages["records"] if row["enabled"]],
        "citation_hypotheses": len(factors["factors"]),
        "runtime": state,
        "gemini": GeminiFreeAdapter().eligibility(),
        "production_modified": False,
    }
    emit(result)
    return 2 if state.get("blocked") else 0


def command_discover(args: argparse.Namespace) -> int:
    languages = args.languages or ["en", "ru"]
    records = discover_prompts(languages, args.per_language)
    if args.output:
        added = append_jsonl_idempotent(Path(args.output), records, "prompt_id")
    else:
        added = len(records)
    emit({"status": "PASS", "records": len(records), "added": added, "languages": languages, "output": args.output})
    return 0


def sample_budget(prompts: list[dict], language: str, requested: int) -> tuple[list[dict], dict]:
    row = configured_language(language)
    system = load_config("system.yaml")
    hard_cap = int(system["daily_live_caps"].get(language, 0))
    configured_cap = int(row["max_daily_prompts"])
    limit = min(max(0, requested), hard_cap, configured_cap)
    selected = [item for item in prompts if item["language"] == language][:limit]
    return selected, {"requested": requested, "hard_cap": hard_cap, "configured_cap": configured_cap, "selected": len(selected)}


def select_grounded_proof_prompts(prompts: list[dict]) -> tuple[list[dict], dict]:
    """Select exactly two public EN and two public RU Prompts for one local proof."""
    selected = []
    by_language = {}
    for language in ("en", "ru"):
        candidates = [row for row in prompts if row.get("language") == language][:2]
        if len(candidates) != 2:
            raise ValueError(f"grounded proof requires exactly two {language} Prompts")
        invalid = [row.get("prompt_id", "unknown") for row in candidates if row.get("source") != "curated_local_v1"]
        if invalid:
            raise ValueError(f"grounded proof accepts only source=curated_local_v1: {invalid}")
        selected.extend(candidates)
        by_language[language] = len(candidates)
    if len(selected) > 4:
        raise ValueError("grounded proof exceeds total hard cap 4")
    return selected, {"requested_per_language":2, "selected_by_language":by_language, "selected":len(selected), "total_cap":4}


def validate_proof_output_path(path: Path) -> Path:
    if not path.is_absolute():
        raise ValueError("grounded proof output must use an absolute path under /private/tmp")
    resolved = path.expanduser().resolve()
    allowed_root = Path("/private/tmp").resolve()
    try:
        resolved.relative_to(allowed_root)
    except ValueError as exc:
        raise ValueError("grounded proof output must remain under /private/tmp") from exc
    return resolved


def execute_samples(adapter: object, prompts: list[dict]) -> list[dict]:
    results = []
    for prompt in prompts:
        result = adapter.search(prompt)
        results.append(result)
        if result.get("stop_sampling"):
            break
    return results


def command_sample(args: argparse.Namespace) -> int:
    prompts = read_records(Path(args.prompts))
    if args.grounded_proof:
        if args.engine != "gemini_api":
            raise ValueError("grounded proof supports only gemini_api")
        if not args.output:
            raise ValueError("grounded proof requires --output under /private/tmp")
        output = validate_proof_output_path(Path(args.output))
        selected, quota = select_grounded_proof_prompts(prompts)
    else:
        if not args.language:
            raise ValueError("--language is required unless --grounded-proof is set")
        output = Path(args.output) if args.output else None
        selected, quota = sample_budget(prompts, args.language, args.limit)
    if args.engine == "gemini_api":
        adapter = GeminiFreeAdapter()
    else:
        adapter = ManualImportAdapter(args.engine)
    results = execute_samples(adapter, selected)
    statuses = [row.get("status", "UNKNOWN") for row in results]
    if statuses and all(status == "OK" for status in statuses):
        status = "PASS"
    elif statuses and statuses[0].startswith("SKIPPED_"):
        status = statuses[0]
    elif any(row.get("stop_sampling") for row in results):
        status = "STOPPED"
    else:
        status = "PARTIAL"
    if output:
        atomic_write_json(output, {"schema_version": 1, "status":status, "engine":args.engine, "results":results, "quota":quota})
    emit({"status":status, "engine":args.engine, "quota":quota, "results":results, "output":str(output) if output else None})
    return 0


def command_import(args: argparse.Namespace) -> int:
    records = [validate_import_record(row, args.our_domain) for row in read_records(Path(args.input))]
    added = append_jsonl_idempotent(Path(args.output), records, "citation_id")
    emit({"status": "PASS", "validated": len(records), "added": added, "output": args.output})
    return 0


def command_analyze(args: argparse.Namespace) -> int:
    result = analyze_citations(read_records(Path(args.citations)))
    if args.output:
        atomic_write_json(Path(args.output), {"schema_version": 1, **result})
    emit(result)
    return 0


def command_draft(args: argparse.Namespace) -> int:
    site_root = Path(args.site_root).resolve()
    page_path = Path(args.page)
    page = analyze_file(site_root / page_path, site_root)
    prompts = read_records(Path(args.prompts))
    gap = {"snapshot_id": "manual-gap", "OUR_PAGE_GAPS": [{"gap": "evidence_collection_required"}]}
    task = draft_task(page_path.as_posix(), prompts, gap, page)
    if args.output:
        atomic_write_json(Path(args.output), {"schema_version": 1, "tasks": [task]})
    emit(task)
    return 0


def command_report(args: argparse.Namespace) -> int:
    output = Path(args.output)
    write_markdown_report(output, args.title, [], [], [], [], [])
    emit({"status": "PASS", "output": str(output), "production_modified": False})
    return 0


def command_retest(args: argparse.Namespace) -> int:
    records = read_records(Path(args.experiment))
    result = {row["experiment_id"]: retest_plan(row) for row in records}
    if args.output:
        atomic_write_json(Path(args.output), {"schema_version": 1, "plans": result})
    emit(result)
    return 0


def command_run(args: argparse.Namespace) -> int:
    state = runtime_state()
    if not state["enabled"]:
        emit({"status": "HEALTH_ONLY", "runtime": state, "production_modified": False})
        return 0
    result = run_pipeline(Path(args.output), Path(args.site_root), fixture=args.fixture)
    emit(result)
    return 0


def command_features_audit(args: argparse.Namespace) -> int:
    site_root = Path(args.site_root).resolve()
    page = analyze_file(site_root / args.page, site_root)
    rows = audit_features(page, args.page, args.language, prompt_id=args.prompt_id)
    if args.output:
        append_jsonl_idempotent(Path(args.output), rows, "observation_id")
    emit({"status": "PASS", "page": args.page, "observations": rows})
    return 0


def command_features_explain(args: argparse.Namespace) -> int:
    emit(explain_factor(args.factor_id))
    return 0


def command_features_compare(args: argparse.Namespace) -> int:
    result = compare_feature_sets(read_records(Path(args.before)), read_records(Path(args.after)), args.citation_before, args.citation_after)
    if args.output:
        atomic_write_json(Path(args.output), {"schema_version": 1, **result})
    emit(result)
    return 0


def parser() -> argparse.ArgumentParser:
    top = argparse.ArgumentParser(prog="ai-geo", description="Safe multilingual AI citation observation and task drafting")
    commands = top.add_subparsers(dest="command", required=True)
    doctor = commands.add_parser("doctor")
    doctor.set_defaults(func=command_doctor)

    discover = commands.add_parser("discover-prompts")
    discover.add_argument("--languages", nargs="+")
    discover.add_argument("--per-language", type=int, default=20)
    discover.add_argument("--output")
    discover.set_defaults(func=command_discover)

    sample = commands.add_parser("sample")
    sample.add_argument("--prompts", required=True)
    sample.add_argument("--language")
    sample.add_argument("--engine", default="gemini_api")
    sample.add_argument("--limit", type=int, default=20)
    sample.add_argument("--grounded-proof", action="store_true")
    sample.add_argument("--output")
    sample.set_defaults(func=command_sample)

    importer = commands.add_parser("import")
    importer.add_argument("--input", required=True)
    importer.add_argument("--output", required=True)
    importer.add_argument("--our-domain", default="www.yuchensy.com")
    importer.set_defaults(func=command_import)

    analyze = commands.add_parser("analyze")
    analyze.add_argument("--citations", required=True)
    analyze.add_argument("--output")
    analyze.set_defaults(func=command_analyze)

    draft = commands.add_parser("draft-tasks")
    draft.add_argument("--site-root", default=".")
    draft.add_argument("--page", required=True)
    draft.add_argument("--prompts", required=True)
    draft.add_argument("--output")
    draft.set_defaults(func=command_draft)

    report = commands.add_parser("report")
    report.add_argument("--output", required=True)
    report.add_argument("--title", default="AI GEO Status Report")
    report.set_defaults(func=command_report)

    retest = commands.add_parser("retest")
    retest.add_argument("--experiment", required=True)
    retest.add_argument("--output")
    retest.set_defaults(func=command_retest)

    run = commands.add_parser("run")
    run.add_argument("--site-root", default=".")
    run.add_argument("--output", required=True)
    run.add_argument("--fixture", action="store_true")
    run.set_defaults(func=command_run)

    features = commands.add_parser("features")
    feature_commands = features.add_subparsers(dest="feature_command", required=True)
    audit = feature_commands.add_parser("audit")
    audit.add_argument("--site-root", default=".")
    audit.add_argument("--page", required=True)
    audit.add_argument("--language", required=True)
    audit.add_argument("--prompt-id")
    audit.add_argument("--output")
    audit.set_defaults(func=command_features_audit)
    explain = feature_commands.add_parser("explain")
    explain.add_argument("factor_id")
    explain.set_defaults(func=command_features_explain)
    compare = feature_commands.add_parser("compare")
    compare.add_argument("--before", required=True)
    compare.add_argument("--after", required=True)
    compare.add_argument("--citation-before", type=float)
    compare.add_argument("--citation-after", type=float)
    compare.add_argument("--output")
    compare.set_defaults(func=command_features_compare)
    return top


def main() -> int:
    try:
        arguments = parser().parse_args()
        return int(arguments.func(arguments))
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        emit({"status": "FAIL", "error": str(exc), "production_modified": False})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
