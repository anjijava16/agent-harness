"""Deep Agents 0.7: the default harness in one call.

create_deep_agent(...) gives you, on top of LangChain's create_agent:
  * filesystem tools: ls, read_file, write_file, edit_file, glob, grep (+ delete in 0.7)
    backed by a pluggable backend (StateBackend by default = files live in graph state)
  * a `task` tool that delegates to subagents, each with its own context window
  * automatic summarization of long histories, tool-call patching, prompt caching
Not included by default since 0.7: the write_todos planner (see 05_todos_and_middleware.py).

Use case: research a customer's overdue balance with a specialist subagent and leave
notes in the agent's filesystem for the next run.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from deepagents import create_deep_agent  # noqa: E402
from langchain.tools import tool  # noqa: E402

from frameworks._fakes.lc_fake import call, model, say, show  # noqa: E402


@tool
def list_overdue_invoices(min_days: int = 1) -> list[dict]:
    """List open invoices overdue by at least min_days."""
    return [{"id": "INV-1038", "customer": "Northwind", "amount": 2400, "days": 14},
            {"id": "INV-1042", "customer": "BrightPath", "amount": 850, "days": 3}]


researcher_model = model(call("list_overdue_invoices", {"min_days": 1}, "r1"),
                         say("2 overdue: INV-1038 Northwind $2,400 (14d); INV-1042 BrightPath $850 (3d)."))
main_model = model(
    call("task", {"description": "List all overdue invoices with amounts", "subagent_type": "ar-researcher"}, "m1"),
    call("write_file", {"file_path": "/notes/collections.md",
                        "content": "# Collections 2026-11-26\n- INV-1038 Northwind $2,400 14d\n- INV-1042 BrightPath $850 3d\n"}, "m2"),
    call("read_file", {"file_path": "/notes/collections.md"}, "m3"),
    say("Two invoices are overdue ($3,250). Notes saved to /notes/collections.md."),
)

agent = create_deep_agent(
    model=main_model,
    tools=[list_overdue_invoices],
    system_prompt="You run accounts receivable for Acme Studio. Delegate research; keep notes in /notes/.",
    subagents=[{
        "name": "ar-researcher",
        "description": "Looks up invoice and customer facts. Use for any ledger question.",
        "system_prompt": "You only research. Return a short factual list.",
        "tools": [list_overdue_invoices],
        "model": researcher_model,
    }],
)

if __name__ == "__main__":
    r = agent.invoke({"messages": [{"role": "user", "content": "What's overdue? Keep notes."}]})
    show(r["messages"])
    print("\nfiles in agent state:", list(r["files"]))
