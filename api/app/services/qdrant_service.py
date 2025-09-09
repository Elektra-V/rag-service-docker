from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
import os

QDRANT_URL = os.getenv("QDRANT_URL","http://qdrant:6333")
COLL = os.getenv("QDRANT_COLLECTION","docs")

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL)
        self.store = QdrantVectorStore(client=self.client, collection_name=COLL)
    def vector_store(self): return self.store
    def reset(self):
        if self.client.collection_exists(COLL): self.client.delete_collection(COLL)
        # collection will be re-created by LlamaIndex on insert
        return True