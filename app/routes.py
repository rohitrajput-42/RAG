from fastapi import FastAPI
from app.endpoints import health, query, upload_document, list_document

def register_routes(app: FastAPI):
    app.include_router(health.router, prefix="/api/health", tags=["Health"])
    app.include_router(query.router, prefix="/api/query", tags=["Query"])
    app.include_router(upload_document.router, prefix="/api/upload_document", tags=["Upload Document"])
    app.include_router(list_document.router, prefix="/api/list_document", tags=["List Document"])