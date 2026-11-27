"""Database index recommendations

When:     23:50 (night)
Trigger:  cron: 50 23 * * 0
Type:     performance

A DBA subagent works through pg_stat_statements in its own context.

Run:  python usecases/swe_day/097_db_index_recommendations/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/097_db_index_recommendations/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "23:50"
BLOCK = "night"
TRIGGER = "cron: 50 23 * * 0"
AUTOMATION = "performance"

USECASE = UseCase(
    id=97,
    domain="swe-" + BLOCK,
    title="Database index recommendations",
    ask="Recommend indexes from this week's slow queries.",
    why="A DBA subagent works through pg_stat_statements in its own context.",
    tools=[TOOL("top_slow_queries", "Top slow queries this week.", [{"q": "invoices WHERE customer_id AND status", "calls": 90000, "mean_ms": 380}]),
           TOOL("existing_indexes", "Indexes on a table.", ["invoices_pkey"], {"table": str})],
    subagents=[SUB("dba", "Reviews query stats and recommends indexes.", ["top_slow_queries", "existing_indexes"],
                   [par(call("top_slow_queries", query="week"), call("existing_indexes", table="invoices")),
                    say("Add (customer_id, status) on invoices; it covers 90k calls/week at 380ms.")])],
    plan=[task("dba", "Recommend indexes from this week's slow queries"),
          say("One index worth adding: invoices(customer_id, status). It covers 90k slow calls a week.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
