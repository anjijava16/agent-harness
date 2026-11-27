"""OpenAPI contract draft

When:     09:50 (planning)
Trigger:  manual
Type:     API design

Writes the contract before the code so frontend and backend can work in parallel.

Run:  python usecases/swe_day/021_openapi_contract_draft/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/021_openapi_contract_draft/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "09:50"
BLOCK = "planning"
TRIGGER = "manual"
AUTOMATION = "API design"

USECASE = UseCase(
    id=21,
    domain="swe-" + BLOCK,
    title="OpenAPI contract draft",
    ask="Draft the OpenAPI spec for GET /invoices/export.",
    why="Writes the contract before the code so frontend and backend can work in parallel.",
    tools=[TOOL("existing_schemas", "Existing API schemas.", ["Invoice", "Error"])],
    plan=[call("existing_schemas", query="all"),
          write("/repo/api/openapi/invoices_export.yaml",
                "paths:\n  /invoices/export:\n    get:\n      parameters: [{name: format, in: query, schema: {enum: [csv]}}]\n      responses: {'200': {description: CSV file}}\n"),
          say("OpenAPI draft written for GET /invoices/export (format=csv), reusing the existing Error schema.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
