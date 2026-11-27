"""Run use cases on one or more frameworks and print a summary.

    python scripts/run_all.py                         # all 200 on all four frameworks (800 runs)
    python scripts/run_all.py --framework langgraph   # one framework
    python scripts/run_all.py --area money -v         # one area, every run listed
    python scripts/run_all.py --id 42 48              # specific use cases

Uses a throwaway SQLite database and in-process Redis unless DATABASE_URL / REDIS_URL are set.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import pathlib
import sys
import tempfile
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
os.environ.setdefault("DATABASE_URL", f"sqlite:///{tempfile.mkdtemp()}/run_all.db")

from app import cache, config, db, runtimes, service, usecases  # noqa: E402


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--framework", choices=config.FRAMEWORKS, action="append")
    ap.add_argument("--area", choices=[a for a, _ in usecases.AREAS])
    ap.add_argument("--id", type=int, nargs="*")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    db.init(os.environ["DATABASE_URL"])
    av = runtimes.available()
    fws = [f for f in (a.framework or config.FRAMEWORKS) if av[f]]
    ucs = [u for u in usecases.all_usecases() if (not a.area or u.area == a.area) and (not a.id or u.id in a.id)]
    print(f"database: {db.dialect()}   redis: {cache.kind()}   frameworks: {', '.join(fws)}   use cases: {len(ucs)}\n")
    totals, failed = {f: [0, 0.0] for f in fws}, []
    for u in ucs:
        for fw in fws:
            cache.clear_tool_cache()
            t0 = time.perf_counter()
            r = await service.start_run("sam", u.id, framework=fw, auto_approve=True)
            totals[fw][1] += time.perf_counter() - t0
            if r["ok"]:
                totals[fw][0] += 1
            else:
                failed.append((u.id, fw, r["error"] or [c[0] for c in r["checks"] if not c[1]]))
            if a.verbose or not r["ok"]:
                print(f"  {'ok  ' if r['ok'] else 'FAIL'} {u.id:>3} {fw:<10} {u.title:<44} {len(r['tool_calls'])} tool calls")
    print("\n| framework | passed | time |\n|---|---|---|")
    for fw, (ok, secs) in totals.items():
        print(f"| {runtimes.LABELS[fw]} | {ok}/{len(ucs)} | {secs:.1f}s |")
    for f in failed:
        print("FAIL", *f)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
