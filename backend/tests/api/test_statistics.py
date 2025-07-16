import pytest
from datetime import date, timedelta
from api.models import Disease, Report, Patient
from api.enums import (
    DiseaseCategoryEnum,
    SeverityLevelEnum,
    TreatmentStatusEnum,
    ReportStateEnum,
    GenderEnum,
)


@pytest.fixture(scope="function")
def setup_statistics_data(db_session, test_user, test_run_id):
    """Seed minimal data for statistics endpoint and cleanup after test."""
    report = Report(
        status=ReportStateEnum.draft,
        created_by=test_user.id,
        creator=test_user,
    )
    db_session.add(report)
    db_session.commit()

    disease = Disease(
        disease_name=f"TestDisease-{test_run_id}",
        disease_category=DiseaseCategoryEnum.viral,
        date_detected=date.today() - timedelta(days=10),
        symptoms=["cough", "fever"],
        severity_level=SeverityLevelEnum.medium,
        treatment_status=TreatmentStatusEnum.ongoing,
        report_id=report.id,
    )
    db_session.add(disease)

    patient = Patient(
        first_name="John",
        last_name="Doe",
        date_of_birth=date.today() - timedelta(days=30 * 365),
        gender=GenderEnum.male,
        medical_record_number=f"MRN-{test_run_id}",
        patient_address="123 Example Street",
    )
    db_session.add(patient)
    db_session.commit()

    report.patients.append(patient)
    db_session.commit()

    yield report, disease, patient

    # ✅ Only delete report (handles disease + associations)
    db_session.query(Report).filter(Report.id == report.id).delete()
    # ✅ Clean up patient explicitly
    db_session.query(Patient).filter(Patient.id == patient.id).delete()
    db_session.commit()


def test_statistics_authenticated(client, auth_headers, setup_statistics_data):
    """Test authenticated statistics retrieval returns expected data."""
    response = client.get("/api/statistics", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()

    assert "total_reports" in data
    assert "reports_by_status" in data
    assert "diseases_by_category" in data
    assert "diseases_by_severity" in data
    assert "average_patient_age" in data
    assert "most_common_disease" in data

    # Validate at least our seeded data is reflected
    assert data["total_reports"] >= 1
    assert data["diseases_by_category"].get("Viral", 0) >= 1
    assert data["most_common_disease"] is not None


def test_statistics_unauthenticated(client):
    response = client.get("/api/statistics")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
