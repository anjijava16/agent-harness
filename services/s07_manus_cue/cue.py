"""Cue by Manus (Sep 28 2026, with Manus 2.0) - agents with their own identity.

Architecture notes
------------------
Cue's distinguishing idea is *per-agent identity*. Each agent gets:
    email address   - sends and receives mail as itself, not as you
    phone number    - takes forwarded calls, writes a summary afterwards
    wallet          - its own virtual card, spending inside limits and permissions you set
    computer        - its own cloud workspace, keeps going after you log off
Several agents can join one group chat, split the work and hand off, while you steer
and make the final call. Connectors (Gmail, Calendar, Slack) and routines handle the
repetitive parts. Built on the same infrastructure as Manus.

Why identity matters: when an agent writes from its own address with its own card,
blast radius is bounded. A compromised agent can spend its wallet, not your card, and
it can't impersonate you in email.

Programmability
---------------
No separate public Cue API was documented at launch. The live mode sends the same
work to the Manus v2 API (see s11) with the identity rules written into the task.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pa_core import (ApprovalGate, ApprovalMode, AutonomousAgent, Budget, SandboxComputer,
                     ScriptedLLM, Step, ToolRegistry, Workspace)
from pa_core.cli import main, require_env
from pa_core.tools import Risk, tool
from pa_core.trace import banner, say, section


@dataclass
class Identity:
    email: str
    phone: str
    wallet: Budget
    computer: SandboxComputer
    inbox: list[dict] = field(default_factory=list)
    calls: list[dict] = field(default_factory=list)


def make_cue_agent(name: str, role: str, script: list[Step], wallet_limit: float, group: list[dict]) -> AutonomousAgent:
    ident = Identity(f"{name.lower()}@agents.cue.im", f"+1-415-555-01{len(group):02d}",
                     Budget(wallet_limit), SandboxComputer(f"{name}-computer"))

    @tool(risk=Risk.EXTERNAL)
    def send_as_agent(to: str, subject: str, body: str) -> dict:
        """Send email from the agent's OWN address (not the user's)."""
        msg = {"from": ident.email, "to": to, "subject": subject, "body": body}
        ident.inbox.append({"sent": msg})
        return {"status": "sent", "from": ident.email}

    @tool(risk=Risk.READ)
    def take_call(caller: str, transcript: str) -> dict:
        """Answer a forwarded call on the agent's number and summarize it."""
        summary = f"Call from {caller}: " + transcript[:80]
        ident.calls.append({"caller": caller, "summary": summary})
        return {"summary": summary}

    @tool(risk=Risk.MONEY)
    def pay_with_wallet(merchant: str, amount: float) -> dict:
        """Pay with the agent's own virtual card (bounded by its wallet limit)."""
        return {"status": "paid", "merchant": merchant, "amount": amount, "card": f"virtual-{name.lower()}"}

    @tool(risk=Risk.READ)
    def group_chat(text: str) -> str:
        """Post into the shared group chat with the user and the other agents."""
        group.append({"from": name, "text": text})
        say("agent", "group", f"{name}: {text}")
        return "posted"

    agent = AutonomousAgent(name, role, ScriptedLLM(script),
                            ToolRegistry([send_as_agent, take_call, pay_with_wallet, group_chat]),
                            gate=ApprovalGate(ApprovalMode.RISK_BASED, human=lambda t, a: True),
                            budget=ident.wallet)
    agent.identity = ident  # type: ignore[attr-defined]
    return agent


def run_mock() -> dict:
    banner("Cue - agents with their own email, phone, wallet and computer (mock)")
    group: list[dict] = []
    ws = Workspace()   # the user's world, which Cue agents do NOT touch directly

    collections = make_cue_agent("Cole", "Collections agent", [
        Step.call("take_call", "Northwind's AP called the agent line.", caller="+44 20 7946 0000",
                  transcript="This is Priya from Northwind AP, we'll pay INV-1038 on Friday, can you confirm the amount?"),
        Step.call("send_as_agent", "Confirming by email from my own address.", to="ap@northwind.com",
                  subject="INV-1038 confirmation", body="Confirming $2,400.00 due Friday. Thanks Priya!"),
        Step.call("group_chat", text="Northwind promised Friday. Confirmed in writing."),
        Step.final("Northwind confirmed for Friday."),
    ], wallet_limit=0.0, group=group)

    errands = make_cue_agent("Ezra", "Errands agent", [
        Step.call("group_chat", text="I'll book the courier to return Northwind's sample boards."),
        Step.call("pay_with_wallet", "Courier pickup.", merchant="CityCourier", amount=24.0),
        Step.call("pay_with_wallet", "Upgrade to same-day?", merchant="CityCourier", amount=40.0),
        Step.call("group_chat", text="Courier booked ($24). Same-day upgrade declined: wallet limit."),
        Step.final("Courier booked."),
    ], wallet_limit=50.0, group=group)

    section("1. Collections agent handles a call on its own number")
    collections.run("Handle Northwind collections")
    section("2. Errands agent pays from its own wallet (limit $50)")
    r = errands.run("Return the sample boards to Northwind")
    section("3. You only see the group chat")
    group.append({"from": "you", "text": "Great, thanks both."})
    return {"group_messages": len(group), "cole_email": collections.identity.email,  # type: ignore[attr-defined]
            "ezra_wallet_left": errands.budget.remaining(), "blocked": [b["reason"] for b in r.blocked],
            "user_workspace_untouched": ws.summary()["sent"] == 0}


def run_live() -> None:
    require_env("MANUS_API_KEY")
    from services.s11_manus.manus import ManusClient

    banner("Cue-style task via the Manus v2 API")
    c = ManusClient()
    t = c.create_task(
        "You are 'Cole', a collections agent. Rules: act only from your own identity, never from mine; "
        "spend nothing; ask me before contacting anyone. Task: draft a confirmation email to a customer who "
        "promised to pay invoice INV-1038 ($2,400) on Friday. Return the draft only.")
    print(c.wait(t["task_id"]))


if __name__ == "__main__":
    main(run_mock, run_live)
