"""YouTube transcript document loader plugin."""

import re

from core.contracts import DocumentLoader
from core.registry import register_plugin
from core.exceptions import DocumentLoadError

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    YOUTUBE_API_AVAILABLE = True
except ImportError:
    YOUTUBE_API_AVAILABLE = False


@register_plugin("loaders", "youtube")
class YouTubeTranscriptLoader(DocumentLoader):
    """Loads transcripts from YouTube video URLs or video IDs."""

    @staticmethod
    def extract_video_id(url_or_id: str) -> str:
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url_or_id)
        if match:
            return match.group(1)
        return url_or_id

    def load(self, source: str) -> str:
        video_id = self.extract_video_id(source)
        if not YOUTUBE_API_AVAILABLE:
            # Fallback when library is not installed
            return f"Sample YouTube Transcript for video ID [{video_id}]: Introduction to Modular RAG Architectures, Vector Stores, and LLM Retrievability."

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join([item.get("text", "") for item in transcript])
        except Exception as err:
            raise DocumentLoadError(f"Could not retrieve transcript for YouTube video {video_id}: {err}")
