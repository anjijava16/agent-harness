"""Policy layer: who decides whether an action actually happens.

This is the part that separates a toy agent from one you'd hand your inbox to.
Three mechanisms cover what the commercial products ship:

ApprovalGate  -> "ask me before X". Modes:
                   AUTO       approve everything (dangerous, demos only)
                   RISK_BASED approve READ/WRITE, ask for EXTERNAL/MONEY  (Dots, Duet, Gemini Task)
                   EVERY      ask for every non-read action             (Copilot Cowork)
                   DENY_ALL   read-only mode                             (Dots background research)
Budget        -> hard spend caps per agent (Cue's wallet, Muse's Link checkout limits)
Sentinel      -> a separate checker that sits between the agent and the network and
                 can veto egress (Meta Muse's Sentinel agent). It does not trust the
                 worker agent's reasoning; it only looks at the concrete action.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

from .tools import Risk, Tool
from .trace import say


class ApprovalMode(str, Enum):
    AUTO = "auto"
    RISK_BASED = "risk_based"
    EVERY = "every"
    DENY_ALL = "deny_all"


# A "human" is just a callback: (tool, args) -> bool. Demos script it; real apps push a
# notification, a Slack button, or an SMS and wait for the reply.
Human = Callable[[Tool, dict], bool]


def always_yes(t: Tool, args: dict) -> bool:  # noqa: ARG001
    return True


def always_no(t: Tool, args: dict) -> bool:  # noqa: ARG001
    return False


@dataclass
class ApprovalGate:
    mode: ApprovalMode = ApprovalMode.RISK_BASED
    human: Human = always_yes
    log: list[dict] = field(default_factory=list)

    def needs_human(self, t: Tool) -> bool:
        if self.mode is ApprovalMode.AUTO:
            return False
        if self.mode is ApprovalMode.EVERY:
            return t.risk > Risk.READ
        if self.mode is ApprovalMode.RISK_BASED:
            return t.risk >= Risk.EXTERNAL
        return t.risk > Risk.READ  # DENY_ALL handled in allow()

    def allow(self, t: Tool, args: dict, who: str = "agent") -> bool:
        if self.mode is ApprovalMode.DENY_ALL and t.risk > Risk.READ:
            say("deny", "policy", f"{t.name} blocked: agent is in read-only mode")
            self.log.append({"tool": t.name, "decision": "blocked_readonly"})
            return False
        if not self.needs_human(t):
            self.log.append({"tool": t.name, "decision": "auto"})
            return True
        say("warn", "approval", f"{who} wants to run {t.name}({_short(args)}) -> asking you")
        ok = bool(self.human(t, args))
        say("ok" if ok else "deny", "approval", "approved" if ok else "rejected")
        self.log.append({"tool": t.name, "decision": "approved" if ok else "rejected"})
        return ok


@dataclass
class Budget:
    limit: float
    spent: float = 0.0

    def charge(self, amount: float) -> bool:
        if self.spent + amount > self.limit:
            say("deny", "budget", f"charge ${amount:.2f} refused, ${self.remaining():.2f} left")
            return False
        self.spent += amount
        return True

    def remaining(self) -> float:
        return round(self.limit - self.spent, 2)


@dataclass
class Sentinel:
    """Egress checker. Rules are deliberately dumb and deterministic.

    allowed_domains: where data may go. Anything else needs a human.
    blocked_terms:   strings that must never leave the machine (card numbers, SSNs...).
    """

    allowed_domains: set[str] = field(default_factory=set)
    allowed_channels: set[str] = field(default_factory=set)
    blocked_terms: list[str] = field(default_factory=list)
    human: Human = always_no
    log: list[dict] = field(default_factory=list)

    def check(self, t: Tool, args: dict) -> bool:
        if t.risk < Risk.EXTERNAL:
            return True
        blob = " ".join(str(v) for v in args.values()).lower()
        for term in self.blocked_terms:
            if term.lower() in blob:
                say("deny", "sentinel", f"blocked {t.name}: payload contains a protected value")
                self.log.append({"tool": t.name, "decision": "blocked_term"})
                return False
        if args.get("channel") in self.allowed_channels:
            self.log.append({"tool": t.name, "decision": "allowed_channel", "dest": args["channel"]})
            return True
        dest = str(args.get("to") or args.get("url") or args.get("channel") or args.get("merchant") or "")
        domain = dest.split("@")[-1].split("/")[0] if dest else ""
        if domain and any(domain.endswith(d) for d in self.allowed_domains):
            self.log.append({"tool": t.name, "decision": "allowed_domain", "dest": dest})
            say("ok", "sentinel", f"egress to {dest} allowed by rule")
            return True
        say("warn", "sentinel", f"{t.name} -> {dest or 'unknown'} is not on the allowlist, asking you")
        ok = bool(self.human(t, args))
        self.log.append({"tool": t.name, "decision": "human_ok" if ok else "human_no", "dest": dest})
        return ok


def _short(args: dict, n: int = 70) -> str:
    s = ", ".join(f"{k}={v!r}" for k, v in args.items())
    return s if len(s) <= n else s[: n - 3] + "..."
