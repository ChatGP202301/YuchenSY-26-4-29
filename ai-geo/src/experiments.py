from __future__ import annotations

from datetime import datetime, timedelta, timezone

from core import stable_id, utc_now


def create_experiment(page: str, language: str, prompt_ids: list[str], change_type: str, baseline_citation_rate=None, baseline_seo=None, created_at: str | None = None) -> dict:
    created = created_at or utc_now()
    identity = {"page":page,"language":language,"prompts":sorted(prompt_ids),"created":created,"change":change_type}
    return {"schema_version":1,"experiment_id":stable_id("experiment", identity),"page":page,"language":language,"prompt_set":sorted(prompt_ids),"baseline_citation_rate":baseline_citation_rate,"baseline_seo_metrics":baseline_seo or {},"change_type":change_type,"commit":None,"deployment_date":None,"7d_metrics":None,"14d_metrics":None,"30d_metrics":None,"result":"UNKNOWN","created_at":created,"cooling_until":None}


def register_deployment(experiment: dict, commit: str, deployment_date: str) -> dict:
    if len(commit) < 7: raise ValueError("deployment commit is required")
    deployed = datetime.fromisoformat(deployment_date.replace("Z", "+00:00"))
    result = dict(experiment)
    result["commit"] = commit
    result["deployment_date"] = deployed.isoformat()
    result["cooling_until"] = (deployed + timedelta(days=14)).isoformat()
    return result


def retest_plan(experiment: dict) -> list[dict]:
    if not experiment.get("commit") or not experiment.get("deployment_date"):
        return [{"status":"NOT_SCHEDULED","reason":"deployment_commit_and_date_required"}]
    deployed = datetime.fromisoformat(experiment["deployment_date"].replace("Z", "+00:00"))
    return [{"schema_version":1,"retest_id":stable_id("retest", {"experiment":experiment["experiment_id"],"day":day}),"experiment_id":experiment["experiment_id"],"day":day,"scheduled_for":(deployed+timedelta(days=day)).isoformat(),"status":"SCHEDULED"} for day in (7,14,30)]


def classify_result(paired_before: list[bool], paired_after: list[bool]) -> str:
    if len(paired_before) != len(paired_after) or len(paired_before) < 10: return "UNKNOWN"
    delta = sum(paired_after) - sum(paired_before)
    if delta >= 2: return "WIN"
    if delta <= -2: return "LOSS"
    return "NEUTRAL"
