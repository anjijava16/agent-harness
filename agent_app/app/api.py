"""FastAPI backend.

    uvicorn app.api:app --reload        (from agent_app/)
    open http://localhost:8000

Run with one worker: paused agents live in this process (see README, "Going to production").
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy import select

from . import cache, config, db, runtimes, service, usecases

Framework = Literal["deepagents", "langgraph", "adk", "claude"]
_background: set[asyncio.Task] = set()


@asynccontextmanager
async def lifespan(_: FastAPI):  # noqa: ANN201
    db.init()
    cache.client()
    yield


app = FastAPI(title="Personal agent app", version="1.0", lifespan=lifespan)


class RunIn(BaseModel):
    user_id: str = "sam"
    usecase_id: int
    framework: Framework | None = None        # None -> the user's preference
    mode: Literal["scripted", "live"] | None = None
    auto_approve: bool = False                # demo: apply the use case's own decisions
    message: str | None = None                # live mode only: replace the use case's ask


class Decision(BaseModel):
    type: Literal["approve", "reject", "edit"] = "approve"
    args: dict | None = None                  # edit: changed arguments (merged into the original)
    message: str | None = None                # reject: reason given back to the agent


class DecisionsIn(BaseModel):
    decisions: list[Decision] = Field(min_length=1)


def _uc_summary(u) -> dict:  # noqa: ANN001
    return {"id": u.id, "area": u.area, "title": u.title, "ask": u.ask, "why": u.why, "features": u.features,
            "tools": [{"name": t.name, "effect": t.effect, "approval": t.name in u.gated, "guard": t.name in u.guards} for t in u.tools]}


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "database": db.dialect(), "redis": cache.kind(), "frameworks": runtimes.available(),
            "default_framework": config.DEFAULT_FRAMEWORK, "default_mode": config.DEFAULT_MODE}


@app.get("/api/frameworks")
def frameworks() -> list[dict]:
    av = runtimes.available()
    return [{"id": k, "label": runtimes.LABELS[k], "installed": av[k]} for k in config.FRAMEWORKS]


@app.get("/api/usecases")
def list_usecases(area: str | None = None, q: str | None = None) -> dict:
    items = [u for u in usecases.all_usecases() if (not area or u.area == area)
             and (not q or q.lower() in (u.title + " " + u.ask).lower())]
    return {"areas": [{"id": a, "label": label} for a, label in usecases.AREAS], "items": [_uc_summary(u) for u in items]}


@app.get("/api/usecases/{uc_id}")
def get_usecase(uc_id: int, user_id: str = "sam") -> dict:
    try:
        u = usecases.get(uc_id)
    except KeyError:
        raise HTTPException(404, "no such use case") from None
    ask, steps = u.resolved(service.effective_prefs(user_id, u))
    return {**_uc_summary(u), "ask": ask, "steps": [{"calls": [{"tool": n, "args": a} for n, a in s.calls], "text": s.text} for s in steps]}


@app.get("/api/users/{user_id}/preferences")
def get_prefs(user_id: str) -> dict:
    p = service.effective_prefs(user_id)
    p.setdefault("framework", config.DEFAULT_FRAMEWORK)
    p.setdefault("mode", config.DEFAULT_MODE)
    return p


@app.put("/api/users/{user_id}/preferences")
def put_prefs(user_id: str, values: dict) -> dict:
    if "framework" in values and values["framework"] not in config.FRAMEWORKS:
        raise HTTPException(422, f"framework must be one of {config.FRAMEWORKS}")
    return service.save_prefs(user_id, values)


@app.get("/api/users/{user_id}/memories")
def memories(user_id: str) -> dict:
    with db.session() as s:
        return {m.key: m.value for m in s.scalars(select(db.Memory).where(db.Memory.user_id == user_id))}


@app.get("/api/users/{user_id}/runs")
def user_runs(user_id: str, limit: int = 20) -> list[dict]:
    with db.session() as s:
        rows = s.scalars(select(db.Run).where(db.Run.user_id == user_id).order_by(db.Run.created_at.desc()).limit(limit)).all()
        return [{"id": r.id, "usecase_id": r.usecase_id, "framework": r.framework, "status": r.status, "created_at": r.created_at.isoformat()} for r in rows]


@app.post("/api/runs")
async def create_run(body: RunIn, wait: bool = Query(True, description="false: return at once and poll GET /api/runs/{id}")) -> dict:
    if not cache.allow(body.user_id):
        raise HTTPException(429, "rate limit: too many runs this minute")
    try:
        usecases.get(body.usecase_id)
    except KeyError:
        raise HTTPException(404, "no such use case") from None
    if not runtimes.available().get(body.framework or service.effective_prefs(body.user_id).get("framework", config.DEFAULT_FRAMEWORK)):
        raise HTTPException(400, "that framework isn't installed on this server")
    run_id = service.create_run(body.user_id, body.usecase_id, body.framework, body.mode, body.auto_approve, body.message)
    if wait:
        return await service.execute(run_id)
    task = asyncio.get_running_loop().create_task(service.execute(run_id))
    _background.add(task)
    task.add_done_callback(_background.discard)
    return {"id": run_id, "status": "running"}


@app.get("/api/runs/{run_id}")
def read_run(run_id: str) -> dict:
    try:
        return service.get_run(run_id)
    except KeyError:
        raise HTTPException(404, "no such run") from None


@app.post("/api/runs/{run_id}/decisions")
async def post_decisions(run_id: str, body: DecisionsIn) -> dict:
    try:
        return await service.decide(run_id, [d.model_dump() for d in body.decisions])
    except LookupError as e:
        raise HTTPException(409, str(e)) from None
    except ValueError as e:
        raise HTTPException(422, str(e)) from None
    except RuntimeError as e:
        raise HTTPException(423, str(e)) from None


@app.get("/")
def index() -> FileResponse:
    return FileResponse(config.ROOT / "ui" / "index.html")
