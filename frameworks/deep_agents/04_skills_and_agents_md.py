"""Deep Agents: skills=[...] and memory=[...] (AGENTS.md).

* memory=["/AGENTS.md"]  - always-loaded instructions (house rules), read from the backend
* skills=["/skills/"]    - a catalog of SKILL.md folders. Only names + descriptions go in
                           the prompt; the agent reads the full file when it decides a skill
                           applies (progressive disclosure, same format as Claude skills)

FilesystemBackend points at a real folder, so you can see and edit these files.

Use case: a team-wide "collections" skill and house rules, shipped as files in a repo.
"""

import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from deepagents import create_deep_agent  # noqa: E402
from deepagents.backends import FilesystemBackend  # noqa: E402

from frameworks._fakes.lc_fake import ScriptedChatModel, call, say  # noqa: E402

root = pathlib.Path(tempfile.mkdtemp(prefix="deepagent_"))
(root / "skills" / "overdue-invoice-reminders").mkdir(parents=True)
(root / "AGENTS.md").write_text("# House rules\n- Never send without approval.\n- Sign off '- Acme Studio'.\n")
(root / "skills" / "overdue-invoice-reminders" / "SKILL.md").write_text(
    "---\nname: overdue-invoice-reminders\n"
    "description: Use when drafting reminders for overdue invoices.\n---\n\n"
    "1. Restate amount and days overdue\n2. Include https://pay.acme.studio/<id>\n"
    "3. Friendly under 30 days, firm after\n")


SEEN_PROMPTS: list = []


class CapturingModel(ScriptedChatModel):
    """Records the system prompt the harness built, so we can show what got injected."""

    def _generate(self, messages, *a, **k):  # noqa: ANN001, ANN002, ANN003
        SEEN_PROMPTS.append(messages[0].content if messages else "")
        return super()._generate(messages, *a, **k)


m = CapturingModel(messages=iter([
    call("read_file", {"file_path": "/skills/overdue-invoice-reminders/SKILL.md"}, "s1"),
    say("Hi Northwind team, INV-1038 ($2,400) is 14 days overdue. Pay: https://pay.acme.studio/INV-1038 - Acme Studio"),
]))
agent = create_deep_agent(model=m, backend=FilesystemBackend(root_dir=root, virtual_mode=True),
                          skills=["/skills/"], memory=["/AGENTS.md"])

if __name__ == "__main__":
    r = agent.invoke({"messages": [{"role": "user", "content": "Draft a reminder for Northwind INV-1038"}]})
    prompt = str(SEEN_PROMPTS[0])
    print("AGENTS.md injected into the prompt? ", "Never send without approval" in prompt)
    print("skill listed in the prompt?        ", "overdue-invoice-reminders" in prompt)
    print("full skill body in the prompt?      ", "pay.acme.studio/<id>" in prompt, "(loaded on demand instead)")
    print("draft:", r["messages"][-1].content)
    print("files on disk:", sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()))
