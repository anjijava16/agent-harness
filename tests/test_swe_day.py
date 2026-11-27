"""The software-engineer-day use cases (usecases/swe_day/NNN_*/) must all pass.
Skipped when deepagents isn't installed."""

import pytest

pytest.importorskip("deepagents")

from usecases.engine import run  # noqa: E402
from usecases.swe_day import BLOCKS, all_usecases  # noqa: E402

UCS = all_usecases()


def test_one_folder_per_usecase_in_time_order():
    assert len(UCS) == 100 and [u.id for u in UCS] == list(range(1, 101))
    assert all(u.folder.startswith(f"{u.id:03d}_") for u in UCS)
    assert [u.time for u in UCS] == sorted(u.time for u in UCS)
    assert {u.block for u in UCS} == {b for b, _, _ in BLOCKS}


@pytest.mark.parametrize("uc", UCS, ids=lambda u: u.folder)
def test_swe_usecase(uc):
    r = run(uc)
    assert r.ok, (r.error, [c for c in r.checks if not c[1]])
