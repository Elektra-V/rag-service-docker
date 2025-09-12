
import sys, types, pytest

class DummyDoc:
    def __init__(self, text, metadata=None):
        self.text = text
        self.metadata = metadata or {}

class DummySourceNode:
    def __init__(self, text, score=None, metadata=None):
        self.text = text
        self.score = score
        self.metadata = metadata or {}

class DummyResult:
    def __init__(self, text, source_nodes=None):
        self._text = text
        self.source_nodes = source_nodes or []
    def __str__(self):
        return self._text

class DummyQueryEngine:
    def __init__(self, reply_text="dummy answer", sources=None):
        self._reply_text = reply_text
        self._sources = sources or []
    def query(self, question):
        return DummyResult(self._reply_text, self._sources)

class DummyIndex:
    def __init__(self):
        pass
    @classmethod
    def from_documents(cls, docs, storage_context=None, embed_model=None):
        idx = cls()
        idx._docs = list(docs)
        return idx
    def as_query_engine(self, llm=None, similarity_top_k=4, response_mode="compact"):
        sources = [
            DummySourceNode(text="source text 1", score=0.9, metadata={"a": 1}),
            DummySourceNode(text="source text 2 " * 40, score=0.5, metadata={"b": 2}),
        ]
        return DummyQueryEngine("dummy answer", sources)

class DummyStorageContext:
    @classmethod
    def from_defaults(cls, vector_store=None):
        inst = cls()
        inst.vector_store = vector_store
        return inst

@pytest.fixture(autouse=True)
def patch_external_libs(monkeypatch):
    # llama_index core
    core_mod = types.SimpleNamespace(
        VectorStoreIndex=DummyIndex,
        StorageContext=DummyStorageContext,
        Document=DummyDoc,
    )
    sys.modules["llama_index.core"] = core_mod

    # llama_index ollama + embeddings
    sys.modules["llama_index.llms.ollama"] = types.SimpleNamespace(
        Ollama=lambda **kwargs: object()
    )
    sys.modules["llama_index.embeddings.ollama"] = types.SimpleNamespace(
        OllamaEmbedding=lambda **kwargs: object()
    )

    # qdrant vector store + client
    sys.modules["llama_index.vector_stores.qdrant"] = types.SimpleNamespace(
        QdrantVectorStore=lambda client, collection_name: object()
    )

    class DummyQdrantClient:
        def __init__(self, url):
            self.url = url
            self._exists = True
        def collection_exists(self, name):
            return self._exists
        def delete_collection(self, name):
            self._exists = False

    sys.modules["qdrant_client"] = types.SimpleNamespace(QdrantClient=DummyQdrantClient)

    yield

@pytest.fixture
def dummy_arxiv(monkeypatch):
    class DummyArxivResult:
        def __init__(self, entry_id, title, summary, authors):
            self.entry_id = entry_id
            self.title = title
            self.summary = summary
            self.authors = [types.SimpleNamespace(name=a) for a in authors]
    class DummySearch:
        def __init__(self, query, max_results, sort_by=None):
            self.query = query
            self.max_results = max_results
        def results(self):
            return [
                DummyArxivResult("id1", "Title One", "Summary one", ["Alice", "Bob"]),
                DummyArxivResult("id2", "Title Two", "Summary two", ["Cara"]),
            ]
    sys.modules["arxiv"] = types.SimpleNamespace(Search=DummySearch)
    yield
