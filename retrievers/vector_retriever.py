"""Dense vector retriever."""

from core.contracts import EmbeddingModel, Retriever, VectorStoreBackend
from core.registry import register_plugin


@register_plugin("retrievers", "dense_retriever")
class DenseVectorRetriever(Retriever):
    def __init__(self, vector_store: VectorStoreBackend, embedding_model: EmbeddingModel) -> None:
        self.vector_store = vector_store
        self.embedding_model = embedding_model

    def retrieve(self, collection_name: str, query: str, top_k: int = 4) -> list[str]:
        if not query.strip():
            return []
        query_embedding = self.embedding_model.embed(query)
        return self.vector_store.query(collection_name, [query_embedding], n_results=top_k)

