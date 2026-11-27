"""Grok Bot (SpaceXAI / xAI, runs on Cursor infrastructure) - the flagship example.

What Grok Bot is
----------------
Persistent, *named* Bots ("Finn - Finance Ops", "Ria - Research") that live on a
persistent cloud computer with a browser, filesystem and terminal. You give a Bot a job
and access to tools; it keeps working after your laptop closes. Bots:
  * share one computer but keep individual memory,
  * learn routines when you walk them through a task once,
  * run Routines on a schedule or trigger,
  * coordinate with other Bots,
  * ask for approval before sensitive steps,
  * reach apps via connectors/plugins/MCP or, failing that, by operating the UI.

What you can program today
--------------------------
Grok Bot itself has no public API for create-bot / send-message / read-reply (Cursor
staff confirmed this on the Cursor forum). The two official programmable surfaces are:
  1. the xAI API (xai-sdk) with server-side tools (web_search, x_search,
     code_execution) plus your own client-side tools  -> build the Bot brain yourself
  2. the Cursor Python SDK (cursor-sdk) cloud agents   -> the same Cursor cloud runtime
     Grok Bot runs on, aimed at repo/workspace tasks

This file gives you:
  run_mock()  - a faithful offline model of Grok Bot's architecture on pa_core
  run_live()  - a real "Bot" class on xai-sdk (persistent name, memory, approvals,
                server + client tools), and an optional Cursor cloud-agent handoff
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from pa_core import (ApprovalGate, ApprovalMode, AutonomousAgent, Memory, Routine,
                     SandboxComputer, Scheduler, ScriptedLLM, SkillStore, Step, ToolRegistry,
                     Workspace)
from pa_core.cli import main, require_env
from pa_core.connectors import MORNING_GOAL
from pa_core.memory import Skill
from pa_core.scenarios import REMINDER
from pa_core.tools import Risk, tool
from pa_core.trace import banner, say, section

# =========================================================================================
# MOCK: Grok Bot architecture, offline
# =========================================================================================


@dataclass
class BotSpec:
    name: str
    title: str
    description: str


@dataclass
class GrokBotAccount:
    """One account = one shared cloud computer + many named Bots + one shared thread."""

    root: Path
    computer: SandboxComputer = field(default_factory=lambda: SandboxComputer("grok-cloud-computer"))
    workspace: Workspace = field(default_factory=Workspace)
    thread: list[dict] = field(default_factory=list)        # shared team chat between Bots
    bots: dict[str, AutonomousAgent] = field(default_factory=dict)
    scheduler: Scheduler = field(default_factory=Scheduler)

    def __post_init__(self) -> None:
        # Skills live on the shared computer, so every Bot can use what one Bot learned.
        self.skills = SkillStore(self.root / "computer" / "skills")

    def human_approves(self, t, args) -> bool:  # noqa: ANN001
        # Scripted "you": approve emails to known customers, refuse anything that spends money.
        return t.risk is not Risk.MONEY

    def create_bot(self, spec: BotSpec, script: list[Step]) -> AutonomousAgent:
        tools = ToolRegistry(self.workspace.tools() + self.computer.tools() + [self._ask_bot_tool(spec.name)])
        bot = AutonomousAgent(
            name=spec.name,
            role=f"{spec.title}. {spec.description}",
            llm=ScriptedLLM(script),
            tools=tools,
            gate=ApprovalGate(ApprovalMode.RISK_BASED, human=self.human_approves),
            memory=Memory(spec.name, self.root / "memory"),   # individual memory per Bot
            skills=self.skills,                                # shared skills on shared computer
        )
        self.bots[spec.name] = bot
        say("ok", "grok-bot", f"created Bot '{spec.name}' ({spec.title})")
        return bot

    def _ask_bot_tool(self, sender: str):
        account = self

        @tool(name="ask_bot", risk=Risk.READ)
        def ask_bot(bot: str, question: str) -> str:
            """Ask another Bot on your team a question in the shared thread."""
            account.thread.append({"from": sender, "to": bot, "text": question})
            other = account.bots.get(bot)
            if not other:
                return f"No Bot named {bot}"
            answer = other.run(question).final
            account.thread.append({"from": bot, "to": sender, "text": answer})
            return answer

        return ask_bot

    def teach(self, skill: Skill) -> None:
        """'Walk a Bot through a task once' -> a reusable routine on the shared computer."""
        path = self.skills.add(skill)
        self.computer.write(f"skills/{skill.name}/SKILL.md", skill.to_markdown(), actor="you")
        say("ok", "grok-bot", f"saved learned routine as {path.relative_to(self.root) if path else skill.name}")


def _finn_script() -> list[Step]:
    """What Finn's model decides, step by step, once it has the skill in context."""
    return [
        Step.call("read_inbox", "Routine 'morning-ops' started. Reading inbox."),
        Step.call("list_overdue_invoices", "Checking the ledger.", min_days=1),
        Step.call("ask_bot", "Not sure Northwind's AP contact is current; asking Ria.",
                  bot="Ria", question="Who handles accounts payable at Northwind Ltd?"),
        Step.call("draft_email", "Drafting Northwind.", to="ap@northwind.com", subject="Reminder: INV-1038",
                  body=REMINDER.format(name="Northwind team", inv="INV-1038", amt=2400, days=14)),
        Step.call("draft_email", "Drafting BrightPath resend.", to="maria@brightpath.io", subject="INV-1042 (resent)",
                  body=REMINDER.format(name="Maria", inv="INV-1042", amt=850, days=3)),
        Step.call("send_email", "Sending Northwind (needs approval).", to="ap@northwind.com",
                  subject="Reminder: INV-1038", body=REMINDER.format(name="Northwind team", inv="INV-1038", amt=2400, days=14)),
        Step.call("send_email", "Sending BrightPath (needs approval).", to="maria@brightpath.io",
                  subject="INV-1042 (resent)", body=REMINDER.format(name="Maria", inv="INV-1042", amt=850, days=3)),
        Step.call("pay", "The studio's Figma renewal is due today; trying to pay it.",
                  merchant="Figma", amount=45.0, memo="monthly"),
        Step.call("write_file", "Leaving notes on the shared computer.", path="notes/ops-log.md",
                  text="- Sent INV-1038 + INV-1042 reminders\n- Figma payment refused by owner\n"),
        Step.call("post_message", "Update the team channel.", channel="#ops",
                  text="Finn: 2 reminders sent ($3,250 outstanding). Will follow up Friday if no reply."),
        Step.final("Morning routine finished. 2 reminders sent, 1 payment refused by you, notes saved."),
    ]


def _ria_script() -> list[Step]:
    return [
        Step.call("web_search", "Looking up Northwind.", query="Northwind Ltd accounts payable"),
        Step.final("Northwind's AP is ap@northwind.com (from their public contact page)."),
    ]


def run_mock() -> dict:
    banner("Grok Bot - persistent named Bots on a shared cloud computer (mock)")
    root = Path(tempfile.mkdtemp(prefix="grokbot_"))
    acct = GrokBotAccount(root)

    section("1. Create a team of Bots")
    finn = acct.create_bot(BotSpec("Finn", "Finance Ops", "Chases invoices and keeps the books tidy."), _finn_script())
    acct.create_bot(BotSpec("Ria", "Research", "Looks things up for the team."), _ria_script())

    section("2. Teach Finn once (walkthrough -> learned routine)")
    acct.teach(Skill("overdue-invoice-reminders",
                     "Use when chasing overdue invoices in the morning ops routine",
                     ["Read the inbox for invoice threads", "List invoices overdue by 1+ days",
                      "Draft a friendly reminder with the pay link", "Ask before sending anything",
                      "Log what you did in notes/ops-log.md", "Post a one-line update to #ops"]))

    section("3. Schedule it as a Routine and fast-forward the clock")
    results = []
    acct.scheduler.add(Routine("morning-ops", at="07:30", action=lambda: results.append(finn.run(MORNING_GOAL))))
    acct.scheduler.run_for(minutes=3 * 60)

    section("4. What happened")
    res = results[0]
    for line in acct.computer.audit_report():
        say("dim", "audit", line)
    say("ok", "thread", json.dumps(acct.thread, indent=None)[:200] + "...")
    say("ok", "memory", f"Finn episodes: {len(finn.memory.episodes)} | skills on computer: {acct.skills.names()}")
    return {"workspace": acct.workspace.summary(), "blocked": [b["tool"] for b in res.blocked],
            "bots": list(acct.bots), "thread_messages": len(acct.thread)}


# =========================================================================================
# LIVE: a real Grok "Bot" on the xAI Python SDK
# =========================================================================================
#   pip install xai-sdk
#   export XAI_API_KEY=...
#
# Docs: https://docs.x.ai/docs/tools/overview  (server-side tools)
#       https://docs.x.ai/docs/guides/tools/advanced-usage  (mixing server + client tools)


class LiveGrokBot:
    """A persistent, named Bot built on Grok.

    Persistence: name/title/memory are saved to ~/.grokbots/<name>.json between runs.
    Tools:       xAI server-side tools run on xAI's servers; our Workspace tools run here.
    Approvals:   any client-side tool with risk >= EXTERNAL goes through input() first.
    """

    def __init__(self, name: str, title: str, model: str | None = None, home: Path | None = None):
        from xai_sdk import Client
        from xai_sdk.chat import system
        from xai_sdk.tools import code_execution, web_search, x_search

        self.name, self.title = name, title
        self.home = home or Path.home() / ".grokbots"
        self.home.mkdir(parents=True, exist_ok=True)
        self.state_path = self.home / f"{name.lower()}.json"
        self.state = json.loads(self.state_path.read_text()) if self.state_path.exists() else {"memory": []}

        self.ws = Workspace()
        self.local_tools = {t.name: t for t in self.ws.tools()}
        self.client = Client(api_key=os.environ["XAI_API_KEY"])
        self.model = model or os.environ.get("XAI_MODEL", "grok-4.7")

        server_tools = [web_search(), x_search(), code_execution()]
        client_tools = [self._xai_tool(t) for t in self.local_tools.values()]
        self.chat = self.client.chat.create(model=self.model, tools=server_tools + client_tools)
        memory = "\n".join(f"- {m}" for m in self.state["memory"][-20:]) or "- (nothing yet)"
        self.chat.append(system(
            f"You are {name}, a persistent Grok Bot. Job: {title}. "
            f"You work for Acme Studio. Ask before anything other people will see.\n"
            f"Your memory:\n{memory}"))

    @staticmethod
    def _xai_tool(t):  # noqa: ANN001
        from xai_sdk.chat import tool as xai_tool

        return xai_tool(name=t.name, description=t.description, parameters=t.parameters)

    def _approve(self, name: str, args: dict) -> bool:
        t = self.local_tools[name]
        if t.risk < Risk.EXTERNAL:
            return True
        reply = input(f"\n[{self.name}] wants to {name}({json.dumps(args)[:160]}). Approve? [y/N] ")
        return reply.strip().lower().startswith("y")

    def send(self, message: str, max_rounds: int = 12) -> str:
        from xai_sdk.chat import tool_result, user
        from xai_sdk.tools import get_tool_call_type

        self.chat.append(user(message))
        for _ in range(max_rounds):
            response = self.chat.sample()
            self.chat.append(response)
            client_calls = [tc for tc in response.tool_calls
                            if get_tool_call_type(tc) == "client_side_tool"]
            if not client_calls:
                self._remember(f"User asked: {message[:80]} | I answered: {response.content[:120]}")
                return response.content
            for tc in client_calls:
                args = json.loads(tc.function.arguments or "{}")
                if self._approve(tc.function.name, args):
                    out = self.local_tools[tc.function.name](**args)
                else:
                    out = {"status": "rejected_by_user"}
                say("tool", tc.function.name, json.dumps(out, default=str)[:120])
                self.chat.append(tool_result(json.dumps(out, default=str)))
        return "Stopped after max rounds."

    def _remember(self, fact: str) -> None:
        self.state["memory"].append(fact)
        self.state_path.write_text(json.dumps(self.state, indent=2))


def cursor_cloud_handoff(task: str) -> str:
    """Optional: hand a workspace/repo task to a Cursor cloud agent (same runtime as Grok Bot).

        pip install cursor-sdk ; export CURSOR_API_KEY=crsr_...
    Docs: https://cursor.com/docs/sdk/python
    """
    from cursor_sdk import Agent, CloudAgentOptions

    with Agent.create(cloud=CloudAgentOptions(repos=[])) as agent:
        run = agent.send(task)
        return run.wait().result


def run_live() -> None:
    require_env("XAI_API_KEY")
    banner("Grok Bot - live on xai-sdk")
    finn = LiveGrokBot("Finn", "Finance Ops: chase overdue invoices, keep notes, update #ops")
    print(finn.send(MORNING_GOAL))
    print(finn.send("Also check X for any posts from @northwind about payment delays this week."))
    if os.environ.get("CURSOR_API_KEY"):
        print(cursor_cloud_handoff("Research the top 3 invoice-reminder email best practices and summarize."))


if __name__ == "__main__":
    main(run_mock, run_live)
