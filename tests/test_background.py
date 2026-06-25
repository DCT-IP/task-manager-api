# tests/test_background.py

def test_background_route(client):

    response = client.post(
        "/background/email?email=test@test.com"
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Email scheduled"
    )