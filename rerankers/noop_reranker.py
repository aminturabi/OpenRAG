"""Pass-through reranker."""

from core.contracts import Reranker
from core.registry import register_plugin


@register_plugin("rerankers", "noop")
class NoOpReranker(Reranker):
    def rerank(self, query: str, candidates: list[str], top_k: int) -> list[str]:
        return candidates[:top_k]

