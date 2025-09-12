
from app.models.schemas import KBLoadParams, QueryRequest, QueryResponse

def test_kbloadparams_defaults():
    p = KBLoadParams()
    assert p.query == "llamaindex"
    assert p.max_results == 3

def test_queryrequest_defaults():
    q = QueryRequest(question="Hi?")
    assert q.top_k == 4
    assert q.question == "Hi?"

def test_queryresponse_model():
    resp = QueryResponse(answer="ok", sources=[{"score": 0.9}])
    assert resp.answer == "ok"
    assert isinstance(resp.sources, list)
