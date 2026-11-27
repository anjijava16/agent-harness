"""Trip recap

Area: travel
Totals spending and saves notes for next time.

Run:  python usecases/100_trip_recap/usecase.py                  # your preferred framework
      python usecases/100_trip_recap/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/100_trip_recap/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=100,
    area="travel",
    title="Trip recap",
    ask="Recap the Denver trip: cost and what I'd do again.",
    why="Totals spending and saves notes for next time.",
    tools=[T("trip_spend", "Total trip spending.", {"trip": str}, 955.0)],
    steps=[call("trip_spend", trip="Denver"), remember("trip_denver", "Maven was great; Watercourse Foods yes; skip the 7am flight"),
           answer("The Denver trip cost $955. Notes saved for next time: stay at the Maven again, skip the 7am flight.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
