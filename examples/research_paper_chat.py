"""Example: Chatting with Research Papers using OpenRAG."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.common import run_file_chat


def main():
    sample_pdf = os.path.join(os.path.dirname(__file__), "sample.pdf")
    question = "What methodology and key findings are presented in this research paper?"

    if not os.path.exists(sample_pdf):
        print(f"Sample research paper not found at {sample_pdf}. Provide a research paper PDF file to run.")
        return

    print(f"Indexing research paper '{sample_pdf}' and asking: '{question}'...")
    try:
        result = run_file_chat(sample_pdf, question)
        print("\n=== OpenRAG Response ===")
        print(result["answer"])
    except Exception as e:
        print(f"Error during research paper chat execution: {e}")


if __name__ == "__main__":
    main()
