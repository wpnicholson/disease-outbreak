import pytest
from api.database import SessionLocal, Base
from fastapi.testclient import TestClient
from api.main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def db_cleanup():
    """Cleanup all data between tests without touching the schema."""
    db = SessionLocal()
    yield
    # Truncate only data, not tables:
    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        if table.name != "alembic_version":
            db.execute(table.delete())
    db.commit()
    db.close()


@pytest.fixture(scope="module")
def test_user(client):
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
