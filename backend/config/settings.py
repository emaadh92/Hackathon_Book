import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Configuration settings for the book embeddings pipeline."""

    # Cohere Configuration
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")

    # Qdrant Configuration
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")

    # Book Site URLs
    BOOK_SITE_URLS: List[str] = os.getenv(
        "BOOK_SITE_URLS", "https://example.com/docs"
    ).split(",")

    # Chunking Configuration
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1024"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "128"))

    # Qdrant Collection Name
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "book_embeddings")

    # Embedding Model
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "embed-multilingual-v3.0")

    # Validation
    @classmethod
    def validate(cls):
        """Validate that required settings are present."""
        errors = []

        if not cls.COHERE_API_KEY:
            errors.append("COHERE_API_KEY is required")

        if not cls.QDRANT_URL:
            errors.append("QDRANT_URL is required")

        if not cls.BOOK_SITE_URLS or cls.BOOK_SITE_URLS == [""]:
            errors.append("At least one BOOK_SITE_URLS is required")

        if cls.CHUNK_SIZE <= 0:
            errors.append("CHUNK_SIZE must be positive")

        if cls.CHUNK_OVERLAP < 0:
            errors.append("CHUNK_OVERLAP must be non-negative")

        if cls.CHUNK_SIZE <= cls.CHUNK_OVERLAP:
            errors.append("CHUNK_SIZE must be greater than CHUNK_OVERLAP")

        if errors:
            raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")


# Global settings instance
settings = Settings()