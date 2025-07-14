from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from api import models, schemas
from api.dependencies import get_db
from api.enums import ReportStateEnum
from api.audit_log import log_audit_event

router = APIRouter()


# --------------------------
# Create new report - POST /api/reports
# --------------------------
@router.post("/", response_model=schemas.Report, status_code=status.HTTP_201_CREATED)
def create_report(created_by: int, db: Session = Depends(get_db)):
    report = models.Report(created_by=created_by)
    db.add(report)
    db.commit()
    db.refresh(report)

    log_audit_event(
        db=db,
        user_id=created_by,
        action="CREATE",
        entity_type="Report",
        entity_id=report.id,
        changes=None,
    )

    return report


# --------------------------
# List reports (paginated) - GET /api/reports
# --------------------------
@router.get("/", response_model=List[schemas.Report])
def list_reports(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.Report).offset(skip).limit(limit).all()


# --------------------------
# Get a specific report by ID - GET /api/reports/{report_id}
# --------------------------
@router.get("/{report_id}", response_model=schemas.Report)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


# --------------------------
# Update a report (only if status is Draft)
# --------------------------
@router.put("/{report_id}", response_model=schemas.Report)
def update_report(
    report_id: int, updated_data: schemas.ReportCreate, db: Session = Depends(get_db)
):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.status.value != ReportStateEnum.draft.value:
        raise HTTPException(status_code=400, detail="Only draft reports can be updated")

    report.status = updated_data.status
    db.commit()
    db.refresh(report)
    return report


# --------------------------
# Delete a report (only if status is Draft)
# --------------------------
@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.status.value != ReportStateEnum.draft.value:
        raise HTTPException(status_code=400, detail="Only draft reports can be deleted")

    db.delete(report)
    db.commit()
    return None


# --------------------------
# Submit a report (change status to 'submitted')
# --------------------------
@router.post("/{report_id}/submit", status_code=status.HTTP_200_OK)
def submit_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.status != ReportStateEnum.draft:
        raise HTTPException(
            status_code=400, detail="Only draft reports can be submitted"
        )

    # Ensure all required relationships exist
    if not report.reporter or not report.patient or not report.disease:
        raise HTTPException(
            status_code=400,
            detail="Cannot submit incomplete report. Ensure reporter, patient, and disease are set.",
        )

    report.status = ReportStateEnum.submitted
    db.commit()
    db.refresh(report)
    return {"message": "Report submitted successfully", "report_id": report.id}


# --------------------------
# Get recent submitted reports (most recent 10)
# --------------------------
@router.get("/recent", response_model=List[schemas.Report])
def get_recent_reports(db: Session = Depends(get_db)):
    recent = (
        db.query(models.Report)
        .filter(models.Report.status == ReportStateEnum.submitted)
        .order_by(models.Report.created_at.desc())
        .limit(10)
        .all()
    )
    return recent
