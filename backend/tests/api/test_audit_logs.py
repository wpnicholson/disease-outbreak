import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone
from api.main import app
from api.models import AuditLog
from api.database import SessionLocal

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_audit_log_test_data():
    db = SessionLocal()

    # Create 5 audit log entries with incremental timestamps
    now = datetime.now(timezone.utc)
    for i in range(5):
        log = AuditLog(
            timestamp=now - timedelta(days=i),
            user_id=None,
            action="TEST_ACTION",
            entity_type="TestEntity",
            entity_id=i + 1,
            changes={"field": f"change_{i}"},
        )
        db.add(log)

    db.commit()
    db.close()
    yield


def test_get_audit_logs_basic():
    response = client.get("/api/audit-logs/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 5
    assert data[0]["action"] == "TEST_ACTION"


def test_get_audit_logs_with_date_filter():
    now = datetime.now(timezone.utc).replace(microsecond=0)
    future_time = (now + timedelta(seconds=1)).isoformat()

    # Future filter should return zero logs
    response = client.get(
        "/api/audit-logs/", params={"start_date": future_time, "limit": 10}
    )
    assert response.status_code == 200, response.text
    assert len(response.json()) == 0

    # Within range filter should return at least one
    two_days_ago = (now - timedelta(days=2)).isoformat()
    response = client.get("/api/audit-logs/", params={"start_date": two_days_ago})
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) >= 1


def test_get_audit_logs_with_pagination():
    response = client.get("/api/audit-logs/", params={"skip": 0, "limit": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Next page
    response_next = client.get("/api/audit-logs/", params={"skip": 0, "limit": 2})
    assert response_next.status_code == 200
    assert len(response_next.json()) == 2
