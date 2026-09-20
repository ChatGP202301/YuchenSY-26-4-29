#!/usr/bin/env python3
"""Restore reviewed PP specification semantics on the CNR selection guide.

The historical sr-me guide and the current CNR guide have the same two tables
and fourteen configurations.  The CNR generator preserved the numeric values
but replaced several material/format fields with generic OEM labels.  This
bounded repair copies only the reviewed table headings and data cells while
preserving CNR configuration IDs, page chrome, links, metadata, and URLs.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROUTE = "pp-melt-blown-filter-cartridge.html"
TABLE_RE = re.compile(
    r'(<table class="sy-config-table".*?</table>)', re.DOTALL
)
HEAD_RE = re.compile(r"<thead>.*?</thead>", re.DOTALL)
BODY_RE = re.compile(r"(<tbody>)(.*?)(</tbody>)", re.DOTALL)
ROW_RE = re.compile(r"<tr>.*?</tr>", re.DOTALL)
TD_RE = re.compile(r"<td>.*?</td>", re.DOTALL)


def replace_data_cells(target_row: str, source_row: str) -> str:
    source_cells = TD_RE.findall(source_row)
    target_cells = TD_RE.findall(target_row)
    if len(source_cells) != 9 or len(target_cells) != 9:
        raise ValueError(
            f"expected nine data cells, found source={len(source_cells)} "
            f"target={len(target_cells)}"
        )
    iterator = iter(source_cells)
    return TD_RE.sub(lambda _match: next(iterator), target_row)


def repair_table(target: str, source: str) -> str:
    source_head = HEAD_RE.search(source)
    target_head = HEAD_RE.search(target)
    source_body = BODY_RE.search(source)
    target_body = BODY_RE.search(target)
    if not all((source_head, target_head, source_body, target_body)):
        raise ValueError("selection guide table is missing a head or body")

    source_rows = ROW_RE.findall(source_body.group(2))
    target_rows = ROW_RE.findall(target_body.group(2))
    if len(source_rows) != len(target_rows):
        raise ValueError(
            f"row count mismatch: source={len(source_rows)} target={len(target_rows)}"
        )
    repaired_rows = [
        replace_data_cells(target_row, source_row)
        for target_row, source_row in zip(target_rows, source_rows)
    ]
    repaired_body = target_body.group(1) + "".join(repaired_rows) + target_body.group(3)
    repaired = (
        target[: target_head.start()]
        + source_head.group(0)
        + target[target_head.end() :]
    )
    repaired_body_match = BODY_RE.search(repaired)
    if repaired_body_match is None:
        raise ValueError("repaired table lost its body")
    return (
        repaired[: repaired_body_match.start()]
        + repaired_body
        + repaired[repaired_body_match.end() :]
    )


def transform(target: str, source: str) -> str:
    target_tables = TABLE_RE.findall(target)
    source_tables = TABLE_RE.findall(source)
    if len(target_tables) != 2 or len(source_tables) != 2:
        raise ValueError(
            f"expected two PP tables, found source={len(source_tables)} "
            f"target={len(target_tables)}"
        )
    repaired_tables = [
        repair_table(target_table, source_table)
        for target_table, source_table in zip(target_tables, source_tables)
    ]
    iterator = iter(repaired_tables)
    repaired = TABLE_RE.sub(lambda _match: next(iterator), target)
    if repaired.count('<table class="sy-config-table"') != 2:
        raise ValueError("unexpected table count after repair")
    return repaired


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-root", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    target_path = args.site_root / "cnr" / ROUTE
    source_path = args.site_root / "sr-me" / ROUTE
    target = target_path.read_text(encoding="utf-8")
    source = source_path.read_text(encoding="utf-8")
    repaired = transform(target, source)

    changed = repaired != target
    if args.apply and changed:
        target_path.write_text(repaired, encoding="utf-8")
    print(
        f"route=cnr/{ROUTE} tables=2 configurations=14 "
        f"changed={str(changed).lower()} applied={str(args.apply and changed).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
