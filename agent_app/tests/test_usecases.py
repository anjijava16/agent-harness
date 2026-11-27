"""All 200 use cases on all four frameworks (800 runs), auto-approved with each use case's own decisions."""

import asyncio

import pytest

from app import cache, config, runtimes, service, usecases

UCS = usecases.all_usecases()
AVAILABLE = runtimes.available()


def test_200_folders_with_unique_ids():
    assert len(UCS) == 200
    assert [u.id for u in UCS] == list(range(1, 201))
    assert all(u.folder.startswith(f"{u.id:03d}_") for u in UCS)
    assert {u.area for u in UCS} == {a for a, _ in usecases.AREAS}


@pytest.mark.parametrize("fw", config.FRAMEWORKS)
@pytest.mark.parametrize("uc", UCS, ids=lambda u: u.folder)
def test_usecase(uc, fw):
    if not AVAILABLE[fw]:
        pytest.skip(f"{fw} not installed")
    cache.clear_tool_cache()
    r = asyncio.run(service.start_run("test-user", uc.id, framework=fw, auto_approve=True))
    assert r["ok"], (r["status"], r["error"], [c for c in r["checks"] if not c[1]], r["final"])
