"""Overnight cloud cost anomaly

When:     07:50 (morning)
Trigger:  cron: 50 7 * * *
Type:     scheduled check

Compares yesterday to the 7-day baseline per service and names the resource behind any
spike.

Run:  python usecases/swe_day/009_aws_cost_anomaly_check/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/009_aws_cost_anomaly_check/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "07:50"
BLOCK = "morning"
TRIGGER = "cron: 50 7 * * *"
AUTOMATION = "scheduled check"

USECASE = UseCase(
    id=9,
    domain="swe-" + BLOCK,
    title="Overnight cloud cost anomaly",
    ask="Did our AWS spend do anything weird overnight?",
    why="Compares yesterday to the 7-day baseline per service and names the resource behind any spike.",
    tools=[TOOL("daily_cost", "Daily cost by service.", {"ec2": 1320, "nat_gateway": 940, "s3": 210}, {"day": str}),
           TOOL("baseline_cost", "7-day average by service.", {"ec2": 1300, "nat_gateway": 180, "s3": 205}),
           TOOL("top_resources", "Top cost resources for a service.", [{"id": "nat-0a1", "gb_out": 21000}], {"service": str})],
    plan=[par(call("daily_cost", day="yesterday"), call("baseline_cost", query="7d")), call("top_resources", service="nat_gateway"),
          say("NAT gateway cost jumped to $940 (5x baseline) from nat-0a1 moving 21 TB. Likely a job pulling data cross-AZ; worth checking.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
