from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
import csv
import io

from api import models, schemas
from api.dependencies import get_db

router = APIRouter()


@router.get(
    "/export/{format}",
    summary="Export reports in specified format",
    description="Exports all reports in the specified format (JSON or CSV).",
    response_description="Exported report data.",
)
def export_reports(format: str, db: Session = Depends(get_db)):
    if format.lower() not in {"json", "csv"}:
        raise HTTPException(status_code=400, detail="Format must be 'json' or 'csv'")

    reports = db.query(models.Report).all()

    if format.lower() == "json":
        data = [schemas.Report.from_orm(r).dict() for r in reports]
        return JSONResponse(content=data)

    # CSV format
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow(
        [
            "report_id",
            "status",
            "created_at",
            "updated_at",
            "reporter_email",
            "patient_name",
            "disease_name",
        ]
    )

    # Rows
    for r in reports:
        writer.writerow(
            [
                r.id,
                r.status.value,
                r.created_at,
                r.updated_at,
                r.reporter.email if r.reporter else "",
                f"{r.patient.first_name} {r.patient.last_name}" if r.patient else "",
                r.disease.disease_name if r.disease else "",
            ]
        )

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=reports.csv"},
    )
