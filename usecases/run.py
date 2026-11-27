"""Run the Deep Agents use cases.

    python usecases/run.py --list                 # catalogue
    python usecases/run.py 1                      # one use case, full trace
    python usecases/run.py 1 7 42                 # several
    python usecases/run.py --domain finance       # a whole domain, traces
    python usecases/run.py --all                  # all 100, summary table
    LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/run.py 1 --live   # real model
"""

from __future__ import annotations

import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from usecases.catalog import all_usecases  # noqa: E402
from usecases.engine import run  # noqa: E402


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--live"]
    ucs = all_usecases()
    if not args or "--list" in args:
        for u in ucs:
            print(f"{u.id:>3}  {u.domain:<16} {u.title:<44} {', '.join(u.features)}")
        print(f"\n{len(ucs)} use cases. Run one with: python usecases/run.py <id>")
        return
    if "--all" in args:
        t0, failed = time.perf_counter(), []
        for u in ucs:
            r = run(u)
            mark = "ok " if r.ok else "FAIL"
            print(f"{mark} {u.id:>3}  {u.domain:<16} {u.title:<44} {len(r.world.calls):>2} tool calls"
                  + (f"   <- {r.error or [c for c in r.checks if not c[1]]}" if not r.ok else ""))
            if not r.ok:
                failed.append(u.id)
        print(f"\n{len(ucs) - len(failed)}/{len(ucs)} passed in {time.perf_counter() - t0:.1f}s")
        sys.exit(1 if failed else 0)
    if "--domain" in args:
        dom = args[args.index("--domain") + 1]
        selected = [u for u in ucs if u.domain == dom]
    else:
        wanted = {int(a) for a in args if a.isdigit()}
        selected = [u for u in ucs if u.id in wanted]
    bad = 0
    for u in selected:
        r = run(u, verbose=True)
        if r.error:
            print("  ERROR:", r.error)
        bad += not r.ok
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
