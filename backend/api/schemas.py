from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import date, datetime
import enum


class GenderEnum(str, enum.Enum):
    male = "Male"
    female = "Female"
    other = "Other"


class DiseaseCategoryEnum(str, enum.Enum):
    bacterial = "Bacterial"
    viral = "Viral"
    parasitic = "Parasitic"
    other = "Other"


class SeverityLevelEnum(str, enum.Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    critical = "Critical"


class TreatmentStatusEnum(str, enum.Enum):
    none = "None"
    ongoing = "Ongoing"
    completed = "Completed"


class ReportStateEnum(str, enum.Enum):
    draft = "Draft"
    submitted = "Submitted"
    under_review = "Under Review"
    approved = "Approved"


# Reporter Schemas
class ReporterBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    job_title: str = Field(..., max_length=100)
    phone_number: str
    hospital_name: str = Field(..., max_length=200)
    hospital_address: str = Field(..., max_length=500)


class ReporterCreate(ReporterBase):
    pass


class Reporter(ReporterBase):
    id: int
    registration_date: datetime

    class Config:
        orm_mode = True


# Patient Schemas
class PatientBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    date_of_birth: date
    gender: GenderEnum
    medical_record_number: str
    patient_address: str = Field(..., max_length=500)
    emergency_contact: Optional[str] = Field(None, max_length=200)


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase):
    id: int

    class Config:
        orm_mode = True


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
    pass


class Disease(DiseaseBase):
    id: int

    class Config:
        orm_mode = True


# Report Schemas
class ReportBase(BaseModel):
    status: ReportStateEnum = ReportStateEnum.draft


class ReportCreate(ReportBase):
    pass


class Report(ReportBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    reporter: Optional[Reporter]
    patient: Optional[Patient]
    disease: Optional[Disease]

    class Config:
        orm_mode = True


class StatisticsSummary(BaseModel):
    total_reports: int
    reports_by_status: Dict[str, int]
    diseases_by_category: Dict[str, int]
    diseases_by_severity: Dict[str, int]
    average_patient_age: Optional[float]
    most_common_disease: Optional[str]
