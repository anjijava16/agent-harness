"""Free up cloud storage

Area: digital
Finds big duplicate files. Deleting needs approval, and the Photos folder is protected.

Run:  python usecases/183_free_up_storage/usecase.py                  # your preferred framework
      python usecases/183_free_up_storage/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/183_free_up_storage/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=183,
    area="digital",
    title="Free up cloud storage",
    ask="My cloud storage is full. Clean it up.",
    why="Finds big duplicate files. Deleting needs approval, and the Photos folder is protected.",
    tools=[T("big_files", "Largest files.", {"limit": int}, [{"path": "/Downloads/old_vm.iso", "gb": 12}, {"path": "/Photos/2019_backup.zip", "gb": 9}]),
           T("delete_file", "Delete a file.", {"path": str}, "deleted", "write")],
    steps=[call("big_files", limit=10), par(call("delete_file", path="/Downloads/old_vm.iso"), call("delete_file", path="/Photos/2019_backup.zip")),
           answer("Deleted old_vm.iso (12 GB). Nothing in /Photos is ever deleted.")],
    approvals={"delete_file": "approve"},
    guards={"delete_file": lambda a, p: "the Photos folder is protected" if a["path"].startswith("/Photos") else None},
    expect=[("photos untouched", lambda c: all(not a["args"]["path"].startswith("/Photos") for a in c["actions"]))]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
