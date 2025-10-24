from __future__ import annotations

import argparse
from pathlib import Path

from news_agency import NewsAgency
from observers import InformPolisObserver, ArigUsObserver


def main() -> None:
    parser = argparse.ArgumentParser(description="Ulan-Ude news agency notifier")
    parser.add_argument(
        "--file",
        type=str,
        default="messages.txt",
        help="Path to messages file (default: messages.txt)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=5.0,
        help="Delay between messages in seconds (default: 5.0)",
    )
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"Messages file not found: {path}")

    agency = NewsAgency()
    agency.register_observer(InformPolisObserver())
    agency.register_observer(ArigUsObserver())

    agency.publish_from_file(str(path), delay_seconds=args.delay)


if __name__ == "__main__":
    main()
