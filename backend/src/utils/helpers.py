import hashlib
import time
import uuid
from typing import Dict, Any, Optional
import logging

def generate_chunk_id(url: str, start_pos: int, end_pos: int) -> str:
    """
    Generate a unique chunk ID based on URL and position.

    Args:
        url: The source URL
        start_pos: Starting position in the content
        end_pos: Ending position in the content

    Returns:
        Unique chunk ID
    """
    content_hash = hashlib.md5(f"{url}_{start_pos}_{end_pos}".encode()).hexdigest()[:12]
    return f"chunk_{content_hash}"


def generate_vector_id(chunk_id: str) -> str:
    """
    Generate a unique vector ID based on chunk ID.

    Args:
        chunk_id: The chunk ID

    Returns:
        Unique vector ID
    """
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk_id))


def retry_on_failure(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator to retry a function on failure with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries
        backoff: Multiplier for delay after each retry
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay

            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        raise e

                    logging.warning(f"Attempt {retries} failed: {str(e)}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff

            return None
        return wrapper
    return decorator


def calculate_similarity_threshold(embedding_size: int) -> float:
    """
    Calculate an appropriate similarity threshold based on embedding size.

    Args:
        embedding_size: Size of the embedding vector

    Returns:
        Appropriate similarity threshold
    """
    # For larger embeddings, we typically need a higher threshold
    if embedding_size >= 2048:
        return 0.75
    elif embedding_size >= 1024:
        return 0.70
    else:
        return 0.65


def sanitize_text(text: str) -> str:
    """
    Sanitize text by removing extra whitespace and normalizing.

    Args:
        text: Raw text to sanitize

    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove special characters that might cause issues
    text = text.replace('\x00', '')  # Remove null bytes
    return text.strip()


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Logger name
        level: Logging level

    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding handlers multiple times
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger