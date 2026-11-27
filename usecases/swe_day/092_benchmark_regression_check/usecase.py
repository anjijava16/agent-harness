"""Benchmark regression check

When:     23:10 (night)
Trigger:  cron: 10 23 * * *
Type:     performance

Compares tonight's benchmark run with the 7-day median.

Run:  python usecases/swe_day/092_benchmark_regression_check/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/092_benchmark_regression_check/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "23:10"
BLOCK = "night"
TRIGGER = "cron: 10 23 * * *"
AUTOMATION = "performance"

USECASE = UseCase(
    id=92,
    domain="swe-" + BLOCK,
    title="Benchmark regression check",
    ask="Did any benchmark regress more than 10% today?",
    why="Compares tonight's benchmark run with the 7-day median.",
    tools=[TOOL("bench_results", "Benchmark results vs 7-day median.", [{"bench": "fee_calc", "change": "+2%"}, {"bench": "ledger_post", "change": "+18%"}])],
    plan=[call("bench_results", query="tonight"),
          say("ledger_post is 18% slower than its 7-day median. fee_calc is within noise.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
