"""Breaking API change detector

When:     13:20 (review)
Trigger:  webhook: pull_request.opened
Type:     API governance

Diffs the OpenAPI spec between main and the branch and names breaking changes.

Run:  python usecases/swe_day/047_breaking_api_change_detector/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/047_breaking_api_change_detector/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "13:20"
BLOCK = "review"
TRIGGER = "webhook: pull_request.opened"
AUTOMATION = "API governance"

USECASE = UseCase(
    id=47,
    domain="swe-" + BLOCK,
    title="Breaking API change detector",
    ask="Does PR #823 break the public API?",
    why="Diffs the OpenAPI spec between main and the branch and names breaking changes.",
    tools=[TOOL("openapi_diff", "Diff two OpenAPI specs.", [{"change": "removed field", "path": "Invoice.due_date", "breaking": True},
                                                           {"change": "added field", "path": "Invoice.currency", "breaking": False}], {"base": str, "head": str})],
    plan=[call("openapi_diff", base="main", head="pr-823"),
          say("Yes: removing Invoice.due_date breaks clients. Adding currency is fine. Deprecate due_date first instead.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
