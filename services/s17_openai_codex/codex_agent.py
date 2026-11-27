"""OpenAI Codex - coding agent you can drive from Python (pip install openai-codex).

Architecture notes
------------------
* The Python SDK controls a local Codex app-server over JSON-RPC; published builds pin
  a compatible Codex CLI runtime, so there's nothing else to install.
* Threads hold conversation + workspace state; each turn can change the sandbox:
      Sandbox.read_only        read files, no writes
      Sandbox.workspace_write  write inside the workspace and configured roots
      Sandbox.full_access      no filesystem limits (use in a disposable VM only)
* Approvals: threads default to ApprovalMode.auto_review; ApprovalMode.deny_all refuses
  anything that needs approval.
* Same harness grew into OpenAI dots (see s02); dots can be launched from Codex.

The pattern below is the one worth copying: plan in read_only, then implement in
workspace_write, then review the diff in read_only again.
"""

from __future__ import annotations

import os

from pa_core.cli import main
from pa_core.trace import banner, say, section


def run_mock() -> dict:
    banner("Codex SDK - plan (read-only) -> implement (workspace-write) -> review (mock)")
    turns = [("read_only", "Plan: add reminders.py with format_reminder(); add tests/test_reminders.py"),
             ("workspace_write", "Wrote reminders.py, tests/test_reminders.py; pytest: 3 passed"),
             ("read_only", "Review: diff is 41 lines, no secrets, tests cover >30-day escalation")]
    for sandbox, out in turns:
        section(f"turn with sandbox={sandbox}")
        say("tool", "codex", out)
    return {"turns": len(turns), "sandboxes": [t[0] for t in turns]}


def run_live() -> None:
    from openai_codex import ApprovalMode, Codex, Sandbox

    banner("Codex SDK - live")
    model = os.environ.get("CODEX_MODEL")  # omit to use your configured default
    with Codex() as codex:
        if os.environ.get("OPENAI_API_KEY") and not os.environ.get("CODEX_SKIP_LOGIN"):
            codex.login_api_key(os.environ["OPENAI_API_KEY"])
        thread = codex.thread_start(model=model, sandbox=Sandbox.read_only,
                                    approval_mode=ApprovalMode.auto_review, cwd=os.getcwd())
        plan = thread.run("Plan a small module reminders.py with format_reminder(name, invoice, amount, days) "
                          "and tests. Don't write anything yet.")
        print(plan.final_response)
        if input("\nImplement it? [y/N] ").lower().startswith("y"):
            done = thread.run("Implement the plan and run the tests.", sandbox=Sandbox.workspace_write)
            print(done.final_response)
            review = thread.run("Review the diff only.", sandbox=Sandbox.read_only)
            print(review.final_response)


if __name__ == "__main__":
    main(run_mock, run_live)
