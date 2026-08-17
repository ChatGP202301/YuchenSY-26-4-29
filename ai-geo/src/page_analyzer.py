from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = []
        self.description = ""
        self.robots = ""
        self.canonical = ""
        self.alternates = []
        self.headings = {"h1":[], "h2":[], "h3":[]}
        self.links = []
        self.images = []
        self.jsonld = []
        self.text = []
        self._capture = None
        self._buffer = []
        self._hidden_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = {str(k).lower(): str(v or "") for k, v in attrs}
        tag = tag.lower()
        if tag in {"script", "style", "nav", "footer"}:
            self._hidden_depth += 1
        if tag == "title" or tag in self.headings or (tag == "script" and attrs.get("type", "").lower() == "application/ld+json"):
            self._capture = "jsonld" if tag == "script" else tag
            self._buffer = []
        if tag == "meta":
            name = attrs.get("name", "").lower()
            if name == "description": self.description = attrs.get("content", "")
            if name == "robots": self.robots = attrs.get("content", "")
        if tag == "link":
            rel = attrs.get("rel", "").lower().split()
            if "canonical" in rel: self.canonical = attrs.get("href", "")
            if "alternate" in rel and attrs.get("hreflang"): self.alternates.append((attrs["hreflang"], attrs.get("href", "")))
        if tag == "a" and attrs.get("href"): self.links.append(attrs["href"])
        if tag == "img": self.images.append({"src":attrs.get("src", ""), "alt":attrs.get("alt", "")})

    def handle_endtag(self, tag):
        tag = tag.lower()
        if self._capture in {tag, "jsonld" if tag == "script" else ""}:
            value = " ".join("".join(self._buffer).split())
            if self._capture == "title": self.title.append(value)
            elif self._capture in self.headings: self.headings[self._capture].append(value)
            elif self._capture == "jsonld" and value: self.jsonld.append(value)
            self._capture = None
            self._buffer = []
        if tag in {"script", "style", "nav", "footer"} and self._hidden_depth:
            self._hidden_depth -= 1

    def handle_data(self, data):
        if self._capture:
            self._buffer.append(data)
        if not self._hidden_depth and data.strip():
            self.text.append(data)


def schema_types(value) -> set[str]:
    result = set()
    if isinstance(value, dict):
        current = value.get("@type")
        if isinstance(current, str): result.add(current)
        elif isinstance(current, list): result.update(str(item) for item in current)
        for child in value.values(): result.update(schema_types(child))
    elif isinstance(value, list):
        for child in value: result.update(schema_types(child))
    return result


CHECKS = {
    "what_product":[r"reverse osmosis|water filter|water purifier|осмос|ósmosis|osmose"],
    "who_for":[r"buyer|distributor|industrial|commercial|покупател|дистрибьютор|industrial|industriel"],
    "problem":[r"problem|remove|treat|quality|проблем|очист|problema|problème"],
    "capacity":[r"capacity|lph|l/h|л/ч|gpd"], "feed_water":[r"feed water|исходн|agua de alimentación|eau d.alimentation"],
    "tds":[r"\btds\b|salinity|солесодерж|salinidad|salinité"], "flow_rate":[r"flow rate|производительност|caudal|débit"],
    "recovery":[r"recovery|выход пермеата|recuperación|récupération"], "membrane":[r"membrane|мембран"],
    "pretreatment":[r"pretreatment|предочист|pretratamiento|prétraitement"], "power":[r"\bkw\b|power|мощност|potencia|puissance"],
    "applications":[r"application|use case|применени|aplicacion|utilisation"], "certifications":[r"certif|сертифик"],
    "faq":[r"faq|frequently asked|часто задаваем|preguntas frecuentes|questions fréquentes"],
    "manufacturer":[r"manufacturer|factory|производител|fabricante|fabricant"], "selection":[r"select|sizing|выб|selecci|choisir"],
}


def page_type(path_or_url: str) -> str:
    value = path_or_url.lower()
    if value.endswith("/index.html") or value.endswith(".com/") or value == "index.html": return "homepage"
    if "products" in value or "catalog" in value: return "category"
    if "about" in value: return "brand"
    if "contact" in value: return "lead"
    return "product"


def analyze_html(html: str, path_or_url: str = "") -> dict:
    parser = PageParser()
    parser.feed(html)
    visible = " ".join(" ".join(parser.text).split())
    lowered = visible.casefold()
    schemas = set()
    errors = []
    for block in parser.jsonld:
        try: schemas.update(schema_types(json.loads(block)))
        except json.JSONDecodeError as exc: errors.append(str(exc))
    kind = page_type(path_or_url)
    applicable = list(CHECKS)
    if kind in {"homepage", "category", "brand", "lead"}:
        applicable = ["what_product", "who_for", "problem", "applications", "faq", "manufacturer", "selection"]
    satisfied = {name:any(re.search(pattern, lowered, re.I) for pattern in patterns) for name, patterns in CHECKS.items() if name in applicable}
    score = round(100 * sum(satisfied.values()) / len(applicable), 2) if applicable else None
    return {
        "page_type":kind, "title":" ".join(parser.title), "meta_description":parser.description, "h1":parser.headings["h1"], "h2":parser.headings["h2"], "h3":parser.headings["h3"],
        "canonical":parser.canonical, "hreflang":sorted(parser.alternates), "robots":parser.robots, "schema_types":sorted(schemas), "schema_errors":errors,
        "links":parser.links, "image_count":len(parser.images), "images_without_alt":sum(not item["alt"].strip() for item in parser.images),
        "word_count":len(re.findall(r"\w+", visible, re.UNICODE)), "visible_text":visible, "opening_text":visible[:600],
        "answer_extractability_score":score, "answer_extractability_coverage":round(100 * len(applicable) / len(CHECKS), 2), "answer_extractability_checks":satisfied,
    }


def analyze_file(path: Path, site_root: Path | None = None) -> dict:
    root = site_root or path.parent
    relative = path.resolve().relative_to(root.resolve()).as_posix() if path.resolve().is_relative_to(root.resolve()) else path.name
    result = analyze_html(path.read_text(encoding="utf-8", errors="replace"), relative)
    result["path"] = relative
    return result


def seo_snapshot(page: dict, site_counts: dict | None = None) -> dict:
    return {
        "canonical":page.get("canonical"), "hreflang":page.get("hreflang", []), "robots":page.get("robots"), "schema_errors":page.get("schema_errors", []),
        "h1_count":len(page.get("h1", [])), "title":page.get("title"), "site_counts":site_counts or {},
    }
