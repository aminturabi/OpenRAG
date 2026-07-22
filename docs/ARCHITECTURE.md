# OpenRAG Architectural Overview

**OpenRAG** is built around Clean Architecture and SOLID principles, fully decoupling delivery layers, business logic, and third-party integrations.

```
                    ┌─────────────────────────┐
                    │  Flask / REST / CLI /   │  (Delivery Layer)
                    │     Example Scripts     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       RAGService        │  (Application Service)
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┴───────────────────────┐
         │              Abstract Core Contracts          │  (Domain Interfaces)
         └───────┬───────┬───────┬───────┬───────┬───────┘
                 │       │       │       │       │
                 ▼       ▼       ▼       ▼       ▼
              Loaders Chunker Embed Vector  LLMs...       (Plugins Layer)
```

---

## 🏗️ Core Architectural Layers

1. **`core/contracts.py`**: Defines abstract interfaces (`DocumentLoader`, `ChunkingStrategy`, `EmbeddingModel`, `VectorStoreBackend`, `Retriever`, `Reranker`, `LLMProvider`, `OutputFormatter`).
2. **`core/registry.py`**: Global plugin registry enabling decoupled `@register_plugin` registrations.
3. **`core/container.py`**: Dependency wiring container reading component settings from `RAGConfig` or `config/default.json`.
4. **`core/service.py`**: `RAGService` orchestrates the indexing and querying pipeline lifecycle.
5. **`plugins/` & component packages**: Plug-and-play implementations (ChromaDB, FAISS, Qdrant, Pinecone, Groq, SentenceTransformers, CSV, Markdown, Web, YouTube).
6. **`api/` & `app.py`**: HTTP routing layer presenting backward-compatible Flask endpoints and serving static UI assets.
