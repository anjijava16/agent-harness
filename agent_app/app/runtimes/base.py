"""What every runtime implements, and the context a run carries."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ..spec import Step, UseCase, system_prompt
from ..tools import ToolRuntime


@dataclass
class RunCtx:
    run_id: str
    user_id: str
    uc: UseCase
    prefs: dict
    mode: str                 # scripted | live
    ask: str
    steps: list[Step]
    tools: ToolRuntime

    @property
    def prompt(self) -> str:
        return system_prompt(self.uc, self.prefs)

    @property
    def scripted(self) -> bool:
        return self.mode == "scripted"


@dataclass
class Outcome:
    status: str                                   # done | paused | error
    final: str = ""
    pending: list = field(default_factory=list)   # [{"id", "tool", "args"}]
    error: str = ""


class Runtime(ABC):
    name = "base"

    @abstractmethod
    async def start(self, ctx: RunCtx) -> Outcome: ...

    @abstractmethod
    async def resume(self, ctx: RunCtx, decisions: list[dict]) -> Outcome:
        """decisions line up with the last Outcome.pending:
        {"type": "approve"} | {"type": "reject", "message": str} | {"type": "edit", "args": {full args}}"""
