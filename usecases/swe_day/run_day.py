"""Run the engineer's day in time order.

    python usecases/swe_day/run_day.py                  # all 100, 06:30 to midnight
    python usecases/swe_day/run_day.py --block review   # one block
    python usecases/swe_day/run_day.py --id 49 50 -v    # specific use cases with full traces
    python usecases/swe_day/run_day.py --list           # just the schedule
"""

from __future__ import annotations

import argparse
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from usecases.engine import run  # noqa: E402
from usecases.swe_day import BLOCKS, all_usecases  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--block", choices=[b for b, _, _ in BLOCKS])
    ap.add_argument("--id", type=int, nargs="*")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--live", action="store_true", help="use a real model (LC_MODEL)")
    a = ap.parse_args()

    ucs = all_usecases()
    if a.block:
        ucs = [u for u in ucs if u.block == a.block]
    if a.id:
        ucs = [u for u in ucs if u.id in a.id]

    failed, t0, current = [], time.perf_counter(), None
    for u in ucs:
        if u.block != current:
            current = u.block
            span = next(s for b, s, _ in BLOCKS if b == u.block)
            print(f"\n== {span}  {u.block} ==")
        if a.list:
            print(f"  {u.time}  {u.id:>3}  {u.title:<46} {u.trigger}")
            continue
        r = run(u, verbose=a.verbose)
        mark = "ok  " if r.ok else "FAIL"
        print(f"  {u.time}  {mark} {u.id:>3}  {u.title:<46} {len(r.world.calls):>2} tools  {u.trigger}")
        if not r.ok:
            failed.append(u.id)
            print(f"           {r.error or [c[0] for c in r.checks if not c[1]]}")
    if not a.list:
        print(f"\n{len(ucs) - len(failed)}/{len(ucs)} passed in {time.perf_counter() - t0:.1f}s")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
