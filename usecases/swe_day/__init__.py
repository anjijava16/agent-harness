"""A software engineer's day, 06:30 to midnight: 100 Deep Agents use cases, one folder each.

Folder names start with a number (001_..., 002_...) so they sort by time of day. They aren't
importable as packages, so this loader imports each folder's usecase.py by path and attaches
its schedule metadata (TIME, BLOCK, TRIGGER, AUTOMATION) to the UseCase.
"""

from __future__ import annotations

import importlib.util
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

BLOCKS = [
    ("morning", "06:30-08:30", "Before you sit down: scheduled digests and checks"),
    ("planning", "08:30-10:00", "Tickets, plans, designs"),
    ("coding", "10:00-12:30", "Writing, testing and fixing code"),
    ("review", "12:30-13:30", "Pull requests and code review"),
    ("ops", "13:30-16:00", "Incidents, infrastructure, support"),
    ("release", "16:00-18:30", "Shipping and wrapping up the day"),
    ("night", "18:30-00:00", "Unattended overnight automations"),
]


def load(folder: pathlib.Path):  # noqa: ANN201
    spec = importlib.util.spec_from_file_location(f"swe_{folder.name}", folder / "usecase.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    uc = mod.USECASE
    uc.time, uc.block, uc.trigger, uc.automation, uc.folder = mod.TIME, mod.BLOCK, mod.TRIGGER, mod.AUTOMATION, folder.name
    return uc


def all_usecases():  # noqa: ANN201
    folders = sorted(p for p in HERE.iterdir() if p.is_dir() and (p / "usecase.py").exists())
    return [load(f) for f in folders]
