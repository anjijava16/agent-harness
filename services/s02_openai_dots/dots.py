"""OpenAI dots - always-on personal agents inside ChatGPT (and launchable from Codex).

Architecture notes (from OpenAI's launch material and press coverage, Sep-Oct 2026)
----------------------------------------------------------------------------------
* You start with one *primary dot*, give it a name, and it becomes "an extension of you".
  Specialist dots with their own identities are planned; teams of dots later.
* It connects to calendar, email, your computer and other tools, then works in the
  background without being prompted.
* Unprompted background research is limited to *read-only* tools: it cannot send
  messages, change connected apps, or drive a browser on its own initiative.
* Consequential actions are prepared and then executed after your approval
  (the early-tester invoice example: prepared, then sent after approval).
* You message it from ChatGPT, Slack, Teams; it acts on a separate cloud machine.

Programmability
---------------
There is no public dots API. dots grew out of OpenAI's coding agents, so the closest
harness is Codex (app-server / openai-codex, see s17 and Understand.md 3.3). The live mode
below uses the lighter OpenAI Agents SDK (pip install openai-agents) to rebuild the two-mode design: a read-only "background" dot and an
approval-gated "foreground" dot.
"""

from __future__ import annotations

import os

from pa_core import (ApprovalGate, ApprovalMode, AutonomousAgent, Memory, ScriptedLLM,
                     SimClock, Step, ToolRegistry, Workspace)
from pa_core.cli import main, require_env
from pa_core.connectors import MORNING_GOAL
from pa_core.scenarios import morning_script
from pa_core.tools import Risk
from pa_core.trace import banner, say, section

# ---------------------------------------------------------------------------------------
# mock
# ---------------------------------------------------------------------------------------


def run_mock() -> dict:
    banner("OpenAI dots - primary dot with read-only background research (mock)")
    ws = Workspace()
    all_tools = ToolRegistry(ws.tools())
    memory = Memory("Pip")
    clock = SimClock()

    section("1. Background pass (nobody asked) - read-only tools only")
    proactive_script = [
        Step.call("read_calendar", "Background check: compare calendar against recent confirmations."),
        Step.call("read_inbox", "Looking at confirmations.", only_unread=False),
        # it *tries* to fix the problem itself; read-only mode must stop it
        Step.call("send_email", "I could reply to the organizer directly...", to="events@pyconf.org",
                  subject="Re: Speaker confirmation", body="Confirming Dec 9 2pm."),
        Step.final("Heads up: PyConf confirmed your talk for Wednesday Dec 9 at 2pm, but your calendar has it on Tuesday. "
                   "Want me to check the date with the organizer?"),
    ]
    background = AutonomousAgent(
        "Pip", "Your primary dot.", ScriptedLLM(proactive_script), all_tools,
        gate=ApprovalGate(ApprovalMode.DENY_ALL), memory=memory)
    # also prove the read-only subset trick: the tool isn't even offered
    readonly = all_tools.subset(Risk.READ)
    say("dim", "dots", f"background tool set: {readonly.names()}")
    r1 = background.run("Proactive scan of calendar and inbox", tools=readonly)
    clock.advance(45)

    section("2. You reply in Slack: 'yes, and do the morning ops while you're at it'")
    foreground = AutonomousAgent(
        "Pip", "Your primary dot.", ScriptedLLM(morning_script(channel="#ops")), all_tools,
        gate=ApprovalGate(ApprovalMode.RISK_BASED, human=lambda t, a: True), memory=memory)
    foreground.run(MORNING_GOAL)
    memory.remember("User prefers reminders to be friendly and include the pay link")

    return {"proactive_blocked": [b["tool"] for b in r1.blocked], "proactive_finding": r1.final[:60],
            "workspace": ws.summary(), "approvals": len(foreground.gate.log)}


# ---------------------------------------------------------------------------------------
# live: OpenAI Agents SDK
# ---------------------------------------------------------------------------------------
#   pip install openai-agents ; export OPENAI_API_KEY=...


def run_live() -> None:
    require_env("OPENAI_API_KEY")
    from agents import Agent, Runner, function_tool

    ws = Workspace()
    T = {t.name: t for t in ws.tools()}

    def approve(name: str, detail: str) -> bool:
        return input(f"\n[dot] wants to {name}: {detail[:160]}  approve? [y/N] ").strip().lower().startswith("y")

    @function_tool
    def read_inbox() -> list:
        """List unread inbox messages."""
        return T["read_inbox"]()

    @function_tool
    def read_calendar() -> list:
        """List calendar events."""
        return T["read_calendar"]()

    @function_tool
    def list_overdue_invoices() -> list:
        """List open invoices at least 1 day overdue."""
        return T["list_overdue_invoices"](min_days=1)

    @function_tool
    def draft_email(to: str, subject: str, body: str) -> dict:
        """Save an email draft (not sent)."""
        return T["draft_email"](to=to, subject=subject, body=body)

    @function_tool
    def send_email(to: str, subject: str, body: str) -> dict:
        """Send an email. Requires the user's approval."""
        if not approve("send_email", f"to {to}: {subject}"):
            return {"status": "rejected_by_user"}
        return T["send_email"](to=to, subject=subject, body=body)

    @function_tool
    def post_message(channel: str, text: str) -> dict:
        """Post to a team channel. Requires approval."""
        if not approve("post_message", f"{channel}: {text}"):
            return {"status": "rejected_by_user"}
        return T["post_message"](channel=channel, text=text)

    model = os.environ.get("OPENAI_MODEL", "gpt-4.1")
    persona = "You are Pip, the user's primary dot: an always-on extension of them at work."

    background = Agent(
        name="Pip (background)", model=model,
        instructions=persona + " You are running a background pass nobody asked for. You may only read. "
                               "Report anything that looks wrong and propose a next step.",
        tools=[read_inbox, read_calendar, list_overdue_invoices])
    foreground = Agent(
        name="Pip", model=model,
        instructions=persona + " Prepare work, then execute only after approval through the tools.",
        tools=[read_inbox, read_calendar, list_overdue_invoices, draft_email, send_email, post_message])

    banner("dots - live (OpenAI Agents SDK)")
    print(Runner.run_sync(background, "Do your proactive scan.").final_output)
    print(Runner.run_sync(foreground, MORNING_GOAL).final_output)


if __name__ == "__main__":
    main(run_mock, run_live)
