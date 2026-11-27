"""Mock an external API for tests

When:     11:25 (coding)
Trigger:  manual
Type:     test tooling

Captures real response shapes once, writes a fixture-backed fake.

Run:  python usecases/swe_day/029_mock_external_service/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/029_mock_external_service/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "11:25"
BLOCK = "coding"
TRIGGER = "manual"
AUTOMATION = "test tooling"

USECASE = UseCase(
    id=29,
    domain="swe-" + BLOCK,
    title="Mock an external API for tests",
    ask="Create a fake Stripe client for our tests from the real API responses.",
    why="Captures real response shapes once, writes a fixture-backed fake.",
    tools=[TOOL("sample_response", "A sample response from an external API.", {"id": "pi_123", "status": "succeeded", "amount": 2000}, {"endpoint": str})],
    plan=[call("sample_response", endpoint="POST /v1/payment_intents"),
          write("/repo/tests/fakes/fake_stripe.py", "class FakeStripe:\n    def create_intent(self, amount):\n        return {'id': 'pi_123', 'status': 'succeeded', 'amount': amount}\n"),
          say("FakeStripe written from a real payment_intents response shape.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
