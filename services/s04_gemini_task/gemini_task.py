"""Gemini Task (Google; launched as Gemini Spark in May 2026, renamed Task / "Tasks in Gemini").

Architecture notes
------------------
Three primitives, straight from Google's product pages:
  * Tasks     - "Help me find and track interior design internships..."
  * Schedules - "Every Monday at 9:00 AM, scan my inbox and give me a recap..."
  * Skills    - "Read my last 50 emails, turn them into a style guide, call that
                 skill 'ghostwriter' whenever I ask you to draft email."
It works in the background (even with your devices off), connects to Workspace
(Gmail, Calendar, Docs, Sheets, Slides, Keep, Tasks), browses with Chrome auto browse
or a *remote browser*, asks before browsing, and stops for you to take over at sign-in
pages or when sensitive info is needed. In the UI it is now a Chat | Task toggle.

Programmability
---------------
No public Gemini Task API. The Google-native way to build the same thing is the
Agent Development Kit (google-adk) + Gemini, which the live mode uses, including ADK's
before_tool_callback as the approval hook.
"""

from __future__ import annotations

import asyncio
import os

from pa_core import (ApprovalGate, ApprovalMode, AutonomousAgent, Routine, SandboxComputer,
                     Scheduler, ScriptedLLM, SkillStore, Step, ToolRegistry, Workspace)
from pa_core.cli import main, require_env
from pa_core.memory import Skill
from pa_core.scenarios import REMINDER
from pa_core.tools import Risk, tool
from pa_core.trace import banner, say, section

# ---------------------------------------------------------------------------------------
# mock
# ---------------------------------------------------------------------------------------


def run_mock() -> dict:
    banner("Gemini Task - Tasks, Schedules, Skills, take-over at sign-in (mock)")
    ws, pc = Workspace(), SandboxComputer("remote-browser")
    skills = SkillStore()
    handoffs: list[str] = []

    @tool(risk=Risk.READ)
    def take_over(reason: str) -> str:
        """Pause and ask the user to take control of the browser (sign-in, payment details)."""
        handoffs.append(reason)
        say("warn", "Gemini", f"Your turn: {reason}. I'll continue when you're done.")
        return "user completed the step"

    tools = ToolRegistry(ws.tools() + pc.tools() + [take_over])

    section("1. Skill: build 'ghostwriter' from your sent mail")
    skills.add(Skill("ghostwriter", "Use whenever drafting email in the user's voice",
                     ["Open with first name, no 'Dear'", "Two short paragraphs max",
                      "Sign off '- Acme Studio'", "Always include a concrete next step"]))
    say("ok", "Gemini", f"skills: {skills.names()}")

    section("2. Task: chase invoices, including one portal that needs sign-in")
    script = [
        Step.call("list_overdue_invoices", "Finding overdue invoices.", min_days=1),
        Step.call("draft_email", "Drafting with ghostwriter.", to="ap@northwind.com", subject="INV-1038",
                  body=REMINDER.format(name="Northwind team", inv="INV-1038", amt=2400, days=14)),
        Step.call("open_url", "Northwind wants invoices uploaded to their supplier portal.",
                  url="https://example.com/login"),
        Step.call("take_over", reason="Sign in to the Northwind supplier portal"),
        Step.call("send_email", "Sending the email copy too.", to="ap@northwind.com", subject="INV-1038",
                  body=REMINDER.format(name="Northwind team", inv="INV-1038", amt=2400, days=14)),
        Step.final("Uploaded to the portal after your sign-in and emailed AP."),
    ]
    agent = AutonomousAgent("Gemini", "Task mode.", ScriptedLLM(script), tools,
                            gate=ApprovalGate(ApprovalMode.RISK_BASED, human=lambda t, a: True), skills=skills)
    agent.run("Chase overdue invoices and draft email in my voice")

    section("3. Schedule: every Monday 09:00 inbox recap")
    recaps = []
    sch = Scheduler()
    sch.clock.minute = 8 * 60 + 30
    sch.add(Routine("monday-recap", at="09:00",
                    action=lambda: recaps.append(f"{len(tools.get('read_inbox')())} unread emails this week")))
    sch.run_for(60)
    return {"skills": skills.names(), "handoffs": handoffs, "workspace": ws.summary(),
            "recaps": recaps, "skill_in_prompt": "ghostwriter" in agent.system_prompt("draft email")}


# ---------------------------------------------------------------------------------------
# live: Google ADK + Gemini
# ---------------------------------------------------------------------------------------
#   pip install google-adk ; export GOOGLE_API_KEY=...   (or Vertex: GOOGLE_GENAI_USE_VERTEXAI=TRUE)


def run_live() -> None:
    if not os.environ.get("GOOGLE_GENAI_USE_VERTEXAI"):
        require_env("GOOGLE_API_KEY")
    asyncio.run(_live())


async def _live() -> None:
    from google.adk.agents import Agent
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types

    ws = Workspace()
    T = {t.name: t for t in ws.tools()}

    # ADK turns plain functions (with docstrings + type hints) into tools.
    def list_overdue_invoices(min_days: int) -> list:
        """List open invoices overdue by at least min_days."""
        return T["list_overdue_invoices"](min_days=min_days)

    def draft_email(to: str, subject: str, body: str) -> dict:
        """Save an email draft in the user's voice."""
        return T["draft_email"](to=to, subject=subject, body=body)

    def send_email(to: str, subject: str, body: str) -> dict:
        """Send an email. The user is asked first."""
        return T["send_email"](to=to, subject=subject, body=body)

    # Gemini Task "checks with you before taking major actions" -> ADK before_tool_callback.
    def confirm_major_actions(tool, args, tool_context):  # noqa: ANN001, ARG001
        if tool.name == "send_email":
            ok = input(f"\n[Gemini] send '{args.get('subject')}' to {args.get('to')}? [y/N] ")
            if not ok.strip().lower().startswith("y"):
                return {"status": "user_declined"}   # returning a dict skips the real tool
        return None

    ghostwriter = ("Ghostwriter skill: open with first name, two short paragraphs max, "
                   "sign off '- Acme Studio', always include a concrete next step.")
    agent = Agent(
        name="gemini_task",
        model=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
        instruction="You are Gemini in Task mode. Work through the task end to end. " + ghostwriter,
        tools=[list_overdue_invoices, draft_email, send_email],
        before_tool_callback=confirm_major_actions,
    )
    sessions = InMemorySessionService()
    runner = Runner(app_name="gemini_task_demo", agent=agent, session_service=sessions)
    session = await sessions.create_session(app_name="gemini_task_demo", user_id="me")

    banner("Gemini Task - live build-alike on Google ADK")
    msg = types.Content(role="user", parts=[types.Part(text="Chase my overdue invoices.")])
    async for event in runner.run_async(user_id="me", session_id=session.id, new_message=msg):
        if event.is_final_response() and event.content and event.content.parts:
            print(event.content.parts[0].text)


if __name__ == "__main__":
    main(run_mock, run_live)
