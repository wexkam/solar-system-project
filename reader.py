from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Iterable

from models import Message
from observers import InfoAgency


def parse_message_line(line: str) -> Message:
    # Expected format: <text> ; <YYYY-mm-dd> ; <type>
    parts = [p.strip() for p in line.strip().split(";")]
    if len(parts) != 3:
        raise ValueError(f"Invalid message line: {line!r}")
    text, date_str, type_str = parts
    message_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    message_type = int(type_str)
    return Message(text=text, date=message_date, message_type=message_type)


def read_messages_with_delay(file_path: str | Path, agency: InfoAgency, delay_seconds: int = 5) -> None:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            message = parse_message_line(line)
            agency.notify(message)
            time.sleep(delay_seconds)
