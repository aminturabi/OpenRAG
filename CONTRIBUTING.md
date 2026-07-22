# Contributing to OpenRAG

Thank you for your interest in contributing to **OpenRAG**! We welcome contributions from developers of all experience levels around the world.

---

## 🌟 How Can You Contribute?

You can contribute to OpenRAG in many ways:
- **Add New Plugins**: Create new document loaders, vector stores, chunking strategies, embeddings, or LLM providers under `plugins/` or component directories.
- **Improve Documentation**: Enhance docstrings, write new guides, or refine existing documentation.
- **Fix Bugs**: Find open issues marked `bug` and submit a Pull Request.
- **Good First Issues**: Check out [docs/GOOD_FIRST_ISSUES.md](docs/GOOD_FIRST_ISSUES.md) for beginner-friendly tasks.

---

## 🛠️ Development Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/aminturabi/OpenRAG.git
   cd OpenRAG
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov
   ```

4. **Run Unit Tests**
   ```bash
   python -m pytest
   ```

---

## 🧩 Adding a New Plugin

Adding a plugin to OpenRAG is as simple as creating a single file:

1. Inherit from the appropriate contract in `core/contracts.py`:
   ```python
   from core.contracts import VectorStoreBackend
   from core.registry import register_plugin

   @register_plugin("vectorstores", "my_custom_store")
   class MyCustomVectorStore(VectorStoreBackend):
       def __init__(self, **kwargs):
           ...
   ```
2. Implement all abstract methods required by the interface.
3. If third-party dependencies are required, handle missing packages gracefully:
   ```python
   from core.exceptions import PluginDependencyError

   try:
       import custom_lib
   except ImportError:
       raise PluginDependencyError("MyCustomVectorStore requires 'custom_lib'. Install via pip install custom_lib")
   ```
4. Add a unit test under `tests/` verifying your plugin instantiation and behavior.

---

## 📝 Pull Request Checklist

Before submitting a Pull Request, please ensure:
- [ ] Code follows PEP 8 styling conventions.
- [ ] Type hints and docstrings are added for all public methods.
- [ ] New features include corresponding unit tests under `tests/`.
- [ ] All tests pass via `python -m pytest`.
- [ ] Commits have clear, descriptive titles.

---

## 💬 Community & Discussions

Have architectural questions or ideas for new plugins? Start a thread on [GitHub Discussions](docs/GITHUB_DISCUSSIONS_GUIDE.md)!
