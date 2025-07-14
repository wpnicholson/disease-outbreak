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


def test_patient_missing_reporter(test_user):
    report_id = client.post("/api/reports/", params={"created_by": test_user}).json()[
        "id"
    ]
    response = client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "Anna",
            "last_name": "Smith",
            "date_of_birth": "1990-01-01",
            "gender": "Female",
            "medical_record_number": "MRN001",
            "patient_address": "Address",
            "emergency_contact": "N/A",
        },
    )
    assert response.status_code == 400


def test_get_patient_not_found(test_user):
    invalid_report = 99999
    response = client.get(f"/api/reports/{invalid_report}/patient")
    assert response.status_code == 404


def test_add_patient_success(test_user):
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
            "phone_number": "+14155552671",
            "hospital_name": "TARDIS",
            "hospital_address": "Everywhere",
        },
    )
    response = client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "Amy",
            "last_name": "Pond",
            "date_of_birth": "1990-01-01",
            "gender": "Female",
            "medical_record_number": "MRN100",
            "patient_address": "Leadworth",
            "emergency_contact": "Rory",
        },
    )
    assert response.status_code == 201


def test_patient_duplicate_mrn_reuse(test_user):
    report1 = client.post("/api/reports/", params={"created_by": test_user}).json()[
        "id"
    ]
    report2 = client.post("/api/reports/", params={"created_by": test_user}).json()[
        "id"
    ]
    client.post(
        f"/api/reports/{report1}/reporter",
        json={
            "first_name": "Doc",
            "last_name": "One",
            "email": "doc1@example.com",
            "job_title": "Doctor",
            "phone_number": "+14155552671",
            "hospital_name": "Metro",
            "hospital_address": "Addr",
        },
    )
    client.post(
        f"/api/reports/{report2}/reporter",
        json={
            "first_name": "Doc",
            "last_name": "Two",
            "email": "doc2@example.com",
            "job_title": "Doctor",
            "phone_number": "+14155552672",
            "hospital_name": "Metro",
            "hospital_address": "Addr",
        },
    )
    patient_payload = {
        "first_name": "Sam",
        "last_name": "Smith",
        "date_of_birth": "1980-01-01",
        "gender": "Male",
        "medical_record_number": "DUPLICATE123",
        "patient_address": "Place",
        "emergency_contact": "N/A",
    }
    client.post(f"/api/reports/{report1}/patient", json=patient_payload)
    response = client.post(f"/api/reports/{report2}/patient", json=patient_payload)
    assert response.status_code == 201


def test_edit_patient_after_submission_forbidden(test_user):
    report_id = client.post("/api/reports/", params={"created_by": test_user}).json()[
        "id"
    ]
    client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "X",
            "last_name": "Y",
            "email": "xy@example.com",
            "job_title": "Doctor",
            "phone_number": "+15555555555",
            "hospital_name": "ABC",
            "hospital_address": "Addr",
        },
    )
    client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "Pat",
            "last_name": "Ent",
            "date_of_birth": "1970-01-01",
            "gender": "Male",
            "medical_record_number": "LOCKED123",
            "patient_address": "Somewhere",
            "emergency_contact": "No one",
        },
    )
    client.post(f"/api/reports/{report_id}/submit")
    response = client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "Patch",
            "last_name": "Edit",
            "date_of_birth": "1970-01-01",
            "gender": "Male",
            "medical_record_number": "LOCKED123",
            "patient_address": "New Addr",
            "emergency_contact": "Still no one",
        },
    )
    assert response.status_code == 400
