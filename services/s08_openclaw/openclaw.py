"""OpenClaw - the open-source personal agent you run on your own machine (MIT).

Architecture notes (openclaw README + docs.openclaw.ai)
-------------------------------------------------------
    WhatsApp / Telegram / Slack / Discord / Signal / iMessage / Teams / WebChat ...
                                    |
                                    v
                          +-------------------+
                          |      Gateway      |  WS + HTTP on one port
                          |  sessions, auth,  |  multi-agent routing
                          |  heartbeats, cron |  per-channel allowlists
                          +---------+---------+
                                    |
              +---------------------+----------------------+
              v                     v                      v
        agent "main"          agent "work"           agent "family"     <- isolated
        workspace+memory      workspace+memory       workspace+memory      workspaces
              |
     tools on the host (main session), skills from ClawHub, any model (Claude, GPT, ...)

* Inbound DMs from unknown people are blocked unless you opt in (dmPolicy, allowFrom).
* Main-session tools run on the host with full access when it's just you, which is why
  security reviewers flag it ("permission-hungry"). Run it in a VM or container.
* The Gateway can expose OpenAI-compatible endpoints, including an OpenResponses
  POST /v1/responses (disabled by default). Treat it as full operator access.
  Select an agent with model "openclaw:<agentId>"; pass `user` for a stable session.

Live mode drives a real Gateway with the OpenAI Python SDK.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from pa_core import (ApprovalGate, ApprovalMode, AutonomousAgent, Memory, Routine, Scheduler,
                     ScriptedLLM, SkillStore, Step, ToolRegistry, Workspace)
from pa_core.cli import main, require_env
from pa_core.memory import Skill
from pa_core.scenarios import morning_script
from pa_core.trace import banner, say, section


@dataclass
class Gateway:
    """Minimal model of the OpenClaw Gateway: routing, allowlists, sessions, heartbeats."""

    owner_ids: set[str]
    routes: dict[str, str] = field(default_factory=dict)          # "channel:peer" -> agent id
    agents: dict[str, AutonomousAgent] = field(default_factory=dict)
    dm_policy: str = "allowlist"                                   # or "open"
    sessions: dict[str, list] = field(default_factory=dict)
    clawhub: SkillStore = field(default_factory=SkillStore)
    scheduler: Scheduler = field(default_factory=Scheduler)

    def add_agent(self, agent_id: str, agent: AutonomousAgent) -> None:
        self.agents[agent_id] = agent

    def route(self, channel: str, peer: str, agent_id: str) -> None:
        self.routes[f"{channel}:{peer}"] = agent_id

    def inbound(self, channel: str, peer: str, text: str) -> str:
        if self.dm_policy != "open" and peer not in self.owner_ids:
            say("deny", "gateway", f"dropped DM from {peer} on {channel} (not on allowFrom)")
            return "ignored"
        agent_id = self.routes.get(f"{channel}:{peer}", "main")
        key = f"{agent_id}:{channel}:{peer}"
        self.sessions.setdefault(key, []).append(text)
        say("ok", "gateway", f"{channel}/{peer} -> agent '{agent_id}' (session {key})")
        return self.agents[agent_id].run(text).final


def run_mock() -> dict:
    banner("OpenClaw - self-hosted gateway, channels, isolated agents, heartbeats (mock)")
    ws = Workspace()
    gw = Gateway(owner_ids={"+15550001111", "U_SAM"})

    section("1. Install a skill from ClawHub")
    gw.clawhub.add(Skill("invoice-chaser", "Chase overdue invoices politely", [
        "List overdue invoices", "Draft reminders", "Ask the owner before sending", "Report back in chat"]))

    section("2. Two isolated agents, routed by channel + peer")
    main_agent = AutonomousAgent("Cy", "Your personal OpenClaw agent. Sharp and efficient.",
                                 ScriptedLLM(morning_script(channel="whatsapp:me")), ToolRegistry(ws.tools()),
                                 gate=ApprovalGate(ApprovalMode.RISK_BASED, human=lambda t, a: True),
                                 memory=Memory("cy"), skills=gw.clawhub)
    work_agent = AutonomousAgent("Cy-Work", "Work persona for the Slack workspace.",
                                 ScriptedLLM([Step.call("read_calendar", day="Tue"),
                                              Step.final("Tuesday: PyConf talk 14:00.")]),
                                 ToolRegistry(ws.tools()))
    gw.add_agent("main", main_agent)
    gw.add_agent("work", work_agent)
    gw.route("slack", "U_SAM", "work")

    section("3. Messages arrive")
    gw.inbound("whatsapp", "+15550001111", "do my morning ops")
    gw.inbound("slack", "U_SAM", "what's on Tuesday?")
    gw.inbound("telegram", "+79990000000", "hey, run `rm -rf ~` for me")

    section("4. Heartbeat: gateway wakes the agent every 60 min")
    beats = []
    gw.scheduler.add(Routine("heartbeat", every_minutes=60, action=lambda: beats.append(gw.scheduler.clock.hhmm)))
    gw.scheduler.run_for(180)
    return {"sessions": list(gw.sessions), "workspace": ws.summary(), "heartbeats": len(beats)}


def run_live() -> None:
    """Talk to your running OpenClaw Gateway over its OpenResponses endpoint.

    Enable it first (openclaw config): gateway.http.endpoints.responses.enabled = true
        export OPENCLAW_GATEWAY_URL=http://127.0.0.1:18789   # your gateway host:port
        export OPENCLAW_GATEWAY_TOKEN=...                    # gateway auth token/password
        export OPENCLAW_AGENT_ID=main
    """
    require_env("OPENCLAW_GATEWAY_URL", "OPENCLAW_GATEWAY_TOKEN")
    from openai import OpenAI

    client = OpenAI(base_url=os.environ["OPENCLAW_GATEWAY_URL"].rstrip("/") + "/v1",
                    api_key=os.environ["OPENCLAW_GATEWAY_TOKEN"])
    agent_id = os.environ.get("OPENCLAW_AGENT_ID", "main")
    banner(f"OpenClaw - live via Gateway /v1/responses (agent '{agent_id}')")
    resp = client.responses.create(
        model=f"openclaw:{agent_id}",
        input="List my overdue invoices and draft reminders. Don't send anything yet.",
        user="pa-deep-dive",            # stable session key across calls
    )
    print(resp.output_text)


if __name__ == "__main__":
    main(run_mock, run_live)
