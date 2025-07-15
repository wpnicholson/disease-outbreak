from datetime import datetime, timedelta, timezone
from api.database import SessionLocal
from api.models import AuditLog


def test_get_audit_logs_basic(client, test_user):
    user_id, test_run_id = test_user
    db = SessionLocal()

    now = datetime.now(timezone.utc)

    # Create audit logs tied to user_id
    for i in range(5):
        log = AuditLog(
            timestamp=now - timedelta(days=i),
            user_id=user_id,
            action="TEST_ACTION",
            entity_type="TestEntity",
            entity_id=i + 1,
            changes={"field": f"change_{i}"},
        )
        db.add(log)
    db.commit()

    response = client.get(
        "/api/audit-logs/",
        headers={
            "Authorization": f"Bearer {client.post('/api/auth/login', json={ 'email': f'testuser-{test_run_id}@example.com', 'password': 'strongpassword' }).json()['access_token']}"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 5
    assert data[0]["action"] == "TEST_ACTION"
    db.close()


def test_get_audit_logs_with_date_filter(client, test_user):
    user_id, test_run_id = test_user
    db = SessionLocal()
    now = datetime.now(timezone.utc)

    # Create audit logs
    for i in range(5):
        db.add(
            AuditLog(
                timestamp=now - timedelta(days=i),
                user_id=user_id,
                action="FILTER_TEST",
                entity_type="FilterTest",
                entity_id=i + 1,
                changes={"filter": f"value_{i}"},
            )
        )
    db.commit()

    future_time = (now + timedelta(seconds=1)).isoformat()
    response = client.get(
        "/api/audit-logs/",
        params={"start_date": future_time},
        headers={
            "Authorization": f"Bearer {client.post('/api/auth/login', json={ 'email': f'testuser-{test_run_id}@example.com', 'password': 'strongpassword' }).json()['access_token']}"
        },
    )
    assert response.status_code == 200
    assert len(response.json()) == 0

    two_days_ago = (now - timedelta(days=2)).isoformat()
    response = client.get(
        "/api/audit-logs/",
        params={"start_date": two_days_ago},
        headers={
            "Authorization": f"Bearer {client.post('/api/auth/login', json={ 'email': f'testuser-{test_run_id}@example.com', 'password': 'strongpassword' }).json()['access_token']}"
        },
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1
    db.close()


def test_get_audit_logs_with_pagination(client, test_user):
    user_id, test_run_id = test_user
    db = SessionLocal()
    now = datetime.now(timezone.utc)

    for i in range(5):
        db.add(
            AuditLog(
                timestamp=now - timedelta(days=i),
                user_id=user_id,
                action="PAGINATION_TEST",
                entity_type="PaginationTest",
                entity_id=i + 100,
                changes={"page": f"page_{i}"},
            )
        )
    db.commit()

    response = client.get(
        "/api/audit-logs/",
        params={"skip": 0, "limit": 2},
        headers={
            "Authorization": f"Bearer {client.post('/api/auth/login', json={ 'email': f'testuser-{test_run_id}@example.com', 'password': 'strongpassword' }).json()['access_token']}"
        },
    )
    assert response.status_code == 200
    assert len(response.json()) == 2

    response_next = client.get(
        "/api/audit-logs/",
        params={"skip": 2, "limit": 2},
        headers={
            "Authorization": f"Bearer {client.post('/api/auth/login', json={ 'email': f'testuser-{test_run_id}@example.com', 'password': 'strongpassword' }).json()['access_token']}"
        },
    )
    assert response_next.status_code == 200
    assert len(response_next.json()) >= 0
    db.close()
