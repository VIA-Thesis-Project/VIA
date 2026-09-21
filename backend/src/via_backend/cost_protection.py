"""Request burst protection shared by HTTP adapters; no worker dependency."""

from __future__ import annotations

from collections.abc import Callable
from math import ceil
from threading import Lock
from time import monotonic


class RateLimitExceededError(Exception):
    def __init__(self, retry_after: int) -> None:
        super().__init__(f"Rate limit exceeded; retry after {retry_after} seconds.")
        self.retry_after = retry_after


class QuotaExceededError(Exception):
    def __init__(self, retry_after: int) -> None:
        super().__init__(f"Quota exceeded; retry after {retry_after} seconds.")
        self.retry_after = retry_after


class FixedWindowLimiter:
    """Atomic, process-local 60-second buckets with an injectable monotonic clock."""

    def __init__(self, clock: Callable[[], float] = monotonic) -> None:
        self._clock = clock
        self._lock = Lock()
        self._buckets: dict[tuple[str, str], tuple[float, int]] = {}

    def check(self, action: str, subject: str, limit: int) -> None:
        now = self._clock()
        key = (action, subject)
        with self._lock:
            start, count = self._buckets.get(key, (now, 0))
            if now - start >= 60:
                start, count = now, 0
            if count >= limit:
                raise RateLimitExceededError(max(1, ceil(60 - (now - start))))
            self._buckets[key] = (start, count + 1)
            # Remove expired buckets opportunistically without a background thread.
            if len(self._buckets) > 10_000:
                self._buckets = {
                    k: v for k, v in self._buckets.items() if now - v[0] < 60
                }
