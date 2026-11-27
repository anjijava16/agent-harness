"""Multi-agent with create_agent (agents as tools) plus resilience middleware.

Pattern: a supervisor agent whose tools are other agents. Each sub-agent has its own
prompt, tools and context window; the supervisor only sees their final answers.

Resilience middleware worth knowing (all in langchain.agents.middleware):
  ModelRetryMiddleware        retry failed model calls with backoff
  ModelFallbackMiddleware     fall back to another model on errors
  ToolRetryMiddleware         retry flaky tools
  ModelCallLimitMiddleware    cap model calls per run/thread (cost guard)
  SummarizationMiddleware     summarize old turns when the context gets long
  TodoListMiddleware          give the agent a write_todos planning tool

Use case: "prepare Monday's collections run" -> research agent + writer agent.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from langchain.agents import create_agent  # noqa: E402
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolRetryMiddleware  # noqa: E402
from langchain.tools import tool  # noqa: E402

from frameworks._fakes.lc_fake import call, model, say, show  # noqa: E402

ATTEMPTS = {"n": 0}


@tool
def ledger_lookup(customer: str) -> dict:
    """Look up a customer's open balance (flaky on the first try)."""
    ATTEMPTS["n"] += 1
    if ATTEMPTS["n"] == 1:
        raise ConnectionError("ledger timeout")
    return {"customer": customer, "open": 2400, "days": 14}


researcher = create_agent(
    model=model(call("ledger_lookup", {"customer": "Northwind"}), say("Northwind owes $2,400, 14 days late.")),
    tools=[ledger_lookup], name="researcher",
    middleware=[ToolRetryMiddleware(max_retries=2, initial_delay=0.01)],
)
writer = create_agent(model=model(say("Hi Northwind team, a friendly nudge on $2,400 (14 days). Pay link inside.")),
                      tools=[], name="writer")


@tool
def ask_researcher(question: str) -> str:
    """Delegate a factual question to the research agent."""
    return researcher.invoke({"messages": [{"role": "user", "content": question}]})["messages"][-1].content


@tool
def ask_writer(brief: str) -> str:
    """Delegate drafting to the writer agent."""
    return writer.invoke({"messages": [{"role": "user", "content": brief}]})["messages"][-1].content


supervisor = create_agent(
    model=model(call("ask_researcher", {"question": "What does Northwind owe?"}),
                call("ask_writer", {"brief": "Gentle reminder: Northwind, $2,400, 14 days"}),
                say("Ready: research done and a draft prepared for Northwind.")),
    tools=[ask_researcher, ask_writer],
    middleware=[ModelCallLimitMiddleware(run_limit=6)],
    system_prompt="You coordinate specialists. Delegate, then summarize.",
)

if __name__ == "__main__":
    r = supervisor.invoke({"messages": [{"role": "user", "content": "Prepare Monday's collections run"}]})
    show(r["messages"])
    print(f"\n  ledger attempts (1 failure retried by ToolRetryMiddleware): {ATTEMPTS['n']}")
