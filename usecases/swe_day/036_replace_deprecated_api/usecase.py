"""Replace a deprecated API

When:     12:20 (coding)
Trigger:  manual
Type:     upgrade

Mechanical upgrade with tests as the safety net.

Run:  python usecases/swe_day/036_replace_deprecated_api/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/036_replace_deprecated_api/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "12:20"
BLOCK = "coding"
TRIGGER = "manual"
AUTOMATION = "upgrade"

USECASE = UseCase(
    id=36,
    domain="swe-" + BLOCK,
    title="Replace a deprecated API",
    ask="Replace datetime.utcnow() (deprecated) across the service.",
    why="Mechanical upgrade with tests as the safety net.",
    tools=[TOOL("run_tests", "Run tests.", {"passed": 212, "failed": 0}, {"path": str})],
    seed_files={"/repo/payments/clock.py": "from datetime import datetime\n\ndef now():\n    return datetime.utcnow()\n"},
    plan=[call("grep", pattern="utcnow", path="/repo"),
          edit("/repo/payments/clock.py", "from datetime import datetime\n\ndef now():\n    return datetime.utcnow()",
               "from datetime import UTC, datetime\n\ndef now():\n    return datetime.now(UTC)"),
          call("run_tests", path="."),
          say("Replaced utcnow() with datetime.now(UTC); tests pass.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
