"""
Reports API Endpoints

This module provides RESTful API endpoints to manage disease outbreak reports within the Disease Outbreak Reporting System.

Each report records details of a disease outbreak and is associated with:
- A creator (User)
- A reporter (optional, healthcare professional details)
- A disease (one-to-one)
- One or more patients (many-to-many)

Core Features:
- Create, retrieve, update, and delete outbreak reports.
- Access control via JWT authentication.
- Supports draft editing lifecycle (only draft reports are editable/deletable).
- Integrated audit logging of report lifecycle changes.

Endpoints:
- POST   /api/reports: Create a new draft report.
- GET    /api/reports: List paginated reports.
- GET    /api/reports/{id}: Retrieve full report details.
- PUT    /api/reports/{id}: Update draft report status.
- DELETE /api/reports/{id}: Delete draft report.

Security:
- Requires authentication via `get_current_user`.
- Audit logs are generated for create, update, and delete actions.

Dependencies:
- FastAPI, SQLAlchemy ORM, JWT-based user authentication.
- Related models: Report, Reporter, Disease, Patient, User.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from api import models, schemas
from api.dependencies import get_db, get_current_user
from api.audit_log import log_audit_event

router = APIRouter()


# -------------------------------
# POST /api/reports
# -------------------------------
@router.post(
    "/",
    response_model=schemas.Report,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new report",
    description="Create a draft disease outbreak report.",
    response_description="The created report with initial status and empty associations.",
    responses={
        400: {"description": "Bad Request - Invalid report data"},
        401: {"description": "Unauthorized - Invalid or missing authentication token"},
        403: {
            "description": "Forbidden - User does not have permission to create reports"
        },
        422: {"description": "Unprocessable Entity - Validation error in report data"},
        201: {
            "description": "Report created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "status": "draft",
                        "created_at": "2023-10-01T12:00:00Z",
                        "updated_at": None,
                        "reporter_id": None,
                        "disease_id": None,
                        "patients": [],
                        "created_by": 1,
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error - Unexpected error during report creation"
        },
    },
)
def create_report(
    report_data: schemas.ReportCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    """
    Create a new draft report in the system.

    The created report is:
    - Linked to the authenticated user as creator.
    - Initially assigned 'draft' status (modifiable).
    - Empty by default (no reporter, disease, or patient attached).

    Args:
        report_data (schemas.ReportCreate): Input schema containing the initial status (defaults to draft).
        db (Session): SQLAlchemy database session (FastAPI dependency).
        user (models.User): The currently authenticated user creating the report.

    Returns:
        schemas.Report: The created report instance, including metadata and empty associations.
    """
    report = models.Report(
        status=report_data.status,
        created_by=user.id,
        creator=user,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    log_audit_event(db, user.id, "CREATE", "Report", report.id)
    return report


# -------------------------------
# GET /api/reports
# -------------------------------
@router.get(
    "/",
    response_model=list[schemas.Report],
    summary="List all reports",
    description="Paginated list of disease outbreak reports.",
    response_description="List of reports with associated reporter, patients, and disease data.",
    responses={
        200: {
            "description": "List of reports retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "status": "draft",
                            "created_at": "2023-10-01T12:00:00Z",
                            "updated_at": None,
                            "reporter_id": None,
                            "disease_id": None,
                            "patients": [],
                            "created_by": 1,
                        }
                    ]
                }
            },
        },
        401: {"description": "Unauthorized - Invalid or missing authentication token"},
        403: {
            "description": "Forbidden - User does not have permission to view reports"
        },
    },
)
def list_reports(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """
    Retrieve a paginated list of all reports.

    Returns a paginated response of all reports in the system, ordered by creation.
    Each report includes nested reporter, patient, and disease data using eager loading
    to avoid N+1 query issues.

    Args:
        skip (int): Number of records to skip for pagination. Defaults to 0.
        limit (int): Maximum number of reports to return. Defaults to 20.
        db (Session): SQLAlchemy database session.

    Returns:
        list[schemas.Report]: List of report objects with associations.
    """

    reports = (
        db.query(models.Report)
        .options(
            joinedload(models.Report.reporter),
            joinedload(models.Report.patients),
            joinedload(models.Report.disease),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
    return reports


# -------------------------------
# GET /api/reports/{id}
# -------------------------------
@router.get(
    "/{report_id}",
    response_model=schemas.Report,
    summary="Get report details",
    description="Retrieve full details of a specific report by ID.",
    response_description="Full report data including reporter, patients, and disease.",
    responses={
        200: {
            "description": "Report retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "status": "draft",
                        "created_at": "2023-10-01T12:00:00Z",
                        "updated_at": None,
                        "reporter_id": None,
                        "disease_id": None,
                        "patients": [],
                        "created_by": 1,
                    }
                }
            },
        },
        404: {"description": "Report not found - No report exists with the given ID"},
        401: {"description": "Unauthorized - Invalid or missing authentication token"},
        403: {
            "description": "Forbidden - User does not have permission to view this report"
        },
    },
)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
):
    """
    Get detailed information for a specific report.

    Fetches a report by its unique ID and returns its full data, including linked
    reporter, patients, and disease. Returns 404 if the report does not exist.

    Args:
        report_id (int): The ID of the report to retrieve.
        db (Session): SQLAlchemy database session.

    Raises:
        HTTPException: 404 if no report is found with the given ID.

    Returns:
        schemas.Report: Full report data with all associations.
    """

    report = (
        db.query(models.Report)
        .options(
            joinedload(models.Report.reporter),
            joinedload(models.Report.patients),
            joinedload(models.Report.disease),
        )
        .filter(models.Report.id == report_id)
        .first()
    )
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


# -------------------------------
# PUT /api/reports/{id}
# -------------------------------
@router.put(
    "/{report_id}",
    response_model=schemas.Report,
    summary="Update a draft report",
    description="Update report details (draft reports only).",
    response_description="The updated report with new status.",
    responses={
        200: {
            "description": "Report updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "status": "submitted",
                        "created_at": "2023-10-01T12:00:00Z",
                        "updated_at": "2023-10-02T12:00:00Z",
                        "reporter_id": None,
                        "disease_id": None,
                        "patients": [],
                        "created_by": 1,
                    }
                }
            },
        },
        400: {"description": "Bad Request - Report is not in draft status"},
        404: {"description": "Report not found - No report exists with the given ID"},
        401: {"description": "Unauthorized - Invalid or missing authentication token"},
        403: {
            "description": "Forbidden - User does not have permission to update this report"
        },
        422: {"description": "Unprocessable Entity - Validation error in report data"},
        500: {
            "description": "Internal Server Error - Unexpected error during report update"
        },
    },
)
def update_report(
    report_id: int,
    report_data: schemas.ReportBase,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    """
    Update a report's status (only allowed for drafts).

    Modifies the status of a report, but only if it is still in the 'draft' state.
    Prevents changes to submitted, under_review, or approved reports. Updates are
    limited to the `status` field.

    Audit logging:
        - Action: UPDATE
        - Entity: Report
        - Recorded fields: Report ID and new status

    Args:
        report_id (int): The ID of the report to update.
        report_data (schemas.ReportBase): The new status to assign.
        db (Session): SQLAlchemy database session.
        user (models.User): Authenticated user making the update.

    Raises:
        HTTPException: 404 if the report does not exist.
        HTTPException: 400 if the report is not in draft status.

    Returns:
        schemas.Report: The updated report object.
    """

    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.status != models.ReportStateEnum.draft:
        raise HTTPException(status_code=400, detail="Only draft reports can be edited")

    report.status = report_data.status
    db.commit()
    db.refresh(report)

    log_audit_event(db, user.id, "UPDATE", "Report", report.id)
    return report


# -------------------------------
# DELETE /api/reports/{id}
# -------------------------------
@router.delete(
    "/{report_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a draft report",
    description="Delete a report (only if in draft state).",
    response_description="Report deleted successfully (HTTP 204 no content response).",
    responses={
        204: {"description": "Report deleted successfully"},
        404: {"description": "Report not found - No report exists with the given ID"},
        400: {"description": "Bad Request - Report is not in draft status"},
        401: {"description": "Unauthorized - Invalid or missing authentication token"},
        403: {
            "description": "Forbidden - User does not have permission to delete this report"
        },
        500: {
            "description": "Internal Server Error - Unexpected error during report deletion"
        },
    },
)
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    """
    Delete a report from the system (only allowed for drafts).

    Deletes a report by ID, but only if the report is in 'draft' state.
    Deletion cascades:
        - Associated `Disease` entry is deleted (one-to-one cascade).
        - Patient links are removed from the association table (many-to-many).
        - The reporter is not deleted, only disassociated if necessary.

    Audit logging:
        - Action: DELETE
        - Entity: Report
        - Recorded fields: Report ID

    Args:
        report_id (int): The ID of the report to delete.
        db (Session): SQLAlchemy database session.
        user (models.User): The authenticated user requesting deletion.

    Raises:
        HTTPException: 404 if the report does not exist.
        HTTPException: 400 if the report is not in draft state.

    Returns:
        None: HTTP 204 No Content.
    """

    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.status != models.ReportStateEnum.draft:
        raise HTTPException(status_code=400, detail="Only draft reports can be deleted")

    db.delete(report)
    db.commit()
    log_audit_event(db, user.id, "DELETE", "Report", report.id)
