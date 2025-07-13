from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base


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


class Reporter(Base):
    __tablename__ = "reporters"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    job_title = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    hospital_name = Column(String(200), nullable=False)
    hospital_address = Column(String(500), nullable=False)
    registration_date = Column(DateTime(timezone=True), server_default=func.now())

    reports = relationship("Report", back_populates="reporter")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    medical_record_number = Column(String(100), nullable=False)
    patient_address = Column(String(500), nullable=False)
    emergency_contact = Column(String(200), nullable=True)

    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    report = relationship("Report", back_populates="patient")


class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    disease_name = Column(String(100), nullable=False)
    disease_category = Column(Enum(DiseaseCategoryEnum), nullable=False)
    date_detected = Column(Date, nullable=False)
    symptoms = Column(JSON, nullable=False)
    severity_level = Column(Enum(SeverityLevelEnum), nullable=False)
    lab_results = Column(String(1000), nullable=True)
    treatment_status = Column(Enum(TreatmentStatusEnum), nullable=False)

    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    report = relationship("Report", back_populates="disease")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(
        Enum(ReportStateEnum), default=ReportStateEnum.draft, nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    reporter_id = Column(Integer, ForeignKey("reporters.id"), nullable=True)
    reporter = relationship("Reporter", back_populates="reports")

    patient = relationship("Patient", uselist=False, back_populates="report")
    disease = relationship("Disease", uselist=False, back_populates="report")
