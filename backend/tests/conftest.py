import pytest


@pytest.fixture(scope="function")
def test_run_id():
    import uuid

    return str(uuid.uuid4())


@pytest.fixture(scope="function")
def client():
    from api.main import app
    from fastapi.testclient import TestClient

    return TestClient(app)


@pytest.fixture(scope="function")
def test_user(client, test_run_id):
    from api.enums import UserRoleEnum

    email = f"testuser-{test_run_id}@example.com"
    resp = client.post(
        "/api/auth/signup",
        json={
            "email": email,
            "password": "strongpassword",
            "full_name": "Test User",
            "role": UserRoleEnum.senior.value,
        },
    )
    assert resp.status_code == 201
    user_id = resp.json()["id"]
    yield user_id, test_run_id

    # Cleanup at end of test
    from api.database import SessionLocal
    from api.models import User, Report, Reporter, Patient, Disease, AuditLog

    db = SessionLocal()

    try:
        db.query(Report).filter(Report.created_by == user_id).delete(
            synchronize_session=False
        )
        db.query(Reporter).filter(Reporter.email.like(f"%{test_run_id}%")).delete(
            synchronize_session=False
        )
        db.query(Patient).filter(
            Patient.medical_record_number.like(f"%{test_run_id}%")
        ).delete(synchronize_session=False)
        db.query(Disease).filter(Disease.disease_name.like(f"%{test_run_id}%")).delete(
            synchronize_session=False
        )
        db.query(AuditLog).filter(
            (AuditLog.user_id == user_id) | (AuditLog.entity_id == user_id)
        ).delete(synchronize_session=False)
        db.query(User).filter(User.id == user_id).delete(synchronize_session=False)

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[Teardown Error] {e}")
    finally:
        db.close()
