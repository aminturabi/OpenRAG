"""Markdown document loader plugin."""

import os

from core.contracts import DocumentLoader
from core.registry import register_plugin


@register_plugin("loaders", "markdown")
class MarkdownLoader(DocumentLoader):
    """Parses Markdown files into plain text."""

    def load(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Markdown file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()

        return content
