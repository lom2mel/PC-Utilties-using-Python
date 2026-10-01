"""Background worker that fetches RSS news off the GUI thread."""

import atexit
import logging
from typing import ClassVar

from PySide6.QtCore import QThread, Signal

from features.ui.news_feed_service import NewsFeedService

logger = logging.getLogger(__name__)


def _drain_live_workers_at_exit() -> None:
    """Interrupt and reap any live fetch threads before interpreter teardown.

    Without this, quitting the app mid-fetch destroys running QThread objects
    during module teardown and Windows reports a crash on exit. Interruption
    stops the fetch after the in-flight feed (bounded by REQUEST_TIMEOUT);
    the wait covers one last feed plus one rate-limit interval.
    """
    for worker in list(NewsFeedWorker._live):
        worker.requestInterruption()
    for worker in list(NewsFeedWorker._live):
        if not worker.wait(20000):
            logger.warning("A news feed worker did not stop within 20 s")


atexit.register(_drain_live_workers_at_exit)


class NewsFeedWorker(QThread):
    """Fetches RSS articles on a background thread.

    Follows the worker pattern used by the converter features
    (features.image_converter.worker, features.office_converter.worker),
    with one deliberate difference: no ``finished`` signal is defined, so
    the built-in ``QThread.finished`` stays available for cleanup.

    The class keeps every running worker in ``_live`` until its thread has
    finished, so the last Python reference can never drop — and PySide
    delete the C++ thread — while the thread is still running.

    Signals:
        articles_ready: Emitted exactly once with the fetched NewsArticle
            list (possibly empty).
        fetch_failed: Emitted exactly once with an error description when
            fetching raised; ``articles_ready`` is not emitted in that case.
    """

    articles_ready = Signal(list)
    fetch_failed = Signal(str)

    _live: ClassVar[set] = set()

    def __init__(self, service: NewsFeedService, limit: int, parent=None) -> None:
        """Initialize the worker.

        Args:
            service: News feed service used to fetch articles
            limit: Maximum number of articles to request
            parent: Optional Qt parent object
        """
        super().__init__(parent)
        self._service = service
        self._limit = limit
        self.finished.connect(self._unregister)
        NewsFeedWorker._live.add(self)

    def _unregister(self) -> None:
        """Drop the class-level reference once the thread has finished."""
        NewsFeedWorker._live.discard(self)

    def run(self) -> None:
        """Fetch articles and emit exactly one terminal signal.

        Catches every exception because an unhandled raise here would
        strand the calling tab's loading label forever. The service polls
        ``isInterruptionRequested`` between feeds so app shutdown is quick.
        """
        try:
            articles = self._service.fetch_articles(
                limit=self._limit,
                should_stop=self.isInterruptionRequested,
            )
        except Exception as e:
            logger.warning(f"News feed fetch failed: {str(e)[:200]}")
            self.fetch_failed.emit(str(e)[:200])
            return
        self.articles_ready.emit(articles)
