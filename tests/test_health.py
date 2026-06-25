from fastapi.testclient import TestClient  #a fake client for testing the API
from app.main import app #importing the app

client = TestClient(app) #Object creation capable of requesting the API

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Task Manager API" in response.text

def test_health(client):
    response = client.get(
        "/api/v1/health/"
    )
    assert response.status_code == 200
    data = response.json()
    assert "status" in data