"""Google Agent Development Kit (pip install google-adk) - multi-agent systems on Gemini.

Core pieces
-----------
    Agent / LlmAgent      model + instruction + tools (+ sub_agents for delegation)
    SequentialAgent,      workflow agents that run sub-agents in order / in parallel /
    ParallelAgent,        in a loop, without an LLM deciding the control flow
    LoopAgent
    Runner                the entry point; binds an agent to session/memory/artifact services
                          and yields a stream of Events from run_async(...)
    SessionService        InMemorySessionService (dev), DatabaseSessionService,
                          VertexAiSessionService (Agent Engine)
    session.state         shared scratchpad; an agent's output_key writes its answer there
    callbacks             before/after_model_callback, before/after_tool_callback
                          (approvals, guardrails, caching)
    deploy                `adk web` locally, Cloud Run, or Vertex AI Agent Engine (AdkApp)

This example builds a coordinator that delegates to a finance agent and a comms agent,
with a SequentialAgent pipeline variant and a before_tool_callback approval.
"""

from __future__ import annotations

import asyncio
import os

from pa_core import (ApprovalGate, ApprovalMode, AutonomousAgent, ScriptedLLM, Step, ToolRegistry,
                     Workspace)
from pa_core.cli import main
from pa_core.scenarios import REMINDER
from pa_core.trace import banner, say, section


def run_mock() -> dict:
    banner("Google ADK concepts - coordinator, sub_agents, session.state, callbacks (mock)")
    ws = Workspace()
    tools = {t.name: t for t in ws.tools()}
    state: dict = {}

    section("SequentialAgent: finance_agent -> comms_agent, passing data via session.state")
    finance = AutonomousAgent("finance_agent", "Finds overdue invoices.", ScriptedLLM([
        Step.call("list_overdue_invoices", min_days=1),
        Step.final("INV-1038 ap@northwind.com 2400 14; INV-1042 maria@brightpath.io 850 3")]),
        ToolRegistry([tools["list_overdue_invoices"]]))
    state["overdue"] = finance.run("find overdue").final     # output_key="overdue"
    say("dim", "state", f"session.state['overdue'] = {state['overdue']}")

    comms = AutonomousAgent("comms_agent", "Sends reminders. Instruction uses {overdue}.", ScriptedLLM([
        Step.call("send_email", to="ap@northwind.com", subject="INV-1038",
                  body=REMINDER.format(name="Northwind team", inv="INV-1038", amt=2400, days=14)),
        Step.call("send_email", to="maria@brightpath.io", subject="INV-1042",
                  body=REMINDER.format(name="Maria", inv="INV-1042", amt=850, days=3)),
        Step.final("Sent what you approved.")]),
        ToolRegistry([tools["send_email"]]),
        # before_tool_callback: approve Northwind, skip BrightPath (only 3 days late)
        gate=ApprovalGate(ApprovalMode.RISK_BASED, human=lambda t, a: "northwind" in a["to"]))
    r = comms.run(f"Send reminders for: {state['overdue']}")
    return {"state_keys": list(state), "workspace": ws.summary(), "skipped": [b["args"]["to"] for b in r.blocked]}


def run_live() -> None:
    """export GOOGLE_API_KEY=...  (or GOOGLE_GENAI_USE_VERTEXAI=TRUE + project/location)"""
    asyncio.run(_live())


async def _live() -> None:
    from google.adk.agents import Agent, SequentialAgent
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types

    ws = Workspace()
    T = {t.name: t for t in ws.tools()}
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

    def list_overdue_invoices(min_days: int) -> list:
        """List open invoices overdue by at least min_days."""
        return T["list_overdue_invoices"](min_days=min_days)

    def send_email(to: str, subject: str, body: str) -> dict:
        """Send an email to a customer."""
        return T["send_email"](to=to, subject=subject, body=body)

    def approve(tool, args, tool_context):  # noqa: ANN001, ARG001
        if tool.name == "send_email" and not input(f"\nsend to {args.get('to')}? [y/N] ").lower().startswith("y"):
            return {"status": "skipped_by_user"}
        return None

    finance = Agent(name="finance_agent", model=model, output_key="overdue",
                    instruction="Call list_overdue_invoices(min_days=1) and return a compact list.",
                    tools=[list_overdue_invoices])
    comms = Agent(name="comms_agent", model=model,
                  instruction="For each invoice in {overdue}, send a short friendly reminder with the pay link "
                              "https://pay.acme.studio/<invoice id>.",
                  tools=[send_email], before_tool_callback=approve)
    pipeline = SequentialAgent(name="collections_pipeline", sub_agents=[finance, comms])

    sessions = InMemorySessionService()
    runner = Runner(app_name="adk_collections", agent=pipeline, session_service=sessions)
    s = await sessions.create_session(app_name="adk_collections", user_id="me")
    banner("Google ADK - live SequentialAgent")
    msg = types.Content(role="user", parts=[types.Part(text="Run collections.")])
    async for ev in runner.run_async(user_id="me", session_id=s.id, new_message=msg):
        if ev.content and ev.content.parts and ev.content.parts[0].text:
            print(f"[{ev.author}] {ev.content.parts[0].text}")
    print("workspace:", ws.summary())


if __name__ == "__main__":
    main(run_mock, run_live)
