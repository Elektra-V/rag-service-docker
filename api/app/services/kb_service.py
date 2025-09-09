from typing import List
import arxiv
from llama_index.core import VectorStoreIndex, StorageContext, Document
from .qdrant_service import QdrantService
from .ollama_service import OllamaService

class KBService:
    def __init__(self):
        self.q = QdrantService()
        self.o = OllamaService()

    def _fetch_arxiv(self, query: str, max_results: int) -> List[Document]:
        """
        Fetch titles + abstracts from arXiv (no extra reader dependency).
        """
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
        )
        docs: List[Document] = []
        for result in search.results():
            text = f"Title: {result.title}\n\nAbstract:\n{result.summary}"
            meta = {
                "source": "arxiv",
                "arxiv_id": result.entry_id.split("/")[-1],
                "title": result.title,
                "authors": [a.name for a in result.authors],
                "primary_category": getattr(result, "primary_category", None),
                "published": result.published.isoformat() if result.published else None,
                "updated": result.updated.isoformat() if result.updated else None,
                "pdf_url": getattr(result, "pdf_url", None),
            }
            docs.append(Document(text=text, metadata=meta))
        return docs

    def load_from_arxiv(self, query: str, max_results: int = 5):
        # 1) fetch arXiv items
        docs = self._fetch_arxiv(query, max_results)

        # 2) build/extend index in Qdrant
        storage = StorageContext.from_defaults(vector_store=self.q.vector_store())
        VectorStoreIndex.from_documents(
            docs,
            storage_context=storage,
            embed_model=self.o.get_embed(),
        )
        return {"ingested": len(docs)}

    def reset(self):
        return self.q.reset()