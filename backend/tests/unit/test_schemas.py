from pydantic import ValidationError
from api.schemas import ReporterCreate
import pytest


def test_reporter_invalid_email():
    with pytest.raises(ValidationError):
        ReporterCreate(
            first_name="A",
            last_name="B",
            email="invalid",
            job_title="Doctor",
            phone_number="+14155552671",  # type: ignore
            hospital_name="Test",
            hospital_address="Addr",
        )
