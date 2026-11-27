"""Google ADK: AgentTool (an agent used like a function) and MCP toolsets.

AgentTool vs sub_agents:
  sub_agents + transfer  -> control moves to the other agent; it talks to the user
  AgentTool(agent)       -> the caller stays in charge; the other agent returns a result

MCP: McpToolset connects an Agent to any MCP server (stdio or streamable HTTP). Shown
here as a live-only snippet because it needs a running server.

Use case: an orchestrator that calls a "summarizer" agent as a tool, then decides itself.
"""

import asyncio
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from google.adk import Agent  # noqa: E402
from google.adk.tools.agent_tool import AgentTool  # noqa: E402

from frameworks._fakes.adk_fake import llm, run  # noqa: E402

summarizer = Agent(name="summarizer", description="Summarizes a customer's account in one line.",
                   model=llm("Northwind: $2,400 open, 14 days late, usually pays within a week of a nudge."),
                   instruction="Summarize the account in one line.")
orchestrator = Agent(
    name="orchestrator",
    model=llm(("tool", "summarizer", {"request": "Summarize Northwind's account"}),
              "Based on the summary, a friendly nudge is enough. No escalation."),
    instruction="Use the summarizer, then decide: nudge or escalate.",
    tools=[AgentTool(agent=summarizer)],
)

MCP_SNIPPET = '''
# Live: connect an ADK agent to an MCP server (needs the server running).
# MCP support is optional in ADK 2.x: pip install mcp   (McpToolset only exports when mcp is installed)
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

files = McpToolset(connection_params=StdioConnectionParams(
    server_params=StdioServerParameters(command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp/acme"])))
agent = Agent(name="files_agent", model="gemini-2.5-flash", instruction="Manage files.", tools=[files])
'''

if __name__ == "__main__":
    asyncio.run(run(orchestrator, "Should we escalate Northwind?"))
    print(MCP_SNIPPET)
