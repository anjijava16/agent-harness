"""The brain. Two implementations behind one tiny interface.

    next_step(messages, tools) -> Step

ScriptedLLM      offline. Replays a planned list of steps, so every demo runs with no
                 keys and gives the same output every time (good for tests and for
                 reading the flow).
OpenAICompatLLM  live. Any endpoint that speaks OpenAI chat-completions tool calling:
                 OpenAI, xAI (https://api.x.ai/v1), OpenRouter, Azure OpenAI, Ollama,
                 vLLM, an OpenClaw gateway, LiteLLM proxy... Set PA_BASE_URL, PA_API_KEY,
                 PA_MODEL and the same agent loop drives a real model.

Vendor-native SDKs (xai-sdk, claude-agent-sdk, google-adk, deepagents, openai-agents,
openai-codex, cursor-sdk) are used directly in the service examples; they bring their
own loops, and the examples show how their concepts map onto this one.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol


@dataclass
class Step:
    kind: str                       # "tool" or "final"
    tool: str = ""
    args: dict = field(default_factory=dict)
    text: str = ""                  # final answer, or the model's short rationale
    call_id: str = ""

    @staticmethod
    def call(tool: str, thought: str = "", **args: Any) -> "Step":
        return Step("tool", tool=tool, args=args, text=thought)

    @staticmethod
    def final(text: str) -> "Step":
        return Step("final", text=text)


class LLM(Protocol):
    def next_step(self, messages: list[dict], tools: list[dict]) -> Step: ...


class ScriptedLLM:
    """Replays steps. A step can also be a callable(messages) -> Step for branching."""

    def __init__(self, steps: list[Step | Callable[[list[dict]], Step]]):
        self._steps = list(steps)
        self._i = 0

    def next_step(self, messages: list[dict], tools: list[dict]) -> Step:  # noqa: ARG002
        if self._i >= len(self._steps):
            return Step.final("Done.")
        s = self._steps[self._i]
        self._i += 1
        return s(messages) if callable(s) else s


class OpenAICompatLLM:
    def __init__(self, model: str | None = None, base_url: str | None = None,
                 api_key: str | None = None, temperature: float = 0.2):
        from openai import OpenAI  # imported lazily so mock mode needs no deps

        self.model = model or os.environ.get("PA_MODEL", "gpt-4.1-mini")
        self.client = OpenAI(
            base_url=base_url or os.environ.get("PA_BASE_URL") or None,
            api_key=api_key or os.environ.get("PA_API_KEY") or os.environ.get("OPENAI_API_KEY"),
        )
        self.temperature = temperature

    def next_step(self, messages: list[dict], tools: list[dict]) -> Step:
        resp = self.client.chat.completions.create(
            model=self.model, messages=messages, tools=tools or None,
            temperature=self.temperature,
        )
        msg = resp.choices[0].message
        if msg.tool_calls:
            tc = msg.tool_calls[0]
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            return Step("tool", tool=tc.function.name, args=args, text=msg.content or "", call_id=tc.id)
        return Step.final(msg.content or "")


def from_env_or_script(script: list[Step]) -> LLM:
    """Use a real model if PA_LIVE=1 and a key is present, otherwise replay the script."""
    if os.environ.get("PA_LIVE") == "1" and (os.environ.get("PA_API_KEY") or os.environ.get("OPENAI_API_KEY")):
        return OpenAICompatLLM()
    return ScriptedLLM(script)
