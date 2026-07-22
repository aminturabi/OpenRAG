"""Application service coordinating the RAG flow."""

import logging
import os
import uuid

from core.contracts import (
    ChunkingStrategy,
    DocumentLoader,
    EmbeddingModel,
    LLMProvider,
    OutputFormatter,
    Reranker,
    Retriever,
    VectorStoreBackend,
)
from core.exceptions import DocumentLoadError

logger = logging.getLogger(__name__)


class RAGService:
    """Use-case service for indexing and querying documents."""

    def __init__(
        self,
        loader: DocumentLoader,
        chunker: ChunkingStrategy,
        embeddings: EmbeddingModel,
        vectorstore: VectorStoreBackend,
        retriever: Retriever,
        reranker: Reranker,
        llm: LLMProvider,
        formatter: OutputFormatter,
    ) -> None:
        self.loader = loader
        self.chunker = chunker
        self.embeddings = embeddings
        self.vectorstore = vectorstore
        self.retriever = retriever
        self.reranker = reranker
        self.llm = llm
        self.formatter = formatter

    @staticmethod
    def build_collection_name(filename: str, file_id: str) -> str:
        clean_base = "".join(ch for ch in filename if ch.isalnum() or ch in ["_", "-"])
        return f"col_{file_id[:8]}_{clean_base[:30]}"

    def index_document(self, file_path: str, original_filename: str) -> dict:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        text = self.loader.load(file_path)
        if not text.strip():
            raise DocumentLoadError("No extractable text found in this document.")

        chunks = self.chunker.chunk(text)
        if not chunks:
            raise DocumentLoadError("Document was too short or could not be chunked.")

        file_id = str(uuid.uuid4())
        collection_name = self.build_collection_name(original_filename, file_id)
        embeddings = self.embeddings.embed_many(chunks)
        ids = [f"{file_id}_chunk_{idx}" for idx in range(len(chunks))]
        self.vectorstore.add_documents(collection_name, chunks, embeddings, ids)

        logger.info("Indexed document %s into %s (%d chunks)", original_filename, collection_name, len(chunks))
        return {
            "filename": original_filename,
            "collection_name": collection_name,
            "chunks_count": len(chunks),
        }

    def query(self, collection_name: str, query: str, top_k: int = 4, api_key: str | None = None) -> dict:
        candidates = self.retriever.retrieve(collection_name=collection_name, query=query, top_k=top_k)
        if not candidates:
            return self.formatter.format(
                "I couldn't retrieve any relevant information from the document to answer your question.", []
            )

        reranked = self.reranker.rerank(query=query, candidates=candidates, top_k=top_k)
        answer = self.llm.generate(question=query, context_chunks=reranked, api_key=api_key)
        return self.formatter.format(answer, reranked)

    def list_collections(self) -> list[str]:
        return self.vectorstore.list_collections()

    def clear_collection(self, collection_name: str) -> bool:
        return self.vectorstore.delete_collection(collection_name)
