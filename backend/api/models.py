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
    Table,
    Column,
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
    UserRoleEnum,
)


class Base(DeclarativeBase):
    pass


# Association table for many-to-many Patient <-> Report relationship
patient_reports = Table(
    "patient_reports",
    Base.metadata,
    Column(
        "patient_id", ForeignKey("patients.id", ondelete="CASCADE"), primary_key=True
    ),
    Column("report_id", ForeignKey("reports.id", ondelete="CASCADE"), primary_key=True),
)


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

    # Enables ORM-level access to all Report instances associated with this Reporter (one-to-many relationship).
    # So basically a Reporter instance can load all their Reports via `reporter.reports`.
    # Deleting a Reporter triggers a database-level cascade (`ondelete="CASCADE"`), which deletes all their associated Report instances.
    # This relationship also uses ORM-level cascading (`cascade="all, delete-orphan"`), which means that removing a Report
    # from `reporter.reports` will mark it for deletion from the database.
    # The cascade is unidirectional: so deleting a Report does not affect the Reporter (no upstream cascade).
    reports: Mapped[List[Report]] = relationship(
        "Report",
        back_populates="reporter",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


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

    # Enables ORM-level access to the associated Report instance.
    # Setting `patient.report = X` will automatically update `X.patient` via bidirectional relationship synchronization.
    reports: Mapped[List[Report]] = relationship(
        "Report",
        secondary=patient_reports,
        back_populates="patients",
    )


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

    # The `report_id` foreign key establishes a required link from Disease to a single Report instance (one-to-one relationship).
    # Deleting a Report triggers a database-level cascade (`ondelete="CASCADE"`), which deletes the associated Disease.
    # You cannot delete a Disease independently at the database level because `report_id` is `nullable=False` and enforced by the schema.
    # To delete a Disease, you must either:
    #   - remove the association via `report.disease = None` (triggers ORM-level delete-orphan), or
    #   - delete the associated Report, which will cascade-delete the Disease.
    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id", ondelete="CASCADE"), nullable=False
    )

    # Enables ORM-level access to the associated Report instance.
    # Setting `disease.report = X` will automatically update `X.disease` via bidirectional relationship synchronization.
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
    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    creator: Mapped[User] = relationship("User", back_populates="reports")

    # The `reporter_id` foreign key establishes an (optional) link from Report to a single Reporter instance.
    # Deleting a Reporter triggers a database-level cascade (`ondelete="CASCADE"`), deleting all their associated Reports.
    # The reverse is not true: deleting a Report has no effect on the Reporter; the Reporter remains in the database.
    reporter_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("reporters.id", ondelete="CASCADE")
    )

    # Enables ORM-level access to the associated Reporter instance.
    # Setting `report.reporter = X` will automatically update `X.reports` via bidirectional relationship synchronization.
    reporter: Mapped[Optional[Reporter]] = relationship(
        "Reporter", back_populates="reports"
    )

    # Deleting a Report will also delete all associated Patient instances (ORM cascade delete from Report downstream to Patients).
    # You cannot delete a Patient independently at the database level because `report_id` is `nullable=False`.
    # To remove a Patient, either:
    #   - delete the Patient instance explicitly via the ORM session, or
    #   - delete the associated Report to cascade-delete all its Patients.
    patient: Mapped[List[Patient]] = relationship(
        "Patient",
        secondary=patient_reports,
        back_populates="reports",
    )

    # Each Report is associated with exactly one Disease instance (One-to-One relationship, enforced via `uselist=False`).
    # Deleting a Report will also delete the associated Disease (ORM cascade delete from Report downstream to Disease).
    # The `single_parent=True` setting ensures a Disease instance can only be attached to one Report at a time,
    # preventing accidental sharing across multiple Reports.
    # You cannot delete a Disease independently via the database because `report_id` is `nullable=False`;
    # you must either:
    #   - remove the association via `report.disease = None` (triggers delete-orphan), or
    #   - delete the Report to cascade-delete the Disease.
    disease: Mapped[Optional[Disease]] = relationship(
        "Disease",
        uselist=False,  # Ordinarily would be Many-to-One, but here we enforce One-to-One.
        back_populates="report",
        cascade="all, delete-orphan",
        single_parent=True,
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    role: Mapped[UserRoleEnum] = mapped_column(
        SqlEnum(UserRoleEnum), nullable=False, default=UserRoleEnum.junior
    )

    # Relationship to the Report created by this user.
    reports: Mapped[List["Report"]] = relationship(
        "Report",
        back_populates="creator",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    user: Mapped[Optional[User]] = relationship("User")

    action: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # e.g., CREATE, UPDATE, DELETE
    entity_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # e.g., Report, Patient
    entity_id: Mapped[int] = mapped_column(nullable=False)  # ID of the entity affected

    changes: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    def __repr__(self):
        return f"<AuditLog(action={self.action}, entity={self.entity_type}, id={self.entity_id})>"
