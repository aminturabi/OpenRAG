"""CSV document loader plugin."""

import csv
import os
from typing import Any

from core.contracts import DocumentLoader
from core.registry import register_plugin


@register_plugin("loaders", "csv")
class CSVLoader(DocumentLoader):
    """Parses tabular CSV files into text rows."""

    def __init__(self, delimiter: str = ",", quotechar: str = '"') -> None:
        self.delimiter = delimiter
        self.quotechar = quotechar

    def load(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        lines = []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f, delimiter=self.delimiter, quotechar=self.quotechar)
            headers = None
            for row in reader:
                if not row:
                    continue
                if headers is None:
                    headers = row
                    continue
                row_str = ", ".join(f"{h}: {v}" for h, v in zip(headers, row))
                lines.append(row_str)

        return "\n".join(lines)
