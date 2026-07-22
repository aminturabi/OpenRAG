from chunking.recursive_character import RecursiveCharacterChunker


def test_recursive_character_chunker_returns_overlapping_chunks():
    chunker = RecursiveCharacterChunker(chunk_size=10, overlap=2)
    chunks = chunker.chunk("abcdefghijklmnopqrstuvwxyz")
    assert chunks[0] == "abcdefghij"
    assert chunks[1].startswith("ij")
    assert len(chunks) >= 3

