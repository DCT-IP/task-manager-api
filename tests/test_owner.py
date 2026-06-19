from fastapi.testclient import TestClient
from app.main import app
from tests.helpers import get_auth_headers

client = TestClient(app)


def test_task_has_owner():

    headers = get_auth_headers()

    response = client.post(
        "/tasks/",
        json={
            "title": "Owned Task"
        },
        headers=headers
    )

    assert response.status_code == 201

    task = response.json()

    assert task["owner_id"] is not None