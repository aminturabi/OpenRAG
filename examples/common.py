"""Reusable example runner for OpenRAG."""

import os
from core.container import build_service


def run_file_chat(file_path: str, question: str) -> dict:
    service = build_service()
    filename = os.path.basename(file_path)
    index_result = service.index_document(file_path=file_path, original_filename=filename)
    return service.query(collection_name=index_result["collection_name"], query=question, top_k=4)
