"""Tests for the news feed worker thread.

Uses a fake ``NewsFeedService`` so no test touches the real network.
"""

import threading
from typing import Any

import pytest

from features.ui.news_feed_service import NewsArticle
from features.ui.news_feed_worker import NewsFeedWorker


def make_article(title: str = "Article") -> NewsArticle:
    """Build a canned article for worker tests."""
    return NewsArticle(
        title=title,
        url="https://example.com/article",
        source="Test Source",
        published_date=None,
        description="A description",
    )


class FakeFeedService:
    """Stand-in for ``NewsFeedService`` with configurable results."""

    def __init__(
        self,
        articles: list[NewsArticle] | None = None,
        error: Exception | None = None,
    ):
        self.articles = articles if articles is not None else []
        self.error = error
        self.calls: list[int] = []
        self.should_stop = None
        self.should_stop_result: bool | None = None

    def fetch_articles(self, limit: int = 10, should_stop=None) -> list[NewsArticle]:
        """Return the canned result, recording the limit and probe."""
        self.calls.append(limit)
        self.should_stop = should_stop
        self.should_stop_result = should_stop() if callable(should_stop) else None
        if self.error:
            raise self.error
        return self.articles


@pytest.fixture
def app_thread() -> threading.Thread:
    """Provide the Python thread running the Qt event loop."""
    return threading.main_thread()


class TestNewsFeedWorker:
    """Tests for signal emission and threading behavior."""

    def test_worker_emits_articles_ready(self, qtbot):
        """A successful fetch emits the article list exactly once."""
        service = FakeFeedService(articles=[make_article("A1"), make_article("A2")])
        worker = NewsFeedWorker(service, limit=15)
        emitted: list[Any] = []
        worker.articles_ready.connect(emitted.append)

        with qtbot.wait_signals([worker.articles_ready, worker.finished], timeout=5000):
            worker.start()

        assert len(emitted) == 1
        assert [a.title for a in emitted[0]] == ["A1", "A2"]

    def test_worker_emits_empty_list(self, qtbot):
        """An empty result still emits articles_ready with an empty list."""
        worker = NewsFeedWorker(FakeFeedService(articles=[]), limit=15)
        emitted: list[Any] = []
        worker.articles_ready.connect(emitted.append)

        with qtbot.wait_signals([worker.articles_ready, worker.finished], timeout=5000):
            worker.start()

        assert emitted == [[]]

    def test_worker_emits_fetch_failed(self, qtbot):
        """A raising service emits fetch_failed and never articles_ready."""
        worker = NewsFeedWorker(FakeFeedService(error=RuntimeError("boom")), limit=15)
        emitted: list[tuple[str, Any]] = []
        worker.articles_ready.connect(lambda a: emitted.append(("articles", a)))
        worker.fetch_failed.connect(lambda m: emitted.append(("failed", m)))

        with qtbot.wait_signals([worker.fetch_failed, worker.finished], timeout=5000):
            worker.start()

        assert len(emitted) == 1
        assert emitted[0][0] == "failed"
        assert "boom" in emitted[0][1]

    def test_worker_passes_limit_to_service(self, qtbot):
        """The configured limit is forwarded to the service call."""
        service = FakeFeedService(articles=[])
        worker = NewsFeedWorker(service, limit=7)

        with qtbot.wait_signals([worker.articles_ready, worker.finished], timeout=5000):
            worker.start()

        assert service.calls == [7]

    def test_interrupting_mid_fetch_flips_the_probe(self, qtbot):
        """Requesting interruption mid-fetch turns the service's probe true.

        The fake service records the probe before and after a blocking wait,
        so this exercises the real shutdown path: interrupt while a fetch is
        in flight, and the service observes it between feeds. (Qt clears the
        interruption flag when a thread starts, so pre-start requests don't
        count — mid-run requests are the ones that matter.)
        """
        release = threading.Event()

        class BlockingFeedService(FakeFeedService):
            """Fake service that pauses mid-fetch on an event."""

            def __init__(self):
                super().__init__(articles=[])
                self.probe_before = None
                self.probe_after = None

            def fetch_articles(self, limit: int = 10, should_stop=None):
                self.calls.append(limit)
                self.probe_before = should_stop() if callable(should_stop) else None
                release.wait(timeout=5000)
                self.probe_after = should_stop() if callable(should_stop) else None
                return self.articles

        service = BlockingFeedService()
        worker = NewsFeedWorker(service, limit=15)
        worker.start()

        qtbot.wait_until(lambda: service.probe_before is not None)
        assert service.probe_before is False

        worker.requestInterruption()
        release.set()

        qtbot.wait_until(worker.isFinished)
        assert service.probe_after is True

    def test_signal_lands_on_gui_thread(self, qtbot, app_thread):
        """Cross-thread signals must be delivered on the main thread."""
        worker = NewsFeedWorker(FakeFeedService(articles=[make_article()]), limit=15)
        seen_threads: list[threading.Thread] = []
        worker.articles_ready.connect(lambda _: seen_threads.append(threading.current_thread()))

        with qtbot.wait_signals([worker.articles_ready, worker.finished], timeout=5000):
            worker.start()

        assert seen_threads == [app_thread]
