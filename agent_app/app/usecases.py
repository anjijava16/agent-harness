"""Loads usecases/NNN_slug/usecase.py folders (by path, since folder names start with digits)."""

from __future__ import annotations

import functools
import importlib.util
import pathlib

from .config import ROOT
from .spec import UseCase

UC_DIR = ROOT / "usecases"

AREAS = [
    ("mornings", "Mornings and daily planning"),
    ("inbox", "Email, messages and calendar"),
    ("money", "Bills, budget and money admin"),
    ("errands", "Shopping, groceries and errands"),
    ("travel", "Travel and getting around"),
    ("home", "Home, family and pets"),
    ("health", "Fitness, food and appointments"),
    ("work", "Work and career"),
    ("learning", "Learning and hobbies"),
    ("digital", "Documents, accounts and digital life"),
]


def load(folder: pathlib.Path) -> UseCase:
    spec = importlib.util.spec_from_file_location(f"uc_{folder.name}", folder / "usecase.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    uc: UseCase = mod.USECASE
    uc.folder = folder.name
    return uc


@functools.cache
def all_usecases() -> tuple[UseCase, ...]:
    return tuple(load(f) for f in sorted(p for p in UC_DIR.iterdir() if (p / "usecase.py").exists()))


def get(uc_id: int) -> UseCase:
    for u in all_usecases():
        if u.id == uc_id:
            return u
    raise KeyError(uc_id)
