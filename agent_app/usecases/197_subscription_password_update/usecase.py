"""Update a card on file

Area: digital
Lists services with the old card on file. You update them yourself; card details never go
through the agent.

Run:  python usecases/197_subscription_password_update/usecase.py                  # your preferred framework
      python usecases/197_subscription_password_update/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/197_subscription_password_update/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=197,
    area="digital",
    title="Update a card on file",
    ask="My card was replaced. Which services have the old one?",
    why="Lists services with the old card on file. You update them yourself; card details never go through the agent.",
    tools=[T("services_with_card", "Services charging a card.", {"card_last4": str}, ["StreamPlus", "Cloud storage", "Gym"])],
    steps=[call("services_with_card", card_last4="4417"),
           answer("3 services still use the card ending 4417: Cloud storage, Gym and StreamPlus. Update each in its own app.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
