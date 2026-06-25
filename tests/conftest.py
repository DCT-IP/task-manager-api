import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.rate_limiting import limiter


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_rate_limits():
    try:
        limiter._storage.reset()
    except AttributeError:
        pass