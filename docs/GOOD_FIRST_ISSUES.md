# Good First Issues for Contributors

Welcome! Below is a curated list of beginner-friendly tasks designed for developers looking to make their first contribution to **RAGForge**.

---

### 1. Add DOCX Loader Plugin
- **Category**: `loaders`
- **Target File**: `loaders/docx_loader.py`
- **Goal**: Implement `DOCXLoader(DocumentLoader)` using `python-docx` to extract text from Microsoft Word `.docx` documents.
- **Contract**: Inherit from `DocumentLoader` in `core/contracts.py`.
- **Registration**: Add `@register_plugin("loaders", "docx")`.

---

### 2. Add EPUB Loader Plugin
- **Category**: `loaders`
- **Target File**: `loaders/epub_loader.py`
- **Goal**: Create an ebook parser using `ebooklib` to extract chapter contents from `.epub` files.
- **Registration**: Add `@register_plugin("loaders", "epub")`.

---

### 3. Add Hybrid Search Retriever (Dense + Keyword BM25)
- **Category**: `retrievers`
- **Target File**: `retrievers/hybrid_retriever.py`
- **Goal**: Combine dense vector retrieval with reciprocal rank fusion (RRF) over BM25 keyword scores.
- **Contract**: Inherit from `Retriever` in `core/contracts.py`.

---

### 4. Add Ollama Local LLM Provider
- **Category**: `llms`
- **Target File**: `llms/ollama_provider.py`
- **Goal**: Allow running fully offline LLMs using Ollama's local HTTP REST API (`http://localhost:11434`).
- **Contract**: Inherit from `LLMProvider` in `core/contracts.py`.

---

### 5. Add CoHERE Reranker Plugin
- **Category**: `rerankers`
- **Target File**: `rerankers/cohere_reranker.py`
- **Goal**: Integrate Cohere's rerank API (`cohere.Client.rerank`) to re-score candidate context passages before generation.
- **Contract**: Inherit from `Reranker` in `core/contracts.py`.

---

### 6. Add Unit Tests for Plugin Error Handling
- **Category**: `tests`
- **Target File**: `tests/test_plugin_errors.py`
- **Goal**: Expand pytest suite to verify that `PluginNotFoundError` and `PluginDependencyError` are raised under improper configurations.
