"""The HTTP API: preferences pick the framework, runs pause for approval, decisions resume them."""

import pytest
from fastapi.testclient import TestClient

from app import config, runtimes
from app.api import app

FWS = [f for f in config.FRAMEWORKS if runtimes.available()[f]]


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_health_and_catalogue(client):
    h = client.get("/api/health").json()
    assert h["ok"] and h["database"] in ("sqlite", "postgresql", "mysql")
    data = client.get("/api/usecases").json()
    assert len(data["items"]) == 200 and len(data["areas"]) == 10
    assert len(client.get("/api/usecases", params={"area": "money"}).json()["items"]) == 20
    assert client.get("/", headers={"accept": "text/html"}).status_code == 200


def test_preferences_choose_framework_and_fill_placeholders(client):
    client.put("/api/users/pat/preferences", json={"framework": "langgraph", "home_city": "Denver"})
    p = client.get("/api/users/pat/preferences").json()
    assert p["framework"] == "langgraph" and p["home_city"] == "Denver"
    r = client.post("/api/runs", json={"user_id": "pat", "usecase_id": 1}).json()
    assert r["framework"] == "langgraph" and r["status"] == "done"
    assert any(c["args"].get("city") == "Denver" for c in r["tool_calls"])
    assert client.put("/api/users/pat/preferences", json={"framework": "nope"}).status_code == 422


@pytest.mark.parametrize("fw", FWS)
def test_manual_approval_edit(client, fw):
    """#48: transfer $500 pauses; the person edits it to $250 over HTTP."""
    r = client.post("/api/runs", json={"user_id": "u-" + fw, "usecase_id": 48, "framework": fw}).json()
    assert r["status"] == "awaiting_approval", r
    assert r["pending"][0]["tool"] == "transfer" and r["pending"][0]["args"]["amount"] == 500.0
    r = client.post(f"/api/runs/{r['id']}/decisions", json={"decisions": [{"type": "edit", "args": {"amount": 250.0}}]}).json()
    assert r["status"] == "done"
    moved = [c for c in r["tool_calls"] if c["tool"] == "transfer"]
    assert moved[0]["args"]["amount"] == 250.0 and moved[0]["status"] == "ok"


@pytest.mark.parametrize("fw", FWS)
def test_manual_reject_and_parallel_approvals(client, fw):
    """#23: three unsubscribes in one turn; approve two, reject one."""
    r = client.post("/api/runs", json={"user_id": "r-" + fw, "usecase_id": 23, "framework": fw}).json()
    seen = []
    while r["status"] == "awaiting_approval":
        decisions = [{"type": "reject"} if p["args"]["sender"] == "local-library" else {"type": "approve"} for p in r["pending"]]
        seen += [p["args"]["sender"] for p in r["pending"]]
        r = client.post(f"/api/runs/{r['id']}/decisions", json={"decisions": decisions}).json()
    assert r["status"] == "done" and sorted(seen) == ["crypto-weekly", "dealsdaily", "local-library"]
    status = {c["args"]["sender"]: c["status"] for c in r["tool_calls"] if c["tool"] == "unsubscribe"}
    assert status == {"dealsdaily": "ok", "crypto-weekly": "ok", "local-library": "rejected"}


@pytest.mark.parametrize("fw", FWS)
def test_guard_uses_preferences(client, fw):
    """#56: the laptop is blocked at the default $200 limit, and bought once the user raises it."""
    uid = "g-" + fw
    r = client.post("/api/runs", json={"user_id": uid, "usecase_id": 56, "framework": fw, "auto_approve": True}).json()
    assert [c["status"] for c in r["tool_calls"] if c["tool"] == "checkout"] == ["blocked"]
    client.put(f"/api/users/{uid}/preferences", json={"max_purchase_without_review": 2000})
    r = client.post("/api/runs", json={"user_id": uid, "usecase_id": 56, "framework": fw, "auto_approve": True}).json()
    assert [c["status"] for c in r["tool_calls"] if c["tool"] == "checkout"] == ["ok"]


def test_memory_shared_across_frameworks(client):
    client.post("/api/runs", json={"user_id": "mem", "usecase_id": 18, "framework": "adk", "auto_approve": True})
    assert client.get("/api/users/mem/memories").json()["goal_today"] == "finish the report draft"
    r = client.post("/api/runs", json={"user_id": "mem", "usecase_id": 19, "framework": "claude", "auto_approve": True}).json()
    recall = next(c for c in r["tool_calls"] if c["tool"] == "recall")
    assert recall["result"] == {"goal_today": "finish the report draft"}


def test_wrong_decision_count_and_finished_run(client):
    r = client.post("/api/runs", json={"user_id": "x", "usecase_id": 48, "framework": "deepagents"}).json()
    bad = client.post(f"/api/runs/{r['id']}/decisions", json={"decisions": [{"type": "approve"}, {"type": "approve"}]})
    assert bad.status_code == 422
    client.post(f"/api/runs/{r['id']}/decisions", json={"decisions": [{"type": "approve"}]})
    assert client.post(f"/api/runs/{r['id']}/decisions", json={"decisions": [{"type": "approve"}]}).status_code == 409


def test_background_run_and_polling(client):
    import time

    r = client.post("/api/runs?wait=false", json={"user_id": "bg", "usecase_id": 7, "framework": "deepagents"}).json()
    assert r["status"] == "running" and r["id"]
    for _ in range(100):
        got = client.get(f"/api/runs/{r['id']}").json()
        if got["status"] != "running":
            break
        time.sleep(0.05)
    assert got["status"] == "done" and got["ok"]


def test_rate_limit(client, monkeypatch):
    monkeypatch.setattr(config, "RATE_LIMIT_PER_MIN", 2)
    codes = [client.post("/api/runs", json={"user_id": "spammy", "usecase_id": 34, "auto_approve": True}).status_code for _ in range(3)]
    assert codes == [200, 200, 429]
