import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import Base, engine
from app.api.router import api_router
from app.services.model_trainer import load_active_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup sequence
    print("[Startup] Initializing Database Tables...")
    Base.metadata.create_all(bind=engine)
    
    print("[Startup] Verifying Machine Learning Models...")
    load_active_model()
    print("[Startup] AI Phishing Detection System is online!")
    yield
    print("[Shutdown] Cleaning up resources...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "status": "online",
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

@app.get(f"{settings.API_V1_STR}/health")
def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred.", "error": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
