def create_report(db: Session) -> models.Report:
    report = models.Report()
    db.add(report)
    db.commit()
    db.refresh(report)
    return report
