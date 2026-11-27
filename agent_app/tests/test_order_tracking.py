"""Live order tracking: 3 agent types x 6 runtimes must reach the same, correct end state."""

import asyncio
import collections
import time

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app import db
from usecases.order_tracking import RUNTIMES, agents, tools
from usecases.order_tracking.models import Approval, Notification, Order, Ticket
from usecases.order_tracking.sim import PLAN, Simulator

KINDS = {"normal": ["out_for_delivery", "delivered"], "delayed": ["delay", "out_for_delivery", "delivered"],
         "weather": ["delay", "out_for_delivery", "delivered"], "address": ["out_for_delivery", "address", "delivered"],
         "lost": ["issue"], "damaged": ["out_for_delivery", "issue"]}
EXPECTED_NOTES = {(1001 + i, k) for i, sc in enumerate(PLAN) for k in KINDS[sc]}
EXPECTED_TICKETS = [1003, 1004, 1006, 1011]
EXPECTED_APPROVALS = [("credit", 1002), ("credit", 1005), ("credit", 1008), ("reship", 1003), ("reship", 1006), ("reship", 1011)]


def fresh() -> Simulator:
    sim = Simulator(seed=7)
    sim.reset()
    return sim


def ticker(sim: Simulator):  # noqa: ANN201
    """Advance the simulator until something happens (or it's finished), like a real feed would."""
    def tick() -> None:
        while not sim.done() and not sim.tick():
            pass
    return tick


def end_state() -> tuple[list, list, list]:
    with db.session() as s:
        notes = [(n.order_id, n.kind) for n in s.scalars(select(Notification))]
        tickets = sorted(t.order_id for t in s.scalars(select(Ticket)))
        approvals = sorted((a.action, a.order_id) for a in s.scalars(select(Approval)))
    return notes, tickets, approvals


def assert_complete() -> None:
    notes, tickets, approvals = end_state()
    assert [k for k, v in collections.Counter(notes).items() if v > 1] == [], "duplicate customer emails"
    assert set(notes) == EXPECTED_NOTES
    assert tickets == EXPECTED_TICKETS
    assert approvals == EXPECTED_APPROVALS


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_looping_agent(runtime):
    sim = fresh()
    r = asyncio.run(agents.run_looping(runtime, interval=0, idle_limit=1, before_poll=ticker(sim)))
    assert r["status"] == "done", r
    assert sim.done() and r["iterations"] >= 5
    assert_complete()


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_graph_agent(runtime):
    sim = fresh()
    ran = asyncio.run(agents.graph_dispatcher(runtime, interval=0, idle_limit=1, before_poll=ticker(sim)))
    assert ran == 28            # every out_for_delivery/delivered/delay/address/lost/damaged scan
    assert_complete()


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_harness_agent(runtime):
    fresh().run_to_end()
    r = asyncio.run(agents.run_harness(runtime, "Where is order 1003?"))
    assert r["status"] == "done" and "lost" in r["answer"]
    _, tickets, approvals = end_state()
    assert tickets == [1003] and approvals == [("reship", 1003)]
    r = asyncio.run(agents.run_harness(runtime, "Which orders have problems?"))
    assert all(f"#{i}" in r["answer"] for i in (1003, 1006, 1011))


def test_looping_and_graph_agents_together_share_the_work():
    """Two always-on agents on different runtimes watch the same stream at once. Redis
    idempotency keys mean customers still get exactly one email of each kind."""
    sim = fresh()
    stop = {"n": 0}

    async def both() -> None:
        async def feed() -> None:
            while not sim.done():
                sim.tick()
                await asyncio.sleep(0.02)
            stop["n"] = 1
        await asyncio.gather(feed(),
                             agents.run_looping("langgraph", interval=0.02, idle_limit=25),
                             agents.graph_dispatcher("adk_workflow", interval=0.02, idle_limit=25))

    asyncio.run(both())
    notes, _, _ = end_state()
    with db.session() as s:
        by = collections.Counter(n.by for n in s.scalars(select(Notification)))
    assert_complete()
    assert set(by) <= {"looping/langgraph", "graph/adk_workflow"} and sum(by.values()) == len(EXPECTED_NOTES)


def test_guards_and_approvals():
    sim = fresh()
    sim.run_to_end()
    ref = tools.start_run("harness", "langchain", "scripted", "guard test")
    t = {x.name: x for x in tools.make_tools(ref)}
    assert t["request_credit"].call(order_id=1003, amount=100.0, reason="sorry")["blocked"]          # over the cap
    assert t["request_reship"].call(order_id=1001, reason="just because")["blocked"]                # delivered, not lost
    a = t["request_reship"].call(order_id=1003, reason="lost")
    assert a["status"] == "pending"
    assert t["request_reship"].call(order_id=1003, reason="lost again")["existing"]                 # one per order
    assert tools.decide(a["approval_id"], True)["status"] == "approved"
    with db.session() as s:
        assert s.get(Order, 1003).status == "reshipped"
    assert "error" in tools.decide(a["approval_id"], True)                                          # already decided


@pytest.fixture(scope="module")
def client():
    from app.api import app

    with TestClient(app) as c:
        yield c


def test_api_end_to_end(client):
    assert client.get("/orders").status_code == 200
    meta = client.get("/api/ot/meta").json()
    assert [r["id"] for r in meta["runtimes"]] == RUNTIMES
    client.post("/api/ot/reset")
    for _ in range(40):
        if client.post("/api/ot/sim/tick").json()["done"]:
            break
    evs = client.get("/api/ot/events?limit=200").json()
    lost = next(e for e in evs if e["code"] == "lost")
    g = client.post("/api/ot/graph/run", json={"runtime": "adk_workflow", "event_id": lost["event_id"]}).json()
    assert g["status"] == "done" and g["path"] == ["load", "classify", "investigate", "act", "draft", "notify", "finish"]
    h = client.post("/api/ot/harness", json={"runtime": "claude", "ask": "Where is order 1006?"}).json()
    assert "damaged" in h["answer"] and any(s["name"] == "request_reship" for s in h["run"]["steps"])
    pending = [a for a in client.get("/api/ot/state").json()["approvals"] if a["status"] == "pending"]
    assert {a["order_id"] for a in pending} == {1003, 1006}
    assert client.post(f"/api/ot/approvals/{pending[0]['id']}", json={"approve": False}).json()["status"] == "rejected"
    assert client.post(f"/api/ot/approvals/{pending[0]['id']}", json={"approve": True}).status_code == 409


def test_sse_stream(client):
    client.post("/api/ot/reset")
    client.post("/api/ot/sim/tick")
    got = []
    with client.stream("GET", "/api/ot/stream?since=start&max_events=5") as r:
        assert r.headers["content-type"].startswith("text/event-stream")
        for line in r.iter_lines():
            if line.startswith("event:"):
                got.append(line.split(":", 1)[1].strip())
    assert len(got) == 5 and set(got) <= {"scan", "activity"}


def test_background_looping_start_stop(client):
    client.post("/api/ot/reset")
    assert client.post("/api/ot/looping/start", json={"runtime": "deepagents", "interval": 0.05}).json()["running"]["looping:deepagents"]
    assert client.post("/api/ot/looping/start", json={"runtime": "deepagents"}).status_code == 409   # one per runtime
    for _ in range(40):
        client.post("/api/ot/sim/tick")
    time.sleep(1.0)
    client.post("/api/ot/looping/stop?runtime=deepagents")
    for _ in range(50):
        if not client.get("/api/ot/state").json()["running"]["looping:deepagents"]:
            break
        time.sleep(0.1)
    st = client.get("/api/ot/state").json()
    assert not st["running"]["looping:deepagents"]
    assert any(r["agent_type"] == "looping" and r["runtime"] == "deepagents" and r["status"] == "done" for r in st["runs"])
    assert len(st["notifications"]) > 10
