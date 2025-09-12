
from app.services.kb_service import KBService
import llama_index.core as core

def test_load_from_arxiv_ingests(dummy_arxiv, monkeypatch):
    calls = {"docs_len": 0}
    real_from_docs = core.VectorStoreIndex.from_documents
    def spy(cls, docs, storage_context=None, embed_model=None):
        calls["docs_len"] = len(list(docs))
        return real_from_docs(docs, storage_context=storage_context, embed_model=embed_model)
    monkeypatch.setattr(core.VectorStoreIndex, "from_documents", classmethod(spy))

    kb = KBService()
    out = kb.load_from_arxiv(query="foo", max_results=2)

    assert calls["docs_len"] >= 2
    assert out == {"ingested": calls["docs_len"]}
