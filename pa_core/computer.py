"""SandboxComputer: the "computer of its own" every personal agent now gets.

Grok Bot gives each account a persistent cloud computer (browser, filesystem, terminal).
Meta Muse runs inside Muse Secure VM. Cue gives every agent its own computer. Perplexity
Personal Computer runs on your Mac mini. Claude Duet and Dots run on a cloud machine.

The common contract is small:
    - a filesystem the agent can read/write
    - a browser it can open pages in
    - a shell with an allowlist
    - an audit log of everything, with undo for reversible actions

This class implements that contract in memory. Swap it for a real VM, a Docker
container, E2B, or a browser-use/Playwright session without touching the agent loop.
"""

from __future__ import annotations

import shlex
import time
from dataclasses import dataclass, field
from typing import Callable

from .tools import Risk, Tool, tool

FAKE_PAGES = {
    "https://pay.acme.studio/INV-1038": "<h1>Pay INV-1038</h1><p>$2,400.00 due</p><button id=pay>Pay</button>",
    "https://pay.acme.studio/INV-1042": "<h1>Pay INV-1042</h1><p>$850.00 due</p><button id=pay>Pay</button>",
    "https://example.com/login": "<form><input name=user><input name=pass type=password></form>",
}


@dataclass
class AuditEntry:
    ts: float
    actor: str
    action: str
    detail: str
    undo: Callable[[], None] | None = None


@dataclass
class SandboxComputer:
    name: str = "cloud-computer-1"
    files: dict[str, str] = field(default_factory=dict)
    shell_allowlist: set[str] = field(default_factory=lambda: {"ls", "cat", "echo", "wc", "grep"})
    audit: list[AuditEntry] = field(default_factory=list)
    open_tabs: list[str] = field(default_factory=list)

    def _log(self, actor: str, action: str, detail: str, undo: Callable[[], None] | None = None) -> None:
        self.audit.append(AuditEntry(time.time(), actor, action, detail, undo))

    # ---- filesystem --------------------------------------------------------------------
    def write(self, path: str, text: str, actor: str = "agent") -> None:
        prev = self.files.get(path)

        def undo() -> None:
            if prev is None:
                self.files.pop(path, None)
            else:
                self.files[path] = prev

        self.files[path] = text
        self._log(actor, "write", path, undo)

    def read(self, path: str) -> str:
        return self.files.get(path, f"<no such file: {path}>")

    # ---- browser -----------------------------------------------------------------------
    def open(self, url: str, actor: str = "agent") -> str:
        self.open_tabs.append(url)
        self._log(actor, "browse", url)
        if "login" in url:
            return "SIGN_IN_REQUIRED"
        return FAKE_PAGES.get(url, f"<html><title>{url}</title><p>Placeholder page</p></html>")

    # ---- shell -------------------------------------------------------------------------
    def sh(self, command: str, actor: str = "agent") -> str:
        argv = shlex.split(command)
        if not argv or argv[0] not in self.shell_allowlist:
            self._log(actor, "shell_denied", command)
            return f"denied: {argv[0] if argv else ''} not on allowlist"
        self._log(actor, "shell", command)
        if argv[0] == "ls":
            return "\n".join(sorted(self.files))
        if argv[0] == "cat" and len(argv) > 1:
            return self.read(argv[1])
        if argv[0] == "echo":
            return " ".join(argv[1:])
        if argv[0] == "wc" and len(argv) > 1:
            return str(len(self.read(argv[1]).split()))
        return ""

    # ---- undo --------------------------------------------------------------------------
    def undo_last(self) -> str:
        for entry in reversed(self.audit):
            if entry.undo:
                entry.undo()
                entry.undo = None
                self._log("user", "undo", entry.detail)
                return f"undid {entry.action} {entry.detail}"
        return "nothing to undo"

    def audit_report(self) -> list[str]:
        return [f"{e.actor:>8} | {e.action:<12} | {e.detail}" for e in self.audit]

    # ---- as tools ----------------------------------------------------------------------
    def tools(self) -> list[Tool]:
        pc = self

        @tool(risk=Risk.WRITE)
        def write_file(path: str, text: str) -> str:
            """Write a text file on the agent's computer."""
            pc.write(path, text)
            return f"wrote {path}"

        @tool(risk=Risk.READ)
        def read_file(path: str) -> str:
            """Read a text file on the agent's computer."""
            return pc.read(path)

        @tool(risk=Risk.READ)
        def open_url(url: str) -> str:
            """Open a URL in the agent's browser and return the page text."""
            return pc.open(url)

        @tool(risk=Risk.WRITE)
        def run_shell(command: str) -> str:
            """Run an allowlisted shell command on the agent's computer."""
            return pc.sh(command)

        return [write_file, read_file, open_url, run_shell]
