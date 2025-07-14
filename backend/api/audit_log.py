from sqlalchemy.orm import Session
from api import models
from datetime import datetime


def log_audit_event(
    db: Session,
    user_id: int | None,
    action: str,
    entity_type: str,
    entity_id: int,
    changes: dict | None = None,
):
    log_entry = models.AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        changes=changes,
        timestamp=datetime.utcnow(),
    )
    db.add(log_entry)
    db.commit()
