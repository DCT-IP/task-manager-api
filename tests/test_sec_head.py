from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_security_headers():
    response = client.get("/api/v1/health")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert (
        response.headers["Referrer-Policy"]
        == "strict-origin-when-cross-origin"
    )
    assert (
        response.headers["Permissions-Policy"]
        == "geolocation=(), microphone=(), camera=()"
    )