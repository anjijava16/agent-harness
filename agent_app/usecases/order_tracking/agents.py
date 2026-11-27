"""The three agent types, on any runtime. These functions own the bookkeeping (run records,
per-order locks, stop flags); the runtime modules own the agent itself."""

from __future__ import annotations

import asyncio

from . import bus
from .brain import CATEGORY
from .runtimes import get
from .runtimes.common import LoopIO
from .tools import finish_run, start_run


async def run_harness(runtime: str, ask: str, mode: str = "scripted") -> dict:
    ref = start_run("harness", runtime, mode, ask)
    try:
        answer = await get(runtime).harness(ref, ask, mode)
        finish_run(ref, answer)
        return {"run_id": ref.run_id, "status": "done", "answer": answer}
    except Exception as e:  # noqa: BLE001
        finish_run(ref, f"{type(e).__name__}: {e}", "error")
        return {"run_id": ref.run_id, "status": "error", "answer": f"{type(e).__name__}: {e}"}


async def run_graph(runtime: str, event: dict, mode: str = "scripted") -> dict:
    oid = event["order_id"]
    if not bus.lock(oid):
        return {"status": "skipped", "summary": f"another agent is working on order {oid}"}
    ref = start_run("graph", runtime, mode, f"event {event.get('event_id')}: {event['code']} on #{oid}")
    try:
        summary, path = await get(runtime).graph(ref, event, mode)
        finish_run(ref, summary, path=path)
        return {"run_id": ref.run_id, "status": "done", "summary": summary, "path": path}
    except Exception as e:  # noqa: BLE001
        finish_run(ref, f"{type(e).__name__}: {e}", "error")
        return {"run_id": ref.run_id, "status": "error", "summary": f"{type(e).__name__}: {e}", "path": []}
    finally:
        bus.unlock(oid)


async def run_looping(runtime: str, mode: str = "scripted", **io_kw) -> dict:  # noqa: ANN003
    who = f"looping:{runtime}"
    bus.flag(f"stop:{who}", False)
    io = LoopIO(who=who, **io_kw)
    ref = start_run("looping", runtime, mode, "carrier event stream")
    try:
        summary = await get(runtime).looping(ref, io, mode)
        finish_run(ref, summary)
        return {"run_id": ref.run_id, "status": "done", "iterations": io.iteration, "summary": summary}
    except Exception as e:  # noqa: BLE001
        finish_run(ref, f"{type(e).__name__}: {e}", "error")
        return {"run_id": ref.run_id, "status": "error", "iterations": io.iteration, "summary": f"{type(e).__name__}: {e}"}


def stop_looping(runtime: str) -> None:
    bus.flag(f"stop:looping:{runtime}", True)


async def graph_dispatcher(runtime: str, mode: str = "scripted", interval: float = 1.0, idle_limit: int = 0,
                           before_poll=None, max_polls: int = 10_000) -> int:  # noqa: ANN001
    """Always-on: start a graph agent for every event that needs one. Returns how many it ran."""
    who = f"graph:{runtime}"
    bus.flag(f"stop:{who}", False)
    io = LoopIO(who=who, interval=interval, idle_limit=idle_limit, max_iterations=max_polls, before_poll=before_poll)
    ran = 0
    while not io.should_stop():
        events = io.poll()
        io.iteration += 1
        for e in events:
            if CATEGORY.get(e["code"]):
                await run_graph(runtime, e, mode)
                ran += 1
        if not events and not io.should_stop():
            await asyncio.sleep(interval)
    return ran
