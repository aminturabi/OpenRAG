"""Pinecone vector store plugin for RAGForge."""

import os
from typing import List, Any

from core.contracts import VectorStoreBackend
from core.registry import register_plugin
from core.exceptions import PluginDependencyError, VectorStoreError

try:
    import pinecone
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False


@register_plugin("vectorstores", "pinecone")
class PineconeVectorStore(VectorStoreBackend):
    """Pinecone-backed vector store plugin for cloud vector database indexing."""

    def __init__(self, api_key: str | None = None, environment: str | None = None, **kwargs: Any) -> None:
        if not PINECONE_AVAILABLE:
            raise PluginDependencyError(
                "Pinecone plugin requires 'pinecone-client'. Please install it using: pip install pinecone-client"
            )

        resolved_api_key = api_key or os.environ.get("PINECONE_API_KEY")
        if not resolved_api_key:
            raise VectorStoreError("Pinecone API key is required. Set PINECONE_API_KEY in your environment.")

        self.pc = pinecone.Pinecone(api_key=resolved_api_key, **kwargs)

    def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        embeddings: List[List[float]],
        ids: List[str],
    ) -> None:
        if not documents or not embeddings:
            return

        index = self.pc.Index(collection_name)
        vectors = [
            {"id": doc_id, "values": emb, "metadata": {"text": doc}}
            for doc_id, emb, doc in zip(ids, embeddings, documents)
        ]
        index.upsert(vectors=vectors)

    def query(self, collection_name: str, query_embeddings: List[List[float]], n_results: int = 4) -> List[str]:
        if not query_embeddings:
            return []

        try:
            index = self.pc.Index(collection_name)
            res = index.query(vector=query_embeddings[0], top_k=n_results, include_metadata=True)
            matches = res.get("matches", [])
            return [m.get("metadata", {}).get("text", "") for m in matches if m.get("metadata")]
        except Exception:
            return []

    def delete_collection(self, collection_name: str) -> bool:
        try:
            self.pc.delete_index(collection_name)
            return True
        except Exception:
            return False

    def list_collections(self) -> List[str]:
        try:
            return [idx.name for idx in self.pc.list_indexes()]
        except Exception:
            return []
