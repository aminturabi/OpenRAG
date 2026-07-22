"""Example: Chatting with Markdown documentation using OpenRAG."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.common import run_file_chat


def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_md = os.path.join(root_dir, "README.md")
    question = "What are the core features of OpenRAG?"

    print(f"Indexing '{target_md}' and asking: '{question}'...")
    try:
        result = run_file_chat(target_md, question)
        print("\n=== OpenRAG Response ===")
        print(result["answer"])
    except Exception as e:
        print(f"Error during Markdown chat execution: {e}")


if __name__ == "__main__":
    main()
