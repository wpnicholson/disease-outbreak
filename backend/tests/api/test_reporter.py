from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_reporter_flow(test_user):
    report_resp = client.post("/api/reports/", params={"created_by": test_user})
    report_id = report_resp.json()["id"]

    reporter_resp = client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "job_title": "Physician",
            "phone_number": "+14155552671",
            "hospital_name": "City Hospital",
            "hospital_address": "123 Main St",
        },
    )
    assert reporter_resp.status_code == 201

    get_resp = client.get(f"/api/reports/{report_id}/reporter")
    assert get_resp.status_code == 200
    assert get_resp.json()["email"] == "alice@example.com"
