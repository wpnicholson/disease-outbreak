import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta

from api.models import Report, Disease


@pytest.fixture(scope="function")
def draft_report(db_session, test_user):
    """Create a draft report linked to test user."""
    report = Report(
        status="Draft",
        created_by=test_user.id,
        creator=test_user,
    )
    db_session.add(report)
    db_session.commit()
    yield report
    db_session.delete(report)
    db_session.commit()


@pytest.fixture(scope="function")
def disease_payload():
    """Valid payload for Disease creation."""
    return {
        "disease_name": "TestDisease",
        "disease_category": "Viral",
        "date_detected": date.today().isoformat(),
        "symptoms": ["cough", "fever"],
        "severity_level": "Medium",
        "treatment_status": "Ongoing",
    }


def test_get_disease_not_found(client: TestClient):
    response = client.get("/api/reports/9999/disease")
    assert response.status_code == 404
    assert response.json()["detail"] == "Report not found"


def test_get_disease_no_disease(client: TestClient, draft_report):
    response = client.get(f"/api/reports/{draft_report.id}/disease")
    assert response.status_code == 404
    assert response.json()["detail"] == "No disease assigned to this report"


def test_create_disease_success(
    client, auth_headers, db_session, draft_report, disease_payload
):
    response = client.post(
        f"/api/reports/{draft_report.id}/disease",
        headers=auth_headers,
        json=disease_payload,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["disease_name"] == disease_payload["disease_name"]

    # Cleanup
    disease = db_session.query(Disease).filter_by(report_id=draft_report.id).first()
    if disease:
        db_session.delete(disease)
        db_session.commit()


def test_create_disease_future_date(
    client, auth_headers, draft_report, disease_payload
):
    future_date = (date.today() + timedelta(days=1)).isoformat()
    disease_payload["date_detected"] = future_date
    response = client.post(
        f"/api/reports/{draft_report.id}/disease",
        headers=auth_headers,
        json=disease_payload,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Date detected cannot be in the future"


def test_create_disease_non_draft(
    client, auth_headers, db_session, test_user, disease_payload
):
    report = Report(
        status="Submitted",
        created_by=test_user.id,
        creator=test_user,
    )
    db_session.add(report)
    db_session.commit()

    response = client.post(
        f"/api/reports/{report.id}/disease",
        headers=auth_headers,
        json=disease_payload,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot modify disease in non-draft report"

    db_session.delete(report)
    db_session.commit()


def test_update_disease(
    client, auth_headers, db_session, draft_report, disease_payload
):
    # Initial creation
    client.post(
        f"/api/reports/{draft_report.id}/disease",
        headers=auth_headers,
        json=disease_payload,
    )

    # Update
    disease_payload["disease_name"] = "UpdatedDisease"
    response = client.post(
        f"/api/reports/{draft_report.id}/disease",
        headers=auth_headers,
        json=disease_payload,
    )
    assert response.status_code == 201
    assert response.json()["disease_name"] == "UpdatedDisease"

    # Cleanup
    disease = db_session.query(Disease).filter_by(report_id=draft_report.id).first()
    if disease:
        db_session.delete(disease)
        db_session.commit()


def test_delete_disease_success(
    client, auth_headers, db_session, draft_report, disease_payload
):
    client.post(
        f"/api/reports/{draft_report.id}/disease",
        headers=auth_headers,
        json=disease_payload,
    )
    response = client.delete(
        f"/api/reports/{draft_report.id}/disease",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "Disease deleted successfully"


def test_delete_disease_not_found(client, auth_headers):
    response = client.delete("/api/reports/9999/disease", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Report not found"


def test_delete_disease_missing(client, auth_headers, draft_report):
    response = client.delete(
        f"/api/reports/{draft_report.id}/disease",
        headers=auth_headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "No disease to delete"


def test_delete_disease_non_draft(
    client, auth_headers, db_session, test_user, disease_payload
):
    report = Report(
        status="Submitted",
        created_by=test_user.id,
        creator=test_user,
    )
    db_session.add(report)
    db_session.commit()

    disease = Disease(
        disease_name=disease_payload["disease_name"],
        disease_category=disease_payload["disease_category"],
        date_detected=date.fromisoformat(disease_payload["date_detected"]),
        symptoms=disease_payload["symptoms"],
        severity_level=disease_payload["severity_level"],
        lab_results=None,
        treatment_status=disease_payload["treatment_status"],
        report=report,
    )
    db_session.add(disease)
    db_session.commit()

    response = client.delete(
        f"/api/reports/{report.id}/disease",
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot delete disease from non-draft report"

    db_session.delete(disease)
    db_session.delete(report)
    db_session.commit()
