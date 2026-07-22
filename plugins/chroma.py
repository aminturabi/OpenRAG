"""Chroma plugin alias."""

from core.registry import register_plugin
from vectorstores.chroma_store import ChromaVectorStore


@register_plugin("vectorstores", "chromadb")
class ChromaDBAliasStore(ChromaVectorStore):
    """Alias plugin so contributors can discover vectorstore registration pattern."""

