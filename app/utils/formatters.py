from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal


def format_currency(value: Decimal | float | int) -> str:
    decimal_value = Decimal(str(value)).quantize(Decimal("0.01"))
    formatted = f"{decimal_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{formatted} EUR"


def format_date(value: date | datetime | None) -> str:
    if value is None:
        return "-"
    if isinstance(value, datetime):
        return value.strftime("%d.%m.%Y %H:%M")
    return value.strftime("%d.%m.%Y")
