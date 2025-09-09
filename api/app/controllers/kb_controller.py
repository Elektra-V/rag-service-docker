from fastapi import APIRouter
from app.models.schemas import KBLoadParams
from app.services.kb_service import KBService

router = APIRouter()
kb = KBService()

@router.get("/load")
def load_kb(p: KBLoadParams = KBLoadParams()):
    return kb.load_from_arxiv(query=p.query, max_results=p.max_results)

@router.delete("/")
def reset_kb():
    return {"cleared": kb.reset()}