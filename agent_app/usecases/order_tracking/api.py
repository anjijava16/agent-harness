"""FastAPI routes for live order tracking. Mounted into the main app (app/api.py), so the same server
serves both UIs:  http://localhost:8000/  and  http://localhost:8000/orders

Standalone:  uvicorn usecases.order_tracking.api:app --reload   (from agent_app/)
"""

from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from sqlalchemy import select

from app import cache, db

from . import AGENT_TYPES, LABELS, RUNTIMES, agents, bus
from .brain import CATEGORY
from .models import AgentRun, AgentStep, Order, TrackingEvent, ensure
from .sim import Simulator
from .tools import decide, snapshot

router = APIRouter()
Runtime = Literal["langchain", "langgraph", "deepagents", "adk", "adk_workflow", "claude"]
Mode = Literal["scripted", "live"]

SIM = Simulator(seed=7)
TASKS: dict[str, asyncio.Task] = {}          # background work in this process: sim, looping:<rt>, graph:<rt>


def _running() -> dict:
    return {k: not t.done() for k, t in TASKS.items()}


def _spawn(key: str, coro) -> None:  # noqa: ANN001
    if key in TASKS and not TASKS[key].done():
        coro.close()
        raise HTTPException(409, f"{key} is already running")
    TASKS[key] = asyncio.get_running_loop().create_task(coro)


def _boot() -> None:
    ensure()
    with db.session() as s:
        empty = s.scalar(select(Order.id).limit(1)) is None
    if empty:
        SIM.reset()


# ---------------- page + state ----------------
@router.get("/orders", include_in_schema=False)
def page() -> FileResponse:
    return FileResponse(__file__.rsplit("/", 1)[0] + "/ui.html")


@router.get("/api/ot/meta")
def meta() -> dict:
    _boot()
    return {"runtimes": [{"id": r, "label": LABELS[r]} for r in RUNTIMES], "agent_types": AGENT_TYPES,
            "database": db.dialect(), "redis": cache.kind()}


@router.get("/api/ot/state")
def state() -> dict:
    _boot()
    return {**snapshot(), "running": _running()}


@router.get("/api/ot/events")
def events(limit: int = 60) -> list[dict]:
    with db.session() as s:
        rows = s.scalars(select(TrackingEvent).order_by(TrackingEvent.id.desc()).limit(limit)).all()
        return [{"event_id": e.id, "order_id": e.order_id, "code": e.code, "detail": e.detail, "location": e.location,
                 "actionable": e.code in CATEGORY, "at": e.at.isoformat(timespec="seconds")} for e in rows]


@router.get("/api/ot/runs/{run_id}")
def run_detail(run_id: int) -> dict:
    with db.session() as s:
        r = s.get(AgentRun, run_id)
        if r is None:
            raise HTTPException(404, "no such run")
        steps = s.scalars(select(AgentStep).where(AgentStep.run_id == run_id).order_by(AgentStep.id)).all()
        return {"id": r.id, "agent_type": r.agent_type, "runtime": r.runtime, "status": r.status, "summary": r.summary, "path": r.path,
                "steps": [{"kind": x.kind, "name": x.name, "args": x.args, "result": x.result, "status": x.status} for x in steps]}


# ---------------- simulator ----------------
class SimIn(BaseModel):
    interval: float = 2.0


@router.post("/api/ot/reset")
async def reset(seed: int = 7) -> dict:
    for k, t in list(TASKS.items()):
        t.cancel()
    TASKS.clear()
    global SIM
    SIM = Simulator(seed=seed)
    SIM.reset()
    return state()


@router.post("/api/ot/sim/tick")
def sim_tick() -> dict:
    return {"events": SIM.tick(), "done": SIM.done()}


@router.post("/api/ot/sim/start")
async def sim_start(body: SimIn) -> dict:
    async def loop() -> None:
        while not SIM.done():
            SIM.tick()
            await asyncio.sleep(body.interval)

    _spawn("sim", loop())
    return {"running": _running()}


@router.post("/api/ot/sim/stop")
def sim_stop() -> dict:
    if "sim" in TASKS:
        TASKS["sim"].cancel()
    return {"running": _running()}


# ---------------- the three agent types ----------------
class HarnessIn(BaseModel):
    runtime: Runtime = "deepagents"
    ask: str
    mode: Mode = "scripted"


@router.post("/api/ot/harness")
async def harness(body: HarnessIn) -> dict:
    out = await agents.run_harness(body.runtime, body.ask, body.mode)
    return {**out, "run": run_detail(out["run_id"])}


class LoopIn(BaseModel):
    runtime: Runtime = "langgraph"
    mode: Mode = "scripted"
    interval: float = 2.0
    max_iterations: int = 500


@router.post("/api/ot/looping/start")
async def looping_start(body: LoopIn) -> dict:
    _spawn(f"looping:{body.runtime}", agents.run_looping(body.runtime, body.mode, interval=body.interval, max_iterations=body.max_iterations))
    return {"running": _running()}


@router.post("/api/ot/looping/stop")
def looping_stop(runtime: Runtime) -> dict:
    agents.stop_looping(runtime)            # the loop sees the Redis flag and finishes its current iteration
    return {"running": _running()}


class GraphIn(BaseModel):
    runtime: Runtime = "adk_workflow"
    event_id: int
    mode: Mode = "scripted"


@router.post("/api/ot/graph/run")
async def graph_run(body: GraphIn) -> dict:
    with db.session() as s:
        e = s.get(TrackingEvent, body.event_id)
        if e is None:
            raise HTTPException(404, "no such event")
        o = s.get(Order, e.order_id)
        ev = {"event_id": e.id, "order_id": e.order_id, "code": e.code, "detail": e.detail, "location": e.location, "status": o.status, "carrier": o.carrier}
    out = await agents.run_graph(body.runtime, ev, body.mode)
    return {**out, "run": run_detail(out["run_id"]) if out.get("run_id") else None}


class AutoIn(BaseModel):
    runtime: Runtime = "adk_workflow"
    mode: Mode = "scripted"
    interval: float = 1.0


@router.post("/api/ot/graph/auto/start")
async def graph_auto_start(body: AutoIn) -> dict:
    _spawn(f"graph:{body.runtime}", agents.graph_dispatcher(body.runtime, body.mode, interval=body.interval))
    return {"running": _running()}


@router.post("/api/ot/graph/auto/stop")
def graph_auto_stop(runtime: Runtime) -> dict:
    bus.flag(f"stop:graph:{runtime}", True)
    return {"running": _running()}


# ---------------- people ----------------
class DecisionIn(BaseModel):
    approve: bool
    who: str = "ops"


@router.post("/api/ot/approvals/{approval_id}")
def approval(approval_id: int, body: DecisionIn) -> dict:
    out = decide(approval_id, body.approve, body.who)
    if "error" in out:
        raise HTTPException(409, out["error"])
    return out


# ---------------- live stream (Server-Sent Events) ----------------
def _tail_id(stream: str) -> str:
    last = bus.r().xrevrange(stream, count=1)
    return last[0][0] if last else "0-0"


@router.get("/api/ot/stream")
async def stream(request: Request, since: str = "now", max_events: int = 0) -> StreamingResponse:
    """Carrier scans and agent activity as they happen. since=now (default) or since=start."""

    async def gen():  # noqa: ANN202
        cur = {s: ("0-0" if since == "start" else _tail_id(s)) for s in (bus.EVENTS, bus.ACTIVITY)}
        sent = 0
        yield "retry: 2000\n\n"
        while True:
            for s, name in ((bus.EVENTS, "scan"), (bus.ACTIVITY, "activity")):
                for i, data in bus.read(s, cur[s], 200):
                    cur[s] = i
                    sent += 1
                    yield f"event: {name}\nid: {i}\ndata: {json.dumps(data, default=str)}\n\n"
                    if max_events and sent >= max_events:
                        return
            if await request.is_disconnected():
                return
            await asyncio.sleep(0.4)

    return StreamingResponse(gen(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# standalone app
@asynccontextmanager
async def _lifespan(_: FastAPI):  # noqa: ANN202
    db.init()
    cache.client()
    yield


app = FastAPI(title="Live order tracking", lifespan=_lifespan)
app.include_router(router)
