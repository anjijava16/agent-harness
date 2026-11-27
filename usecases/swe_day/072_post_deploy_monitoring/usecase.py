"""Post-deploy watch

When:     17:00 (release)
Trigger:  cron: */10 17 * * * (after deploy)
Type:     monitoring

Compares key metrics to the pre-deploy baseline and only speaks up if something moved.

Run:  python usecases/swe_day/072_post_deploy_monitoring/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/072_post_deploy_monitoring/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "17:00"
BLOCK = "release"
TRIGGER = "cron: */10 17 * * * (after deploy)"
AUTOMATION = "monitoring"

USECASE = UseCase(
    id=72,
    domain="swe-" + BLOCK,
    title="Post-deploy watch",
    ask="Watch payments-api for 30 minutes after the deploy.",
    why="Compares key metrics to the pre-deploy baseline and only speaks up if something moved.",
    tools=[TOOL("metrics_vs_baseline", "Metrics compared to baseline.", {"error_rate": "+0%", "p99": "+4%", "throughput": "+1%"}, {"service": str})],
    plan=[call("metrics_vs_baseline", service="payments-api"),
          say("30 minutes after the deploy: errors flat, p99 +4% (within noise). Nothing to do.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
