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
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    job_title: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    hospital_name: Mapped[str] = mapped_column(String(200), nullable=False)
    hospital_address: Mapped[str] = mapped_column(String(500), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    reports: Mapped[List[Report]] = relationship("Report", back_populates="reporter")


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(SqlEnum(GenderEnum), nullable=False)
    medical_record_number: Mapped[str] = mapped_column(String(100), nullable=False)
    patient_address: Mapped[str] = mapped_column(String(500), nullable=False)
    emergency_contact: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"), nullable=False)
    report: Mapped[Report] = relationship("Report", back_populates="patient")


class Disease(Base):
    __tablename__ = "diseases"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    disease_name: Mapped[str] = mapped_column(String(100), nullable=False)
    disease_category: Mapped[DiseaseCategoryEnum] = mapped_column(
        SqlEnum(DiseaseCategoryEnum), nullable=False
    )
    date_detected: Mapped[date] = mapped_column(Date, nullable=False)
    symptoms: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    severity_level: Mapped[SeverityLevelEnum] = mapped_column(
        SqlEnum(SeverityLevelEnum), nullable=False
    )
    lab_results: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
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
