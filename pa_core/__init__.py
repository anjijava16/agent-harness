"""pa_core: a small, readable harness for building autonomous personal agents.

Every personal agent product in this repo (Grok Bot, Dots, Claude Duet, Gemini Task,
Muse, Copilot Cowork, Cue, OpenClaw, Instinct, Personal Computer, ...) is built from the
same handful of parts. This package implements those parts in plain Python so you can
read them, run them offline, and swap in a real model when you want.

    llm.py        -> the "brain": ScriptedLLM (offline) and OpenAICompatLLM (live)
    tools.py      -> tool registry with risk levels
    policy.py     -> approval gate, budgets, sentinel egress checks
    memory.py     -> per-agent memory and a skills store (SKILL.md style)
    computer.py   -> sandboxed "cloud computer" with files, browser stub, audit log, undo
    scheduler.py  -> routines, heartbeats and a simulated clock
    connectors.py -> fake inbox / calendar / invoices / chat used by every demo
    agent.py      -> the autonomous loop: plan -> act -> observe -> reflect
    trace.py      -> readable console output
"""

from .agent import AutonomousAgent, AgentResult
from .tools import Tool, ToolRegistry, Risk, tool
from .policy import ApprovalGate, ApprovalMode, Budget, Sentinel
from .memory import Memory, SkillStore
from .computer import SandboxComputer
from .scheduler import Scheduler, Routine, SimClock
from .connectors import Workspace
from .llm import ScriptedLLM, OpenAICompatLLM, LLM, Step

__all__ = [
    "AutonomousAgent", "AgentResult", "Tool", "ToolRegistry", "Risk", "tool",
    "ApprovalGate", "ApprovalMode", "Budget", "Sentinel", "Memory", "SkillStore",
    "SandboxComputer", "Scheduler", "Routine", "SimClock", "Workspace",
    "ScriptedLLM", "OpenAICompatLLM", "LLM", "Step",
]
