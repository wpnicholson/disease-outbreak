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


def test_add_disease_success(test_user):
    report_id = client.post("/api/reports/", params={"created_by": test_user}).json()[
        "id"
    ]
    client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "job_title": "Doctor",
            "phone_number": "+14155552671",
            "hospital_name": "Gen Hospital",
            "hospital_address": "Addr",
        },
    )
    client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "gender": "Male",
            "medical_record_number": "PAT100",
            "patient_address": "Addr",
            "emergency_contact": "None",
        },
    )
    response = client.post(
        f"/api/reports/{report_id}/disease",
        json={
            "disease_name": "Covid",
            "disease_category": "Viral",
            "date_detected": "2021-01-01",
            "symptoms": ["Cough"],
            "severity_level": "High",
            "treatment_status": "Ongoing",
        },
    )
    assert response.status_code == 200


def test_disease_overwrite_success(test_user):
    report_id = client.post("/api/reports/", params={"created_by": test_user}).json()[
        "id"
    ]
    client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "Y",
            "last_name": "Z",
            "email": "yz@example.com",
            "job_title": "Doctor",
            "phone_number": "+14155552671",
            "hospital_name": "Metro",
            "hospital_address": "Addr",
        },
    )
    client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "Alice",
            "last_name": "Bob",
            "date_of_birth": "2000-01-01",
            "gender": "Female",
            "medical_record_number": "PAT101",
            "patient_address": "Addr",
            "emergency_contact": "N/A",
        },
    )
    first_response = client.post(
        f"/api/reports/{report_id}/disease",
        json={
            "disease_name": "Cold",
            "disease_category": "Viral",
            "date_detected": "2021-01-01",
            "symptoms": ["Sneezing"],
            "severity_level": "Low",
            "treatment_status": "Ongoing",
        },
    )
    assert first_response.status_code == 200
    overwrite_response = client.post(
        f"/api/reports/{report_id}/disease",
        json={
            "disease_name": "Influenza",
            "disease_category": "Viral",
            "date_detected": "2021-01-01",
            "symptoms": ["Fever"],
            "severity_level": "Medium",
            "treatment_status": "Ongoing",
        },
    )
    assert overwrite_response.status_code == 200


def test_edit_disease_after_submission_forbidden(test_user):
    report_id = client.post("/api/reports/", params={"created_by": test_user}).json()[
        "id"
    ]
    client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "No",
            "last_name": "Edit",
            "email": "lock@example.com",
            "job_title": "Doctor",
            "phone_number": "+16665553333",
            "hospital_name": "Metro",
            "hospital_address": "Addr",
        },
    )
    client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "Locked",
            "last_name": "Patient",
            "date_of_birth": "1980-01-01",
            "gender": "Male",
            "medical_record_number": "LOCK100",
            "patient_address": "Addr",
            "emergency_contact": "None",
        },
    )
    client.post(
        f"/api/reports/{report_id}/disease",
        json={
            "disease_name": "Typhoid",
            "disease_category": "Bacterial",
            "date_detected": "2019-01-01",
            "symptoms": ["Fever"],
            "severity_level": "High",
            "treatment_status": "Ongoing",
        },
    )
    client.post(f"/api/reports/{report_id}/submit")
    response = client.post(
        f"/api/reports/{report_id}/disease",
        json={
            "disease_name": "Update",
            "disease_category": "Other",
            "date_detected": "2020-01-01",
            "symptoms": ["N/A"],
            "severity_level": "Critical",
            "treatment_status": "Completed",
        },
    )
    assert response.status_code == 400


def test_disease_categories():
    response = client.get("/api/reports/diseases/categories")
    assert response.status_code == 200
    assert "Viral" in response.json()
