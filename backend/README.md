# Book Website Embeddings Pipeline

This pipeline crawls Docusaurus-based book websites, extracts clean text content, generates semantic embeddings using Cohere's models, and stores the vectors in Qdrant Cloud with preserved metadata.

## Prerequisites

- Python 3.11+
- `uv` package manager installed (`pip install uv` or visit https://docs.astral.sh/uv/)

## Setup

1. **Install dependencies with uv**:
   ```bash
   cd backend
   uv venv  # Create virtual environment
   source .venv/bin/activate  # Activate virtual environment
   uv pip install -e .
   ```

2. **Configure environment variables**:
   Copy the example environment file and add your API keys:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_cloud_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   BOOK_SITE_URLS=https://yoursite.com/docs,https://anothersite.com/book
   ```

## Running the Pipeline

### Basic Usage
```bash
python main.py
```

### With Specific Configuration
```bash
# Override default settings via command line
python main.py --urls "https://example.com/docs" --chunk-size 512 --chunk-overlap 64
```

### Configuration Options
- `--urls`: Comma-separated list of Docusaurus site URLs to crawl
- `--chunk-size`: Size of text chunks for embedding (default: 1024)
- `--chunk-overlap`: Overlap between chunks (default: 128)
- `--collection-name`: Qdrant collection name (default: "book_embeddings")

## Architecture

The pipeline consists of four main components:

1. **Crawlers**: Responsible for crawling Docusaurus sites and extracting clean text
2. **Embeddings**: Handles text chunking and Cohere embedding generation
3. **Storage**: Manages vector storage in Qdrant with metadata preservation
4. **Utils**: Common utilities and helper functions

## Configuration

The pipeline supports both environment variable and command-line configuration:

- **Environment Variables**: Set in `.env` file
- **Command-Line Args**: Override environment variables for specific runs

## Troubleshooting

- **API Rate Limits**: The pipeline implements exponential backoff for Cohere and Qdrant API calls
- **Network Issues**: Failed pages are logged and can be retried individually
- **Authentication**: Verify API keys are correctly set in environment variables