"""Changelog entry from a PR

When:     12:55 (review)
Trigger:  webhook: pull_request.labeled
Type:     docs

Keeps CHANGELOG.md in Keep-a-Changelog format without anyone thinking about it.

Run:  python usecases/swe_day/042_changelog_entry/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/042_changelog_entry/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "12:55"
BLOCK = "review"
TRIGGER = "webhook: pull_request.labeled"
AUTOMATION = "docs"

USECASE = UseCase(
    id=42,
    domain="swe-" + BLOCK,
    title="Changelog entry from a PR",
    ask="Add a changelog entry for PR #812.",
    why="Keeps CHANGELOG.md in Keep-a-Changelog format without anyone thinking about it.",
    tools=[TOOL("get_pr", "PR metadata.", {"title": "Refunds API", "labels": ["feature"]}, {"pr": int})],
    seed_files={"/repo/CHANGELOG.md": "# Changelog\n\n## [Unreleased]\n### Added\n"},
    plan=[call("get_pr", pr=812), read("/repo/CHANGELOG.md"),
          edit("/repo/CHANGELOG.md", "### Added\n", "### Added\n- Refunds API (#812)\n"),
          say("Added 'Refunds API (#812)' under Unreleased / Added.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
