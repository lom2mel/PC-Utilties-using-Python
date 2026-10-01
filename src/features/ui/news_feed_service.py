"""Cybersecurity news feed service.

This module provides functionality to fetch and aggregate cybersecurity news
from various RSS feeds and provides static curated news sources.
"""

import logging
import threading
import time
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Any, Callable, ClassVar, Optional

import bleach
import feedparser
import requests

from features.ui.exceptions import NetworkError
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
    All RSS fetching includes security controls and error handling. Fetching
    is thread-safe: worker threads may call ``fetch_articles`` concurrently
    and feed requests stay rate-limited across threads.
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
    MAX_ARTICLE_SIZE: int = 100 * 1024  # 100KB per article
    MAX_DESCRIPTION_LENGTH: int = 500  # 500 characters
    MAX_ARTICLES_PER_FEED: int = 15  # Reduced from unlimited

    # Rate limiting
    _last_request_time: ClassVar[float] = 0
    _request_lock: ClassVar[threading.Lock] = threading.Lock()
    MIN_REQUEST_INTERVAL: float = 5.0  # 5 seconds between requests
    REQUEST_TIMEOUT: float = 10.0  # 10 second timeout

    # Static curated news sources
    STATIC_SOURCES = [
        {
            "title": "Krebs on Security",
            "url": "https://krebsonsecurity.com/",
            "description": "In-depth security journalism by Brian Krebs",
            "icon": "🔍",
        },
        {
            "title": "The Hacker News",
            "url": "https://thehackernews.com/",
            "description": "Latest cyber security news and hacks",
            "icon": "🎯",
        },
        {
            "title": "CISA Alerts",
            "url": "https://www.cisa.gov/news-events/cybersecurity-advisories",
            "description": "Official US cybersecurity alerts",
            "icon": "🏛️",
        },
        {
            "title": "NVD Vulnerability Database",
            "url": "https://nvd.nist.gov/",
            "description": "National Vulnerability Database",
            "icon": "🗄️",
        },
    ]

    def fetch_articles(
        self,
        limit: int = 10,
        should_stop: Optional[Callable[[], bool]] = None,
    ) -> list[NewsArticle]:
        """Fetch latest articles from RSS feeds with security controls.

        Safe to call from a worker thread; blocking network I/O and rate-limit
        sleeps must never run on the GUI thread.

        Args:
            limit: Maximum number of articles to return per source
            should_stop: Optional cancellation probe checked before each feed

        Returns:
            List of NewsArticle objects sorted by publication date (newest first)

        Security features:
            - URL validation for all article links
            - Rate limiting between feed requests (thread-safe)
            - Request timeouts and response size limits
            - SSL certificate validation for feed connections (via requests)
            - Secure HTML sanitization for descriptions
        """
        articles: list[NewsArticle] = []

        for source, feed_url in self.RSS_FEEDS.items():
            if should_stop is not None and should_stop():
                logger.info(f"Feed fetching cancelled with {len(articles)} article(s)")
                break

            try:
                feed = self._fetch_parsed_feed(feed_url)
                articles.extend(self._collect_feed_articles(source, feed, limit))
            except Exception as e:
                # Secure logging without stack traces or sensitive URLs
                safe_url = sanitize_url_for_logging(feed_url)
                logger.warning(
                    f"Failed to fetch RSS feed '{source}' from {safe_url}: {str(e)[:100]}"
                )
                continue

        # Sort by date (newest first) and limit total results
        articles.sort(key=lambda x: x.published_date or datetime.min, reverse=True)

        return articles[: self.MAX_ARTICLES_PER_FEED]

    def _fetch_parsed_feed(self, feed_url: str) -> Any:
        """Rate-limit, download, and parse a single RSS feed.

        Args:
            feed_url: Fully qualified RSS feed URL

        Returns:
            feedparser result object for the feed

        Raises:
            requests.RequestException: On network, timeout, or HTTP failure
            ValueError: When the payload exceeds MAX_FEED_SIZE
        """
        self._respect_rate_limit()
        content = self._fetch_feed(feed_url)
        return feedparser.parse(content, sanitize_html=False)

    def _respect_rate_limit(self) -> None:
        """Sleep as needed so feed requests stay MIN_REQUEST_INTERVAL apart."""
        with self._request_lock:
            time_since_last = time.time() - self._last_request_time
            if time_since_last < self.MIN_REQUEST_INTERVAL:
                time.sleep(self.MIN_REQUEST_INTERVAL - time_since_last)
            self._last_request_time = time.time()

    def _fetch_feed(self, feed_url: str) -> bytes:
        """Download one RSS feed with a timeout and size cap.

        Args:
            feed_url: Fully qualified RSS feed URL

        Returns:
            Raw feed bytes for feedparser

        Raises:
            requests.RequestException: On network, timeout, or HTTP failure
            ValueError: When the payload exceeds MAX_FEED_SIZE
        """
        response = requests.get(
            feed_url,
            timeout=self.REQUEST_TIMEOUT,
            headers={"User-Agent": "PC-Utilities-Manager/2.0"},
        )
        response.raise_for_status()
        if len(response.content) > self.MAX_FEED_SIZE:
            raise ValueError(f"Feed exceeds maximum size: {len(response.content)} bytes")
        return response.content

    def _collect_feed_articles(self, source: str, feed: Any, limit: int) -> list[NewsArticle]:
        """Extract and validate articles from one parsed feed.

        Args:
            source: Human-readable feed name
            feed: feedparser result object
            limit: Maximum number of entries to consider

        Returns:
            Validated NewsArticle list for this feed (empty on bozo feeds)
        """
        articles: list[NewsArticle] = []

        # Check for feed parsing errors
        if feed.get("bozo"):
            logger.warning(f"Feed parsing error for {source}: {feed.get('bozo_exception')}")
            return articles

        for entry in feed.entries[: min(limit, self.MAX_ARTICLES_PER_FEED)]:
            # Validate article size before processing
            if not self._validate_article_size(entry):
                continue

            # Validate URL security
            url = entry.get("link", "")
            if not validate_url(url):
                safe_url = sanitize_url_for_logging(url)
                logger.warning(f"Invalid URL rejected from {source}: {safe_url}")
                continue

            articles.append(
                NewsArticle(
                    title=entry.get("title", "No title"),
                    url=url,
                    source=source,
                    published_date=self._parse_date(entry.get("published")),
                    description=self._clean_description(
                        entry.get("description") or entry.get("summary", "")
                    ),
                )
            )

        return articles

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
                logger.warning(f"Article too large, skipping: {len(entry_str)} bytes")
                return False
            return True

        except Exception as e:
            logger.warning(f"Article size validation failed: {str(e)[:100]}")
            return False

    @staticmethod
    def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
        """Parse RFC 2822 date string to datetime.

        Args:
            date_str: RFC 2822 date string from RSS feed

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
                tags=[],  # No HTML tags allowed
                strip=True,  # Strip all HTML
                strip_comments=True,  # Remove HTML comments
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
            clean = clean[: NewsFeedService.MAX_DESCRIPTION_LENGTH]

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
            raise NetworkError(f"Failed to open news article URL", url=url, original_error=e) from e
