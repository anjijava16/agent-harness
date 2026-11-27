"""OpenHands Software Agent SDK (MIT): a model-agnostic coding harness as a Python library.

The SDK is the core of OpenHands V1: agent, tools and workspaces are separate packages,
and the same code runs locally, in Docker, or against a remote agent server.

    pip install openhands-sdk openhands-tools        # package names per the OpenHands docs
    export LLM_MODEL=anthropic/claude-sonnet-4-5 LLM_API_KEY=...
    python harness_agents/examples/openhands_sdk_example.py

Live only (it needs a model). The structure mirrors the minimal example in the OpenHands
SDK paper and README.
"""

import os
import sys
import tempfile


def main() -> None:
    if not os.environ.get("LLM_API_KEY"):
        sys.exit("Set LLM_MODEL and LLM_API_KEY to run this example (it calls a real model).")
    from openhands.sdk import LLM, Conversation
    from openhands.tools.preset.default import get_default_agent

    llm = LLM(model=os.environ.get("LLM_MODEL", "anthropic/claude-sonnet-4-5"), api_key=os.environ["LLM_API_KEY"])
    agent = get_default_agent(llm=llm)
    workspace = tempfile.mkdtemp(prefix="openhands_")
    conversation = Conversation(agent=agent, workspace=workspace)
    conversation.send_message("Create reminders.py with format_reminder() and a passing test.")
    conversation.run()
    print("done; see", workspace)


if __name__ == "__main__":
    main()
