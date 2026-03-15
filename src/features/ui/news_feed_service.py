"""Cybersecurity news feed service.

This module provides functionality to fetch and aggregate cybersecurity news
from various RSS feeds and provides static curated news sources.
"""

import webbrowser
from dataclasses import dataclass
from datetime import datetime, UTC
from email.utils import parsedate_to_datetime
from typing import Optional

import feedparser

from features.ui.design_system import COLORS


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
    All RSS fetching includes error handling to prevent UI freezing.
    """

    # Reputable cybersecurity RSS feeds
    RSS_FEEDS = {
        "The Hacker News": "https://thehackernews.com/feeds/posts/default",
        "Krebs on Security": "https://krebsonsecurity.com/feed/",
        "Security Week": "https://www.securityweek.com/feed",
        "Dark Reading": "https://www.darkreading.com/rss.xml",
    }

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
        """Fetch latest articles from RSS feeds.

        Args:
            limit: Maximum number of articles to return per source

        Returns:
            List of NewsArticle objects sorted by publication date (newest first)
        """
        articles = []

        for source, feed_url in self.RSS_FEEDS.items():
            try:
                feed = feedparser.parse(feed_url)

                for entry in feed.entries[:limit]:
                    # Parse publication date
                    pub_date = self._parse_date(entry.get("published"))

                    # Clean description (remove HTML tags if present)
                    description = self._clean_description(
                        entry.get("description") or entry.get("summary", "")
                    )

                    articles.append(
                        NewsArticle(
                            title=entry.get("title", "No title"),
                            url=entry.get("link", ""),
                            source=source,
                            published_date=pub_date,
                            description=description[:200] if description else None,
                        )
                    )
            except Exception:
                # Silently skip failed feeds to prevent UI issues
                continue

        # Sort by date (newest first) and limit total results
        articles.sort(
            key=lambda x: x.published_date or datetime.min, reverse=True
        )

        return articles[:15]  # Return top 15 articles total

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
        """Clean HTML tags from description.

        Args:
            description: Raw description text (may contain HTML)

        Returns:
            Cleaned text without HTML tags
        """
        # Simple HTML tag removal
        import re

        clean = re.sub(r"<[^>]+>", "", description)
        clean = re.sub(r"&nbsp;", " ", clean)
        clean = re.sub(r"&amp;", "&", clean)
        clean = re.sub(r"&lt;", "<", clean)
        clean = re.sub(r"&gt;", ">", clean)
        clean = re.sub(r"&quot;", '"', clean)

        # Remove extra whitespace
        clean = re.sub(r"\s+", " ", clean).strip()

        return clean

    @staticmethod
    def open_url(url: str) -> None:
        """Open URL in default web browser.

        Args:
            url: URL to open
        """
        try:
            webbrowser.open(url)
        except Exception as e:
            # Silently fail - UI will handle feedback
            pass
