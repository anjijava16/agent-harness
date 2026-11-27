import os
import pathlib
import sys
import tempfile

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Tests use a throwaway SQLite file and in-process Redis unless you point them elsewhere:
#   TEST_DATABASE_URL=postgresql+psycopg://... TEST_REDIS_URL=redis://localhost:6379/15 pytest
os.environ.setdefault("DATABASE_URL", os.environ.get("TEST_DATABASE_URL") or f"sqlite:///{tempfile.mkdtemp()}/test.db")
os.environ.setdefault("REDIS_URL", os.environ.get("TEST_REDIS_URL", ""))


@pytest.fixture(scope="session", autouse=True)
def _stores():
    from app import cache, config, db

    db.init(config.DATABASE_URL)
    cache.connect(config.REDIS_URL)
    yield
