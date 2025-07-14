from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from api import models, schemas
from api.dependencies import get_db
from api.enums import DiseaseCategoryEnum, ReportStateEnum
from datetime import date

router = APIRouter()


# --------------------------
# Get disease for a report
# --------------------------
@router.get(
    "/{report_id}/disease",
    response_model=schemas.Disease,
    summary="Get disease for report",
    description="Fetches the disease associated with a specific report.",
    response_description="Disease details associated with the report.",
    responses={
        404: {
            "description": "Report not found or disease not associated with report",
            "content": {"application/json": {"example": {"detail": "Not Found"}}},
        }
    },
)
def get_disease(report_id: int, db: Session = Depends(get_db)):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if not report.disease:
        raise HTTPException(
            status_code=404, detail="Disease not associated with report"
        )
    return report.disease


# --------------------------
# Add or update disease for a report
# --------------------------
@router.post(
    "/{report_id}/disease",
    response_model=schemas.Disease,
    status_code=status.HTTP_200_OK,
    summary="Add or update disease for report",
    description="Adds or updates the disease associated with a specific report.",
    response_description="Disease details after adding or updating.",
    responses={
        404: {
            "description": "Report not found",
            "content": {"application/json": {"example": {"detail": "Not Found"}}},
        },
        400: {
            "description": "Invalid request data or report state",
            "content": {"application/json": {"example": {"detail": "Bad Request"}}},
        },
    },
)
def upsert_disease(
    report_id: int, disease_data: schemas.DiseaseCreate, db: Session = Depends(get_db)
):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.status != ReportStateEnum.draft:
        raise HTTPException(
            status_code=400, detail="Cannot modify disease in non-draft report"
        )
    if not report.patient:
        raise HTTPException(
            status_code=400, detail="Cannot add disease before patient is set"
        )

    # Validation Rules: Cross-field validation (disease date vs patient DOB).
    if disease_data.date_detected < report.patient.date_of_birth:
        raise HTTPException(
            status_code=400,
            detail="Disease detection date cannot be before patient's date of birth",
        )

    # Validation Rules: date range validations.
    if disease_data.date_detected > date.today():
        raise HTTPException(
            status_code=400,
            detail="Disease detection date cannot be in the future",
        )

    # Check if the report already has a disease.
    if report.disease:
        db.delete(report.disease)
        db.flush()

    # Always create a new Disease per report.
    new_disease = models.Disease(**disease_data.model_dump())
    report.disease = new_disease
    db.add(new_disease)

    db.commit()
    db.refresh(report)
    return report.disease


# --------------------------
# Get all disease categories (enum values)
# --------------------------
@router.get(
    "/diseases/categories",
    response_model=List[str],
    summary="Get disease categories",
    description="Fetches all disease categories defined in the system.",
    response_description="List of disease categories.",
    responses={
        200: {
            "description": "List of disease categories",
            "content": {
                "application/json": {"example": ["Infectious", "Genetic", "Chronic"]}
            },
        }
    },
)
def get_disease_categories():
    return [category.value for category in DiseaseCategoryEnum]
