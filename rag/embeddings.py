"""Backward-compatible embeddings adapter."""

from embeddings.sentence_transformer import SentenceTransformerEmbeddings


class EmbeddingManager:
    _instance = None

    def __new__(cls, model_name: str = "all-MiniLM-L6-v2"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._embedding_model = SentenceTransformerEmbeddings(model_name=model_name)
        return cls._instance

    def get_embedding(self, text: str) -> list[float]:
        return self._embedding_model.embed(text)

    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        return self._embedding_model.embed_many(texts)
