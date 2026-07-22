"""Abstract contracts for replaceable RAG components."""

from abc import ABC, abstractmethod


class DocumentLoader(ABC):
    @abstractmethod
    def load(self, file_path: str) -> str:
        """Load and normalize text from a source."""


class ChunkingStrategy(ABC):
    @abstractmethod
    def chunk(self, text: str) -> list[str]:
        """Split text into chunks."""


class EmbeddingModel(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Embed a single text."""

    @abstractmethod
    def embed_many(self, texts: list[str]) -> list[list[float]]:
        """Embed many texts."""


class VectorStoreBackend(ABC):
    @abstractmethod
    def add_documents(
        self,
        collection_name: str,
        documents: list[str],
        embeddings: list[list[float]],
        ids: list[str],
    ) -> None:
        """Store document vectors."""

    @abstractmethod
    def query(self, collection_name: str, query_embeddings: list[list[float]], n_results: int = 4) -> list[str]:
        """Query nearest documents."""

    @abstractmethod
    def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection."""

    @abstractmethod
    def list_collections(self) -> list[str]:
        """List collections."""


class Retriever(ABC):
    @abstractmethod
    def retrieve(self, collection_name: str, query: str, top_k: int = 4) -> list[str]:
        """Retrieve candidate context chunks."""


class Reranker(ABC):
    @abstractmethod
    def rerank(self, query: str, candidates: list[str], top_k: int) -> list[str]:
        """Rerank candidates."""


class LLMProvider(ABC):
    @abstractmethod
    def generate(
        self,
        question: str,
        context_chunks: list[str],
        model_name: str | None = None,
        api_key: str | None = None,
    ) -> str:
        """Generate answer from question and context."""


class OutputFormatter(ABC):
    @abstractmethod
    def format(self, answer: str, context_chunks: list[str]) -> dict:
        """Format response payload."""
