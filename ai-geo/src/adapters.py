from __future__ import annotations

import json
import ipaddress
import os
import re
from abc import ABC, abstractmethod
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from core import load_config, normalize_url, sha256_text, stable_id, utc_now

MANUAL_ENGINES = {"chatgpt_web", "google_ai_web", "perplexity_web", "deepseek_web", "yandex_ai_web", "grok_web", "copilot_web", "yuanbao_web"}


def validated_https_reference(value: str, label: str) -> str:
    parsed = urlsplit(value.strip())
    if parsed.scheme.lower() != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError(f"{label} must be an HTTPS URL without credentials")
    if parsed.port not in {None, 443}:
        raise ValueError(f"{label} must use port 443")
    try:
        address = ipaddress.ip_address(parsed.hostname)
    except ValueError:
        address = None
    if address is not None and not address.is_global:
        raise ValueError(f"{label} cannot use a private or non-global address")
    return normalize_url(value)


class AIEngineAdapter(ABC):
    name = "base"
    surface = "unknown"

    @abstractmethod
    def search(self, prompt: dict) -> dict:
        raise NotImplementedError

    def parse_answer(self, payload: dict) -> dict:
        return payload

    def extract_citations(self, payload: dict) -> list[dict]:
        return []

    def normalize_urls(self, citations: list[dict]) -> list[dict]:
        result = []
        for row in citations:
            item = dict(row)
            item["url"] = normalize_url(str(item["url"]))
            result.append(item)
        return result


class ManualImportAdapter(AIEngineAdapter):
    surface = "web"

    def __init__(self, engine: str):
        if engine not in MANUAL_ENGINES:
            raise ValueError(f"unsupported manual engine: {engine}")
        self.name = engine

    def search(self, prompt: dict) -> dict:
        return {"status":"MANUAL_REQUIRED", "engine":self.name, "prompt_id":prompt["prompt_id"]}


class GeminiFreeAdapter(AIEngineAdapter):
    name = "gemini_api"
    surface = "api"

    def __init__(self, env: dict[str, str] | None = None):
        self.env = os.environ if env is None else env
        self.config = load_config("system.yaml")

    def eligibility(self) -> str:
        if not self.env.get("GEMINI_API_KEY"):
            return "SKIPPED_NO_CREDENTIAL"
        if self.env.get(self.config["gemini_free_confirmation_env"], "").lower() != "true":
            return "SKIPPED_FREE_TIER_UNCONFIRMED"
        if self.config["budget_usd"] != 0:
            return "DENIED_NONZERO_BUDGET"
        return "ELIGIBLE"

    def search(self, prompt: dict) -> dict:
        if prompt.get("source") != "curated_local_v1":
            return {
                "status":"DENIED_NONPUBLIC_PROMPT",
                "engine":self.name,
                "prompt_id":prompt.get("prompt_id"),
                "stop_sampling":True,
            }
        status = self.eligibility()
        if status != "ELIGIBLE":
            return {"status":status, "engine":self.name, "prompt_id":prompt["prompt_id"]}
        model = self.config["gemini_model"]
        key = self.env["GEMINI_API_KEY"]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        body = {
            "contents":[{"parts":[{"text":prompt["prompt_text"]}]}],
            "tools":[{"google_search":{}}],
        }
        request = Request(url, data=json.dumps(body).encode(), headers={"Content-Type":"application/json", "x-goog-api-key":key}, method="POST")
        try:
            with urlopen(request, timeout=30) as response:
                payload = json.loads(response.read(1024 * 1024))
        except HTTPError as exc:
            code = int(exc.code)
            terminal = code in {403, 429}
            return {
                "status":f"STOPPED_HTTP_{code}" if terminal else f"ERROR_HTTP_{code}",
                "engine":self.name,
                "prompt_id":prompt["prompt_id"],
                "http_status":code,
                "stop_sampling":True,
            }
        except (URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            return {
                "status":"ERROR_NETWORK_RESPONSE",
                "engine":self.name,
                "prompt_id":prompt["prompt_id"],
                "error_type":type(exc).__name__,
                "stop_sampling":True,
            }
        text_parts = []
        citations = []
        query_hashes = []
        grounding_used = False
        for candidate in payload.get("candidates", []):
            for part in candidate.get("content", {}).get("parts", []):
                if isinstance(part.get("text"), str):
                    text_parts.append(part["text"])
            grounding = candidate.get("groundingMetadata", {})
            if grounding:
                grounding_used = True
            for query in grounding.get("webSearchQueries", []):
                if isinstance(query, str):
                    query_hashes.append(sha256_text(query))
            for position, chunk in enumerate(grounding.get("groundingChunks", []), 1):
                web = chunk.get("web", {})
                if web.get("uri"):
                    citations.append({"url":web["uri"], "position":position, "title":web.get("title", "")})
        answer = "\n".join(text_parts)
        citations = self.normalize_urls(citations)
        return {
            "status":"OK",
            "observation_status":"cited" if citations else "no-citation",
            "engine":self.name,
            "surface":self.surface,
            "model":model,
            "prompt_id":prompt["prompt_id"],
            "answer_sha256":sha256_text(answer),
            "grounding_used":grounding_used,
            "search_query_count":len(query_hashes),
            "search_query_sha256":query_hashes,
            "citations":citations,
            "captured_at":utc_now(),
            "stop_sampling":False,
        }


def validate_import_record(record: dict, our_domain: str = "www.yuchensy.com") -> dict:
    required = {"AI_engine", "language", "country", "prompt_id", "prompt", "intent", "captured_at", "source"}
    missing = sorted(required - set(record))
    if missing:
        raise ValueError(f"missing citation fields: {missing}")
    if record["source"] not in {"live", "manual", "fixture"}:
        raise ValueError("invalid citation source")
    evidence_url = validated_https_reference(str(record["evidence_url"]), "evidence_url") if record.get("evidence_url") else None
    screenshot_sha256 = str(record.get("screenshot_sha256") or "").lower() or None
    if screenshot_sha256 and not re.fullmatch(r"[0-9a-f]{64}", screenshot_sha256):
        raise ValueError("screenshot_sha256 must be a full SHA-256 hex digest")
    evidence_present = bool(evidence_url or screenshot_sha256)
    default_verified = record["source"] in {"live", "fixture"} or (record["source"] == "manual" and evidence_present)
    supplied_verified = record.get("verified", default_verified)
    if isinstance(supplied_verified, str):
        verified = supplied_verified.strip().lower() == "true"
    else:
        verified = bool(supplied_verified)
    if record["source"] == "manual" and not evidence_present:
        verified = False
    citations = []
    for index, value in enumerate(record.get("citations", []), 1):
        url = validated_https_reference(str(value.get("url", "")), "citation URL")
        citations.append({"url":url, "position":int(value.get("position", index)), "title":str(value.get("title", ""))})
    our_urls = [row["url"] for row in citations if (row["url"].split("/", 3)[2].lower() == our_domain)]
    identity = {"engine":record["AI_engine"], "surface":record.get("surface", "web"), "prompt_id":record["prompt_id"], "captured_at":record["captured_at"], "source":record["source"]}
    return {
        "schema_version":1, "citation_id":stable_id("citation", identity), "timestamp":record["captured_at"],
        "AI_engine":record["AI_engine"], "surface":record.get("surface", "web"), "model_interface":record.get("model_interface", "unknown"),
        "language":record["language"], "country":record["country"], "prompt_id":record["prompt_id"], "prompt":record["prompt"], "intent":record["intent"],
        "answer_sha256":record.get("answer_sha256", ""), "citations":citations, "our_domain":our_domain, "our_url":our_urls[0] if our_urls else None,
        "our_cited":bool(our_urls), "our_position":next((row["position"] for row in citations if row["url"] in our_urls), None),
        "source":record["source"], "evidence_url":evidence_url, "screenshot_sha256":screenshot_sha256, "verified":verified,
        "notes":record.get("notes", ""),
    }
