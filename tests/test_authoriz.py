import uuid
from fastapi.testclient import TestClient
from app.main import app
from tests.helpers import create_user_and_login

client = TestClient(app)

def test_user_cannot_view_other_user_task():
    headers_a = create_user_and_login()
    create_response = client.post(
        "/tasks/",
        json={
            "title": "User A Task"
        },
        headers=headers_a
    )
    task_id = create_response.json()["id"]
    headers_b = create_user_and_login()
    response = client.get(
        f"/tasks/{task_id}",
        headers=headers_b
    )
    assert response.status_code == 403

def test_user_cannot_update_other_user_task():
    headers_a = create_user_and_login()
    create_response = client.post(
        "/tasks/",
        json={
            "title": "User A Task"
        },
        headers=headers_a
    )
    task_id = create_response.json()["id"]
    headers_b = create_user_and_login()
    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Hacked"
        },
        headers=headers_b
    )
    assert response.status_code == 403

def test_user_cannot_delete_other_user_task():
    headers_a = create_user_and_login()
    create_response = client.post(
        "/tasks/",
        json={
            "title": "Delete Test"
        },
        headers=headers_a
    )
    task_id = create_response.json()["id"]
    headers_b = create_user_and_login()
    response = client.delete(
        f"/tasks/{task_id}",
        headers=headers_b
    )
    assert response.status_code == 403

def test_user_sees_only_own_tasks():
    headers_a = create_user_and_login()
    client.post(
        "/tasks/",
        json={
            "title": "A Task"
        },
        headers=headers_a
    )
    headers_b = create_user_and_login()
    client.post(
        "/tasks/",
        json={
            "title": "B Task"
        },
        headers=headers_b
    )
    response = client.get(
        "/tasks/",
        headers=headers_a
    )
    tasks = response.json()
    titles = [
        task["title"]
        for task in tasks
    ]
    assert "A Task" in titles
    assert "B Task" not in titles

