from __future__ import annotations

from datetime import date


def parse_optional_date(text: str) -> date | None:
    text = text.strip()
    if not text:
        return None
    day, month, year = text.split(".")
    return date(int(year), int(month), int(day))
