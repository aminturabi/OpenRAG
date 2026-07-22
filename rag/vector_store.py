"""Backward-compatible vector store adapter."""

from vectorstores.chroma_store import ChromaVectorStore


class VectorStore(ChromaVectorStore):
    """Legacy class alias preserving previous public API."""
