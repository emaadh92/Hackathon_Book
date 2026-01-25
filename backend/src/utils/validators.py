import re
from urllib.parse import urlparse
from typing import List, Union
import requests
from .helpers import get_logger

logger = get_logger(__name__)

def is_valid_url(url: str) -> bool:
    """
    Validate if a string is a properly formatted URL.

    Args:
        url: URL string to validate

    Returns:
        True if URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def is_docusaurus_site(url: str) -> bool:
    """
    Check if a URL appears to be a Docusaurus site by checking headers and content.

    Args:
        url: URL to check

    Returns:
        True if likely a Docusaurus site, False otherwise
    """
    try:
        response = requests.head(url, timeout=10)
        # Check for common Docusaurus indicators in headers
        server_header = response.headers.get('server', '').lower()
        if 'docusaurus' in server_header:
            return True

        # Additional check by fetching a small portion of the page
        response = requests.get(url, timeout=10)
        content = response.text.lower()

        # Look for common Docusaurus indicators in HTML
        docusaurus_indicators = [
            'docusaurus',
            'data-theme',
            'doc-sidebar',
            'doc-page',
            'navbar'
        ]

        return any(indicator in content for indicator in docusaurus_indicators)
    except Exception:
        # If we can't connect or check, assume it might be valid
        # and let the crawler handle the actual validation
        logger.warning(f"Could not verify if {url} is a Docusaurus site, assuming it is")
        return True


def validate_urls(urls: List[str]) -> List[str]:
    """
    Validate a list of URLs and return only the valid ones.

    Args:
        urls: List of URLs to validate

    Returns:
        List of valid URLs
    """
    valid_urls = []
    for url in urls:
        url = url.strip()  # Remove leading/trailing whitespace
        if is_valid_url(url):
            valid_urls.append(url)
        else:
            logger.warning(f"Invalid URL skipped: {url}")

    return valid_urls


def is_valid_embedding(embedding: Union[List[float], None]) -> bool:
    """
    Validate if an embedding is properly formatted.

    Args:
        embedding: Embedding vector to validate

    Returns:
        True if embedding is valid, False otherwise
    """
    if embedding is None:
        return False

    if not isinstance(embedding, list):
        return False

    if len(embedding) == 0:
        return False

    # Check that all elements are floats/numbers
    for value in embedding:
        if not isinstance(value, (int, float)):
            return False

    return True


def validate_chunk_size(chunk_size: int, max_size: int = 4096) -> bool:
    """
    Validate chunk size parameters.

    Args:
        chunk_size: Size of the chunk
        max_size: Maximum allowed size

    Returns:
        True if valid, False otherwise
    """
    return 0 < chunk_size <= max_size


def validate_overlap_params(chunk_size: int, overlap: int) -> bool:
    """
    Validate that overlap parameters are consistent.

    Args:
        chunk_size: Size of the chunk
        overlap: Overlap size

    Returns:
        True if valid, False otherwise
    """
    return 0 <= overlap < chunk_size


def validate_embedding_model(model_name: str) -> bool:
    """
    Validate if the embedding model name is supported.

    Args:
        model_name: Name of the embedding model

    Returns:
        True if valid, False otherwise
    """
    supported_models = [
        "embed-multilingual-v3.0",
        "embed-english-v3.0",
        "embed-multilingual-light-v3.0",
        "embed-english-light-v3.0",
        "large",
        "multilingual-22-12",
        "embed-english-v2.0"
    ]

    return model_name in supported_models


def validate_collection_name(name: str) -> bool:
    """
    Validate Qdrant collection name.

    Args:
        name: Collection name to validate

    Returns:
        True if valid, False otherwise
    """
    # Qdrant collection names must match this pattern
    pattern = r'^[a-zA-Z][a-zA-Z0-9_-]*$'
    return bool(re.match(pattern, name)) and 3 <= len(name) <= 63


def validate_api_key(api_key: str) -> bool:
    """
    Basic validation for API keys.

    Args:
        api_key: API key to validate

    Returns:
        True if valid, False otherwise
    """
    return bool(api_key and len(api_key.strip()) > 0)


def validate_text_content(text: str, min_length: int = 10) -> bool:
    """
    Validate text content for embedding.

    Args:
        text: Text content to validate
        min_length: Minimum length required

    Returns:
        True if valid, False otherwise
    """
    if not text:
        return False

    # Remove whitespace and check length
    clean_text = text.strip()
    return len(clean_text) >= min_length