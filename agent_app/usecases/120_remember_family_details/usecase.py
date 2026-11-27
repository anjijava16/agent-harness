"""Remember family details

Area: home
Saves it so meal planning uses it.

Run:  python usecases/120_remember_family_details/usecase.py                  # your preferred framework
      python usecases/120_remember_family_details/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/120_remember_family_details/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=120,
    area="home",
    title="Remember family details",
    ask="Remember: Maya likes cheese and pasta, hates mushrooms.",
    why="Saves it so meal planning uses it.",
    tools=[],
    steps=[remember("family_likes", "Maya: likes cheese, pasta; hates mushrooms"), answer("Noted: cheese and pasta yes, mushrooms no.")],
    expect=[("likes saved", lambda c: "mushrooms" in c["memories"].get("family_likes", ""))]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
