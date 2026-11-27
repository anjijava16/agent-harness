"""Hermes Agent (Nous Research, MIT, Feb 2026) - the agent that grows with you.

Architecture notes
------------------
* Terminal-native autonomous agent with persistent memory (~/.hermes), a messaging
  gateway, built-in cron with delivery to any platform, and sub-agents.
* Closed learning loop: after doing a task it creates or refines a *skill* (portable
  SKILL.md, agentskills.io format) so the next run is shorter and more reliable.
  It can also install skills from hubs (agentskills.io, ClawHub, LobeHub...), with
  quarantine/audit.
* Model-agnostic: Nous Portal, OpenRouter, OpenAI, or any custom endpoint
  (OPENAI_BASE_URL + OPENAI_API_KEY in ~/.hermes/.env).
* Research hooks: batch trajectory generation and RL environments (Atropos).

Mock = the learning loop: run 1 explores and writes a skill, run 2 uses the skill.
Live = same loop on any OpenAI-compatible model via pa_core. To use the real thing:
    curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash ; hermes
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from pa_core import (ApprovalGate, ApprovalMode, AutonomousAgent, Memory, ScriptedLLM, SkillStore,
                     Step, ToolRegistry, Workspace)
from pa_core.cli import main, require_env
from pa_core.llm import OpenAICompatLLM
from pa_core.scenarios import REMINDER
from pa_core.trace import banner, say, section

GOAL = "chase overdue invoices for acme"


def run_mock() -> dict:
    banner("Hermes Agent - closed learning loop: do, distil a skill, reuse (mock)")
    home = Path(tempfile.mkdtemp(prefix="hermes_"))
    skills = SkillStore(home / "skills")
    ws = Workspace()
    tools = ToolRegistry(ws.tools())
    gate = ApprovalGate(ApprovalMode.RISK_BASED, human=lambda t, a: True)

    section("Run 1: exploring (8 steps, a couple of dead ends)")
    explore = [
        Step.call("read_calendar", "Not sure where invoices live; checking calendar."),
        Step.call("read_inbox", "Inbox mentions Stripe."),
        Step.call("web_search", query="northwind ltd"),
        Step.call("list_overdue_invoices", min_days=1),
        Step.call("draft_email", to="ap@northwind.com", subject="INV-1038",
                  body=REMINDER.format(name="Northwind team", inv="INV-1038", amt=2400, days=14)),
        Step.call("draft_email", to="maria@brightpath.io", subject="INV-1042",
                  body=REMINDER.format(name="Maria", inv="INV-1042", amt=850, days=3)),
        Step.final("Drafted 2 reminders."),
    ]
    a1 = AutonomousAgent("Hermes", "Self-improving agent.", ScriptedLLM(explore), tools, gate=gate,
                         memory=Memory("hermes", home), skills=skills, learn_skills=True)
    r1 = a1.run(GOAL)
    say("ok", "hermes", f"skill file: {next((home / 'skills').glob('*/SKILL.md'))}")

    section("Run 2: same goal, the skill is in context, fewer steps")
    direct = [
        Step.call("list_overdue_invoices", "Skill says start with the ledger.", min_days=1),
        Step.call("draft_email", to="ap@northwind.com", subject="INV-1038",
                  body=REMINDER.format(name="Northwind team", inv="INV-1038", amt=2400, days=14)),
        Step.call("draft_email", to="maria@brightpath.io", subject="INV-1042",
                  body=REMINDER.format(name="Maria", inv="INV-1042", amt=850, days=3)),
        Step.final("Drafted 2 reminders using my skill."),
    ]
    a2 = AutonomousAgent("Hermes", "Self-improving agent.", ScriptedLLM(direct), tools, gate=gate,
                         memory=Memory("hermes", home), skills=SkillStore(home / "skills"), learn_skills=True)
    prompt = a2.system_prompt(GOAL)
    r2 = a2.run(GOAL)
    return {"run1_steps": len(r1.actions), "run2_steps": len(r2.actions), "learned": r1.learned_skill,
            "skill_in_prompt": "Use your skill" in prompt, "episodes": len(a2.memory.episodes)}


def run_live() -> None:
    require_env("PA_API_KEY")
    banner("Hermes-style learning loop - live model (e.g. OpenRouter)")
    home = Path.home() / ".pa_hermes"
    skills = SkillStore(home / "skills")
    agent = AutonomousAgent("Hermes", "Self-improving agent. Prefer known skills.", OpenAICompatLLM(),
                            ToolRegistry(Workspace().tools()),
                            gate=ApprovalGate(ApprovalMode.RISK_BASED,
                                              human=lambda t, a: input(f"{t.name}? [y/N] ").lower() == "y"),
                            memory=Memory("hermes", home), skills=skills, learn_skills=True)
    r = agent.run(GOAL)
    print(r.final, "| learned:", r.learned_skill, "| skills dir:", home / "skills")


if __name__ == "__main__":
    main(run_mock, run_live)
