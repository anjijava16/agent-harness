"""Memory and skills.

Memory   -> facts and episode notes per agent. Grok Bot keeps individual Bot memory even
            when Bots share one computer; OpenClaw and Hermes keep it in files on disk.
SkillStore -> reusable procedures written as SKILL.md files (the agentskills.io format
            used by Claude, Hermes, OpenClaw/ClawHub and Gemini Task "Skills").
            A skill is just: name, when to use it, and the steps.

Both are file-backed JSON/Markdown so you can open them and see what the agent "knows".
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Memory:
    owner: str
    root: Path | None = None
    facts: list[str] = field(default_factory=list)
    episodes: list[dict] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.root:
            self.root.mkdir(parents=True, exist_ok=True)
            p = self._path()
            if p.exists():
                data = json.loads(p.read_text())
                self.facts, self.episodes = data.get("facts", []), data.get("episodes", [])

    def _path(self) -> Path:
        assert self.root
        return self.root / f"{self.owner}.memory.json"

    def remember(self, fact: str) -> None:
        if fact not in self.facts:
            self.facts.append(fact)
            self._save()

    def log_episode(self, goal: str, outcome: str) -> None:
        self.episodes.append({"goal": goal, "outcome": outcome})
        self.episodes = self.episodes[-50:]
        self._save()

    def recall(self, query: str, k: int = 5) -> list[str]:
        """Keyword recall. Real systems use embeddings; the interface is the same."""
        words = {w for w in re.findall(r"\w+", query.lower()) if len(w) > 3}
        scored = [(sum(w in f.lower() for w in words), f) for f in self.facts]
        return [f for s, f in sorted(scored, reverse=True) if s > 0][:k]

    def _save(self) -> None:
        if self.root:
            self._path().write_text(json.dumps({"facts": self.facts, "episodes": self.episodes}, indent=2))


@dataclass
class Skill:
    name: str
    description: str
    steps: list[str]

    def to_markdown(self) -> str:
        body = "\n".join(f"{i}. {s}" for i, s in enumerate(self.steps, 1))
        return f"---\nname: {self.name}\ndescription: {self.description}\n---\n\n# {self.name}\n\n{body}\n"

    @staticmethod
    def from_markdown(text: str) -> "Skill":
        name = re.search(r"^name:\s*(.+)$", text, re.M).group(1).strip()
        desc = re.search(r"^description:\s*(.+)$", text, re.M).group(1).strip()
        steps = re.findall(r"^\d+\.\s+(.+)$", text, re.M)
        return Skill(name, desc, steps)


class SkillStore:
    def __init__(self, root: Path | None = None):
        self.root = root
        self._skills: dict[str, Skill] = {}
        if root:
            root.mkdir(parents=True, exist_ok=True)
            for p in root.glob("*/SKILL.md"):
                s = Skill.from_markdown(p.read_text())
                self._skills[s.name] = s

    def add(self, skill: Skill) -> Path | None:
        self._skills[skill.name] = skill
        if self.root:
            d = self.root / skill.name
            d.mkdir(parents=True, exist_ok=True)
            p = d / "SKILL.md"
            p.write_text(skill.to_markdown())
            return p
        return None

    def get(self, name: str) -> Skill | None:
        return self._skills.get(name)

    def match(self, goal: str) -> Skill | None:
        """Pick a skill whose name or description overlaps the goal."""
        g = goal.lower()
        best, score = None, 0
        for s in self._skills.values():
            words = set(re.findall(r"\w+", (s.name + " " + s.description).lower()))
            sc = sum(1 for w in words if len(w) > 3 and w in g)
            if sc > score:
                best, score = s, sc
        return best

    def names(self) -> list[str]:
        return list(self._skills)
