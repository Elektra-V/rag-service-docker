from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.services.query_service import QueryService

router = APIRouter()
svc = QueryService()

@router.post("/", response_model=QueryResponse)
def query(req: QueryRequest):
    answer, sources = svc.ask(req.question, top_k=req.top_k)
    return QueryResponse(answer=answer, sources=sources)