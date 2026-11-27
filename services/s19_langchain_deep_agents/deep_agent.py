"""LangChain Deep Agents (pip install deepagents) - an opinionated harness on LangGraph.

What you get from create_deep_agent(...)
----------------------------------------
* NOTE: since deepagents 0.7 the write_todos planner is NOT in the default harness; add it
  with middleware=[TodoListMiddleware()] (see frameworks/deep_agents/05_*). The mock below
  still models a todo tool, because it's a useful pattern.
* a virtual filesystem (ls/read_file/write_file/edit_file) as working memory,
  with pluggable backends: StateBackend (default), FilesystemBackend, StoreBackend,
  CompositeBackend(routes={"/memories/": ...}) for memory that survives threads
* sub-agents via the task tool: subagents=[{"name","description","system_prompt","tools","model"}]
* skills=["./skills/"] and memory=["./AGENTS.md"]
* human-in-the-loop: interrupt_on={"send_email": True} + a checkpointer; resume with
  Command(resume={"decisions": [{"type": "approve"}]})  (or "reject" / "edit")
* LangGraph runtime: durable execution, streaming, checkpoints, LangSmith tracing

Mock mirrors those pieces on pa_core; live is the real library.
"""

from __future__ import annotations

import os

from pa_core import (ApprovalGate, ApprovalMode, AutonomousAgent, SandboxComputer, ScriptedLLM, Step,
                     ToolRegistry, Workspace)
from pa_core.cli import main
from pa_core.scenarios import REMINDER
from pa_core.tools import Risk, tool
from pa_core.trace import banner, say, section


def run_mock() -> dict:
    banner("Deep Agents concepts - todos, virtual FS, subagent, interrupt_on (mock)")
    ws, fs = Workspace(), SandboxComputer("virtual-fs")
    todos: list[str] = []

    @tool(risk=Risk.READ)
    def write_todos(items: list) -> str:
        """Write or replace the todo list."""
        todos[:] = items
        for i in items:
            say("agent", "todo", f"[ ] {i}")
        return "ok"

    @tool(risk=Risk.READ)
    def task(subagent: str, instructions: str) -> str:
        """Delegate to a subagent with its own context window."""
        sub = AutonomousAgent(subagent, "researcher subagent", ScriptedLLM([
            Step.call("list_overdue_invoices", min_days=1), Step.final("2 overdue: INV-1038, INV-1042")]),
            ToolRegistry([t for t in ws.tools() if t.name == "list_overdue_invoices"]))
        return sub.run(instructions).final

    tools = ToolRegistry(ws.tools() + fs.tools() + [write_todos, task])
    script = [
        Step.call("write_todos", items=["research overdue", "draft reminders", "send (needs approval)", "save notes"]),
        Step.call("task", subagent="researcher", instructions="Find overdue invoices"),
        Step.call("draft_email", to="ap@northwind.com", subject="INV-1038",
                  body=REMINDER.format(name="Northwind team", inv="INV-1038", amt=2400, days=14)),
        Step.call("send_email", to="ap@northwind.com", subject="INV-1038",
                  body=REMINDER.format(name="Northwind team", inv="INV-1038", amt=2400, days=14)),
        Step.call("write_file", path="/memories/collections.md", text="Northwind reminded on day 14."),
        Step.final("Done. Notes in /memories/collections.md."),
    ]
    section("interrupt_on={'send_email': True} -> pauses for a decision")
    agent = AutonomousAgent("deep-agent", "Deep agent.", ScriptedLLM(script), tools,
                            gate=ApprovalGate(ApprovalMode.RISK_BASED, human=lambda t, a: True))
    r = agent.run("Chase overdue invoices")
    return {"todos": len(todos), "files": list(fs.files), "workspace": ws.summary(), "steps": len(r.actions)}


def run_live() -> None:
    """export ANTHROPIC_API_KEY=... (or set DEEP_MODEL=openai:gpt-4.1 / google_genai:gemini-2.5-flash)"""
    from deepagents import create_deep_agent
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.types import Command

    ws = Workspace()
    T = {t.name: t for t in ws.tools()}

    def list_overdue_invoices(min_days: int = 1) -> list:
        """List open invoices overdue by at least min_days."""
        return T["list_overdue_invoices"](min_days=min_days)

    def draft_email(to: str, subject: str, body: str) -> dict:
        """Save an email draft."""
        return T["draft_email"](to=to, subject=subject, body=body)

    def send_email(to: str, subject: str, body: str) -> dict:
        """Send an email to a customer."""
        return T["send_email"](to=to, subject=subject, body=body)

    agent = create_deep_agent(
        model=os.environ.get("DEEP_MODEL", "anthropic:claude-sonnet-4-6"),
        tools=[list_overdue_invoices, draft_email, send_email],
        system_prompt="You run collections for Acme Studio. Plan with todos, delegate research, keep notes in /memories/.",
        subagents=[{"name": "researcher", "description": "Finds overdue invoices",
                    "system_prompt": "Only research. Return a short list.", "tools": [list_overdue_invoices]}],
        interrupt_on={"send_email": {"allowed_decisions": ["approve", "reject"]}},
        checkpointer=MemorySaver(),
    )
    cfg = {"configurable": {"thread_id": "collections-1"}}
    banner("Deep Agents - live")
    result = agent.invoke({"messages": [{"role": "user", "content": "Chase my overdue invoices."}]}, config=cfg)
    while result.get("__interrupt__"):
        req = result["__interrupt__"][0].value
        decisions = []
        for action in req["action_requests"]:
            yes = input(f"\n{action['name']}({action['args']})? [y/N] ").lower().startswith("y")
            decisions.append({"type": "approve"} if yes else {"type": "reject", "message": "user declined"})
        result = agent.invoke(Command(resume={"decisions": decisions}), config=cfg)
    print(result["messages"][-1].content)
    print("workspace:", ws.summary())


if __name__ == "__main__":
    main(run_mock, run_live)
