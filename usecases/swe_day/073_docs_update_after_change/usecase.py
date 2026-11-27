"""Update docs after an API change

When:     17:10 (release)
Trigger:  webhook: pull_request.merged
Type:     docs

Edits the real docs file so docs ship with the code.

Run:  python usecases/swe_day/073_docs_update_after_change/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/073_docs_update_after_change/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "17:10"
BLOCK = "release"
TRIGGER = "webhook: pull_request.merged"
AUTOMATION = "docs"

USECASE = UseCase(
    id=73,
    domain="swe-" + BLOCK,
    title="Update docs after an API change",
    ask="Update the API docs for the new Idempotency-Key header.",
    why="Edits the real docs file so docs ship with the code.",
    tools=[],
    seed_files={"/repo/docs/api/payments.md": "## POST /payments\nCreates a payment.\n"},
    plan=[read("/repo/docs/api/payments.md"),
          edit("/repo/docs/api/payments.md", "Creates a payment.\n", "Creates a payment.\n\nSend `Idempotency-Key` to make retries safe. Keys last 24h.\n"),
          say("Documented the Idempotency-Key header in docs/api/payments.md.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
