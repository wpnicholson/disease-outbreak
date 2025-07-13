from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api import models, schemas
from api.dependencies import get_db

router = APIRouter()


# --------------------------
# Get disease for a report
# --------------------------
@router.get("/{report_id}/disease", response_model=schemas.Disease)
def get_disease(report_id: int, db: Session = Depends(get_db)):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if not report.disease:
        raise HTTPException(
            status_code=404, detail="Disease not associated with report"
        )
    return report.disease


# --------------------------
# Add or update disease for a report
# --------------------------
@router.post(
    "/{report_id}/disease",
    response_model=schemas.Disease,
    status_code=status.HTTP_201_CREATED,
)
def upsert_disease(
    report_id: int, disease_data: schemas.DiseaseCreate, db: Session = Depends(get_db)
):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.status != models.ReportStateEnum.draft:
        raise HTTPException(
            status_code=400, detail="Cannot modify disease in non-draft report"
        )

    # If disease already exists (via disease_name), use it
    existing_disease = (
        db.query(models.Disease)
        .filter(models.Disease.disease_name == disease_data.disease_name)
        .first()
    )
    if existing_disease:
        report.disease = existing_disease
    else:
        new_disease = models.Disease(**disease_data.dict())
        db.add(new_disease)
        report.disease = new_disease

    db.commit()
    db.refresh(report)
    return report.disease
