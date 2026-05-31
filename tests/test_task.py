from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_task():
    response = client.post(
        "/tasks/",
        json={
            "title": "Test Task"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["completed"] is False

def test_get_task():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_task():
    created = client.post(
        "/tasks/",
        json={
            "title": "Single Task"
        }
    )
    task_id = created.json()["id"]
    response = client.get(
        f"/tasks/{task_id}"
    )
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_update_task():
    created = client.post(
        "/tasks/",
        json={
            "title": "Old Title"
        }
    )
    task_id = created.json()["id"]
    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "New Title",
            "completed": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["completed"] is True

def test_delete_task():
    created = client.post(
        "/tasks/",
        json={
            "title": "Delete Me"
        }
    )
    task_id = created.json()["id"]
    response = client.delete(
        f"/tasks/{task_id}"
    )
    assert response.status_code == 200