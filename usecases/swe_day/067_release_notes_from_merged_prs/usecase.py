"""Release notes from merged PRs

When:     16:00 (release)
Trigger:  webhook: release.drafted
Type:     docs

Groups merged PRs by label and writes notes that people actually read.

Run:  python usecases/swe_day/067_release_notes_from_merged_prs/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/067_release_notes_from_merged_prs/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "16:00"
BLOCK = "release"
TRIGGER = "webhook: release.drafted"
AUTOMATION = "docs"

USECASE = UseCase(
    id=67,
    domain="swe-" + BLOCK,
    title="Release notes from merged PRs",
    ask="Write release notes for payments-api v2.32.0.",
    why="Groups merged PRs by label and writes notes that people actually read.",
    tools=[TOOL("merged_prs", "PRs merged since the last tag.",
                [{"pr": 812, "title": "Refunds API", "label": "feature"}, {"pr": 820, "title": "Idempotency keys", "label": "feature"},
                 {"pr": 824, "title": "Fix rounding in refunds", "label": "bug"}], {"since": str})],
    plan=[call("merged_prs", since="v2.31.0"),
          write("/releases/v2.32.0.md", "## Features\n- Refunds API (#812)\n- Idempotency keys (#820)\n## Fixes\n- Rounding in refunds (#824)\n"),
          say("Release notes for v2.32.0: 2 features, 1 fix.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
