# app/services/qdrant_service.py
import os
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore

QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
COLL = os.getenv("QDRANT_COLLECTION", "docs")

class QdrantService:
    def __init__(self,
                 client=None,
                 store=None,
                 url: Optional[str] = None,
                 collection: Optional[str] = None):
        self.url = url or QDRANT_URL
        self.collection = collection or COLL
        self._client = client
        self._store = store

    @property
    def client(self):
        if self._client is None:
            # created only when first used (tests can stub qdrant_client beforehand)
            self._client = QdrantClient(url=self.url)
        return self._client

    @property
    def store(self):
        if self._store is None:
            self._store = QdrantVectorStore(client=self.client, collection_name=self.collection)
        return self._store

    def vector_store(self):
        return self.store

    def reset(self) -> bool:
        # uses the (possibly stubbed) client
        if self.client.collection_exists(self.collection):
            self.client.delete_collection(self.collection)
        # collection will be recreated by LlamaIndex on insert
        return True