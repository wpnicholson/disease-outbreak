"""
Statistics Endpoint

This module provides an API endpoint to fetch basic statistical summaries from the
Disease Outbreak Reporting System. It includes counts of reports, disease breakdowns,
patient age averages, and most common diseases.

Accessible only to authenticated users.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from api import models, schemas
from api.dependencies import get_db, get_current_user

router = APIRouter()


@router.get(
    "/statistics",
    response_model=schemas.StatisticsSummary,
    summary="Get basic statistics summary",
    description="Returns statistical summaries such as total reports, reports by status, diseases by category, most common disease, and average patient age.",
    response_description="Basic statistics summary.",
)
def get_statistics(
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    """
    Retrieve aggregated statistics from the system.

    Statistics include:
    - Total number of reports.
    - Number of reports by status.
    - Number of diseases by category and severity.
    - Most common disease by report count.
    - Average patient age across all patients.

    Args:
        db (Session): SQLAlchemy database session.
        _: models.User: Authenticated user making the request (validated but unused).

    Returns:
        schemas.StatisticsSummary: Statistical summary response.
    """
    total_reports = db.query(func.count(models.Report.id)).scalar()

    # Reports by status
    reports_by_status = {
        status.value: db.query(func.count(models.Report.id))
        .filter(models.Report.status == status)
        .scalar()
        for status in models.ReportStateEnum
    }

    # Diseases by category
    diseases_by_category = {
        category.value: db.query(func.count(models.Disease.id))
        .filter(models.Disease.disease_category == category)
        .scalar()
        for category in models.DiseaseCategoryEnum
    }

    # Diseases by severity
    diseases_by_severity = {
        severity.value: db.query(func.count(models.Disease.id))
        .filter(models.Disease.severity_level == severity)
        .scalar()
        for severity in models.SeverityLevelEnum
    }

    # Most common disease by name (if any)
    most_common_disease = (
        db.query(
            models.Disease.disease_name, func.count(models.Disease.id).label("count")
        )
        .group_by(models.Disease.disease_name)
        .order_by(func.count(models.Disease.id).desc())
        .limit(1)
        .first()
    )
    most_common_disease_name = most_common_disease[0] if most_common_disease else None

    # Average patient age calculation
    today = date.today()
    ages_query = db.query(
        func.avg(func.date_part("year", func.age(today, models.Patient.date_of_birth)))
    ).scalar()

    average_patient_age = round(ages_query, 2) if ages_query is not None else None

    return schemas.StatisticsSummary(
        total_reports=total_reports,
        reports_by_status=reports_by_status,
        diseases_by_category=diseases_by_category,
        diseases_by_severity=diseases_by_severity,
        average_patient_age=average_patient_age,
        most_common_disease=most_common_disease_name,
    )
