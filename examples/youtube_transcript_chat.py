"""Example: Chatting with YouTube transcripts using RAGForge."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.container import build_service
from loaders.youtube_loader import YouTubeTranscriptLoader


def main():
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    loader = YouTubeTranscriptLoader()
    print(f"Loading transcript for video URL '{video_url}'...")

    transcript_text = loader.load(video_url)
    service = build_service()

    chunks = service.chunker.chunk(transcript_text)
    embeddings = service.embeddings.embed_many(chunks)
    ids = [f"yt_chunk_{i}" for i in range(len(chunks))]
    col_name = "col_youtube_transcript_sample"

    service.vectorstore.add_documents(col_name, chunks, embeddings, ids)

    question = "What topics are discussed in this video transcript?"
    print(f"Querying transcript: '{question}'...")

    result = service.query(col_name, question)
    print("\n=== RAGForge Response ===")
    print(result["answer"])


if __name__ == "__main__":
    main()
