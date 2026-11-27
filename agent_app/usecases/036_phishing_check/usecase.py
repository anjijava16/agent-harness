"""Is this email phishing?

Area: inbox
Checks the sender domain and links. It never clicks anything.

Run:  python usecases/036_phishing_check/usecase.py                  # your preferred framework
      python usecases/036_phishing_check/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/036_phishing_check/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=36,
    area="inbox",
    title="Is this email phishing?",
    ask="Is the 'your account is locked' email real?",
    why="Checks the sender domain and links. It never clicks anything.",
    tools=[T("inspect_email", "Headers and links of an email.", {"id": int}, {"from_domain": "paypa1-support.com", "links": ["http://paypa1-support.com/login"], "spf": "fail"})],
    steps=[call("inspect_email", id=88),
           answer("That's phishing: the sender is paypa1-support.com (a 1 instead of an l) and SPF fails. Delete it, and don't click the link.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
