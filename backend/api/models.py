from __future__ import annotations
from datetime import date, datetime
from typing import Optional, List

from sqlalchemy import (
    String,
    Date,
    DateTime,
    ForeignKey,
    JSON,
    func,
    Enum as SqlEnum,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from api.enums import (
    GenderEnum,
    DiseaseCategoryEnum,
    SeverityLevelEnum,
    TreatmentStatusEnum,
    ReportStateEnum,
)


class Base(DeclarativeBase):
    pass


class Reporter(Base):
    __tablename__ = "reporters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # First name (required, max 50 chars).
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Last name (required, max 50 chars).
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Email (required, unique, valid email format).
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # Job title (required, max 100 chars).
    job_title: Mapped[str] = mapped_column(String(100), nullable=False)

    # Phone number (required, format validation).
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)

    # Hospital/Organization name (required, max 200 chars).
    hospital_name: Mapped[str] = mapped_column(String(200), nullable=False)

    # Hospital address (required, max 500 chars).
    hospital_address: Mapped[str] = mapped_column(String(500), nullable=False)

    # Registration date (auto-populated).
    registration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    reports: Mapped[List[Report]] = relationship("Report", back_populates="reporter")


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # First name (required, max 50 chars).
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Last name (required, max 50 chars).
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Date of birth (required, no future dates).
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)

    # Gender (required, enum: Male/Female/Other).
    gender: Mapped[GenderEnum] = mapped_column(SqlEnum(GenderEnum), nullable=False)

    # Medical record number (required, unique per hospital).
    medical_record_number: Mapped[str] = mapped_column(String(100), nullable=False)

    # Patient address (required, max 500 chars).
    patient_address: Mapped[str] = mapped_column(String(500), nullable=False)

    # Emergency contact (optional, max 200 chars).
    emergency_contact: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"), nullable=False)
    report: Mapped[Report] = relationship("Report", back_populates="patient")


class Disease(Base):
    __tablename__ = "diseases"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Disease name (required, max 100 chars).
    disease_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Disease category (required, enum: Bacterial/Viral/Parasitic/Other)
    disease_category: Mapped[DiseaseCategoryEnum] = mapped_column(
        SqlEnum(DiseaseCategoryEnum), nullable=False
    )

    # Date detected (required, cannot be future date, cannot be before patient DOB).
    date_detected: Mapped[date] = mapped_column(Date, nullable=False)

    # Symptoms (required, JSON array or text field).
    symptoms: Mapped[list[str]] = mapped_column(JSON, nullable=False)

    # Severity level (required, enum: Low/Medium/High/Critical).
    severity_level: Mapped[SeverityLevelEnum] = mapped_column(
        SqlEnum(SeverityLevelEnum), nullable=False
    )

    # Lab results (optional, text field).
    lab_results: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    # Treatment status (required, enum: None/Ongoing/Completed).
    treatment_status: Mapped[TreatmentStatusEnum] = mapped_column(
        SqlEnum(TreatmentStatusEnum), nullable=False
    )

    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"), nullable=False)
    report: Mapped[Report] = relationship("Report", back_populates="disease")


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    status: Mapped[ReportStateEnum] = mapped_column(
        SqlEnum(ReportStateEnum), default=ReportStateEnum.draft, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    reporter_id: Mapped[Optional[int]] = mapped_column(ForeignKey("reporters.id"))
    reporter: Mapped[Optional[Reporter]] = relationship(
        "Reporter", back_populates="reports"
    )

    patient: Mapped[Optional[Patient]] = relationship(
        "Patient", uselist=False, back_populates="report"
    )
    disease: Mapped[Optional[Disease]] = relationship(
        "Disease", uselist=False, back_populates="report"
    )
