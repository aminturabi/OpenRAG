"""Default recursive character chunking strategy."""

from core.contracts import ChunkingStrategy
from core.registry import register_plugin


@register_plugin("chunkers", "recursive_character")
class RecursiveCharacterChunker(ChunkingStrategy):
    def __init__(self, chunk_size: int = 1000, overlap: int = 150) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if overlap < 0:
            raise ValueError("overlap cannot be negative")
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        normalized = text.strip()
        if not normalized:
            return []

        chunks: list[str] = []
        start = 0
        size = len(normalized)
        while start < size:
            end = min(start + self.chunk_size, size)
            piece = normalized[start:end].strip()
            if piece:
                chunks.append(piece)
            if end == size:
                break
            start = end - self.overlap
        return chunks

