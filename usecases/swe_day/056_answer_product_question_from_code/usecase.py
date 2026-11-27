"""Answer a product question from the code

When:     14:35 (ops)
Trigger:  slack: #ask-payments
Type:     Q&A

Answers from the actual code, with the file and line, not from what someone remembers.

Run:  python usecases/swe_day/056_answer_product_question_from_code/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/056_answer_product_question_from_code/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "14:35"
BLOCK = "ops"
TRIGGER = "slack: #ask-payments"
AUTOMATION = "Q&A"

USECASE = UseCase(
    id=56,
    domain="swe-" + BLOCK,
    title="Answer a product question from the code",
    ask="PM asks: do we retry failed webhooks, and how many times?",
    why="Answers from the actual code, with the file and line, not from what someone remembers.",
    tools=[TOOL("search_code", "Search code.", ["webhooks/sender.py:14 MAX_RETRIES = 5", "webhooks/sender.py:15 BACKOFF = [1, 5, 30, 120, 600]"], {"query": str})],
    plan=[call("search_code", query="MAX_RETRIES webhooks"),
          say("Yes, 5 retries with backoff of 1s, 5s, 30s, 2m, 10m (webhooks/sender.py:14). After that the event is marked failed.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
