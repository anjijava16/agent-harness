"""Instinct (Spear Street Technology, Inc. - invite-only, 2026).

Architecture notes
------------------
* "There are no new interfaces": you text it or call it. No app with buttons.
* Connects to your mail, messaging, calendar and devices, and is trained to use a phone
  and a computer the way a person would.
* Runs on a persistent cloud computer with browser access and cached credentials on the
  company's servers. Not self-hostable. Pricing not published.
* Privacy is the main critique: it can ask for audio, location and screen data.

The pattern worth stealing is the *transport*: an SMS/voice webhook in front of an
agent. Everything else (tools, approvals) is the same loop. Approvals happen in the
same text thread ("Reply YES to send").

Programmability
---------------
No public API. Mock = SMS thread in front of the harness with in-thread approvals.
Live = the same loop driven by any OpenAI-compatible model; wire `on_sms` to a Twilio
(or similar) webhook to make it real.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pa_core import (ApprovalGate, ApprovalMode, AutonomousAgent, ScriptedLLM, ToolRegistry,
                     Workspace)
from pa_core.cli import main, require_env
from pa_core.connectors import MORNING_GOAL
from pa_core.llm import LLM, OpenAICompatLLM
from pa_core.scenarios import morning_script
from pa_core.trace import banner, say, section


@dataclass
class SmsThread:
    """The whole UI. Outbound messages go here; your replies are queued in `replies`."""

    number: str
    log: list[tuple[str, str]] = field(default_factory=list)
    replies: list[str] = field(default_factory=list)

    def to_user(self, text: str) -> None:
        self.log.append(("instinct", text))
        say("agent", f"SMS->{self.number}", text)

    def from_user(self) -> str:
        r = self.replies.pop(0) if self.replies else "NO"
        self.log.append(("you", r))
        say("ok", f"SMS<-{self.number}", r)
        return r


class InstinctLike:
    def __init__(self, llm: LLM, thread: SmsThread):
        self.ws = Workspace()
        self.thread = thread

        def ask_by_text(t, args) -> bool:  # noqa: ANN001
            what = args.get("to") or args.get("channel") or args.get("merchant")
            thread.to_user(f"OK to {t.name.replace('_', ' ')} -> {what}? Reply YES or NO")
            return thread.from_user().strip().upper().startswith("Y")

        self.agent = AutonomousAgent("Instinct", "A personal assistant you text.", llm,
                                     ToolRegistry(self.ws.tools()),
                                     gate=ApprovalGate(ApprovalMode.RISK_BASED, human=ask_by_text))

    def on_sms(self, body: str) -> str:
        """Webhook handler: inbound SMS -> agent run -> outbound SMS."""
        result = self.agent.run(body)
        self.thread.to_user(result.final)
        return result.final


def run_mock() -> dict:
    banner("Instinct - an agent you text, approvals inside the SMS thread (mock)")
    thread = SmsThread("+1 415 555 0199", replies=["YES", "NO", "YES"])
    bot = InstinctLike(ScriptedLLM(morning_script(channel="#ops")), thread)
    section("You text: 'morning ops pls'")
    bot.on_sms(MORNING_GOAL)
    return {"sms_messages": len(thread.log), "workspace": bot.ws.summary()}


def run_live() -> None:
    require_env("PA_API_KEY")
    banner("Instinct build-alike - live model, terminal as the SMS thread")
    thread = SmsThread("terminal")
    thread.from_user = lambda: input("you> ")  # type: ignore[method-assign]
    bot = InstinctLike(OpenAICompatLLM(), thread)
    bot.on_sms(input("text Instinct> ") or MORNING_GOAL)


if __name__ == "__main__":
    main(run_mock, run_live)
