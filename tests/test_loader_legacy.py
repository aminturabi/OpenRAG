from pathlib import Path

from loaders.document_loader import load_document, split_into_chunks


def test_load_document_txt(tmp_path: Path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello world", encoding="utf-8")
    assert load_document(str(file_path)) == "hello world"


def test_split_into_chunks_legacy_wrapper():
    chunks = split_into_chunks("abcdefghijk", chunk_size=5, overlap=1)
    assert chunks[0] == "abcde"
    assert chunks[1].startswith("e")

