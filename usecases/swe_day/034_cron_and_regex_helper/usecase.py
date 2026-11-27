"""Cron and regex helper

When:     12:10 (coding)
Trigger:  manual
Type:     helper

Small but error-prone; typed output you can paste.

Run:  python usecases/swe_day/034_cron_and_regex_helper/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/034_cron_and_regex_helper/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "12:10"
BLOCK = "coding"
TRIGGER = "manual"
AUTOMATION = "helper"

USECASE = UseCase(
    id=34,
    domain="swe-" + BLOCK,
    title="Cron and regex helper",
    ask="Cron for 'every weekday at 06:30 New York time', and a regex for invoice ids like INV-1038.",
    why="Small but error-prone; typed output you can paste.",
    tools=[],
    plan=[answer("Snippets", cron="CRON_TZ=America/New_York 30 6 * * 1-5", regex="^INV-\\d{4,}$")],
    output=("Snippets", {"cron": str, "regex": str})
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
