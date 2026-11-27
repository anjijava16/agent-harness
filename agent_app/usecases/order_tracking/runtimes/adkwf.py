"""Google ADK 2.x Workflows: the graph engine. Function nodes do the deterministic work, Agent
nodes (mode="single_turn") do the parts that need a model, and ctx.route picks the edge.

harness  START -> intake -> assistant (agent node with tools) -> audit
looping  a cycle: poll -> think (agent node) -> record -> poll, plus poll -> wait -> poll when idle
graph    load -> ask_classify -> classifier -> route -> investigate -> act -> ask_draft -> drafter -> notify -> finish
"""

from __future__ import annotations

import asyncio
import uuid

from google.adk import Agent, Context, Runner, Workflow
from google.adk.sessions import InMemorySessionService
from google.adk.workflow import START
from google.genai import types
from sqlalchemy import func, select

from app import db

from ..brain import SYSTEM, task_text
from ..models import AgentStep
from ..tools import make_tools, step
from .common import (act, adk_model, adk_tools, classify_prompt, draft_prompt, graph_summary, investigate, load, notify,
                     parse_category, route_after_classify, tools_by_name)

APP = "order_tracking_wf"


async def run_workflow(wf: Workflow, text: str) -> str:
    ss = InMemorySessionService()
    sid = uuid.uuid4().hex
    await ss.create_session(app_name=APP, user_id="ops", session_id=sid)
    runner = Runner(app_name=APP, node=wf, session_service=ss)
    final = ""
    async for ev in runner.run_async(user_id="ops", session_id=sid, new_message=types.Content(role="user", parts=[types.Part(text=text)])):
        if isinstance(getattr(ev, "output", None), str):        # function nodes report their result here
            final = ev.output
        for p in (ev.content.parts if ev.content and ev.content.parts else []):
            if p.text and not p.thought:                         # agent nodes report it as text
                final = p.text
    return final


async def harness(ref, ask: str, mode: str) -> str:  # noqa: ANN001
    assistant = Agent(name="assistant", mode="single_turn", model=adk_model(mode), instruction=SYSTEM["harness"], tools=adk_tools(make_tools(ref)))
    answer: dict = {}

    def intake(node_input) -> str:  # noqa: ANN001
        step(ref, "node", "intake")
        return task_text({"agent": "harness", "ask": node_input.parts[0].text})

    def audit(node_input) -> str:  # noqa: ANN001
        step(ref, "node", "audit")
        with db.session() as s:
            n = s.scalar(select(func.count()).select_from(AgentStep).where(AgentStep.run_id == ref.run_id, AgentStep.kind == "tool"))
        answer["text"] = str(node_input)
        return f"{node_input} ({n} tool calls, audited)"

    return await run_workflow(Workflow(name="harness", edges=[(START, intake, assistant, audit)]), ask)


async def looping(ref, io, mode: str) -> str:  # noqa: ANN001
    thinker = Agent(name="think", mode="single_turn", model=adk_model(mode), instruction=SYSTEM["looping"], tools=adk_tools(make_tools(ref)))
    batch: dict = {"events": []}

    def poll(ctx: Context, node_input) -> str:  # noqa: ANN001
        events = [] if io.should_stop() else io.poll()
        batch["events"] = events
        ctx.route = "events" if events else ("stop" if io.should_stop() else "idle")
        return io.task(events) if events else "idle"

    async def wait(node_input) -> str:  # noqa: ANN001
        await asyncio.sleep(io.interval)
        return "poll"

    def record(node_input) -> str:  # noqa: ANN001
        io.record(ref, batch["events"], str(node_input))
        return "recorded"

    def done(node_input) -> str:  # noqa: ANN001
        return f"{io.iteration} iterations. " + (io.summaries[-1] if io.summaries else "No events.")

    wf = Workflow(name="watch_loop", edges=[
        (START, poll),
        (poll, {"events": thinker, "idle": wait, "stop": done}),
        (thinker, record, poll),
        (wait, poll),
    ])
    return await run_workflow(wf, "start watching")


async def graph(ref, event: dict, mode: str) -> tuple[str, list]:  # noqa: ANN001
    tb, path, st = tools_by_name(ref), [], {"event": event, "actions": []}
    classifier = Agent(name="classifier", mode="single_turn", model=adk_model(mode), instruction=SYSTEM["classify"])
    drafter = Agent(name="drafter", mode="single_turn", model=adk_model(mode), instruction=SYSTEM["draft"])

    def mark(name: str) -> None:
        path.append(name)
        step(ref, "node", name)

    def load_n(node_input) -> dict:  # noqa: ANN001
        mark("load")
        st.update(load(tb, event))
        return st["order"]

    def ask_classify(node_input) -> str:  # noqa: ANN001
        mark("classify")
        return classify_prompt(event)

    def route(ctx: Context, node_input) -> str:  # noqa: ANN001
        st["category"] = parse_category(str(node_input), event)
        ctx.route = route_after_classify(st["category"])
        return st["category"]

    def investigate_n(node_input) -> dict:  # noqa: ANN001
        mark("investigate")
        st["actions"].append(investigate(tb, st["order"]))
        return st["order"]

    def act_n(node_input) -> dict:  # noqa: ANN001
        mark("act")
        st["actions"] += act(tb, st["category"], st["order"])
        return st["order"]

    def ask_draft(node_input) -> str:  # noqa: ANN001
        mark("draft")
        return draft_prompt(st["category"], st["order"])

    def notify_n(node_input) -> str:  # noqa: ANN001
        mark("notify")
        st["notified"] = notify(tb, st["category"], st["order"], str(node_input))
        return "notified"

    def finish(node_input) -> str:  # noqa: ANN001
        mark("finish")
        return graph_summary(event, st.get("category", "routine"), st["actions"], st.get("notified"))

    wf = Workflow(name="event_graph", edges=[
        (START, load_n, ask_classify, classifier, route),
        (route, {"finish": finish, "draft": ask_draft, "act": act_n, "investigate": investigate_n}),
        (investigate_n, act_n),
        (act_n, ask_draft),
        (ask_draft, drafter, notify_n, finish),
    ])
    summary = await run_workflow(wf, f"event {event.get('event_id')}")
    return summary, path
