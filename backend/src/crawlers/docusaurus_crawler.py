import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Tuple
from urllib.parse import urljoin, urlparse
import time
import logging
from concurrent.futures import ThreadPoolExecutor

from ..storage.models import DocusaurusPage
from ..utils.helpers import retry_on_failure, get_logger
from ..utils.validators import is_valid_url, validate_text_content

logger = get_logger(__name__)


class DocusaurusCrawler:
    """
    Crawler for Docusaurus-based websites that extracts clean text content.
    """

    def __init__(self, max_concurrent_requests: int = 5, delay_between_requests: float = 0.5):
        """
        Initialize the crawler.

        Args:
            max_concurrent_requests: Maximum number of concurrent requests
            delay_between_requests: Delay between requests to be respectful
        """
        self.max_concurrent_requests = max_concurrent_requests
        self.delay_between_requests = delay_between_requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; BookEmbeddingsBot/1.0)'
        })

    def _get_robots_txt_content(self, base_url: str) -> Optional[str]:
        """
        Retrieve robots.txt content for a given base URL.

        Args:
            base_url: Base URL of the site

        Returns:
            Content of robots.txt or None if not found
        """
        try:
            robots_url = urljoin(base_url, '/robots.txt')
            response = self.session.get(robots_url, timeout=10)
            if response.status_code == 200:
                return response.text
        except Exception:
            logger.warning(f"Could not fetch robots.txt from {base_url}")

        return None

    def _is_allowed_by_robots(self, url: str, robots_content: Optional[str] = None) -> bool:
        """
        Check if a URL is allowed by robots.txt rules.

        Args:
            url: URL to check
            robots_content: Content of robots.txt file

        Returns:
            True if allowed, False otherwise
        """
        if not robots_content:
            return True  # If no robots.txt, assume allowed

        # Simple robots.txt parser (for demonstration)
        # In a real implementation, you'd want a more robust parser
        parsed_url = urlparse(url)
        path = parsed_url.path

        # Check if the path is disallowed
        lines = robots_content.split('\n')
        for line in lines:
            if line.startswith('Disallow:'):
                disallowed_path = line.split(':', 1)[1].strip()
                if path.startswith(disallowed_path):
                    return False

        return True

    def _extract_links_from_sitemap(self, base_url: str) -> List[str]:
        """
        Attempt to extract links from sitemap.xml if available.

        Args:
            base_url: Base URL of the site

        Returns:
            List of URLs found in sitemap
        """
        sitemap_url = urljoin(base_url, '/sitemap.xml')
        try:
            response = self.session.get(sitemap_url, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                loc_tags = soup.find_all('loc')
                urls = [loc.get_text().strip() for loc in loc_tags if loc]

                # Filter URLs that belong to the same domain
                base_domain = urlparse(base_url).netloc
                filtered_urls = [
                    url for url in urls
                    if urlparse(url).netloc == base_domain and url.endswith(('.html', '/'))
                ]

                logger.info(f"Found {len(filtered_urls)} URLs in sitemap")
                return filtered_urls
        except Exception as e:
            logger.warning(f"Could not fetch sitemap from {sitemap_url}: {e}")

        return []

    def _discover_urls_from_base_page(self, base_url: str) -> List[str]:
        """
        Discover URLs by scraping the base page for navigation links.

        Args:
            base_url: Base URL to start discovery from

        Returns:
            List of discovered URLs
        """
        try:
            response = self.session.get(base_url, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find common navigation elements in Docusaurus sites
                nav_links = soup.find_all('a', href=True)

                # Filter for internal links
                base_domain = urlparse(base_url).netloc
                urls = set()

                for link in nav_links:
                    href = link['href']

                    # Convert relative URLs to absolute
                    full_url = urljoin(base_url, href)

                    # Only include URLs from the same domain
                    if urlparse(full_url).netloc == base_domain:
                        # Only include URLs that look like documentation pages
                        if full_url.endswith(('.html', '/', '#')) and '#' not in full_url.split('?')[0]:
                            urls.add(full_url)

                logger.info(f"Discovered {len(urls)} URLs from base page")
                return list(urls)
        except Exception as e:
            logger.warning(f"Could not discover URLs from {base_url}: {e}")

        return []

    def discover_urls(self, base_urls: List[str]) -> List[str]:
        """
        Discover all accessible URLs from the provided base URLs.

        Args:
            base_urls: List of base URLs to discover from

        Returns:
            List of discovered URLs
        """
        all_urls = set()

        for base_url in base_urls:
            logger.info(f"Discovering URLs from: {base_url}")

            # Try sitemap first (faster and more complete)
            sitemap_urls = self._extract_links_from_sitemap(base_url)
            if sitemap_urls:
                all_urls.update(sitemap_urls)
            else:
                # Fall back to manual discovery
                discovered_urls = self._discover_urls_from_base_page(base_url)
                all_urls.update(discovered_urls)

            # Add the base URL itself if it's a valid page
            if is_valid_url(base_url):
                all_urls.add(base_url)

        # Validate URLs
        valid_urls = [url for url in all_urls if is_valid_url(url)]
        logger.info(f"Discovered {len(valid_urls)} valid URLs total")

        return valid_urls

    def _fetch_page(self, url: str, robots_content: Optional[str] = None) -> Optional[DocusaurusPage]:
        """
        Fetch a single page and extract clean text content.

        Args:
            url: URL to fetch
            robots_content: Content of robots.txt for the domain

        Returns:
            DocusaurusPage object or None if failed
        """
        try:
            # Check robots.txt compliance
            if not self._is_allowed_by_robots(url, robots_content):
                logger.warning(f"URL not allowed by robots.txt: {url}")
                return None

            time.sleep(self.delay_between_requests)  # Be respectful
            response = self.session.get(url, timeout=30)

            if response.status_code != 200:
                logger.error(f"Failed to fetch {url}: Status {response.status_code}")
                return DocusaurusPage(
                    url=url,
                    status_code=response.status_code,
                    error_message=f"HTTP {response.status_code}"
                )

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove unwanted elements that are common in Docusaurus sites
            for element in soup(['script', 'style', 'nav', 'footer', 'aside']):
                element.decompose()

            # Try to find the main content area (common selectors in Docusaurus)
            main_content = (
                soup.find('main') or
                soup.find('article') or
                soup.find(class_='main-wrapper') or
                soup.find(class_='container') or
                soup.find(id='main') or
                soup.find(id='content') or
                soup
            )

            # Extract clean text
            text_content = main_content.get_text(separator='\n', strip=True)

            # Get page title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else ''

            # Validate content
            if not validate_text_content(text_content):
                logger.warning(f"Insufficient content extracted from {url}")
                return DocusaurusPage(
                    url=url,
                    title=title,
                    status_code=response.status_code,
                    error_message="Insufficient content extracted"
                )

            logger.info(f"Successfully fetched and parsed: {url}")

            return DocusaurusPage(
                url=url,
                title=title,
                content=text_content,
                html_content=str(main_content),
                status_code=response.status_code
            )

        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return DocusaurusPage(
                url=url,
                status_code=0,
                error_message=str(e)
            )

    @retry_on_failure(max_retries=3, delay=1.0, backoff=2.0)
    def crawl_urls(self, urls: List[str]) -> List[DocusaurusPage]:
        """
        Crawl a list of URLs and extract clean text content.

        Args:
            urls: List of URLs to crawl

        Returns:
            List of DocusaurusPage objects
        """
        logger.info(f"Starting to crawl {len(urls)} URLs")

        # Get robots.txt content for the domain (assuming all URLs are from the same domain)
        if urls:
            base_domain = urlparse(urls[0]).netloc
            base_url = f"https://{base_domain}"
            robots_content = self._get_robots_txt_content(base_url)
        else:
            robots_content = None

        pages = []
        successful = 0
        failed = 0

        with ThreadPoolExecutor(max_workers=self.max_concurrent_requests) as executor:
            futures = [
                executor.submit(self._fetch_page, url, robots_content)
                for url in urls
            ]

            for future in futures:
                page = future.result()
                if page:
                    pages.append(page)
                    if page.error_message is None:
                        successful += 1
                    else:
                        failed += 1

        logger.info(f"Crawling completed: {successful} successful, {failed} failed")
        return pages

    def crawl_sites(self, base_urls: List[str]) -> List[DocusaurusPage]:
        """
        Complete crawling process: discover URLs and crawl them.

        Args:
            base_urls: List of base URLs to crawl

        Returns:
            List of DocusaurusPage objects
        """
        logger.info(f"Starting crawl of sites: {base_urls}")

        # Discover URLs
        discovered_urls = self.discover_urls(base_urls)

        if not discovered_urls:
            logger.warning("No URLs discovered, returning empty result")
            return []

        # Crawl the discovered URLs
        pages = self.crawl_urls(discovered_urls)

        return pages


# Example usage function
def example_usage():
    """
    Example of how to use the DocusaurusCrawler.
    """
    crawler = DocusaurusCrawler(max_concurrent_requests=3, delay_between_requests=0.5)

    # Example URLs - replace with actual Docusaurus sites
    urls = [
        "https://docusaurus.io/docs",
        # Add more URLs as needed
    ]

    pages = crawler.crawl_sites(urls)

    for page in pages[:5]:  # Show first 5 pages
        print(f"URL: {page.url}")
        print(f"Title: {page.title}")
        print(f"Content length: {len(page.content)} characters")
        print("---")


if __name__ == "__main__":
    example_usage()