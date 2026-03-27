from fastapi import APIRouter
from app.api.routes import analyze_repo

router = APIRouter()

router.include_router(analyze_repo.router, prefix="/analyze")