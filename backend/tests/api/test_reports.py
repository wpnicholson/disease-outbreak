import pytest
from fastapi.testclient import TestClient
from api.models import User
from api.main import app
from api.database import Base, engine, SessionLocal

client = TestClient(app)

# Global variable to store created user ID across tests
user_id = None


# Ensure fresh database (for integration test purposes)
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    global user_id

    # Setup the database.
    Base.metadata.create_all(bind=engine)

    # Create a test user.
    db = SessionLocal()
    user = User(
        email="test@example.com", hashed_password="hashed", full_name="Test User"
    )
    db.add(user)
    db.commit()
    user_id = user.id
    db.close()

    yield

    # Teardown the database.
    Base.metadata.drop_all(bind=engine)


def create_report():
    """Helper function to create a report associated with test user."""
    response = client.post("/api/reports/", params={"created_by": user_id})
    assert response.status_code == 201, response.text
    return response.json()["id"]


def test_create_report():
    response = client.post("/api/reports/", params={"created_by": user_id})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["status"] == "Draft"


def test_list_reports():
    response = client.get("/api/reports/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # At least the one we created


def test_get_specific_report():
    report_id = create_report()
    response = client.get(f"/api/reports/{report_id}")
    assert response.status_code == 200
    assert response.json()["id"] == report_id


def test_update_report_status():
    report_id = create_report()
    update_resp = client.put(f"/api/reports/{report_id}", json={"status": "Submitted"})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "Submitted"


def test_delete_report():
    report_id = create_report()
    delete_resp = client.delete(f"/api/reports/{report_id}")
    assert delete_resp.status_code == 204

    # Ensure report is actually deleted
    get_resp = client.get(f"/api/reports/{report_id}")
    assert get_resp.status_code == 404
