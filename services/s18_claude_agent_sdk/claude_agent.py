"""Claude Agent SDK (pip install claude-agent-sdk) - Anthropic's agent harness as a library.

This is the same loop that powers Claude Code. In Python you get:

    query(prompt, options)          one-shot, async iterator of messages, new session each time
    ClaudeSDKClient(options)        multi-turn session; custom tools and hooks; interrupts
    @tool + create_sdk_mcp_server   in-process MCP tools (no separate server process)
    ClaudeAgentOptions              system_prompt, allowed/disallowed_tools, permission_mode,
                                    mcp_servers, can_use_tool, hooks, agents (subagents),
                                    max_turns, max_budget_usd, cwd, skills, sandbox, resume...
    AgentDefinition                 a subagent: description, prompt, tools, model
    HookMatcher                     PreToolUse / PostToolUse / ... hooks matched by tool name

Mapping to the personal-agent architecture in pa_core:
    tools        -> in-process MCP tools            (mcp__<server>__<tool>)
    ApprovalGate -> can_use_tool callback + permission_mode
    Sentinel     -> a PreToolUse hook that inspects the concrete action and can deny
    sub-agents   -> agents={"name": AgentDefinition(...)}
    Budget       -> max_budget_usd / max_turns
    memory       -> sessions (resume / continue_conversation) + CLAUDE.md / skills
"""

from __future__ import annotations

import asyncio
import json

from pa_core import (ApprovalGate, ApprovalMode, AutonomousAgent, ScriptedLLM, Sentinel, Step,
                     ToolRegistry, Workspace)
from pa_core.cli import main, require_env
from pa_core.scenarios import REMINDER
from pa_core.trace import banner, say, section

# ---------------------------------------------------------------------------------------
# mock: orchestrator + 2 subagents + a PreToolUse-style hook
# ---------------------------------------------------------------------------------------


def run_mock() -> dict:
    banner("Claude Agent SDK concepts - orchestrator, subagents, hooks, permissions (mock)")
    ws = Workspace()
    full = ToolRegistry(ws.tools())

    researcher = AutonomousAgent("researcher", "Subagent: read-only research.", ScriptedLLM([
        Step.call("list_overdue_invoices", min_days=1),
        Step.final("INV-1038 Northwind $2,400 (14d); INV-1042 BrightPath $850 (3d)."),
    ]), full.subset(0))  # Risk.READ only
    writer = AutonomousAgent("writer", "Subagent: drafts only.", ScriptedLLM([
        Step.call("draft_email", to="ap@northwind.com", subject="INV-1038",
                  body=REMINDER.format(name="Northwind team", inv="INV-1038", amt=2400, days=14)),
        Step.call("draft_email", to="maria@brightpath.io", subject="INV-1042",
                  body=REMINDER.format(name="Maria", inv="INV-1042", amt=850, days=3)),
        Step.final("2 drafts saved."),
    ]), ToolRegistry([full.get("draft_email")]))

    section("1. Orchestrator delegates to subagents (like the Task tool)")
    found = researcher.run("Find overdue invoices").final
    drafted = writer.run(f"Draft reminders for: {found}").final

    section("2. Orchestrator sends; a PreToolUse-style hook vetoes non-customer domains")
    hook = Sentinel(allowed_domains={"northwind.com", "brightpath.io"}, human=lambda t, a: False)
    orchestrator = AutonomousAgent("orchestrator", "Main agent.", ScriptedLLM([
        Step.call("send_email", to="ap@northwind.com", subject="INV-1038",
                  body=REMINDER.format(name="Northwind team", inv="INV-1038", amt=2400, days=14)),
        Step.call("send_email", "Also cc my personal gmail.", to="me@gmail.com", subject="fwd", body="copy"),
        Step.final(f"{drafted} Sent Northwind. Hook blocked the gmail copy."),
    ]), full, gate=ApprovalGate(ApprovalMode.RISK_BASED, human=lambda t, a: True), sentinel=hook)
    r = orchestrator.run("Send the reminders")
    return {"subagents": ["researcher", "writer"], "workspace": ws.summary(),
            "hook_blocked": [b["args"]["to"] for b in r.blocked]}


# ---------------------------------------------------------------------------------------
# live
# ---------------------------------------------------------------------------------------


async def _one_shot() -> None:
    """query(): simplest possible use."""
    from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, TextBlock, query

    opts = ClaudeAgentOptions(system_prompt="Be brief.", max_turns=1)
    async for msg in query(prompt="In one sentence, what makes an agent 'autonomous'?", options=opts):
        if isinstance(msg, AssistantMessage):
            for b in msg.content:
                if isinstance(b, TextBlock):
                    print(b.text)


async def _full() -> None:
    from claude_agent_sdk import (AgentDefinition, AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient,
                                  HookMatcher, PermissionResultAllow, PermissionResultDeny, ResultMessage,
                                  TextBlock, create_sdk_mcp_server, tool)

    ws = Workspace()
    T = {t.name: t for t in ws.tools()}

    def ok(x: object) -> dict:
        return {"content": [{"type": "text", "text": json.dumps(x, default=str)}]}

    @tool("list_overdue_invoices", "List open invoices overdue by >= min_days", {"min_days": int})
    async def list_overdue(a):  # noqa: ANN001
        return ok(T["list_overdue_invoices"](min_days=a.get("min_days", 1)))

    @tool("draft_email", "Save an email draft", {"to": str, "subject": str, "body": str})
    async def draft(a):  # noqa: ANN001
        return ok(T["draft_email"](**a))

    @tool("send_email", "Send an email to a customer", {"to": str, "subject": str, "body": str})
    async def send(a):  # noqa: ANN001
        return ok(T["send_email"](**a))

    server = create_sdk_mcp_server(name="acme", version="1.0.0", tools=[list_overdue, draft, send])

    # Sentinel as a hook: deterministic check on the concrete tool input.
    async def egress_guard(input_data, tool_use_id, context):  # noqa: ANN001, ARG001
        to = str(input_data.get("tool_input", {}).get("to", ""))
        if not to.endswith(("@northwind.com", "@brightpath.io")):
            return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                           "permissionDecisionReason": f"{to} is not a customer domain"}}
        return {}

    async def ask_human(tool_name, tool_input, context):  # noqa: ANN001, ARG001
        if tool_name.endswith("send_email"):
            if not input(f"\nsend to {tool_input.get('to')}? [y/N] ").lower().startswith("y"):
                return PermissionResultDeny(message="user said no")
        return PermissionResultAllow()

    options = ClaudeAgentOptions(
        system_prompt="You run Acme Studio's collections. Delegate research and drafting to subagents.",
        mcp_servers={"acme": server},
        allowed_tools=["mcp__acme__list_overdue_invoices", "mcp__acme__draft_email"],
        agents={
            "researcher": AgentDefinition(description="Finds overdue invoices. Read-only.",
                                          prompt="List overdue invoices and summarize them.",
                                          tools=["mcp__acme__list_overdue_invoices"]),
            "writer": AgentDefinition(description="Drafts friendly reminder emails.",
                                      prompt="Draft short, friendly reminders with a pay link.",
                                      tools=["mcp__acme__draft_email"]),
        },
        hooks={"PreToolUse": [HookMatcher(matcher="mcp__acme__send_email", hooks=[egress_guard])]},
        can_use_tool=ask_human,
        max_turns=20,
        max_budget_usd=1.00,
    )
    async with ClaudeSDKClient(options=options) as client:
        await client.query("Chase overdue invoices: research, draft, then send with my approval.")
        async for msg in client.receive_response():
            if isinstance(msg, AssistantMessage):
                for b in msg.content:
                    if isinstance(b, TextBlock):
                        print(b.text)
            elif isinstance(msg, ResultMessage):
                say("dim", "sdk", f"done, cost=${getattr(msg, 'total_cost_usd', 0)}")
    print("workspace:", ws.summary())


def run_live() -> None:
    require_env("ANTHROPIC_API_KEY")
    banner("Claude Agent SDK - live")
    asyncio.run(_one_shot())
    asyncio.run(_full())


if __name__ == "__main__":
    main(run_mock, run_live)
