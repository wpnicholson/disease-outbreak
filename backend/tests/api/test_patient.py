# tests/api/test_patient.py

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def patient_payload(test_run_id):
    """Fixture for patient creation payload with unique MRN"""
    return {
        "first_name": "Test",
        "last_name": "Patient",
        "date_of_birth": "1990-01-01",
        "gender": "Male",
        "medical_record_number": f"MRN-{test_run_id}",
        "patient_address": "123 Testing Lane",
        "emergency_contact": "Contact Person, +1234567890",
    }


def test_create_patient(client: TestClient, auth_headers, patient_payload):
    """Test patient creation via API and cleanup via API"""
    response = client.post(
        "/api/reports/patient", headers=auth_headers, json=patient_payload
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == patient_payload["first_name"]

    # Cleanup via API
    delete = client.delete(f"/api/reports/patient/{data['id']}", headers=auth_headers)
    assert delete.status_code == 204


def test_get_patient_by_id(client, auth_headers, patient_payload):
    """Test retrieval of a created patient"""
    create = client.post(
        "/api/reports/patient", headers=auth_headers, json=patient_payload
    )
    assert create.status_code == 201
    patient = create.json()

    get = client.get(f"/api/reports/patient/{patient['id']}", headers=auth_headers)
    assert get.status_code == 200
    assert get.json()["id"] == patient["id"]

    delete = client.delete(
        f"/api/reports/patient/{patient['id']}", headers=auth_headers
    )
    assert delete.status_code == 204


def test_get_patient_not_found(client, auth_headers):
    response = client.get("/api/reports/patient/99999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"


def test_delete_patient(client, auth_headers, patient_payload):
    create = client.post(
        "/api/reports/patient", headers=auth_headers, json=patient_payload
    )
    assert create.status_code == 201
    patient = create.json()

    delete = client.delete(
        f"/api/reports/patient/{patient['id']}", headers=auth_headers
    )
    assert delete.status_code == 204


def test_delete_patient_not_found(client, auth_headers):
    response = client.delete("/api/reports/patient/99999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"


@pytest.fixture(scope="function")
def test_report(client, auth_headers):
    """Create draft report via API and cleanup"""
    response = client.post("/api/reports", headers=auth_headers, json={})
    assert response.status_code == 201
    report = response.json()
    yield report
    client.delete(f"/api/reports/{report['id']}", headers=auth_headers)


def test_add_patients_to_report(client, auth_headers, patient_payload, test_report):
    create = client.post(
        "/api/reports/patient", headers=auth_headers, json=patient_payload
    )
    assert create.status_code == 201
    patient = create.json()

    response = client.post(
        f"/api/reports/{test_report['id']}/patient",
        headers=auth_headers,
        json={"patient_ids": [patient["id"]]},
    )
    assert response.status_code == 201
    assert any(p["id"] == patient["id"] for p in response.json())

    client.delete(f"/api/reports/patient/{patient['id']}", headers=auth_headers)


def test_add_patients_to_nonexistent_report(client, auth_headers):
    response = client.post(
        "/api/reports/99999/patient",
        headers=auth_headers,
        json={"patient_ids": [1]},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Report not found"


def test_add_nonexistent_patients_to_report(client, auth_headers, test_report):
    response = client.post(
        f"/api/reports/{test_report['id']}/patient",
        headers=auth_headers,
        json={"patient_ids": [99999]},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "One or more patients not found"


def test_get_patients_for_report(client, auth_headers, patient_payload, test_report):
    create = client.post(
        "/api/reports/patient", headers=auth_headers, json=patient_payload
    )
    assert create.status_code == 201
    patient = create.json()

    # Associate patient with report
    link = client.post(
        f"/api/reports/{test_report['id']}/patient",
        headers=auth_headers,
        json={"patient_ids": [patient["id"]]},
    )
    assert link.status_code == 201

    response = client.get(
        f"/api/reports/{test_report['id']}/patient", headers=auth_headers
    )
    assert response.status_code == 200
    assert any(p["id"] == patient["id"] for p in response.json())

    client.delete(f"/api/reports/patient/{patient['id']}", headers=auth_headers)


def test_get_patients_for_nonexistent_report(client, auth_headers):
    response = client.get("/api/reports/99999/patient", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Report not found"
