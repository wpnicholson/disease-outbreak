import pytest
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import Reporter, Patient, Disease, Report
from api.sample_data import create_sample_data


@pytest.fixture(scope="module")
def db():
    """Provides a session scoped to the module, respects global DB setup."""
    session = SessionLocal()
    yield session
    session.close()


def test_sample_data_seeding(db: Session, test_user: int):
    """Test sample data seeding on already prepared test DB."""
    create_sample_data(db, test_user)
    report_count = db.query(Report).count()

    assert db.query(Reporter).count() == 3
    assert db.query(Report).count() == 3
    assert db.query(Patient).count() == report_count
    assert db.query(Disease).count() == 3

    reports = db.query(Report).all()
    for report in reports:
        assert report.reporter is not None
        assert report.patient is not None
        assert report.disease is not None
