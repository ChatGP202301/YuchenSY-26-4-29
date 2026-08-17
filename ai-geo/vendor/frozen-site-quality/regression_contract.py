#!/usr/bin/env python3
"""Shared, fail-closed helpers for the accepted local regression contract."""

from __future__ import annotations

import copy
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable


CONTRACT_RELATIVE_PATH = Path("migration/site-quality-control/accepted-regression-contract.json")


def canonical_string_list_sha256(values: Iterable[str]) -> str:
    payload = json.dumps(
        sorted(str(value) for value in values),
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_regression_contract(site_root: Path) -> tuple[dict[str, object], dict[str, str]]:
    path = site_root.resolve() / CONTRACT_RELATIVE_PATH
    if not path.is_file():
        raise ValueError(f"accepted regression contract is missing: {path}")
    raw = path.read_bytes()
    try:
        contract = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"accepted regression contract is invalid JSON: {exc}") from exc
    if contract.get("schema_version") != 1:
        raise ValueError("accepted regression contract schema_version must be 1")
    if contract.get("publication_allowed") != "NO":
        raise ValueError("accepted regression contract must keep publication_allowed=NO")
    return contract, {
        "path": CONTRACT_RELATIVE_PATH.as_posix(),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def sitemap_locations(document: str) -> list[str]:
    """Return sitemap locations independent of an XML namespace prefix."""
    root = ET.fromstring(document)
    return [
        (element.text or "").strip()
        for element in root.iter()
        if element.tag.rsplit("}", 1)[-1] == "loc" and (element.text or "").strip()
    ]


def duplicate_first_sitemap_url(document: str) -> str:
    """Create an in-memory duplicate URL entry for a reverse test."""
    root = ET.fromstring(document)
    first_url = next(
        (element for element in list(root) if element.tag.rsplit("}", 1)[-1] == "url"),
        None,
    )
    if first_url is None:
        raise ValueError("cannot create sitemap duplicate test")
    root.append(copy.deepcopy(first_url))
    return ET.tostring(root, encoding="unicode")
