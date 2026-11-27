"""Find a performance hotspot

When:     11:55 (coding)
Trigger:  manual
Type:     performance

A profiler subagent digs through traces; you get the one line that matters.

Run:  python usecases/swe_day/032_profile_hotspot/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/032_profile_hotspot/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "11:55"
BLOCK = "coding"
TRIGGER = "manual"
AUTOMATION = "performance"

USECASE = UseCase(
    id=32,
    domain="swe-" + BLOCK,
    title="Find a performance hotspot",
    ask="Why is GET /invoices slow?",
    why="A profiler subagent digs through traces; you get the one line that matters.",
    tools=[TOOL("trace_breakdown", "Span breakdown for an endpoint.", {"total_ms": 840, "db_ms": 790, "queries": 101}, {"endpoint": str}),
           TOOL("slow_queries", "Slowest queries for an endpoint.", ["SELECT * FROM customers WHERE id = $1 (x100)"], {"endpoint": str})],
    subagents=[SUB("profiler", "Analyzes traces and query plans.", ["trace_breakdown", "slow_queries"],
                   [par(call("trace_breakdown", endpoint="GET /invoices"), call("slow_queries", endpoint="GET /invoices")),
                    say("N+1: 100 customer lookups per request, 790 of 840 ms in the DB.")])],
    plan=[task("profiler", "Why is GET /invoices slow?"),
          say("It's an N+1: 100 separate customer queries per request (790 of 840 ms). Join customers in the invoice query.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
