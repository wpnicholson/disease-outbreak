import pytest
from fastapi.testclient import TestClient
from api.models import User


@pytest.fixture(scope="function")
def signup_payload(test_run_id):
    return {
        "email": f"pytest-user-{test_run_id}@example.com",
        "password": "pytestpassword",
        "full_name": "Pytest User",
        "role": "Senior",
    }


def test_signup_success(client: TestClient, db_session, signup_payload):
    """Test successful user signup and cleanup created user."""
    response = client.post("/api/auth/signup", json=signup_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == signup_payload["email"]
    assert data["full_name"] == signup_payload["full_name"]
    assert data["is_active"] is True
    assert "id" in data
    assert "created_at" in data

    # Cleanup
    created_user = (
        db_session.query(User).filter(User.email == signup_payload["email"]).first()
    )
    if created_user:
        db_session.delete(created_user)
        db_session.commit()


def test_signup_duplicate_email(client: TestClient, test_user):
    """Test signup with duplicate email returns 400 error."""
    payload = {
        "email": test_user.email,
        "password": "pytestpassword",
        "full_name": "Duplicate User",
        "role": "Senior",
    }
    response = client.post("/api/auth/signup", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success(client: TestClient, test_user):
    """Test successful login returns access token."""
    login_data = {"email": test_user.email, "password": "strongpassword"}
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data


def test_login_nonexistent_email(client: TestClient):
    """Test login with nonexistent email returns 404."""
    login_data = {"email": "nonexistent@example.com", "password": "any-password"}
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_login_invalid_password(client: TestClient, test_user):
    """Test login with invalid password returns 401."""
    login_data = {"email": test_user.email, "password": "wrongpassword"}
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
