from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_patient_validation(test_user):
    report_id = client.post("/api/reports/", params={"created_by": test_user}).json()[
        "id"
    ]
    client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "Dr.",
            "last_name": "Who",
            "email": "doctor@example.com",
            "job_title": "Doctor",
            "phone_number": "+111111111",
            "hospital_name": "TARDIS",
            "hospital_address": "Everywhere",
        },
    )

    future_dob = "2999-01-01"
    invalid_resp = client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": future_dob,
            "gender": "Male",
            "medical_record_number": "ABC123",
            "patient_address": "123 St",
            "emergency_contact": "None",
        },
    )
    assert invalid_resp.status_code == 400
