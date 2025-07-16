from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session, joinedload
import csv
import io

from api import models, schemas
from api.dependencies import get_db, get_current_user
from api.audit_log import log_audit_event

router = APIRouter()


@router.get(
    "/export/{format}",
    summary="Export reports in specified format",
    description="Exports all reports in the specified format (JSON or CSV). Only authenticated users can access this endpoint.",
    response_description="Exported report data.",
    responses={
        400: {
            "description": "Invalid format specified",
            "content": {
                "application/json": {
                    "example": {"detail": "Format must be 'json' or 'csv'"}
                }
            },
        }
    },
)
def export_reports(
    format: str,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    """
    Export all report data in the specified format (json or csv).
    Authenticated users only. Records an audit log of the export.

    Args:
        format (str): Export format ('json' or 'csv').
        db (Session): Database session.
        user (models.User): Authenticated user requesting the export.

    Returns:
        JSONResponse or StreamingResponse: Exported data.
    """
    if format.lower() not in {"json", "csv"}:
        raise HTTPException(status_code=400, detail="Format must be 'json' or 'csv'")

    reports = (
        db.query(models.Report)
        .options(
            joinedload(models.Report.reporter),
            joinedload(models.Report.patients),
            joinedload(models.Report.disease),
        )
        .all()
    )

    # Log the export event
    log_audit_event(
        db=db,
        user_id=user.id,
        action="EXPORT",
        entity_type="Report",
        entity_id=0,
        changes={"format": format.lower()},
    )

    if format.lower() == "json":
        data = [
            schemas.Report.model_validate(r, from_attributes=True).model_dump(
                mode="json"
            )
            for r in reports
        ]
        return JSONResponse(content=data)

    # CSV export
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(
        [
            "report_id",
            "status",
            "created_at",
            "updated_at",
            "reporter_email",
            "patients",
            "disease_name",
        ]
    )

    for r in reports:
        patient_names = (
            ", ".join(f"{p.first_name} {p.last_name}" for p in r.patients)
            if r.patients
            else ""
        )
        writer.writerow(
            [
                r.id,
                r.status.value,
                r.created_at.isoformat() if r.created_at else "",
                r.updated_at.isoformat() if r.updated_at else "",
                r.reporter.email if r.reporter else "",
                patient_names,
                r.disease.disease_name if r.disease else "",
            ]
        )

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=reports.csv"},
    )
