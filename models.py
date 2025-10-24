from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Message:
    """Immutable message model.

    Attributes:
        text: Arbitrary message text, e.g., weather, currency, news.
        date: Message date in ISO format (YYYY-mm-dd).
        message_type: Integer type: 1-weather, 2-currency, 3-city news.
    """

    text: str
    date: date
    message_type: int
