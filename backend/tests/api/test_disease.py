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
    """GET returns 404 when report does not exist."""
    response = client.get("/api/reports/9999/disease")
    assert response.status_code == 404
    assert response.json()["detail"] == "Report not found"


def test_get_disease_no_disease(client: TestClient, db_session, draft_report):
    """GET returns 404 when disease not assigned."""
    response = client.get(f"/api/reports/{draft_report.id}/disease")
    assert response.status_code == 404
    assert response.json()["detail"] == "No disease assigned to this report"


def test_create_disease_success(
    client: TestClient, auth_headers, db_session, draft_report, disease_payload
):
    """POST creates disease successfully."""
    response = client.post(
        f"/api/reports/{draft_report.id}/disease",
        headers=auth_headers,
        json=disease_payload,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["disease_name"] == disease_payload["disease_name"]
    assert data["severity_level"] == disease_payload["severity_level"]

    # Cleanup
    disease = db_session.query(Disease).filter_by(report_id=draft_report.id).first()
    if disease:
        db_session.delete(disease)
        db_session.commit()


def test_create_disease_future_date(
    client: TestClient, auth_headers, draft_report, disease_payload
):
    """POST rejects future date_detected."""
    disease_payload["date_detected"] = str(date.today() + timedelta(days=1))
    response = client.post(
        f"/api/reports/{draft_report.id}/disease",
        headers=auth_headers,
        json=disease_payload,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Date detected cannot be in the future"


def test_create_disease_non_draft(
    client: TestClient, auth_headers, db_session, test_user, disease_payload
):
    """POST rejects non-draft report."""
    report = Report(
        status="Submitted",
        created_by=test_user.id,
        creator=test_user,
    )
    db_session.add(report)
    db_session.commit()

    response = client.post(
        f"/api/reports/{report.id}/disease", headers=auth_headers, json=disease_payload
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot modify disease in non-draft report"

    db_session.delete(report)
    db_session.commit()


def test_update_disease(
    client: TestClient, auth_headers, db_session, draft_report, disease_payload
):
    """POST updates existing disease."""
    # First create
    client.post(
        f"/api/reports/{draft_report.id}/disease",
        headers=auth_headers,
        json=disease_payload,
    )

    # Update with new name
