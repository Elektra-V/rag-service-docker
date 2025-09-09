from pydantic import BaseModel
from typing import List, Optional

class KBLoadParams(BaseModel):
    query: str = "llamaindex"
    max_results: int = 3

class QueryRequest(BaseModel):
    question: str
    top_k: int = 4

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]