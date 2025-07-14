from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_disease_crossfield_validation(test_user):
    # Create report with valid user_id
    report_id = client.post("/api/reports/", params={"created_by": test_user}).json()[
        "id"
    ]

    client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "Sam",
            "last_name": "Dean",
            "email": "sam@example.com",
            "job_title": "Doctor",
            "phone_number": "+123123123",
            "hospital_name": "Metro",
            "hospital_address": "456 St",
        },
    )
    client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "date_of_birth": "2000-01-01",
            "gender": "Female",
            "medical_record_number": "MED123",
            "patient_address": "789 St",
            "emergency_contact": "N/A",
        },
    )

    disease_resp = client.post(
        f"/api/reports/{report_id}/disease",
        json={
            "disease_name": "Flu",
            "disease_category": "Viral",
            "date_detected": "1999-01-01",
            "symptoms": ["Cough", "Fever"],
            "severity_level": "Low",
            "treatment_status": "Ongoing",
        },
    )
    assert disease_resp.status_code == 400


def test_disease_missing_patient(test_user):
    report_id = client.post("/api/reports/", params={"created_by": test_user}).json()[
        "id"
    ]
    client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "Mark",
            "last_name": "Jones",
            "email": "mark@example.com",
            "job_title": "Doctor",
            "phone_number": "+222222222",
            "hospital_name": "Metro",
            "hospital_address": "456 St",
        },
    )
    response = client.post(
        f"/api/reports/{report_id}/disease",
        json={
            "disease_name": "Cold",
            "disease_category": "Viral",
            "date_detected": "2020-01-01",
            "symptoms": ["Sneezing"],
            "severity_level": "Low",
            "treatment_status": "Ongoing",
        },
    )
    assert response.status_code == 400


def test_get_disease_not_found(test_user):
    invalid_report = 99999
    response = client.get(f"/api/reports/{invalid_report}/disease")
    assert response.status_code == 404
