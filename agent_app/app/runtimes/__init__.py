"""Runtime registry. Imports are lazy so a missing framework only matters if you pick it."""

from __future__ import annotations

import importlib

from .base import Outcome, RunCtx, Runtime

_PATHS = {
    "deepagents": ("deepagents_rt", "DeepAgentsRuntime", "deepagents"),
    "langgraph": ("langgraph_rt", "LangGraphRuntime", "langgraph"),
    "adk": ("adk_rt", "AdkRuntime", "google.adk"),
    "claude": ("claude_rt", "ClaudeRuntime", "claude_agent_sdk"),
}
LABELS = {"deepagents": "LangChain Deep Agents", "langgraph": "LangGraph", "adk": "Google ADK", "claude": "Claude Agent SDK"}


def available() -> dict[str, bool]:
    out = {}
    for k, (_, _, pkg) in _PATHS.items():
        try:
            importlib.import_module(pkg)
            out[k] = True
        except Exception:  # noqa: BLE001
            out[k] = False
    return out


def get(name: str) -> Runtime:
    if name not in _PATHS:
        raise ValueError(f"unknown framework {name!r}; pick one of {list(_PATHS)}")
    mod, cls, _ = _PATHS[name]
    return getattr(importlib.import_module(f"{__name__}.{mod}"), cls)()


__all__ = ["LABELS", "Outcome", "RunCtx", "Runtime", "available", "get"]
