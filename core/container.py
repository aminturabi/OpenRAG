"""Dependency wiring for default framework runtime."""

from core.config import RAGConfig
from core.registry import create_plugin
from core.service import RAGService
from plugins import discover_plugins


def build_service(config: RAGConfig | None = None) -> RAGService:
    cfg = config or RAGConfig()

    discover_plugins()

    loader = create_plugin("loaders", cfg.loader.name, **cfg.loader.options)
    chunker = create_plugin("chunkers", cfg.chunker.name, **cfg.chunker.options)
    embeddings = create_plugin("embeddings", cfg.embeddings.name, **cfg.embeddings.options)
    vectorstore = create_plugin("vectorstores", cfg.vectorstore.name, **cfg.vectorstore.options)
    retriever = create_plugin(
        "retrievers",
        cfg.retriever.name,
        vector_store=vectorstore,
        embedding_model=embeddings,
        **cfg.retriever.options,
    )
    reranker = create_plugin("rerankers", cfg.reranker.name, **cfg.reranker.options)
    llm = create_plugin("llms", cfg.llm.name, **cfg.llm.options)
    formatter = create_plugin("formatters", cfg.formatter.name, **cfg.formatter.options)

    return RAGService(
        loader=loader,
        chunker=chunker,
        embeddings=embeddings,
        vectorstore=vectorstore,
        retriever=retriever,
        reranker=reranker,
        llm=llm,
        formatter=formatter,
    )

