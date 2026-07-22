"""Backward-compatible retriever adapter."""

from rag.embeddings import EmbeddingManager
from rag.vector_store import VectorStore
from retrievers.vector_retriever import DenseVectorRetriever


class _EmbeddingAdapter:
    def __init__(self, manager: EmbeddingManager) -> None:
        self.manager = manager

    def embed(self, text: str) -> list[float]:
        return self.manager.get_embedding(text)


class RAGRetriever(DenseVectorRetriever):
    def __init__(self, vector_store: VectorStore | None = None, embedding_manager: EmbeddingManager | None = None):
        store = vector_store or VectorStore()
        manager = embedding_manager or EmbeddingManager()
        super().__init__(vector_store=store, embedding_model=_EmbeddingAdapter(manager))
