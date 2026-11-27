"""Run every framework example offline and report pass/fail.

LangChain/LangGraph/Deep Agents and ADK are best kept in separate virtualenvs; this runner
skips a folder whose library isn't importable in the current interpreter.

    python frameworks/run_all.py                 # whatever is installed here
    python frameworks/run_all.py langgraph adk   # only some folders
"""

from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
# This folder contains sub-folders named like the libraries (langchain/, langgraph/), so drop
# it from sys.path before probing, or they'd be mistaken for the real packages.
sys.path[:] = [p for p in sys.path if pathlib.Path(p or ".").resolve() != HERE]
FOLDERS = {
    "langchain": "langchain.agents",
    "langgraph": "langgraph.graph",
    "deep_agents": "deepagents",
    "google_adk": "google.adk",
    "google_adk_workflows": "google.adk",
}


def has(mod: str) -> bool:
    try:
        return importlib.util.find_spec(mod) is not None
    except ModuleNotFoundError:
        return False


def main() -> None:
    wanted = [a for a in sys.argv[1:] if not a.startswith("-")]
    failures = 0
    for folder, mod in FOLDERS.items():
        if wanted and not any(w in folder for w in wanted):
            continue
        if not has(mod):
            print(f"-- {folder:<22} skipped ({mod} not installed in this interpreter)")
            continue
        for f in sorted((HERE / folder).glob("[0-9]*.py")):
            t = time.perf_counter()
            r = subprocess.run([sys.executable, str(f)], capture_output=True, text=True, timeout=300)
            ok = r.returncode == 0
            failures += not ok
            print(f"{'ok ' if ok else 'FAIL'} {folder}/{f.name:<44} {(time.perf_counter() - t):5.1f}s")
            if not ok:
                print("     " + r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "     (no stderr)")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
