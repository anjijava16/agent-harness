"""LangChain Deep Agents: create_deep_agent + interrupt_on for approvals + a checkpointer."""

from __future__ import annotations

from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from . import lc_common
from .base import Outcome, RunCtx, Runtime

# Process-wide. In production use PostgresSaver/SqliteSaver so a paused run survives a restart.
CHECKPOINTER = MemorySaver()


class DeepAgentsRuntime(Runtime):
    name = "deepagents"

    async def start(self, ctx: RunCtx) -> Outcome:
        self.agent = create_deep_agent(
            model=lc_common.model(ctx),
            tools=lc_common.tools(ctx),
            system_prompt=ctx.prompt,
            interrupt_on={t: {"allowed_decisions": ["approve", "edit", "reject"]} for t in ctx.uc.gated},
            checkpointer=CHECKPOINTER,
        )
        self.cfg = {"configurable": {"thread_id": ctx.run_id}, "recursion_limit": 60}
        return self._outcome(await self.agent.ainvoke({"messages": [{"role": "user", "content": ctx.ask}]}, self.cfg))

    async def resume(self, ctx: RunCtx, decisions: list[dict]) -> Outcome:
        da = []
        for p, d in zip(self.pending, decisions, strict=True):
            if d["type"] == "approve":
                da.append({"type": "approve"})
            elif d["type"] == "reject":
                da.append({"type": "reject", "message": d.get("message", "The user declined.")})
            else:
                da.append({"type": "edit", "edited_action": {"name": p["tool"], "args": d["args"]}})
        return self._outcome(await self.agent.ainvoke(Command(resume={"decisions": da}), self.cfg))

    def _outcome(self, r: dict) -> Outcome:
        if r.get("__interrupt__"):
            req = r["__interrupt__"][0].value
            self.pending = [{"id": str(i), "tool": a["name"], "args": a["args"]} for i, a in enumerate(req["action_requests"])]
            return Outcome("paused", pending=self.pending)
        return Outcome("done", final=lc_common.final_text(r["messages"]))
