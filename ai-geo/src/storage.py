from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from core import canonical_json


TABLES = {
    "prompts": "prompt_id",
    "citations": "citation_id",
    "feature_observations": "observation_id",
    "competitor_snapshots": "snapshot_id",
    "experiments": "experiment_id",
    "deployments": "deployment_id",
    "retests": "retest_id",
}


def read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    records = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL {path}:{number}: {exc}") from exc
        if not isinstance(value, dict) or value.get("schema_version") != 1:
            raise ValueError(f"invalid record schema {path}:{number}")
        records.append(value)
    return records


def append_jsonl_idempotent(path: Path, records: list[dict], id_field: str) -> int:
    existing = read_jsonl(path)
    by_id = {str(item[id_field]): canonical_json(item) for item in existing}
    new_items = []
    for item in records:
        key = str(item[id_field])
        payload = canonical_json(item)
        if key in by_id:
            if by_id[key] != payload:
                raise ValueError(f"immutable record collision: {key}")
            continue
        by_id[key] = payload
        new_items.append(item)
    if not new_items:
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for item in new_items:
            handle.write(json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
    return len(new_items)


def create_schema(connection: sqlite3.Connection) -> None:
    for table, key in TABLES.items():
        connection.execute(f"CREATE TABLE IF NOT EXISTS {table} ({key} TEXT PRIMARY KEY, payload TEXT NOT NULL)")
    connection.execute("CREATE TABLE IF NOT EXISTS migrations (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)")
    connection.execute("INSERT OR IGNORE INTO migrations(version, applied_at) VALUES (1, datetime('now'))")
    connection.commit()


def rebuild_sqlite(database: Path, sources: dict[str, Path]) -> dict[str, int]:
    database.parent.mkdir(parents=True, exist_ok=True)
    if database.exists():
        database.unlink()
    counts = {}
    with sqlite3.connect(database) as connection:
        create_schema(connection)
        for table, path in sources.items():
            key = TABLES[table]
            records = read_jsonl(path)
            connection.executemany(
                f"INSERT INTO {table}({key}, payload) VALUES (?, ?)",
                [(str(item[key]), canonical_json(item).decode("utf-8")) for item in records],
            )
            counts[table] = len(records)
        connection.commit()
    return counts
