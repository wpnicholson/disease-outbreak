import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.database import Base, engine

client = TestClient(app)


# Ensure fresh database (for integration test purposes)
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_report():
    response = client.post("/api/reports/")
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
    # Create a report to get
    create_resp = client.post("/api/reports/")
    report_id = create_resp.json()["id"]

    response = client.get(f"/api/reports/{report_id}")
    assert response.status_code == 200
    assert response.json()["id"] == report_id


def test_update_report_status():
    create_resp = client.post("/api/reports/")
    report_id = create_resp.json()["id"]

    update_resp = client.put(f"/api/reports/{report_id}", json={"status": "Submitted"})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "Submitted"


def test_delete_report():
    create_resp = client.post("/api/reports/")
    report_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/api/reports/{report_id}")
    assert delete_resp.status_code == 204

    # Ensure report is actually deleted
    get_resp = client.get(f"/api/reports/{report_id}")
    assert get_resp.status_code == 404
