"""Manus - autonomous task execution through the Manus API (v2).

Architecture notes
------------------
Manus is a *general agent platform*: you hand it a task, it plans, runs on its own
cloud computer (browser, code, files) and returns artifacts. Manus 2.0 (Sep 28 2026)
added Cascade, Studio, Automations and the separate Cue app (see s07).

The API is task-oriented and asynchronous:
    POST /v2/task.create        -> task_id, task_url (and share_url if not private)
    GET  /v2/task.detail        -> status and result
    GET  /v2/task.listMessages  -> event stream incl. status_update events
    POST /v2/task.sendMessage   -> follow-up message into the same task
Auth: x-manus-api-key header (or OAuth for Open Apps). Every response is wrapped as
{"ok": true, "request_id": ...} or {"ok": false, "error": {...}}. Uploaded files are
deleted after 48h. Prefer webhooks in production; polling is fine for scripts.
There's also an OpenAI-compatible Responses surface at https://api.manus.ai/v1.

Docs: https://open.manus.ai/docs  (v2 reference)
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field

from pa_core.cli import main, require_env
from pa_core.trace import banner, say, section

BASE = "https://api.manus.ai"
TERMINAL = {"completed", "stopped", "failed", "error", "cancelled", "waiting_for_input"}


class ManusClient:
    """Thin wrapper over the v2 REST API. Field names follow the public reference;
    the getters are defensive because the response envelope can carry extra keys."""

    def __init__(self, api_key: str | None = None, base: str = BASE, session=None):  # noqa: ANN001
        import requests

        self.http = session or requests.Session()
        self.http.headers.update({"x-manus-api-key": api_key or os.environ["MANUS_API_KEY"],
                                  "Content-Type": "application/json"})
        self.base = base

    def _check(self, r) -> dict:  # noqa: ANN001
        r.raise_for_status()
        data = r.json()
        if data.get("ok") is False:
            err = data.get("error", {})
            raise RuntimeError(f"Manus error {err.get('code')}: {err.get('message')} (request_id={data.get('request_id')})")
        return data

    def create_task(self, text: str, **extra) -> dict:  # noqa: ANN003
        body = {"message": {"content": text}, **extra}
        return self._check(self.http.post(f"{self.base}/v2/task.create", json=body))

    def detail(self, task_id: str) -> dict:
        return self._check(self.http.get(f"{self.base}/v2/task.detail", params={"task_id": task_id}))

    def messages(self, task_id: str, limit: int = 10) -> dict:
        return self._check(self.http.get(f"{self.base}/v2/task.listMessages",
                                         params={"task_id": task_id, "order": "desc", "limit": limit}))

    def send(self, task_id: str, text: str) -> dict:
        return self._check(self.http.post(f"{self.base}/v2/task.sendMessage",
                                          json={"task_id": task_id, "message": {"content": text}}))

    @staticmethod
    def status_of(detail: dict) -> str:
        task = detail.get("task", detail)
        return str(task.get("status") or task.get("agent_status") or "unknown").lower()

    def wait(self, task_id: str, every: float = 10.0, timeout: float = 1800) -> dict:
        start = time.time()
        while time.time() - start < timeout:
            d = self.detail(task_id)
            st = self.status_of(d)
            say("dim", "manus", f"status={st}")
            if st in TERMINAL:
                return d
            time.sleep(every)
        raise TimeoutError(task_id)


# ---------------------------------------------------------------------------------------
# mock: a fake Manus server with the same lifecycle
# ---------------------------------------------------------------------------------------


@dataclass
class FakeManus:
    tasks: dict = field(default_factory=dict)

    def create_task(self, text: str, **_) -> dict:  # noqa: ANN003
        tid = f"task_{len(self.tasks) + 1:04d}"
        self.tasks[tid] = {"status": "running", "ticks": 0, "prompt": text, "events": []}
        return {"ok": True, "task_id": tid, "task_url": f"https://manus.im/app/{tid}"}

    def detail(self, tid: str) -> dict:
        t = self.tasks[tid]
        t["ticks"] += 1
        plan = ["planning", "browsing Stripe dashboard", "drafting reminders", "writing summary.md"]
        if t["ticks"] <= len(plan):
            t["events"].append({"type": "status_update", "agent_status": "running", "step": plan[t["ticks"] - 1]})
            return {"ok": True, "task": {"status": "running", "step": plan[t["ticks"] - 1]}}
        t["status"] = "completed"
        return {"ok": True, "task": {"status": "completed", "result": "2 reminders drafted; summary.md attached",
                                     "attachments": ["summary.md", "reminders.docx"]}}


def run_mock() -> dict:
    banner("Manus - async task lifecycle (mock server)")
    m = FakeManus()
    section("create -> poll -> result")
    created = m.create_task("Find overdue Stripe invoices for Acme Studio and draft reminders. "
                            "Return a summary.md.")
    tid = created["task_id"]
    say("ok", "manus", f"created {tid} -> {created['task_url']}")
    while True:
        d = m.detail(tid)
        st = ManusClient.status_of(d)
        say("dim", "manus", f"status={st} {d['task'].get('step', '')}")
        if st in TERMINAL:
            break
    say("ok", "manus", d["task"]["result"])
    return {"task_id": tid, "status": st, "attachments": d["task"]["attachments"]}


def run_live() -> None:
    require_env("MANUS_API_KEY")
    banner("Manus - live v2 API")
    c = ManusClient()
    t = c.create_task("List three practical tips for writing a friendly overdue-invoice reminder email. "
                      "Keep it under 120 words.")
    print("task:", t.get("task_id"), t.get("task_url"))
    print(c.wait(t["task_id"]))


if __name__ == "__main__":
    main(run_mock, run_live)
