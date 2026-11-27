"""A Pi-style minimal coding harness: four tools, real files, real shell.

Pi (Mario Zechner's pi-mono, the engine inside OpenClaw) bets that a model which can read,
write, edit and run code needs nothing else: four tools, a very short system prompt, no
built-in MCP, no subagents. Everything else gets built *by the agent* as scripts and CLIs.

This file builds that harness on pa_core:
    read(path)                 read a file
    write(path, content)       create/overwrite a file
    edit(path, old, new)       exact-match replace (fails if `old` isn't found exactly once)
    bash(cmd)                  run a shell command in the workspace, with a timeout

Offline it replays a scripted model doing a real fix-the-failing-test loop in a temp
folder (the commands genuinely run). With PA_LIVE=1 and PA_* set, a real model drives it.

    python harness_agents/examples/pi_style_minimal_harness.py
    PA_LIVE=1 PA_BASE_URL=... PA_API_KEY=... PA_MODEL=... python ...
"""

from __future__ import annotations

import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pa_core import ApprovalGate, ApprovalMode, AutonomousAgent, Step, ToolRegistry  # noqa: E402
from pa_core.llm import from_env_or_script  # noqa: E402
from pa_core.tools import Risk, tool  # noqa: E402

SYSTEM = "You are a coding agent. Tools: read, write, edit, bash. Make the tests pass. Be brief."


def make_tools(ws: pathlib.Path):
    def safe(path: str) -> pathlib.Path:
        p = (ws / path).resolve()
        if ws.resolve() not in p.parents and p != ws.resolve():
            raise ValueError("path escapes the workspace")
        return p

    @tool(risk=Risk.READ)
    def read(path: str) -> str:
        """Read a text file in the workspace."""
        return safe(path).read_text()

    @tool(risk=Risk.WRITE)
    def write(path: str, content: str) -> str:
        """Create or overwrite a file in the workspace."""
        p = safe(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return f"wrote {len(content)} bytes to {path}"

    @tool(risk=Risk.WRITE)
    def edit(path: str, old: str, new: str) -> str:
        """Replace exactly one occurrence of `old` with `new` in a file."""
        p = safe(path)
        text = p.read_text()
        n = text.count(old)
        if n != 1:
            return f"error: expected exactly 1 match for old text, found {n}"
        p.write_text(text.replace(old, new))
        return f"edited {path}"

    @tool(risk=Risk.WRITE)
    def bash(cmd: str) -> str:
        """Run a shell command in the workspace (30 s timeout). Returns exit code and output."""
        r = subprocess.run(cmd, shell=True, cwd=ws, capture_output=True, text=True, timeout=30)
        return f"exit={r.returncode}\n{(r.stdout + r.stderr)[-1500:]}"

    return [read, write, edit, bash]


SCRIPT = [
    Step.call("write", "Create the module.", path="reminders.py", content=(
        "def format_reminder(name, invoice, amount, days):\n"
        "    tone = 'friendly' if days < 30 else 'firm'\n"
        "    return f'[{tone}] Hi {name}, {invoice} (${amount}) is {days} days overdue.'\n")),
    Step.call("write", "Add a test, including the 30-day boundary.", path="test_reminders.py", content=(
        "from reminders import format_reminder\n"
        "def test_friendly():\n    assert format_reminder('Maria','INV-1042',850,3).startswith('[friendly]')\n"
        "def test_boundary_is_friendly():\n    assert format_reminder('Northwind','INV-1038',2400,30).startswith('[friendly]')\n"
        "if __name__ == '__main__':\n    test_friendly(); test_boundary_is_friendly(); print('ALL PASS')\n")),
    Step.call("bash", "Run the tests.", cmd=f"{sys.executable} test_reminders.py"),
    Step.call("edit", "Boundary is wrong: 30 days should still be friendly.", path="reminders.py",
              old="days < 30", new="days <= 30"),
    Step.call("bash", "Re-run.", cmd=f"{sys.executable} test_reminders.py"),
    Step.final("Fixed the off-by-one at the 30-day boundary; tests pass."),
]


def main() -> None:
    ws = pathlib.Path(tempfile.mkdtemp(prefix="pi_ws_"))
    agent = AutonomousAgent("pi", SYSTEM, from_env_or_script(SCRIPT), ToolRegistry(make_tools(ws)),
                            gate=ApprovalGate(ApprovalMode.AUTO), max_steps=15)
    r = agent.run("reminders.py should format friendly reminders up to and including 30 days. Write it and test it.")
    outputs = [a["result"] for a in r.actions if a["tool"] == "bash"]
    print("\nworkspace:", ws)
    print("first test run :", outputs[0].splitlines()[0] if outputs else "-")
    print("last test run  :", outputs[-1].replace("\n", " ")[:80] if outputs else "-")


if __name__ == "__main__":
    main()
