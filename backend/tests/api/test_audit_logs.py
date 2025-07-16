# tests/api/test_audit_logs.py

import pytest
from datetime import datetime, timedelta, timezone
import urllib.parse
from api.models import AuditLog


@pytest.fixture(scope="function")
def seeded_audit_logs(db_session, test_user):
    """Create audit logs for testing and ensure cleanup after test."""
    now = datetime.now(timezone.utc)
    logs = []
    for i in range(5):
        log = AuditLog(
            user_id=test_user.id,
            action="TEST_ACTION",
            entity_type="TestEntity",
            entity_id=i,
            changes={"field": f"value-{i}"},
            timestamp=now - timedelta(days=i),
        )
        db_session.add(log)
        logs.append(log)

    db_session.commit()
    yield logs

    # Cleanup
    db_session.query(AuditLog).filter(AuditLog.user_id == test_user.id).delete()
    db_session.commit()


def test_get_audit_logs_success(client, auth_headers, seeded_audit_logs):
    response = client.get("/api/audit-logs/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5  # At least 5 logs created
    assert all("id" in log for log in data)


def test_audit_logs_pagination(client, auth_headers, seeded_audit_logs):
    response = client.get("/api/audit-logs/?skip=0&limit=2", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_audit_logs_filter_start_date(client, auth_headers, seeded_audit_logs):
    now = datetime.now(timezone.utc)
    start_date = (now - timedelta(days=2)).isoformat()
    start_date_encoded = urllib.parse.quote(start_date)

    response = client.get(
        f"/api/audit-logs/?start_date={start_date_encoded}", headers=auth_headers
    )
    assert response.status_code == 200

    data = response.json()
    for log in data:
        timestamp = datetime.fromisoformat(log["timestamp"].replace("Z", "+00:00"))
        assert timestamp >= datetime.fromisoformat(start_date)


def test_audit_logs_filter_end_date(client, auth_headers, seeded_audit_logs):
    now = datetime.now(timezone.utc)
    end_date = (now - timedelta(days=3)).isoformat()
    end_date_encoded = urllib.parse.quote(end_date)

    response = client.get(
        f"/api/audit-logs/?end_date={end_date_encoded}", headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()
    for log in data:
        timestamp = datetime.fromisoformat(log["timestamp"].replace("Z", "+00:00"))
        assert timestamp <= datetime.fromisoformat(end_date)


def test_audit_logs_filter_start_and_end_date(client, auth_headers, seeded_audit_logs):
    now = datetime.now(timezone.utc)
    start_date = (now - timedelta(days=4)).isoformat()
    end_date = (now - timedelta(days=1)).isoformat()

    start_date_encoded = urllib.parse.quote(start_date)
    end_date_encoded = urllib.parse.quote(end_date)

    response = client.get(
        f"/api/audit-logs/?start_date={start_date_encoded}&end_date={end_date_encoded}",
        headers=auth_headers,
    )
    assert response.status_code == 200

    data = response.json()
    for log in data:
        timestamp = datetime.fromisoformat(log["timestamp"])
        assert (
            datetime.fromisoformat(start_date)
            <= timestamp
            <= datetime.fromisoformat(end_date)
        )


def test_audit_logs_requires_auth(client):
    response = client.get("/api/audit-logs/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
