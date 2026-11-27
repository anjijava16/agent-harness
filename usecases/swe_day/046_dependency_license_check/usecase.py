"""License check on new dependencies

When:     13:15 (review)
Trigger:  webhook: pull_request.opened
Type:     compliance

Catches a GPL dependency before legal does.

Run:  python usecases/swe_day/046_dependency_license_check/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/046_dependency_license_check/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "13:15"
BLOCK = "review"
TRIGGER = "webhook: pull_request.opened"
AUTOMATION = "compliance"

USECASE = UseCase(
    id=46,
    domain="swe-" + BLOCK,
    title="License check on new dependencies",
    ask="Do the new deps in PR #822 have acceptable licenses?",
    why="Catches a GPL dependency before legal does.",
    tools=[TOOL("new_dependencies", "Dependencies added in a PR.", [{"name": "httpx", "license": "BSD"}, {"name": "pdfmagic", "license": "AGPL-3.0"}], {"pr": int})],
    agents_md="# License policy\nAllowed: MIT, BSD, Apache-2.0. Needs legal: GPL, AGPL, LGPL.\n",
    plan=[call("new_dependencies", pr=822),
          answer("LicenseReport", ok=["httpx"], needs_legal=["pdfmagic (AGPL-3.0)"])],
    output=("LicenseReport", {"ok": list, "needs_legal": list})
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
