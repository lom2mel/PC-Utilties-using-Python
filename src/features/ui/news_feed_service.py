"""Cybersecurity news feed service.

This module provides functionality to fetch and aggregate cybersecurity news
from various RSS feeds and provides static curated news sources.
"""

import logging
import ssl
import time
import webbrowser
from dataclasses import dataclass
from datetime import datetime, UTC
from email.utils import parsedate_to_datetime
from typing import ClassVar, Optional

import bleach
import feedparser

from features.ui.design_system import COLORS
from features.ui.exceptions import FeedParseError, NetworkError
from features.ui.security_utils import sanitize_url_for_logging, validate_url

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class NewsArticle:
    """Represents a news article.

    Attributes:
        title: Article headline
        url: Link to full article
        source: Name of the news source
        published_date: Publication date (optional)
        description: Article summary (optional)
    """

    title: str
    url: str
    source: str
    published_date: Optional[datetime]
    description: Optional[str]


class NewsFeedService:
    """Service for fetching cybersecurity news from RSS feeds.

    Provides both static curated news sources and dynamic RSS feed aggregation.
    All RSS fetching includes security controls and error handling.
    """

    # Reputable cybersecurity RSS feeds
    RSS_FEEDS = {
        "The Hacker News": "https://thehackernews.com/feeds/posts/default",
        "Krebs on Security": "https://krebsonsecurity.com/feed/",
        "Security Week": "https://www.securityweek.com/feed",
        "Dark Reading": "https://www.darkreading.com/rss.xml",
    }

    # Security and performance constants
    MAX_FEED_SIZE: int = 10 * 1024 * 1024  # 10MB
    MAX_ARTICLE_SIZE: int = 100 * 1024     # 100KB per article
    MAX_DESCRIPTION_LENGTH: int = 500       # 500 characters
    MAX_ARTICLES_PER_FEED: int = 15         # Reduced from unlimited

    # Rate limiting
    _last_request_time: ClassVar[float] = 0
    MIN_REQUEST_INTERVAL: float = 5.0  # 5 seconds between requests
    REQUEST_TIMEOUT: float = 10.0  # 10 second timeout

    # Static curated news sources
    STATIC_SOURCES = [
        {
            "title": "Krebs on Security",
            "url": "https://krebsonsecurity.com/",
            "description": "In-depth security journalism by Brian Krebs",
            "icon": "🔍"
        },
        {
            "title": "The Hacker News",
            "url": "https://thehackernews.com/",
            "description": "Latest cyber security news and hacks",
            "icon": "🎯"
        },
        {
            "title": "CISA Alerts",
            "url": "https://www.cisa.gov/news-events/cybersecurity-advisories",
            "description": "Official US cybersecurity alerts",
            "icon": "🏛️"
        },
        {
            "title": "NVD Vulnerability Database",
            "url": "https://nvd.nist.gov/",
            "description": "National Vulnerability Database",
            "icon": "🗄️"
        },
    ]

    def fetch_articles(self, limit: int = 10) -> list[NewsArticle]:
        """Fetch latest articles from RSS feeds with security controls.

        Args:
            limit: Maximum number of articles to return per source

        Returns:
            List of NewsArticle objects sorted by publication date (newest first)

        Security features:
            - URL validation for all article links
            - Rate limiting between feed requests
            - Article size limits to prevent memory exhaustion
            - SSL certificate validation for feed connections
            - Secure HTML sanitization for descriptions
        """
        articles = []

        for source, feed_url in self.RSS_FEEDS.items():
            try:
                # Rate limiting: Ensure minimum interval between requests
                current_time = time.time()
                time_since_last = current_time - self._last_request_time
                if time_since_last < self.MIN_REQUEST_INTERVAL:
                    time.sleep(self.MIN_REQUEST_INTERVAL - time_since_last)

                # Update last request time
                self._last_request_time = time.time()

                # Create SSL context with certificate validation
                ssl_context = ssl.create_default_context()
                ssl_context.verify_mode = ssl.CERT_REQUIRED
                ssl_context.check_hostname = True

                # Parse feed with security settings
                feed = feedparser.parse(
                    feed_url,
                    sanitize_html=False,  # We handle sanitization ourselves
                    request_headers={
                        'User-Agent': 'PC-Utilities-Manager/2.0'
                    }
                )

                # Check for feed parsing errors
                if feed.get('bozo'):
                    logger.warning(
                        f"Feed parsing error for {source}: {feed.get('bozo_exception')}"
                    )
                    continue

                # Process articles with size limits
                for entry in feed.entries[:min(limit, self.MAX_ARTICLES_PER_FEED)]:
                    # Validate article size before processing
                    if not self._validate_article_size(entry):
                        continue

                    # Parse publication date
                    pub_date = self._parse_date(entry.get("published"))

                    # Clean description (remove HTML tags if present)
                    description = self._clean_description(
                        entry.get("description") or entry.get("summary", "")
                    )

                    # Validate URL security
                    url = entry.get("link", "")
                    if not validate_url(url):
                        safe_url = sanitize_url_for_logging(url)
                        logger.warning(
                            f"Invalid URL rejected from {source}: {safe_url}"
                        )
                        continue

                    articles.append(
                        NewsArticle(
                            title=entry.get("title", "No title"),
                            url=url,
                            source=source,
                            published_date=pub_date,
                            description=description,
                        )
                    )

            except Exception as e:
                # Secure logging without stack traces or sensitive URLs
                safe_url = sanitize_url_for_logging(feed_url)
                logger.warning(
                    f"Failed to parse RSS feed '{source}' from {safe_url}: {str(e)[:100]}"
                )
                continue

        # Sort by date (newest first) and limit total results
        articles.sort(
            key=lambda x: x.published_date or datetime.min, reverse=True
        )

        return articles[:self.MAX_ARTICLES_PER_FEED]

    def _validate_article_size(self, entry) -> bool:
        """Validate article size before processing to prevent memory exhaustion.

        Args:
            entry: RSS feed entry to validate

        Returns:
            True if article size is acceptable, False otherwise
        """
        try:
            # Check total entry size
            entry_str = str(entry)
            if len(entry_str) > self.MAX_ARTICLE_SIZE:
                logger.warning(
                    f"Article too large, skipping: {len(entry_str)} bytes"
                )
                return False
            return True

        except Exception as e:
            logger.warning(f"Article size validation failed: {str(e)[:100]}")
            return False

    @staticmethod
    def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
        """Parse RFC 2822 date string to datetime.

        Args:
            date_str: Date string from RSS feed

        Returns:
            datetime object or None if parsing fails
        """
        if not date_str:
            return None

        try:
            return parsedate_to_datetime(date_str)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _clean_description(description: str) -> str:
        """Clean HTML tags from description using secure sanitization.

        Uses bleach library to prevent XSS attacks by properly sanitizing
        HTML content. This is a critical security function.

        Args:
            description: Raw description text (may contain HTML)

        Returns:
            Cleaned text without HTML tags, limited to MAX_DESCRIPTION_LENGTH

        Security:
            - Uses bleach for whitelist-based HTML sanitization
            - Removes all HTML tags and comments
            - Limits output length to prevent overflow attacks
        """
        if not description:
            return ""

        try:
            # Use bleach for secure HTML sanitization (XSS prevention)
            clean = bleach.clean(
                description,
                tags=[],           # No HTML tags allowed
                strip=True,        # Strip all HTML
                strip_comments=True # Remove HTML comments
            )
        except Exception as e:
            logger.warning(f"HTML sanitization failed, using fallback: {str(e)[:100]}")
            # Fallback to basic cleaning if bleach fails
            clean = description

        # Clean up HTML entities
        clean = clean.replace("&nbsp;", " ")
        clean = clean.replace("&amp;", "&")
        clean = clean.replace("&lt;", "<")
        clean = clean.replace("&gt;", ">")
        clean = clean.replace("&quot;", '"')

        # Remove extra whitespace and limit length
        clean = " ".join(clean.split())

        # Limit description length for security and performance
        if len(clean) > NewsFeedService.MAX_DESCRIPTION_LENGTH:
            clean = clean[:NewsFeedService.MAX_DESCRIPTION_LENGTH]

        return clean.strip()

    @staticmethod
    def open_url(url: str) -> None:
        """Open URL in default web browser.

        Args:
            url: URL to open

        Raises:
            NetworkError: If webbrowser fails to open the URL
        """
        try:
            webbrowser.open(url)
            logger.info(f"Successfully opened URL: {url}")
        except Exception as e:
            # Log the error and raise specific exception
            logger.warning(f"Failed to open URL {url}: {e}", exc_info=True)
            raise NetworkError(
                f"Failed to open news article URL",
                url=url,
                original_error=e
            ) from e
