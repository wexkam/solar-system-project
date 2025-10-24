from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, List

from models import Message


class Observer(ABC):
    @abstractmethod
    def update(self, message: Message) -> None:
        """Receive an update with a new message."""
        raise NotImplementedError


class Subject(Protocol):
    def attach(self, observer: Observer) -> None: ...
    def detach(self, observer: Observer) -> None: ...
    def notify(self, message: Message) -> None: ...


class InfoAgency(Subject):
    """Subject that holds a list of observers and notifies them."""

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, message: Message) -> None:
        for observer in list(self._observers):
            observer.update(message)
