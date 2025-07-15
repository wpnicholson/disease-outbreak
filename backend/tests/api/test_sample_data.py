import pytest
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import Reporter, Patient, Disease, Report
from api.sample_data import create_sample_data


@pytest.fixture(scope="function")
def db():
    """Provides a session scoped to the function."""
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def test_user(client):
    """Create a persistent user without teardown (for sample data)."""
    from api.enums import UserRoleEnum

    email = "sample-data-user@example.com"
    resp = client.post(
        "/api/auth/signup",
        json={
            "email": email,
            "password": "strongpassword",
            "full_name": "Sample Data User",
            "role": UserRoleEnum.senior.value,
        },
    )
    assert resp.status_code == 201
    user_id = resp.json()["id"]
    return user_id


def test_sample_data_seeding(db: Session, test_user: int):
    create_sample_data(db, test_user)
    report_count = db.query(Report).count()

    assert db.query(Reporter).count() == 5
    assert db.query(Report).count() == 15
    assert db.query(Patient).count() == report_count
    assert db.query(Disease).count() == 15
