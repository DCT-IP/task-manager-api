def test_background_route(client):
    response = client.post(
        "/api/v1/background/email?email=test@test.com"
    )
    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "Email scheduled"
    )