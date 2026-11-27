"""Real-time order tracking: one live dataset, three kinds of agent, six runtimes.

Agent types:  harness (answers and investigates), looping (watches the event stream),
              graph (a fixed workflow per exception event)
Runtimes:     langchain, langgraph, deepagents, adk, adk_workflow, claude
"""

RUNTIMES = ["langchain", "langgraph", "deepagents", "adk", "adk_workflow", "claude"]
AGENT_TYPES = ["harness", "looping", "graph"]
LABELS = {"langchain": "LangChain", "langgraph": "LangGraph", "deepagents": "Deep Agents", "adk": "Google ADK",
          "adk_workflow": "ADK Workflows", "claude": "Claude Agent SDK"}
