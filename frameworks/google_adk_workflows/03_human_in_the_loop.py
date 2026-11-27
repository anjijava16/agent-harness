"""ADK 2.0 Workflow: human-in-the-loop that durably waits.

Two built-in ways for a node to stop and ask a person:

1. return / yield RequestInput(interrupt_id=..., message=..., payload=...)
   The run ends with an `adk_request_input` function call event. Later, send a user
   message containing a FunctionResponse with the same id; the workflow resumes and the
   node (marked rerun_on_resume=True) finds the answer in ctx.resume_inputs[id].

2. @node(require_confirmation=True)
   The framework asks for approve/reject *before* running the node at all (see 06).

The paused state lives in the session, so the answer can arrive minutes or days later,
from a different process.

Use case: approve an outgoing reminder, possibly editing the text.
"""

import asyncio
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from google.adk import Context, Workflow  # noqa: E402
from google.adk.events.request_input import RequestInput  # noqa: E402
from google.adk.utils._function_call_names import REQUEST_INPUT_FUNCTION_CALL_NAME  # noqa: E402
from google.adk.workflow import START, node  # noqa: E402
from google.genai import types  # noqa: E402

from frameworks._fakes.adk_fake import run  # noqa: E402

OUTBOX: list[dict] = []


def draft(node_input) -> dict:  # noqa: ANN001, ARG001
    return {"to": "ap@northwind.com", "body": "Hi Northwind, INV-1038 is 14 days overdue."}


@node(rerun_on_resume=True)
def approval(ctx: Context, node_input: dict):  # noqa: ANN201
    answer = ctx.resume_inputs.get("approve-reminder")
    if answer is None:
        return RequestInput(interrupt_id="approve-reminder",
                            message=f"Send this to {node_input['to']}?", payload=node_input)
    if answer.get("decision") == "edit":
        node_input = {**node_input, "body": answer["body"]}
    ctx.route = "send" if answer.get("decision") in ("approve", "edit") else "drop"
    return node_input


def send(node_input: dict) -> str:
    OUTBOX.append(node_input)
    return f"sent to {node_input['to']}: {node_input['body']}"


def drop(node_input: dict) -> str:  # noqa: ARG001
    return "not sent"


workflow = Workflow(name="approve_reminder", edges=[
    (START, draft, approval),
    (approval, {"send": send, "drop": drop}),
])


def answer(payload: dict) -> types.Content:
    return types.Content(role="user", parts=[types.Part(function_response=types.FunctionResponse(
        id="approve-reminder", name=REQUEST_INPUT_FUNCTION_CALL_NAME, response=payload))])


async def main() -> None:
    print("== run 1: pauses and asks ==")
    runner, session = await run(workflow, "chase Northwind")
    print("\n== ...later: the human edits the text and approves ==")
    await run(workflow, answer({"decision": "edit", "body": "Quick note: INV-1038, pay link inside."}),
              runner=runner, session=session)
    print("\noutbox:", OUTBOX)


if __name__ == "__main__":
    asyncio.run(main())
