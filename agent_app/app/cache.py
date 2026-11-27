"""Redis: tool-result cache, preference cache, rate limits, run locks, and the approval queue
used by the Claude Agent SDK runtime. Uses real Redis when REDIS_URL is set, otherwise an
in-process fakeredis so the app and tests run with nothing installed."""

from __future__ import annotations

import hashlib
import json
import time

from . import config

_r = None


def client():
    global _r
    if _r is None:
        connect(config.REDIS_URL)
    return _r


def connect(url: str = "") -> None:
    global _r
    if url:
        import redis

        _r = redis.Redis.from_url(url, decode_responses=True)
        _r.ping()
    else:
        import fakeredis

        _r = fakeredis.FakeRedis(decode_responses=True)


def kind() -> str:
    return "fakeredis" if type(client()).__module__.startswith("fakeredis") else "redis"


# ---- tool result cache (read-only tools only) ----
def _key(tool: str, args: dict) -> str:
    return f"cache:tool:{tool}:" + hashlib.sha256(json.dumps(args, sort_keys=True, default=str).encode()).hexdigest()[:16]


def cache_get(tool: str, args: dict):  # noqa: ANN201
    v = client().get(_key(tool, args))
    return json.loads(v) if v is not None else None


def cache_set(tool: str, args: dict, value) -> None:  # noqa: ANN001
    client().set(_key(tool, args), json.dumps(value, default=str), ex=config.TOOL_CACHE_TTL)


def clear_tool_cache() -> None:
    r = client()
    for k in r.scan_iter("cache:tool:*"):
        r.delete(k)


# ---- preference cache ----
def prefs_get(user_id: str) -> dict | None:
    v = client().get(f"prefs:{user_id}")
    return json.loads(v) if v else None


def prefs_set(user_id: str, prefs: dict) -> None:
    client().set(f"prefs:{user_id}", json.dumps(prefs, default=str), ex=3600)


def prefs_drop(user_id: str) -> None:
    client().delete(f"prefs:{user_id}")


# ---- rate limit: fixed window per user per minute ----
def allow(user_id: str, limit: int | None = None) -> bool:
    limit = limit or config.RATE_LIMIT_PER_MIN
    key = f"ratelimit:{user_id}:{int(time.time() // 60)}"
    n = client().incr(key)
    if n == 1:
        client().expire(key, 70)
    return n <= limit


# ---- one decision at a time per run ----
def lock(run_id: str, seconds: int = 120) -> bool:
    return bool(client().set(f"lock:run:{run_id}", "1", nx=True, ex=seconds))


def unlock(run_id: str) -> None:
    client().delete(f"lock:run:{run_id}")


# ---- approval hand-off for runtimes that wait inside a callback (Claude Agent SDK) ----
def push_decisions(run_id: str, decisions: list) -> None:
    client().rpush(f"decisions:{run_id}", json.dumps(decisions))


async def wait_decisions(run_id: str, timeout: float = 3600) -> list | None:
    import anyio

    end = time.monotonic() + timeout
    while time.monotonic() < end:
        v = client().lpop(f"decisions:{run_id}")
        if v is not None:
            return json.loads(v)
        await anyio.sleep(0.05)
    return None
