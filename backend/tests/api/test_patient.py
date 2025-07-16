# tests/api/test_patient.py

import pytest
from fastapi.testclient import TestClient
from api.models import Patient, Report


@pytest.fixture(scope="function")
def patient_payload(test_run_id):
    """Fixture for patient creation payload"""
    return {
        "first_name": "Test",
        "last_name": "Patient",
        "date_of_birth": "1990-01-01",
        "gender": "Male",
        "medical_record_number": f"MRN-{test_run_id}",
        "patient_address": "123 Testing Lane",
        "emergency_contact": "Contact Person, +1234567890",
    }


def test_create_patient(
    client: TestClient, db_session, auth_headers, patient_payload, test_run_id
):
    """Test creating a patient and cleaning it up"""
    response = client.post(
        "/api/reports/patient", headers=auth_headers, json=patient_payload
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == patient_payload["first_name"]

    # Cleanup
    patient = (
        db_session.query(Patient)
        .filter(
            Patient.medical_record_number == patient_payload["medical_record_number"]
        )
        .first()
    )
    db_session.delete(patient)
    db_session.commit()


def test_get_patient_by_id(
    client: TestClient, db_session, auth_headers, patient_payload, test_run_id
):
    """Test retrieving patient by ID"""
    # Create patient
    patient = Patient(**patient_payload)
    db_session.add(patient)
    db_session.commit()
    db_session.refresh(patient)

    response = client.get(f"/api/reports/patient/{patient.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == patient.id

    db_session.delete(patient)
    db_session.commit()


def test_get_patient_not_found(client: TestClient, auth_headers):
    """Test retrieving non-existent patient returns 404"""
    response = client.get("/api/reports/patient/99999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"


def test_delete_patient(
    client: TestClient, db_session, auth_headers, patient_payload, test_run_id
):
    """Test deleting a patient"""
    patient = Patient(**patient_payload)
    db_session.add(patient)
    db_session.commit()
    db_session.refresh(patient)

    response = client.delete(f"/api/reports/patient/{patient.id}", headers=auth_headers)
    assert response.status_code == 204

    # Verify deletion
    assert db_session.query(Patient).filter(Patient.id == patient.id).first() is None


def test_delete_patient_not_found(client: TestClient, auth_headers):
    """Test deleting non-existent patient returns 404"""
    response = client.delete("/api/reports/patient/99999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"


@pytest.fixture(scope="function")
def test_report(db_session, test_user):
    """Create a report fixture to associate patients with"""
    report = Report(status="Draft", created_by=test_user.id)
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)
    yield report

    # Clean up patients and report after test
    report.patients.clear()
    db_session.delete(report)
    db_session.commit()


def test_add_patients_to_report(
    client: TestClient, db_session, auth_headers, patient_payload, test_report
):
    """Test adding patients to a report"""
    # Create patient
    patient = Patient(**patient_payload)
    db_session.add(patient)
    db_session.commit()
    db_session.refresh(patient)

    payload = {"patient_ids": [patient.id]}
    response = client.post(
        f"/api/reports/{test_report.id}/patient", headers=auth_headers, json=payload
    )
    assert response.status_code == 201
    assert any(p["id"] == patient.id for p in response.json())

    db_session.delete(patient)
    db_session.commit()


def test_add_patients_to_nonexistent_report(client: TestClient, auth_headers):
    """Test adding patients to a non-existent report"""
    response = client.post(
        "/api/reports/99999/patient", headers=auth_headers, json={"patient_ids": [1]}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Report not found"


def test_add_nonexistent_patients_to_report(
    client: TestClient, auth_headers, test_report
):
    """Test adding invalid patient IDs returns 404"""
    response = client.post(
        f"/api/reports/{test_report.id}/patient",
        headers=auth_headers,
        json={"patient_ids": [99999]},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "One or more patients not found"


def test_get_patients_for_report(
    client: TestClient, db_session, auth_headers, patient_payload, test_report
):
    """Test getting patients linked to a report"""
    patient = Patient(**patient_payload)
    db_session.add(patient)
    db_session.commit()
    db_session.refresh(patient)

    test_report.patients.append(patient)
    db_session.commit()

    response = client.get(
        f"/api/reports/{test_report.id}/patient", headers=auth_headers
    )
    assert response.status_code == 200
    assert any(p["id"] == patient.id for p in response.json())

    db_session.delete(patient)
    db_session.commit()


def test_get_patients_for_nonexistent_report(client: TestClient, auth_headers):
    """Test getting patients for non-existent report returns 404"""
    response = client.get("/api/reports/99999/patient", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Report not found"
