from pathlib import Path
from loaders.csv_loader import CSVLoader
from loaders.markdown_loader import MarkdownLoader
from loaders.web_loader import WebLoader
from loaders.youtube_loader import YouTubeTranscriptLoader


def test_csv_loader(tmp_path: Path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("Name,Role\nAlice,Architect\nBob,Developer", encoding="utf-8")
    loader = CSVLoader()
    text = loader.load(str(csv_file))
    assert "Name: Alice" in text
    assert "Role: Architect" in text
    assert "Name: Bob" in text


def test_markdown_loader(tmp_path: Path):
    md_file = tmp_path / "doc.md"
    md_file.write_text("# OpenRAG\n\nModular RAG Framework.", encoding="utf-8")
    loader = MarkdownLoader()
    text = loader.load(str(md_file))
    assert "# OpenRAG" in text
    assert "Modular RAG Framework." in text


def test_web_loader_local(tmp_path: Path):
    html_file = tmp_path / "page.html"
    html_file.write_text("<html><body><h1>Hello World</h1><script>alert(1);</script></body></html>", encoding="utf-8")
    loader = WebLoader()
    text = loader.load(str(html_file))
    assert "Hello World" in text
    assert "alert" not in text


def test_youtube_loader_extract_id():
    loader = YouTubeTranscriptLoader()
    vid_id = loader.extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert vid_id == "dQw4w9WgXcQ"
