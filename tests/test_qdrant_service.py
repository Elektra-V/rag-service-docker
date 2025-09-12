
from app.services.qdrant_service import QdrantService

def test_reset_deletes_collection():
    s = QdrantService()
    assert s.reset() is True
