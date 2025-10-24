from __future__ import annotations

from models import Message
from observers import Observer


class InformPolisObserver(Observer):
    def update(self, message: Message) -> None:
        print(
            f"Информ полис получил информацию: {message.text}, {message.date.isoformat()}, {message.message_type}"
        )


class ArigUsObserver(Observer):
    def update(self, message: Message) -> None:
        print(
            f"Ариг Ус получил информацию: {message.text}, {message.date.isoformat()}, {message.message_type}"
        )
