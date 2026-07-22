# Changelog

All notable changes to the **RAGForge** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v1.0.0] - 2026-07-23

### Added
- Modular RAG core framework with abstract contracts (`DocumentLoader`, `ChunkingStrategy`, `EmbeddingModel`, `VectorStoreBackend`, `Retriever`, `Reranker`, `LLMProvider`, `OutputFormatter`).
- Dynamic plugin registry supporting simple `@register_plugin` decorators.
- Plug-and-play vector store support for ChromaDB, FAISS, Qdrant, and Pinecone.
- Expanded document loaders for CSV, Markdown, Web pages, YouTube transcripts, and GitHub repository codebases.
- Production-quality open-source governance files (`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `LICENSE`).
- Comprehensive GitHub Actions CI workflow for linting and test coverage.
- Interactive example suite for multi-modal document chat workflows.
- Maintained 100% backward compatibility with Flask backend and frontend UI.
