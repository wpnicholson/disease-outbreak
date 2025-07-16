# tests/api/test_search.py

import pytest
from api.models import Report, Disease, Reporter
from api.enums import (
    ReportStateEnum,
    DiseaseCategoryEnum,
    SeverityLevelEnum,
    TreatmentStatusEnum,
)


@pytest.fixture(scope="function")
def seeded_reports(db_session, test_user, test_run_id):
    """Creates test reports with varying status, disease name, and hospital name."""
    reports = []

    # Create reporters with different hospital names
    reporter_a = Reporter(
        first_name="Alice",
        last_name="Smith",
        email=f"reporter-a-{test_run_id}@example.com",
        job_title="Doctor",
        phone_number="+123456789",
        hospital_name=f"Hospital A {test_run_id}",
        hospital_address="123 Main Street",
    )

    reporter_b = Reporter(
        first_name="Bob",
        last_name="Jones",
        email=f"reporter-b-{test_run_id}@example.com",
        job_title="Doctor",
        phone_number="+987654321",
        hospital_name=f"Hospital B {test_run_id}",
        hospital_address="456 Elm Street",
    )

    db_session.add_all([reporter_a, reporter_b])
    db_session.commit()

    # Create reports linked to reporters
    for idx, status in enumerate(
        [ReportStateEnum.draft, ReportStateEnum.submitted, ReportStateEnum.approved]
    ):
        report = Report(
            status=status,
            created_by=test_user.id,
            reporter=reporter_a if idx % 2 == 0 else reporter_b,
        )
        db_session.add(report)
        db_session.commit()
        db_session.refresh(report)

        # Assign disease
        disease = Disease(
            disease_name=f"Disease {idx} {test_run_id}",
            disease_category=DiseaseCategoryEnum.viral,
            date_detected="2024-01-01",
            symptoms=["cough"],
            severity_level=SeverityLevelEnum.medium,
            treatment_status=TreatmentStatusEnum.ongoing,
            report_id=report.id,
        )
        db_session.add(disease)
        report.disease = disease
        db_session.commit()
        db_session.refresh(report)

        reports.append(report)

    yield reports

    # Cleanup all created data
    db_session.query(Disease).delete()
    db_session.query(Report).delete()
    db_session.query(Reporter).filter(Reporter.email.like(f"%{test_run_id}%")).delete()
    db_session.commit()


def test_search_by_status(client, auth_headers, seeded_reports):
    target_status = seeded_reports[0].status.value

    response = client.get(
        f"/api/reports/search?status={target_status}", headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert all(r["status"] == target_status for r in data)


def test_search_by_disease_name(client, auth_headers, seeded_reports, test_run_id):
    disease_name = seeded_reports[0].disease.disease_name.split()[0]

    response = client.get(
        f"/api/reports/search?disease_name={disease_name}", headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert any(disease_name in r["disease"]["disease_name"] for r in data)


def test_search_by_hospital_name(client, auth_headers, seeded_reports, test_run_id):
    hospital_name = "Hospital A"

    response = client.get(
        f"/api/reports/search?hospital_name={hospital_name}", headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert all(hospital_name in r["reporter"]["hospital_name"] for r in data)


def test_search_pagination(client, auth_headers, seeded_reports):
    response = client.get("/api/reports/search?skip=0&limit=2", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 2  # At most 2 results returned


def test_search_without_filters(client, auth_headers, seeded_reports):
    response = client.get("/api/reports/search", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(seeded_reports)


def test_search_invalid_auth(client):
    response = client.get("/api/reports/search")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
