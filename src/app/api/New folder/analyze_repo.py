from fastapi import APIRouter
from app.schemas.repo_schema import RepoRequest
from app.services.evaluation_service import evaluate_repo

router = APIRouter()

@router.post("/")
async def analyze_repository(req: RepoRequest): 
    report = await evaluate_repo(req.repo_url)
    return report