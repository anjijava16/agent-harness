"""LangGraph Functional API: @entrypoint and @task.

Same runtime (checkpoints, interrupts, streaming), but you write ordinary Python control
flow instead of declaring nodes and edges. @task results are checkpointed, so on resume
finished tasks are not re-run. Calling a task returns a future; .result() waits, which
makes parallel work trivial.

Use case: a nightly job. Fetch invoices, score each in parallel, pause for approval if any
are severe, then send.
"""

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.types import Command, interrupt

CALLS = {"fetch": 0}


@task
def fetch_invoices() -> list[dict]:
    CALLS["fetch"] += 1
    return [{"id": "INV-1038", "days": 14}, {"id": "INV-1042", "days": 3}, {"id": "INV-0990", "days": 45}]


@task
def score(inv: dict) -> dict:
    return {**inv, "severity": "high" if inv["days"] > 30 else "medium" if inv["days"] > 7 else "low"}


@entrypoint(checkpointer=InMemorySaver())
def nightly(run_date: str) -> dict:
    invoices = fetch_invoices().result()
    scored = [f.result() for f in [score(i) for i in invoices]]          # fan out, then join
    severe = [s["id"] for s in scored if s["severity"] == "high"]
    if severe:
        ok = interrupt({"severe": severe, "question": "Escalate these to a human?"})
        if not ok:
            severe = []
    return {"date": run_date, "scored": scored, "escalated": severe}


if __name__ == "__main__":
    cfg = {"configurable": {"thread_id": "nightly-2026-11-26"}}
    first = nightly.invoke("2026-11-26", cfg)
    print("paused:", first if isinstance(first, dict) and "__interrupt__" not in first else "waiting for approval")
    for chunk in nightly.stream(Command(resume=True), cfg):
        print("resumed ->", chunk)
    print("fetch_invoices ran", CALLS["fetch"], "time(s) (checkpointed task not re-run on resume)")
