"""New security advisories for our dependencies

When:     07:55 (morning)
Trigger:  cron: 55 7 * * *
Type:     scheduled scan

Matches new advisories against each service's lockfile and opens tickets only for
reachable ones.

Run:  python usecases/swe_day/010_dependency_security_advisories/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/010_dependency_security_advisories/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "07:55"
BLOCK = "morning"
TRIGGER = "cron: 55 7 * * *"
AUTOMATION = "scheduled scan"

USECASE = UseCase(
    id=10,
    domain="swe-" + BLOCK,
    title="New security advisories for our dependencies",
    ask="Any new CVEs affecting our services?",
    why="Matches new advisories against each service's lockfile and opens tickets only for reachable ones.",
    tools=[TOOL("new_advisories", "Advisories published in the last day.", [{"id": "CVE-2026-4412", "pkg": "urllib3", "fixed": "2.5.1"}]),
           TOOL("services_using", "Services that depend on a package and version.", [{"svc": "payments-api", "version": "2.4.0"}], {"pkg": str}),
           TOOL("create_ticket", "Create a Jira ticket.", "SEC-201", {"title": str, "priority": str}, "write")],
    plan=[call("new_advisories", query="24h"), call("services_using", pkg="urllib3"),
          call("create_ticket", title="Bump urllib3 to 2.5.1 in payments-api (CVE-2026-4412)", priority="P2"),
          say("CVE-2026-4412 (urllib3) affects payments-api 2.4.0. Opened SEC-201 to bump to 2.5.1.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
