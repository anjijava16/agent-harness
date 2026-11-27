"""Travel money setup

Area: travel
Adds a travel notice. Changing card settings needs approval.

Run:  python usecases/092_currency_and_cards/usecase.py                  # your preferred framework
      python usecases/092_currency_and_cards/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/092_currency_and_cards/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=92,
    area="travel",
    title="Travel money setup",
    ask="Set up my card for the Spain trip.",
    why="Adds a travel notice. Changing card settings needs approval.",
    tools=[T("travel_notice", "Add a travel notice to a card.", {"card": str, "country": str, "dates": str}, "added", "write")],
    steps=[call("travel_notice", card="Visa ending 4417", country="Spain", dates="Apr 3-13"),
           answer("A travel notice is on the Visa ending 4417 for Spain, Apr 3-13.")],
    approvals={"travel_notice": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
