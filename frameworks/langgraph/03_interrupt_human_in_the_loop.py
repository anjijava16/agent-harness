"""LangGraph: human-in-the-loop with interrupt() and Command(resume=...).

interrupt(payload) pauses the graph *inside* a node and saves everything to the
checkpointer. Your app shows the payload to a person. Later (seconds or days), you call
graph.invoke(Command(resume=answer), same thread_id) and the node continues from the
interrupt() call with `answer` as its return value.

This is the durable-approval pattern every personal agent needs: Duet's "reply send",
Cowork's approve-each-action, Instinct's "Reply YES".

Use case: approve, edit or reject an outgoing reminder.
"""

from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict):
    to: str
    body: str
    status: str


def draft(state: State) -> dict:
    return {"body": f"Hi, a friendly nudge about your invoice. - Acme ({state['to']})"}


def approval(state: State) -> dict:
    answer = interrupt({"question": "Send this email?", "to": state["to"], "body": state["body"]})
    if answer["decision"] == "edit":
        return {"body": answer["body"], "status": "edited"}
    return {"status": answer["decision"]}


def send(state: State) -> dict:
    if state["status"] in ("approve", "edited"):
        return {"status": f"SENT to {state['to']}: {state['body']}"}
    return {"status": "not sent"}


g = StateGraph(State)
g.add_node("draft", draft)
g.add_node("approval", approval)
g.add_node("send", send)
g.add_edge(START, "draft")
g.add_edge("draft", "approval")
g.add_edge("approval", "send")
g.add_edge("send", END)
graph = g.compile(checkpointer=InMemorySaver())

if __name__ == "__main__":
    for thread, answer in [("a", {"decision": "approve"}),
                           ("b", {"decision": "edit", "body": "Quick note on INV-1038, pay link inside."}),
                           ("c", {"decision": "reject"})]:
        cfg = {"configurable": {"thread_id": thread}}
        paused = graph.invoke({"to": "ap@northwind.com", "status": ""}, cfg)
        print(f"[{thread}] paused, asking:", paused["__interrupt__"][0].value["question"])
        print(f"[{thread}] state saved at node:", graph.get_state(cfg).next)
        done = graph.invoke(Command(resume=answer), cfg)
        print(f"[{thread}] -> {done['status']}\n")
