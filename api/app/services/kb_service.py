# api/app/services/kb_service.py
from typing import List
from llama_index.core import VectorStoreIndex, StorageContext, Document
from .qdrant_service import QdrantService
from .ollama_service import OllamaService

# try the dedicated papers reader first
def _load_arxiv_docs(query: str, max_results: int) -> List[Document]:
    try:
        # new reader package
        from llama_index.readers.papers import ArxivReader  # requires llama-index-readers-papers
        reader = ArxivReader()
        # by query (you can also use paper_ids=[...])
        return reader.load_data(query=query, max_results=max_results)
    except Exception:
        # fallback: plain arxiv client → title+abstract
        import arxiv
        docs: List[Document] = []
        search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.SubmittedDate)
        for r in search.results():
            text = f"Title: {r.title}\n\nAbstract:\n{r.summary}"
            meta = {
                "source": "arxiv",
                "arxiv_id": r.entry_id.split("/")[-1],
                "title": r.title,
                "authors": [a.name for a in r.authors],
                "published": r.published.isoformat() if r.published else None,
                "updated": r.updated.isoformat() if r.updated else None,
                "pdf_url": getattr(r, "pdf_url", None),
            }
            docs.append(Document(text=text, metadata=meta))
        return docs

class KBService:
    def __init__(self):
        self.q = QdrantService()
        self.o = OllamaService()

    def load_from_arxiv(self, query: str, max_results: int = 3):
        docs = _load_arxiv_docs(query, max_results)
        storage = StorageContext.from_defaults(vector_store=self.q.vector_store())
        VectorStoreIndex.from_documents(
            docs,
            storage_context=storage,
            embed_model=self.o.get_embed(),
        )
        return {"ingested": len(docs)}

    def reset(self):
        return self.q.reset()
