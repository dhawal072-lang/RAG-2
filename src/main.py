
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.documents import router as documents_router
from src.api.routes.health import router as health_router
from src.api.routes.chat import router as chat_router

app = FastAPI(
    title="Document Intelligence Platform",
    description="A team-based AI platform for PDF intelligence.",
    version="0.1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["System"]
)
app.include_router(
    chat_router,
    prefix="/api/v1/chat",
    tags=["Chat"]
)

app.include_router(
    documents_router,
    prefix="/api/v1/documents",
    tags=["Documents"]
)


@app.get("/")
def root():
    return {
        "message": "Document Intelligence Platform API",
        "docs": "/docs"
    }
