"""Redis for the real-time parts:

  ot:events          stream of carrier scans (the simulator writes, agents and the UI read)
  ot:activity        stream of what agents did (the UI's live feed)
  ot:cursor:{who}    how far each always-on agent has read in ot:events
  ot:once:{key}      idempotency: one 'delivered' email per order, one ticket per problem
  ot:lock:order:{id} one agent at a time per order
  ot:carrier:{id}    carrier API responses, cached for 60 s
  ot:flag:{name}     start/stop switches for background loops
"""

from __future__ import annotations

import json

from app import cache

EVENTS, ACTIVITY = "ot:events", "ot:activity"


def r():  # noqa: ANN201
    return cache.client()


def publish_event(ev: dict) -> str:
    return r().xadd(EVENTS, {"data": json.dumps(ev, default=str)}, maxlen=5000)


def publish_activity(item: dict) -> str:
    return r().xadd(ACTIVITY, {"data": json.dumps(item, default=str)}, maxlen=5000)


def read(stream: str, after: str = "0-0", count: int = 500) -> list[tuple[str, dict]]:
    start = "(" + after if after != "0-0" else "-"
    return [(i, json.loads(f["data"])) for i, f in r().xrange(stream, min=start, max="+", count=count)]


def cursor(who: str) -> str:
    return r().get(f"ot:cursor:{who}") or "0-0"


def set_cursor(who: str, last_id: str) -> None:
    r().set(f"ot:cursor:{who}", last_id)


def once(key: str, ttl: int = 7 * 86400) -> bool:
    """True the first time a key is seen. Makes always-on agents safe to re-run."""
    return bool(r().set(f"ot:once:{key}", "1", nx=True, ex=ttl))


def lock(order_id: int, ttl: int = 30) -> bool:
    return bool(r().set(f"ot:lock:order:{order_id}", "1", nx=True, ex=ttl))


def unlock(order_id: int) -> None:
    r().delete(f"ot:lock:order:{order_id}")


def carrier_cache_get(order_id: int) -> dict | None:
    v = r().get(f"ot:carrier:{order_id}")
    return json.loads(v) if v else None


def carrier_cache_set(order_id: int, value: dict) -> None:
    r().set(f"ot:carrier:{order_id}", json.dumps(value, default=str), ex=60)


def flag(name: str, value: bool | None = None) -> bool:
    if value is not None:
        r().set(f"ot:flag:{name}", "1" if value else "0")
    return r().get(f"ot:flag:{name}") == "1"


def wipe() -> None:
    for k in r().scan_iter("ot:*"):
        r().delete(k)
