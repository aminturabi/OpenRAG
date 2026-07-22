"""Example: Chatting with PDF documents using OpenRAG."""

import os
import sys

# Ensure root directory is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.common import run_file_chat


def main():
    sample_pdf = os.path.join(os.path.dirname(__file__), "sample.pdf")
    if not os.path.exists(sample_pdf):
        print(f"Sample PDF not found at {sample_pdf}. Please specify a valid PDF file path.")
        return

    question = "What is the main summary of this PDF document?"
    print(f"Indexing '{sample_pdf}' and asking: '{question}'...")
    
    try:
        result = run_file_chat(sample_pdf, question)
        print("\n=== OpenRAG Response ===")
        print(result["answer"])
        print("\n=== Context Grounding ===")
        for i, ctx in enumerate(result.get("context", []), 1):
            print(f"[{i}] {ctx[:150]}...")
    except Exception as e:
        print(f"Error during PDF chat execution: {e}")


if __name__ == "__main__":
    main()
