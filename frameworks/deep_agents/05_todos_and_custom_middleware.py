"""Deep Agents: add planning back, and bring your own middleware.

Deep Agents 0.7 removed the write_todos planner from the default harness. For long tasks
where a visible plan helps, add LangChain's TodoListMiddleware. Any other create_agent
middleware works too; here a custom @wrap_tool_call logs every tool call as an audit trail
(the same idea as Perplexity Personal Computer's audit log).

Use case: month-end close, a multi-step job you want to watch progress on.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from deepagents import create_deep_agent  # noqa: E402
from langchain.agents.middleware import TodoListMiddleware, wrap_tool_call  # noqa: E402
from langchain.tools import tool  # noqa: E402

from frameworks._fakes.lc_fake import call, model, say  # noqa: E402

AUDIT: list[str] = []


@wrap_tool_call
def audit(request, handler):  # noqa: ANN001
    AUDIT.append(f"{request.tool_call['name']}({request.tool_call['args']})")
    return handler(request)


@tool
def reconcile(account: str) -> str:
    """Reconcile one ledger account."""
    return f"{account}: reconciled, 0 differences"


todos = [{"content": "Reconcile AR", "status": "in_progress"},
         {"content": "Reconcile AP", "status": "pending"},
         {"content": "Write close memo", "status": "pending"}]
agent = create_deep_agent(
    model=model(
        call("write_todos", {"todos": todos}, "t1"),
        call("reconcile", {"account": "AR"}, "t2"),
        call("reconcile", {"account": "AP"}, "t3"),
        call("write_todos", {"todos": [{**t, "status": "completed"} for t in todos]}, "t4"),
        say("Month-end close done: AR and AP reconciled, memo drafted."),
    ),
    tools=[reconcile],
    middleware=[TodoListMiddleware(), audit],
)

if __name__ == "__main__":
    r = agent.invoke({"messages": [{"role": "user", "content": "Do the month-end close"}]})
    print("final todos:")
    for t in r["todos"]:
        print(f"  [{'x' if t['status'] == 'completed' else ' '}] {t['content']}")
    print("audit trail:")
    for a in AUDIT:
        print("  ", a)
    print(r["messages"][-1].content)
