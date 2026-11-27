"""Tools every agent uses, whatever its runtime. They do the real work against the database and
Redis, record each call as an agent step, and post it to the live activity feed.

Two safety rules live here, in code:
  * credits and reships never execute from an agent; they become approval requests
  * guards: credits are capped, reships only for lost or damaged parcels
And Redis makes repeated work harmless: one email per order per kind, one open ticket per order.
"""

from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass, field
from typing import Any, Callable

from sqlalchemy import select

from app import db

from . import bus
from .models import AgentRun, AgentStep, Approval, Notification, Order, Ticket, TrackingEvent, ensure

PROBLEM = ("delayed", "exception", "lost", "damaged")
CREDIT_CAP = 25.0


@dataclass
class RunRef:
    """Which agent run tool calls belong to. Built once per run and bound into the tools."""
    agent_type: str
    runtime: str
    run_id: int = 0
    iteration: int = 0

    @property
    def by(self) -> str:
        return f"{self.agent_type}/{self.runtime}"


@dataclass
class Tool:
    name: str
    desc: str
    params: dict
    fn: Callable[..., Any]
    effect: str = "read"
    call: Callable[..., Any] = field(default=None, repr=False)   # set by bind()


# ---------------- runs ----------------
def start_run(agent_type: str, runtime: str, mode: str, trigger: str) -> RunRef:
    ensure()
    with db.session() as s:
        run = AgentRun(agent_type=agent_type, runtime=runtime, mode=mode, trigger=trigger)
        s.add(run)
    bus.publish_activity({"kind": "run_start", "run_id": run.id, "agent": agent_type, "runtime": runtime, "trigger": trigger})
    return RunRef(agent_type, runtime, run.id)


def finish_run(ref: RunRef, summary: str, status: str = "done", path: list | None = None) -> None:
    with db.session() as s:
        run = s.get(AgentRun, ref.run_id)
        run.summary, run.status, run.finished = summary, status, db._now()
        if path is not None:
            run.path = path
    bus.publish_activity({"kind": "run_end", "run_id": ref.run_id, "agent": ref.agent_type, "runtime": ref.runtime,
                          "status": status, "summary": summary[:300], "path": path or []})


def step(ref: RunRef, kind: str, name: str, args: dict | None = None, result: Any = None, status: str = "ok") -> None:
    with db.session() as s:
        s.add(AgentStep(run_id=ref.run_id, kind=kind, name=name, args=args or {}, result=result, status=status))
    item = {"kind": kind, "run_id": ref.run_id, "agent": ref.agent_type, "runtime": ref.runtime, "name": name, "args": args or {}, "status": status}
    if kind == "iteration":
        item["summary"] = str(result)[:300]
    bus.publish_activity(item)


# ---------------- tool bodies ----------------
def _order_dict(o: Order) -> dict:
    late = max(0, (o.eta - o.promised).days)
    return {"order_id": o.id, "customer": o.customer, "email": o.email, "items": o.items, "total": o.total, "carrier": o.carrier,
            "tracking_no": o.tracking_no, "status": o.status, "promised": o.promised.isoformat(), "eta": o.eta.isoformat(), "days_late": late}


def get_order(order_id: int) -> dict:
    with db.session() as s:
        o = s.get(Order, int(order_id))
        return _order_dict(o) if o else {"error": f"no order {order_id}"}


def get_tracking(order_id: int) -> list:
    with db.session() as s:
        evs = s.scalars(select(TrackingEvent).where(TrackingEvent.order_id == int(order_id)).order_by(TrackingEvent.id)).all()
        return [{"code": e.code, "detail": e.detail, "location": e.location, "at": e.at.isoformat(timespec="seconds")} for e in evs][-10:]


def list_orders(status: str) -> list:
    with db.session() as s:
        rows = s.scalars(select(Order).order_by(Order.id)).all()
    if status == "problems":
        rows = [o for o in rows if o.status in PROBLEM]
    elif status != "all":
        rows = [o for o in rows if o.status == status]
    return [{"order_id": o.id, "customer": o.customer, "status": o.status, "eta": o.eta.isoformat()} for o in rows]


def carrier_status(order_id: int) -> dict:
    """The carrier's own view. Cached in Redis for 60 s (carrier APIs are slow and rate-limited)."""
    hit = bus.carrier_cache_get(int(order_id))
    if hit:
        return {**hit, "cached": True}
    o = get_order(order_id)
    trk = get_tracking(order_id)
    last = trk[-1] if trk else {}
    out = {"order_id": int(order_id), "carrier": o.get("carrier"), "last_scan": last.get("code"), "facility": last.get("location"),
           "claim_eligible": o.get("status") in ("lost", "damaged"), "note": last.get("detail", "")}
    bus.carrier_cache_set(int(order_id), out)
    return out


def _notify(ref: RunRef, order_id: int, kind: str, message: str) -> dict:
    if not bus.once(f"notify:{order_id}:{kind}"):
        return {"skipped": f"customer already got a '{kind}' message"}
    with db.session() as s:
        s.add(Notification(order_id=int(order_id), kind=kind, message=message, by=ref.by))
    return {"sent": True, "kind": kind}


def _ticket(ref: RunRef, order_id: int, reason: str, priority: str) -> dict:
    with db.session() as s:
        t = s.scalars(select(Ticket).where(Ticket.order_id == int(order_id), Ticket.status == "open")).first()
        if t:
            return {"ticket_id": t.id, "existing": True}
        t = Ticket(order_id=int(order_id), reason=reason, priority=priority if priority in ("low", "normal", "high") else "normal", by=ref.by)
        s.add(t)
    return {"ticket_id": t.id, "existing": False}


def _approval(ref: RunRef, order_id: int, action: str, args: dict, reason: str) -> dict:
    with db.session() as s:
        a = s.scalars(select(Approval).where(Approval.order_id == int(order_id), Approval.action == action)).first()
        if a:
            return {"approval_id": a.id, "status": a.status, "existing": True}
        a = Approval(order_id=int(order_id), action=action, args=args, reason=reason, by=ref.by)
        s.add(a)
    bus.publish_activity({"kind": "approval", "approval_id": a.id, "order_id": int(order_id), "action": action, "by": ref.by})
    return {"approval_id": a.id, "status": "pending", "note": "queued for a person to approve"}


def _credit(ref: RunRef, order_id: int, amount: float, reason: str) -> dict:
    o = get_order(order_id)
    cap = min(CREDIT_CAP, 0.2 * o.get("total", 0))
    if float(amount) > cap:
        return {"blocked": True, "reason": f"credits are capped at ${cap:.2f} for this order"}
    return _approval(ref, order_id, "credit", {"amount": float(amount)}, reason)


def _reship(ref: RunRef, order_id: int, reason: str) -> dict:
    if get_order(order_id).get("status") not in ("lost", "damaged"):
        return {"blocked": True, "reason": "reships are only for lost or damaged parcels"}
    return _approval(ref, order_id, "reship", {}, reason)


def make_tools(ref: RunRef) -> list[Tool]:
    """The tool set, bound to one run. Every call is recorded and streamed to the UI."""
    specs = [
        Tool("get_order", "Order details: customer, items, status, promised date, ETA, days late.", {"order_id": int}, get_order),
        Tool("get_tracking", "The carrier scans for an order, oldest first.", {"order_id": int}, get_tracking),
        Tool("list_orders", "List orders by status. Use 'problems' for delayed/exception/lost/damaged, or 'all'.", {"status": str}, list_orders),
        Tool("carrier_status", "Ask the carrier about a parcel (last scan, facility, claim eligibility).", {"order_id": int}, carrier_status),
        Tool("notify_customer", "Email the customer. kind: out_for_delivery|delivered|delay|address|issue. Sends once per kind.",
             {"order_id": int, "kind": str, "message": str}, lambda order_id, kind, message: _notify(ref, order_id, kind, message), "external"),
        Tool("open_ticket", "Open a support ticket (one open ticket per order). priority: low|normal|high.",
             {"order_id": int, "reason": str, "priority": str}, lambda order_id, reason, priority: _ticket(ref, order_id, reason, priority), "write"),
        Tool("request_credit", f"Ask a person to approve a goodwill credit (max ${CREDIT_CAP:.0f}, and at most 20% of the order).",
             {"order_id": int, "amount": float, "reason": str}, lambda order_id, amount, reason: _credit(ref, order_id, amount, reason), "money"),
        Tool("request_reship", "Ask a person to approve sending a replacement (lost or damaged parcels only).",
             {"order_id": int, "reason": str}, lambda order_id, reason: _reship(ref, order_id, reason), "money"),
    ]
    for t in specs:
        t.call = _recorder(ref, t)
    return specs


def _recorder(ref: RunRef, t: Tool) -> Callable[..., Any]:
    def call(**kw) -> Any:  # noqa: ANN003, ANN401
        try:
            out = t.fn(**kw)
            status = "blocked" if isinstance(out, dict) and out.get("blocked") else "skipped" if isinstance(out, dict) and out.get("skipped") else "ok"
        except Exception as e:  # noqa: BLE001
            out, status = {"error": f"{type(e).__name__}: {e}"}, "error"
        step(ref, "tool", t.name, kw, out, status)
        return out
    return call


def as_json(x: Any) -> str:  # noqa: ANN401
    return json.dumps(x, default=str)


# ---------------- people decide approvals ----------------
def decide(approval_id: int, approve: bool, who: str = "ops") -> dict:
    with db.session() as s:
        a = s.get(Approval, approval_id)
        if a is None or a.status != "pending":
            return {"error": "not pending"}
        a.status, a.decided_by = ("approved" if approve else "rejected"), who
        order_id, action, args = a.order_id, a.action, a.args
        if approve:
            if action == "reship":
                s.get(Order, order_id).status = "reshipped"
            msg = (f"A ${args.get('amount', 0):.2f} credit has been added to your account." if action == "credit"
                   else "A replacement is on its way; you'll get new tracking soon.")
            s.add(Notification(order_id=order_id, kind=action, message=msg, by=f"person/{who}"))
    bus.publish_activity({"kind": "approval_decided", "approval_id": approval_id, "approved": approve, "order_id": order_id, "action": action})
    return {"approval_id": approval_id, "status": "approved" if approve else "rejected"}


def snapshot() -> dict:
    """Everything the UI shows, in one call."""
    ensure()
    with db.session() as s:
        orders = [_order_dict(o) for o in s.scalars(select(Order).order_by(Order.id))]
        approvals = [{"id": a.id, "order_id": a.order_id, "action": a.action, "args": a.args, "reason": a.reason, "status": a.status, "by": a.by}
                     for a in s.scalars(select(Approval).order_by(Approval.id.desc()))]
        tickets = [{"id": t.id, "order_id": t.order_id, "reason": t.reason, "priority": t.priority, "by": t.by}
                   for t in s.scalars(select(Ticket).order_by(Ticket.id.desc()))]
        notes = [{"order_id": n.order_id, "kind": n.kind, "message": n.message, "by": n.by}
                 for n in s.scalars(select(Notification).order_by(Notification.id.desc()))]
        runs = [{"id": r.id, "agent_type": r.agent_type, "runtime": r.runtime, "status": r.status, "summary": r.summary, "path": r.path,
                 "trigger": r.trigger} for r in s.scalars(select(AgentRun).order_by(AgentRun.id.desc()).limit(30))]
    return {"orders": orders, "approvals": approvals, "tickets": tickets, "notifications": notes, "runs": runs,
            "today": dt.date.today().isoformat()}
