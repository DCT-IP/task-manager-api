from fastapi.testclient import TestClient
from app.main import app
from tests.helpers import get_auth_headers
import uuid

client = TestClient(app)


def test_login_rate_limit():

    for _ in range(5):
        client.post(
            "/auth/login",
            data={
                "username": "wronguser",
                "password": "wrongpass"
            }
        )

    response = client.post(
        "/auth/login",
        data={
            "username": "wronguser",
            "password": "wrongpass"
        }
    )

    assert response.status_code == 429


def test_register_rate_limit():

    for _ in range(3):
        response = client.post(
            "/auth/register",
            json={
                "username": f"user_{uuid.uuid4().hex[:8]}",
                "email": f"{uuid.uuid4().hex[:8]}@test.com",
                "password": "secret123"
            }
        )

        assert response.status_code == 201

    response = client.post(
        "/auth/register",
        json={
            "username": f"user_{uuid.uuid4().hex[:8]}",
            "email": f"{uuid.uuid4().hex[:8]}@test.com",
            "password": "secret123"
        }
    )

    assert response.status_code == 429


def test_create_task_rate_limit():

    headers = get_auth_headers()

    for i in range(20):
        client.post(
            "/tasks/",
            json={
                "title": f"Task {i}"
            },
            headers=headers
        )

    response = client.post(
        "/tasks/",
        json={
            "title": "Blocked"
        },
        headers=headers
    )

    assert response.status_code == 429


def test_get_tasks_rate_limit():

    headers = get_auth_headers()

    for _ in range(60):
        client.get(
            "/tasks/",
            headers=headers
        )

    response = client.get(
        "/tasks/",
        headers=headers
    )

    assert response.status_code == 429


def test_update_task_rate_limit():

    headers = get_auth_headers()

    created = client.post(
        "/tasks/",
        json={
            "title": "Initial Task"
        },
        headers=headers
    )

    assert created.status_code == 201

    task_id = created.json()["id"]

    for i in range(20):
        client.put(
            f"/tasks/{task_id}",
            json={
                "title": f"Updated {i}"
            },
            headers=headers
        )

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Blocked"
        },
        headers=headers
    )

    assert response.status_code == 429