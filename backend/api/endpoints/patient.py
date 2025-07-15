"""
Patient Endpoints

This module provides API endpoints to manage patient records and their association
with disease outbreak reports within the Disease Outbreak Reporting System.

Endpoints include:
- Creating individual patient records.
- Associating and updating patients within specific reports.
- Retrieving patient information independently or by report.
- Deleting patient records and their associations from the system.

Audit logging is automatically handled for all create, update, and delete operations,
ensuring full traceability of data changes.

Security:
- Most endpoints require authenticated users.
- Audit logging captures the user ID for traceability.

Returns:
    - Patient records, list of patients associated with reports, or confirmation of deletions.
"""

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from typing import List

from api import models, schemas
from api.dependencies import get_db, get_current_user
from api.audit_log import log_audit_event

router = APIRouter()


# -------------------------------
# POST /api/reports/{report_id}/patient
# -------------------------------
@router.post(
    "/{report_id}/patient",
    response_model=List[schemas.Patient],
    status_code=status.HTTP_201_CREATED,
    summary="Add or update patient details to report",
    description="Adds a list of patient IDs to a specific report, replacing existing links.",
    response_description="List of all patients associated with the report.",
    responses={
        404: {"description": "Report not found or one or more patients not found"},
        400: {"description": "Invalid patient data or report not in draft state"},
    },
)
def add_or_update_patients_to_report(
    patient_link: schemas.ReportPatientsLink,
    report_id: int = Path(..., description="Report ID"),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    """
    Add or update the list of patients associated with a report.

    This endpoint allows replacing the entire list of patients linked to a report
    with a new set of patient IDs provided by the client.

    Args:
        patient_link (schemas.ReportPatientsLink): List of patient IDs to associate with the report.
        report_id (int): ID of the report to update patient associations.
        db (Session): SQLAlchemy database session.
        user (models.User): Authenticated user performing the operation.

    Raises:
        HTTPException (404): If the report is not found.
        HTTPException (404): If one or more patient IDs do not exist in the system.

    Returns:
        List[schemas.Patient]: List of patient records now associated with the report.
    """
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    patients = (
        db.query(models.Patient)
        .filter(models.Patient.id.in_(patient_link.patient_ids))
        .all()
    )

    if len(patients) != len(patient_link.patient_ids):
        raise HTTPException(status_code=404, detail="One or more patients not found")

    report.patients = patients
    db.commit()
    db.refresh(report)

    log_audit_event(
        db,
        user_id=user.id,
        action="UPDATE",
        entity_type="Report",
        entity_id=report_id,
        changes={"patients": [p.id for p in patients]},
    )

    return report.patients


# -------------------------------
# GET /api/reports/{report_id}/patient
# -------------------------------
@router.get(
    "/{report_id}/patient",
    response_model=List[schemas.Patient],
    status_code=status.HTTP_200_OK,
    summary="Get patients associated with a report",
    description="Retrieves a list of patients linked to a specific report.",
    response_description="List of patients linked to the report.",
    responses={404: {"description": "Report not found"}},
)
def get_patients_for_report(
    report_id: int = Path(..., description="Report ID"),
    db: Session = Depends(get_db),
):
    """
    Retrieve all patients associated with a specific report.

    Args:
        report_id (int): ID of the report whose patients are to be retrieved.
        db (Session): SQLAlchemy database session.

    Raises:
        HTTPException (404): If the report is not found.

    Returns:
        List[schemas.Patient]: List of patients associated with the report.
    """
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return report.patients


# -------------------------------
# POST /api/patient
# -------------------------------
@router.post(
    "/patient",
    response_model=schemas.Patient,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new patient record",
    description="Creates a new patient independently of any report.",
    response_description="The newly created patient record.",
    responses={
        400: {"description": "Invalid patient data"},
    },
)
def create_patient(
    patient_data: schemas.PatientCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    """
    Create a new patient record in the system.

    This endpoint allows for creating patient records without associating them with any specific report.
    These records can later be linked to reports via other endpoints.

    Args:
        patient_data (schemas.PatientCreate): Patient details.
        db (Session): SQLAlchemy database session.
        user (models.User): Authenticated user performing the creation.

    Returns:
        schemas.Patient: The newly created patient record.
    """
    patient = models.Patient(**patient_data.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)

    log_audit_event(
        db,
        user_id=user.id,
        action="CREATE",
        entity_type="Patient",
        entity_id=patient.id,
        changes=patient_data.model_dump(),
    )

    return patient


# -------------------------------
# GET /api/patient/{patient_id}
# -------------------------------
@router.get(
    "/patient/{patient_id}",
    response_model=schemas.Patient,
    status_code=status.HTTP_200_OK,
    summary="Get patient details by ID",
    description="Retrieve a single patient record by its ID.",
    response_description="The patient record.",
    responses={404: {"description": "Patient not found"}},
)
def get_patient_by_id(
    patient_id: int = Path(..., description="Patient ID"),
    db: Session = Depends(get_db),
):
    """
    Retrieve the details of a specific patient by ID.

    Args:
        patient_id (int): ID of the patient to retrieve.
        db (Session): SQLAlchemy database session.

    Raises:
        HTTPException (404): If the patient is not found.

    Returns:
        schemas.Patient: Patient record corresponding to the given ID.
    """
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# -------------------------------
# DELETE /api/patient/{patient_id}
# -------------------------------
@router.delete(
    "/patient/{patient_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a patient",
    description="Deletes a patient record independently of reports. This removes only the patient and its report associations.",
    response_description="Patient deleted successfully.",
    responses={404: {"description": "Patient not found"}},
)
def delete_patient(
    patient_id: int = Path(..., description="Patient ID"),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    """
    Delete a patient record from the database.

    This operation:
    - Deletes the patient.
    - Removes any association between the patient and reports via the association table.
    - Does not delete or alter any reports the patient was previously linked to.

    Args:
        patient_id (int): ID of the patient to delete.
        db (Session): SQLAlchemy database session.
        user (models.User): Authenticated user performing the deletion.

    Raises:
        HTTPException (404): If the patient is not found.

    Returns:
        None
    """
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(patient)
    db.commit()

    log_audit_event(
        db,
        user_id=user.id,
        action="DELETE",
        entity_type="Patient",
        entity_id=patient_id,
    )
