"""Example: Chatting with CSV datasets using RAGForge."""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.common import run_file_chat


def main():
    # Create a temporary sample CSV file if none exists
    csv_content = (
        "Project,Version,Status,Category\n"
        "RAGForge,1.0.0,Active,Framework\n"
        "ChromaDB,0.4.0,Active,VectorStore\n"
        "GroqInference,2.1.0,Active,LLM\n"
    )
    
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write(csv_content)
        temp_csv_path = f.name

    question = "What is the status and version of RAGForge?"
    print(f"Indexing sample CSV and asking: '{question}'...")

    try:
        result = run_file_chat(temp_csv_path, question)
        print("\n=== RAGForge Response ===")
        print(result["answer"])
    finally:
        if os.path.exists(temp_csv_path):
            os.remove(temp_csv_path)


if __name__ == "__main__":
    main()
