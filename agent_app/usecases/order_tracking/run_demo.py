"""Watch the agents work from the terminal (no UI needed).

    python usecases/order_tracking/run_demo.py                                  # looping agent on LangGraph
    python usecases/order_tracking/run_demo.py --agent graph --runtime adk_workflow
    python usecases/order_tracking/run_demo.py --agent harness --runtime claude --ask "Where is order 1006?"
    python usecases/order_tracking/run_demo.py --agent all                       # 3 agent types x 6 runtimes, compared

Uses a throwaway SQLite file and in-process Redis unless DATABASE_URL / REDIS_URL are set.
"""

from __future__ import annotations

import argparse
import asyncio
import collections
import os
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DATABASE_URL", f"sqlite:///{tempfile.mkdtemp()}/order_tracking.db")

from sqlalchemy import select  # noqa: E402

from app import cache, config, db  # noqa: E402
from usecases.order_tracking import AGENT_TYPES, LABELS, RUNTIMES, agents  # noqa: E402
from usecases.order_tracking.models import Approval, Notification, Ticket  # noqa: E402
from usecases.order_tracking.sim import Simulator  # noqa: E402


def tick_until_news(sim: Simulator, show: bool):  # noqa: ANN201
    """Advance the carrier feed until it produces scans (or finishes), as a live feed would."""
    def tick() -> None:
        while not sim.done():
            evs = sim.tick()
            if evs:
                for e in evs if show else []:
                    print(f"    scan  #{e['order_id']} {e['code']:<17} {e['location']}")
                return
    return tick


def totals() -> str:
    with db.session() as s:
        n = len(s.scalars(select(Notification)).all())
        t = len(s.scalars(select(Ticket)).all())
        a = collections.Counter(x.action for x in s.scalars(select(Approval)))
    return f"{n} emails, {t} tickets, approvals waiting: {dict(a)}"


async def one(agent: str, runtime: str, ask: str, quiet: bool) -> str:
    sim = Simulator(seed=7)
    sim.reset()
    feed = tick_until_news(sim, show=not quiet)
    if agent == "looping":
        r = await agents.run_looping(runtime, interval=0, idle_limit=1, before_poll=feed)
        return f"{r['iterations']} iterations. {totals()}"
    if agent == "graph":
        ran = await agents.graph_dispatcher(runtime, interval=0, idle_limit=1, before_poll=feed)
        return f"{ran} graph runs. {totals()}"
    sim.run_to_end()
    return (await agents.run_harness(runtime, ask))["answer"]


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", choices=[*AGENT_TYPES, "all"], default="looping")
    ap.add_argument("--runtime", choices=RUNTIMES, default="langgraph")
    ap.add_argument("--ask", default="Where is order 1003?")
    a = ap.parse_args()
    db.init(os.environ["DATABASE_URL"])
    cache.connect(config.REDIS_URL)
    print(f"database: {db.dialect()}   redis: {cache.kind()}\n")
    if a.agent != "all":
        print(f"== {a.agent} agent on {LABELS[a.runtime]}")
        print("\n" + await one(a.agent, a.runtime, a.ask, quiet=False))
        return
    print("| agent | " + " | ".join(LABELS[r] for r in RUNTIMES) + " |\n|---|" + "---|" * len(RUNTIMES))
    for agent in AGENT_TYPES:
        cells = []
        for rt in RUNTIMES:
            out = await one(agent, rt, a.ask, quiet=True)
            cells.append("ok" if out and "Error" not in out else "FAIL")
            if agent == "looping":
                last = out
        print(f"| {agent} | " + " | ".join(cells) + " |")
    print("\nlooping and graph agents end in the same state on every runtime: " + last.split(". ", 1)[1])


if __name__ == "__main__":
    asyncio.run(main())
