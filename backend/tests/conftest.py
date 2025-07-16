import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from api.main import app
from api.database import SessionLocal
from api.models import User, Report, Reporter, Patient, Disease, AuditLog
from api.enums import UserRoleEnum
from api.endpoints.auth import hash_password
import uuid


@pytest.fixture(scope="function")
def client():
    """FastAPI test client."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def test_run_id():
    """Unique identifier for test data isolation."""
    return str(uuid.uuid4())


@pytest.fixture(scope="function")
def db_session():
    """Provides a database session for each test function."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_user(db_session: Session, test_run_id: str):
    """Creates a test user with cleanup after test."""
    email = f"testuser-{test_run_id}@example.com"
    user = User(
        email=email,
        hashed_password=hash_password("strongpassword"),
        full_name="Test User",
        role=UserRoleEnum.senior,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    yield user

    # Cleanup cascade deletions for isolation
    db_session.query(Report).filter(Report.created_by == user.id).delete()
    db_session.query(Reporter).filter(Reporter.email.like(f"%{test_run_id}%")).delete()
    db_session.query(Patient).filter(
        Patient.medical_record_number.like(f"%{test_run_id}%")
    ).delete()
    db_session.query(Disease).delete()
    db_session.query(AuditLog).filter(AuditLog.user_id == user.id).delete()
    db_session.query(User).filter(User.id == user.id).delete()
    db_session.commit()


@pytest.fixture(scope="function")
def signup_payload(test_run_id):
    return {
        "email": f"pytest-user-{test_run_id}@example.com",
        "password": "pytestpassword",
        "full_name": "Pytest User",
        "role": "Senior",
    }


@pytest.fixture(scope="function")
def auth_headers(client, db_session, signup_payload, test_run_id):
    client.post("/api/auth/signup", json=signup_payload)
    response = client.post(
        "/api/auth/login",
        json={"email": signup_payload["email"], "password": signup_payload["password"]},
    )
    token = response.json()["access_token"]

    yield {"Authorization": f"Bearer {token}"}

    # Cleanup block after test finishes
    from api.models import User, AuditLog, Report

    # Cleanup user
    user = db_session.query(User).filter(User.email == signup_payload["email"]).first()
    if user:
        db_session.query(Report).filter(Report.created_by == user.id).delete()
        db_session.query(AuditLog).filter(AuditLog.user_id == user.id).delete()
        db_session.delete(user)
        db_session.commit()
