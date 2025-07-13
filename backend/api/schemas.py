from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional, List, Dict
from datetime import date, datetime
from api.enums import (
    GenderEnum,
    DiseaseCategoryEnum,
    SeverityLevelEnum,
    TreatmentStatusEnum,
    ReportStateEnum,
)


# Reporter Schemas
class ReporterBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    job_title: str = Field(..., max_length=100)
    phone_number: PhoneNumber
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
