import cohere
from typing import List, Dict, Optional, Union
import logging
from ..utils.helpers import retry_on_failure, get_logger
from ..utils.validators import is_valid_embedding, validate_embedding_model
from ..storage.models import EmbeddingVector
from ..crawlers.html_parser import HTMLParser

logger = get_logger(__name__)


class CohereClient:
    """
    Client for interacting with Cohere's embedding API.
    """

    def __init__(self, api_key: str, model: str = "embed-multilingual-v3.0"):
        """
        Initialize the Cohere client.

        Args:
            api_key: Cohere API key
            model: Embedding model to use
        """
        if not api_key:
            raise ValueError("Cohere API key is required")

        if not validate_embedding_model(model):
            raise ValueError(f"Invalid embedding model: {model}")

        self.client = cohere.Client(api_key)
        self.model = model

    @retry_on_failure(max_retries=3, delay=1.0, backoff=2.0)
    def generate_embeddings(
        self,
        texts: List[str],
        truncate: str = "END",
        input_type: str = "search_document"
    ) -> List[EmbeddingVector]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of texts to embed
            truncate: How to handle texts longer than the maximum length ('START', 'END', or 'NONE')
            input_type: Type of input for the model ('search_document', 'search_query', 'classification', 'clustering')

        Returns:
            List of EmbeddingVector objects
        """
        if not texts:
            return []

        logger.info(f"Generating embeddings for {len(texts)} texts using model: {self.model}")

        try:
            # Call Cohere API to generate embeddings
            response = self.client.embed(
                texts=texts,
                model=self.model,
                truncate=truncate,
                input_type=input_type
            )

            embeddings = response.embeddings
            embedding_size = len(embeddings[0]) if embeddings else 0

            embedding_vectors = []
            for i, embedding in enumerate(embeddings):
                if not is_valid_embedding(embedding):
                    logger.warning(f"Invalid embedding received for text {i}")
                    continue

                # Generate a unique vector ID
                chunk_id = f"text_chunk_{i}"
                vector_id = f"{chunk_id}_emb_{hash(str(embedding)[:10])}"

                embedding_vector = EmbeddingVector(
                    vector_id=vector_id,
                    chunk_id=chunk_id,
                    embedding=embedding,
                    size=embedding_size
                )

                embedding_vectors.append(embedding_vector)

            logger.info(f"Successfully generated {len(embedding_vectors)} embeddings")
            return embedding_vectors

        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    @retry_on_failure(max_retries=3, delay=1.0, backoff=2.0)
    def generate_single_embedding(
        self,
        text: str,
        truncate: str = "END",
        input_type: str = "search_document"
    ) -> Optional[EmbeddingVector]:
        """
        Generate a single embedding for a text.

        Args:
            text: Text to embed
            truncate: How to handle texts longer than the maximum length
            input_type: Type of input for the model ('search_document', 'search_query', 'classification', 'clustering')

        Returns:
            EmbeddingVector object or None if failed
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for embedding")
            return None

        try:
            embeddings = self.generate_embeddings([text], truncate, input_type)
            return embeddings[0] if embeddings else None
        except Exception as e:
            logger.error(f"Error generating single embedding: {str(e)}")
            return None

    def get_model_info(self) -> Dict[str, any]:
        """
        Get information about the current embedding model.

        Returns:
            Dictionary with model information
        """
        # Note: Cohere doesn't have a direct API for model info
        # This is a simplified implementation
        return {
            "model_name": self.model,
            "expected_dimensions": self._get_expected_dimensions(self.model),
            "language_support": self._get_language_support(self.model)
        }

    def _get_expected_dimensions(self, model_name: str) -> int:
        """
        Get expected embedding dimensions for a model.

        Args:
            model_name: Name of the model

        Returns:
            Expected dimensions
        """
        model_dims = {
            "embed-multilingual-v3.0": 1024,
            "embed-english-v3.0": 1024,
            "embed-multilingual-light-v3.0": 384,
            "embed-english-light-v3.0": 384,
            "large": 4096,
            "multilingual-22-12": 768
        }
        return model_dims.get(model_name, 1024)  # Default to 1024

    def _get_language_support(self, model_name: str) -> str:
        """
        Get language support for a model.

        Args:
            model_name: Name of the model

        Returns:
            Language support description
        """
        if "multilingual" in model_name:
            return "Multi-language support"
        elif "english" in model_name:
            return "English-focused"
        else:
            return "Mixed language support"

    def validate_embeddings_response(self, embeddings: List[List[float]]) -> bool:
        """
        Validate the embeddings response from Cohere API.

        Args:
            embeddings: List of embedding vectors

        Returns:
            True if valid, False otherwise
        """
        if not embeddings:
            return False

        # Check that all embeddings have the same length
        first_len = len(embeddings[0])
        for emb in embeddings:
            if len(emb) != first_len:
                logger.error("Embeddings have inconsistent lengths")
                return False

        # Check that all values are numbers
        for emb in embeddings:
            for val in emb:
                if not isinstance(val, (int, float)):
                    logger.error("Embedding contains non-numeric values")
                    return False

        return True

    def batch_generate_embeddings(
        self,
        texts: List[str],
        batch_size: int = 96,  # Cohere's default max batch size is 96
        input_type: str = "search_document"
    ) -> List[EmbeddingVector]:
        """
        Generate embeddings in batches to handle large lists of texts.

        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process in each batch
            input_type: Type of input for the model ('search_document', 'search_query', 'classification', 'clustering')

        Returns:
            List of EmbeddingVector objects
        """
        if not texts:
            return []

        all_embeddings = []
        total_texts = len(texts)

        logger.info(f"Starting batch embedding generation for {total_texts} texts in batches of {batch_size}")

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")

            batch_embeddings = self.generate_embeddings(batch, input_type=input_type)
            all_embeddings.extend(batch_embeddings)

        logger.info(f"Completed batch embedding generation: {len(all_embeddings)} embeddings created")
        return all_embeddings


# Example usage function
def example_usage():
    """
    Example of how to use the CohereClient.
    """
    # This would normally be initialized with a real API key
    # client = CohereClient(api_key="your-cohere-api-key")

    # For demo purposes, we'll show the structure
    print("CohereClient initialized with embedding model")
    print("- Can generate embeddings for lists of texts")
    print("- Handles batching for large inputs")
    print("- Implements retry logic for API failures")


if __name__ == "__main__":
    example_usage()