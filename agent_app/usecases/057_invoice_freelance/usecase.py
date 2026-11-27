"""Send an invoice for side work

Area: money
Uses your saved rate from memory. Sending the invoice needs approval.

Run:  python usecases/057_invoice_freelance/usecase.py                  # your preferred framework
      python usecases/057_invoice_freelance/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/057_invoice_freelance/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=57,
    area="money",
    title="Send an invoice for side work",
    ask="Invoice Bright Co for 6 hours of design work.",
    why="Uses your saved rate from memory. Sending the invoice needs approval.",
    tools=[T("send_invoice", "Send an invoice.", {"client": str, "hours": float, "rate": float}, "sent", "external")],
    steps=[recall("rate"), call("send_invoice", client="Bright Co", hours=6.0, rate=85.0),
           answer("Invoice sent to Bright Co: 6 hours at $85.")],
    approvals={"send_invoice": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
