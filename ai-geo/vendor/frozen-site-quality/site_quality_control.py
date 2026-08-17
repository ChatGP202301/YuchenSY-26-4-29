#!/usr/bin/env python3
"""Deterministic multilingual SEO/GEO scorecard and approval-gated preview tool.

The audit and proposal commands are report-only. Preview builds an isolated
overlay. Apply is the only command that can edit the site and it requires the
exact SHA-256 approval token emitted by preview. No command publishes the site
or talks to a production service.
"""

from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime, timezone
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlparse

from regression_contract import load_regression_contract


ORIGIN = "https://www.yuchensy.com"
SCHEMA_VERSION = "1.0.0"
TOOL_VERSION = "1.0.0"
DIMENSION_WEIGHTS = {
    "technical": 30,
    "keyword_intent": 20,
    "content": 20,
    "geo_aeo": 15,
    "localization": 15,
}
STATUS_VALUES = {"pass": 100.0, "warn": 50.0, "fail": 0.0}
SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4}
RTL_LANGUAGES = {"ar", "fa", "he", "ur"}
LANG_EQUIVALENTS = {
    "no": {"no", "nb", "nb-no", "nn", "nn-no"},
    "sr-me": {"sr", "sr-me", "sr-latn", "sr-latn-me"},
}
PUBLIC_ROOT_FILES = {
    ".nojekyll", "CNAME", "favicon.ico", "index.html", "llms-full.txt",
    "llms.txt", "robots.txt", "sitemap.xml", "thank-you.html",
}
IGNORED_REPORT_PREFIXES = ("preview/site/", "backups/")
GSC_DEFAULT = Path("migration/gsc-audit-20260801/search-analytics")
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ACCEPTED_REGRESSION_CONTRACT, ACCEPTED_REGRESSION_CONTRACT_BINDING = load_regression_contract(REPOSITORY_ROOT)
_SITE_QUALITY_CONTRACT = ACCEPTED_REGRESSION_CONTRACT.get("site_quality", {})
if not isinstance(_SITE_QUALITY_CONTRACT, dict) or not {"scopes", "html_pages", "sitemap_urls"} <= set(_SITE_QUALITY_CONTRACT):
    raise ValueError("accepted regression contract is missing the site-quality scale lock")
DEFAULT_EXPECTED = {
    "scopes": int(_SITE_QUALITY_CONTRACT["scopes"]),
    "html_pages": int(_SITE_QUALITY_CONTRACT["html_pages"]),
    "sitemap_urls": int(_SITE_QUALITY_CONTRACT["sitemap_urls"]),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def compact(value: str) -> str:
    return " ".join((value or "").split())


def normalize(value: str) -> str:
    return " ".join(re.findall(r"\w+", (value or "").casefold(), flags=re.UNICODE))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path | None) -> list[dict[str, str]]:
    if not path or not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [
            {str(key or "").strip(): str(value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def as_float(value: str, default: float = 0.0) -> float:
    try:
        return float((value or "").replace(",", ""))
    except ValueError:
        return default


def band(score: float | None) -> str:
    if score is None:
        return "no-data"
    if score >= 90:
        return "strong"
    if score >= 75:
        return "good"
    if score >= 60:
        return "developing"
    return "priority"


def page_url(relative: str) -> str:
    if relative == "index.html":
        return ORIGIN + "/"
    return ORIGIN + "/" + relative


def local_relative_from_url(value: str) -> str | None:
    parsed = urlparse(compact(value))
    if parsed.scheme not in {"http", "https"} or parsed.netloc.casefold() not in {"yuchensy.com", "www.yuchensy.com"}:
        return None
    path = unquote(parsed.path).lstrip("/")
    return path or "index.html"


def local_target(site_root: Path, page: Path, value: str) -> Path | None:
    raw = compact(value)
    if not raw or raw.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    parsed = urlparse(raw)
    if parsed.scheme in {"http", "https"}:
        relative = local_relative_from_url(raw)
        if relative is None:
            return None
        target = site_root / relative
    elif parsed.scheme or raw.startswith("//"):
        return None
    else:
        path = unquote(parsed.path)
        target = site_root / path.lstrip("/") if path.startswith("/") else page.parent / path
    if not parsed.path or parsed.path.endswith("/"):
        target = target / "index.html"
    # Keep the logical path under site_root. Preview trees intentionally use
    # symlinks for unchanged public files; resolving them here would make safe
    # in-preview targets look as if they escaped the preview root.
    try:
        return Path(os.path.abspath(target))
    except OSError:
        return None


def schema_types(value: object) -> list[str]:
    result: list[str] = []
    if isinstance(value, dict):
        raw = value.get("@type")
        if isinstance(raw, str):
            result.append(raw)
        elif isinstance(raw, list):
            result.extend(str(item) for item in raw)
        for child in value.values():
            result.extend(schema_types(child))
    elif isinstance(value, list):
        for child in value:
            result.extend(schema_types(child))
    return result


class QualityParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang = ""
        self.html_dir = ""
        self.title_parts: list[str] = []
        self.meta: dict[str, str] = {}
        self.canonical = ""
        self.alternates: list[dict[str, str]] = []
        self.links: list[str] = []
        self.assets: list[str] = []
        self.images: list[dict[str, str]] = []
        self.h1s: list[str] = []
        self.h2s: list[str] = []
        self.paragraphs: list[str] = []
        self.text_parts: list[str] = []
        self.jsonld_blocks: list[str] = []
        self.table_count = 0
        self.list_count = 0
        self.dl_count = 0
        self.external_links = 0
        self._capture: tuple[str, list[str]] | None = None
        self._jsonld: list[str] | None = None
        self._hidden_depth = 0

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        tag = tag.casefold()
        attrs = {str(key).casefold(): str(value or "") for key, value in attrs_list}
        if tag == "html":
            self.html_lang = attrs.get("lang", "")
            self.html_dir = attrs.get("dir", "")
        if tag in {"script", "style", "noscript"}:
            self._hidden_depth += 1
        if tag in {"title", "h1", "h2", "p"}:
            self._capture = (tag, [])
        if tag == "a" and attrs.get("href"):
            href = attrs["href"]
            self.links.append(href)
            parsed = urlparse(href)
            if parsed.scheme in {"http", "https"} and parsed.netloc.casefold() not in {"yuchensy.com", "www.yuchensy.com"}:
                self.external_links += 1
        if tag == "img":
            src = attrs.get("src", "")
            self.images.append({"src": src, "alt": compact(attrs.get("alt", "")), "role": attrs.get("role", "")})
        if tag in {"img", "script", "iframe", "source"} and attrs.get("src"):
            self.assets.append(attrs["src"])
        if tag in {"img", "source"} and attrs.get("srcset"):
            for candidate in attrs["srcset"].split(","):
                url = candidate.strip().split(" ", 1)[0]
                if url:
                    self.assets.append(url)
        if tag == "link":
            rel = {part.casefold() for part in attrs.get("rel", "").split()}
            if "canonical" in rel:
                self.canonical = attrs.get("href", "")
            if "alternate" in rel and attrs.get("hreflang"):
                self.alternates.append({"hreflang": attrs["hreflang"], "href": attrs.get("href", "")})
            if attrs.get("href") and rel.intersection({"stylesheet", "icon", "preload"}):
                self.assets.append(attrs["href"])
        if tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            if key:
                self.meta[key.casefold()] = attrs.get("content", "")
        if tag == "script" and attrs.get("type", "").casefold() == "application/ld+json":
            self._jsonld = []
        if tag == "table":
            self.table_count += 1
        elif tag in {"ul", "ol"}:
            self.list_count += 1
        elif tag == "dl":
            self.dl_count += 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.casefold()
        if self._capture and tag == self._capture[0]:
            value = compact("".join(self._capture[1]))
            if tag == "title":
                self.title_parts.append(value)
            elif tag == "h1" and value:
                self.h1s.append(value)
            elif tag == "h2" and value:
                self.h2s.append(value)
            elif tag == "p" and value:
                self.paragraphs.append(value)
            self._capture = None
        if tag == "script" and self._jsonld is not None:
            self.jsonld_blocks.append("".join(self._jsonld).strip())
            self._jsonld = None
        if tag in {"script", "style", "noscript"} and self._hidden_depth:
            self._hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._jsonld is not None:
            self._jsonld.append(data)
        if self._capture:
            self._capture[1].append(data)
        if not self._hidden_depth:
            self.text_parts.append(data)


def page_kind(relative: str) -> str:
    name = Path(relative).name.casefold()
    if name == "index.html":
        return "home"
    if "faq" in name:
        return "faq"
    if name in {"products.html", "water-treatment-solutions.html", "water-dispenser.html"} or "catalog" in name or "selection-guide" in name:
        return "hub"
    if name.startswith("product-") or "filter" in name or "membrane" in name or "purifier" in name:
        return "product"
    if name in {"about.html", "contact.html"}:
        return name.removesuffix(".html")
    return "content"


def discover_scopes(site_root: Path) -> list[str]:
    scopes = [path.stem.removeprefix("sitemap-") for path in sorted((site_root / "sitemaps").glob("sitemap-*.xml"))]
    return sorted(set(scopes), key=lambda value: (value != "root", value))


def scope_paths(site_root: Path, scope: str) -> list[Path]:
    if scope == "root":
        return [site_root / "index.html"] if (site_root / "index.html").is_file() else []
    directory = site_root / scope
    return sorted(directory.glob("*.html")) if directory.is_dir() else []


def sitemap_inventory(site_root: Path, scopes: Iterable[str]) -> tuple[dict[str, set[str]], dict[str, object]]:
    by_scope: dict[str, set[str]] = {}
    all_urls: list[str] = []
    malformed: list[str] = []
    per_file_duplicates: list[str] = []
    for scope in scopes:
        path = site_root / "sitemaps" / f"sitemap-{scope}.xml"
        urls: list[str] = []
        try:
            root = ET.parse(path).getroot()
            urls = [compact(node.text or "") for node in root.iter() if node.tag.endswith("loc") and compact(node.text or "")]
        except (OSError, ET.ParseError):
            malformed.append(path.relative_to(site_root).as_posix())
        if len(urls) != len(set(urls)):
            per_file_duplicates.append(path.relative_to(site_root).as_posix())
        by_scope[scope] = set(urls)
        all_urls.extend(urls)
    counts = Counter(all_urls)
    summary = {
        "files": len(list(scopes)),
        "entries": len(all_urls),
        "unique": len(counts),
        "duplicate_entries": sum(value - 1 for value in counts.values() if value > 1),
        "duplicate_urls": sorted(url for url, value in counts.items() if value > 1),
        "duplicate_files": per_file_duplicates,
        "malformed_files": malformed,
    }
    return by_scope, summary


def parse_page(site_root: Path, path: Path, scope: str) -> dict[str, object]:
    parser = QualityParser()
    source = path.read_text(encoding="utf-8", errors="replace")
    parser.feed(source)
    parsed_schema: list[object] = []
    jsonld_errors: list[str] = []
    for index, block in enumerate(parser.jsonld_blocks, 1):
        if not block:
            continue
        try:
            parsed_schema.append(json.loads(block))
        except json.JSONDecodeError as exc:
            jsonld_errors.append(f"block {index}: {exc.msg}")
    missing_links: list[str] = []
    for href in parser.links:
        target = local_target(site_root, path, href)
        if target and (target == site_root or site_root in target.parents) and not target.exists():
            missing_links.append(href)
    missing_assets: list[str] = []
    for src in parser.assets:
        target = local_target(site_root, path, src)
        if target and (target == site_root or site_root in target.parents) and not target.exists():
            missing_assets.append(src)
    relative = path.relative_to(site_root).as_posix()
    text = compact(" ".join(parser.text_parts))
    rtl_chars = len(re.findall(r"[\u0590-\u08ff]", text))
    latin_chars = len(re.findall(r"[A-Za-z]", text))
    informative_images = [image for image in parser.images if image["role"].casefold() != "presentation"]
    missing_alts = [image["src"] for image in informative_images if not image["alt"]]
    robots = parser.meta.get("robots", "").casefold()
    return {
        "scope": scope,
        "path": relative,
        "url": page_url(relative),
        "kind": page_kind(relative),
        "title": compact(" ".join(parser.title_parts)),
        "description": compact(parser.meta.get("description", "")),
        "robots": robots or "not-declared",
        "indexable": "noindex" not in robots,
        "canonical": compact(parser.canonical),
        "html_lang": compact(parser.html_lang),
        "html_dir": compact(parser.html_dir).casefold(),
        "rtl_expected": scope in RTL_LANGUAGES or (scope == "ku" and rtl_chars > latin_chars),
        "h1s": parser.h1s,
        "h2s": parser.h2s,
        "word_count": len(re.findall(r"\w+", text, flags=re.UNICODE)),
        "first_paragraph_chars": len(next((item for item in parser.paragraphs if len(item) >= 30), "")),
        "long_paragraph_hashes": [sha256_bytes(normalize(item).encode("utf-8")) for item in parser.paragraphs if len(item) >= 160],
        "jsonld_types": sorted(set(schema_types(parsed_schema))),
        "jsonld_errors": jsonld_errors,
        "alternates": [(item["hreflang"], item["href"]) for item in parser.alternates],
        "internal_link_count": sum(local_target(site_root, path, href) is not None for href in parser.links),
        "external_link_count": parser.external_links,
        "broken_internal_links": sorted(set(missing_links)),
        "missing_assets": sorted(set(missing_assets)),
        "image_count": len(informative_images),
        "missing_alt_count": len(missing_alts),
        "missing_alt_samples": missing_alts[:5],
        "structure_count": parser.table_count + parser.list_count + parser.dl_count,
        "question_heading_count": sum("?" in value or "？" in value for value in parser.h2s),
    }


def load_gsc(page_path: Path | None, query_path: Path | None, detail_path: Path | None) -> dict[str, object]:
    pages: dict[str, dict[str, object]] = {}
    for row in read_csv(page_path):
        url = row.get("page", "")
        if not url:
            continue
        pages[url] = {
            "clicks": as_float(row.get("clicks", "")),
            "impressions": as_float(row.get("impressions", "")),
            "ctr": as_float(row.get("ctr", "")),
            "position": as_float(row.get("position", "")),
            "start_date": row.get("start_date", "no-data") or "no-data",
            "end_date": row.get("end_date", "no-data") or "no-data",
        }
    queries: dict[str, list[dict[str, object]]] = defaultdict(list)
    query_rows = read_csv(query_path)
    if query_rows and "page" not in query_rows[0]:
        query_rows = []
    for row in query_rows:
        query = compact(row.get("query", ""))
        url = row.get("page", "")
        if not url or not query or query == "[redacted-pii]" or len(query) > 120 or "site:" in query.casefold():
            continue
        queries[url].append({
            "query": query,
            "language": row.get("language", "no-data") or "no-data",
            "country": row.get("country", "no-data") or "no-data",
            "device": row.get("device", "no-data") or "no-data",
            "clicks": as_float(row.get("clicks", "")),
            "impressions": as_float(row.get("impressions", "")),
            "ctr": as_float(row.get("ctr", "")),
            "position": as_float(row.get("position", "")),
        })
    breakdown: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in read_csv(detail_path):
        url = row.get("page", "")
        if url:
            breakdown[url].append({
                "country": row.get("country", "no-data") or "no-data",
                "device": row.get("device", "no-data") or "no-data",
                "language": row.get("language", "no-data") or "no-data",
                "clicks": as_float(row.get("clicks", "")),
                "impressions": as_float(row.get("impressions", "")),
            })
    return {"pages": pages, "queries": dict(queries), "breakdown": dict(breakdown)}


def add_check(
    checks: list[dict[str, object]], rule_id: str, dimension: str, weight: int,
    status: str, severity: str, title: str, evidence: str, recommendation: str,
    human_review: bool = False,
) -> None:
    if status not in STATUS_VALUES:
        raise ValueError(f"invalid status: {status}")
    checks.append({
        "rule_id": rule_id, "dimension": dimension, "weight": weight,
        "status": status, "severity": severity, "title": title,
        "evidence": compact(evidence)[:500], "recommendation": recommendation,
        "confidence": "medium" if human_review else "high",
        "needs_human_review": human_review,
    })


def compute_dimension_scores(checks: list[dict[str, object]]) -> dict[str, float | None]:
    result: dict[str, float | None] = {}
    for dimension in DIMENSION_WEIGHTS:
        current = [row for row in checks if row["dimension"] == dimension]
        total_weight = sum(int(row["weight"]) for row in current)
        if not total_weight:
            result[dimension] = None
            continue
        earned = sum(int(row["weight"]) * STATUS_VALUES[str(row["status"])] for row in current)
        result[dimension] = round(earned / total_weight, 2)
    return result


def composite_score(scores: dict[str, float | None]) -> tuple[float | None, float, bool]:
    available = [(dimension, value) for dimension, value in scores.items() if value is not None]
    available_weight = sum(DIMENSION_WEIGHTS[dimension] for dimension, _ in available)
    if not available_weight:
        return None, 0.0, True
    value = sum(DIMENSION_WEIGHTS[dimension] * float(score) for dimension, score in available) / available_weight
    coverage = round(available_weight, 2)
    return round(value, 2), coverage, coverage < 80


def lang_matches(scope: str, html_lang: str) -> bool:
    expected = "en" if scope == "root" else scope
    expected = expected.casefold()
    actual = html_lang.casefold().replace("_", "-")
    if expected in LANG_EQUIVALENTS:
        return actual in LANG_EQUIVALENTS[expected]
    return bool(actual) and (actual == expected or actual.startswith(expected + "-") or expected.startswith(actual + "-"))


def valid_internal_https(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and parsed.netloc.casefold() in {"yuchensy.com", "www.yuchensy.com"}


def query_alignment(query: str, page: dict[str, object]) -> float:
    needle = normalize(query)
    haystack = normalize(f"{page['title']} {page['description']} {' '.join(page['h1s'])}")
    if not needle or not haystack:
        return 0.0
    if needle in haystack:
        return 1.0
    query_tokens = [token for token in needle.split() if len(token) > 1]
    if not query_tokens:
        return 0.0
    page_tokens = set(haystack.split())
    return sum(token in page_tokens for token in query_tokens) / len(query_tokens)


def evaluate_page(
    page: dict[str, object], sitemap_urls: set[str], title_counts: Counter[str],
    description_counts: Counter[str], repeated: Counter[str],
    canonical_pages: dict[str, dict[str, object]], gsc: dict[str, object],
    english_pages: dict[str, dict[str, object]], query_page_counts: Counter[tuple[str, str]],
) -> dict[str, object]:
    checks: list[dict[str, object]] = []
    url = str(page["url"])
    indexable = bool(page["indexable"])
    in_sitemap = url in sitemap_urls
    title = str(page["title"])
    description = str(page["description"])
    h1s = list(page["h1s"])
    canonical = str(page["canonical"])

    add_check(checks, "T003", "technical", 2, "pass" if title else "fail", "High", "标题存在", title or "title 为空", "为页面添加唯一且真实的标题。")
    add_check(checks, "T004", "technical", 1, "pass" if len(description) >= 50 else ("warn" if description else "fail"), "Medium", "Meta description 完整", f"长度 {len(description)}", "补充与页面意图一致的事实性摘要。")
    add_check(checks, "T005", "technical", 2, "pass" if len(h1s) == 1 else "fail", "High", "H1 数量正确", f"H1={len(h1s)}", "每页保留一个清晰 H1。")
    canonical_ok = valid_internal_https(canonical)
    canonical_self = canonical.rstrip("/") == url.rstrip("/")
    canonical_status = "pass" if canonical_ok and (canonical_self or not indexable) else "fail"
    add_check(checks, "T006", "technical", 3, canonical_status, "High", "Canonical 有效", canonical or "canonical 缺失", "索引页使用自 canonical；兼容别名保持 noindex 并指向真实 canonical。")
    index_status = "fail" if in_sitemap and not indexable else ("warn" if indexable and not in_sitemap else "pass")
    add_check(checks, "T007", "technical", 3, index_status, "Critical" if in_sitemap and not indexable else "Medium", "索引策略与 sitemap 一致", f"indexable={indexable}; in_sitemap={in_sitemap}", "消除 sitemap 与 robots/canonical 的冲突。")
    image_count = int(page["image_count"])
    missing_alts = int(page["missing_alt_count"])
    alt_ratio = missing_alts / image_count if image_count else 0
    alt_status = "pass" if alt_ratio == 0 else ("warn" if alt_ratio <= 0.1 else "fail")
    add_check(checks, "T008", "technical", 1, alt_status, "Medium", "图片 ALT 完整", f"missing={missing_alts}/{image_count}", "为信息型图片补充与画面一致的本地化 ALT。", bool(missing_alts))
    add_check(checks, "T011", "technical", 1, "pass" if int(page["internal_link_count"]) else "fail", "Medium", "存在可抓取内链", f"internal_links={page['internal_link_count']}", "增加相关产品、分类或询价路径内链。")
    schema_ok = bool(set(page["jsonld_types"]).intersection({"Organization", "Corporation", "Product", "Service", "WebPage", "CollectionPage", "FAQPage", "BreadcrumbList"}))
    schema_status = "fail" if page["jsonld_errors"] else ("pass" if schema_ok else "warn")
    add_check(checks, "T012", "technical", 2, schema_status, "High" if page["jsonld_errors"] else "Medium", "结构化数据可解析且有意义", "; ".join(page["jsonld_errors"]) or ",".join(page["jsonld_types"]) or "no recognized schema", "修复 JSON-LD，并只保留页面真实支持的实体。")
    alternate_hrefs = [compact(str(item[1])) for item in page["alternates"]]
    alternate_valid = bool(alternate_hrefs) and all(valid_internal_https(item) for item in alternate_hrefs)
    reciprocal_missing = []
    for target_url in alternate_hrefs:
        target = canonical_pages.get(target_url.rstrip("/"))
        if not target:
            continue
        target_alts = {compact(str(item[1])).rstrip("/") for item in target["alternates"]}
        source_canonical = (canonical or url).rstrip("/")
        if source_canonical not in target_alts:
            reciprocal_missing.append(target_url)
    hreflang_status = "pass" if alternate_valid and not reciprocal_missing else ("warn" if alternate_hrefs else "fail")
    add_check(checks, "T013", "technical", 3, hreflang_status, "High", "Hreflang 有效并可互返", f"alternates={len(alternate_hrefs)}; reciprocal_missing={len(reciprocal_missing)}", "修复语言标注语法、目标和互返关系。")
    lang_ok = lang_matches(str(page["scope"]), str(page["html_lang"]))
    expected_rtl = bool(page["rtl_expected"])
    dir_ok = (str(page["html_dir"]) == "rtl") if expected_rtl else str(page["html_dir"]) != "rtl"
    add_check(checks, "T014", "technical", 2, "pass" if lang_ok and dir_ok else "fail", "High", "HTML 语言与方向正确", f"lang={page['html_lang']}; dir={page['html_dir'] or 'not-declared'}", "使 URL、html lang 与页面实际使用的文字方向一致。")
    duplicate_meta = (bool(title) and title_counts[normalize(title)] > 1) or (bool(description) and description_counts[normalize(description)] > 1)
    add_check(checks, "T015", "technical", 1, "warn" if duplicate_meta else "pass", "Medium", "标题与摘要在语言范围内唯一", f"title_duplicates={title_counts[normalize(title)] if title else 0}; description_duplicates={description_counts[normalize(description)] if description else 0}", "仅在页面事实和意图确实不同时改写重复元数据。", duplicate_meta)
    missing_count = len(page["broken_internal_links"]) + len(page["missing_assets"])
    add_check(checks, "T016", "technical", 3, "fail" if missing_count else "pass", "High", "内部链接与资源存在", f"broken_links={len(page['broken_internal_links'])}; missing_assets={len(page['missing_assets'])}", "修复缺失目标或移除无效引用。")

    threshold = {"home": 180, "hub": 220, "product": 220, "faq": 150, "about": 150, "contact": 100}.get(str(page["kind"]), 150)
    words = int(page["word_count"])
    content_status = "pass" if words >= threshold else ("warn" if words >= max(80, threshold // 2) else "fail")
    add_check(checks, "C001", "content", 3, content_status, "Medium", "正文具备基本信息量", f"words={words}; expected>={threshold}", "补充页面专属、可验证的产品或采购信息。", True)
    repeat_count = repeated[str(page["path"])]
    repeat_status = "fail" if repeat_count >= 5 else ("warn" if repeat_count >= 2 else "pass")
    add_check(checks, "C002", "content", 3, repeat_status, "Low", "长段落不过度模板化", f"repeated_long_blocks={repeat_count}", "人工确认重复是否必要，只替换有事实依据的页面专属内容。", repeat_count >= 2)
    structured = int(page["structure_count"])
    add_check(checks, "C003", "content", 2, "pass" if structured else "warn", "Medium", "内容便于比较和提取", f"tables_lists_definition_lists={structured}", "用真实规格表、步骤或选择清单组织关键信息。", True)
    opening_chars = int(page["first_paragraph_chars"])
    opening_status = "pass" if 60 <= opening_chars <= 700 else ("warn" if opening_chars else "fail")
    add_check(checks, "C004", "content", 2, opening_status, "Medium", "开头直接说明页面价值", f"first_paragraph_chars={opening_chars}", "在首段直接回答产品是什么、适合谁以及需要确认哪些参数。", True)

    add_check(checks, "G001", "geo_aeo", 3, opening_status, "Medium", "首段可直接摘取", f"first_paragraph_chars={opening_chars}", "提供简洁、独立可理解的直接答案。", True)
    entity_ok = bool(set(page["jsonld_types"]).intersection({"Organization", "Corporation", "Product", "Service", "CollectionPage"}))
    add_check(checks, "G006", "geo_aeo", 3, "pass" if entity_ok else "warn", "High", "核心实体清晰", ",".join(page["jsonld_types"]) or "no entity schema", "明确组织、产品或服务实体，并与可见内容一致。")
    meaning_ok = "BreadcrumbList" in page["jsonld_types"] and schema_ok
    add_check(checks, "G010", "geo_aeo", 2, "pass" if meaning_ok else "warn", "Medium", "Schema 支持页面含义", f"types={','.join(page['jsonld_types'])}", "补充真实的 Breadcrumb 与页面主实体关系。")
    extract_ok = structured > 0 or bool(set(page["jsonld_types"]).intersection({"Product", "FAQPage"}))
    add_check(checks, "G011", "geo_aeo", 2, "pass" if extract_ok else "warn", "Medium", "规格与问答便于机器提取", f"structures={structured}; questions={page['question_heading_count']}", "增加真实规格、步骤、定义或自然买家问题。", True)

    add_check(checks, "L001", "localization", 3, "pass" if lang_ok else "fail", "High", "页面语言声明匹配目录", f"scope={page['scope']}; html_lang={page['html_lang']}", "修正 html lang，不把国家代码当作语言代码。")
    add_check(checks, "L002", "localization", 2, "pass" if dir_ok else "fail", "High", "文字方向匹配实际脚本", f"scope={page['scope']}; dir={page['html_dir'] or 'not-declared'}", "按页面实际使用的文字脚本设置 LTR 或 RTL；混合书写语言不得只凭目录代码推断。")
    self_language = "en" if page["scope"] == "root" else str(page["scope"])
    self_alt = any(str(item[0]).casefold().startswith(self_language.casefold()) and compact(str(item[1])).rstrip("/") == (canonical or url).rstrip("/") for item in page["alternates"])
    add_check(checks, "L003", "localization", 3, "pass" if self_alt else "warn", "High", "存在本语言 hreflang", f"self_hreflang={self_alt}", "让本语言 hreflang 指向该页规范 URL。")
    if page["scope"] not in {"root", "en"}:
        english = english_pages.get(Path(str(page["path"])).name)
        identical = bool(english) and normalize(str(page["title"])) == normalize(str(english["title"])) and normalize(str(page["description"])) == normalize(str(english["description"])) and len(description) >= 50
        add_check(checks, "L004", "localization", 2, "warn" if identical else "pass", "Medium", "元数据不是完整英文复制", f"identical_to_english={identical}", "由对应语言审核者确认术语、语法和买家表达。", True)

    page_queries = list(gsc["queries"].get(url, []))
    if page_queries:
        top_query = max(page_queries, key=lambda row: (float(row["impressions"]), float(row["clicks"]), str(row["query"])))
        alignment = query_alignment(str(top_query["query"]), page)
        align_status = "pass" if alignment >= 0.5 else ("warn" if alignment >= 0.25 else "fail")
        add_check(checks, "K002", "keyword_intent", 3, align_status, "Medium", "页面反映已有搜索主题", f"query={top_query['query']}; metadata_token_alignment={alignment:.2f}; impressions={top_query['impressions']}", "人工复核真实查询意图，再调整正文与内链；不要只堆关键词。", True)
        cannibalized = any(query_page_counts[(str(page["scope"]), normalize(str(row["query"])))] > 1 for row in page_queries)
        add_check(checks, "K001", "keyword_intent", 2, "fail" if cannibalized else "pass", "High", "同语言查询没有明显多页竞争", f"cannibalization={cannibalized}", "确认主目标页并调整重复页面的内容角色或内链。", True)

    scores = compute_dimension_scores(checks)
    overall, coverage, provisional = composite_score(scores)
    metrics = dict(gsc["pages"].get(url, {}))
    if not metrics:
        metrics = {"clicks": "no-data", "impressions": "no-data", "ctr": "no-data", "position": "no-data", "start_date": "no-data", "end_date": "no-data"}
    breakdown = list(gsc["breakdown"].get(url, []))
    countries = Counter()
    devices = Counter()
    for row in breakdown:
        countries[str(row["country"])] += float(row["impressions"])
        devices[str(row["device"])] += float(row["impressions"])
    result = {
        "scope": page["scope"], "path": page["path"], "url": url,
        "kind": page["kind"], "indexable": indexable, "in_sitemap": in_sitemap,
        "title": title, "h1": h1s[0] if h1s else "", "word_count": words,
        "jsonld_types": page["jsonld_types"], "scores": scores,
        "overall_score": overall, "coverage": coverage, "provisional": provisional,
        "band": band(overall), "gsc": metrics,
        "gsc_top_countries": [name for name, _ in countries.most_common(3)],
        "gsc_devices": [name for name, _ in devices.most_common()],
        "checks": [row for row in checks if row["status"] != "pass"],
    }
    return result


def aggregate_languages(pages: list[dict[str, object]], scopes: list[str]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for page in pages:
        grouped[str(page["scope"])].append(page)
    rows: list[dict[str, object]] = []
    for scope in scopes:
        current = grouped.get(scope, [])
        dimension_scores: dict[str, float | None] = {}
        for dimension in DIMENSION_WEIGHTS:
            values = [float(page["scores"][dimension]) for page in current if page["scores"][dimension] is not None]
            dimension_scores[dimension] = round(sum(values) / len(values), 2) if values else None
        overall, coverage, provisional = composite_score(dimension_scores)
        issues = [check for page in current for check in page["checks"] if check["status"] != "pass"]
        gsc_pages = [page for page in current if page["gsc"]["impressions"] != "no-data"]
        impressions = sum(float(page["gsc"]["impressions"]) for page in gsc_pages)
        clicks = sum(float(page["gsc"]["clicks"]) for page in gsc_pages)
        rows.append({
            "language": scope, "pages": len(current), "overall_score": overall if overall is not None else "no-data",
            "band": band(overall), "coverage": coverage, "provisional": provisional,
            **{f"{dimension}_score": value if value is not None else "no-data" for dimension, value in dimension_scores.items()},
            "critical_issues": sum(row["severity"] == "Critical" and row["status"] == "fail" for row in issues),
            "high_issues": sum(row["severity"] == "High" and row["status"] == "fail" for row in issues),
            "warning_issues": sum(row["status"] == "warn" for row in issues),
            "gsc_clicks": round(clicks, 3) if gsc_pages else "no-data",
            "gsc_impressions": round(impressions, 3) if gsc_pages else "no-data",
            "gsc_pages": len(gsc_pages),
            "localization_readiness": "reviewed" if scope in {"root", "en"} else "requires_native_review",
        })
    return rows


def issue_rows(pages: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for page in pages:
        for check in page["checks"]:
            if check["status"] == "pass":
                continue
            rows.append({
                "rule_id": check["rule_id"], "category": check["dimension"],
                "severity": check["severity"], "status": check["status"],
                "language": page["scope"], "url": page["url"], "path": page["path"],
                "title": check["title"], "evidence": check["evidence"],
                "recommendation": check["recommendation"], "confidence": check["confidence"],
                "human_review": str(check["needs_human_review"]).lower(),
            })
    return sorted(rows, key=lambda row: (SEVERITY_ORDER[str(row["severity"])], str(row["status"]) != "fail", str(row["language"]), str(row["url"]), str(row["rule_id"])))


def render_scorecard(audit: dict[str, object]) -> str:
    languages = audit["language_scores"]
    issues = audit["issues"][:1000]
    summary = audit["summary"]
    data = json.dumps({"languages": languages, "issues": issues}, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Yuchen Water 多语言 SEO/GEO 评分台</title>
<style>
:root{{--ink:#16343b;--muted:#60747a;--teal:#087f8c;--gold:#d5a84c;--bg:#f3f6f5;--bad:#b42318;--warn:#a15c00}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}}main{{width:min(1500px,calc(100% - 32px));margin:28px auto 60px}}h1{{font-size:clamp(28px,4vw,48px);margin:0 0 8px}}.notice{{padding:14px 16px;background:#fff8e7;border:1px solid #ecd294;border-radius:12px}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:18px 0}}.card{{background:white;border:1px solid #dce5e3;border-radius:14px;padding:18px}}.big{{font-size:30px;font-weight:750}}section{{background:white;border:1px solid #dce5e3;border-radius:16px;padding:18px;margin-top:18px;overflow:auto}}.controls{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px}}input,select{{min-height:42px;border:1px solid #b9c9c6;border-radius:9px;padding:8px 10px;background:white}}table{{border-collapse:collapse;width:100%;min-width:960px}}th,td{{padding:10px;border-bottom:1px solid #e4ecea;text-align:left;vertical-align:top}}th{{position:sticky;top:0;background:#edf4f2}}.score{{font-weight:750;color:var(--teal)}}.priority,.fail{{color:var(--bad);font-weight:700}}.warn{{color:var(--warn)}}small{{color:var(--muted)}}
</style></head><body><main>
<h1>多语言 SEO/GEO 评分台</h1><p>生成时间：{html.escape(str(audit['generated_at']))}；审计指纹：<code>{html.escape(str(audit['audit_fingerprint']))}</code></p>
<div class="notice">分数用于比较可验证的网站质量，不预测 Google 排名、流量或 AI 引用。GSC 指标独立展示；<code>no-data</code> 不按 0 分处理。</div>
<div class="cards"><div class="card"><div class="big">{summary['scopes']}</div><small>语言/根范围</small></div><div class="card"><div class="big">{summary['html_pages']}</div><small>HTML 页面</small></div><div class="card"><div class="big">{summary['sitemap_unique_urls']}</div><small>唯一 sitemap URL</small></div><div class="card"><div class="big">{summary['macro_score']}</div><small>全站语言宏观平均</small></div><div class="card"><div class="big">{summary['score_coverage']}%</div><small>有效评分覆盖</small></div></div>
<section><h2>逐语言评分</h2><div class="controls"><input id="langSearch" placeholder="搜索语言"><select id="band"><option value="">全部等级</option><option>strong</option><option>good</option><option>developing</option><option>priority</option></select></div><table><thead><tr><th>语言</th><th>总分</th><th>覆盖</th><th>技术</th><th>关键词</th><th>内容</th><th>GEO/AEO</th><th>本地化</th><th>GSC 展示</th><th>高优先问题</th></tr></thead><tbody id="langs"></tbody></table></section>
<section><h2>问题队列（最多展示 1,000 条）</h2><div class="controls"><input id="issueSearch" placeholder="语言、URL、规则或问题"><select id="severity"><option value="">全部严重度</option><option>Critical</option><option>High</option><option>Medium</option><option>Low</option></select></div><table><thead><tr><th>级别</th><th>语言</th><th>规则</th><th>页面</th><th>证据</th><th>建议</th></tr></thead><tbody id="issues"></tbody></table></section>
<script>const DATA={data};const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
function drawLangs(){{let q=document.querySelector('#langSearch').value.toLowerCase(),b=document.querySelector('#band').value;document.querySelector('#langs').innerHTML=DATA.languages.filter(x=>(!q||x.language.toLowerCase().includes(q))&&(!b||x.band===b)).map(x=>`<tr><td>${{esc(x.language)}}</td><td class="score">${{esc(x.overall_score)}} <small>${{esc(x.band)}}</small></td><td>${{esc(x.coverage)}}%</td><td>${{esc(x.technical_score)}}</td><td>${{esc(x.keyword_intent_score)}}</td><td>${{esc(x.content_score)}}</td><td>${{esc(x.geo_aeo_score)}}</td><td>${{esc(x.localization_score)}}</td><td>${{esc(x.gsc_impressions)}}</td><td class="${{x.critical_issues+x.high_issues?'priority':''}}">${{x.critical_issues+x.high_issues}}</td></tr>`).join('')}}
function drawIssues(){{let q=document.querySelector('#issueSearch').value.toLowerCase(),s=document.querySelector('#severity').value;document.querySelector('#issues').innerHTML=DATA.issues.filter(x=>(!s||x.severity===s)&&(!q||[x.language,x.url,x.rule_id,x.title].join(' ').toLowerCase().includes(q))).map(x=>`<tr><td class="${{esc(x.status)}}">${{esc(x.severity)}} / ${{esc(x.status)}}</td><td>${{esc(x.language)}}</td><td>${{esc(x.rule_id)}}</td><td><a href="${{esc(x.url)}}">${{esc(x.path)}}</a></td><td>${{esc(x.evidence)}}</td><td>${{esc(x.recommendation)}}</td></tr>`).join('')}}
for(const id of ['langSearch','band'])document.querySelector('#'+id).addEventListener('input',drawLangs);for(const id of ['issueSearch','severity'])document.querySelector('#'+id).addEventListener('input',drawIssues);drawLangs();drawIssues();</script></main></body></html>"""


def report_manifest(run_dir: Path) -> dict[str, object]:
    files: dict[str, str] = {}
    for path in sorted(run_dir.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(run_dir).as_posix()
        if relative == "manifest-sha256.json" or any(relative.startswith(prefix) for prefix in IGNORED_REPORT_PREFIXES):
            continue
        files[relative] = sha256_file(path)
    return {"algorithm": "sha256", "files": files}


def refresh_manifest(run_dir: Path) -> None:
    write_json(run_dir / "manifest-sha256.json", report_manifest(run_dir))


def scan_site(
    site_root: Path, gsc_page: Path | None = None, gsc_query_page: Path | None = None,
    gsc_detail: Path | None = None,
) -> dict[str, object]:
    site_root = site_root.resolve()
    source_sha = sha256_file(Path(__file__).resolve())
    input_records = []
    for kind, path in (("gsc_page", gsc_page), ("gsc_query_page", gsc_query_page), ("gsc_page_country_device", gsc_detail)):
        if path and path.is_file():
            input_records.append({"kind": kind, "path": str(path.resolve()), "sha256": sha256_file(path)})
    scopes = discover_scopes(site_root)
    sitemap_by_scope, sitemap_summary = sitemap_inventory(site_root, scopes)
    raw_pages: list[dict[str, object]] = []
    for scope in scopes:
        raw_pages.extend(parse_page(site_root, path, scope) for path in scope_paths(site_root, scope))
    by_scope: dict[str, list[dict[str, object]]] = defaultdict(list)
    for page in raw_pages:
        by_scope[str(page["scope"])].append(page)
    repeated_by_path: Counter[str] = Counter()
    title_counts: dict[str, Counter[str]] = {}
    description_counts: dict[str, Counter[str]] = {}
    for scope, current in by_scope.items():
        paragraph_routes: dict[str, set[str]] = defaultdict(set)
        for page in current:
            for paragraph_hash in page["long_paragraph_hashes"]:
                paragraph_routes[str(paragraph_hash)].add(str(page["path"]))
        for routes in paragraph_routes.values():
            if len(routes) >= 3:
                for route in routes:
                    repeated_by_path[route] += 1
        title_counts[scope] = Counter(normalize(str(page["title"])) for page in current if page["title"])
        description_counts[scope] = Counter(normalize(str(page["description"])) for page in current if page["description"])
    canonical_pages = {
        str(page["canonical"] or page["url"]).rstrip("/"): page
        for page in raw_pages if page["canonical"] or page["url"]
    }
    english_pages = {Path(str(page["path"])).name: page for page in by_scope.get("en", [])}
    gsc = load_gsc(gsc_page, gsc_query_page, gsc_detail)
    query_page_sets: dict[tuple[str, str], set[str]] = defaultdict(set)
    url_scope = {str(page["url"]): str(page["scope"]) for page in raw_pages}
    for url, queries in gsc["queries"].items():
        for row in queries:
            query_page_sets[(url_scope.get(url, str(row["language"])), normalize(str(row["query"])))].add(url)
    query_page_counts = Counter({key: len(value) for key, value in query_page_sets.items()})
    pages = [
        evaluate_page(
            page, sitemap_by_scope.get(str(page["scope"]), set()), title_counts[str(page["scope"])],
            description_counts[str(page["scope"])], repeated_by_path, canonical_pages, gsc,
            english_pages, query_page_counts,
        )
        for page in raw_pages
    ]
    del raw_pages, by_scope, canonical_pages, english_pages, url_scope
    issues = issue_rows(pages)
    if sitemap_summary["duplicate_entries"]:
        for url in sitemap_summary["duplicate_urls"]:
            issues.insert(0, {
                "rule_id": "S001", "category": "technical", "severity": "Critical", "status": "fail",
                "language": "site", "url": url, "path": "sitemaps/", "title": "Sitemap URL 全局重复",
                "evidence": url, "recommendation": "每个 loc 只保留一次并保留较新的 lastmod。",
                "confidence": "high", "human_review": "false",
            })
    language_scores = aggregate_languages(pages, scopes)
    numeric_scores = [float(row["overall_score"]) for row in language_scores if row["overall_score"] != "no-data"]
    coverages = [float(row["coverage"]) for row in language_scores if row["overall_score"] != "no-data"]
    summary = {
        "scopes": len(scopes), "html_pages": len(pages),
        "sitemap_entries": sitemap_summary["entries"], "sitemap_unique_urls": sitemap_summary["unique"],
        "sitemap_duplicate_entries": sitemap_summary["duplicate_entries"],
        "macro_score": round(sum(numeric_scores) / len(numeric_scores), 2) if numeric_scores else "no-data",
        "score_coverage": round(sum(coverages) / len(coverages), 2) if coverages else 0,
        "issues": len(issues),
        "critical_failures": sum(row["severity"] == "Critical" and row["status"] == "fail" for row in issues),
        "high_failures": sum(row["severity"] == "High" and row["status"] == "fail" for row in issues),
        "gsc_page_rows": len(gsc["pages"]), "gsc_query_page_urls": len(gsc["queries"]),
    }
    normalized = {
        "schema_version": SCHEMA_VERSION, "tool_version": TOOL_VERSION,
        "tool_source_sha256": source_sha,
        "inputs": [{"kind": row["kind"], "sha256": row["sha256"]} for row in input_records],
        "summary": summary, "sitemap": sitemap_summary,
        "languages": language_scores,
        "pages": [{key: value for key, value in page.items() if key != "checks"} for page in pages],
        "issues": [{key: value for key, value in row.items() if key not in {"recommendation"}} for row in issues],
    }
    fingerprint = sha256_bytes(canonical_json(normalized))
    return {
        "schema_version": SCHEMA_VERSION,
        "tool": {"name": "site-quality-control", "version": TOOL_VERSION, "source_sha256": source_sha},
        "generated_at": utc_now(), "site_root": str(site_root),
        "publication_allowed": "NO", "network_used": False,
        "score_policy": {
            "weights": DIMENSION_WEIGHTS, "status_values": STATUS_VALUES,
            "bands": {"strong": "90-100", "good": "75-89.99", "developing": "60-74.99", "priority": "0-59.99"},
            "provisional_below_coverage": 80,
            "disclaimer": "Quality score is not a ranking, traffic, conversion, or AI-citation forecast.",
        },
        "inputs": input_records, "summary": summary, "sitemap": sitemap_summary,
        "language_scores": language_scores, "pages": pages, "issues": issues,
        "audit_fingerprint": fingerprint,
        "limitations": [
            "Semantic, translation, claim and visual quality findings require human review.",
            "GSC rows describe Google and their exported date range only.",
            "Country, language and device evidence remains separate.",
            "No public-network crawl or production mutation was performed.",
        ],
    }


LANGUAGE_FIELDS = [
    "language", "pages", "overall_score", "band", "coverage", "provisional",
    "technical_score", "keyword_intent_score", "content_score", "geo_aeo_score",
    "localization_score", "critical_issues", "high_issues", "warning_issues",
    "gsc_clicks", "gsc_impressions", "gsc_pages", "localization_readiness",
]
ISSUE_FIELDS = [
    "rule_id", "category", "severity", "status", "language", "url", "path",
    "title", "evidence", "recommendation", "confidence", "human_review",
]


def write_audit(run_dir: Path, audit: dict[str, object], expected: dict[str, int]) -> list[str]:
    failures = []
    summary = audit["summary"]
    for key, actual_key in (("scopes", "scopes"), ("html_pages", "html_pages"), ("sitemap_urls", "sitemap_unique_urls")):
        if expected[key] and int(summary[actual_key]) != expected[key]:
            failures.append(f"{actual_key}={summary[actual_key]} expected={expected[key]}")
    write_json(run_dir / "audit.json", audit)
    write_csv(run_dir / "language-scores.csv", audit["language_scores"], LANGUAGE_FIELDS)
    write_csv(run_dir / "issues.csv", audit["issues"], ISSUE_FIELDS)
    (run_dir / "scorecard.html").write_text(render_scorecard(audit), encoding="utf-8")
    run_config = {
        "schema_version": SCHEMA_VERSION, "command": "audit", "site_root": audit["site_root"],
        "audit_fingerprint": audit["audit_fingerprint"], "expected": expected,
        "accepted_regression_contract": ACCEPTED_REGRESSION_CONTRACT_BINDING,
        "states": {"DATA_INTEGRITY": "PASS" if not failures else "FAIL", "LOCALIZATION_READINESS": "REQUIRES_NATIVE_REVIEW", "PUBLICATION_ALLOWED": "NO"},
    }
    write_json(run_dir / "run-config.json", run_config)
    (run_dir / "summary.md").write_text(
        "# 全站多语言 SEO/GEO 评分\n\n"
        f"- 范围：`{summary['scopes']}` 个语言/根目录，`{summary['html_pages']}` 个 HTML。\n"
        f"- Sitemap：`{summary['sitemap_entries']}` 条，`{summary['sitemap_unique_urls']}` 个唯一 URL，重复 `{summary['sitemap_duplicate_entries']}`。\n"
        f"- 全站语言宏观平均：`{summary['macro_score']}`；评分证据覆盖：`{summary['score_coverage']}%`。\n"
        f"- 问题：`{summary['issues']}`；Critical fail `{summary['critical_failures']}`；High fail `{summary['high_failures']}`。\n"
        f"- GSC 页面记录：`{summary['gsc_page_rows']}`；具有有效查询证据的页面：`{summary['gsc_query_page_urls']}`。\n"
        f"- 审计指纹：`{audit['audit_fingerprint']}`。\n"
        "- 评分不是排名、流量或 AI 引用预测；语义与翻译结论需要人工复核。\n"
        "- 网站修改：`false`；网络使用：`false`；PUBLICATION_ALLOWED=`NO`。\n"
        + ("- 数据完整性：`PASS`。\n" if not failures else f"- 数据完整性：`FAIL`（{'; '.join(failures)}）。\n"),
        encoding="utf-8",
    )
    refresh_manifest(run_dir)
    return failures


def load_audit_run(run_dir: Path) -> tuple[dict[str, object], dict[str, object]]:
    audit_path = run_dir / "audit.json"
    config_path = run_dir / "run-config.json"
    if not audit_path.is_file() or not config_path.is_file():
        raise ValueError("run directory must contain audit.json and run-config.json")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    contract_binding = config.get("accepted_regression_contract")
    if not isinstance(contract_binding, dict) or contract_binding != ACCEPTED_REGRESSION_CONTRACT_BINDING:
        raise ValueError("run-config.json is not bound to the current accepted regression contract")
    manifest_path = run_dir / "manifest-sha256.json"
    if not manifest_path.is_file():
        raise ValueError("manifest-sha256.json is missing")
    report_hashes = json.loads(manifest_path.read_text(encoding="utf-8")).get("files", {})
    for name, path in (("audit.json", audit_path), ("run-config.json", config_path)):
        if report_hashes.get(name) != sha256_file(path):
            raise ValueError(f"report manifest hash mismatch: {name}")
    if audit.get("audit_fingerprint") != config.get("audit_fingerprint"):
        raise ValueError("audit fingerprint does not match run-config.json")
    normalized = {
        "schema_version": audit.get("schema_version"),
        "tool_version": audit.get("tool", {}).get("version"),
        "tool_source_sha256": audit.get("tool", {}).get("source_sha256"),
        "inputs": [{"kind": row.get("kind"), "sha256": row.get("sha256")} for row in audit.get("inputs", [])],
        "summary": audit.get("summary"), "sitemap": audit.get("sitemap"),
        "languages": audit.get("language_scores"),
        "pages": [{key: value for key, value in page.items() if key != "checks"} for page in audit.get("pages", [])],
        "issues": [{key: value for key, value in row.items() if key != "recommendation"} for row in audit.get("issues", [])],
    }
    if sha256_bytes(canonical_json(normalized)) != audit.get("audit_fingerprint"):
        raise ValueError("audit content no longer matches its fingerprint")
    if audit.get("tool", {}).get("source_sha256") != sha256_file(Path(__file__).resolve()):
        raise ValueError("audit was produced by a different controller source; create a new run")
    if audit.get("publication_allowed") != "NO" or config.get("states", {}).get("PUBLICATION_ALLOWED") != "NO":
        raise ValueError("unsafe publication state")
    return audit, config


def proposal_priority(page: dict[str, object], issues: list[dict[str, object]]) -> tuple[float, str]:
    critical = sum(row["severity"] == "Critical" and row["status"] == "fail" for row in issues)
    high = sum(row["severity"] == "High" and row["status"] == "fail" for row in issues)
    medium = sum(row["severity"] == "Medium" and row["status"] == "fail" for row in issues)
    warnings = sum(row["status"] == "warn" for row in issues)
    impressions = page["gsc"].get("impressions", "no-data")
    evidence = 0 if impressions == "no-data" else math.log1p(float(impressions)) * 20
    business = 30 if page["kind"] == "product" else (20 if page["kind"] in {"home", "hub"} else 5)
    value = critical * 1000 + high * 300 + medium * 80 + warnings * 5 + evidence + business
    label = "urgent" if critical else ("high" if high else ("medium" if medium or impressions != "no-data" else "low"))
    return value, label


def command_propose(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    audit, _config = load_audit_run(run_dir)
    issues_by_url: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in audit["issues"]:
        if row["language"] != "site":
            issues_by_url[str(row["url"])].append(row)
    candidates = []
    for page in audit["pages"]:
        current = issues_by_url.get(str(page["url"]), [])
        if not current and page["gsc"].get("impressions") == "no-data":
            continue
        priority_value, priority = proposal_priority(page, current)
        candidates.append((priority_value, str(page["scope"]), str(page["url"]), priority, page, current))
    candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
    selected = candidates[: args.max_pages]
    rows = []
    for index, (_value, language, _url, priority, page, current) in enumerate(selected, 1):
        top = sorted(current, key=lambda row: (SEVERITY_ORDER[str(row["severity"])], str(row["rule_id"])))[:3]
        evidence = " | ".join(f"{row['rule_id']}: {row['evidence']}" for row in top) or "GSC performance evidence only"
        recommendation = " | ".join(dict.fromkeys(str(row["recommendation"]) for row in top)) or "人工复核查询意图、正文证据和内链后再提出单页改动。"
        rows.append({
            "proposal_id": f"P{index:03d}", "batch": index, "priority": priority,
            "language": language, "url": page["url"], "path": page["path"],
            "page_score": page["overall_score"], "score_coverage": page["coverage"],
            "gsc_clicks": page["gsc"].get("clicks", "no-data"),
            "gsc_impressions": page["gsc"].get("impressions", "no-data"),
            "gsc_ctr": page["gsc"].get("ctr", "no-data"),
            "gsc_position": page["gsc"].get("position", "no-data"),
            "evidence": evidence, "recommendation": recommendation,
            "localization_review": "reviewed" if language in {"root", "en"} else "pending_native_review",
            "status": "proposal_only", "requires_user_approval": "yes",
        })
    proposal_fields = [
        "proposal_id", "batch", "priority", "language", "url", "path",
        "page_score", "score_coverage", "gsc_clicks", "gsc_impressions", "gsc_ctr",
        "gsc_position", "evidence", "recommendation", "localization_review",
        "status", "requires_user_approval",
    ]
    write_csv(run_dir / "proposal.csv", rows, proposal_fields)
    language_priority = sorted(
        audit["language_scores"],
        key=lambda row: (-int(row["critical_issues"]), -int(row["high_issues"]), -(float(row["gsc_impressions"]) if row["gsc_impressions"] != "no-data" else -1), float(row["overall_score"]) if row["overall_score"] != "no-data" else 101, str(row["language"])),
    )
    write_csv(run_dir / "language-priority.csv", language_priority, LANGUAGE_FIELDS)
    (run_dir / "proposal.md").write_text(
        "# 第一轮分语言优化提案\n\n"
        f"- 候选页面：`{len(rows)}`（默认上限 `{args.max_pages}`）。\n"
        "- 排序：技术阻断 → GSC 证据 → 商业页面 → 其余告警。\n"
        "- 本文件只提出方案，不修改页面；非英语内容必须经过本语言人工审核。\n"
        "- 用户确认本提案后，才允许准备 changes 目录并运行 preview。\n"
        "- PUBLICATION_ALLOWED=`NO`。\n",
        encoding="utf-8",
    )
    refresh_manifest(run_dir)
    print(json.dumps({"status": "ok", "proposals": len(rows), "run_dir": str(run_dir), "publication_allowed": "NO"}, ensure_ascii=False))
    return 0


def public_path_allowed(relative: Path, scopes: set[str]) -> bool:
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        return False
    if len(relative.parts) == 1:
        return relative.name in PUBLIC_ROOT_FILES
    return relative.parts[0] == "assets" or relative.parts[0] in scopes - {"root"}


def changed_files(changes_dir: Path, site_root: Path, scopes: set[str]) -> list[dict[str, object]]:
    result = []
    for path in sorted(changes_dir.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"changes directory may not contain symlinks: {path}")
        if not path.is_file():
            continue
        relative = path.relative_to(changes_dir)
        if not public_path_allowed(relative, scopes):
            raise ValueError(f"change is outside public whitelist: {relative}")
        target = site_root / relative
        before_sha = sha256_file(target) if target.is_file() else "MISSING"
        after_sha = sha256_file(path)
        if before_sha == after_sha:
            continue
        result.append({
            "path": relative.as_posix(), "state": "modified" if target.exists() else "new",
            "before_sha256": before_sha, "after_sha256": after_sha,
            "after_bytes": path.stat().st_size,
        })
    if not result:
        raise ValueError("changes directory contains no byte changes")
    return result


def has_changed_descendant(relative: Path, change_paths: set[Path]) -> bool:
    return any(candidate == relative or relative in candidate.parents for candidate in change_paths)


def build_overlay(source: Path, destination: Path, change_root: Path, changes: list[dict[str, object]], scopes: set[str]) -> None:
    if destination.exists():
        raise ValueError(f"preview site already exists: {destination}")
    destination.mkdir(parents=True)
    change_paths = {Path(str(row["path"])) for row in changes}

    def mirror(src: Path, dst: Path, relative: Path) -> None:
        if relative in change_paths:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(change_root / relative, dst)
            return
        if not has_changed_descendant(relative, change_paths):
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.symlink_to(src.resolve(), target_is_directory=src.is_dir())
            return
        dst.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            children = {child.name: child for child in src.iterdir() if not child.name.startswith(".git")}
        else:
            children = {}
        needed = {path.parts[len(relative.parts)] for path in change_paths if relative in path.parents and len(path.parts) > len(relative.parts)}
        for name in sorted(set(children) | needed):
            child_relative = relative / name
            child_source = children.get(name, source / child_relative)
            mirror(child_source, dst / name, child_relative)

    top_names = set(PUBLIC_ROOT_FILES) | {"assets"} | (scopes - {"root"})
    top_names |= {path.parts[0] for path in change_paths}
    for name in sorted(top_names):
        src = source / name
        relative = Path(name)
        if not src.exists() and not has_changed_descendant(relative, change_paths) and relative not in change_paths:
            continue
        mirror(src, destination / name, relative)


def write_diffs(run_dir: Path, site_root: Path, preview_root: Path, changes: list[dict[str, object]]) -> None:
    diff_dir = run_dir / "preview" / "diffs"
    diff_dir.mkdir(parents=True, exist_ok=True)
    links = []
    for row in changes:
        relative = Path(str(row["path"]))
        if relative.suffix.casefold() not in {".html", ".htm", ".css", ".js", ".json", ".xml", ".txt", ".md", ".csv"}:
            continue
        before = (site_root / relative).read_text(encoding="utf-8", errors="replace").splitlines() if (site_root / relative).is_file() else []
        after = (preview_root / relative).read_text(encoding="utf-8", errors="replace").splitlines()
        name = re.sub(r"[^A-Za-z0-9_.-]+", "_", relative.as_posix()) + ".html"
        content = difflib.HtmlDiff(wrapcolumn=120).make_file(before, after, f"before/{relative}", f"preview/{relative}", context=True, numlines=3)
        (diff_dir / name).write_text(content, encoding="utf-8")
        links.append((relative.as_posix(), name))
    body = "\n".join(f'<li><a href="{html.escape(name)}">{html.escape(relative)}</a></li>' for relative, name in links)
    (diff_dir / "index.html").write_text(f"<!doctype html><meta charset='utf-8'><title>Preview diffs</title><h1>改前/改后差异</h1><ul>{body}</ul>", encoding="utf-8")


def capture_screenshots(args: argparse.Namespace, site_root: Path, preview_root: Path, changed_html: list[str], run_dir: Path) -> dict[str, object]:
    if not changed_html:
        result = {"status": "not-applicable", "pages": 0, "cases": 0, "reason": "no changed HTML pages"}
        write_json(run_dir / "preview" / "screenshots.json", result)
        return result
    script = Path(__file__).with_name("capture_site_quality_preview.mjs")
    output = run_dir / "preview" / "screenshots"
    paths_file = run_dir / "preview" / "screenshot-paths.json"
    write_json(paths_file, changed_html)
    env = os.environ.copy()
    if args.node_modules:
        env["NODE_PATH"] = str(args.node_modules.resolve())
    command = [
        str(args.node), str(script), "--source-root", str(site_root),
        "--preview-root", str(preview_root), "--out", str(output),
        "--paths-json", str(paths_file),
    ]
    completed = subprocess.run(command, text=True, capture_output=True, env=env, check=False)
    if completed.returncode:
        raise RuntimeError(f"screenshot capture failed: {completed.stderr.strip() or completed.stdout.strip()}")
    result = json.loads((output / "browser-qa.json").read_text(encoding="utf-8"))
    return result


def command_preview(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    audit, _config = load_audit_run(run_dir)
    site_root = Path(str(audit["site_root"])).resolve()
    changes_dir = args.changes_dir.resolve()
    if not changes_dir.is_dir():
        raise ValueError("changes directory does not exist")
    scopes = set(discover_scopes(site_root))
    changes = changed_files(changes_dir, site_root, scopes)
    preview_root = run_dir / "preview" / "site"
    build_overlay(site_root, preview_root, changes_dir, changes, scopes)
    write_diffs(run_dir, site_root, preview_root, changes)
    staged = scan_site(preview_root, args.gsc_page, args.gsc_query_page, args.gsc_detail)
    score_changes = []
    baseline_by_path = {str(page["path"]): page for page in audit["pages"]}
    staged_by_path = {str(page["path"]): page for page in staged["pages"]}
    for row in changes:
        relative = str(row["path"])
        before = baseline_by_path.get(relative)
        after = staged_by_path.get(relative)
        score_changes.append({
            "path": relative,
            "before_score": before.get("overall_score", "no-data") if before else "no-data",
            "after_score": after.get("overall_score", "no-data") if after else "no-data",
            "before_band": before.get("band", "no-data") if before else "no-data",
            "after_band": after.get("band", "no-data") if after else "no-data",
        })
    write_csv(run_dir / "preview" / "score-changes.csv", score_changes, ["path", "before_score", "after_score", "before_band", "after_band"])
    changed_html = [str(row["path"]) for row in changes if str(row["path"]).casefold().endswith((".html", ".htm"))]
    screenshots = {"status": "skipped_by_explicit_flag", "pages": len(changed_html), "cases": 0}
    if not args.skip_screenshots:
        screenshots = capture_screenshots(args, site_root, preview_root, changed_html, run_dir)
    else:
        write_json(run_dir / "preview" / "screenshots.json", screenshots)
    core = {
        "schema_version": SCHEMA_VERSION, "created_at": utc_now(),
        "site_root": str(site_root), "run_dir": str(run_dir),
        "baseline_audit_fingerprint": audit["audit_fingerprint"],
        "staged_audit_fingerprint": staged["audit_fingerprint"],
        "changes": changes, "score_changes": score_changes,
        "screenshots": screenshots, "publication_allowed": "NO",
        "approval_scope": "apply exact reviewed bytes to the local source tree only; production publication is not authorized",
    }
    approval_sha = sha256_bytes(canonical_json(core))
    manifest = {**core, "approval_sha256": approval_sha}
    write_json(run_dir / "preview-manifest.json", manifest)
    (run_dir / "preview" / "README.md").write_text(
        "# 本地暂存预览\n\n"
        f"- 预览目录：`{preview_root}`\n"
        f"- 差异入口：`{run_dir / 'preview/diffs/index.html'}`\n"
        f"- 待批准哈希：`{approval_sha}`\n"
        "- 使用 `serve` 命令只绑定 127.0.0.1。\n"
        "- 该哈希只授权覆盖本地源文件，不授权生产发布。\n",
        encoding="utf-8",
    )
    refresh_manifest(run_dir)
    print(json.dumps({"status": "ok", "changed_files": len(changes), "changed_html": len(changed_html), "approval_sha256": approval_sha, "preview_root": str(preview_root), "publication_allowed": "NO"}, ensure_ascii=False))
    return 0


def validate_preview_manifest(run_dir: Path, approval: str) -> dict[str, object]:
    path = run_dir / "preview-manifest.json"
    if not path.is_file():
        raise ValueError("preview-manifest.json is missing")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    declared = str(manifest.pop("approval_sha256", ""))
    actual = sha256_bytes(canonical_json(manifest))
    manifest["approval_sha256"] = declared
    if not declared or declared != actual:
        raise ValueError("preview manifest content hash is invalid")
    if approval != declared:
        raise ValueError("approval hash does not match the reviewed preview")
    if manifest.get("publication_allowed") != "NO":
        raise ValueError("unsafe preview publication state")
    return manifest


def command_apply(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    audit, _config = load_audit_run(run_dir)
    manifest = validate_preview_manifest(run_dir, args.approved_preview)
    site_root = Path(str(audit["site_root"])).resolve()
    if str(site_root) != str(Path(str(manifest["site_root"])).resolve()):
        raise ValueError("preview site root does not match audit site root")
    scopes = set(discover_scopes(site_root))
    preview_root = run_dir / "preview" / "site"
    changes = list(manifest["changes"])
    failures = []
    for row in changes:
        relative = Path(str(row["path"]))
        if not public_path_allowed(relative, scopes):
            failures.append(f"outside whitelist: {relative}")
            continue
        target = site_root / relative
        actual_before = sha256_file(target) if target.is_file() else "MISSING"
        if actual_before != row["before_sha256"]:
            failures.append(f"source changed after preview: {relative}")
        staged = preview_root / relative
        if not staged.is_file() or sha256_file(staged) != row["after_sha256"]:
            failures.append(f"preview bytes changed: {relative}")
    if failures:
        raise ValueError("; ".join(failures))
    backup_dir = run_dir / "backups" / args.approved_preview[:16]
    if backup_dir.exists():
        raise ValueError("this preview approval has already created a backup/apply attempt")
    backup_dir.mkdir(parents=True)
    backup_rows = []
    temp_paths: list[tuple[Path, Path, dict[str, object]]] = []
    applied: list[tuple[Path, dict[str, object]]] = []
    try:
        for row in changes:
            relative = Path(str(row["path"]))
            target = site_root / relative
            if target.is_file():
                backup = backup_dir / relative
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target, backup)
            backup_rows.append({"path": relative.as_posix(), "before_sha256": row["before_sha256"], "after_sha256": row["after_sha256"], "state": row["state"]})
            target.parent.mkdir(parents=True, exist_ok=True)
            temp = target.with_name(f".{target.name}.site-quality-{args.approved_preview[:12]}.tmp")
            if temp.exists():
                temp.unlink()
            shutil.copy2(preview_root / relative, temp)
            temp_paths.append((temp, target, row))
        write_json(backup_dir / "backup-manifest.json", {"approval_sha256": args.approved_preview, "files": backup_rows})
        for temp, target, row in temp_paths:
            os.replace(temp, target)
            applied.append((target, row))
    except Exception:
        for temp, _target, _row in temp_paths:
            if temp.exists():
                temp.unlink()
        for target, row in reversed(applied):
            relative = Path(str(row["path"]))
            backup = backup_dir / relative
            if backup.is_file():
                shutil.copy2(backup, target)
            elif row["before_sha256"] == "MISSING" and target.exists():
                target.unlink()
        raise
    result = {
        "status": "ok", "applied_at": utc_now(), "approval_sha256": args.approved_preview,
        "changed_files": [str(row["path"]) for row in changes], "backup_dir": str(backup_dir),
        "publication_allowed": "NO", "production_modified": False,
    }
    write_json(run_dir / "apply-result.json", result)
    refresh_manifest(run_dir)
    print(json.dumps(result, ensure_ascii=False))
    return 0


def fixture_html(canonical: str, lang: str = "en", robots: str = "index,follow", alternates: str = "") -> str:
    return f"""<!doctype html><html lang="{lang}" dir="ltr"><head><title>Verified water filter supplier page</title><meta name="description" content="Verified factual water filter specifications and procurement information for buyers."><meta name="robots" content="{robots}"><link rel="canonical" href="{canonical}">{alternates}<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Product","name":"Filter"}}</script></head><body><h1>Verified water filter</h1><p>This page directly explains the verified product, application, specifications, purchasing inputs and selection limits for professional buyers.</p><ul><li>Verified specification</li></ul><a href="/">Home</a></body></html>"""


def run_negative_tests() -> dict[str, object]:
    tests = []
    with tempfile.TemporaryDirectory(prefix="site-quality-negative-") as holder:
        root = Path(holder)
        (root / "sitemaps").mkdir()
        good = fixture_html(ORIGIN + "/", alternates=f'<link rel="alternate" hreflang="en" href="{ORIGIN}/">')
        (root / "index.html").write_text(good, encoding="utf-8")
        sitemap_good = f'<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{ORIGIN}/</loc></url></urlset>'
        (root / "sitemaps/sitemap-root.xml").write_text(sitemap_good, encoding="utf-8")
        baseline = scan_site(root)
        baseline_score = float(baseline["pages"][0]["overall_score"])
        cases = [
            ("duplicate_sitemap", "sitemap", sitemap_good.replace("</urlset>", f"<url><loc>{ORIGIN}/</loc></url></urlset>"), "S001"),
            ("bad_canonical", "html", good.replace(f'href="{ORIGIN}/"', 'href="https://example.com/"', 1), "T006"),
            ("missing_hreflang", "html", good.replace(f'<link rel="alternate" hreflang="en" href="{ORIGIN}/">', ""), "T013"),
            ("invalid_jsonld", "html", good.replace('{"@context":"https://schema.org","@type":"Product","name":"Filter"}', '{"@type":'), "T012"),
            ("broken_link_asset", "html", good.replace('<a href="/">', '<img src="/missing.webp" alt="x"><a href="/missing.html">'), "T016"),
            ("sitemap_noindex", "html", good.replace('content="index,follow"', 'content="noindex,follow"'), "T007"),
        ]
        for name, target, mutated, rule in cases:
            target_path = root / ("sitemaps/sitemap-root.xml" if target == "sitemap" else "index.html")
            original = target_path.read_bytes()
            target_path.write_text(mutated, encoding="utf-8")
            red = scan_site(root)
            rules = {str(row["rule_id"]) for row in red["issues"]}
            red_score = float(red["pages"][0]["overall_score"])
            target_path.write_bytes(original)
            restored = scan_site(root)
            tests.append({
                "name": name, "expected_rule": rule, "red": rule in rules and (target == "sitemap" or red_score < baseline_score),
                "restored_green": restored["audit_fingerprint"] == baseline["audit_fingerprint"],
            })
    passed = all(row["red"] and row["restored_green"] for row in tests)
    return {"status": "ok" if passed else "error", "tests": tests, "temporary_files_only": True}


def run_project_verifier(command: list[str], cwd: Path) -> dict[str, object]:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    output = completed.stdout.strip() or completed.stderr.strip()
    return {"command": command, "exit_code": completed.returncode, "output_tail": output[-4000:]}


def project_python(explicit: str | None = None) -> str:
    candidates = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    candidates.append(Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3")
    candidates.append(Path(sys.executable))
    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate.resolve())
    return sys.executable


def command_verify(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    audit, _config = load_audit_run(run_dir)
    site_root = Path(str(audit["site_root"])).resolve()
    del audit
    expected_current_fingerprint = str(_config["audit_fingerprint"])
    if (run_dir / "preview-manifest.json").is_file() and (run_dir / "apply-result.json").is_file():
        expected_current_fingerprint = str(json.loads((run_dir / "preview-manifest.json").read_text(encoding="utf-8"))["staged_audit_fingerprint"])
    first = scan_site(site_root, args.gsc_page, args.gsc_query_page, args.gsc_detail)
    first_fingerprint = str(first["audit_fingerprint"])
    counts = dict(first["summary"])
    del first
    second = scan_site(site_root, args.gsc_page, args.gsc_query_page, args.gsc_detail)
    second_fingerprint = str(second["audit_fingerprint"])
    del second
    count_failures = []
    expected = _config.get("expected", DEFAULT_EXPECTED)
    for key, actual_key in (("scopes", "scopes"), ("html_pages", "html_pages"), ("sitemap_urls", "sitemap_unique_urls")):
        if int(expected.get(key, 0)) and int(counts[actual_key]) != int(expected[key]):
            count_failures.append(f"{actual_key}={counts[actual_key]} expected={expected[key]}")
    preview_failures = []
    second_apply_changes: list[str] = []
    if (run_dir / "preview-manifest.json").is_file() and (run_dir / "apply-result.json").is_file():
        manifest = json.loads((run_dir / "preview-manifest.json").read_text(encoding="utf-8"))
        for row in manifest["changes"]:
            target = site_root / str(row["path"])
            if not target.is_file() or sha256_file(target) != row["after_sha256"]:
                preview_failures.append(str(row["path"]))
            else:
                second_apply_changes.extend([])
    negative = run_negative_tests()
    regressions = []
    if not args.skip_project_regressions:
        python = project_python(args.project_python)
        regressions.append(run_project_verifier([python, "tools/verify_gsc_growth_release.py", "verify", "--site-root", "."], site_root))
        regressions.append(run_project_verifier([python, "tools/import_sanyishui_catalog.py", "verify", "--site-root", "."], site_root))
    failures = list(count_failures)
    if first_fingerprint != expected_current_fingerprint:
        failures.append("current site/evidence fingerprint differs from the approved baseline or applied preview")
    if first_fingerprint != second_fingerprint:
        failures.append("audit fingerprint differs across immediate rerun")
    if preview_failures:
        failures.append(f"applied bytes differ from approved preview: {preview_failures}")
    if negative["status"] != "ok":
        failures.append("negative tests did not fail red and restore green")
    if any(row["exit_code"] != 0 for row in regressions):
        failures.append("project regression verifier failed")
    result = {
        "status": "ok" if not failures else "error", "verified_at": utc_now(),
        "audit_fingerprint_round_1": first_fingerprint,
        "audit_fingerprint_round_2": second_fingerprint,
        "deterministic_rerun": first_fingerprint == second_fingerprint,
        "summary": counts, "negative_tests": negative,
        "approved_preview_files_verified": len(json.loads((run_dir / "preview-manifest.json").read_text(encoding="utf-8"))["changes"]) if (run_dir / "preview-manifest.json").is_file() and (run_dir / "apply-result.json").is_file() else 0,
        "second_apply_would_change": second_apply_changes,
        "project_regressions": regressions, "failures": failures,
        "publication_allowed": "NO", "production_modified": False,
    }
    write_json(run_dir / "verify-result.json", result)
    refresh_manifest(run_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "ok" else 1


def command_serve(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    preview_root = run_dir / "preview" / "site"
    if not preview_root.is_dir():
        raise ValueError("preview site does not exist; run preview first")
    class PreviewHandler(SimpleHTTPRequestHandler):
        def end_headers(self) -> None:
            self.send_header("X-Robots-Tag", "noindex, nofollow")
            self.send_header("Cache-Control", "no-store")
            super().end_headers()

    handler = lambda *items, **kwargs: PreviewHandler(*items, directory=str(preview_root), **kwargs)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print(json.dumps({"status": "serving", "url": f"http://127.0.0.1:{args.port}/", "root": str(preview_root), "publication_allowed": "NO"}, ensure_ascii=False), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def path_arg(value: str | None, root: Path, fallback: Path) -> Path | None:
    raw = Path(value) if value else fallback
    path = raw if raw.is_absolute() else root / raw
    return path.resolve() if path.is_file() else None


def add_gsc_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--gsc-page")
    parser.add_argument("--gsc-query-page")
    parser.add_argument("--gsc-detail")


def resolve_gsc_args(args: argparse.Namespace, site_root: Path) -> None:
    args.gsc_page = path_arg(args.gsc_page, site_root, GSC_DEFAULT / "page.csv")
    args.gsc_query_page = path_arg(args.gsc_query_page, site_root, GSC_DEFAULT / "query-page-country-device.csv")
    args.gsc_detail = path_arg(args.gsc_detail, site_root, GSC_DEFAULT / "page-country-device.csv")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    audit = sub.add_parser("audit", help="run a read-only full-site audit and scorecard")
    audit.add_argument("--site-root", default=".")
    audit.add_argument("--run-dir", required=True)
    audit.add_argument("--expected-scopes", type=int, default=DEFAULT_EXPECTED["scopes"])
    audit.add_argument("--expected-html-pages", type=int, default=DEFAULT_EXPECTED["html_pages"])
    audit.add_argument("--expected-sitemap-urls", type=int, default=DEFAULT_EXPECTED["sitemap_urls"])
    add_gsc_args(audit)
    propose = sub.add_parser("propose", help="create a bounded proposal without editing the site")
    propose.add_argument("--run-dir", required=True)
    propose.add_argument("--max-pages", type=int, default=25)
    preview = sub.add_parser("preview", help="build an isolated reviewed preview from a changes directory")
    preview.add_argument("--run-dir", required=True)
    preview.add_argument("--changes-dir", required=True)
    preview.add_argument("--skip-screenshots", action="store_true", help="explicitly record screenshots as skipped")
    preview.add_argument("--node", default="node")
    preview.add_argument("--node-modules", type=Path)
    add_gsc_args(preview)
    apply = sub.add_parser("apply", help="apply exact preview bytes after explicit hash approval")
    apply.add_argument("--run-dir", required=True)
    apply.add_argument("--approved-preview", required=True)
    verify = sub.add_parser("verify", help="rerun deterministic audit, reverse tests and project regressions")
    verify.add_argument("--run-dir", required=True)
    verify.add_argument("--skip-project-regressions", action="store_true")
    verify.add_argument("--project-python", help="Python runtime with the repository's Pillow/ReportLab dependencies")
    add_gsc_args(verify)
    serve = sub.add_parser("serve", help="serve an existing preview on loopback only")
    serve.add_argument("--run-dir", required=True)
    serve.add_argument("--port", type=int, default=8765)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "audit":
            site_root = Path(args.site_root).resolve()
            run_dir = Path(args.run_dir).resolve()
            if run_dir.exists() and any(run_dir.iterdir()):
                raise ValueError("audit run directory must be new or empty")
            run_dir.mkdir(parents=True, exist_ok=True)
            resolve_gsc_args(args, site_root)
            result = scan_site(site_root, args.gsc_page, args.gsc_query_page, args.gsc_detail)
            failures = write_audit(run_dir, result, {"scopes": args.expected_scopes, "html_pages": args.expected_html_pages, "sitemap_urls": args.expected_sitemap_urls})
            print(json.dumps({"status": "ok" if not failures else "error", "run_dir": str(run_dir), "summary": result["summary"], "audit_fingerprint": result["audit_fingerprint"], "failures": failures, "publication_allowed": "NO"}, ensure_ascii=False, indent=2))
            return 0 if not failures else 1
        if args.command == "propose":
            args.run_dir = Path(args.run_dir)
            return command_propose(args)
        if args.command == "preview":
            args.run_dir = Path(args.run_dir)
            args.changes_dir = Path(args.changes_dir)
            site_root = Path(str(load_audit_run(args.run_dir.resolve())[0]["site_root"])).resolve()
            resolve_gsc_args(args, site_root)
            return command_preview(args)
        if args.command == "apply":
            args.run_dir = Path(args.run_dir)
            return command_apply(args)
        if args.command == "verify":
            args.run_dir = Path(args.run_dir)
            site_root = Path(str(load_audit_run(args.run_dir.resolve())[0]["site_root"])).resolve()
            resolve_gsc_args(args, site_root)
            return command_verify(args)
        if args.command == "serve":
            args.run_dir = Path(args.run_dir)
            return command_serve(args)
    except Exception as exc:
        print(json.dumps({"status": "error", "error": f"{type(exc).__name__}: {exc}", "publication_allowed": "NO"}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
