"""PDF loader implementation."""

from pypdf import PdfReader


class PDFLoader:
    def load(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        return "\n".join((page.extract_text() or "") for page in reader.pages)

