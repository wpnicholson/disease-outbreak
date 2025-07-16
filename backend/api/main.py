from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom OpenAPI schema with Bearer Authentication
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="Disease Outbreak Reporting System API documentation",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(search.router, prefix="/api/reports", tags=["Search"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(reporter.router, prefix="/api/reports", tags=["Reporter"])
app.include_router(patient.router, prefix="/api/reports", tags=["Patient"])
app.include_router(disease.router, prefix="/api/reports", tags=["Disease"])
app.include_router(statistics.router, prefix="/api", tags=["Statistics"])
app.include_router(export.router, prefix="/api/reports", tags=["Export"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(audit_logs.router, prefix="/api/audit-logs", tags=["Audit Logs"])
