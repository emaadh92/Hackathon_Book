"""
Test configuration for the book embeddings pipeline.
"""
import pytest
import os
from unittest.mock import Mock


@pytest.fixture
def sample_text():
    """Provide sample text for testing."""
    return """
    This is a sample text for testing the embedding pipeline.
    It contains multiple sentences to test various aspects of the system.
    The text should be long enough to be chunked properly.
    """


@pytest.fixture
def sample_url():
    """Provide a sample URL for testing."""
    return "https://example.com/test-page"


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    class MockSettings:
        COHERE_API_KEY = "test-key"
        QDRANT_URL = "http://localhost:6333"
        QDRANT_API_KEY = "test-key"
        BOOK_SITE_URLS = ["https://example.com/docs"]
        CHUNK_SIZE = 512
        CHUNK_OVERLAP = 64
        COLLECTION_NAME = "test_embeddings"
        EMBEDDING_MODEL = "embed-multilingual-v3.0"

        @classmethod
        def validate(cls):
            pass

    return MockSettings()


@pytest.fixture
def mock_cohere_client():
    """Mock Cohere client for testing."""
    mock_client = Mock()
    mock_client.embed.return_value = Mock()
    mock_client.embed.return_value.embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    return mock_client