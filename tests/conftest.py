import pytest
from app.core.rate_limiting import limiter

@pytest.fixture(autouse=True)
def reset_rate_limits():
    try:
        limiter._storage.reset()
    except AttributeError:
        pass