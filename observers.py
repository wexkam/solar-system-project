from __future__ import annotations

from typing import Final

from news_agency import AgencyMessage, Observer


class InformPolisObserver:
    NAME: Final[str] = "Информ полис"

    def update(self, message: AgencyMessage) -> None:
        print(f"{self.NAME} получил информацию: {message.text}, {message.date}, {message.message_type}")


class ArigUsObserver:
    NAME: Final[str] = "Ариг Ус"

    def update(self, message: AgencyMessage) -> None:
        print(f"{self.NAME} получил информацию: {message.text}, {message.date}, {message.message_type}")
