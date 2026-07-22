"""GitHub Repository and codebase loader plugin."""

import os
from typing import List

from core.contracts import DocumentLoader
from core.registry import register_plugin


@register_plugin("loaders", "github")
class GitHubRepoLoader(DocumentLoader):
    """Loads source code files from a local repository directory or file tree."""

    def __init__(self, allowed_extensions: List[str] | None = None) -> None:
        self.allowed_extensions = set(allowed_extensions or [".py", ".md", ".json", ".txt", ".js", ".css", ".html"])

    def load(self, repo_path: str) -> str:
        if not os.path.exists(repo_path):
            raise FileNotFoundError(f"Repository directory not found: {repo_path}")

        extracted_files = []
        for root, dirs, files in os.walk(repo_path):
            # Ignore hidden folders like .git
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in self.allowed_extensions:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, repo_path)
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            extracted_files.append(f"=== File: {rel_path} ===\n{content}")
                    except Exception:
                        pass

        return "\n\n".join(extracted_files)
