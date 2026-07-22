"""Qdrant vector store plugin for OpenRAG."""

from typing import List, Dict, Any

from core.contracts import VectorStoreBackend
from core.registry import register_plugin
from core.exceptions import PluginDependencyError

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False


@register_plugin("vectorstores", "qdrant")
class QdrantVectorStore(VectorStoreBackend):
    """Qdrant-backed vector store plugin supporting local in-memory or remote server mode."""

    def __init__(self, location: str = ":memory:", api_key: str | None = None, **kwargs: Any) -> None:
        if not QDRANT_AVAILABLE:
            raise PluginDependencyError(
                "Qdrant plugin requires 'qdrant-client'. Please install it using: pip install qdrant-client"
            )
        self.client = QdrantClient(location=location, api_key=api_key, **kwargs)
        self._collections: Dict[str, bool] = {}

    def _ensure_collection(self, collection_name: str, vector_size: int = 384) -> None:
        if collection_name not in self._collections:
            if not self.client.collection_exists(collection_name):
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
                )
            self._collections[collection_name] = True

    def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        embeddings: List[List[float]],
        ids: List[str],
    ) -> None:
        if not documents or not embeddings:
            return

        vector_size = len(embeddings[0])
        self._ensure_collection(collection_name, vector_size=vector_size)

        points = [
            PointStruct(id=idx_str, vector=emb, payload={"document": doc})
            for idx_str, emb, doc in zip(ids, embeddings, documents)
        ]
        self.client.upsert(collection_name=collection_name, points=points)

    def query(self, collection_name: str, query_embeddings: List[List[float]], n_results: int = 4) -> List[str]:
        if not query_embeddings:
            return []

        try:
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_embeddings[0],
                limit=n_results,
            )
            return [hit.payload.get("document", "") for hit in results if hit.payload]
        except Exception:
            return []

    def delete_collection(self, collection_name: str) -> bool:
        try:
            self.client.delete_collection(collection_name=collection_name)
            if collection_name in self._collections:
                del self._collections[collection_name]
            return True
        except Exception:
            return False

    def list_collections(self) -> List[str]:
        try:
            cols = self.client.get_collections()
            return [col.name for col in cols.collections]
        except Exception:
            return list(self._collections.keys())
