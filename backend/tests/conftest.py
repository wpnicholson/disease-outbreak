import pytest
from api.database import Base, engine
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def test_user():
    signup_resp = client.post(
        "/api/auth/signup",
        json={
            "email": "testuser@example.com",
            "password": "strongpassword",
            "full_name": "Test User",
        },
    )
    assert signup_resp.status_code == 201
    return signup_resp.json()["id"]
