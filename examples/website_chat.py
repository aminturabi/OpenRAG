"""Example: Chatting with Website content using OpenRAG."""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.container import build_service
from loaders.web_loader import WebLoader


def main():
    # Demonstrating WebLoader parsing an HTML structure
    html_sample = """
    <html>
        <head><title>OpenRAG Modular Framework</title></head>
        <body>
            <h1>Welcome to OpenRAG</h1>
            <p>OpenRAG is an open-source framework for building modular Retrieval-Augmented Generation systems.</p>
            <p>It supports customizable vector stores including ChromaDB, FAISS, Qdrant, and Pinecone.</p>
        </body>
    </html>
    """
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html_sample)
        temp_html_path = f.name

    question = "Which vector stores are supported by OpenRAG?"
    print(f"Indexing web content and asking: '{question}'...")

    try:
        service = build_service()
        idx_res = service.index_document(temp_html_path, "sample_website.html")
        result = service.query(idx_res["collection_name"], question)

        print("\n=== OpenRAG Response ===")
        print(result["answer"])
    finally:
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)


if __name__ == "__main__":
    main()
