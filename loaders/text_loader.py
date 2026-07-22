"""Text-like file loader."""


class TextLoader:
    def load(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            return file.read()

