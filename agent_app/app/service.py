"""Runs a use case on the framework the user prefers, pauses for approvals, and stores
everything (runs, tool calls, events, memory) in the database."""

from __future__ import annotations

from collections import Counter

from sqlalchemy import select

from . import cache, config, db, runtimes, usecases
from .runtimes import Outcome, RunCtx, Runtime
from .spec import scripted_decision
from .tools import ToolRuntime

# Live agent objects for runs that are running or paused, keyed by run id. Per process.
LIVE: dict[str, tuple[Runtime, RunCtx, bool]] = {}


def effective_prefs(user_id: str, uc=None) -> dict:  # noqa: ANN001
    """Defaults < the use case's needs < the user's saved preferences. Cached in Redis."""
    user = cache.prefs_get(user_id)
    if user is None:
        user = db.get_prefs(user_id)
        cache.prefs_set(user_id, user)
    return {**config.DEFAULT_PROFILE, **(uc.prefs if uc else {}), **user}


def save_prefs(user_id: str, values: dict) -> dict:
    db.set_prefs(user_id, values)
    cache.prefs_drop(user_id)
    return effective_prefs(user_id)


def create_run(user_id: str, usecase_id: int, framework: str | None = None, mode: str | None = None,
               auto_approve: bool = False, message: str | None = None) -> str:
    """Store the run and build its context. Returns the run id; execute() does the work."""
    db.ensure_user(user_id)
    uc = usecases.get(usecase_id)
    prefs = effective_prefs(user_id, uc)
    framework = framework or prefs.get("framework") or config.DEFAULT_FRAMEWORK
    mode = mode or prefs.get("mode") or config.DEFAULT_MODE
    ask, steps = uc.resolved(prefs)
    if message and mode == "live":
        ask = message
    with db.session() as s:
        run = db.Run(user_id=user_id, usecase_id=uc.id, framework=framework, mode=mode, ask=ask)
        s.add(run)
    ctx = RunCtx(run.id, user_id, uc, prefs, mode, ask, steps, ToolRuntime(run.id, user_id, uc, prefs))
    db.add_event(run.id, "start", {"framework": framework, "mode": mode, "usecase": uc.id})
    LIVE[run.id] = (runtimes.get(framework), ctx, auto_approve)
    return run.id


async def execute(run_id: str) -> dict:
    rt, ctx, _ = LIVE[run_id]
    try:
        out = await rt.start(ctx)
    except Exception as e:  # noqa: BLE001
        out = Outcome("error", error=f"{type(e).__name__}: {e}")
    return await _settle(run_id, out)


async def start_run(user_id: str, usecase_id: int, framework: str | None = None, mode: str | None = None,
                    auto_approve: bool = False, message: str | None = None) -> dict:
    return await execute(create_run(user_id, usecase_id, framework, mode, auto_approve, message))


async def decide(run_id: str, decisions: list[dict]) -> dict:
    if run_id not in LIVE:
        raise LookupError("This run isn't paused in this process (finished, or the server restarted). "
                          "Use a persistent checkpointer/session service to resume across restarts.")
    if not cache.lock(run_id):
        raise RuntimeError("Another decision for this run is being processed.")
    try:
        rt, ctx, _ = LIVE[run_id]
        with db.session() as s:
            pending = s.get(db.Run, run_id).pending
        if len(decisions) != len(pending):
            raise ValueError(f"expected {len(pending)} decisions, got {len(decisions)}")
        decisions = _normalise(ctx, pending, decisions)
        try:
            out = await rt.resume(ctx, decisions)
        except Exception as e:  # noqa: BLE001
            out = Outcome("error", error=f"{type(e).__name__}: {e}")
        return await _settle(run_id, out)
    finally:
        cache.unlock(run_id)


def _normalise(ctx: RunCtx, pending: list, decisions: list[dict]) -> list[dict]:
    out = []
    for p, d in zip(pending, decisions, strict=True):
        kind = d.get("type", "approve")
        if kind == "edit":
            d = {"type": "edit", "args": {**p["args"], **(d.get("args") or {})}}
        elif kind == "reject":
            d = {"type": "reject", "message": d.get("message") or f"The user declined {p['tool']}."}
            ctx.tools.rejected(p["tool"], p["args"], d["message"])
        else:
            d = {"type": "approve"}
        db.add_event(ctx.run_id, "decision", {"tool": p["tool"], "decision": d["type"]})
        out.append(d)
    return out


async def _settle(run_id: str, out: Outcome) -> dict:
    rt, ctx, auto = LIVE[run_id]
    while out.status == "paused" and auto:
        decisions = []
        for p in out.pending:
            n = ctx.tools.decided.get(p["tool"], 0)
            ctx.tools.decided[p["tool"]] = n + 1
            decisions.append(scripted_decision(ctx.uc, p["tool"], n, p["args"]))
        decisions = _normalise(ctx, out.pending, decisions)
        try:
            out = await rt.resume(ctx, decisions)
        except Exception as e:  # noqa: BLE001
            out = Outcome("error", error=f"{type(e).__name__}: {e}")
    status = {"paused": "awaiting_approval"}.get(out.status, out.status)
    with db.session() as s:
        run = s.get(db.Run, run_id)
        run.status, run.final, run.pending, run.error = status, out.final, out.pending, out.error
        if status in ("done", "error"):
            run.checks = checks(ctx, out)
    db.add_event(run_id, status, {"pending": out.pending} if out.pending else {"final": out.final[:200]})
    if status in ("done", "error"):
        LIVE.pop(run_id, None)
    return get_run(run_id)


def checks(ctx: RunCtx, out: Outcome) -> list:
    calls = tool_calls(ctx.run_id)
    seen = Counter(c["tool"] for c in calls)
    res = [("finished without error", out.status == "done")]
    if ctx.scripted:
        # Every planned call must end up recorded once: ok, cached, blocked or rejected.
        planned = Counter(n for s in ctx.steps for n, _ in s.calls)
        res.append(("every planned call ran (or was blocked/rejected on purpose)", all(seen[n] >= k for n, k in planned.items())))
        expected = next((s.text for s in reversed(ctx.steps) if s.text), "")
        res.append(("final answer delivered", out.final.strip() == (expected or "").strip()))
    else:
        res.append(("final answer delivered", bool(out.final.strip())))
    c = {"calls": calls, "actions": [x for x in calls if x["status"] == "ok" and x["effect"] != "read"],
         "blocked": [x for x in calls if x["status"] == "blocked"], "rejected": [x for x in calls if x["status"] == "rejected"],
         "final": out.final, "prefs": ctx.prefs, "memories": ctx.tools._recall("")}
    for label, fn in ctx.uc.expect:
        try:
            ok = bool(fn(c))
        except Exception:  # noqa: BLE001
            ok = False
        res.append((label, ok))
    return [[label, ok] for label, ok in res]


def tool_calls(run_id: str) -> list[dict]:
    with db.session() as s:
        rows = s.scalars(select(db.ToolCall).where(db.ToolCall.run_id == run_id).order_by(db.ToolCall.id)).all()
        return [{"tool": r.tool, "args": r.args, "result": r.result, "effect": r.effect, "status": r.status, "note": r.note} for r in rows]


def get_run(run_id: str) -> dict:
    with db.session() as s:
        r = s.get(db.Run, run_id)
        if r is None:
            raise KeyError(run_id)
        ev = s.scalars(select(db.Event).where(db.Event.run_id == run_id).order_by(db.Event.id)).all()
        d = {k: getattr(r, k) for k in ("id", "user_id", "usecase_id", "framework", "mode", "status", "ask", "final", "pending", "checks", "error")}
        d["events"] = [{"kind": e.kind, "data": e.data} for e in ev]
    d["tool_calls"] = tool_calls(run_id)
    d["ok"] = d["status"] == "done" and all(ok for _, ok in d["checks"])
    return d
