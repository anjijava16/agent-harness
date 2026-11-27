"""Every demo must run offline and produce the behaviour its README promises."""

import importlib
import os

import pytest

os.environ["PA_QUIET"] = "1"

from pa_core import (ApprovalGate, ApprovalMode, AutonomousAgent, Budget, SandboxComputer,  # noqa: E402
                     ScriptedLLM, Sentinel, Step, ToolRegistry, Workspace)
from pa_core.tools import Risk  # noqa: E402
from run_all import SERVICES  # noqa: E402


@pytest.mark.parametrize("num,label,mod", SERVICES)
def test_mock_runs(num, label, mod):
    out = importlib.import_module(mod).run_mock()
    assert isinstance(out, dict) and out


def m(name):
    return importlib.import_module(dict((s[0], s[2]) for s in SERVICES)[name]).run_mock()


def test_grok_bot_shared_thread_and_refused_payment():
    out = m("01")
    assert out["bots"] == ["Finn", "Ria"] and out["thread_messages"] == 2
    assert out["blocked"] == ["pay"] and out["workspace"]["sent"] == 2


def test_dots_background_is_read_only():
    assert m("02")["proactive_blocked"] == ["send_email"]


def test_muse_sentinel_blocks_exfiltration_and_budget_caps():
    out = m("05")
    assert ("send_email", "sentinel veto") in out["blocked"]
    assert ("pay", "over budget") in out["blocked"] and out["budget_left"] == 62.0


def test_cowork_asks_for_every_action():
    out = m("06")
    assert out["approvals_asked"] == 6 and out["rejected"] == ["send_email"]


def test_cue_wallet_and_identity():
    out = m("07")
    assert out["cole_email"].endswith("@agents.cue.im") and out["ezra_wallet_left"] == 26.0


def test_openclaw_drops_unknown_dm():
    assert all("telegram" not in s for s in m("08")["sessions"])


def test_personal_computer_undo_and_shell_allowlist():
    out = m("10")
    assert "Finance/ar_summary.csv" not in out["files"] and out["shell_denied"]


def test_hermes_learns_and_gets_faster():
    out = m("12")
    assert out["learned"] and out["run2_steps"] < out["run1_steps"] and out["skill_in_prompt"]


def test_comet_blocks_injected_navigation():
    out = m("14")
    assert any("evil.test" in f for f in out["flags"])


# ---- core unit tests -----------------------------------------------------------------

def test_readonly_subset():
    reg = ToolRegistry(Workspace().tools()).subset(Risk.READ)
    assert "send_email" not in reg and "read_inbox" in reg


def test_deny_all_blocks_writes():
    ws = Workspace()
    a = AutonomousAgent("x", "y", ScriptedLLM([Step.call("draft_email", to="a@b.c", subject="s", body="b")]),
                        ToolRegistry(ws.tools()), gate=ApprovalGate(ApprovalMode.DENY_ALL))
    r = a.run("g")
    assert r.blocked and not ws.drafts


def test_budget():
    b = Budget(10)
    assert b.charge(6) and not b.charge(5) and b.remaining() == 4


def test_sentinel_blocks_terms():
    t = ToolRegistry(Workspace().tools()).get("send_email")
    s = Sentinel(allowed_domains={"ok.com"}, blocked_terms=["secret"])
    assert s.check(t, {"to": "a@ok.com", "body": "hi"})
    assert not s.check(t, {"to": "a@ok.com", "body": "the secret"})


def test_undo():
    pc = SandboxComputer()
    pc.write("a.txt", "1")
    pc.write("a.txt", "2")
    pc.undo_last()
    assert pc.read("a.txt") == "1"
