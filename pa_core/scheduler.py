"""Routines, heartbeats, and a simulated clock.

"Always-on" is mostly a scheduler. The products differ in cadence and trigger:

    Grok Bot      -> Routines: saved prompts that run on a schedule or trigger
    Gemini Task   -> Schedules: "Every Monday at 9:00, scan my inbox..."
    Claude Duet   -> checks connected accounts every few hours, sends a morning brief
    OpenClaw      -> heartbeats: the gateway wakes the agent periodically
    Hermes Agent  -> built-in cron with delivery to any chat platform

SimClock lets the demos "fast forward" a day in milliseconds. In production you would
back this with APScheduler, Cloud Scheduler, a Temporal workflow, or plain cron.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .trace import say


@dataclass
class SimClock:
    minute: int = 6 * 60  # start the day at 06:00

    def advance(self, minutes: int) -> None:
        self.minute += minutes

    @property
    def hhmm(self) -> str:
        h, m = divmod(self.minute % (24 * 60), 60)
        return f"{h:02d}:{m:02d}"


@dataclass
class Routine:
    name: str
    every_minutes: int | None = None     # heartbeat style
    at: str | None = None                # "HH:MM" daily
    action: Callable[[], object] = lambda: None
    last_run: int | None = None
    runs: int = 0

    def due(self, clock: SimClock) -> bool:
        if self.at:
            h, m = map(int, self.at.split(":"))
            target = h * 60 + m
            return clock.minute >= target and (self.last_run is None or self.last_run < target)
        if self.every_minutes:
            return self.last_run is None or clock.minute - self.last_run >= self.every_minutes
        return False


@dataclass
class Scheduler:
    clock: SimClock = field(default_factory=SimClock)
    routines: list[Routine] = field(default_factory=list)

    def add(self, r: Routine) -> None:
        self.routines.append(r)

    def tick(self) -> list[str]:
        fired = []
        for r in self.routines:
            if r.due(self.clock):
                say("agent", "scheduler", f"{self.clock.hhmm} firing routine '{r.name}'")
                r.action()
                r.last_run = self.clock.minute
                r.runs += 1
                fired.append(r.name)
        return fired

    def run_for(self, minutes: int, step: int = 30) -> list[str]:
        fired: list[str] = []
        end = self.clock.minute + minutes
        while self.clock.minute < end:
            fired += self.tick()
            self.clock.advance(step)
        return fired
