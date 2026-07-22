"""FAISS vector store plugin for OpenRAG."""

import os
import pickle
from typing import Dict, List, Any

from core.contracts import VectorStoreBackend
from core.registry import register_plugin
from core.exceptions import PluginDependencyError

try:
    import faiss
    import numpy as np
    FAISS_AVAILABLE = True
except ImportError:
    try:
        import numpy as np
        FAISS_AVAILABLE = "numpy_only"
    except ImportError:
        FAISS_AVAILABLE = False


@register_plugin("vectorstores", "faiss")
class FaissVectorStore(VectorStoreBackend):
    """FAISS-backed vector store implementation with optional numpy fallback."""

    def __init__(self, persist_directory: str | None = None) -> None:
        if FAISS_AVAILABLE is False:
            raise PluginDependencyError(
                "FAISS plugin requires 'numpy' or 'faiss-cpu'. Please install via: pip install faiss-cpu numpy"
            )
        
        if persist_directory is None:
            root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            persist_directory = os.path.join(root, "data", "faiss_store")
        
        os.makedirs(persist_directory, exist_ok=True)
        self.persist_directory = persist_directory
        self._collections: Dict[str, Dict[str, Any]] = {}
        self._load_store()

    def _get_store_path(self, collection_name: str) -> str:
        clean_name = "".join(ch for ch in collection_name if ch.isalnum() or ch in ["_", "-"])
        return os.path.join(self.persist_directory, f"{clean_name}.pkl")

    def _load_store(self) -> None:
        if not os.path.exists(self.persist_directory):
            return
        for file_name in os.listdir(self.persist_directory):
            if file_name.endswith(".pkl"):
                col_name = file_name[:-4]
                file_path = os.path.join(self.persist_directory, file_name)
                try:
                    with open(file_path, "rb") as f:
                        self._collections[col_name] = pickle.load(f)
                except Exception:
                    pass

    def _save_collection(self, collection_name: str) -> None:
        file_path = self._get_store_path(collection_name)
        with open(file_path, "wb") as f:
            pickle.dump(self._collections.get(collection_name, {}), f)

    def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        embeddings: List[List[float]],
        ids: List[str],
    ) -> None:
        if not documents or not embeddings:
            return

        if collection_name not in self._collections:
            self._collections[collection_name] = {"documents": [], "embeddings": [], "ids": []}

        col = self._collections[collection_name]
        col["documents"].extend(documents)
        col["embeddings"].extend(embeddings)
        col["ids"].extend(ids)
        self._save_collection(collection_name)

    def query(self, collection_name: str, query_embeddings: List[List[float]], n_results: int = 4) -> List[str]:
        if collection_name not in self._collections or not query_embeddings:
            return []

        col = self._collections[collection_name]
        doc_embeddings = col["embeddings"]
        documents = col["documents"]

        if not doc_embeddings or not documents:
            return []

        q_vec = np.array(query_embeddings[0], dtype=np.float32)
        doc_vecs = np.array(doc_embeddings, dtype=np.float32)

        if FAISS_AVAILABLE is True:
            dimension = doc_vecs.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(doc_vecs)
            distances, indices = index.search(np.array([q_vec]), min(n_results, len(documents)))
            results = []
            for idx in indices[0]:
                if 0 <= idx < len(documents):
                    results.append(documents[idx])
            return results
        else:
            # Numpy fallback using dot product / cosine distance
            q_norm = q_vec / (np.linalg.norm(q_vec) + 1e-10)
            doc_norms = doc_vecs / (np.linalg.norm(doc_vecs, axis=1, keepdims=True) + 1e-10)
            scores = np.dot(doc_norms, q_norm)
            top_indices = np.argsort(scores)[::-1][:n_results]
            return [documents[idx] for idx in top_indices if idx < len(documents)]

    def delete_collection(self, collection_name: str) -> bool:
        if collection_name in self._collections:
            del self._collections[collection_name]
            file_path = self._get_store_path(collection_name)
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        return False

    def list_collections(self) -> List[str]:
        return list(self._collections.keys())
