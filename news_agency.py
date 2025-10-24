from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from threading import RLock
from time import sleep
from typing import Iterable, List, Protocol, Optional


@dataclass(frozen=True)
class AgencyMessage:
    """Represents a single agency message unit.

    Attributes:
        text: Raw message text (free-form).
        date: Date in YYYY-mm-dd format.
        message_type: Integer type id (1=weather, 2=currency, 3=city news).
    """

    text: str
    date: str
    message_type: int

    def __post_init__(self) -> None:
        # Validate date format early to surface errors near the source.
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError(f"Invalid date format, expected YYYY-mm-dd, got: {self.date}") from exc

        if not isinstance(self.message_type, int):
            raise TypeError("message_type must be int")
        if self.message_type not in (1, 2, 3):
            # Keep it permissive but clear; allow extension by clients later if needed
            # For now restrict to the three known types per task requirements.
            raise ValueError(
                f"Unsupported message_type: {self.message_type}. Expected one of (1, 2, 3)."
            )


class Observer(Protocol):
    """Observer interface for receiving agency messages."""

    def update(self, message: AgencyMessage) -> None:
        ...


class NewsAgency:
    """Subject that manages observers and publishes messages to them.

    - Allows registering/unregistering observers at runtime
    - Notifies all current observers for each new message
    - Can publish messages read from a file with a delay between entries
    """

    def __init__(self) -> None:
        self._observers: List[Observer] = []
        self._lock = RLock()

    def register_observer(self, observer: Observer) -> None:
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)

    def unregister_observer(self, observer: Observer) -> None:
        with self._lock:
            try:
                self._observers.remove(observer)
            except ValueError:
                # Silently ignore if not present; idempotent removal
                pass

    def notify_observers(self, message: AgencyMessage) -> None:
        # Copy to avoid mutation issues during iteration
        with self._lock:
            current_observers = list(self._observers)
        for observer in current_observers:
            try:
                observer.update(message)
            except Exception:
                # Observers are isolated; a faulty observer must not break the flow
                # In production we would log this.
                continue

    @staticmethod
    def _parse_line_to_message(line: str) -> Optional[AgencyMessage]:
        """Parse a single line of the form: "<text>; <date>; <type>".

        Returns None for empty/comment lines.
        Raises ValueError for structurally invalid lines.
        """
        raw = line.strip()
        if not raw:
            return None
        if raw.startswith("#"):
            return None

        parts = [p.strip() for p in raw.split(";")]
        if len(parts) != 3:
            raise ValueError(
                f"Invalid line format (expected 3 semicolon-separated parts): {line!r}"
            )

        text, date_str, type_str = parts
        try:
            message_type = int(type_str)
        except ValueError as exc:
            raise ValueError(f"Invalid message type (must be int): {type_str!r}") from exc

        return AgencyMessage(text=text, date=date_str, message_type=message_type)

    def publish_from_file(self, file_path: str, delay_seconds: float = 5.0) -> None:
        """Read messages from a text file and notify observers with delay.

        Each line must be in the format: "<text>; <YYYY-mm-dd>; <type>".
        There is a delay of `delay_seconds` between processing consecutive lines.
        """
        with open(file_path, "r", encoding="utf-8") as fh:
            first_emitted = False
            for raw_line in fh:
                try:
                    message = self._parse_line_to_message(raw_line)
                except Exception:
                    # Skip malformed lines; in a real system we would log this.
                    message = None

                if message is None:
                    # empty/comment/invalid
                    continue

                # Sleep before notifying for every message after the first one
                if first_emitted:
                    sleep(delay_seconds)

                self.notify_observers(message)

                if not first_emitted:
                    first_emitted = True

    def publish(self, messages: Iterable[AgencyMessage], delay_seconds: float = 5.0) -> None:
        """Publish an in-memory iterable of messages with delay between them."""
        iterator = iter(messages)
        first = True
        for msg in iterator:
            if not first:
                sleep(delay_seconds)
            self.notify_observers(msg)
            if first:
                first = False
