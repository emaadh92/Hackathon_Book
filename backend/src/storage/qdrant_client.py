from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Optional, Union
import logging
from ..storage.models import EmbeddingVector, StorageRecord, StorageResult
from ..utils.helpers import get_logger
from ..utils.validators import validate_collection_name
from datetime import datetime
import uuid

logger = get_logger(__name__)


class QdrantStorageClient:
    """
    Client for storing embeddings in Qdrant vector database.
    """

    def __init__(
        self,
        url: str,
        api_key: Optional[str] = None,
        collection_name: str = "book_embeddings",
        vector_size: int = 1024,
        distance_metric: str = "Cosine"
    ):
        """
        Initialize the Qdrant client.

        Args:
            url: Qdrant server URL
            api_key: Qdrant API key (for cloud instances)
            collection_name: Name of the collection to use
            vector_size: Size of the embedding vectors
            distance_metric: Distance metric for similarity search
        """
        if not validate_collection_name(collection_name):
            raise ValueError(f"Invalid collection name: {collection_name}")

        if distance_metric not in ["Cosine", "Euclid", "Dot"]:
            raise ValueError(f"Invalid distance metric: {distance_metric}")

        self.url = url
        self.api_key = api_key
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.distance_metric = distance_metric

        # Initialize Qdrant client
        if api_key:
            self.client = QdrantClient(url=url, api_key=api_key)
        else:
            self.client = QdrantClient(url=url)

    def create_collection(self) -> bool:
        """
        Create the collection if it doesn't exist.

        Returns:
            True if collection was created or already exists
        """
        try:
            # Check if collection already exists
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]

            if self.collection_name in collection_names:
                logger.info(f"Collection '{self.collection_name}' already exists")
                return True

            # Create the collection
            distance_enum = {
                "Cosine": models.Distance.COSINE,
                "Euclid": models.Distance.EUCLID,
                "Dot": models.Distance.DOT
            }[self.distance_metric]

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=distance_enum
                )
            )

            # Create payload indexes for efficient querying
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="url",
                field_schema=models.PayloadSchemaType.KEYWORD
            )

            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="section_title",
                field_schema=models.PayloadSchemaType.KEYWORD
            )

            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="created_at",
                field_schema=models.PayloadSchemaType.INTEGER
            )

            logger.info(f"Collection '{self.collection_name}' created successfully")
            return True

        except Exception as e:
            logger.error(f"Error creating collection '{self.collection_name}': {str(e)}")
            raise

    def store_embeddings(self, storage_records: List[StorageRecord]) -> StorageResult:
        """
        Store embedding vectors in Qdrant with metadata.

        Args:
            storage_records: List of StorageRecord objects to store

        Returns:
            StorageResult with statistics
        """
        if not storage_records:
            logger.warning("No records to store")
            return StorageResult(stored_records=0, failed_records=0, total_time=0.0)

        start_time = datetime.now()
        stored_count = 0
        failed_count = 0

        logger.info(f"Storing {len(storage_records)} embedding records in Qdrant")

        try:
            # Prepare points for insertion
            points = []
            for record in storage_records:
                point = models.PointStruct(
                    id=record.qdrant_point_id,
                    vector=record.vector,
                    payload=record.payload
                )
                points.append(point)

            # Batch insert points
            batch_size = 100  # Process in batches to avoid memory issues
            for i in range(0, len(points), batch_size):
                batch = points[i:i + batch_size]

                try:
                    self.client.upsert(
                        collection_name=self.collection_name,
                        points=batch
                    )
                    stored_count += len(batch)
                    logger.info(f"Stored batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1}")

                except Exception as batch_error:
                    logger.error(f"Failed to store batch {i//batch_size + 1}: {str(batch_error)}")
                    failed_count += len(batch)

        except Exception as e:
            logger.error(f"Error storing embeddings: {str(e)}")
            failed_count += len(storage_records) - stored_count

        finally:
            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()

        result = StorageResult(
            stored_records=stored_count,
            failed_records=failed_count,
            total_time=total_time,
            started_at=start_time,
            completed_at=end_time
        )

        logger.info(f"Storage completed: {stored_count} stored, {failed_count} failed in {total_time:.2f}s")
        return result

    def store_embedding_vectors(
        self,
        embedding_vectors: List[EmbeddingVector],
        text_chunks: List['TextChunk'],  # Forward reference to avoid circular import
        additional_metadata: Optional[Dict[str, any]] = None
    ) -> StorageResult:
        """
        Store EmbeddingVector objects in Qdrant by converting them to StorageRecords.

        Args:
            embedding_vectors: List of EmbeddingVector objects to store
            text_chunks: Corresponding TextChunk objects for metadata
            additional_metadata: Additional metadata to include

        Returns:
            StorageResult with statistics
        """
        if len(embedding_vectors) != len(text_chunks):
            raise ValueError("embedding_vectors and text_chunks must have the same length")

        # Create StorageRecords from EmbeddingVectors and TextChunks
        storage_records = []
        for emb_vec, text_chunk in zip(embedding_vectors, text_chunks):
            record = StorageRecord.from_embedding_vector(
                embedding_vector=emb_vec,
                text_chunk=text_chunk,
                additional_metadata=additional_metadata
            )
            storage_records.append(record)

        return self.store_embeddings(storage_records)

    def search_similar(
        self,
        query_vector: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, any]] = None
    ) -> List[Dict[str, any]]:
        """
        Search for similar vectors in the collection.

        Args:
            query_vector: Vector to search for similar ones
            limit: Maximum number of results to return
            filters: Optional filters to apply to the search

        Returns:
            List of similar records with payload and score
        """
        try:
            # Build filter conditions if provided
            qdrant_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    if isinstance(value, str):
                        condition = models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        )
                    elif isinstance(value, list):
                        condition = models.FieldCondition(
                            key=key,
                            match=models.MatchAny(any=value)
                        )
                    else:
                        # For numeric values, use range filter
                        condition = models.FieldCondition(
                            key=key,
                            range=models.Range(gte=float(value), lte=float(value))
                        )
                    conditions.append(condition)

                if conditions:
                    qdrant_filter = models.Filter(must=conditions)

            # Perform search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                query_filter=qdrant_filter
            )

            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'id': result.id,
                    'score': result.score,
                    'payload': result.payload,
                    'vector': result.vector if hasattr(result, 'vector') else None
                })

            logger.info(f"Search returned {len(formatted_results)} results")
            return formatted_results

        except Exception as e:
            logger.error(f"Error searching for similar vectors: {str(e)}")
            return []

    def delete_collection(self) -> bool:
        """
        Delete the entire collection.

        Returns:
            True if deletion was successful
        """
        try:
            self.client.delete_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' deleted successfully")
            return True
        except Exception as e:
            logger.error(f"Error deleting collection '{self.collection_name}': {str(e)}")
            return False

    def get_collection_info(self) -> Dict[str, any]:
        """
        Get information about the collection.

        Returns:
            Dictionary with collection information
        """
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                'name': info.config.params.vectors.size,
                'vector_size': info.config.params.vectors.size,
                'distance': info.config.params.vectors.distance.name,
                'point_count': info.points_count,
                'indexed_vectors_count': info.indexed_vectors_count
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            return {}

    def count_points(self) -> int:
        """
        Count the number of points in the collection.

        Returns:
            Number of points in the collection
        """
        try:
            info = self.client.get_collection(self.collection_name)
            return info.points_count
        except Exception as e:
            logger.error(f"Error counting points: {str(e)}")
            return 0

    def check_duplicate_by_url_and_content(
        self,
        url: str,
        content: str
    ) -> bool:
        """
        Check if an embedding with the same URL and content already exists.

        Args:
            url: URL to check
            content: Content to check

        Returns:
            True if duplicate exists, False otherwise
        """
        try:
            # Search for existing records with the same URL and similar content
            search_result = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="url",
                            match=models.MatchValue(value=url)
                        )
                    ]
                ),
                limit=100  # Limit to prevent too many results
            )

            # Check if any of the found records have similar content
            for record, _ in search_result:
                if record.payload.get("content") == content:
                    return True

            return False

        except Exception as e:
            logger.error(f"Error checking for duplicates: {str(e)}")
            return False  # Assume no duplicate on error

    def close_connection(self):
        """
        Close the connection to Qdrant.
        """
        if hasattr(self.client, '_client'):
            try:
                self.client.close()
                logger.info("Qdrant connection closed")
            except Exception as e:
                logger.error(f"Error closing Qdrant connection: {str(e)}")


# Example usage function
def example_usage():
    """
    Example of how to use the QdrantStorageClient.
    """
    # This would normally be initialized with real Qdrant credentials
    # client = QdrantStorageClient(
    #     url="https://your-cluster-url.qdrant.tech",
    #     api_key="your-api-key",
    #     collection_name="book_embeddings"
    # )

    print("QdrantStorageClient initialized")
    print("- Creates collections with proper indexing")
    print("- Stores embeddings with metadata")
    print("- Supports similarity search")
    print("- Handles duplicate detection")


if __name__ == "__main__":
    example_usage()