"""Slow query analysis

When:     14:25 (ops)
Trigger:  webhook: db_slow_query_alert
Type:     performance

Runs EXPLAIN through a read-only tool and recommends an index.

Run:  python usecases/swe_day/055_slow_query_analysis/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/055_slow_query_analysis/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "14:25"
BLOCK = "ops"
TRIGGER = "webhook: db_slow_query_alert"
AUTOMATION = "performance"

USECASE = UseCase(
    id=55,
    domain="swe-" + BLOCK,
    title="Slow query analysis",
    ask="This query on invoices takes 4s. Why?",
    why="Runs EXPLAIN through a read-only tool and recommends an index.",
    tools=[TOOL("explain", "EXPLAIN ANALYZE a query (read-only replica).", "Seq Scan on invoices (rows=8.2M) Filter: customer_id = 42 AND status = 'open'", {"sql": str})],
    plan=[call("explain", sql="SELECT * FROM invoices WHERE customer_id=42 AND status='open'"),
          answer("QueryFix", cause="sequential scan over 8.2M rows", fix="CREATE INDEX CONCURRENTLY ix_invoices_customer_status ON invoices(customer_id, status)")],
    output=("QueryFix", {"cause": str, "fix": str})
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
