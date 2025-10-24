from __future__ import annotations

from observers import InfoAgency
from concrete_observers import InformPolisObserver, ArigUsObserver
from reader import read_messages_with_delay


def main() -> None:
    agency = InfoAgency()
    inform_polis = InformPolisObserver()
    arig_us = ArigUsObserver()

    agency.attach(inform_polis)
    agency.attach(arig_us)

    # Read messages from a file with a 5-second delay between notifications
    read_messages_with_delay("messages.txt", agency, delay_seconds=5)


if __name__ == "__main__":
    main()
