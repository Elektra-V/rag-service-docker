from llama_index.core import VectorStoreIndex, StorageContext
from .qdrant_service import QdrantService
from .ollama_service import OllamaService

class QueryService:
    def __init__(self):
        self.q = QdrantService()
        self.o = OllamaService()
        storage = StorageContext.from_defaults(vector_store=self.q.vector_store())
        self.index = VectorStoreIndex.from_documents([], storage_context=storage, embed_model=self.o.get_embed())
        self.engine = None

    def ask(self, question: str, top_k: int = 4):
        if self.engine is None:
            self.engine = self.index.as_query_engine(llm=self.o.get_llm(), similarity_top_k=top_k, response_mode="compact")
        result = self.engine.query(question)
        sources = []
        if hasattr(result, "source_nodes"):
            for sn in result.source_nodes:
                sources.append({
                    "score": float(sn.score) if sn.score is not None else None,
                    "text": sn.text[:300] + ("..." if len(sn.text) > 300 else ""),
                    "metadata": sn.metadata or {},
                })
        return str(result), sources