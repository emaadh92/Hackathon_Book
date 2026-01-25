# Quickstart: Book Website Embeddings Pipeline

## Prerequisites

- Python 3.11+
- `uv` package manager installed (`pip install uv` or visit https://docs.astral.sh/uv/)

## Setup

1. **Clone and navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies with uv**:
   ```bash
   uv venv  # Create virtual environment
   source .venv/bin/activate  # Activate virtual environment
   uv pip install -r requirements.txt  # Install dependencies (or use pyproject.toml)
   ```

3. **Configure environment variables**:
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

## Expected Output
- Crawled pages and extracted content logged to console
- Progress indicators for each phase of the pipeline
- Final count of vectors stored in Qdrant
- Summary statistics about the ingestion process

## Troubleshooting

- **API Rate Limits**: The pipeline implements exponential backoff for Cohere and Qdrant API calls
- **Network Issues**: Failed pages are logged and can be retried individually
- **Authentication**: Verify API keys are correctly set in environment variables

## Next Steps
1. Customize the chunking strategy based on your content type
2. Adjust the embedding model based on your needs (multilingual vs English-optimized)
3. Set up monitoring for production deployments