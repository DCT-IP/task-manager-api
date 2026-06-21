import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_auth_headers():

    username = f"user_{uuid.uuid4().hex[:8]}"
    email = f"{uuid.uuid4().hex[:8]}@test.com"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "secret123"
        }
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "secret123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def create_user_and_login():

    username = f"user_{uuid.uuid4().hex[:8]}"
    email = f"{uuid.uuid4().hex[:8]}@test.com"

    client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "secret123"
        }
    )

    login = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "secret123"
        }
    )

    token = login.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }