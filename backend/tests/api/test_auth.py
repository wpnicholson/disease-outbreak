from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_signup_and_login():
    signup_resp = client.post(
        "/api/auth/signup",
        json={
            "email": "authuser@example.com",
            "password": "strongpassword",
            "full_name": "Auth User",
        },
    )
    assert signup_resp.status_code == 201

    login_resp = client.post(
        "/api/auth/login",
        json={"email": "authuser@example.com", "password": "strongpassword"},
    )
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()
