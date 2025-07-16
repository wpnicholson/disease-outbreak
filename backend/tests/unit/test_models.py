import pytest
from api.models import Reporter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database import Base


@pytest.fixture(scope="module")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def test_reporter_unique_email(session):
    reporter = Reporter(
        first_name="A",
        last_name="B",
        email="unique@example.com",
        job_title="Doc",
        phone_number="+1111111",
        hospital_name="Test",
        hospital_address="Addr",
    )
    session.add(reporter)
    session.commit()

    duplicate = Reporter(
        first_name="X",
        last_name="Y",
        email="unique@example.com",
        job_title="Nurse",
        phone_number="+2222222",
        hospital_name="Another",
        hospital_address="Other",
    )
    with pytest.raises(Exception):
        session.add(duplicate)
        session.commit()
