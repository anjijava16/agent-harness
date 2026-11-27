"""Cursor - AI coding agent with local and cloud runtimes (and the home of Grok Bot).

Architecture notes
------------------
* The Cursor Python SDK (pip install cursor-sdk) wraps two runtimes behind one API:
    local  -> runs against a working tree on your machine
    cloud  -> runs in an isolated Cursor-hosted VM with your repo cloned in
  Same code either way: Agent.create(...) -> agent.send(prompt) -> run.wait().result
* Cloud Agents REST API: POST /v1/agents (public beta), Basic or Bearer auth with a
  crsr_ key. Agents can auto-create PRs.
* Agent SDK (@grok/agent-sdk, formerly @cursor/bdk) is for agents-as-code you deploy;
  Grok Bot runs on the same persistent-cloud-computer infrastructure.
* The Cloud Agents API runs agent *workflows*; it is not a chat-completions API.

Docs: https://cursor.com/docs/sdk/python , https://cursor.com/docs/cloud-agent/api/endpoints
"""

from __future__ import annotations

import os

from pa_core.cli import main, require_env
from pa_core.trace import banner, say, section


class FakeCloudRun:
    def __init__(self, prompt: str):
        self.prompt, self.status = prompt, "running"

    def wait(self):  # noqa: ANN201
        for step in ["cloning acme/billing@main", "reading src/reminders.py", "editing 2 files",
                     "running pytest (14 passed)", "opening PR #42"]:
            say("dim", "cursor-cloud", step)
        self.status = "finished"
        self.result = "Added overdue-reminder job with tests. PR #42 opened."
        return self


def run_mock() -> dict:
    banner("Cursor SDK - cloud agent lifecycle (mock)")
    section("Agent.create(cloud=...) -> send -> wait")
    run = FakeCloudRun("Add a nightly job that emails reminders for invoices >7 days overdue, with tests.")
    res = run.wait()
    say("ok", "cursor", res.result)
    return {"status": res.status, "pr": "#42"}


def run_live() -> None:
    require_env("CURSOR_API_KEY")
    from cursor_sdk import Agent, CloudAgentOptions, CloudRepository, LocalAgentOptions

    banner("Cursor SDK - live")
    repo = os.environ.get("CURSOR_REPO_URL")
    if repo:
        cloud = CloudAgentOptions(repos=[CloudRepository(url=repo, starting_ref=os.environ.get("CURSOR_REF", "main"))],
                                  auto_create_pr=False)
        with Agent.create(cloud=cloud, name="pa-deep-dive") as agent:
            run = agent.send("Read the repo and propose (don't apply) a design for an overdue-invoice reminder job.")
            print(run.wait().result)
    else:
        with Agent.create(local=LocalAgentOptions(cwd=os.getcwd())) as agent:
            run = agent.send("Summarize what pa_core/agent.py does in 5 bullets. Don't edit anything.")
            print(run.wait().result)


if __name__ == "__main__":
    main(run_mock, run_live)
