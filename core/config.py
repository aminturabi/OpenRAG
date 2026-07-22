"""Configuration models for the modular RAG framework."""

from dataclasses import dataclass, field


@dataclass(slots=True)
class ComponentConfig:
    name: str
    options: dict = field(default_factory=dict)


@dataclass(slots=True)
class RAGConfig:
    loader: ComponentConfig = field(default_factory=lambda: ComponentConfig("composite"))
    chunker: ComponentConfig = field(
        default_factory=lambda: ComponentConfig("recursive_character", {"chunk_size": 1000, "overlap": 150})
    )
    embeddings: ComponentConfig = field(
        default_factory=lambda: ComponentConfig("sentence_transformer", {"model_name": "all-MiniLM-L6-v2"})
    )
    vectorstore: ComponentConfig = field(default_factory=lambda: ComponentConfig("chroma"))
    retriever: ComponentConfig = field(default_factory=lambda: ComponentConfig("dense_retriever"))
    reranker: ComponentConfig = field(default_factory=lambda: ComponentConfig("noop"))
    llm: ComponentConfig = field(default_factory=lambda: ComponentConfig("groq", {"model_name": "openai/gpt-oss-120b"}))
    formatter: ComponentConfig = field(default_factory=lambda: ComponentConfig("default_json"))

