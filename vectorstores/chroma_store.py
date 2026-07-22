"""ChromaDB vector store plugin."""

import os

import chromadb

from core.contracts import VectorStoreBackend
from core.registry import register_plugin


@register_plugin("vectorstores", "chroma")
class ChromaVectorStore(VectorStoreBackend):
    def __init__(self, persist_directory: str | None = None) -> None:
        if persist_directory is None:
            root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            persist_directory = os.path.join(root, "data", "vector_store")
        os.makedirs(persist_directory, exist_ok=True)
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)

    @staticmethod
    def normalize_collection_name(name: str) -> str:
        clean_name = "".join(ch for ch in name if ch.isalnum() or ch in ["_", "-"])
        if len(clean_name) < 3:
            clean_name = f"col_{clean_name}"
        return clean_name[:63]

    def get_or_create_collection(self, name: str):
        return self.client.get_or_create_collection(self.normalize_collection_name(name))

    def add_documents(
        self,
        collection_name: str,
        documents: list[str],
        embeddings: list[list[float]],
        ids: list[str],
    ) -> None:
        if not documents:
            return
        collection = self.get_or_create_collection(collection_name)
        collection.add(ids=ids, documents=documents, embeddings=embeddings)

    def query(self, collection_name: str, query_embeddings: list[list[float]], n_results: int = 4) -> list[str]:
        try:
            collection = self.client.get_collection(self.normalize_collection_name(collection_name))
        except Exception:
            return []

        results = collection.query(query_embeddings=query_embeddings, n_results=n_results)
        if results and "documents" in results and results["documents"]:
            return results["documents"][0]
        return []

    def delete_collection(self, collection_name: str) -> bool:
        try:
            self.client.delete_collection(self.normalize_collection_name(collection_name))
            return True
        except Exception:
            return False

    def list_collections(self) -> list[str]:
        return [col.name for col in self.client.list_collections()]

