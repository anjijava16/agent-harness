"""Genspark - AI workspace and agents, reached by developers over MCP.

Architecture notes
------------------
* Started as an AI search engine, pivoted to no-code personal agents in 2025: AI Slides,
  AI Sheets, AI Docs, "Call For Me" phone calls, AI browser, Genspark Claw, plus a
  mixture-of-agents engine that routes across several frontier models and cross-checks.
* Developer surface: a hosted *remote MCP server* (path /api/mcp) exposing Genspark's
  tools, resources and prompts over streamable HTTP, behind OAuth 2.1 (authorization
  code + PKCE, refresh tokens, dynamic client registration). There is no widely
  documented REST API beyond that.

So the right way to "use Genspark from Python" is: be an MCP client. Mock = a fake MCP
server with Genspark-shaped tools. Live = the official `mcp` Python SDK talking to the
remote server with a bearer token you got from the OAuth flow.
"""

from __future__ import annotations

import asyncio
import os

from pa_core import (ApprovalGate, ApprovalMode, AutonomousAgent, ScriptedLLM, Step, Tool,
                     ToolRegistry)
from pa_core.cli import main, require_env
from pa_core.tools import Risk
from pa_core.trace import banner, say, section


class FakeMCPServer:
    """Same shape as an MCP server: list_tools() and call_tool(name, args)."""

    TOOLS = {
        "deep_research": ("Multi-model research with cross-checked citations", Risk.READ),
        "create_slides": ("Generate a slide deck from a brief", Risk.WRITE),
        "call_for_me": ("Place a phone call on the user's behalf and summarize it", Risk.EXTERNAL),
    }

    def list_tools(self) -> list[dict]:
        return [{"name": n, "description": d} for n, (d, _) in self.TOOLS.items()]

    def call_tool(self, name: str, args: dict) -> dict:
        if name == "deep_research":
            return {"answer": "Friendly, specific, include a pay link; escalate after 30 days.",
                    "sources": 3, "models_agreed": ["gpt", "claude", "gemini"]}
        if name == "create_slides":
            return {"deck_url": "https://www.genspark.ai/slides/abc123", "slides": 6}
        if name == "call_for_me":
            return {"summary": f"Spoke to {args.get('to')}: payment scheduled Friday."}
        raise KeyError(name)


def mcp_tools_as_local(server: FakeMCPServer) -> list[Tool]:
    """Adapter: every remote MCP tool becomes a local Tool the agent loop can call."""
    out = []
    for spec in server.list_tools():
        name = spec["name"]
        out.append(Tool(name=name, description=spec["description"], risk=FakeMCPServer.TOOLS[name][1],
                        fn=lambda _n=name, **kw: server.call_tool(_n, kw),
                        parameters={"type": "object", "properties": {}}))
    return out


def run_mock() -> dict:
    banner("Genspark - consume a remote MCP server as agent tools (mock)")
    server = FakeMCPServer()
    section("1. Discover tools")
    for t in server.list_tools():
        say("ok", "mcp", f"{t['name']}: {t['description']}")
    script = [
        Step.call("deep_research", "Ask Genspark's mixture-of-agents for guidance.",
                  query="overdue invoice reminder best practice"),
        Step.call("create_slides", "Turn it into a 6-slide deck for the team.", brief="AR collections playbook"),
        Step.call("call_for_me", "Call Northwind AP.", to="+44 20 7946 0000", goal="confirm payment date"),
        Step.final("Research done, deck created, Northwind says Friday."),
    ]
    section("2. Use them from an agent")
    agent = AutonomousAgent("Orchestrator", "Uses Genspark via MCP.", ScriptedLLM(script),
                            ToolRegistry(mcp_tools_as_local(server)),
                            gate=ApprovalGate(ApprovalMode.RISK_BASED, human=lambda t, a: True))
    r = agent.run("Build an AR collections playbook and confirm Northwind's payment date")
    return {"tools": [t["name"] for t in server.list_tools()], "used": r.tools_used}


async def _live() -> None:
    import httpx
    from mcp import ClientSession

    try:  # mcp >= 2.x
        from mcp.client.streamable_http import streamable_http_client as connect
        new_api = True
    except ImportError:  # mcp 1.x
        from mcp.client.streamable_http import streamablehttp_client as connect
        new_api = False

    url = os.environ["GENSPARK_MCP_URL"]
    headers = {"Authorization": f"Bearer {os.environ['GENSPARK_MCP_TOKEN']}"}
    if new_api:
        cm = connect(url, http_client=httpx.AsyncClient(headers=headers, timeout=60))
    else:
        cm = connect(url, headers=headers)
    async with cm as streams:
        read, write = streams[0], streams[1]
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            for t in tools.tools:
                print("-", t.name, ":", (t.description or "")[:80])
            name = os.environ.get("GENSPARK_TOOL")
            if name:
                res = await session.call_tool(name, {"query": "overdue invoice reminder best practices"})
                print(res.content)


def run_live() -> None:
    """export GENSPARK_MCP_URL=https://<genspark host>/api/mcp   (check Genspark's MCP docs)
       export GENSPARK_MCP_TOKEN=<OAuth access token from Genspark's OAuth 2.1 flow>
       export GENSPARK_TOOL=<optional tool name to call>"""
    require_env("GENSPARK_MCP_URL", "GENSPARK_MCP_TOKEN")
    banner("Genspark - live MCP client")
    asyncio.run(_live())


if __name__ == "__main__":
    main(run_mock, run_live)
