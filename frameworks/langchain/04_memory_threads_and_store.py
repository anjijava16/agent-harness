"""Short-term and long-term memory in LangChain 1.x.

Short-term  = the conversation thread. A checkpointer (InMemorySaver here; Postgres/SQLite
              in production) saves state per thread_id, so a second call continues the chat.
Long-term   = facts that outlive a thread. A LangGraph store (InMemoryStore here) is
              reachable from tools through the runtime, namespaced per user.

Use case: a personal agent that remembers "Northwind prefers reminders on Mondays" across
completely separate conversations.
"""

import pathlib
import sys
import warnings
from dataclasses import dataclass

# langgraph 1.2 emits a harmless pydantic serializer warning when a context object is passed.
warnings.filterwarnings("ignore", message="Pydantic serializer warnings")

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from langchain.agents import create_agent  # noqa: E402
from langchain.tools import ToolRuntime, tool  # noqa: E402
from langgraph.checkpoint.memory import InMemorySaver  # noqa: E402
from langgraph.store.memory import InMemoryStore  # noqa: E402

from frameworks._fakes.lc_fake import call, model, say  # noqa: E402


@dataclass
class UserCtx:
    """Per-request context (who is talking). Passed with invoke(..., context=...)."""
    user_id: str


@tool
def remember(fact: str, runtime: ToolRuntime) -> str:
    """Save a long-term fact about the user's customers."""
    user = runtime.context.user_id
    n = len(runtime.store.search((user, "facts")))
    runtime.store.put((user, "facts"), f"f{n}", {"fact": fact})
    return "saved"


@tool
def recall(runtime: ToolRuntime) -> list[str]:
    """Return all saved long-term facts."""
    return [i.value["fact"] for i in runtime.store.search((runtime.context.user_id, "facts"))]


store, saver = InMemoryStore(), InMemorySaver()
agent = create_agent(
    model=model(
        call("remember", {"fact": "Northwind prefers reminders on Mondays"}), say("Noted."),
        say("You told me your name is Sam."),                                  # same thread
        call("recall", {}), say("Northwind prefers reminders on Mondays."),     # new thread
    ),
    tools=[remember, recall], checkpointer=saver, store=store,
    context_schema=UserCtx,
)

if __name__ == "__main__":
    ctx = UserCtx(user_id="sam")
    t1 = {"configurable": {"thread_id": "t1"}}
    agent.invoke({"messages": [{"role": "user", "content": "I'm Sam. Remember Northwind likes Monday reminders."}]}, t1, context=ctx)
    r = agent.invoke({"messages": [{"role": "user", "content": "What's my name?"}]}, t1, context=ctx)
    print("same thread  :", r["messages"][-1].content, f"({len(r['messages'])} messages in thread t1)")
    t2 = {"configurable": {"thread_id": "t2"}}
    r = agent.invoke({"messages": [{"role": "user", "content": "When should I remind Northwind?"}]}, t2, context=ctx)
    print("new thread   :", r["messages"][-1].content, f"({len(r['messages'])} messages in thread t2)")
    print("store content:", [i.value for i in store.search(("sam", "facts"))])
