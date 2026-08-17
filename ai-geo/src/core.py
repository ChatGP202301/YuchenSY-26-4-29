from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

SCHEMA_VERSION = 1
AI_GEO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_ROOT = AI_GEO_ROOT / "config"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def stable_id(prefix: str, value: object) -> str:
    return f"{prefix}-{hashlib.sha256(canonical_json(value)).hexdigest()[:20]}"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_config(name: str) -> dict:
    path = CONFIG_ROOT / name
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"unsupported config schema: {path}")
    return data


def atomic_write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def normalize_url(url: str) -> str:
    parsed = urlsplit(url.strip())
    scheme = parsed.scheme.lower()
    host = (parsed.hostname or "").lower()
    if parsed.port and not (scheme == "https" and parsed.port == 443):
        netloc = f"{host}:{parsed.port}"
    else:
        netloc = host
    path = parsed.path or "/"
    return urlunsplit((scheme, netloc, path, parsed.query, ""))


def runtime_state(env: dict[str, str] | None = None) -> dict:
    env = os.environ if env is None else env
    config = load_config("system.yaml")
    enabled = env.get(config["enabled_env"], str(config["default_enabled"])).lower() == "true"
    mode = env.get(config["mode_env"], config["default_mode"]).upper()
    if mode not in {"DRY_RUN", "AUTO_L1"}:
        mode = "DRY_RUN"
    auto_ready = bool(config["repository_policy"]["allow_auto_merge"] and config["repository_policy"]["branch_protection_verified"])
    if mode == "AUTO_L1" and not auto_ready:
        mode = "DRY_RUN"
        blocked = "REQUIRES_GITHUB_PERMISSION"
    else:
        blocked = None
    return {"enabled": enabled, "mode": mode, "auto_l1_ready": auto_ready, "blocked": blocked, "budget_usd": config["budget_usd"]}
