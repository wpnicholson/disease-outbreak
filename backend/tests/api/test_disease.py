# tests/api/test_disease.py

import pytest
from datetime import date, timedelta
from sqlalchemy.orm import Session
from collections.abc import Generator
from api.models import Report, Disease, ReportStateEnum
from api.database import SessionLocal


@pytest.fixture
def client(client):
    return client


@pytest.fixture
def db() -> Generator[Session, None, None]:
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def auth_header(test_user_token):
    return {"Authorization": f"Bearer {test_user_token}"}


def create_draft_report_with_user(db: Session, user_id: int) -> Report:
    report = Report(status=ReportStateEnum.draft, created_by=user_id)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def test_get_disease_not_found(client, auth_header, db):
    response = client.get("/api/reports/999/disease", headers=auth_header)
    assert response.status_code == 404


def test_create_disease_success(client, auth_header, db, test_user):
    report = create_draft_report_with_user(db, test_user.id)

    disease_data = {
        "disease_name": "Test Disease",
        "disease_category": "Bacterial",
        "date_detected": date.today().isoformat(),
        "symptoms": ["fever", "rash"],
        "severity_level": "Medium",
        "treatment_status": "Ongoing",
    }

    response = client.post(
        f"/api/reports/{report.id}/disease", json=disease_data, headers=auth_header
    )
    assert response.status_code == 200
    assert response.json()["disease_name"] == "Test Disease"

    # Disease should be attached in DB
    db.refresh(report)
    assert report.disease is not None


def test_create_disease_invalid_date(client, auth_header, db, test_user):
    report = create_draft_report_with_user(db, test_user.id)

    disease_data = {
        "disease_name": "Future Disease",
        "disease_category": "Viral",
        "date_detected": (date.today() + timedelta(days=10)).isoformat(),
        "symptoms": ["cough"],
        "severity_level": "High",
        "treatment_status": "Ongoing",
    }

    response = client.post(
        f"/api/reports/{report.id}/disease", json=disease_data, headers=auth_header
    )
    assert response.status_code == 400
    assert "future" in response.json()["detail"]


def test_update_disease_success(client, auth_header, db, test_user):
    report = create_draft_report_with_user(db, test_user.id)

    # Initial disease
    disease = Disease(
        disease_name="Initial Disease",
        disease_category="Bacterial",
        date_detected=date.today(),
        symptoms=["initial symptom"],
        severity_level="Low",
        treatment_status="Ongoing",
        report=report,
    )
    db.add(disease)
    db.commit()

    update_data = {
        "disease_name": "Updated Disease",
        "disease_category": "Parasitic",
        "date_detected": date.today().isoformat(),
        "symptoms": ["updated symptom"],
        "severity_level": "Critical",
        "treatment_status": "Completed",
    }

    response = client.post(
        f"/api/reports/{report.id}/disease", json=update_data, headers=auth_header
    )
    assert response.status_code == 200
    assert response.json()["disease_name"] == "Updated Disease"

    db.refresh(report)
    assert report.disease.disease_name == "Updated Disease"


def test_delete_disease_success(client, auth_header, db, test_user):
    report = create_draft_report_with_user(db, test_user.id)

    disease = Disease(
        disease_name="To Delete",
        disease_category="Viral",
        date_detected=date.today(),
        symptoms=["symptom"],
        severity_level="Medium",
        treatment_status="Ongoing",
        report=report,
    )
    db.add(disease)
    db.commit()

    response = client.delete(f"/api/reports/{report.id}/disease", headers=auth_header)
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["detail"]

    db.refresh(report)
    assert report.disease is None


def test_prevent_changes_on_submitted_report(client, auth_header, db, test_user):
    report = create_draft_report_with_user(db, test_user.id)
    report.status = ReportStateEnum.submitted
    db.commit()

    disease_data = {
        "disease_name": "Should Fail",
        "disease_category": "Other",
        "date_detected": date.today().isoformat(),
        "symptoms": ["symptom"],
        "severity_level": "High",
        "treatment_status": "None",
    }

    post_response = client.post(
        f"/api/reports/{report.id}/disease", json=disease_data, headers=auth_header
    )
    assert post_response.status_code == 400

    delete_response = client.delete(
        f"/api/reports/{report.id}/disease", headers=auth_header
    )
    assert delete_response.status_code == 400
