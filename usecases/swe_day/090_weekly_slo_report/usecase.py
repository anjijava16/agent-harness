"""Weekly SLO report

When:     22:45 (night)
Trigger:  cron: 45 22 * * 5
Type:     reporting

Pulls all SLOs in parallel and writes a report people actually skim.

Run:  python usecases/swe_day/090_weekly_slo_report/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/090_weekly_slo_report/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "22:45"
BLOCK = "night"
TRIGGER = "cron: 45 22 * * 5"
AUTOMATION = "reporting"

USECASE = UseCase(
    id=90,
    domain="swe-" + BLOCK,
    title="Weekly SLO report",
    ask="Write the weekly SLO report.",
    why="Pulls all SLOs in parallel and writes a report people actually skim.",
    tools=[TOOL("slo", "SLO attainment for a service this week.", lambda service: {"payments-api": 99.95, "checkout": 99.71, "ledger": 99.99}[service], {"service": str})],
    plan=[par(call("slo", service="payments-api"), call("slo", service="checkout"), call("slo", service="ledger")),
          write("/reports/slo-weekly.md", "payments-api 99.95 (target 99.9) OK\ncheckout 99.71 (target 99.9) MISSED: INC-77\nledger 99.99 OK\n"),
          say("Checkout missed its SLO (99.71% vs 99.9%) because of INC-77. Others are fine.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
