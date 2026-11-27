"""API usage analytics

When:     23:30 (night)
Trigger:  cron: 30 23 * * 0
Type:     analytics

Tells you which clients to chase before turning v1 off.

Run:  python usecases/swe_day/094_api_usage_analytics/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/094_api_usage_analytics/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "23:30"
BLOCK = "night"
TRIGGER = "cron: 30 23 * * 0"
AUTOMATION = "analytics"

USECASE = UseCase(
    id=94,
    domain="swe-" + BLOCK,
    title="API usage analytics",
    ask="Who still calls the deprecated v1 endpoints?",
    why="Tells you which clients to chase before turning v1 off.",
    tools=[TOOL("endpoint_usage", "Calls per client for an endpoint prefix.", [{"client": "mobile-ios-5.2", "calls": 12000}, {"client": "partner-acme", "calls": 300}], {"prefix": str})],
    plan=[call("endpoint_usage", prefix="/v1/"),
          answer("V1Usage", clients=["mobile-ios-5.2", "partner-acme"], total_calls=12300)],
    output=("V1Usage", {"clients": list, "total_calls": int})
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
