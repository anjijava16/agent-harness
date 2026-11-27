"""Scaffold a feature from the service template

When:     09:10 (planning)
Trigger:  manual
Type:     scaffolding

Reads the team's template files and writes the new module skeleton so you start from
conventions, not a blank page.

Run:  python usecases/swe_day/017_scaffold_feature_branch/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/017_scaffold_feature_branch/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "09:10"
BLOCK = "planning"
TRIGGER = "manual"
AUTOMATION = "scaffolding"

USECASE = UseCase(
    id=17,
    domain="swe-" + BLOCK,
    title="Scaffold a feature from the service template",
    ask="Scaffold the invoice-export module from our template.",
    why="Reads the team's template files and writes the new module skeleton so you start from conventions, not a blank page.",
    tools=[TOOL("create_branch", "Create a git branch.", "branch created", {"name": str}, "write")],
    seed_files={"/templates/module/service.py": "class {Name}Service:\n    def __init__(self, repo):\n        self.repo = repo\n",
                "/templates/module/test_service.py": "def test_{name}_smoke():\n    assert True\n"},
    plan=[call("create_branch", name="feature/PAY-440-invoice-export"),
          read("/templates/module/service.py"),
          write("/repo/payments/invoice_export/service.py", "class InvoiceExportService:\n    def __init__(self, repo):\n        self.repo = repo\n"),
          write("/repo/payments/invoice_export/test_service.py", "def test_invoice_export_smoke():\n    assert True\n"),
          say("Branch feature/PAY-440-invoice-export created with the module and test skeleton from the template.")],
    expect=[("module written", lambda c: "/repo/payments/invoice_export/service.py" in c["files"])]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
