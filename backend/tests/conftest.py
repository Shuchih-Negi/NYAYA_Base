"""Use a temp SQLite DB so integration tests do not touch developer nyaya.db."""
import os
import tempfile
from pathlib import Path

import pytest

_tmp = Path(tempfile.mkdtemp(prefix="nyaya_test_")) / "test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp.as_posix()}"
# Avoid real Gemini calls in tests unless explicitly enabled
os.environ.setdefault("GEMINI_API_KEY", "")

# Import app after env is set so engine binds to test DB
from app.main import app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
