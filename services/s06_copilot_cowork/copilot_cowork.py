"""Microsoft 365 Copilot Cowork (GA June 2026).

Architecture notes (Microsoft Learn + M365 blog)
------------------------------------------------
* You describe the outcome; Cowork grounds on your work context (Work IQ), plans, then
  executes across Microsoft 365, Dynamics 365 and Fabric: sends email, schedules
  meetings, creates documents, posts in Teams, manages your calendar.
* "You approve each action before it happens." That is the defining policy choice.
* Skills load during a session (the side panel shows which are active); plugins from the
  Microsoft 365 App Store add skills and connectors (Accounting, Finance, Capital Markets).
* Runs inside the Microsoft 365 trust boundary; IT admins control access; usage-based
  billing. At GA it ran on Anthropic models (Opus 4.8, Sonnet 4.6), GPT 5.5 in Frontier.

Programmability
---------------
Cowork has no public "run a Cowork task" API. Enterprise extension points are plugins,
Copilot Studio and Agent 365. Mock = the plan -> approve-every-action loop with
plugin-loaded skills. Live = the same loop on any OpenAI-compatible endpoint, which
includes Azure OpenAI / Azure AI Foundry (set PA_BASE_URL to your deployment).
"""

from __future__ import annotations

from pa_core import (ApprovalGate, ApprovalMode, AutonomousAgent, ScriptedLLM, SkillStore, Step,
                     ToolRegistry, Workspace)
from pa_core.cli import main, require_env
from pa_core.connectors import MORNING_GOAL
from pa_core.llm import OpenAICompatLLM
from pa_core.memory import Skill
from pa_core.scenarios import morning_script
from pa_core.tools import Risk, tool
from pa_core.trace import banner, say, section

TENANT_DOMAIN = "acme.studio"


class Plugin:
    def __init__(self, name: str, skills: list[Skill]):
        self.name, self.skills = name, skills


ACCOUNTING_PLUGIN = Plugin("Accounting for Cowork", [
    Skill("ar-collections", "Use for overdue invoices and accounts receivable collections",
          ["Pull open AR from the ledger", "Draft reminders using the approved template",
           "Never promise discounts", "Log outreach in the AR tracker"])])


def run_mock() -> dict:
    banner("Copilot Cowork - plan first, approve every action, plugin skills (mock)")
    ws = Workspace()
    skills = SkillStore()

    section("1. Install a plugin -> new skills appear in the side panel")
    for s in ACCOUNTING_PLUGIN.skills:
        skills.add(s)
    say("ok", "cowork", f"active skills: {skills.names()}")

    @tool(risk=Risk.READ)
    def show_plan(steps: list) -> str:
        """Show the user the plan before doing anything."""
        for i, s in enumerate(steps, 1):
            say("agent", "plan", f"{i}. {s}")
        return "plan shown"

    tools = ToolRegistry(ws.tools() + [show_plan])
    script = [Step.call("show_plan", "Here's what I'll do.", steps=[
        "Read inbox and AR", "Draft 2 reminders (ar-collections skill)", "Send both after you approve",
        "Block Tue 9-11 for focus", "Post a status in Teams #ops"])] + morning_script(channel="Teams:#ops")

    section("2. Execute - every non-read step asks you (you decline the BrightPath send)")
    decisions = iter([True, True, True, False, True, True])   # draft, draft, send, send, focus, post

    def you(t, a):  # noqa: ANN001
        return next(decisions, True)

    cowork = AutonomousAgent("Cowork", "Microsoft 365 Copilot Cowork.", ScriptedLLM(script), tools,
                             gate=ApprovalGate(ApprovalMode.EVERY, human=you), skills=skills)
    r = cowork.run(MORNING_GOAL)
    asks = sum(1 for e in cowork.gate.log if e["decision"] in ("approved", "rejected"))
    return {"approvals_asked": asks, "rejected": [b["tool"] for b in r.blocked], "workspace": ws.summary(),
            "skill_used": "ar-collections" in cowork.system_prompt("overdue invoices collections")}


def run_live() -> None:
    require_env("PA_API_KEY")
    banner("Cowork build-alike - live (works with Azure OpenAI via PA_BASE_URL)")
    ws = Workspace()
    human = lambda t, a: input(f"\n[Cowork] {t.name}({a})? [y/N] ").lower().startswith("y")  # noqa: E731
    agent = AutonomousAgent("Cowork", "Plan first, then do the work; every change needs approval.",
                            OpenAICompatLLM(), ToolRegistry(ws.tools()),
                            gate=ApprovalGate(ApprovalMode.EVERY, human=human))
    print(agent.run(MORNING_GOAL).final)


if __name__ == "__main__":
    main(run_mock, run_live)
