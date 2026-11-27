"""Customer escalation investigation

When:     14:00 (ops)
Trigger:  webhook: support_escalation
Type:     investigation

Pulls the payment events and logs and writes up what actually happened for support.

Run:  python usecases/swe_day/052_customer_escalation_investigation/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/052_customer_escalation_investigation/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "14:00"
BLOCK = "ops"
TRIGGER = "webhook: support_escalation"
AUTOMATION = "investigation"

USECASE = UseCase(
    id=52,
    domain="swe-" + BLOCK,
    title="Customer escalation investigation",
    ask="Customer says they were charged twice for order 99812. Investigate.",
    why="Pulls the payment events and logs and writes up what actually happened for support.",
    tools=[TOOL("payment_events", "Payment events for an order.", [{"t": "10:01:02", "event": "charge", "id": "ch_1"}, {"t": "10:01:03", "event": "charge", "id": "ch_2"}], {"order": str}),
           TOOL("request_logs", "Request logs for an order.", ["POST /payments order=99812 (no Idempotency-Key)", "POST /payments order=99812 retry"], {"order": str})],
    plan=[par(call("payment_events", order="99812"), call("request_logs", order="99812")),
          say("Confirmed double charge: the client retried after 1s without an Idempotency-Key. Refund ch_2. PAY-431 fixes this class of bug.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
