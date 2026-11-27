"""Claude Agent SDK.

harness  ClaudeSDKClient + the tools as an in-process MCP server. Claude's harness plans,
         calls tools and answers.
looping  one long-lived ClaudeSDKClient session; each batch of events is the next query in the
         same conversation, so Claude keeps context across iterations
graph    the graph is plain Python; Claude is called at the nodes that need judgment (classify,
         draft) and runs as a full agent at the 'investigate' node for lost/damaged parcels
"""

from __future__ import annotations

from claude_agent_sdk import ClaudeSDKClient

from ..brain import SYSTEM, task_text
from ..tools import make_tools, step
from .common import (act, claude_ask, claude_once, claude_options, classify_prompt, draft_prompt, graph_summary, load, notify,
                     parse_category, python_loop, route_after_classify, tools_by_name)


async def harness(ref, ask: str, mode: str) -> str:  # noqa: ANN001
    return await claude_once(make_tools(ref), SYSTEM["harness"], task_text({"agent": "harness", "ask": ask}), mode)


async def looping(ref, io, mode: str) -> str:  # noqa: ANN001
    opts, transport = claude_options(make_tools(ref), SYSTEM["looping"], mode)
    async with ClaudeSDKClient(options=opts, transport=transport) as client:
        return await python_loop(io, ref, lambda task: claude_ask(client, task))


async def graph(ref, event: dict, mode: str) -> tuple[str, list]:  # noqa: ANN001
    tb, path = tools_by_name(ref), []

    def mark(name: str) -> None:
        path.append(name)
        step(ref, "node", name)

    mark("load")
    st = load(tb, event)
    order = st["order"]
    mark("classify")
    category = parse_category(await claude_once([], SYSTEM["classify"], classify_prompt(event), mode), event)
    nxt = route_after_classify(category)
    if nxt == "finish":
        mark("finish")
        return graph_summary(event, category, [], None), path
    if nxt == "investigate":                     # an agentic node: Claude investigates and acts with tools
        mark("investigate")
        report = await claude_once(make_tools(ref), SYSTEM["investigator"], task_text({"agent": "investigator", "order_id": order["order_id"]}), mode)
        mark("finish")
        return report, path
    actions = []
    if nxt == "act":
        mark("act")
        actions = act(tb, category, order)
    mark("draft")
    message = await claude_once([], SYSTEM["draft"], draft_prompt(category, order), mode)
    mark("notify")
    notified = notify(tb, category, order, message)
    mark("finish")
    return graph_summary(event, category, actions, notified), path
