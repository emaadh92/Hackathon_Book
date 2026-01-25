from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Tuple
import re
import logging
from urllib.parse import urljoin, urlparse

from ..storage.models import DocusaurusPage
from ..utils.helpers import get_logger

logger = get_logger(__name__)


class HTMLParser:
    """
    Advanced HTML parser for extracting clean text content from Docusaurus sites.
    """

    def __init__(self):
        # Common Docusaurus CSS classes and selectors for content extraction
        self.content_selectors = [
            'main',
            'article',
            '.main-wrapper',
            '.container',
            '#main',
            '#content',
            '.markdown',
            '.theme-doc-markdown',
            '.doc-content',
            '.docs-content',
            '.main-content',
            '.content',
        ]

        # Elements to remove (navigation, ads, etc.)
        self.elements_to_remove = [
            'nav', 'header', 'footer', 'aside', 'script', 'style',
            '.nav', '.navbar', '.sidebar', '.toc', '.table-of-contents',
            '.menu', '.mobile-nav', '.mobile-sidebar', '.ads', '.advertisement',
            '.cookie-banner', '.consent-banner', '.tracking-consent',
            '[role="banner"]', '[role="navigation"]', '[role="complementary"]'
        ]

        # Headers to preserve for context
        self.header_selectors = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

    def extract_main_content(self, html_content: str) -> Tuple[str, str, List[str]]:
        """
        Extract the main content from HTML, preserving section titles.

        Args:
            html_content: Raw HTML content

        Returns:
            Tuple of (clean_text, title, section_titles)
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        # Get the page title
        title = ""
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()

        # Remove unwanted elements
        self._remove_unwanted_elements(soup)

        # Try to find main content using common selectors
        main_content = self._find_main_content_element(soup)

        if not main_content:
            # If no specific content container found, use the body
            body = soup.find('body')
            main_content = body if body else soup

        # Extract text with section context
        clean_text, section_titles = self._extract_text_with_sections(main_content)

        return clean_text, title, section_titles

    def _remove_unwanted_elements(self, soup: BeautifulSoup) -> None:
        """
        Remove navigation, ads, and other unwanted elements from the soup.

        Args:
            soup: BeautifulSoup object to clean
        """
        for selector in self.elements_to_remove:
            # Handle both tag names and CSS selectors
            if '.' in selector or '#' in selector or '[' in selector:
                elements = soup.select(selector)
            else:
                elements = soup.find_all(selector)

            for element in elements:
                element.decompose()

    def _find_main_content_element(self, soup: BeautifulSoup) -> Optional[BeautifulSoup]:
        """
        Find the main content element using common Docusaurus selectors.

        Args:
            soup: BeautifulSoup object

        Returns:
            Main content element or None if not found
        """
        for selector in self.content_selectors:
            if '.' in selector or '#' in selector or '[' in selector:
                element = soup.select_one(selector)
            else:
                element = soup.find(selector)

            if element:
                return element

        return None

    def _extract_text_with_sections(self, element) -> Tuple[str, List[str]]:
        """
        Extract text content while preserving section titles for context.

        Args:
            element: BeautifulSoup element to extract from

        Returns:
            Tuple of (text_content, section_titles)
        """
        section_titles = []
        text_parts = []

        # Process the element and its children
        for child in element.descendants:
            if child.name in self.header_selectors:
                header_text = child.get_text().strip()
                if header_text:
                    section_titles.append(header_text)
                    text_parts.append(f"\n### {header_text}\n")
            elif child.name == 'p':
                paragraph_text = child.get_text().strip()
                if paragraph_text:
                    text_parts.append(paragraph_text)
            elif child.name in ['div', 'span', 'li', 'td']:
                # Extract text from block elements if they don't contain headers
                if not any(child.find(header) for header in self.header_selectors):
                    text = child.get_text().strip()
                    if text and len(text) > 20:  # Only add substantial text
                        text_parts.append(text)

        # Join all text parts with appropriate spacing
        clean_text = '\n'.join(text_parts)

        # Clean up excessive whitespace
        clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text)  # Replace multiple newlines with double newline
        clean_text = clean_text.strip()

        return clean_text, section_titles

    def extract_structured_content(self, html_content: str) -> Dict[str, any]:
        """
        Extract structured content with metadata from HTML.

        Args:
            html_content: Raw HTML content

        Returns:
            Dictionary with structured content and metadata
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract title
        title = ""
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()

        # Extract meta description
        meta_desc = ""
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            meta_desc = meta_tag.get('content', '')

        # Remove unwanted elements
        self._remove_unwanted_elements(soup)

        # Find main content
        main_content = self._find_main_content_element(soup)
        if not main_content:
            main_content = soup

        # Extract text with sections
        clean_text, section_titles = self._extract_text_with_sections(main_content)

        # Extract all links
        all_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text().strip()
            if href and text:
                all_links.append({'url': href, 'text': text})

        # Extract code blocks
        code_blocks = []
        for code_block in soup.find_all(['code', 'pre']):
            code_text = code_block.get_text().strip()
            if code_text:
                code_blocks.append(code_text)

        return {
            'title': title,
            'meta_description': meta_desc,
            'clean_text': clean_text,
            'section_titles': section_titles,
            'links': all_links,
            'code_blocks': code_blocks
        }

    def parse_page(self, docusaurus_page: DocusaurusPage) -> DocusaurusPage:
        """
        Parse a DocusaurusPage and update it with clean content.

        Args:
            docusaurus_page: Page to parse

        Returns:
            Updated DocusaurusPage with clean content
        """
        if not docusaurus_page.html_content:
            logger.warning(f"No HTML content to parse for {docusaurus_page.url}")
            return docusaurus_page

        try:
            clean_text, title, section_titles = self.extract_main_content(docusaurus_page.html_content)

            # Update the page with parsed content
            updated_page = DocusaurusPage(
                url=docusaurus_page.url,
                title=title or docusaurus_page.title,
                content=clean_text,
                html_content=docusaurus_page.html_content,
                last_modified=docusaurus_page.last_modified,
                status_code=docusaurus_page.status_code,
                error_message=docusaurus_page.error_message
            )

            logger.info(f"Parsed content for {docusaurus_page.url}: {len(clean_text)} characters")
            return updated_page

        except Exception as e:
            logger.error(f"Error parsing page {docusaurus_page.url}: {str(e)}")
            docusaurus_page.error_message = f"Parsing error: {str(e)}"
            return docusaurus_page

    def batch_parse_pages(self, pages: List[DocusaurusPage]) -> List[DocusaurusPage]:
        """
        Parse multiple pages in batch.

        Args:
            pages: List of pages to parse

        Returns:
            List of parsed pages
        """
        parsed_pages = []
        for page in pages:
            parsed_page = self.parse_page(page)
            parsed_pages.append(parsed_page)

        return parsed_pages

    def extract_faq_content(self, html_content: str) -> List[Dict[str, str]]:
        """
        Specialized method to extract FAQ-style content.

        Args:
            html_content: HTML content to extract FAQs from

        Returns:
            List of dictionaries with question-answer pairs
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        faqs = []

        # Look for common FAQ patterns
        faq_selectors = [
            '.faq-item', '.accordion-item', '.question-answer',
            '[class*="faq"]', '[class*="question"]', '[class*="answer"]'
        ]

        for selector in faq_selectors:
            items = soup.select(selector)
            for item in items:
                # Try to find question and answer elements
                question_el = item.find(['h3', 'h4', 'h5', 'dt', '.question'])
                answer_el = item.find(['p', 'div', 'dd', '.answer'])

                if question_el and answer_el:
                    faqs.append({
                        'question': question_el.get_text().strip(),
                        'answer': answer_el.get_text().strip()
                    })

        return faqs

    def extract_table_of_contents(self, html_content: str) -> List[Dict[str, any]]:
        """
        Extract table of contents from the HTML.

        Args:
            html_content: HTML content to extract TOC from

        Returns:
            List of TOC items with hierarchy
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        toc_items = []

        # Find all headers
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        for header in headers:
            level = int(header.name[1])  # Extract number from h1, h2, etc.
            text = header.get_text().strip()

            # Try to find an anchor link for the header
            anchor = header.find('a')
            link = anchor.get('href') if anchor else None

            toc_items.append({
                'level': level,
                'text': text,
                'link': link
            })

        return toc_items


# Example usage function
def example_usage():
    """
    Example of how to use the HTMLParser.
    """
    html_sample = """
    <html>
        <head><title>Sample Docusaurus Page</title></head>
        <body>
            <nav>Navigation content</nav>
            <main>
                <h1>Main Title</h1>
                <h2>Section 1</h2>
                <p>This is the content of section 1.</p>
                <h3>Subsection 1.1</h3>
                <p>This is the content of subsection 1.1.</p>
                <h2>Section 2</h2>
                <p>This is the content of section 2.</p>
            </main>
            <footer>Footer content</footer>
        </body>
    </html>
    """

    parser = HTMLParser()
    clean_text, title, sections = parser.extract_main_content(html_sample)

    print(f"Title: {title}")
    print(f"Sections: {sections}")
    print(f"Clean text: {clean_text}")


if __name__ == "__main__":
    example_usage()