"""
Reporter Endpoints for Disease Outbreak Reporting System.

This module provides API endpoints for managing reporter details associated with disease outbreak reports.
Reporters represent healthcare professionals submitting the reports and are linked to individual reports
via a one-to-many relationship (one reporter can submit multiple reports).

Endpoints:
    - POST /api/reports/{id}/reporter: Add or update reporter details for a specific report.
    - GET /api/reports/{id}/reporter: Retrieve reporter details associated with a specific report.

Features:
    - Automatically creates a new reporter if the provided email does not exist.
    - Updates existing reporter details if the email matches an existing record.
    - Only allows assigning or modifying reporter details on draft reports.
    - Includes audit logging for all create and update actions.
    - Requires authenticated user access for all operations.

Security:
    - All endpoints require valid authentication via JWT token.
    - Access is restricted to authenticated users, validated using OAuth2 password flow.

See Also:
    - Models: `models.Reporter`, `models.Report`
    - Schemas: `schemas.ReporterCreate`, `schemas.Reporter`
    - Audit Logging: `log_audit_event` in `audit_log.py`
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import models, schemas
from api.dependencies import get_db, get_current_user
from api.audit_log import log_audit_event

router = APIRouter()


# -------------------------------
# POST /api/reports/{id}/reporter
# -------------------------------
@router.post(
    "/{report_id}/reporter",
    response_model=schemas.Reporter,
    status_code=status.HTTP_201_CREATED,
    summary="Add or Update Reporter to Report",
    description="Assign a reporter to a report. If the reporter does not exist, it will be created. Otherwise, it will update the reporter details.",
    response_description="Reporter details assigned to the report.",
    responses={
        404: {"description": "Report not found"},
        400: {"description": "Reporter can only be added to draft reports"},
    },
)
def add_or_update_reporter(
    report_id: int,
    reporter_data: schemas.ReporterCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Assign or update reporter details for a specific report.

    This endpoint allows authenticated users to assign a reporter to a draft report. If the reporter email
    already exists in the system, the reporter's details will be updated. Otherwise, a new reporter record
    will be created and linked to the report.

    Business Rules:
        - Only draft reports can have their reporter details modified.
        - Reporter uniqueness is determined by email address.
        - Automatically creates or updates the reporter and links them to the report.
        - Triggers audit log events for both reporter creation and update actions.

    Args:
        report_id (int): ID of the report to which the reporter should be assigned.
        reporter_data (schemas.ReporterCreate): Reporter information including name, contact details,
            job title, and organization details.
        db (Session): Database session dependency.
        current_user (models.User): Authenticated user performing the action.

    Raises:
        HTTPException (404): If the report does not exist.
        HTTPException (400): If the report is not in draft status.

    Returns:
        schemas.Reporter: The reporter details associated with the report.
    """
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.status != schemas.ReportStateEnum.draft:
        raise HTTPException(
            status_code=400, detail="Reporter can only be added to draft reports"
        )

    # Check if reporter exists by email
    reporter = (
        db.query(models.Reporter)
        .filter(models.Reporter.email == reporter_data.email)
        .first()
    )

    if reporter:
        # Update reporter details
        for field, value in reporter_data.dict().items():
            setattr(reporter, field, value)
        action = "UPDATE"
    else:
        # Create new reporter
        reporter = models.Reporter(**reporter_data.dict())
        db.add(reporter)
        action = "CREATE"

    # Link reporter to report
    report.reporter = reporter

    db.commit()
    db.refresh(reporter)

    log_audit_event(
        db=db,
        user_id=current_user.id,
        action=action,
        entity_type="Reporter",
        entity_id=reporter.id,
        changes=reporter_data.model_dump(mode="json"),
    )

    return reporter


# -------------------------------
# GET /api/reports/{id}/reporter
# -------------------------------
@router.get(
    "/{report_id}/reporter",
    response_model=schemas.Reporter,
    status_code=status.HTTP_200_OK,
    summary="Get Reporter by Report",
    description="Fetch the reporter associated with a specific report.",
    response_description="Reporter details of the report.",
    responses={
        404: {
            "description": "Report not found or reporter not associated with this report"
        },
    },
)
def get_reporter_by_report(
    report_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve reporter details linked to a specific report.

    This endpoint fetches the reporter assigned to a particular report. It ensures the report exists and
    has an associated reporter.

    Business Rules:
        - Works for all reports irrespective of status (draft, submitted, approved).
        - Ensures the report exists before fetching associated reporter details.

    Args:
        report_id (int): ID of the report whose reporter is to be fetched.
        db (Session): Database session dependency.

    Raises:
        HTTPException (404): If the report does not exist.
        HTTPException (404): If no reporter is associated with the report.

    Returns:
        schemas.Reporter: The reporter details associated with the report.
    """
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if not report.reporter:
        raise HTTPException(
            status_code=404, detail="Reporter not associated with this report"
        )

    return report.reporter
