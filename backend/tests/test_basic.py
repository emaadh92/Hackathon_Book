"""
Basic tests for the book embeddings pipeline components.
"""
import pytest
from src.embeddings.text_chunker import TextChunker
from src.utils.validators import validate_text_content


def test_text_chunker_initialization():
    """Test that TextChunker initializes with valid parameters."""
    chunker = TextChunker(chunk_size=512, chunk_overlap=64)

    assert chunker.chunk_size == 512
    assert chunker.chunk_overlap == 64


def test_text_chunker_chunking():
    """Test that TextChunker can chunk text properly."""
    chunker = TextChunker(chunk_size=50, chunk_overlap=10)
    text = "This is a sample text for testing the chunking functionality. " * 3  # Repeat to make it longer
    url = "https://example.com/test"

    chunks = chunker.chunk_text(text, url)

    assert len(chunks) > 0
    for chunk in chunks:
        assert len(chunk.content) <= chunker.chunk_size or chunk.content == text[min(chunk.start_pos, len(text)):min(chunk.end_pos, len(text))]


def test_validate_text_content():
    """Test the text validation function."""
    # Valid content
    assert validate_text_content("This is a valid text with sufficient length.")

    # Invalid content (too short)
    assert not validate_text_content("Hi")

    # Invalid content (empty)
    assert not validate_text_content("")

    # Invalid content (None)
    assert not validate_text_content(None)


def test_text_chunker_update_settings():
    """Test that TextChunker can update settings dynamically."""
    chunker = TextChunker(chunk_size=512, chunk_overlap=64)

    # Update settings
    chunker.update_chunk_settings(chunk_size=256, chunk_overlap=32)

    assert chunker.chunk_size == 256
    assert chunker.chunk_overlap == 32


if __name__ == "__main__":
    pytest.main([__file__])