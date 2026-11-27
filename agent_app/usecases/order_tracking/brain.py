"""The stand-in model's decisions, plus the prompts a real model gets.

Offline, every runtime gets a stand-in model that asks `decide(task, observations)` what to do
next. It is a small rule-based policy: it reads the task and the tool results so far, and returns
either tool calls or a final answer. It reacts to the live data, so different events lead to
different actions. Only the model is replaced; the framework, tools, database and Redis are real.

In live mode the same TASK text goes to a real model with SYSTEM[agent_type] as instructions.
"""

from __future__ import annotations

import json
import re

CATEGORY = {"out_for_delivery": "heads_up", "delivered": "delivered", "delayed": "delay", "weather_hold": "delay",
            "address_issue": "address", "lost": "lost", "damaged": "damaged"}          # anything else: routine
STATUS_CATEGORY = {"delayed": "delay", "exception": "address", "lost": "lost", "damaged": "damaged",
                   "out_for_delivery": "heads_up", "delivered": "delivered"}

RULES = """How to handle each kind of event:
- out_for_delivery: notify_customer kind=out_for_delivery
- delivered: notify_customer kind=delivered
- delayed / weather_hold: notify_customer kind=delay with the new ETA; if days_late >= 2, request_credit of $5
- address_issue: open_ticket priority=high, notify_customer kind=address asking for the full address
- lost / damaged: check carrier_status, open_ticket priority=high, request_reship, notify_customer kind=issue
- anything else: no action
Credits and reships are requests for a person to approve; say so. Notifications are sent once per kind."""

SYSTEM = {
    "harness": "You are the order-support agent for an online store. Use the tools to look things up before answering. "
               "Fix problems you find, following these rules.\n" + RULES + "\nEnd with a short, plain answer for the person asking.",
    "looping": "You watch the live stream of carrier scans. Each turn you get the new events as JSON. Look up the orders you need, "
               "act on each event by these rules, then reply with one line summarizing what you did.\n" + RULES,
    "classify": "Classify the carrier event into exactly one category: heads_up, delivered, delay, address, lost, damaged, routine. "
                'Reply with JSON only: {"category": "..."}',
    "draft": "Write a short, friendly customer email (2 sentences max) for this order situation. Plain text only.",
    "investigator": "You investigate one problem parcel: check carrier_status and the order, open a high-priority ticket, "
                    "request a reship, notify the customer (kind=issue), then report back in one sentence.",
}


def task_text(task: dict) -> str:
    return "TASK: " + json.dumps(task, default=str)


def parse_task(text: str) -> dict:
    m = re.search(r"TASK:\s*(\{.*\})", text or "", re.S)
    if not m:
        return {"agent": "harness", "ask": text or ""}
    return json.loads(m.group(1))


def _first(name: str) -> str:
    return (name or "there").split()[0]


def message_for(category: str, order: dict) -> str:
    f, items = _first(order.get("customer", "")), order.get("items", "order")
    return {
        "heads_up": f"Good news {f}: your {items} is out for delivery today.",
        "delivered": f"Hi {f}, your {items} was delivered. Enjoy!",
        "delay": f"Sorry {f}, your {items} is running late. New estimated delivery: {order.get('eta')}.",
        "address": f"Hi {f}, the driver couldn't deliver your {items}: the address is missing an apartment number. Reply with the full address and we'll redeliver.",
        "lost": f"Sorry {f}, the carrier lost your {items}. We've opened a case and asked for a replacement to be sent.",
        "damaged": f"Sorry {f}, your {items} arrived damaged. We've opened a case and asked for a replacement to be sent.",
    }.get(category, "")


def actions_for(category: str, order: dict) -> list[tuple[str, dict]]:
    """The rules above, as tool calls. Shared by the looping agent, the harness and the graph."""
    oid = order["order_id"]
    msg = message_for(category, order)
    if category == "heads_up":
        return [("notify_customer", {"order_id": oid, "kind": "out_for_delivery", "message": msg})]
    if category == "delivered":
        return [("notify_customer", {"order_id": oid, "kind": "delivered", "message": msg})]
    if category == "delay":
        out = [("notify_customer", {"order_id": oid, "kind": "delay", "message": msg})]
        if order.get("days_late", 0) >= 2:
            out.append(("request_credit", {"order_id": oid, "amount": 5.0, "reason": f"{order['days_late']} days late"}))
        return out
    if category == "address":
        return [("open_ticket", {"order_id": oid, "reason": "address incomplete: needs apartment number", "priority": "high"}),
                ("notify_customer", {"order_id": oid, "kind": "address", "message": msg})]
    if category in ("lost", "damaged"):
        return [("open_ticket", {"order_id": oid, "reason": f"parcel {category}", "priority": "high"}),
                ("request_reship", {"order_id": oid, "reason": f"parcel {category}"}),
                ("notify_customer", {"order_id": oid, "kind": "issue", "message": msg})]
    return []


def _results(obs: list[dict], tool: str) -> list:
    return [o["result"] for o in obs if o["tool"] == tool]


def _did(obs: list[dict], tool: str) -> bool:
    return any(o["tool"] == tool for o in obs)


def _summary(obs: list[dict]) -> str:
    parts = []
    for o in obs:
        r = o["result"] if isinstance(o["result"], dict) else {}
        a = o["args"]
        if o["tool"] == "notify_customer":
            parts.append(f"emailed #{a.get('order_id')} ({a.get('kind')})" if r.get("sent") else f"#{a.get('order_id')} already had a '{a.get('kind')}' email")
        elif o["tool"] == "open_ticket":
            parts.append(f"ticket for #{a.get('order_id')}")
        elif o["tool"] in ("request_credit", "request_reship"):
            what = "credit" if o["tool"] == "request_credit" else "reship"
            parts.append(f"{what} for #{a.get('order_id')} blocked ({r.get('reason')})" if r.get("blocked") else f"{what} for #{a.get('order_id')} sent for approval")
    return "; ".join(parts)


def decide(task: dict, obs: list[dict]) -> dict:
    """Returns {"calls": [(tool, args), ...]} or {"final": text}."""
    kind = task.get("agent")

    if kind == "classify":
        return {"final": json.dumps({"category": CATEGORY.get(task["event"]["code"], "routine")})}

    if kind == "draft":
        return {"final": message_for(task["category"], task["order"]) or "No message needed."}

    if kind == "looping":
        events = [e for e in task.get("events", []) if CATEGORY.get(e["code"])]
        if not events:
            return {"final": f"Iteration {task.get('iteration')}: {len(task.get('events', []))} new events, nothing to do."}
        ids = sorted({e["order_id"] for e in events})
        if not _did(obs, "get_order"):
            calls = [("get_order", {"order_id": i}) for i in ids]
            calls += [("carrier_status", {"order_id": e["order_id"]}) for e in events if CATEGORY[e["code"]] in ("lost", "damaged")]
            return {"calls": calls}
        if not any(o["tool"] in ("notify_customer", "open_ticket") for o in obs):
            orders = {r["order_id"]: r for r in _results(obs, "get_order") if "order_id" in r}
            calls = [c for e in events for c in actions_for(CATEGORY[e["code"]], orders[e["order_id"]])]
            return {"calls": calls}
        return {"final": f"Iteration {task.get('iteration')}: {len(events)} events needed action. " + _summary(obs) + "."}

    if kind == "investigator":
        oid = task["order_id"]
        if not _did(obs, "get_order"):
            return {"calls": [("get_order", {"order_id": oid}), ("carrier_status", {"order_id": oid})]}
        order = _results(obs, "get_order")[0]
        cat = STATUS_CATEGORY.get(order["status"], "routine")
        if not _did(obs, "open_ticket") and cat in ("lost", "damaged"):
            return {"calls": actions_for(cat, order)}
        return {"final": f"Investigated #{oid}: carrier confirms it is {order['status']}. " + (_summary(obs) or "nothing to do") + "."}

    # ---- harness: a question or an investigation, phrased by a person ----
    ask = task.get("ask", "")
    oid = task.get("order_id") or next((int(x) for x in re.findall(r"\b(1\d{3})\b", ask)), None)
    if oid is None:
        if not _did(obs, "list_orders"):
            return {"calls": [("list_orders", {"status": "problems"})]}
        rows = _results(obs, "list_orders")[0]
        if not rows:
            return {"final": "No orders have problems right now."}
        return {"final": f"{len(rows)} orders need attention: " + ", ".join(f"#{r['order_id']} {r['customer']} ({r['status']})" for r in rows) + "."}
    if not _did(obs, "get_order"):
        return {"calls": [("get_order", {"order_id": oid}), ("get_tracking", {"order_id": oid})]}
    order = _results(obs, "get_order")[0]
    if "error" in order:
        return {"final": f"I can't find order {oid}."}
    cat = STATUS_CATEGORY.get(order["status"], "routine")
    if cat in ("lost", "damaged") and task.get("delegate") and not _did(obs, "task"):
        return {"calls": [("task", {"subagent_type": "carrier-investigator",
                                    "description": task_text({"agent": "investigator", "order_id": oid})})]}
    if cat in ("delay", "address", "lost", "damaged") and not _did(obs, "carrier_status") and not _did(obs, "task"):
        return {"calls": [("carrier_status", {"order_id": oid})]}
    acted = any(o["tool"] in ("notify_customer", "open_ticket", "task") for o in obs)
    todo = [] if acted else [c for c in actions_for(cat, order) if cat not in ("heads_up", "delivered")]
    if todo:
        return {"calls": todo}
    trk = _results(obs, "get_tracking")[0] if _did(obs, "get_tracking") else []
    last = trk[-1] if trk else {}
    text = f"Order #{oid} ({order['items']} for {order['customer']}) is {order['status'].replace('_', ' ')}."
    if last:
        text += f" Last scan: {last['detail']} in {last['location']}."
    text += f" ETA {order['eta']}" + (f", {order['days_late']} days late." if order["days_late"] else ".")
    done = _summary(obs) or next((o["result"] for o in obs if o["tool"] == "task"), "")
    return {"final": text + (f" What I did: {str(done).rstrip('.')}." if done else "")}
