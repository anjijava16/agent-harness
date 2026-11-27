"""Story point estimate from history

When:     08:50 (planning)
Trigger:  manual
Type:     estimation

Grounds estimates in data instead of gut feel.

Run:  python usecases/swe_day/015_story_point_estimate/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/015_story_point_estimate/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "08:50"
BLOCK = "planning"
TRIGGER = "manual"
AUTOMATION = "estimation"

USECASE = UseCase(
    id=15,
    domain="swe-" + BLOCK,
    title="Story point estimate from history",
    ask="Estimate PAY-440 based on similar past tickets.",
    why="Grounds estimates in data instead of gut feel.",
    tools=[TOOL("similar_tickets", "Past tickets similar to a description.",
                [{"key": "PAY-201", "title": "Export payments CSV", "points": 3, "days": 2}, {"key": "PAY-260", "title": "PDF export", "points": 5, "days": 4}],
                {"text": str})],
    plan=[call("similar_tickets", text="export invoices as CSV"),
          answer("Estimate", points=3, confidence="medium", based_on=["PAY-201"])],
    output=("Estimate", {"points": int, "confidence": str, "based_on": list})
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
