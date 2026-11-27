"""Console tracing. Kept dependency-free so the demos run anywhere."""

from __future__ import annotations

import os
import sys

_COLORS = {
    "agent": "\033[36m",    # cyan
    "tool": "\033[33m",     # yellow
    "ok": "\033[32m",       # green
    "warn": "\033[35m",     # magenta
    "deny": "\033[31m",     # red
    "dim": "\033[2m",
    "bold": "\033[1m",
}
_RESET = "\033[0m"
QUIET = os.environ.get("PA_QUIET") == "1"


def _use_color() -> bool:
    return sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def say(kind: str, who: str, msg: str) -> None:
    if QUIET:
        return
    tag = f"[{who}]"
    if _use_color():
        tag = f"{_COLORS.get(kind, '')}{tag}{_RESET}"
    print(f"{tag} {msg}")


def banner(title: str) -> None:
    if QUIET:
        return
    line = "=" * max(20, len(title) + 4)
    print(f"\n{line}\n  {title}\n{line}")


def section(title: str) -> None:
    if QUIET:
        return
    print(f"\n--- {title} ---")
