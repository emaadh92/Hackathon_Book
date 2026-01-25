#!/usr/bin/env python3
"""
Main entry point for the Book Website Embeddings Pipeline.

This script orchestrates the complete pipeline:
1. Crawls Docusaurus sites to extract text content
2. Chunks the text appropriately
3. Generates embeddings using Cohere
4. Stores embeddings in Qdrant with metadata
"""

import argparse
import sys
import os
from typing import List, Optional
import logging
from datetime import datetime

# Add the backend directory to the path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from config.settings import settings, Settings
from src.crawlers.docusaurus_crawler import DocusaurusCrawler
from src.crawlers.html_parser import HTMLParser
from src.embeddings.text_chunker import TextChunker
from src.embeddings.cohere_client import CohereClient
from src.storage.qdrant_client import QdrantStorageClient
from src.storage.models import DocusaurusPage, TextChunk, EmbeddingVector, StorageRecord
from src.utils.helpers import get_logger

logger = get_logger(__name__)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Book Website Embeddings Pipeline"
    )

    parser.add_argument(
        '--urls',
        type=str,
        help='Comma-separated list of Docusaurus site URLs to crawl'
    )

    parser.add_argument(
        '--chunk-size',
        type=int,
        help='Size of text chunks for embedding'
    )

    parser.add_argument(
        '--chunk-overlap',
        type=int,
        help='Overlap between chunks'
    )

    parser.add_argument(
        '--collection-name',
        type=str,
        help='Qdrant collection name'
    )

    parser.add_argument(
        '--embedding-model',
        type=str,
        help='Cohere embedding model to use'
    )

    parser.add_argument(
        '--max-concurrent-requests',
        type=int,
        default=5,
        help='Maximum number of concurrent requests for crawling'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    return parser.parse_args()


def validate_configuration(args) -> Settings:
    """Validate and update settings based on command line arguments."""
    # Update settings from command line arguments if provided
    if args.urls:
        settings.BOOK_SITE_URLS = [url.strip() for url in args.urls.split(',')]

    if args.chunk_size:
        settings.CHUNK_SIZE = args.chunk_size

    if args.chunk_overlap:
        settings.CHUNK_OVERLAP = args.chunk_overlap

    if args.collection_name:
        settings.COLLECTION_NAME = args.collection_name

    if args.embedding_model:
        settings.EMBEDDING_MODEL = args.embedding_model

    # Validate configuration
    settings.validate()

    return settings


def main():
    """Main function to orchestrate the complete embedding pipeline."""
    start_time = datetime.now()
    logger.info("Starting Book Website Embeddings Pipeline")

    # Parse command line arguments
    args = parse_arguments()

    # Set logging level based on verbose flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Validate configuration
        config = validate_configuration(args)
        logger.info(f"Configuration validated: {len(config.BOOK_SITE_URLS)} URLs, "
                   f"chunk size {config.CHUNK_SIZE}, overlap {config.CHUNK_OVERLAP}")

        # Step 1: Crawl Docusaurus sites
        logger.info("Step 1: Crawling Docusaurus sites...")
        crawler = DocusaurusCrawler(
            max_concurrent_requests=args.max_concurrent_requests,
            delay_between_requests=0.5
        )

        pages = crawler.crawl_sites(config.BOOK_SITE_URLS)
        successful_pages = [p for p in pages if p.error_message is None]

        logger.info(f"Crawling completed: {len(successful_pages)} successful, "
                   f"{len(pages) - len(successful_pages)} failed")

        if not successful_pages:
            logger.error("No pages were successfully crawled. Exiting.")
            return 1

        # Step 2: Parse HTML content to extract clean text
        logger.info("Step 2: Parsing HTML content to extract clean text...")
        parser = HTMLParser()
        parsed_pages = parser.batch_parse_pages(successful_pages)

        # Collect all text content with URLs for chunking
        text_content = [(page.content, page.url, page.title) for page in parsed_pages
                       if page.content and len(page.content.strip()) > 10]

        if not text_content:
            logger.error("No valid text content found after parsing. Exiting.")
            return 1

        logger.info(f"Extracted text from {len(text_content)} pages")

        # Step 3: Chunk text appropriately
        logger.info("Step 3: Chunking text content...")
        chunker = TextChunker(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )

        all_chunks = []
        for content, url, title in text_content:
            chunks = chunker.chunk_text(content, url, title)
            all_chunks.extend(chunks)

        logger.info(f"Text chunked into {len(all_chunks)} chunks")

        if not all_chunks:
            logger.error("No text chunks created. Exiting.")
            return 1

        # Step 4: Generate embeddings using Cohere
        logger.info("Step 4: Generating embeddings using Cohere...")

        if not config.COHERE_API_KEY:
            logger.error("COHERE_API_KEY is not set. Please set it in your environment.")
            return 1

        cohere_client = CohereClient(
            api_key=config.COHERE_API_KEY,
            model=config.EMBEDDING_MODEL
        )

        # Extract text content from chunks for embedding
        texts_to_embed = [chunk.content for chunk in all_chunks]

        # Generate embeddings in batches to handle large amounts of text
        embedding_vectors = cohere_client.batch_generate_embeddings(texts_to_embed)

        logger.info(f"Generated {len(embedding_vectors)} embeddings")

        if len(embedding_vectors) != len(all_chunks):
            logger.warning(f"Mismatch: {len(all_chunks)} chunks but {len(embedding_vectors)} embeddings generated")

        # Step 5: Store embeddings in Qdrant
        logger.info("Step 5: Storing embeddings in Qdrant...")

        if not config.QDRANT_URL:
            logger.error("QDRANT_URL is not set. Please set it in your environment.")
            return 1

        qdrant_client = QdrantStorageClient(
            url=config.QDRANT_URL,
            api_key=config.QDRANT_API_KEY,
            collection_name=config.COLLECTION_NAME,
            vector_size=len(embedding_vectors[0].embedding) if embedding_vectors else 1024
        )

        # Create collection if it doesn't exist
        qdrant_client.create_collection()

        # Create storage records from embeddings and chunks
        storage_records = []
        for emb_vec, text_chunk in zip(embedding_vectors, all_chunks):
            # Update the embedding vector with the actual chunk ID
            emb_vec.chunk_id = text_chunk.chunk_id
            record = StorageRecord.from_embedding_vector(emb_vec, text_chunk)
            storage_records.append(record)

        # Store the embeddings
        storage_result = qdrant_client.store_embeddings(storage_records)

        logger.info(f"Storage completed: {storage_result.stored_records} stored, "
                   f"{storage_result.failed_records} failed")

        # Step 6: Report results
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()

        logger.info("=" * 50)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info(f"Total execution time: {total_time:.2f} seconds")
        logger.info(f"Pages processed: {len(successful_pages)}")
        logger.info(f"Text chunks created: {len(all_chunks)}")
        logger.info(f"Embeddings generated: {len(embedding_vectors)}")
        logger.info(f"Vectors stored: {storage_result.stored_records}")
        logger.info(f"Failed operations: {storage_result.failed_records}")
        logger.info("=" * 50)

        return 0

    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
        return 130  # Standard exit code for Ctrl+C
    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}", exc_info=True)
        return 1
    finally:
        # Close any connections
        try:
            if 'qdrant_client' in locals():
                qdrant_client.close_connection()
        except:
            pass  # Ignore errors when closing connections


def run_pipeline_for_urls(urls: List[str], config_override: Optional[dict] = None):
    """
    Run the pipeline programmatically for specific URLs with optional config override.

    Args:
        urls: List of URLs to process
        config_override: Optional dictionary to override configuration

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    # This would be used for programmatic access to the pipeline
    # For now, it's a placeholder for potential future extension
    pass


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)