"""Drive any installed coding-agent harness from Python, headless.

Most harnesses have a non-interactive mode, which makes them usable as one step in a
bigger pipeline (a cron job, a LangGraph node, an ADK FunctionNode, a CI step). This
script detects which CLIs are on your PATH, shows the command it would run, and with
--run executes the same task with each one in its own scratch folder.

Flags change between releases. Treat the templates below as a starting point and check
`<tool> --help` for your installed version.

    python harness_agents/examples/drive_headless_harnesses.py          # detect + show
    python harness_agents/examples/drive_headless_harnesses.py --run    # actually run
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile

TASK = "Create reminders.py with format_reminder(name, invoice, amount, days) and a test file. Run the test."

# name -> (binary, argv template). {task} is replaced with TASK.
HARNESSES = {
    "Claude Code": ("claude", ["claude", "-p", "{task}"]),
    "Codex CLI": ("codex", ["codex", "exec", "{task}"]),
    "OpenCode": ("opencode", ["opencode", "run", "{task}"]),
    "goose": ("goose", ["goose", "run", "-t", "{task}"]),
    "Aider": ("aider", ["aider", "--yes-always", "--message", "{task}"]),
    "Gemini CLI": ("gemini", ["gemini", "-p", "{task}"]),   # succeeded by the Antigravity CLI
    "Pi": ("pi", ["pi", "-p", "{task}"]),
    "Hermes": ("hermes", ["hermes", "chat", "-q", "{task}"]),
}


def main() -> None:
    run = "--run" in sys.argv
    found = 0
    for name, (binary, argv) in HARNESSES.items():
        path = shutil.which(binary)
        cmd = [a.replace("{task}", TASK) for a in argv]
        status = "found" if path else "not installed"
        print(f"{name:<24} {status:<14} {' '.join(cmd[:-1])} \"...\"")
        if path and run:
            found += 1
            ws = tempfile.mkdtemp(prefix=f"{binary}_")
            r = subprocess.run(cmd, cwd=ws, capture_output=True, text=True, timeout=900)
            print(f"   exit={r.returncode} in {ws}\n   {r.stdout[-400:].strip()}")
    if run and not found:
        print("\nNo harness CLIs found on PATH.")


if __name__ == "__main__":
    main()
