from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api import models, schemas
from api.dependencies import get_db
from api.enums import ReportStateEnum

router = APIRouter()


# --------------------------
# Get reporter for a report
# --------------------------
@router.get(
    "/{report_id}/reporter",
    response_model=schemas.Reporter,
    summary="Get reporter for a report",
    description="Retrieve the reporter associated with a specific report by its ID.",
    response_description="Reporter details",
)
def get_reporter(report_id: int, db: Session = Depends(get_db)):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if not report.reporter:
        raise HTTPException(
            status_code=404, detail="Reporter not associated with report"
        )
    return report.reporter


# --------------------------
# Add or update reporter for a report
# --------------------------
@router.post(
    "/{report_id}/reporter",
    response_model=schemas.Reporter,
    status_code=status.HTTP_201_CREATED,
    summary="Add or update reporter for a report",
    description="Add a new reporter or update an existing reporter associated with a specific report by its ID.",
    response_description="Reporter details",
)
def upsert_reporter(
    report_id: int, reporter_data: schemas.ReporterCreate, db: Session = Depends(get_db)
):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.status != ReportStateEnum.draft:
        raise HTTPException(
            status_code=400, detail="Cannot modify reporter in non-draft report"
        )

    # If reporter already exists (via email), use them
    existing_reporter = (
        db.query(models.Reporter)
        .filter(models.Reporter.email == reporter_data.email)
        .first()
    )
    if existing_reporter:
        report.reporter = existing_reporter
    else:
        new_reporter = models.Reporter(**reporter_data.dict())
        db.add(new_reporter)
        report.reporter = new_reporter

    db.commit()
    db.refresh(report)
    return report.reporter
