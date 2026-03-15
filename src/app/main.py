from fastapi import FastAPI
from app.api.router import router

app = FastAPI(title="RepoRoast")

app.include_router(router)