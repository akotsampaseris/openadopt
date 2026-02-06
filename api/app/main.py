"""
OpenAdopt API - Main application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.auth import router as auth_router
from app.api.admin.animals import router as admin_animals_router
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    debug=settings.DEBUG,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://192.168.1.100:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for local storage
if settings.STORAGE_BACKEND == "local":
    uploads_path = Path(settings.STORAGE_LOCAL_PATH)
    uploads_path.mkdir(parents=True, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=str(uploads_path)), name="uploads")

# Include routers
app.include_router(auth_router)
app.include_router(admin_animals_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to OpenAdopt API",
        "version": "0.1.0",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
