"""ADK 2.0 Workflow: @node(require_confirmation=True).

The simplest approval gate: the framework pauses *before* the node runs and asks for a
ToolConfirmation (confirmed: true/false). It can also be a predicate, e.g. only confirm
payments over $500. The confirmation request comes out as an adk_request_input call whose
id starts with "wf_tool_confirmation:".

Use case: paying a vendor bill. Small amounts go through; large ones need a yes.
"""

import asyncio
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from google.adk import Workflow  # noqa: E402
from google.adk.utils._function_call_names import REQUEST_INPUT_FUNCTION_CALL_NAME  # noqa: E402
from google.adk.workflow import START, node  # noqa: E402
from google.genai import types  # noqa: E402

from frameworks._fakes.adk_fake import run  # noqa: E402

PAID: list[dict] = []


def prepare(node_input) -> dict:  # noqa: ANN001
    amount = float(node_input.parts[0].text)
    return {"vendor": "Figma", "amount": amount}


@node(require_confirmation=lambda node_input, **_: node_input["amount"] > 500)
def pay_vendor(node_input: dict) -> str:
    PAID.append(node_input)
    return f"paid {node_input['vendor']} ${node_input['amount']:.2f}"


workflow = Workflow(name="pay_bill", edges=[(START, prepare, pay_vendor)])


async def pending_confirmation_id(runner, session) -> str | None:  # noqa: ANN001
    s = await runner.session_service.get_session(app_name="demo", user_id="me", session_id=session.id)
    for ev in reversed(s.events):
        for p in (ev.content.parts if ev.content and ev.content.parts else []):
            if p.function_call and p.function_call.name == REQUEST_INPUT_FUNCTION_CALL_NAME:
                return p.function_call.id
    return None


async def main() -> None:
    print("== $45 bill (under threshold) ==")
    await run(workflow, "45")
    print("\n== $1,200 bill (needs confirmation) ==")
    runner, session = await run(workflow, "1200")
    cid = await pending_confirmation_id(runner, session)
    print(f"  pending confirmation id: {cid}")
    yes = types.Content(role="user", parts=[types.Part(function_response=types.FunctionResponse(
        id=cid, name=REQUEST_INPUT_FUNCTION_CALL_NAME, response={"confirmed": True}))])
    await run(workflow, yes, runner=runner, session=session)
    print("\npaid:", PAID)


if __name__ == "__main__":
    asyncio.run(main())
