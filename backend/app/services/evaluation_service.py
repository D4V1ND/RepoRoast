from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_chroma import Chroma
from typing_extensions import TypedDict
from app.agents.judges import alex_judge_node, sam_judge_node, jordan_judge_node
from app.agents.preparation_node import preparation_node
from app.agents.retriever_node import retriever_node

class repo_agent(TypedDict): 
    url: str
    local_dir: str
    vector_db: Chroma
    retriever: Chroma
    technical_eval: str
    qa_agent: RetrievalQA
    project_summary: str
    alex_judge: str
    sam_judge: str
    jordan_judge: str

def evaluate_repo(): 
    builder = StateGraph(repo_agent)
    builder.add_node("retriever_node", retriever_node)
    builder.add_node("preparation_node", preparation_node)
    builder.add_node("alex_judge_node", alex_judge_node)
    builder.add_node("sam_judge_node", sam_judge_node)
    builder.add_node("jordan_judge_node", jordan_judge_node)

    builder.add_edge(START, "retriever_node")
    builder.add_edge("retriever_node", "preparation_node")
    builder.add_edge("preparation_node", "alex_judge_node")
    builder.add_edge("alex_judge_node", "sam_judge_node")
    builder.add_edge("sam_judge_node", "jordan_judge_node")

    return builder.compile()