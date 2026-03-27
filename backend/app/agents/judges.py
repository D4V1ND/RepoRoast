from data.prompts import ALEX_PROMPT, SAM_PROMPT, JORDAN_PROMPT
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.output_parsers.retry import RetryWithErrorOutputParser
from app.model.model import model_03, model_0, embeddings_model
from typing import Literal, List, Dict
from pydantic import BaseModel, Field
import time

class alex_output(BaseModel): 
    innovation_score: int = Field(ge=1, le=10, description = "How innovative the project is (1-10).")
    strongest_innovation: str = Field(description = "Best innovation Idea.")
    brutally_honest_feedback: List[str] = Field(description = "Direct criticism about this project.")

def alex_judge_node(state):

    start1 = time.time()
    
    # summary = state["project_summary"]
    retriever = state["retriever"]
    queries = [
        "README project overview", 
        "system architecture workflow",                   
    ]
    docs = []
    for q in queries: 
        docs.extend(retriever.invoke(q))

    context = "\n\n".join(
        f"FILE: {d.metadata.get('file_path', 'unknown')}\n{d.page_content}"
        for d in docs
    )
    parser = PydanticOutputParser(pydantic_object=alex_output)
    
    innovation_prompt = PromptTemplate.from_template(ALEX_PROMPT)
    formatted_prompt = innovation_prompt.format_prompt(
        project_summary = context, 
        format_instructions = parser.get_format_instructions()
    )

    response = model_0.invoke(formatted_prompt.to_string())
    retry_parser = RetryWithErrorOutputParser.from_llm(
        parser=parser, 
        llm=model_0
    )

    parsed_alex_judge = retry_parser.parse_with_prompt(
        response.content, formatted_prompt
    )

    end1 = time.time()
    print(f"Execution time from alex judge is {end1 - start1: .4f} seconds")
    
    return {"alex_judge": parsed_alex_judge.dict()}


class FindingsOutput(BaseModel):
    file_path: str = Field(description="File path")
    severity: Literal["low", "medium", "high"] = Field(description="low|medium|high")
    issue: str = Field(description="Problem summary")
    evidence: str = Field(description="Code evidence")
    suggested_fix: str = Field(description="Fix suggestion")

class sam_output(BaseModel):
    score: int = Field(description="1-10 quality score")
    strengths: List[str] = Field(description="Good aspects")
    weakness: List[str] = Field(description = "bad aspects")
    # findings: List[str] = Field(description="Detected issues")
    
def sam_judge_node(state):

    start2 = time.time()
    
    retriever = state["retriever"]
        
    # queries = [
    #     "python functions classes error handling exceptions",
    #     "api backend routes database queries",
    # ]

    queries = [
    "python functions classes error handling exceptions api backend routes database queries"
    ]
    
    docs = []
    seen = set()
    for q in queries:
        results = retriever.invoke(q)
        for d in results: 
            key = (d.metadata.get("file_path"), d.page_content[:300])
            if key not in seen: 
                seen.add(key)
                docs.append(d)

    docs = docs[:8]
    context = "\n\n".join(
        f"FILE: {d.metadata.get('file_path', 'unknown')}\n{d.page_content[:800]}"
        for d in docs
    )
    parser = PydanticOutputParser(pydantic_object=sam_output)
    
    architecture_prompt = PromptTemplate.from_template(SAM_PROMPT)
    formatted_prompt = architecture_prompt.format_prompt(
        context = context,
        format_instructions = parser.get_format_instructions()
    )


    response = model_0.invoke(formatted_prompt.to_string())
    retry_parser = RetryWithErrorOutputParser.from_llm(
        parser=parser, 
        llm=model_0
    )
    parsed_sam_judge = retry_parser.parse_with_prompt(
        response.content, formatted_prompt
    )

    end2 = time.time()
    print(f"Execution time of sam judge is: {end2 - start2 :.4f} Seconds.")
    
    return {"sam_judge": parsed_sam_judge.dict()}



class jordan_output(BaseModel): 
    score: int = Field(ge=1, le=10, description = "a numeric score (1-10) that represents the impact of this project to real world.")
    impact: str = Field(description = "The real-world impact this project has.")
    evidence_of_real_world_value: List[str] = Field(description = "Evidence of Real-World Value")

def jordan_judge_node(state):
    
    start3 = time.time()
    
    retriever = state["retriever"]
    queries = ["README project purpose problem solved use case benefits"]
    docs = []
    for q in queries: 
        docs.extend(retriever.invoke(q))
        
    context = "\n\n".join(
        f"FILE: {d.metadata.get('file_path', 'unknown')}\n{d.page_content}"
        for d in docs
    )
    
    parser = PydanticOutputParser(pydantic_object=jordan_output)

    innovation_prompt = PromptTemplate.from_template(JORDAN_PROMPT)
    formatted_prompt = innovation_prompt.format_prompt(
        context = context, 
        format_instructions = parser.get_format_instructions()
    )

    response = model_0.invoke(formatted_prompt.to_string())
    retry_parser = RetryWithErrorOutputParser.from_llm(
        parser=parser, 
        llm=model_0
    )

    parsed_jordan_judge = retry_parser.parse_with_prompt(
        response.content, formatted_prompt
    )

    end3 = time.time()
    print(f"Execution time of judge node is {end3 - start3 :.4f} Seconds")
    
    return {"jordan_judge": parsed_jordan_judge.dict()}




