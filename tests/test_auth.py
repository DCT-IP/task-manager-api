from fastapi.testclient import TestClient
from app.main import app
import uuid
client = TestClient(app)

#Registration Test
def test_register_user():

    response = client.post(
        "/auth/register",
        json={
            "username": f"testuser{uuid.uuid4()}",
            "email": f"test{uuid.uuid4()}@test.com",
            "password": "secret123"
        }
    )

    assert response.status_code == 201

#login success 
def test_login_success():
    username = f"loginuser{uuid.uuid4().hex[:8]}"
    email = f"{username}@test.com"
    client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "secret123"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": "secret123"
        }
    )

    assert response.status_code == 200

#login failure
def test_login_failure():

    response = client.post(
        "/auth/login",
        json={
            "username": "loginuser",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401