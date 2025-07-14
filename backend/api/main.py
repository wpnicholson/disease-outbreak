from fastapi import FastAPI
from api.endpoints import (
    reports,
    reporter,
    patient,
    disease,
    statistics,
    search,
    export,
    auth,
    audit_logs,
)

app = FastAPI(title="Disease Outbreak Reporting System", version="0.1.0")

app.include_router(search.router, prefix="/api/reports", tags=["Search"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(reporter.router, prefix="/api/reports", tags=["Reporter"])
app.include_router(patient.router, prefix="/api/reports", tags=["Patient"])
app.include_router(disease.router, prefix="/api/reports", tags=["Disease"])
app.include_router(statistics.router, prefix="/api", tags=["Statistics"])
app.include_router(export.router, prefix="/api/reports", tags=["Export"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(audit_logs.router, prefix="/api/audit-logs", tags=["Audit Logs"])
