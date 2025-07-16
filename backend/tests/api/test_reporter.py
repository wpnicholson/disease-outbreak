import pytest
from api.models import Reporter, Report


@pytest.fixture(scope="function")
def create_report(db_session, test_user):
    """Creates a draft report for testing."""
    report = Report(status="Draft", created_by=test_user.id)
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)
    yield report
    db_session.delete(report)
    db_session.commit()


@pytest.fixture(scope="function")
def reporter_payload(test_run_id):
    """Generates unique reporter payload."""
    return {
        "first_name": "Alice",
        "last_name": "Doe",
        "email": f"reporter-{test_run_id}@example.com",
        "job_title": "Epidemiologist",
        "phone_number": "+1234567890",
        "hospital_name": "City Hospital",
        "hospital_address": "123 Health St, Metropolis",
    }


def test_add_reporter_success(
    client, auth_headers, create_report, reporter_payload, db_session
):
    """Test adding a reporter to a draft report (new reporter creation)."""
    response = client.post(
        f"/api/reports/{create_report.id}/reporter",
        json=reporter_payload,
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == reporter_payload["email"]

    db_session.expire_all()

    db_report = db_session.query(Report).filter_by(id=create_report.id).first()
    assert db_report.reporter is not None
    assert db_report.reporter.email == reporter_payload["email"]


def test_update_existing_reporter(
    client, auth_headers, create_report, reporter_payload, db_session
):
    """Test updating an existing reporter assigned to a report."""
    reporter = Reporter(**reporter_payload)
    db_session.add(reporter)
    db_session.commit()

    response = client.post(
        f"/api/reports/{create_report.id}/reporter",
        json=reporter_payload,
        headers=auth_headers,
    )
    assert response.status_code == 201

    updated_payload = reporter_payload.copy()
    updated_payload["first_name"] = "UpdatedName"

    response = client.post(
        f"/api/reports/{create_report.id}/reporter",
        json=updated_payload,
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["first_name"] == "UpdatedName"


def test_add_reporter_invalid_report_id(client, auth_headers, reporter_payload):
    """Test adding a reporter to a non-existent report."""
    response = client.post(
        "/api/reports/9999/reporter",
        json=reporter_payload,
        headers=auth_headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Report not found"


def test_add_reporter_non_draft_report(
    client, auth_headers, db_session, test_user, reporter_payload
):
    """Test adding reporter fails if report is not draft."""
    # Create submitted report
    report = Report(status="Submitted", created_by=test_user.id)
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    response = client.post(
        f"/api/reports/{report.id}/reporter",
        json=reporter_payload,
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert "draft" in response.json()["detail"].lower()

    db_session.delete(report)
    db_session.commit()


def test_get_reporter_success(
    client, auth_headers, create_report, reporter_payload, db_session
):
    """Test retrieving reporter attached to a report."""
    reporter = Reporter(**reporter_payload)
    db_session.add(reporter)
    db_session.commit()
    create_report.reporter = reporter
    db_session.commit()

    response = client.get(
        f"/api/reports/{create_report.id}/reporter", headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["email"] == reporter_payload["email"]


def test_get_reporter_not_found(client, auth_headers, create_report):
    """Test GET reporter returns 404 when no reporter is associated."""
    response = client.get(
        f"/api/reports/{create_report.id}/reporter", headers=auth_headers
    )
    assert response.status_code == 404
    assert "Reporter not associated" in response.json()["detail"]


def test_get_reporter_invalid_report(client, auth_headers):
    """Test GET reporter with invalid report ID."""
    response = client.get("/api/reports/9999/reporter", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Report not found"
