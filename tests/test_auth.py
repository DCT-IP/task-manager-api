from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)


def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": f"user_{uuid.uuid4().hex[:8]}",
            "email": f"test{uuid.uuid4()}@test.com",
            "password": "Password123!"
        }
    )
    print(response.status_code)
    print(response.json())
    assert response.status_code == 201


def test_login_success():
    username = f"loginuser{uuid.uuid4().hex[:8]}"
    email = f"{username}@test.com"
    client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "Password123!"
        }
    )
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": username,
            "password": "Password123!"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "doesnotexist",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401

def test_short_username():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "ab",
            "email": f"{uuid.uuid4().hex}@test.com",
            "password": "Password123!"
        }
    )
    assert response.status_code == 422


def test_whitespace_username():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "     ",
            "email": f"{uuid.uuid4().hex}@test.com",
            "password": "Password123!"
        }
    )
    assert response.status_code == 422


def test_weak_password():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": f"user_{uuid.uuid4().hex[:8]}",
            "email": f"{uuid.uuid4().hex}@test.com",
            "password": "abc"
        }
    )
    assert response.status_code == 422

def test_invalid_email():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "not-an-email",
            "password": "Password123!"
        }
    )
    assert response.status_code == 422