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

# NEGATIVE TESTS :3

def test_get_nonexistent_task():
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_delete_nonexistent_task():
    response = client.delete("/tasks/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_update_nonexistent_task():
    response = client.put(
        "/tasks/999999",
        json={
            "title": "Updated"
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_empty_title():
    response = client.post(
        "/tasks/",
        json={
            "title": ""
        }
    )
    assert response.status_code == 422

def test_missing_title():
    response = client.post(
        "/tasks/",
        json={}
    )
    assert response.status_code == 422

def test_title_too_long():
    response = client.post(
        "/tasks/",
        json={
            "title": "A" * 101
        }
    )
    assert response.status_code == 422

def test_invalid_title_type():
    response = client.post(
        "/tasks/",
        json={
            "title": 12345
        }
    )
    assert response.status_code == 422
