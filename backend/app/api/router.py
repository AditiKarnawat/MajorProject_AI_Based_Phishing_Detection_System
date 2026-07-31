from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.scan import router as scan_router
from app.api.v1.history import router as history_router
from app.api.v1.stats import router as stats_router
from app.api.v1.model import router as model_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(scan_router)
api_router.include_router(history_router)
api_router.include_router(stats_router)
api_router.include_router(model_router)
