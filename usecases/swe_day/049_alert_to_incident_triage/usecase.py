"""Alert to incident triage

When:     13:30 (ops)
Trigger:  webhook: alertmanager
Type:     incident response

Pulls metrics, logs and recent deploys in parallel; the triage note is written before a
human joins.

Run:  python usecases/swe_day/049_alert_to_incident_triage/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/049_alert_to_incident_triage/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "13:30"
BLOCK = "ops"
TRIGGER = "webhook: alertmanager"
AUTOMATION = "incident response"

USECASE = UseCase(
    id=49,
    domain="swe-" + BLOCK,
    title="Alert to incident triage",
    ask="High 5xx on checkout. Triage.",
    why="Pulls metrics, logs and recent deploys in parallel; the triage note is written before a human joins.",
    tools=[TOOL("error_rate", "5xx rate for a service.", {"now": 0.08, "baseline": 0.002}, {"service": str}),
           TOOL("recent_deploys", "Deploys in the last N hours.", [{"service": "checkout", "version": "v2.31.0", "mins_ago": 12}], {"hours": int}),
           TOOL("top_errors", "Most common error lines.", ["KeyError: 'currency' in pricing.py:88 (2,104x)"], {"service": str})],
    plan=[par(call("error_rate", service="checkout"), call("recent_deploys", hours=2), call("top_errors", service="checkout")),
          write("/incidents/checkout-5xx.md", "Started ~12m after v2.31.0. KeyError currency pricing.py:88. Suspect deploy.\n"),
          say("5xx at 8% (baseline 0.2%), started 12 minutes after checkout v2.31.0. Top error: KeyError 'currency' in pricing.py:88. Rollback is the likely fix.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
