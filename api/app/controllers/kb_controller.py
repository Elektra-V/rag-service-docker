# api/app/controllers/kb_controller.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.kb_service import KBService

router = APIRouter()
kb = KBService()

class KBLoadParams(BaseModel):
    query: str
    max_results: int = 3

@router.post("/load_arxiv")
def load_arxiv(p: KBLoadParams):
    try:
        return kb.load_from_arxiv(query=p.query, max_results=p.max_results)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/")
def reset_kb():
    return {"cleared": kb.reset()}
