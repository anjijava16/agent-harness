"""Deep Agents backends: where the agent's files actually live.

  StateBackend()                       files in graph state; gone when the thread ends
  FilesystemBackend(root_dir, virtual_mode=True)   real files under root_dir (sandboxed paths)
  StoreBackend(namespace=..., store=...)           a LangGraph store: survives across threads
  CompositeBackend(default, routes={"/memories/": ...})   mix them by path prefix
  LocalShellBackend / sandbox backends             add an `execute` tool for shell commands

The CompositeBackend pattern is the one to copy: scratch work is ephemeral, but anything
written under /memories/ persists. That's long-term memory with zero extra tools.

Use case: thread 1 learns a customer preference; thread 2 (new conversation) reads it back.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from deepagents import create_deep_agent  # noqa: E402
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend  # noqa: E402
from langgraph.checkpoint.memory import MemorySaver  # noqa: E402
from langgraph.store.memory import InMemoryStore  # noqa: E402

from frameworks._fakes.lc_fake import call, model, say  # noqa: E402

store = InMemoryStore()
backend = CompositeBackend(
    default=StateBackend(),
    routes={"/memories/": StoreBackend(namespace=lambda rt: ("acme", "memories"), store=store)},
)

agent = create_deep_agent(
    model=model(
        # thread 1
        call("write_file", {"file_path": "/scratch/draft.md", "content": "draft v1"}, "a"),
        call("write_file", {"file_path": "/memories/customers.md",
                            "content": "- Northwind: prefers Monday reminders, AP = ap@northwind.com\n"}, "b"),
        say("Saved the preference to long-term memory."),
        # thread 2
        call("ls", {"path": "/"}, "c"),
        call("read_file", {"file_path": "/memories/customers.md"}, "d"),
        say("Northwind prefers Monday reminders."),
    ),
    backend=backend, store=store, checkpointer=MemorySaver(),
)

if __name__ == "__main__":
    agent.invoke({"messages": [{"role": "user", "content": "Remember Northwind likes Mondays"}]},
                 {"configurable": {"thread_id": "t1"}})
    r = agent.invoke({"messages": [{"role": "user", "content": "When does Northwind like reminders?"}]},
                     {"configurable": {"thread_id": "t2"}})
    for m in r["messages"]:
        if m.type == "tool":
            print(f"  tool {m.name}: {m.content[:120]!r}")
    print("  answer:", r["messages"][-1].content)
    print("  /scratch/draft.md visible in thread 2?", "/scratch/draft.md" in str(r["messages"]))
    print("  store keys:", [i.key for i in store.search(("acme", "memories"))])
