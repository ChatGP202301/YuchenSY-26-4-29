from __future__ import annotations

import fnmatch
import re
from datetime import datetime, timezone
from pathlib import Path

from core import load_config


def normalized_repo_path(path: str) -> str:
    clean = path.replace("\\", "/")
    while clean.startswith("./"):
        clean = clean[2:]
    return clean.lstrip("/")


def path_denied(path: str, policy: dict | None = None) -> bool:
    policy = policy or load_config("risk-policy.yaml")
    clean = normalized_repo_path(path)
    return any(fnmatch.fnmatch(clean, pattern) for pattern in policy["deny_paths"])


def protected_page(path: str, signals: list[str] | None = None) -> bool:
    config = load_config("protected-pages.yaml")
    clean = normalized_repo_path(path)
    if clean in config["exact_paths"] or any(fnmatch.fnmatch(clean, pattern) for pattern in config["patterns"]):
        return True
    return bool(set(signals or []) & set(config["dynamic_sources"]))


def in_cooling(last_changed_at: str | None, days: int = 14, now: datetime | None = None) -> bool:
    if not last_changed_at: return False
    now = now or datetime.now(timezone.utc)
    changed = datetime.fromisoformat(last_changed_at.replace("Z", "+00:00"))
    return (now - changed).total_seconds() < days * 86400


def content_guard(added_text: str, trusted: dict | None = None) -> dict:
    trusted = trusted or load_config("trusted-facts.json")
    normalized = added_text.casefold()
    approved = [(str(item.get("predicate", "")).casefold(), str(item["value"]).casefold()) for item in trusted["facts"] if item.get("status") == "verified"]
    violations = []
    for term in trusted["forbidden_without_explicit_fact"]:
        term_key = term.casefold()
        has_matching_fact = any(term_key in predicate or term_key in value for predicate, value in approved)
        mentions_term = bool(re.search(rf"(?<!\w){re.escape(term_key)}(?!\w)", normalized, re.I))
        if mentions_term and not has_matching_fact:
            violations.append(f"unverified_claim:{term}")
    if re.search(r"\b(guaranteed|always|100%|best in the world|永久|保证100%)\b", added_text, re.I):
        violations.append("unsupported_absolute_claim")
    if re.search(r"\bupdated\s+(today|202[0-9]-[01][0-9]-[0-3][0-9])\b", added_text, re.I):
        violations.append("unverified_freshness_claim")
    return {"passed":not violations, "violations":sorted(set(violations))}


def diff_guard(files: list[str], added_lines: int, deleted_lines: int, pages: int, weekly: bool = False) -> dict:
    policy = load_config("risk-policy.yaml")
    limits = policy["limits"]
    total = added_lines + deleted_lines
    deletion_ratio = deleted_lines / max(total, 1)
    violations = []
    if any(path_denied(path, policy) for path in files): violations.append("protected_file")
    if len(files) > limits["files"]: violations.append("file_limit")
    if total > limits["changed_lines"]: violations.append("line_limit")
    if pages > limits["weekly_pages" if weekly else "daily_pages"]: violations.append("page_limit")
    if deletion_ratio > limits["deletion_ratio"]: violations.append("deletion_ratio")
    return {"passed":not violations, "violations":violations, "total_lines":total, "deletion_ratio":round(deletion_ratio, 6)}


def seo_guard(before: dict, after: dict) -> dict:
    protected_keys = ["canonical", "hreflang", "robots"]
    violations = [f"unexpected_{key}_change" for key in protected_keys if before.get(key) != after.get(key)]
    if after.get("schema_errors"): violations.append("schema_error")
    if before.get("h1_count") != after.get("h1_count"): violations.append("h1_count_change")
    before_counts, after_counts = before.get("site_counts", {}), after.get("site_counts", {})
    for key in ("html_pages", "sitemap_urls", "indexable_pages", "broken_links", "not_found"):
        if key in before_counts and before_counts.get(key) != after_counts.get(key):
            violations.append(f"site_{key}_change")
    return {"passed":not violations, "violations":violations}


def classify_risk(proposal: dict) -> dict:
    policy = load_config("risk-policy.yaml")
    reasons = []
    files = proposal.get("files", [])
    operations = set(proposal.get("operations", []))
    if any(path_denied(path, policy) for path in files) or operations & set(policy["deny_operations"]):
        return {"risk":"L3", "decision":"DENIED", "reasons":["protected_path_or_operation"]}
    if protected_page(proposal.get("page", ""), proposal.get("protected_signals")):
        reasons.append("protected_page")
    if proposal.get("ownership") != "verified": reasons.append("ownership_unknown")
    if proposal.get("gsc_status") in {None, "unknown", "no-data"}: reasons.append("gsc_unknown")
    if proposal.get("already_ai_cited"): reasons.append("already_ai_cited")
    if proposal.get("change_type") in policy["l2_change_types"]: reasons.append("l2_change_type")
    if proposal.get("content_guard", {}).get("passed") is False: reasons.append("content_guard_failed")
    if proposal.get("seo_guard", {}).get("passed") is False: reasons.append("seo_guard_failed")
    if proposal.get("diff_guard", {}).get("passed") is False: reasons.append("diff_guard_failed")
    if in_cooling(proposal.get("last_changed_at"), policy["limits"]["cooling_days"]): reasons.append("cooling")
    if reasons: return {"risk":"L2", "decision":"REVIEW_REQUIRED", "reasons":reasons}
    if proposal.get("change_type") not in policy["l1_change_types"]:
        return {"risk":"L2", "decision":"REVIEW_REQUIRED", "reasons":["unknown_change_type"]}
    if not proposal.get("citation_gap_verified") or not proposal.get("trusted_facts_verified"):
        return {"risk":"L2", "decision":"REVIEW_REQUIRED", "reasons":["evidence_incomplete"]}
    return {"risk":"L1", "decision":"SAFE_AUTO_ELIGIBLE", "reasons":[]}
