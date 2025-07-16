import pytest
from api.models import Report
from api.enums import ReportStateEnum


@pytest.fixture(scope="function")
def report_payload():
    """Payload to create a report (status draft)."""
    return {"status": ReportStateEnum.draft}


def test_create_report_success(
    client, auth_headers, db_session, test_user, report_payload
):
    """Test successful creation of a report."""
    response = client.post("/api/reports/", json=report_payload, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "Draft"
    assert data["reporter"] is None
    assert data["patients"] == []
    assert data["disease"] is None

    # Cleanup
    db_session.query(Report).filter(Report.id == data["id"]).delete()
    db_session.commit()


def test_list_reports(client, auth_headers, db_session, test_user):
    """Test listing reports with pagination."""
    report = Report(status=ReportStateEnum.draft, created_by=test_user.id)
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    response = client.get("/api/reports/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert any(r["id"] == report.id for r in data)

    # Cleanup
    db_session.query(Report).filter(Report.id == report.id).delete()
    db_session.commit()


def test_get_report_success(client, auth_headers, db_session, test_user):
    """Test retrieving a report by ID."""
    report = Report(status=ReportStateEnum.draft, created_by=test_user.id)
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    response = client.get(f"/api/reports/{report.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == report.id

    db_session.query(Report).filter(Report.id == report.id).delete()
    db_session.commit()


def test_get_report_not_found(client, auth_headers):
    """Test retrieving a non-existent report returns 404."""
    response = client.get("/api/reports/999999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Report not found"


def test_update_report_success(client, auth_headers, db_session, test_user):
    """Test updating a draft report's status."""
    report = Report(status=ReportStateEnum.draft, created_by=test_user.id)
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    payload = {"status": ReportStateEnum.submitted}
    response = client.put(
        f"/api/reports/{report.id}", json=payload, headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Submitted"

    # Cleanup
    db_session.query(Report).filter(Report.id == report.id).delete()
    db_session.commit()


def test_update_report_not_found(client, auth_headers):
    """Test updating a non-existent report returns 404."""
    payload = {"status": ReportStateEnum.submitted}
    response = client.put("/api/reports/999999", json=payload, headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Report not found"


def test_update_report_not_draft(client, auth_headers, db_session, test_user):
    """Test updating a non-draft report returns 400."""
    report = Report(status=ReportStateEnum.submitted, created_by=test_user.id)
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    payload = {"status": ReportStateEnum.approved}
    response = client.put(
        f"/api/reports/{report.id}", json=payload, headers=auth_headers
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Only draft reports can be edited"

    db_session.query(Report).filter(Report.id == report.id).delete()
    db_session.commit()


def test_delete_report_success(client, auth_headers, db_session, test_user):
    """Test successful deletion of a draft report."""
    report = Report(status=ReportStateEnum.draft, created_by=test_user.id)
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    response = client.delete(f"/api/reports/{report.id}", headers=auth_headers)
    assert response.status_code == 204

    exists = db_session.query(Report).filter(Report.id == report.id).first()
    assert exists is None


def test_delete_report_not_found(client, auth_headers):
    """Test deleting a non-existent report returns 404."""
    response = client.delete("/api/reports/999999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Report not found"


def test_delete_report_not_draft(client, auth_headers, db_session, test_user):
    """Test deleting a non-draft report returns 400."""
    report = Report(status=ReportStateEnum.submitted, created_by=test_user.id)
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    response = client.delete(f"/api/reports/{report.id}", headers=auth_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Only draft reports can be deleted"

    db_session.query(Report).filter(Report.id == report.id).delete()
    db_session.commit()
