"""LangGraph: multi-agent supervisor with Command(goto=...) handoffs.

A node can return Command(goto="other_node", update={...}) to both update state and pick
the next node. That's the handoff primitive behind supervisor and swarm architectures:
the supervisor decides who works next; workers hand control back.

Here the supervisor is an LLM agent (scripted offline) whose tools are handoffs.

Use case: a Chief-of-Staff agent (Grok Bot users build exactly this) routing between a
finance specialist and a comms specialist.
"""

import pathlib
import sys
from typing import Annotated, Literal, TypedDict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from langchain_core.messages import AIMessage, AnyMessage  # noqa: E402
from langgraph.graph import END, START, StateGraph  # noqa: E402
from langgraph.graph.message import add_messages  # noqa: E402
from langgraph.types import Command  # noqa: E402

from frameworks._fakes.lc_fake import model, say  # noqa: E402


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    done: list[str]


# The supervisor's "decisions", as a real model would emit them.
supervisor_llm = model(say("finance"), say("comms"), say("FINISH"))


def supervisor(state: State) -> Command[Literal["finance", "comms", "__end__"]]:
    choice = supervisor_llm.invoke(state["messages"]).content.strip()
    print(f"  supervisor -> {choice}")
    return Command(goto=END if choice == "FINISH" else choice)


def finance(state: State) -> Command[Literal["supervisor"]]:
    msg = AIMessage(content="Finance: Northwind $2,400 (14d), BrightPath $850 (3d).", name="finance")
    return Command(goto="supervisor", update={"messages": [msg], "done": state["done"] + ["finance"]})


def comms(state: State) -> Command[Literal["supervisor"]]:
    msg = AIMessage(content="Comms: two reminders drafted and queued for approval.", name="comms")
    return Command(goto="supervisor", update={"messages": [msg], "done": state["done"] + ["comms"]})


g = StateGraph(State)
g.add_node("supervisor", supervisor)
g.add_node("finance", finance)
g.add_node("comms", comms)
g.add_edge(START, "supervisor")
graph = g.compile()

if __name__ == "__main__":
    out = graph.invoke({"messages": [{"role": "user", "content": "Run Monday collections"}], "done": []})
    for m in out["messages"][1:]:
        print(f"  {m.name}: {m.content}")
    print("  order of work:", out["done"])
