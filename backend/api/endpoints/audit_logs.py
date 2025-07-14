"""Audit Logs Endpoint

This module provides an endpoint to retrieve audit logs from the database.
It supports optional date filtering and pagination.

Returns:
    - List of audit logs with optional date filtering and pagination.
"""

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
    """Fetch audit logs with optional date filtering and pagination.

    Args:
        start_date (Optional[datetime], optional): Date from which to retrieve audit logs. Defaults to Query(None).
        end_date (Optional[datetime], optional): Date until which to retrieve audit logs. Defaults to Query(None).
        skip (int, optional): Number of logs to skip for pagination. Defaults to 0.
        limit (int, optional): Maximum number of logs to return. Defaults to 20.
        db (Session, optional): Database session dependency. Defaults to Depends(get_db). Defaults to Depends(get_db).

    Returns:
        List[schemas.AuditLog]: List of audit logs filtered by date and paginated.
    """
    query = db.query(models.AuditLog)

    if start_date:
        query = query.filter(models.AuditLog.timestamp >= start_date)
    if end_date:
        query = query.filter(models.AuditLog.timestamp <= end_date)

    logs = (
        query.order_by(models.AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    )
    return logs
