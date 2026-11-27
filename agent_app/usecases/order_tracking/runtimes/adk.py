"""Google ADK 2.x agents (no workflow engine).

harness  one Agent with the tools; the model plans and acts
looping  one Runner and one session for the whole watch, so the agent keeps context across
         iterations; a Python loop feeds it each batch
graph    an agent tree: a 'dispatcher' agent reads the event and transfers control
         (transfer_to_agent) to the right specialist sub-agent. The graph is the agent hierarchy;
         the edges are the transfers the model chooses.
"""

from __future__ import annotations

import uuid

from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from ..brain import CATEGORY, SYSTEM, task_text
from ..standins import PolicyLlm
from ..tools import make_tools, step
from .common import adk_model, adk_tools, graph_summary, python_loop

APP = "order_tracking"
HANDLER = {"heads_up": "notify_handler", "delivered": "notify_handler", "delay": "delay_handler",
           "address": "address_handler", "lost": "loss_handler", "damaged": "loss_handler"}


async def ask(runner: Runner, user: str, session: str, text: str) -> tuple[str, list[str]]:
    final, authors = "", []
    msg = types.Content(role="user", parts=[types.Part(text=text)])
    async for ev in runner.run_async(user_id=user, session_id=session, new_message=msg):
        if ev.author and ev.author != "user" and (not authors or authors[-1] != ev.author):
            authors.append(ev.author)
        for p in (ev.content.parts if ev.content and ev.content.parts else []):
            if p.text and not p.thought:
                final = p.text
    return final, authors


async def _runner(agent: Agent) -> tuple[Runner, str]:
    ss = InMemorySessionService()          # production: DatabaseSessionService(db_url=...) on the same database
    sid = uuid.uuid4().hex
    await ss.create_session(app_name=APP, user_id="ops", session_id=sid)
    return Runner(app_name=APP, agent=agent, session_service=ss), sid


async def harness(ref, ask_text: str, mode: str) -> str:  # noqa: ANN001
    agent = Agent(name="order_support", model=adk_model(mode), instruction=SYSTEM["harness"], tools=adk_tools(make_tools(ref)))
    runner, sid = await _runner(agent)
    return (await ask(runner, "ops", sid, task_text({"agent": "harness", "ask": ask_text})))[0]


async def looping(ref, io, mode: str) -> str:  # noqa: ANN001
    agent = Agent(name="stream_watcher", model=adk_model(mode), instruction=SYSTEM["looping"], tools=adk_tools(make_tools(ref)))
    runner, sid = await _runner(agent)

    async def think(task: str) -> str:
        return (await ask(runner, "ops", sid, task))[0]

    return await python_loop(io, ref, think)


class DispatcherLlm(PolicyLlm):
    """Stand-in for the dispatcher: pick the specialist from the event, or stop for routine scans."""

    def decide(self, task: dict, obs: list) -> dict:
        cat = CATEGORY.get(task["events"][0]["code"], "routine")
        if cat == "routine":
            return {"final": "Routine scan, no action needed."}
        return {"calls": [("transfer_to_agent", {"agent_name": HANDLER[cat]})]}


async def graph(ref, event: dict, mode: str) -> tuple[str, list]:  # noqa: ANN001
    tools = adk_tools(make_tools(ref))

    def handler(name: str, what: str) -> Agent:
        return Agent(name=name, model=adk_model(mode), tools=tools, disallow_transfer_to_parent=True,
                     instruction=f"You handle {what}. Look up the order, act on the event by these rules, then reply in one line.\n" + SYSTEM["looping"])

    subs = [handler("notify_handler", "out-for-delivery and delivered scans"), handler("delay_handler", "delays and weather holds"),
            handler("address_handler", "failed deliveries due to address problems"), handler("loss_handler", "lost and damaged parcels")]
    dispatcher = Agent(name="dispatcher", model=DispatcherLlm() if mode == "scripted" else adk_model(mode), sub_agents=subs,
                       instruction="Read the carrier event and transfer to exactly one specialist: " + ", ".join(sorted(set(HANDLER.values())))
                       + ". For routine scans (label created, picked up, in transit) reply 'Routine scan, no action needed.'")
    runner, sid = await _runner(dispatcher)
    # handlers reuse the looping rules on a one-event batch
    final, authors = await ask(runner, "ops", sid, task_text({"agent": "looping", "iteration": 1, "events": [event]}))
    for a in authors:
        step(ref, "node", a)
    cat = CATEGORY.get(event["code"], "routine")
    return (final if cat != "routine" else graph_summary(event, "routine", [], None)), authors
