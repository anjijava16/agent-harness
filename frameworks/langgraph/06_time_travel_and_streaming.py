"""LangGraph: checkpoints for time travel, and streaming modes.

Every super-step is a checkpoint. You can:
  * list history       graph.get_state_history(cfg)
  * fork from the past graph.update_state(old_cfg, {...}) then invoke(None, new_cfg)
  * stream             stream_mode="updates" (per-node deltas), "values" (full state),
                       "custom" (anything a node writes with get_stream_writer()),
                       "messages" (LLM tokens)

Use case: debugging an agent run. "What if the tone had been firm instead?" without
re-running the expensive steps before it.
"""

from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.config import get_stream_writer
from langgraph.graph import END, START, StateGraph

EXPENSIVE = {"n": 0}


class State(TypedDict):
    research: str
    tone: str
    draft: str


def research(state: State) -> dict:
    EXPENSIVE["n"] += 1
    get_stream_writer()({"progress": "researching customer history..."})
    return {"research": "Northwind: 3 late payments this year"}


def pick_tone(state: State) -> dict:
    return {"tone": "friendly"}


def write(state: State) -> dict:
    return {"draft": f"[{state['tone']}] Reminder for Northwind. Context: {state['research']}"}


g = StateGraph(State)
for n, f in [("research", research), ("pick_tone", pick_tone), ("write", write)]:
    g.add_node(n, f)
g.add_edge(START, "research")
g.add_edge("research", "pick_tone")
g.add_edge("pick_tone", "write")
g.add_edge("write", END)
graph = g.compile(checkpointer=InMemorySaver())

if __name__ == "__main__":
    cfg = {"configurable": {"thread_id": "debug-1"}}
    print("== stream (updates + custom) ==")
    for mode, chunk in graph.stream({"research": "", "tone": "", "draft": ""}, cfg, stream_mode=["updates", "custom"]):
        print(f"  {mode:>7}: {chunk}")

    print("\n== history (newest first) ==")
    history = list(graph.get_state_history(cfg))
    for snap in history:
        print(f"  next={snap.next!s:<16} tone={snap.values.get('tone')!r}")

    print("\n== fork: go back to just after pick_tone and change the tone ==")
    before_write = next(s for s in history if s.next == ("write",))
    forked = graph.update_state(before_write.config, {"tone": "firm"})
    print("  ", graph.invoke(None, forked)["draft"])
    print(f"  research ran {EXPENSIVE['n']} time(s); the fork reused the checkpoint")
