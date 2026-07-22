"""Example: Chatting with GitHub repository codebases using OpenRAG."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.container import build_service
from loaders.github_loader import GitHubRepoLoader


def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loader = GitHubRepoLoader(allowed_extensions=[".py", ".md"])
    print(f"Loading local codebase from {root_dir}...")
    
    codebase_text = loader.load(root_dir)
    print(f"Loaded {len(codebase_text)} characters of codebase documentation and code.")

    service = build_service()
    chunks = service.chunker.chunk(codebase_text)
    embeddings = service.embeddings.embed_many(chunks)
    ids = [f"code_chunk_{i}" for i in range(len(chunks))]
    col_name = "col_github_repo_sample"

    service.vectorstore.add_documents(col_name, chunks, embeddings, ids)

    question = "How are components registered in the OpenRAG plugin architecture?"
    print(f"Querying codebase: '{question}'...")
    
    result = service.query(col_name, question)
    print("\n=== OpenRAG Response ===")
    print(result["answer"])


if __name__ == "__main__":
    main()
