"""The shared tool layer. Every runtime calls tools through here, so guards, caching and
recording behave the same whichever framework the user picked."""

from __future__ import annotations

import json

from sqlalchemy import select

from . import cache, db
from .spec import UseCase


class ToolRuntime:
    def __init__(self, run_id: str, user_id: str, uc: UseCase, prefs: dict):
        self.run_id, self.user_id, self.uc, self.prefs = run_id, user_id, uc, prefs
        self.decided: dict[str, int] = {}   # tool -> gated calls decided so far (for scripted decisions)

    def invoke(self, name: str, args: dict):  # noqa: ANN201
        t = self.uc.tool(name)
        guard = self.uc.guards.get(name)
        reason = guard(args, self.prefs) if guard else None
        if reason:
            self._record(name, args, None, t.effect, "blocked", reason)
            return {"blocked": True, "reason": reason}
        if name == "remember":
            result = self._remember(args["key"], args["value"])
        elif name == "recall":
            result = self._recall(args.get("topic", ""))
        elif t.effect == "read":
            hit = cache.cache_get(name, args)
            if hit is not None:
                self._record(name, args, hit, t.effect, "cached")
                return hit
            result = t.compute(args)
            cache.cache_set(name, args, result)
        else:
            result = t.compute(args)
        self._record(name, args, result, t.effect, "ok")
        return result

    def invoke_json(self, name: str, args: dict) -> str:
        return json.dumps(self.invoke(name, args), default=str)

    def rejected(self, name: str, args: dict, note: str = "") -> None:
        self._record(name, args, None, self.uc.tool(name).effect, "rejected", note)

    # ---- long-term memory, stored in the database ----
    def _remember(self, key: str, value: str) -> dict:
        with db.session() as s:
            row = s.get(db.Memory, (self.user_id, key))
            if row is None:
                s.add(db.Memory(user_id=self.user_id, key=key, value=value))
            else:
                row.value = value
        return {"saved": key}

    def _recall(self, topic: str) -> dict:
        with db.session() as s:
            rows = s.scalars(select(db.Memory).where(db.Memory.user_id == self.user_id)).all()
        t = topic.lower().strip()
        return {r.key: r.value for r in rows if not t or t in r.key.lower() or t in r.value.lower()}

    def _record(self, tool: str, args: dict, result, effect: str, status: str, note: str = "") -> None:  # noqa: ANN001
        with db.session() as s:
            s.add(db.ToolCall(run_id=self.run_id, tool=tool, args=args, result=result, effect=effect, status=status, note=note))
        db.add_event(self.run_id, "tool", {"tool": tool, "status": status, "args": args})
