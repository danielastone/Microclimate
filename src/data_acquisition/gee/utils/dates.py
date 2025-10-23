"""Date utilities shared across GEE pipelines."""

from __future__ import annotations

import datetime as _dt
from collections.abc import Iterator
from typing import Tuple


def daterange(start: _dt.date, end: _dt.date, step_days: int) -> Iterator[Tuple[_dt.date, _dt.date]]:
    """Yield sliding windows between ``start`` and ``end`` using ``step_days`` increments."""
    current = start
    delta = _dt.timedelta(days=step_days)
    while current < end:
        next_edge = current + delta
        yield current, min(next_edge, end)
        current = next_edge
