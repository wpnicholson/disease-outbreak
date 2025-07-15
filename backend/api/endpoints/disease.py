"""
Disease Endpoints

This module provides API endpoints to manage disease details associated with a disease outbreak report
within the Disease Outbreak Reporting System.

Functionalities include:
- Retrieving disease details linked to a report.
- Adding or updating disease information for draft reports.
- Removing disease details from draft reports.

Business Rules:
- Disease can only be modified when a report is in 'draft' status.
- Disease cannot be added with a detection date in the future.
- Disease records are managed via a one-to-one relationship with reports.
- Deleting a report cascade-deletes the associated disease.
- Full audit logging is performed on all create, update, and delete actions.

Security:
- Write actions (POST, DELETE) require authenticated users.
- Retrieval actions (GET) are accessible without user authentication.

Returns:
    JSON responses with disease details or confirmation messages.
"""

from fastapi import APIRouter, HTTPException, Depends, Path, status
from sqlalchemy.orm import Session
from datetime import date

from api import models, schemas
from api.dependencies import get_db, get_current_user
from api.audit_log import log_audit_event

router = APIRouter()


# -------------------------------
# GET /api/reports/{report_id}/disease
# -------------------------------
@router.get(
    "/{report_id}/disease",
    response_model=schemas.Disease,
    status_code=status.HTTP_200_OK,
    summary="Get disease details for a report",
    description="Retrieve disease details attached to a specific report.",
    response_description="Disease details.",
    responses={404: {"description": "Report or disease not found"}},
)
def get_disease(report_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    """
    Retrieve disease details associated with a specific report.

    Args:
        report_id (int): Unique identifier of the report. Must be greater than 0.
        db (Session): SQLAlchemy database session dependency.

    Raises:
        HTTPException (404): If the report or disease is not found.

    Returns:
        schemas.Disease: The disease details associated with the given report.
    """
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if not report.disease:
        raise HTTPException(
            status_code=404, detail="No disease assigned to this report"
        )
    return report.disease


# -------------------------------
# POST /api/reports/{report_id}/disease
# -------------------------------
@router.post(
    "/{report_id}/disease",
    response_model=schemas.Disease,
    status_code=status.HTTP_201_CREATED,
    summary="Add or update disease details for a report",
    description="Add or update disease details for a specific report. Only allowed if report status is 'draft'.",
    response_description="Updated disease details.",
    responses={
        404: {"description": "Report not found"},
        400: {
            "description": "Invalid request, report not in draft or date detected is in the future"
        },
    },
)
def create_or_update_disease(
    report_id: int,
    disease_data: schemas.DiseaseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Create or update disease details for a report.

    Business logic:
    - If no disease is linked to the report, creates a new disease.
    - If a disease exists, updates its attributes with new values.
    - Disease date cannot be in the future.
    - Operation allowed only if report is in draft status.
    - Audit logs are created for both creation and update actions.

    Args:
        report_id (int): ID of the report to which disease is being linked.
        disease_data (schemas.DiseaseCreate): Input payload containing disease details.
        db (Session): SQLAlchemy session dependency.
        current_user (models.User): Authenticated user making the request.

    Raises:
        HTTPException (404): If report not found.
        HTTPException (400): If report is not in draft or date_detected is invalid.

    Returns:
        schemas.Disease: The created or updated disease instance.
    """
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.status != models.ReportStateEnum.draft:
        raise HTTPException(
            status_code=400, detail="Cannot modify disease in non-draft report"
        )

    # Validation: Disease date cannot be in future
    if disease_data.date_detected > date.today():
        raise HTTPException(
            status_code=400, detail="Date detected cannot be in the future"
        )

    # Business logic: Attach disease to report
    if report.disease:
        disease = report.disease
        disease.disease_name = disease_data.disease_name
        disease.disease_category = disease_data.disease_category
        disease.date_detected = disease_data.date_detected
        disease.symptoms = disease_data.symptoms
        disease.severity_level = disease_data.severity_level
        disease.lab_results = disease_data.lab_results
        disease.treatment_status = disease_data.treatment_status
        action = "UPDATE"
    else:
        disease = models.Disease(
            disease_name=disease_data.disease_name,
            disease_category=disease_data.disease_category,
            date_detected=disease_data.date_detected,
            symptoms=disease_data.symptoms,
            severity_level=disease_data.severity_level,
            lab_results=disease_data.lab_results,
            treatment_status=disease_data.treatment_status,
            report=report,
        )
        db.add(disease)
        action = "CREATE"

    db.commit()
    db.refresh(disease)

    log_audit_event(
        db=db,
        user_id=current_user.id,
        action=action,
        entity_type="Disease",
        entity_id=disease.id,
        changes=disease_data.model_dump(),
    )

    return disease


# -------------------------------
# DELETE /api/reports/{report_id}/disease
# -------------------------------
@router.delete(
    "/{report_id}/disease",
    response_model=dict,
    summary="Remove disease from report",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Remove disease details from a report. Only possible if report is in draft state.",
    response_description="Disease removed successfully.",
    responses={
        404: {"description": "Report or disease not found"},
        400: {"description": "Cannot delete disease from non-draft report"},
    },
)
def delete_disease(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Remove the disease entry from a specific report.

    Business logic:
    - Disease removal is only allowed on draft reports.
    - The disease is deleted using ORM `delete-orphan` cascade via the report relationship.
    - Audit log is created recording the deletion event.

    Args:
        report_id (int): Unique identifier of the report.
        db (Session): SQLAlchemy session dependency.
        current_user (models.User): Authenticated user performing the deletion.

    Raises:
        HTTPException (404): If the report or disease does not exist.
        HTTPException (400): If the report is not in draft state.

    Returns:
        dict: Confirmation message on successful deletion.
    """
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.status != models.ReportStateEnum.draft:
        raise HTTPException(
            status_code=400, detail="Cannot delete disease from non-draft report"
        )

    if not report.disease:
        raise HTTPException(status_code=404, detail="No disease to delete")

    disease_id = report.disease.id
    report.disease = None  # triggers delete-orphan cascade

    db.commit()

    log_audit_event(
        db=db,
        user_id=current_user.id,
        action="DELETE",
        entity_type="Disease",
        entity_id=disease_id,
        changes=None,
    )

    return {"detail": "Disease deleted successfully"}
