from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from api import models, schemas
from api.dependencies import get_db

router = APIRouter()


@router.get(
    "/",
    response_model=List[schemas.AuditLog],
    summary="Get audit logs",
    description="Fetches audit logs with optional date filtering and pagination.",
    response_description="List of audit logs.",
    responses={200: {"description": "Successful response"}},
)
def get_audit_logs(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    query = db.query(models.AuditLog)

    if start_date:
        query = query.filter(models.AuditLog.timestamp >= start_date)
    if end_date:
        query = query.filter(models.AuditLog.timestamp <= end_date)

    logs = (
        query.order_by(models.AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    )
    return logs
