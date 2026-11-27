"""Run one use case from the terminal: python usecases/001_.../usecase.py [--framework adk | --all] [--manual] [--live]"""

from __future__ import annotations

import argparse
import asyncio
import json

from . import cache, config, db, service
from .spec import UseCase


async def _run(uc: UseCase, fw: str, manual: bool, mode: str, user: str) -> dict:
    cache.clear_tool_cache()
    r = await service.start_run(user, uc.id, framework=fw, mode=mode, auto_approve=not manual)
    while r["status"] == "awaiting_approval":
        decisions = []
        for p in r["pending"]:
            a = input(f"  approve {p['tool']}({json.dumps(p['args'])})? [y]es / [n]o / [e]dit: ").strip().lower()
            if a.startswith("e"):
                decisions.append({"type": "edit", "args": json.loads(input("  new args as JSON: "))})
            else:
                decisions.append({"type": "approve" if a in ("", "y", "yes") else "reject"})
        r = await service.decide(r["id"], decisions)
    return r


def main(uc: UseCase) -> None:
    ap = argparse.ArgumentParser(description=uc.title)
    ap.add_argument("--framework", choices=config.FRAMEWORKS)
    ap.add_argument("--all", action="store_true", help="run on all four frameworks")
    ap.add_argument("--manual", action="store_true", help="answer approvals yourself")
    ap.add_argument("--live", action="store_true", help="a real model decides (needs API keys)")
    ap.add_argument("--user", default="sam")
    a = ap.parse_args()
    db.init()
    fws = config.FRAMEWORKS if a.all else [a.framework or service.effective_prefs(a.user).get("framework") or config.DEFAULT_FRAMEWORK]
    ok = True
    for fw in fws:
        r = asyncio.run(_run(uc, fw, a.manual, "live" if a.live else "scripted", a.user))
        print(f"\n== {uc.id}. {uc.title}  [{fw}] -> {r['status']}")
        for c in r["tool_calls"]:
            print(f"  {c['status']:<8} {c['tool']}({json.dumps(c['args'])[:90]}){'  - ' + c['note'] if c['note'] else ''}")
        print(f"  answer: {r['final'] or r['error']}")
        for label, passed in r["checks"]:
            print(f"  [{'pass' if passed else 'FAIL'}] {label}")
        ok = ok and r["ok"]
    raise SystemExit(0 if ok else 1)
