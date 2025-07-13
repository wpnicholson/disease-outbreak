from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from api import models, schemas
from api.dependencies import get_db
from api.enums import ReportStateEnum

router = APIRouter()


@router.get("/search", response_model=List[schemas.Report])
def search_reports(
    status: Optional[ReportStateEnum] = Query(None),
    disease_name: Optional[str] = Query(None),
    hospital_name: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    query = db.query(models.Report)

    if status:
        query = query.filter(models.Report.status == status)

    if disease_name:
        query = query.join(models.Disease).filter(
            models.Disease.disease_name.ilike(f"%{disease_name}%")
        )

    if hospital_name:
        query = query.join(models.Reporter).filter(
            models.Reporter.hospital_name.ilike(f"%{hospital_name}%")
        )

    results = query.offset(skip).limit(limit).all()
    return results
