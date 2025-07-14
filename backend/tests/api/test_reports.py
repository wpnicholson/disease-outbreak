from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def create_report(user_id):
    """Helper function to create a report associated with test user."""
    response = client.post("/api/reports/", params={"created_by": user_id})
    assert response.status_code == 201, response.text
    return response.json()["id"]


def test_create_report(user_id):
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


def test_get_specific_report(user_id):
    report_id = create_report(user_id)
    response = client.get(f"/api/reports/{report_id}")
    assert response.status_code == 200
    assert response.json()["id"] == report_id


def test_get_nonexistent_report():
    response = client.get("/api/reports/999999")
    assert response.status_code == 404


def test_update_report_status(user_id):
    report_id = create_report(user_id)
    update_resp = client.put(f"/api/reports/{report_id}", json={"status": "Submitted"})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "Submitted"


def test_update_nonexistent_report():
    response = client.put("/api/reports/999999", json={"status": "Submitted"})
    assert response.status_code == 404


def test_update_non_draft_report(user_id):
    report_id = create_report(user_id)
    # First, submit the report
    client.put(f"/api/reports/{report_id}", json={"status": "Submitted"})
    # Then, try to update it again
    response = client.put(f"/api/reports/{report_id}", json={"status": "Draft"})
    assert response.status_code == 400


def test_delete_report(user_id):
    report_id = create_report(user_id)
    delete_resp = client.delete(f"/api/reports/{report_id}")
    assert delete_resp.status_code == 204

    # Ensure report is actually deleted
    get_resp = client.get(f"/api/reports/{report_id}")
    assert get_resp.status_code == 404


def test_delete_nonexistent_report():
    response = client.delete("/api/reports/999999")
    assert response.status_code == 404


def test_delete_non_draft_report(user_id):
    report_id = create_report(user_id)
    client.put(f"/api/reports/{report_id}", json={"status": "Submitted"})
    response = client.delete(f"/api/reports/{report_id}")
    assert response.status_code == 400


def test_submit_report_without_required_links(user_id):
    report_id = create_report(user_id)
    response = client.post(f"/api/reports/{report_id}/submit")
    assert response.status_code == 400
    assert "Ensure reporter, patient, and disease are set" in response.json()["detail"]


def test_submit_nonexistent_report():
    response = client.post("/api/reports/999999/submit")
    assert response.status_code == 404


def test_submit_non_draft_report(user_id):
    report_id = create_report(user_id)
    client.put(f"/api/reports/{report_id}", json={"status": "Submitted"})
    response = client.post(f"/api/reports/{report_id}/submit")
    assert response.status_code == 400


def test_get_recent_reports():
    response = client.get("/api/reports/recent")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
