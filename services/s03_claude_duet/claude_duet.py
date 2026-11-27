"""Claude Duet (Anthropic, research preview Oct 21 2026).

Architecture notes
------------------
* A Claude you message like a person; it *messages you first* when something needs you.
* Each morning it sends a short brief on the most important items across connected apps.
* No continuous monitoring: it checks connected accounts every few hours, which keeps
  usage inside subscription limits. Background work counts against the same limits.
* Uses the same memories, skills and connectors as regular Claude, can search past
  chats, runs on a cloud computer after the app closes.
* Integrations called out at launch: Stripe (unpaid invoices -> drafted reminders),
  Link / Shop Pay (purchases with approval).
* Built on Anthropic's trustworthy-agents framework (same as Claude Code / Claude in Chrome).

Programmability
---------------
Duet has no public API. Its building blocks are public though: the Claude Agent SDK
(pip install claude-agent-sdk) gives you the same agent loop, in-process MCP tools,
permission callbacks and hooks. The live mode below rebuilds the "check every few
hours -> triage -> morning brief -> act with approval" pattern on it.
"""

from __future__ import annotations

import asyncio
import json

from pa_core import (ApprovalGate, ApprovalMode, AutonomousAgent, Routine, Scheduler,
                     ScriptedLLM, Step, ToolRegistry, Workspace)
from pa_core.cli import main, require_env
from pa_core.scenarios import REMINDER
from pa_core.trace import banner, say, section

# ---------------------------------------------------------------------------------------
# mock
# ---------------------------------------------------------------------------------------


def run_mock() -> dict:
    banner("Claude Duet - periodic checks, morning brief, act on approval (mock)")
    ws = Workspace()
    tools = ToolRegistry(ws.tools())
    attention: list[str] = []
    briefs: list[str] = []

    def check() -> None:
        """A cheap periodic check: read-only, collects 'needs attention' items."""
        overdue = tools.get("list_overdue_invoices")(min_days=1)
        unread = tools.get("read_inbox")()
        for inv in overdue:
            item = f"{inv['id']} {inv['customer']} ${inv['amount']:,.0f} ({inv['days_overdue']}d overdue)"
            if item not in attention:
                attention.append(item)
        for m in unread:
            if "invoice" in m["subject"].lower() and m["from"] not in str(attention):
                attention.append(f"{m['from']} replied about an invoice")

    def morning_brief() -> None:
        text = "Good morning. Needs you today:\n" + "\n".join(f"  - {a}" for a in attention)
        text += "\nI drafted reminders for both invoices. Reply 'send' and I'll send them."
        briefs.append(text)
        say("agent", "Duet", text)

    section("1. Heartbeat every 3 hours + 07:00 morning brief")
    sch = Scheduler()
    sch.add(Routine("check-connected-apps", every_minutes=180, action=check))
    sch.add(Routine("morning-brief", at="07:00", action=morning_brief))
    sch.run_for(minutes=4 * 60, step=30)

    section("2. You reply 'send' -> Duet acts, asking before anything external")
    act = [
        Step.call("draft_email", to="ap@northwind.com", subject="Reminder: INV-1038",
                  body=REMINDER.format(name="Northwind team", inv="INV-1038", amt=2400, days=14)),
        Step.call("send_email", to="ap@northwind.com", subject="Reminder: INV-1038",
                  body=REMINDER.format(name="Northwind team", inv="INV-1038", amt=2400, days=14)),
        Step.call("draft_email", to="maria@brightpath.io", subject="INV-1042 (resent)",
                  body=REMINDER.format(name="Maria", inv="INV-1042", amt=850, days=3)),
        Step.call("send_email", to="maria@brightpath.io", subject="INV-1042 (resent)",
                  body=REMINDER.format(name="Maria", inv="INV-1042", amt=850, days=3)),
        Step.final("Both reminders are out. I'll check again this afternoon and tell you if either pays."),
    ]
    duet = AutonomousAgent("Duet", "A proactive Claude that works alongside you.", ScriptedLLM(act), tools,
                           gate=ApprovalGate(ApprovalMode.RISK_BASED, human=lambda t, a: True))
    r = duet.run("User replied 'send' to the morning brief.")
    return {"checks": sch.routines[0].runs, "briefs": len(briefs), "attention_items": len(attention),
            "workspace": ws.summary(), "final": r.final[:40]}


# ---------------------------------------------------------------------------------------
# live: Claude Agent SDK
# ---------------------------------------------------------------------------------------
#   pip install claude-agent-sdk ; export ANTHROPIC_API_KEY=...
#   (the SDK drives the Claude Code runtime; install it per the SDK README if needed)


def run_live() -> None:
    require_env("ANTHROPIC_API_KEY")
    asyncio.run(_live())


async def _live() -> None:
    from claude_agent_sdk import (AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient,
                                  PermissionResultAllow, PermissionResultDeny, ResultMessage,
                                  TextBlock, create_sdk_mcp_server, tool)

    ws = Workspace()
    T = {t.name: t for t in ws.tools()}

    def wrap(result: object) -> dict:
        return {"content": [{"type": "text", "text": json.dumps(result, default=str)}]}

    @tool("list_overdue_invoices", "List open invoices overdue by at least min_days", {"min_days": int})
    async def list_overdue(args):  # noqa: ANN001
        return wrap(T["list_overdue_invoices"](min_days=args.get("min_days", 1)))

    @tool("read_inbox", "List unread inbox messages", {})
    async def read_inbox(args):  # noqa: ANN001, ARG001
        return wrap(T["read_inbox"]())

    @tool("draft_email", "Save an email draft", {"to": str, "subject": str, "body": str})
    async def draft_email(args):  # noqa: ANN001
        return wrap(T["draft_email"](**args))

    @tool("send_email", "Send an email (other people will see it)", {"to": str, "subject": str, "body": str})
    async def send_email(args):  # noqa: ANN001
        return wrap(T["send_email"](**args))

    server = create_sdk_mcp_server(name="acme", version="1.0.0",
                                   tools=[list_overdue, read_inbox, draft_email, send_email])

    # Duet-style permission model: reads/drafts are fine, anything external asks you.
    async def can_use_tool(tool_name, input_data, context):  # noqa: ANN001, ARG001
        if tool_name.endswith("send_email"):
            ok = input(f"\n[Duet] send to {input_data.get('to')}: {input_data.get('subject')}? [y/N] ")
            if not ok.strip().lower().startswith("y"):
                return PermissionResultDeny(message="User declined")
        return PermissionResultAllow()

    options = ClaudeAgentOptions(
        system_prompt=("You are Duet, a proactive assistant. When you check in, lead with what needs the "
                       "user's attention, keep it short, and prepare work so they only have to say yes."),
        mcp_servers={"acme": server},
        allowed_tools=["mcp__acme__list_overdue_invoices", "mcp__acme__read_inbox", "mcp__acme__draft_email"],
        can_use_tool=can_use_tool,
        max_turns=12,
    )

    banner("Claude Duet - live build-alike on the Claude Agent SDK")
    async with ClaudeSDKClient(options=options) as client:
        for prompt in ["Do your periodic check and write me a 4-line morning brief. Draft reminders for "
                       "anything overdue.", "send"]:
            await client.query(prompt)
            async for msg in client.receive_response():
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, TextBlock):
                            print(block.text)
                elif isinstance(msg, ResultMessage):
                    say("dim", "duet", f"turn cost: {getattr(msg, 'total_cost_usd', None)}")


if __name__ == "__main__":
    main(run_mock, run_live)
