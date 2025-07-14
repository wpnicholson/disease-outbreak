from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from api import models, schemas
from api.dependencies import get_db

router = APIRouter()


@router.get(
    "/statistics",
    response_model=schemas.StatisticsSummary,
    summary="Get aggregate disease report statistics",
    description="Returns counts of reports by status, disease category, severity, average patient age, and most common disease.",
    response_description="Statistics summary of reports in the system.",
)
def get_statistics(db: Session = Depends(get_db)):
    total_reports = db.query(func.count(models.Report.id)).scalar()

    status_counts = dict(
        db.query(models.Report.status, func.count(models.Report.id))
        .group_by(models.Report.status)
        .all()
    )

    category_counts = dict(
        db.query(models.Disease.disease_category, func.count(models.Disease.id))
        .group_by(models.Disease.disease_category)
        .all()
    )

    severity_counts = dict(
        db.query(models.Disease.severity_level, func.count(models.Disease.id))
        .group_by(models.Disease.severity_level)
        .all()
    )

    today = date.today()
    patient_ages = db.query(models.Patient.date_of_birth).all()
    age_values = [
        today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        for (dob,) in patient_ages
    ]
    average_age = round(sum(age_values) / len(age_values), 1) if age_values else None

    most_common_disease = (
        db.query(models.Disease.disease_name, func.count(models.Disease.id))
        .group_by(models.Disease.disease_name)
        .order_by(func.count(models.Disease.id).desc())
        .first()
    )

    return schemas.StatisticsSummary(
        total_reports=total_reports,
        reports_by_status=status_counts,
        diseases_by_category=category_counts,
        diseases_by_severity=severity_counts,
        average_patient_age=average_age,
        most_common_disease=most_common_disease[0] if most_common_disease else None,
    )
