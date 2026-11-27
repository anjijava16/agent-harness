"""Perplexity Personal Computer (Mac Apr 2026, Windows Jul 2026).

Architecture notes
------------------
* "Takes Computer out of the cloud-only world and onto your device": a local agent
  harness that orchestrates sub-agents across local files, native apps and the web.
* Hybrid: runs on your Mac (ideally an always-on Mac mini) or Windows PC, connected to
  Perplexity's servers and ~20 frontier models.
* Safety story: explicit approval for sensitive actions, a complete audit log, files
  created in a sandbox, and actions that are auditable and *reversible*.
* Four of the APIs behind it were opened to developers: Search, Agent, Embeddings,
  Sandbox. The Agent API (POST /v1/agent, also /v1/responses) is OpenAI-Responses
  compatible and supports presets like "pro-search".

Mock = local sandbox + audit log + undo. Live = Perplexity Agent API for the research
step (pip install perplexityai), then local, reversible file actions.
"""

from __future__ import annotations

import os

from pa_core import (ApprovalGate, ApprovalMode, AutonomousAgent, SandboxComputer, ScriptedLLM,
                     Step, ToolRegistry)
from pa_core.cli import main, require_env
from pa_core.trace import banner, say, section


def _seed(pc: SandboxComputer) -> None:
    for name in ["Downloads/inv_northwind_1038.pdf", "Downloads/inv_brightpath_1042.pdf",
                 "Downloads/boarding_pass.pdf", "Downloads/receipt_figma_nov.pdf"]:
        pc.files[name] = f"%PDF fake {name}"


def run_mock() -> dict:
    banner("Perplexity Personal Computer - local files, audit log, undo (mock)")
    pc = SandboxComputer("mac-mini")
    _seed(pc)
    script = [
        Step.call("run_shell", "Looking at Downloads.", command="ls"),
        Step.call("write_file", "Filing invoices.", path="Finance/Invoices/inv_northwind_1038.pdf",
                  text=pc.files["Downloads/inv_northwind_1038.pdf"]),
        Step.call("write_file", path="Finance/Invoices/inv_brightpath_1042.pdf",
                  text=pc.files["Downloads/inv_brightpath_1042.pdf"]),
        Step.call("write_file", path="Finance/Receipts/receipt_figma_nov.pdf",
                  text=pc.files["Downloads/receipt_figma_nov.pdf"]),
        Step.call("write_file", "Building a summary.", path="Finance/ar_summary.csv",
                  text="invoice,customer,amount\nINV-1038,Northwind,2400\nINV-1042,BrightPath,850\n"),
        Step.call("run_shell", "Trying to clean up originals.", command="rm Downloads/*.pdf"),
        Step.final("Filed 3 PDFs, wrote Finance/ar_summary.csv. I didn't delete originals (rm isn't allowed)."),
    ]
    agent = AutonomousAgent("Personal Computer", "Local agent on your Mac.", ScriptedLLM(script),
                            ToolRegistry(pc.tools()), gate=ApprovalGate(ApprovalMode.RISK_BASED))
    section("1. Organize Downloads and build an AR summary")
    agent.run("Sort my Downloads PDFs and build an AR summary")
    section("2. Audit log")
    for line in pc.audit_report():
        say("dim", "audit", line)
    section("3. You don't like the CSV -> undo")
    say("ok", "undo", pc.undo_last())
    return {"files": sorted(k for k in pc.files if k.startswith("Finance/")),
            "audit_entries": len(pc.audit), "shell_denied": any(e.action == "shell_denied" for e in pc.audit)}


def run_live() -> None:
    require_env("PERPLEXITY_API_KEY")
    from perplexity import Perplexity

    banner("Personal Computer pattern - Perplexity Agent API + local reversible actions")
    client = Perplexity()
    resp = client.responses.create(
        preset=os.environ.get("PPLX_PRESET", "pro-search"),
        input="What are current best practices for late-payment reminder emails for small agencies? "
              "Give 5 bullets with sources.",
    )
    text = resp.output_text
    print(text)
    pc = SandboxComputer("local")
    pc.write("Research/payment_reminders.md", text)
    print("\n".join(pc.audit_report()))
    print(pc.undo_last())


if __name__ == "__main__":
    main(run_mock, run_live)
