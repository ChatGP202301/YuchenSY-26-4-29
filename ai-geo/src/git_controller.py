from __future__ import annotations

from core import runtime_state, stable_id, utc_now
from guards import diff_guard


def simulate_git_action(language: str, pages: list[str], prompt_ids: list[str], reason: str, before_score, after_score, validation: dict) -> dict:
    state = runtime_state()
    experiment = stable_id("experiment", {"language":language,"pages":pages,"prompts":prompt_ids,"reason":reason})
    return {
        "status":"SIMULATED" if state["mode"] == "DRY_RUN" else "READY_FOR_GUARDS", "mode":state["mode"], "branch":f"ai-geo/{utc_now()[:10]}/{language}-{experiment[-8:]}",
        "commit_subject":f"GEO({language.upper()}): {reason}",
        "commit_body":{"Risk":"L2","Language":language,"Pages":pages,"Prompt IDs":prompt_ids,"Reason":reason,"Before score":before_score,"After score":after_score,"Validation result":validation,"Experiment ID":experiment},
        "push_performed":False,"pr_created":False,"merged":False,"deployed":False,"production_modified":False,"blocked":state.get("blocked"),
    }


def emergency_revert_plan(commit: str, ai_owned: bool, severe_technical_regression: bool, head_contains_commit: bool) -> dict:
    if not (ai_owned and severe_technical_regression and head_contains_commit and len(commit) >= 7):
        return {"decision":"DENIED","direct_main_write":False}
    return {"decision":"CREATE_REVERT_PR","branch":f"ai-geo/emergency-revert-{commit[:8]}","command":["git","revert",commit],"direct_main_write":False,"force_push":False,"auto_merge":False}
