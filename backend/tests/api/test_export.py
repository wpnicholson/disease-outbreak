# tests/api/test_export.py

import pytest


@pytest.fixture(scope="function")
def report_payload(test_run_id):
    return {"status": "draft"}


def test_export_json_success(client, auth_headers, db_session):
    """Test exporting reports in JSON format."""
    response = client.get("/api/reports/export/json", headers=auth_headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, list)


def test_export_csv_success(client, auth_headers, db_session):
    """Test exporting reports in CSV format."""
    response = client.get("/api/reports/export/csv", headers=auth_headers)
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "attachment; filename=reports.csv" in response.headers["content-disposition"]
    content = response.content.decode()
    assert "report_id" in content
    assert "status" in content


def test_export_invalid_format(client, auth_headers):
    """Test export endpoint with invalid format returns 400."""
    response = client.get("/api/reports/export/xml", headers=auth_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Format must be 'json' or 'csv'"


def test_export_unauthenticated(client):
    """Test unauthenticated export request fails."""
    response = client.get("/api/reports/export/json")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
