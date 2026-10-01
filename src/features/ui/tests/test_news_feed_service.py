"""Tests for the news feed service network layer.

All network I/O is faked: ``requests.get`` and ``feedparser.parse`` are
monkeypatched, so no test in this module touches the real network.
"""

from typing import Any

import pytest
import requests

import features.ui.news_feed_service as news_feed_service_module
from features.ui.news_feed_service import NewsFeedService

USER_AGENT = "PC-Utilities-Manager/2.0"
HTTP_CLIENT_ERROR = 400


class FakeResponse:
    """Minimal stand-in for ``requests.Response``."""

    def __init__(self, content: bytes = b"<rss></rss>", status_code: int = 200):
        self.content = content
        self.status_code = status_code

    def raise_for_status(self) -> None:
        """Raise ``requests.HTTPError`` for non-2xx statuses."""
        if self.status_code >= HTTP_CLIENT_ERROR:
            raise requests.HTTPError(f"HTTP {self.status_code}")


def make_entry(**overrides: Any) -> dict[str, Any]:
    """Build a minimal RSS entry dict as feedparser would produce."""
    entry: dict[str, Any] = {
        "title": "Test Article",
        "link": "https://example.com/article",
        "published": "Tue, 01 Jul 2025 10:00:00 +0000",
        "description": "<p>Clean text</p>",
    }
    entry.update(overrides)
    return entry


class FakeFeed(dict):
    """Dict that also exposes keys as attributes, like feedparser's result."""

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc


def make_feed(entries: list[dict[str, Any]] | None = None, bozo: bool = False) -> FakeFeed:
    """Build a minimal feedparser result stand-in."""
    return FakeFeed(
        bozo=bozo,
        bozo_exception="not xml" if bozo else "",
        entries=entries if entries is not None else [],
    )


@pytest.fixture(autouse=True)
def fast_rate_limit(monkeypatch: pytest.MonkeyPatch):
    """Disable rate-limit pacing and reset limiter state for fast tests."""
    monkeypatch.setattr(NewsFeedService, "MIN_REQUEST_INTERVAL", 0.0)
    monkeypatch.setattr(NewsFeedService, "_last_request_time", 0.0)


@pytest.fixture
def fake_get(monkeypatch: pytest.MonkeyPatch):
    """Patch the service's ``requests.get`` and record every call.

    The returned callable exposes ``calls`` (recorded requests) and
    ``responses`` (per-URL canned ``FakeResponse`` or ``Exception``).
    """
    calls: list[dict[str, Any]] = []
    responses: dict[str, FakeResponse | Exception] = {}

    def _get(url: str, **kwargs: Any) -> FakeResponse:
        calls.append({"url": url, **kwargs})
        response = responses.get(url, FakeResponse())
        if isinstance(response, Exception):
            raise response
        return response

    _get.calls = calls  # type: ignore[attr-defined]
    _get.responses = responses  # type: ignore[attr-defined]
    monkeypatch.setattr(news_feed_service_module.requests, "get", _get)
    return _get


@pytest.fixture
def fake_parse(monkeypatch: pytest.MonkeyPatch):
    """Patch the service's ``feedparser.parse``, record calls, allow result override."""
    recorded: dict[str, Any] = {
        "source": None,
        "kwargs": None,
        "result": make_feed(entries=[make_entry()]),
    }

    def _parse(source: Any, *_args: Any, **kwargs: Any) -> dict[str, Any]:
        recorded["source"] = source
        recorded["kwargs"] = kwargs
        return recorded["result"]

    monkeypatch.setattr(news_feed_service_module.feedparser, "parse", _parse)
    return recorded


class TestNewsFeedServiceFetching:
    """Tests for how feeds are downloaded and handed to feedparser."""

    @pytest.mark.usefixtures("fake_parse")
    def test_fetch_passes_request_timeout(self, fake_get):
        """Every feed request must carry REQUEST_TIMEOUT (regression: dead constant)."""
        articles = NewsFeedService().fetch_articles()

        assert articles is not None
        assert len(fake_get.calls) == len(NewsFeedService.RSS_FEEDS)
        assert all(call["timeout"] == NewsFeedService.REQUEST_TIMEOUT for call in fake_get.calls)

    @pytest.mark.usefixtures("fake_parse")
    def test_fetch_sends_user_agent(self, fake_get):
        """Feed requests must identify with the application user agent."""
        NewsFeedService().fetch_articles()

        assert all(call["headers"]["User-Agent"] == USER_AGENT for call in fake_get.calls)

    def test_feedparser_receives_bytes_not_url(self, fake_get, fake_parse):
        """feedparser must parse pre-fetched bytes so the timeout is effective."""
        feed_url = next(iter(NewsFeedService.RSS_FEEDS.values()))
        fake_get.responses[feed_url] = FakeResponse(content=b"<rss><channel/></rss>")

        NewsFeedService().fetch_articles()

        assert isinstance(fake_parse["source"], bytes)

    @pytest.mark.usefixtures("fake_get", "fake_parse")
    def test_fetch_returns_parsed_articles(self):
        """A healthy feed yields sanitized NewsArticle objects."""
        articles = NewsFeedService().fetch_articles()

        # The fake parse result is returned once per configured feed
        assert len(articles) == len(NewsFeedService.RSS_FEEDS)
        article = articles[0]
        assert article.title == "Test Article"
        assert article.url == "https://example.com/article"
        assert article.description == "Clean text"

    @pytest.mark.usefixtures("fake_parse")
    def test_http_error_yields_empty_list(self, fake_get):
        """An HTTP failure on every feed skips them instead of raising."""
        for url in NewsFeedService.RSS_FEEDS.values():
            fake_get.responses[url] = FakeResponse(status_code=403)

        assert NewsFeedService().fetch_articles() == []

    @pytest.mark.usefixtures("fake_parse")
    def test_oversized_feed_is_skipped(self, fake_get):
        """A payload above MAX_FEED_SIZE is rejected before parsing."""
        oversized = b"x" * (NewsFeedService.MAX_FEED_SIZE + 1)
        for url in NewsFeedService.RSS_FEEDS.values():
            fake_get.responses[url] = FakeResponse(content=oversized)

        assert NewsFeedService().fetch_articles() == []

    @pytest.mark.usefixtures("fake_get")
    def test_garbage_xml_yields_empty_list(self, fake_parse):
        """A bozo feed with no usable entries contributes no articles."""
        fake_parse["result"] = make_feed(bozo=True)

        assert NewsFeedService().fetch_articles() == []

    @pytest.mark.usefixtures("fake_parse")
    def test_one_failed_feed_does_not_block_others(self, fake_get):
        """A failing feed is skipped; the remaining feeds still produce articles."""
        failing_name, failing_url = next(iter(NewsFeedService.RSS_FEEDS.items()))
        fake_get.responses[failing_url] = requests.ConnectionError("boom")

        articles = NewsFeedService().fetch_articles()

        other_sources = set(NewsFeedService.RSS_FEEDS) - {failing_name}
        assert len(articles) == len(NewsFeedService.RSS_FEEDS) - 1
        assert all(article.source in other_sources for article in articles)

    @pytest.mark.usefixtures("fake_parse")
    def test_should_stop_cancels_remaining_feeds(self, fake_get):
        """A true cancellation probe stops requests after the current feed."""

        def stop_after_first() -> bool:
            return len(fake_get.calls) >= 1

        articles = NewsFeedService().fetch_articles(should_stop=stop_after_first)

        assert len(fake_get.calls) == 1
        assert len(articles) == 1
