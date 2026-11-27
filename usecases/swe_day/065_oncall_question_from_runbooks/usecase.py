"""On-call Q&A from runbooks

When:     15:50 (ops)
Trigger:  slack: #payments-oncall
Type:     Q&A

Answers from the team's runbooks, not from memory, so on-call answers stay consistent.

Run:  python usecases/swe_day/065_oncall_question_from_runbooks/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/065_oncall_question_from_runbooks/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "15:50"
BLOCK = "ops"
TRIGGER = "slack: #payments-oncall"
AUTOMATION = "Q&A"

USECASE = UseCase(
    id=65,
    domain="swe-" + BLOCK,
    title="On-call Q&A from runbooks",
    ask="How do I replay dead-lettered webhooks?",
    why="Answers from the team's runbooks, not from memory, so on-call answers stay consistent.",
    tools=[],
    seed_files={"/runbooks/webhook-dlq.md": "Replay DLQ: `make replay-dlq QUEUE=webhooks LIMIT=100`. Check consumer lag first.\n"},
    plan=[call("grep", pattern="dead-letter|DLQ", path="/runbooks"), read("/runbooks/webhook-dlq.md"),
          say("Check consumer lag first, then run `make replay-dlq QUEUE=webhooks LIMIT=100`.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
