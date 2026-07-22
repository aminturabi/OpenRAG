"""SentenceTransformers embedding plugin."""

from sentence_transformers import SentenceTransformer

from core.contracts import EmbeddingModel
from core.registry import register_plugin


@register_plugin("embeddings", "sentence_transformer")
class SentenceTransformerEmbeddings(EmbeddingModel):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        self._model: SentenceTransformer | None = None

    def _get_model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed(self, text: str) -> list[float]:
        return self._get_model().encode(text, show_progress_bar=False).tolist()

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        return self._get_model().encode(texts, show_progress_bar=False).tolist()

