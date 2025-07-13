from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from api import models, schemas
from api.dependencies import get_db

router = APIRouter()


# --------------------------
# Create a new report
# --------------------------
@router.post("/", response_model=schemas.Report, status_code=status.HTTP_201_CREATED)
def create_report(db: Session = Depends(get_db)):
    report = models.Report()
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


# --------------------------
# List paginated reports
# --------------------------
@router.get("/", response_model=List[schemas.Report])
def list_reports(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.Report).offset(skip).limit(limit).all()


# --------------------------
# Get a specific report by ID
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
    if report.status != models.ReportStateEnum.draft:
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
    if report.status != models.ReportStateEnum.draft:
        raise HTTPException(status_code=400, detail="Only draft reports can be deleted")

    db.delete(report)
    db.commit()
    return None
