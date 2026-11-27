"""The autonomous loop.

Every product in this repo runs some version of this:

    goal
     |
     v
    [context]  role + recalled memory + matching skill + tool list
     |
     v
    [think]    model picks the next action (or decides it's done)
     |
     v
    [guard]    approval gate -> sentinel -> budget        (policy.py)
     |
     v
    [act]      run the tool on connectors / the sandbox computer
     |
     v
    [observe]  append the result; loop until final or max_steps
     |
     v
    [reflect]  write an episode to memory; optionally distil a new skill (Hermes-style)

The loop is short on purpose. The interesting differences between products live in
how they configure it: which tools, which approval mode, who the "human" is, what
triggers a run, and whether several agents share a computer or a thread.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from .llm import LLM, Step
from .memory import Memory, Skill, SkillStore
from .policy import ApprovalGate, Budget, Sentinel
from .tools import Risk, Tool, ToolRegistry, to_text
from .trace import say


@dataclass
class AgentResult:
    agent: str
    goal: str
    final: str
    actions: list[dict] = field(default_factory=list)
    blocked: list[dict] = field(default_factory=list)
    learned_skill: str | None = None

    @property
    def tools_used(self) -> list[str]:
        return [a["tool"] for a in self.actions]


@dataclass
class AutonomousAgent:
    name: str
    role: str
    llm: LLM
    tools: ToolRegistry
    gate: ApprovalGate = field(default_factory=ApprovalGate)
    sentinel: Sentinel | None = None
    budget: Budget | None = None
    memory: Memory | None = None
    skills: SkillStore | None = None
    max_steps: int = 20
    learn_skills: bool = False

    # ------------------------------------------------------------------------------------
    def system_prompt(self, goal: str) -> str:
        parts = [f"You are {self.name}. {self.role}",
                 "Work step by step with the tools. Ask for approval through the tools, "
                 "never claim an action happened unless a tool confirmed it."]
        if self.memory:
            facts = self.memory.recall(goal)
            if facts:
                parts.append("Things you know:\n- " + "\n- ".join(facts))
        if self.skills:
            sk = self.skills.match(goal)
            if sk:
                parts.append(f"Use your skill '{sk.name}':\n" + "\n".join(f"{i}. {s}" for i, s in enumerate(sk.steps, 1)))
        return "\n\n".join(parts)

    # ------------------------------------------------------------------------------------
    def run(self, goal: str, *, tools: ToolRegistry | None = None) -> AgentResult:
        registry = tools or self.tools
        messages: list[dict] = [
            {"role": "system", "content": self.system_prompt(goal)},
            {"role": "user", "content": goal},
        ]
        result = AgentResult(self.name, goal, final="")
        say("agent", self.name, f"goal: {goal[:110]}{'...' if len(goal) > 110 else ''}")

        for _ in range(self.max_steps):
            step: Step = self.llm.next_step(messages, registry.schemas())
            if step.kind == "final":
                result.final = step.text
                say("ok", self.name, f"done: {step.text}")
                break

            if step.tool not in registry:
                obs = f"error: tool {step.tool} is not available to {self.name}"
                result.blocked.append({"tool": step.tool, "reason": "not_available"})
                say("deny", self.name, obs)
                self._append(messages, step, obs)
                continue

            t = registry.get(step.tool)
            if step.text:
                say("agent", self.name, step.text)
            ok, reason = self._guard(t, step.args)
            if not ok:
                obs = f"blocked: {reason}"
                result.blocked.append({"tool": t.name, "args": step.args, "reason": reason})
                self._append(messages, step, obs)
                continue

            try:
                out = t(**step.args)
            except Exception as e:  # tool errors are observations, not crashes
                out = f"error: {e}"
            say("tool", t.name, _preview(out))
            result.actions.append({"tool": t.name, "args": step.args, "result": out})
            self._append(messages, step, to_text(out))
        else:
            result.final = "Stopped: step limit reached."

        self._reflect(result)
        return result

    # ------------------------------------------------------------------------------------
    def _guard(self, t: Tool, args: dict) -> tuple[bool, str]:
        if not self.gate.allow(t, args, who=self.name):
            return False, "not approved"
        if self.sentinel and not self.sentinel.check(t, args):
            return False, "sentinel veto"
        if t.risk is Risk.MONEY and self.budget is not None:
            if not self.budget.charge(float(args.get("amount", 0))):
                return False, "over budget"
        return True, ""

    @staticmethod
    def _append(messages: list[dict], step: Step, observation: str) -> None:
        call_id = step.call_id or f"call_{len(messages)}"
        messages.append({"role": "assistant", "content": step.text or None, "tool_calls": [{
            "id": call_id, "type": "function",
            "function": {"name": step.tool, "arguments": json.dumps(step.args)}}]})
        messages.append({"role": "tool", "tool_call_id": call_id, "content": observation})

    def _reflect(self, result: AgentResult) -> None:
        if self.memory:
            self.memory.log_episode(result.goal, result.final or "no final answer")
        if self.learn_skills and self.skills and result.actions:
            name = "-".join(w for w in result.goal.lower().split()[:4] if w.isalpha()) or "learned-skill"
            if not self.skills.get(name):
                steps = [f"call {a['tool']} with {json.dumps(a['args'])[:80]}" for a in result.actions]
                self.skills.add(Skill(name, f"Learned from: {result.goal[:80]}", steps))
                result.learned_skill = name
                say("ok", self.name, f"learned a new skill: {name}")


def _preview(x: object, n: int = 110) -> str:
    s = to_text(x)
    return s if len(s) <= n else s[: n - 3] + "..."
