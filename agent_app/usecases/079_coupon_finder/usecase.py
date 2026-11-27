"""Coupons before I check out

Area: errands
Tries the available codes and keeps the best one.

Run:  python usecases/079_coupon_finder/usecase.py                  # your preferred framework
      python usecases/079_coupon_finder/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/079_coupon_finder/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=79,
    area="errands",
    title="Coupons before I check out",
    ask="Any coupons for my HomeMart cart?",
    why="Tries the available codes and keeps the best one.",
    tools=[T("try_codes", "Try coupon codes on a cart.", {"store": str}, [{"code": "SAVE10", "saves": 10.0}, {"code": "FREESHIP", "saves": 6.99}])],
    steps=[call("try_codes", store="HomeMart"), answer("SAVE10 saves the most ($10). FREESHIP only saves $6.99.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
