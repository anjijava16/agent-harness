"""Wake-up routine

Area: mornings
Turns on the lights and coffee. Unlocking the front door is blocked by a guard, whatever the
model decides.

Run:  python usecases/004_wake_up_routine/usecase.py                  # your preferred framework
      python usecases/004_wake_up_routine/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/004_wake_up_routine/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=4,
    area="mornings",
    title="Wake-up routine",
    ask="Run my wake-up routine.",
    why="Turns on the lights and coffee. Unlocking the front door is blocked by a guard, whatever the model decides.",
    tools=[T("set_lights", "Set lights in a room.", {"room": str, "level": int}, "ok", "write"),
           T("start_coffee", "Start the coffee machine.", {"size": str}, "brewing", "write"),
           T("unlock_door", "Unlock a door.", {"door": str}, "unlocked", "write")],
    steps=[par(call("set_lights", room="bedroom", level=40), call("start_coffee", size="large")),
           call("unlock_door", door="front"),
           answer("Lights at 40% and coffee is brewing. I didn't unlock the front door; the routine never does that.")],
    guards={"unlock_door": lambda a, p: "routines never unlock doors"},
    expect=[("door stayed locked", lambda c: c["blocked"] and c["blocked"][0]["tool"] == "unlock_door")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
