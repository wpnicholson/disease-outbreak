from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import date, datetime, timezone
from api.enums import (
    GenderEnum,
    DiseaseCategoryEnum,
    SeverityLevelEnum,
    TreatmentStatusEnum,
    ReportStateEnum,
    UserRoleEnum,
)


# Reporter Schemas
class ReporterBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    job_title: str = Field(..., max_length=100)
    phone_number: str = Field(..., max_length=20)
    hospital_name: str = Field(..., max_length=200)
    hospital_address: str = Field(..., max_length=500)


class ReporterCreate(ReporterBase):
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Alice",
                "last_name": "Doe",
                "email": "alice.doe@example.com",
                "job_title": "Epidemiologist",
                "phone_number": "+1234567890",
                "hospital_name": "City Hospital",
                "hospital_address": "123 Health St, Metropolis",
            }
        }


class Reporter(ReporterBase):
    id: int
    registration_date: datetime

    model_config = {"from_attributes": True}


class ReportPatientsLink(BaseModel):
    patient_ids: List[int]

    class Config:
        json_schema_extra = {"example": {"patient_ids": [1, 2, 3]}}


# Patient Schemas
class PatientBase(BaseModel):
    """Base model for patient data.

    Sets the `first_name`, `last_name`, `date_of_birth`, `gender`, `medical_record_number`, and `patient_address` fields as required.

    The `emergency_contact` field is optional.

    Args:
        BaseModel (BaseModel): Base model for all Pydantic models.
    """

    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    date_of_birth: date
    gender: GenderEnum
    medical_record_number: str
    patient_address: str = Field(..., max_length=500)
    emergency_contact: Optional[str] = Field(None, max_length=200)


class PatientCreate(PatientBase):
    """Patient creation model.

    Inherits all fields from `PatientBase`.

    Provides an example for JSON schema generation.

    The `emergency_contact` field is optional.

    Args:
        PatientBase (PatientBase): Base model for patient data.
    """

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1990-01-01",
                "gender": GenderEnum.male,
                "medical_record_number": "MRN123456",
                "patient_address": "456 Health Ave, Wellness City",
                "emergency_contact": "Jane Doe, +1234567890",
            }
        }


class Patient(PatientBase):
    """Patient model.

    Inherits all fields from `PatientBase`.

    The `emergency_contact` field is optional.

    Args:
        PatientBase (PatientBase): Base model for patient data.
    """

    id: int

    model_config = {"from_attributes": True}


# Disease Schemas
class DiseaseBase(BaseModel):
    disease_name: str = Field(..., max_length=100)
    disease_category: DiseaseCategoryEnum
    date_detected: date
    symptoms: List[str]
    severity_level: SeverityLevelEnum
    lab_results: Optional[str] = None
    treatment_status: TreatmentStatusEnum


class DiseaseCreate(DiseaseBase):
    class Config:
        json_schema_extra = {
            "example": {
                "disease_name": "Influenza",
                "disease_category": DiseaseCategoryEnum.viral,
                "date_detected": "2023-10-01",
                "symptoms": ["fever", "cough"],
                "severity_level": SeverityLevelEnum.medium,
                "treatment_status": TreatmentStatusEnum.ongoing,
                "report_id": 1,
            }
        }


class Disease(DiseaseBase):
    id: int

    model_config = {"from_attributes": True}


# Report Schemas
class ReportBase(BaseModel):
    """Base model for report data.

    Sets the `status` field to `draft` by default.

    All other fields are defined in class `Report`.

    Args:
        BaseModel (BaseModel): Base model for all Pydantic models.
    """

    status: ReportStateEnum = ReportStateEnum.draft


class ReportCreate(ReportBase):
    """Report creation model.

    To create a new report, this model requires only the `status` field, which defaults to `draft`.

    The `created_at` field will be set automatically to the `Datetime` of creation.

    All other fields are optional and can be set later.

    See endpoint POST `/api/reports/` in function `reports.create_report` for more details on report creation.

    Args:
        ReportBase (ReportBase): Base model for report data.
    """

    class Config:
        json_schema_extra = {
            "example": {
                "status": ReportStateEnum.draft,
                "created_by": 1,
                "reporter_id": 1,
                "disease_id": 1,
                "patients": [1, 2, 3],
            }
        }


class ReportUpdate(BaseModel):
    """Report update model.

    Updating a report can be done piecemeal, and so this model sets all fields as optional.

    The `status` field remains defaulted to `draft`, but can be set to any valid `ReportStateEnum`.
    The `updated_at` field will be set automatically to the current `Datetime` when the report is updated.

    See endpoint PUT `/api/reports/{report_id}` in function `reports.update_report` for more details on report updates.

    Args:
        BaseModel (BaseModel): Base model for all Pydantic models.
    """

    status: Optional[ReportStateEnum] = ReportStateEnum.draft
    reporter_id: Optional[int] = None
    reporter: Optional[Reporter] = None
    disease_id: Optional[int] = None
    disease: Optional[Disease] = None
    patients: Optional[List[Patient]] = None
    updated_at: Optional[datetime] = datetime.now(timezone.utc)

    class Config:
        json_schema_extra = {
            "example": {
                "status": ReportStateEnum.draft,
                "reporter_id": 1,
                "reporter": {
                    "id": 1,
                    "first_name": "Alice",
                    "last_name": "Doe",
                    "email": "reporter@email.com",
                    "job_title": "Epidemiologist",
                    "phone_number": "+1234567890",
                    "hospital_name": "City Hospital",
                    "hospital_address": "123 Health St, Metropolis",
                },
                "disease_id": 2,
                "disease": {
                    "id": 2,
                    "disease_name": "Influenza",
                    "disease_category": DiseaseCategoryEnum.viral,
                    "date_detected": "2023-10-01",
                    "symptoms": ["fever", "cough"],
                    "severity_level": SeverityLevelEnum.medium,
                    "treatment_status": TreatmentStatusEnum.ongoing,
                },
                "patients": [1, 2],
                "updated_at": "2023-10-01T12:00:00Z",
            }
        }


class Report(ReportBase):
    """Report model.

    Inherits field `status` from `ReportBase` and adds fields for the report's ID, creation date,
    and relationships to other models.

    The `status` field defaults to `draft`, and the `created_at` field is set automatically
    to the current `Datetime` when the report is created.

    All other fields are optional and can be set later.

    Args:
        ReportBase (ReportBase): Base model for report data.
    """

    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    reporter: Optional[Reporter]
    patients: List[Patient] = []
    disease: Optional[Disease]

    model_config = {"from_attributes": True}


class StatisticsSummary(BaseModel):
    total_reports: int
    reports_by_status: Dict[str, int]
    diseases_by_category: Dict[str, int]
    diseases_by_severity: Dict[str, int]
    average_patient_age: Optional[float]
    most_common_disease: Optional[str]


class UserBase(BaseModel):
    """Base model for user data.

    Args:
        BaseModel (BaseModel): Pydantic base model for data validation.
    """

    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)


class UserSignup(UserBase):
    """Create model for user data during signup.

    Inherits `email` and `full_name` from UserBase and adds `password` and `role` fields.

    All fields except `role` are needed to signup. The `role` defaults to "junior" if not provided.

    Args:
        UserBase (UserBase): Base model for user data.
    """

    password: str = Field(..., min_length=8, max_length=128)
    role: UserRoleEnum = Field(default=UserRoleEnum.junior)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "bob.smith@example.com",
                "password": "plaintext_password_here",
                "full_name": "Bob Smith",
                "role": UserRoleEnum.junior,
            }
        }


class UserLogin(BaseModel):
    """Login model for user authentication.

    Does not inherit from `UserBase` to avoid requiring `full_name` and `role` at login.

    Args:
        BaseModel (BaseModel): Pydantic base model for data validation.
    """

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "bob.smith@example.com",
                "password": "plaintext_password_here",
            }
        }


# For safe user data exposure.
class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


class AuditLog(BaseModel):
    id: int
    timestamp: datetime
    user_id: Optional[int]
    action: str
    entity_type: str
    entity_id: int
    changes: Optional[dict]

    model_config = {"from_attributes": True}
