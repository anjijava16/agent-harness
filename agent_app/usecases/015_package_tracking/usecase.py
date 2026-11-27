"""Packages arriving today

Area: mornings
Checks every carrier at once.

Run:  python usecases/015_package_tracking/usecase.py                  # your preferred framework
      python usecases/015_package_tracking/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/015_package_tracking/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=15,
    area="mornings",
    title="Packages arriving today",
    ask="Are any packages coming today?",
    why="Checks every carrier at once.",
    tools=[T("track", "Track packages with a carrier.", {"carrier": str}, lambda carrier: {"ups": [{"item": "running shoes", "eta": "today 2-6pm"}], "fedex": [], "usps": [{"item": "library book", "eta": "tomorrow"}]}[carrier])],
    steps=[par(call("track", carrier="ups"), call("track", carrier="fedex"), call("track", carrier="usps")),
           answer("One today: the running shoes (UPS, 2-6pm). The library book comes tomorrow.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
