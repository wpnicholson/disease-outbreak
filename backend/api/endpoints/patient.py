from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from api import models, schemas
from api.dependencies import get_db
from api.enums import ReportStateEnum

router = APIRouter()


# --------------------------
# Get patient details for a report
# --------------------------
@router.get(
    "/{report_id}/patient",
    response_model=schemas.Patient,
    summary="Get patient details for a report",
    description="Retrieves the patient details associated with a specific report.",
    response_description="Patient details.",
    responses={
        404: {
            "description": "Report not found or patient not associated with report",
            "content": {"application/json": {"example": {"detail": "Not Found"}}},
        }
    },
)
def get_patient(report_id: int, db: Session = Depends(get_db)):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if not report.patient:
        raise HTTPException(
            status_code=404, detail="Patient not associated with report"
        )
    return report.patient


# --------------------------
# Add or update patient details for a report
# --------------------------
@router.post(
    "/{report_id}/patient",
    response_model=schemas.Patient,
    status_code=status.HTTP_201_CREATED,
    summary="Add or update patient details for a report",
    description="Adds or updates the patient details associated with a specific report. "
    "This can only be done if the report is in draft state and has a reporter set.",
    response_description="Patient details after upsert.",
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
def upsert_patient(
    report_id: int, patient_data: schemas.PatientCreate, db: Session = Depends(get_db)
):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.status != ReportStateEnum.draft:
        raise HTTPException(
            status_code=400, detail="Cannot modify patient in non-draft report"
        )
    if not report.reporter:
        raise HTTPException(
            status_code=400, detail="Cannot add patient before reporter is set"
        )
    if patient_data.date_of_birth > date.today():
        raise HTTPException(
            status_code=400, detail="Date of birth cannot be in the future"
        )

    # Ensure medical_record_number is unique per hospital
    hospital_name = report.reporter.hospital_name
    existing_patient = (
        db.query(models.Patient)
        .join(models.Report)
        .join(models.Reporter)
        .filter(
            models.Patient.medical_record_number == patient_data.medical_record_number,
            models.Report.reporter_id == models.Reporter.id,
            models.Reporter.hospital_name == hospital_name,
        )
        .first()
    )

    if existing_patient:
        report.patient = existing_patient
    else:
        new_patient = models.Patient(**patient_data.dict())
        report.patient = new_patient
        db.add(new_patient)

    db.commit()
    db.refresh(report)
    return report.patient
