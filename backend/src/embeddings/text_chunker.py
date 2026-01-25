from typing import List, Tuple, Optional
import re
from ..storage.models import TextChunk
from ..utils.helpers import generate_chunk_id, get_logger
from ..utils.validators import validate_chunk_size, validate_overlap_params, validate_text_content

logger = get_logger(__name__)


class TextChunker:
    """
    Text chunker for splitting documents into smaller pieces for embedding.
    """

    def __init__(self, chunk_size: int = 1024, chunk_overlap: int = 128, chunk_strategy: str = 'sliding_window'):
        """
        Initialize the text chunker.

        Args:
            chunk_size: Maximum size of each chunk
            chunk_overlap: Number of characters to overlap between chunks
            chunk_strategy: Strategy for chunking ('sliding_window', 'semantic_boundaries', 'by_headers', 'paragraph_based')
        """
        if not validate_chunk_size(chunk_size):
            raise ValueError(f"Invalid chunk_size: {chunk_size}")

        if not validate_overlap_params(chunk_size, chunk_overlap):
            raise ValueError(f"Invalid overlap params: chunk_size={chunk_size}, overlap={chunk_overlap}")

        if not self.validate_chunk_strategy(chunk_strategy):
            raise ValueError(f"Unsupported chunk strategy: {chunk_strategy}")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.chunk_strategy = chunk_strategy

    def update_chunk_settings(self, chunk_size: Optional[int] = None, chunk_overlap: Optional[int] = None, chunk_strategy: Optional[str] = None):
        """
        Update chunking settings dynamically.

        Args:
            chunk_size: New chunk size
            chunk_overlap: New chunk overlap
            chunk_strategy: New chunking strategy
        """
        if chunk_size is not None:
            if not validate_chunk_size(chunk_size):
                raise ValueError(f"Invalid chunk_size: {chunk_size}")
            self.chunk_size = chunk_size

        if chunk_overlap is not None:
            if not validate_overlap_params(self.chunk_size, chunk_overlap):
                raise ValueError(f"Invalid overlap params: chunk_size={self.chunk_size}, overlap={chunk_overlap}")
            self.chunk_overlap = chunk_overlap

        if chunk_strategy is not None:
            if not self.validate_chunk_strategy(chunk_strategy):
                raise ValueError(f"Unsupported chunk strategy: {chunk_strategy}")
            self.chunk_strategy = chunk_strategy

        logger.info(f"Updated chunk settings: size={self.chunk_size}, overlap={self.chunk_overlap}, strategy={self.chunk_strategy}")

    def chunk_text(self, text: str, url: str, section_title: Optional[str] = None) -> List[TextChunk]:
        """
        Split text into chunks of specified size with overlap.

        Args:
            text: Text to chunk
            url: Original URL of the text
            section_title: Title of the section this text belongs to

        Returns:
            List of TextChunk objects
        """
        if not validate_text_content(text):
            logger.warning(f"Insufficient content to chunk from {url}")
            return []

        # Clean up the text
        text = text.strip()

        # Split text into chunks
        chunks = []
        start_idx = 0

        while start_idx < len(text):
            # Determine the end index for this chunk
            end_idx = start_idx + self.chunk_size

            # If we're near the end, just take the rest
            if end_idx >= len(text):
                end_idx = len(text)
            else:
                # Try to break at sentence boundary if possible
                original_end_idx = end_idx
                # Look for sentence endings before the hard limit
                for i in range(min(end_idx, len(text)) - 1, start_idx, -1):
                    if text[i] in '.!?。！？':
                        end_idx = i + 1
                        break
                # If no sentence ending found, use the hard limit
                if end_idx == original_end_idx:
                    # Try to break at word boundary
                    for i in range(min(end_idx, len(text)) - 1, start_idx, -1):
                        if text[i] == ' ':
                            end_idx = i
                            break

            # Extract the chunk content
            chunk_content = text[start_idx:end_idx]

            # Generate a unique chunk ID
            chunk_id = generate_chunk_id(url, start_idx, end_idx)

            # Create TextChunk object
            text_chunk = TextChunk(
                chunk_id=chunk_id,
                original_url=url,
                content=chunk_content,
                start_pos=start_idx,
                end_pos=end_idx,
                section_title=section_title,
                chunk_metadata={
                    'original_text_length': len(text),
                    'chunk_position': len(chunks) + 1,
                    'total_chunks': -1  # Will update later
                }
            )

            chunks.append(text_chunk)

            # Move start index forward, accounting for overlap
            start_idx = end_idx - self.chunk_overlap

            # Handle edge case where we're stuck (overlap might be too large)
            if start_idx <= start_idx:
                start_idx = end_idx

        # Update total chunks in metadata
        for i, chunk in enumerate(chunks):
            chunk.chunk_metadata['total_chunks'] = len(chunks)
            chunk.chunk_metadata['chunk_position'] = i + 1

        logger.info(f"Split text from {url} into {len(chunks)} chunks")
        return chunks

    def chunk_multiple_texts(
        self,
        texts: List[Tuple[str, str]],  # List of (text, url) tuples
        section_title: Optional[str] = None
    ) -> List[TextChunk]:
        """
        Chunk multiple texts at once.

        Args:
            texts: List of (text, url) tuples
            section_title: Title of the section these texts belong to

        Returns:
            List of TextChunk objects
        """
        all_chunks = []

        for text, url in texts:
            chunks = self.chunk_text(text, url, section_title)
            all_chunks.extend(chunks)

        return all_chunks

    def chunk_by_semantic_boundaries(self, text: str, url: str, section_title: Optional[str] = None) -> List[TextChunk]:
        """
        Chunk text by semantic boundaries like paragraphs and sections.

        Args:
            text: Text to chunk
            url: Original URL of the text
            section_title: Title of the section this text belongs to

        Returns:
            List of TextChunk objects
        """
        if not validate_text_content(text):
            logger.warning(f"Insufficient content to chunk from {url}")
            return []

        # Split by paragraphs first
        paragraphs = re.split(r'\n\s*\n+', text)

        chunks = []
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # If paragraph is smaller than chunk size, use as is
            if len(para) <= self.chunk_size:
                chunk_id = generate_chunk_id(url, text.index(para), text.index(para) + len(para))

                text_chunk = TextChunk(
                    chunk_id=chunk_id,
                    original_url=url,
                    content=para,
                    start_pos=text.index(para),
                    end_pos=text.index(para) + len(para),
                    section_title=section_title,
                    chunk_metadata={
                        'boundary_type': 'paragraph',
                        'original_text_length': len(text)
                    }
                )
                chunks.append(text_chunk)
            else:
                # If paragraph is too large, fall back to sliding window
                para_chunks = self.chunk_text(para, url, section_title)
                for chunk in para_chunks:
                    # Update boundary type
                    chunk.chunk_metadata['boundary_type'] = 'sliding_window'
                    chunks.append(chunk)

        logger.info(f"Semantically chunked text from {url} into {len(chunks)} chunks")
        return chunks

    def chunk_by_headers(self, text: str, url: str, headers: List[Tuple[int, str, str]] = None) -> List[TextChunk]:
        """
        Chunk text based on headers found in the document.

        Args:
            text: Text to chunk
            url: Original URL of the text
            headers: List of (position, level, title) tuples representing headers

        Returns:
            List of TextChunk objects
        """
        if not headers:
            # If no headers provided, fall back to regular chunking
            return self.chunk_text(text, url)

        # Sort headers by position
        sorted_headers = sorted(headers, key=lambda x: x[0])

        chunks = []
        start_pos = 0

        for i, (pos, level, title) in enumerate(sorted_headers):
            # Get content from previous header to this one
            if pos > start_pos:
                content = text[start_pos:pos]
                if content.strip():
                    chunk_id = generate_chunk_id(url, start_pos, pos)

                    text_chunk = TextChunk(
                        chunk_id=chunk_id,
                        original_url=url,
                        content=content,
                        start_pos=start_pos,
                        end_pos=pos,
                        section_title=title,
                        chunk_metadata={
                            'header_level': level,
                            'header_title': title
                        }
                    )
                    chunks.append(text_chunk)

            # Set start position to after this header
            start_pos = pos

        # Add remaining content after last header
        if start_pos < len(text):
            content = text[start_pos:]
            if content.strip():
                chunk_id = generate_chunk_id(url, start_pos, len(text))

                text_chunk = TextChunk(
                    chunk_id=chunk_id,
                    original_url=url,
                    content=content,
                    start_pos=start_pos,
                    end_pos=len(text),
                    section_title=sorted_headers[-1][2] if sorted_headers else None,
                    chunk_metadata={
                        'header_level': sorted_headers[-1][1] if sorted_headers else 'none',
                        'header_title': sorted_headers[-1][2] if sorted_headers else 'none'
                    }
                )
                chunks.append(text_chunk)

        logger.info(f"Header-based chunked text from {url} into {len(chunks)} chunks")
        return chunks

    def get_optimal_chunk_size(self, avg_sentence_length: float = 20.0) -> int:
        """
        Calculate an optimal chunk size based on average sentence length.

        Args:
            avg_sentence_length: Average number of words per sentence

        Returns:
            Recommended chunk size
        """
        # Estimate characters per sentence (avg word length ~5 chars + spaces)
        chars_per_sentence = avg_sentence_length * 6

        # Aim for 3-5 sentences per chunk
        optimal_size = int(chars_per_sentence * 4)

        # Ensure it's within reasonable bounds
        optimal_size = max(256, min(optimal_size, 4096))

        return optimal_size

    def validate_chunk_strategy(self, strategy: str) -> bool:
        """
        Validate if a chunking strategy is supported.

        Args:
            strategy: Name of the chunking strategy

        Returns:
            True if supported, False otherwise
        """
        supported_strategies = [
            'sliding_window',
            'semantic_boundaries',
            'by_headers',
            'paragraph_based'
        ]
        return strategy in supported_strategies


# Example usage function
def example_usage():
    """
    Example of how to use the TextChunker.
    """
    chunker = TextChunker(chunk_size=512, chunk_overlap=64)

    sample_text = """
    This is the first paragraph of our sample text. It contains some important information
    that we want to preserve when chunking. The paragraph discusses various topics related
    to the subject matter at hand.

    This is the second paragraph which continues the discussion. It provides additional
    details and examples that complement the information in the first paragraph. Together,
    these paragraphs form a cohesive unit of information.

    Finally, this is the third paragraph which concludes our example. It summarizes the
    key points and provides a closing thought to wrap up the discussion.
    """

    url = "https://example.com/sample-document"

    # Regular chunking
    chunks = chunker.chunk_text(sample_text, url)
    print(f"Regular chunking resulted in {len(chunks)} chunks")

    # Semantic chunking
    semantic_chunks = chunker.chunk_by_semantic_boundaries(sample_text, url)
    print(f"Semantic chunking resulted in {len(semantic_chunks)} chunks")


if __name__ == "__main__":
    example_usage()