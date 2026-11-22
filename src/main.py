from fastapi import FastAPI
from src.api.routes.health import router as health_router

app = FastAPI(
    title="Document Intelligence Platform",
    description="A team-based AI platform for PDF intelligence.",
    version="0.1.0"
)

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["System"]
)


@app.get("/")
def root():
    return {
        "message": "Document Intelligence Platform API",
        "docs": "/docs"
    }
