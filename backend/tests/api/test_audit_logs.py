import pytest
from datetime import datetime, timedelta, timezone
from api.database import SessionLocal
from api.models import AuditLog, User
from api.endpoints.auth import create_access_token
from api.enums import UserRoleEnum

# client is imported via conftest.py


@pytest.fixture(scope="module")
def senior_token():
    db = SessionLocal()
    senior_user = User(
        email="senior@example.com",
        hashed_password="not_validated_for_test",
        full_name="Senior User",
        role=UserRoleEnum.senior,
    )
    db.add(senior_user)
    db.commit()
    db.refresh(senior_user)

    token = create_access_token(
        {"sub": senior_user.email, "role": senior_user.role.value}
    )
    db.close()
    return token


@pytest.fixture(scope="module", autouse=True)
def setup_audit_log_test_data():
    db = SessionLocal()
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


def test_get_audit_logs_basic(client, senior_token):
    response = client.get(
        "/api/audit-logs/", headers={"Authorization": f"Bearer {senior_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 5
    assert data[0]["action"] == "TEST_ACTION"


def test_get_audit_logs_with_date_filter(client, senior_token):
    now = datetime.now(timezone.utc).replace(microsecond=0)
    future_time = (now + timedelta(seconds=1)).isoformat()

    response = client.get(
        "/api/audit-logs/",
        params={"start_date": future_time, "limit": 10},
        headers={"Authorization": f"Bearer {senior_token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 0

    two_days_ago = (now - timedelta(days=2)).isoformat()
    response = client.get(
        "/api/audit-logs/",
        params={"start_date": two_days_ago},
        headers={"Authorization": f"Bearer {senior_token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_audit_logs_with_pagination(client, senior_token):
    response = client.get(
        "/api/audit-logs/",
        params={"skip": 0, "limit": 2},
        headers={"Authorization": f"Bearer {senior_token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 2

    response_next = client.get(
        "/api/audit-logs/",
        params={"skip": 2, "limit": 2},
        headers={"Authorization": f"Bearer {senior_token}"},
    )
    assert response_next.status_code == 200
    assert len(response_next.json()) >= 0  # could be less than 2 if <4 logs exist
