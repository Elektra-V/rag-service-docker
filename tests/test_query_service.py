
from app.services.query_service import QueryService

def test_query_service_ask_formats_sources():
    svc = QueryService()
    answer, sources = svc.ask("What is RAG?", top_k=3)

    assert isinstance(answer, str) and "dummy answer" in answer
    assert isinstance(sources, list) and len(sources) >= 1
    long = [s for s in sources if len(s["text"]) >= 300 or s["text"].endswith("...")]
    assert len(long) >= 1
    assert set(sources[0].keys()) == {"score", "text", "metadata"}
