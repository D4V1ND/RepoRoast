from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.schemas.repo_schema import RepoRequest
from fastapi.responses import StreamingResponse
from langgraph.graph import StateGraph, START, END
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_chroma import Chroma
from typing_extensions import TypedDict
import time
import asyncio
import json 


from app.services.evaluation_service import evaluate_repo


router = APIRouter()

graph = evaluate_repo()

@router.post("/")
async def analyze_repository(req: RepoRequest): 
    queue = asyncio.Queue()
    """Run the graph and push each node's output to the queue."""
    async def run_graph():
        start_time = time.time()
        try:
            # You may need to wrap nodes manually if invoke is synchronous
            result = graph.invoke({"url": req.url})
            await queue.put({"node": "final_result", "output_alex": result["alex_judge"], "output_sam": result["sam_judge"], "output_jordan": result["jordan_judge"]})
        except Exception as e:
            await queue.put({"error": str(e)})
        finally:
            elapsed = time.time() - start_time
            await queue.put({"status": "done", "execution_time_seconds": elapsed})
            await queue.put(None)  # Sentinel

    async def event_generator():
        """Yield items from queue as JSON lines."""
        asyncio.create_task(run_graph())
        while True:
            item = await queue.get()
            if item is None:
                break
            yield json.dumps(item) + "\n"

    return StreamingResponse(event_generator(), media_type="application/json")