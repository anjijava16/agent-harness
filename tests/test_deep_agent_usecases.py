"""All 100 Deep Agents use cases must pass. Skipped when deepagents isn't installed
(the base test suite stays stdlib-only)."""

import pytest

pytest.importorskip("deepagents")

from usecases.catalog import all_usecases  # noqa: E402
from usecases.engine import run  # noqa: E402

UCS = all_usecases()


def test_there_are_100_with_unique_ids():
    assert len(UCS) == 100 and len({u.id for u in UCS}) == 100


@pytest.mark.parametrize("uc", UCS, ids=lambda u: f"{u.id:03d}-{u.domain}")
def test_usecase(uc):
    r = run(uc)
    assert r.ok, (r.error, [c for c in r.checks if not c[1]])
