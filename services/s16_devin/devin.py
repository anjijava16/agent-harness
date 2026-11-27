"""Devin (Cognition) - autonomous software engineer, driven by the Devin API v3.

Architecture notes
------------------
* A Devin *session* is a cloud machine with shell, editor and browser that works on a
  prompt until it's done, asking questions in the session thread if it gets stuck.
* API v3 (service users + RBAC, keys start with cog_):
    POST /v3/organizations/{org_id}/sessions                  create   {"prompt": ...}
    GET  /v3/organizations/{org_id}/sessions/{devin_id}       status
    POST /v3/organizations/{org_id}/sessions/{id}/messages    follow-up message
  plus knowledge notes, playbooks, attachments, and scheduled sessions via automations.
* Because a session can be created from one HTTP call, any tool or other agent can
  "hand off" work to Devin. That's the integration pattern to remember.

Docs: https://docs.devin.ai/api-reference/v3/usage-examples
"""

from __future__ import annotations

import os
import time

from pa_core.cli import main, require_env
from pa_core.trace import banner, say, section

BASE = "https://api.devin.ai/v3"


class DevinClient:
    def __init__(self, api_key: str | None = None, org_id: str | None = None):
        import requests

        self.org = org_id or os.environ["DEVIN_ORG_ID"]
        self.http = requests.Session()
        self.http.headers.update({"Authorization": f"Bearer {api_key or os.environ['DEVIN_API_KEY']}",
                                  "Content-Type": "application/json"})

    def create(self, prompt: str, **extra) -> dict:  # noqa: ANN003
        r = self.http.post(f"{BASE}/organizations/{self.org}/sessions", json={"prompt": prompt, **extra})
        r.raise_for_status()
        return r.json()

    def get(self, devin_id: str) -> dict:
        r = self.http.get(f"{BASE}/organizations/{self.org}/sessions/{devin_id}")
        r.raise_for_status()
        return r.json()

    def message(self, devin_id: str, text: str) -> dict:
        r = self.http.post(f"{BASE}/organizations/{self.org}/sessions/{devin_id}/messages", json={"message": text})
        r.raise_for_status()
        return r.json()

    @staticmethod
    def session_id(created: dict) -> str:
        return created.get("devin_id") or created.get("session_id") or created.get("id")

    def wait(self, devin_id: str, every: float = 20, timeout: float = 3600) -> dict:
        t0 = time.time()
        while time.time() - t0 < timeout:
            s = self.get(devin_id)
            status = str(s.get("status") or s.get("status_enum") or "").lower()
            say("dim", "devin", f"status={status}")
            if status in {"finished", "blocked", "stopped", "expired", "exit", "suspended"}:
                return s
            time.sleep(every)
        raise TimeoutError(devin_id)


def run_mock() -> dict:
    banner("Devin API v3 - session lifecycle (mock)")
    section("create -> working -> blocked (question) -> message -> finished")
    timeline = ["working: reading repo", "working: writing reminder job",
                "blocked: 'Should reminders go from billing@ or the account owner?'",
                "-> you: 'billing@acme.studio'", "working: adding tests", "finished: PR opened"]
    for t in timeline:
        say("dim", "devin", t)
    return {"final_status": "finished", "questions_asked": 1}


def run_live() -> None:
    require_env("DEVIN_API_KEY", "DEVIN_ORG_ID")
    banner("Devin - live v3 API")
    c = DevinClient()
    s = c.create("In a new scratch repo, write a Python function that formats a friendly overdue-invoice "
                 "reminder, with pytest tests. Keep it small.")
    sid = c.session_id(s)
    print("session:", sid, s.get("url"))
    print(c.wait(sid))


if __name__ == "__main__":
    main(run_mock, run_live)
