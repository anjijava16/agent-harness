"""Why is the Wi-Fi slow

Area: digital
Checks the router and the connected devices, then restarts after approval.

Run:  python usecases/190_wifi_troubleshoot/usecase.py                  # your preferred framework
      python usecases/190_wifi_troubleshoot/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/190_wifi_troubleshoot/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=190,
    area="digital",
    title="Why is the Wi-Fi slow",
    ask="The Wi-Fi is slow. What's wrong?",
    why="Checks the router and the connected devices, then restarts after approval.",
    tools=[T("router_status", "Router status.", {"router": str}, {"speed_mbps": 18, "plan_mbps": 300, "top_user": "Living room TV (4K stream)"}),
           T("restart_router", "Restart the router.", {"router": str}, "restarted", "write")],
    steps=[call("router_status", router="home"), call("restart_router", router="home"),
           answer("You were getting 18 of your 300 Mbps, and the TV was streaming 4K. The router restarted; test again in 2 minutes.")],
    approvals={"restart_router": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
