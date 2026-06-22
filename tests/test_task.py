from fastapi.testclient import TestClient
from app.main import app
from tests.helpers import get_auth_headers

client = TestClient(app)


def test_create_task():
    headers = get_auth_headers()
    response = client.post(
        "/tasks/",
        json={
            "title": "Test Task"
        },
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["completed"] is False


def test_get_task():
    headers = get_auth_headers()
    response = client.get(
        "/tasks/",
        headers=headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_task():
    headers = get_auth_headers()
    created = client.post(
        "/tasks/",
        json={
            "title": "Single Task"
        },
        headers=headers
    )
    task_id = created.json()["id"]
    response = client.get(
        f"/tasks/{task_id}",
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_update_task():
    headers = get_auth_headers()
    created = client.post(
        "/tasks/",
        json={
            "title": "Old Title"
        },
        headers=headers
    )
    task_id = created.json()["id"]
    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "New Title",
            "completed": True
        },
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["completed"] is True


def test_delete_task():
    headers = get_auth_headers()
    created = client.post(
        "/tasks/",
        json={
            "title": "Delete Me"
        },
        headers=headers
    )
    task_id = created.json()["id"]
    response = client.delete(
        f"/tasks/{task_id}",
        headers=headers
    )
    assert response.status_code == 200


def test_get_nonexistent_task():
    headers = get_auth_headers()
    response = client.get(
        "/tasks/9999",
        headers=headers
    )
    assert response.status_code == 404


def test_delete_nonexistent_task():
    headers = get_auth_headers()
    response = client.delete(
        "/tasks/999999",
        headers=headers
    )
    assert response.status_code == 404


def test_update_nonexistent_task():
    headers = get_auth_headers()
    response = client.put(
        "/tasks/999999",
        json={
            "title": "Updated"
        },
        headers=headers
    )
    assert response.status_code == 404


def test_empty_title():
    headers = get_auth_headers()
    response = client.post(
        "/tasks/",
        json={
            "title": ""
        },
        headers=headers
    )
    assert response.status_code == 422


def test_missing_title():
    headers = get_auth_headers()
    response = client.post(
        "/tasks/",
        json={},
        headers=headers
    )
    assert response.status_code == 422


def test_title_too_long():
    headers = get_auth_headers()
    response = client.post(
        "/tasks/",
        json={
            "title": "A" * 101
        },
        headers=headers
    )
    assert response.status_code == 422


def test_invalid_title_type():

    headers = get_auth_headers()
    response = client.post(
        "/tasks/",
        json={
            "title": 12345
        },
        headers=headers
    )
    assert response.status_code == 422


def test_whitespace_title():
    headers = get_auth_headers()
    response = client.post(
        "/tasks/",
        json = {
            "title": "  "
        },
        headers=headers
    )
    assert response.status_code == 422


def test_description_too_long():
    headers = get_auth_headers()
    response = client.post(
        "/tasks/",
        json={
            "title": "Valid Title",
            "description": "A" * 1001
        },
        headers=headers
    )
    assert response.status_code == 422